from fastapi import FastAPI
from pydantic import BaseModel
from agents import create_crew
from tts_service import generate_audio_sync
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
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
@app.post("/generate")
def generate_podcast(request: TopicRequest):
    result = create_crew(request.topic)

    try:
        import json
        parsed = json.loads(result.raw)

        audio_path = generate_audio_sync(parsed["dialogue"])

        filename = audio_path.split("\\")[-1]  # Windows safe
        audio_url = f"http://localhost:8000/audio/{filename}"

        return {
            "dialogue": parsed["dialogue"],
            "audio_url": audio_url
        }

    except Exception as e:
        return {
            "error": "Failed to generate podcast",
            "details": str(e)
        }