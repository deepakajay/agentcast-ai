from fastapi import FastAPI, Request
from pydantic import BaseModel
from agents import create_crew
from tts_service import generate_audio_sync
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os
import json

app = FastAPI()

origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "https://agentcast-e3wu9scki-deepakajays-projects.vercel.app",
    "https://agentcast-xi.vercel.app/"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

class TopicRequest(BaseModel):
    topic: str

# Ensure audio folder exists (important for Docker)
os.makedirs("audio", exist_ok=True)

app.mount("/audio", StaticFiles(directory="audio"), name="audio")


@app.post("/generate")
def generate_podcast(request: TopicRequest, req: Request):
    try:
        # Generate script
        result = create_crew(request.topic)
        parsed = json.loads(result.raw)

        # Generate audio
        audio_path = generate_audio_sync(parsed["dialogue"])

        # Extract filename safely
        filename = os.path.basename(audio_path)

        # Dynamically build base URL (works in local & production)
        base_url = str(req.base_url).rstrip("/")
        audio_url = f"{base_url}/audio/{filename}"

        return {
            "dialogue": parsed["dialogue"],
            "audio_url": audio_url
        }

    except Exception as e:
        return {
            "error": "Failed to generate podcast",
            "details": str(e)
        }