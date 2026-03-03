# 🎙️ AgentCast Backend
### *Turn Any Topic Into an AI Debate Podcast*
 

> AgentCast is an AI-powered backend that transforms any topic into a fully generated, two-speaker debate podcast — complete with Indian voice narration and intro music.

It combines **multi-agent AI orchestration**, **LLM intelligence**, and **text-to-speech audio generation** into one seamless pipeline.

---
<img width="3410" height="593" alt="mermaid-diagram" src="https://github.com/user-attachments/assets/76cfe851-7cef-4b6f-91ef-78a9d550f273" />


## 🌍 What It Does

Send a single request:

```json
{
  "topic": "How AI agents work"
}
```

And AgentCast will:

- 🧠 **Plan** the topic structure
- 🎭 **Generate** a fun two-person debate script
- 🎙️ **Convert** it into realistic Indian voice audio
- 🎵 **Add** intro music
- 🔗 **Return** a streamable podcast URL

---

## 🏗️ Architecture Overview

```
User → API → 3 AI Agents → LLM → Script → TTS → Audio File → Public URL
```

Think of it as a small AI-powered production studio:

1. 🎧 A listener sends a topic
2. 🧑‍💻 Three AI "writers" collaborate
3. 🤖 A powerful language model drafts the script
4. 🎙️ Two voice actors perform it
5. 🎵 Intro music is added
6. 📡 The episode is published

---

## 🤖 The Three-Agent System

AgentCast uses three coordinated agents, each with a distinct role — not a single AI call.

### 1️⃣ Topic Planner Agent
> *The outline writer*

- Breaks down the topic logically
- Organizes the flow and structure
- Ensures content clarity

### 2️⃣ Debate Podcast Creator Agent
> *Where the magic happens*

- Turns the outline into a lively, engaging debate
- Adds humor, analogies, and conversational fillers
- Assigns dialogue to two speakers:
  - 🎙️ **Speaker A** — Indian Female Voice
  - 🎙️ **Speaker B** — Indian Male Voice

### 3️⃣ JSON Formatter Agent
> *The quality enforcer*

- Enforces strict JSON output for clean downstream processing

```json
{
  "dialogue": [
    { "speaker": "A", "text": "..." },
    { "speaker": "B", "text": "..." }
  ]
}
```

---

## 🔄 Async Job Architecture

Generating LLM output, TTS audio, and assembling the final file takes **20–40 seconds**. Blocking APIs don't scale, so AgentCast implements an in-memory background job queue.

### API Flow

```
POST /generate        →  returns job_id
GET  /status/{job_id} →  poll for progress
GET  /result/{job_id} →  fetch completed result
```

### Lifecycle

```
User clicks Generate
        ↓
Backend creates job
        ↓
Job runs in background
        ↓
Frontend polls /status
        ↓
When complete → fetch /result
```

> **Note:** For public deployment on Render (free tier), the system uses a blocking model due to container restarts. The async architecture is production-ready and documented for self-hosted deployments.

---

## 🎧 Audio Processing Pipeline

Once the script is ready, the audio pipeline runs sequentially:

```
🎵 Load intro music
🎙️ Generate Speaker A audio
🎙️ Generate Speaker B audio
📦 Concatenate all segments
💾 Save to /audio
🌐 Serve via public URL
```

---

## 📦 Tech Stack

| Layer | Technology |
|---|---|
| API | FastAPI |
| AI Orchestration | CrewAI |
| LLM Routing | LiteLLM |
| Model Provider | OpenRouter |
| Text-to-Speech | edge-tts |
| Deployment | Render (Docker) |
| Frontend | React (Vercel) |

---

## 🔐 Environment Variables

```env
OPENROUTER_API_KEY=your_key_here
```

> ⚠️ Never hardcode API keys in source files.

---

## 🛠️ Run Locally

```bash
pip install -r requirements.txt
uvicorn main:app --reload
```

Open the interactive API docs at: [http://localhost:8000/docs](http://localhost:8000/docs)

---

## 🌱 Roadmap

- [ ] Redis-based persistent job queue
- [ ] WebSocket live progress updates
- [ ] Podcast history storage (Database)
- [ ] Background music mixing engine
- [ ] Multi-language support
- [ ] User accounts & history

---

## 🎯 Why This Project Matters

AgentCast is more than an AI wrapper. It demonstrates real-world engineering across multiple domains:

| Skill | How It's Applied |
|---|---|
| Multi-agent orchestration | Three coordinated CrewAI agents |
| Structured LLM pipelines | Chained prompting with JSON enforcement |
| Async backend design | Job queue with polling endpoints |
| Audio generation | TTS + music concatenation pipeline |
| Production deployment | Docker, CORS, environment management |

> It combines **AI + Backend Engineering + Media Processing** in one cohesive system.

---

## 👨‍💻 Author

**Deepak Ajay**  
*Backend Engineer · AI Systems Explorer · System Design Learner*

---

*⭐ If you find this project useful, star the repo and share your feedback!*
