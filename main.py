from fileinput import filename

from fastapi import FastAPI
from pydantic import BaseModel
from agents import create_crew
from tts_service import generate_audio_sync
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi import Request
import uuid
import asyncio
import json

app = FastAPI()
origins = [
    "http://localhost:5173",  # Vite default
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
class TopicRequest(BaseModel):
    topic: str
    

app.mount("/audio", StaticFiles(directory="audio"), name="audio")

# In-memory job store
jobs = {}

# Async job processor
async def process_job(job_id: str, topic: str, req: Request):
    jobs[job_id]["status"] = "processing"
    try:
        result = await asyncio.to_thread(create_crew, topic)
        parsed = json.loads(result.raw)
        audio_path = await asyncio.to_thread(generate_audio_sync, parsed["dialogue"])
        filename = audio_path.split("\\")[-1]
        base_url = str(req.base_url).rstrip("/")
        audio_url = f"{base_url}/audio/{filename}"
        jobs[job_id]["status"] = "completed"
        jobs[job_id]["result"] = {
            "dialogue": parsed["dialogue"],
            "audio_url": audio_url
        }
    except Exception as e:
        jobs[job_id]["status"] = "failed"
        jobs[job_id]["error"] = str(e)

# POST /generate: Start job, return job_id
@app.post("/generate")
async def generate_podcast(request: TopicRequest, req: Request):
    job_id = uuid.uuid4().hex
    jobs[job_id] = {
        "status": "queued",
        "topic": request.topic
    }
    asyncio.create_task(process_job(job_id, request.topic, req))
    return {"job_id": job_id}

# GET /status/{job_id}: Return job status
@app.get("/status/{job_id}")
async def get_status(job_id: str):
    job = jobs.get(job_id)
    if not job:
        return {"status": "not_found"}
    return {"status": job["status"]}


# GET /result/{job_id}: Return result if completed
@app.get("/result/{job_id}")
async def get_result(job_id: str):
    job = jobs.get(job_id)
    if not job:
        return {"error": "Job not found"}
    if job["status"] == "completed":
        return job["result"]
    elif job["status"] == "failed":
        return {"error": "Job failed", "details": job.get("error", "Unknown error")}
    else:
        return {"error": "Job not completed yet"}


# GET /podcasts: List all podcasts in audio folder with audio and random image
import os
@app.get("/podcasts")
async def list_podcasts():
    # Use Unsplash official random image endpoint
    image_api = "https://images.unsplash.com/photo-1506744038136-46273834b3fb?auto=format&fit=crop&w=400&q=80"
    audio_dir = "audio"
    podcasts = []
    for filename in os.listdir(audio_dir):
        if filename.endswith(".mp3"):
            job_id = filename.split("_")[-1].replace(".mp3", "")
            podcasts.append({
                "job_id": job_id,
                "filename": filename,
                "audio_url": f"http://localhost:8000/audio/{filename}",
                "image_url": image_api,
                "topic": jobs.get(job_id, {}).get("topic", "")
            })
    return {"podcasts": podcasts}