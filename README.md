<img width="1445" height="326" alt="mermaid-diagram (1)" src="https://github.com/user-attachments/assets/a296973b-9f46-4100-ad3e-74e46ba6211f" /><img width="1445" height="326" alt="mermaid-diagram (1)" src="https://github.com/user-attachments/assets/2d7b0538-d7fd-4c8c-aa9f-944d98d8b5cf" /><img width="3410" height="593" alt="mermaid-diagram" src="https://github.com/user-attachments/assets/921a0ae1-83f6-4031-a4f7-130b450b7749" /># 🎙️ AgentCast Backend  
### Turn Any Topic Into an AI Debate Podcast

AgentCast is an AI-powered backend that transforms any topic into a fully generated, two-speaker debate podcast — complete with Indian voice narration and intro music.

It combines **multi-agent AI orchestration**, **LLM intelligence**, and **text-to-speech audio generation** into one seamless pipeline.

---

## 🌍 What This Project Does

Send a request like:

```json
{
  "topic": "How AI agents work"
}
And the system will:

🧠 Plan the topic structure

🎭 Turn it into a fun two-person debate

🎙 Convert it into realistic Indian voice audio

🎵 Add intro music

🔗 Return a streamable podcast URL

🧠 How It Works (High-Level View)
User → API → 3 AI Agents → LLM → Script → TTS → Audio File → Public URL

🏗 Architecture Overview

Imagine this as a small production studio:

🎧 A listener sends a topic.

🧑‍💻 Three AI “writers” collaborate.

🤖 A powerful language model drafts the script.

🎙 Two voice actors perform it.

🎵 Intro music is added.

📡 The episode is published.

🖼 System Architecture Diagram
<img width="3410" height="593" alt="mermaid-diagram" src="https://github.com/user-attachments/assets/745aa08f-f78c-4148-a377-e6c83665e476" />
🤖 The Three-Agent System

AgentCast does not rely on a single AI call.
It uses three coordinated agents, each with a specific role.

1️⃣ Topic Planner Agent

Role: Break down the topic logically.

Creates structure

Organizes flow

Ensures clarity

Think of this as the outline writer.

2️⃣ Debate Podcast Creator Agent

Role: Turn outline into a lively debate.

Adds humor

Adds conversational fillers

Uses analogies

Keeps it engaging

Speakers:

🎙 Speaker A — Indian Female Voice

🎙 Speaker B — Indian Male Voice

This is where the magic happens.

3️⃣ JSON Formatter Agent

Role: Enforce structure.

Ensures final output is strict JSON:

{
  "dialogue": [
    { "speaker": "A", "text": "..." },
    { "speaker": "B", "text": "..." }
  ]
}

This guarantees clean downstream processing.

🔄 Async Job Architecture (Evolution)

During development, we implemented an in-memory background job queue to prevent blocking requests.

Why?

Generating:

LLM output

TTS audio

File assembly

Takes 20–40 seconds.

Blocking APIs don’t scale well.

🔁 Async Flow Model
POST /generate → returns job_id
GET /status/{job_id} → polling
GET /result/{job_id} → final result

Flow:

User clicks Generate
        ↓
Backend creates job
        ↓
Job runs in background
        ↓
Frontend polls status
        ↓
When completed → fetch result

For public deployment on free hosting (Render), the system uses a blocking model due to container restarts — but the async architecture is production-ready and documented.

🎧 Audio Processing Pipeline

Once script is ready:

🎵 Intro music is loaded

🎙 Speaker A audio is generated

🎙 Speaker B audio is generated

📦 All segments are concatenated

💾 Saved in /audio

🌐 Served via public URL

📦 Tech Stack
Layer	Technology
API	FastAPI
AI Orchestration	CrewAI
LLM Routing	LiteLLM
Model Provider	OpenRouter
TTS	edge-tts
Deployment	Render (Docker)
Frontend	React (Vercel)
🌐 Deployment Architecture
<img width="1445" height="326" alt="mermaid-diagram (1)" src="https://github.com/user-attachments/assets/8944b49c-3d20-42db-adee-9af9ee68a68a" />
🔐 Environment Variables

Required:

OPENROUTER_API_KEY=your_key_here

Never hardcoded in source.

🛠 Run Locally
pip install -r requirements.txt
uvicorn main:app --reload

Open:

http://localhost:8000/docs
🌱 Future Improvements

Redis-based persistent job queue

WebSocket live progress updates

Podcast history storage (Database)

Background music mixing engine

Multi-language support

User accounts

🎯 Why This Project Matters

AgentCast is more than an AI wrapper.

It demonstrates:

Multi-agent orchestration

Structured LLM pipelines

Async backend design

Audio generation system

Production deployment with Docker

CORS & environment management

Real-world engineering trade-offs

It combines:

AI + Backend Engineering + Media Processing

👨‍💻 Author

Deepak Ajay
Backend Engineer | AI Systems Explorer | System Design Learner

⭐ If You Like This Project

Star the repo and share feedback!
