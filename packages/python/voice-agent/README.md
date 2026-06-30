# Voice Agent

Multi-provider AI voice agent platform built on [VideoSDK](https://videosdk.live). Each pipeline is a fully independent, self-contained folder you can edit, build, and deploy without touching anything else.

---

## Pipelines

| Pipeline | STT | LLM | TTS | Type |
|---|---|---|---|---|
| `openai_realtime` | — | GPT-4o Realtime | — | Realtime |
| `google_realtime` | — | Gemini 2.0 Flash | — | Realtime |
| `openai_cascade` | OpenAI Whisper | GPT-4o | OpenAI TTS | Cascade |
| `google_cascade` | Google STT | Gemini 1.5 Flash | Google TTS | Cascade |
| `sarvam_cascade` | Sarvam AI | Sarvam AI | Sarvam AI | Cascade |
| `custom_cascade` | Deepgram | Claude 3.5 Sonnet | ElevenLabs | Cascade |
| `sip` | OpenAI Whisper | GPT-4o | OpenAI TTS | SIP/Telephony |

All pipelines include **Silero VAD** for voice activity detection.

---

## Folder Structure

Every pipeline lives entirely inside its own folder. Nothing is shared between pipelines.

```
src/features/{pipeline}/
├── src/
│   ├── __init__.py
│   └── agent.py          ← edit this to change agent behaviour
├── Dockerfile            ← builds only this pipeline
├── docker-compose.yaml   ← run this pipeline locally
├── requirements.txt      ← this pipeline's dependencies only
├── runner.py             ← entry point (do not edit)
├── videosdk.yaml         ← VideoSDK cloud deployment manifest
└── context.yaml          ← pipeline metadata
```

---

## Prerequisites

- Python 3.12+
- Docker & Docker Compose
- A [VideoSDK](https://videosdk.live) account with API key and secret
- Provider API keys for the pipeline you want to run

---

## Environment Setup

Create a `.env` file inside the pipeline folder you want to run:

```bash
cp packages/python/voice-agent/.env.example \
   packages/python/voice-agent/src/features/openai_realtime/.env
```

Fill in the required keys for your chosen pipeline:

```env
# Required for all pipelines
VIDEOSDK_TOKEN=your_videosdk_jwt_token
VIDEOSDK_MEETING_ID=your_meeting_id
INSTRUCTIONS=You are a helpful voice assistant.

# OpenAI pipelines (openai_realtime, openai_cascade, sip)
OPENAI_API_KEY=your_openai_key

# Google pipelines (google_realtime, google_cascade)
GOOGLE_API_KEY=your_google_key

# Sarvam pipeline (sarvam_cascade)
SARVAM_API_KEY=your_sarvam_key

# Custom pipeline (custom_cascade)
DEEPGRAM_API_KEY=your_deepgram_key
ANTHROPIC_API_KEY=your_anthropic_key
ELEVENLABS_API_KEY=your_elevenlabs_key
```

---

## Run with Docker (Recommended)

Navigate into any pipeline folder and run it:

```bash
cd packages/python/voice-agent/src/features/openai_realtime

# Build and start
docker compose up --build

# Run in background
docker compose up --build -d

# Stop
docker compose down
```

Same command works for every pipeline — just change the folder:

```bash
cd packages/python/voice-agent/src/features/google_realtime && docker compose up --build
cd packages/python/voice-agent/src/features/sarvam_cascade  && docker compose up --build
cd packages/python/voice-agent/src/features/custom_cascade  && docker compose up --build
```

---

## Run All Pipelines Together

To run all pipelines simultaneously using the top-level orchestrator:

```bash
cd packages/python/voice-agent

docker compose -f deploy/docker/docker-compose.worker.yaml up --build
```

Run a specific pipeline only:

```bash
docker compose -f deploy/docker/docker-compose.worker.yaml up --build openai-realtime-agent
docker compose -f deploy/docker/docker-compose.worker.yaml up --build sarvam-cascade-agent
```

---

## Run Locally (Without Docker)

```bash
# Install dependencies
cd packages/python/voice-agent/src/features/openai_realtime
pip install -r requirements.txt

# Set environment variables
cp /path/to/.env .env

# Run
python runner.py
```

---

## Deploy to VideoSDK Cloud

```bash
cd packages/python/voice-agent/src/features/openai_realtime
videosdk deploy videosdk.yaml
```

Each pipeline has its own `videosdk.yaml` — deploy them independently.

---

## Edit a Pipeline

To change what an agent says, its instructions, model, or voice — edit only:

```
src/features/{pipeline}/src/agent.py
```

Then rebuild:

```bash
cd src/features/{pipeline}
docker compose up --build
```

---

## Add a New Pipeline

```bash
# Copy an existing pipeline as template
cp -r packages/python/voice-agent/src/features/openai_cascade \
       packages/python/voice-agent/src/features/my_pipeline

# Edit the agent logic
nano packages/python/voice-agent/src/features/my_pipeline/src/agent.py

# Edit dependencies
nano packages/python/voice-agent/src/features/my_pipeline/requirements.txt

# Build and run
cd packages/python/voice-agent/src/features/my_pipeline
docker compose up --build
```

---

## REST API (Optional)

A lightweight FastAPI server is available for room creation and agent dispatch:

```bash
cd packages/python/voice-agent
uvicorn api.rest.v1.server:app --host 0.0.0.0 --port 8000
```

Endpoints:
- `POST /room/create` — create a VideoSDK meeting room
- `POST /agent/dispatch` — dispatch an agent into a room

---

## Shared Utilities

Located in `src/shared/utils/`:

| File | Purpose |
|---|---|
| `token_generator.py` | Generate VideoSDK JWT tokens |
| `room_creator.py` | Create VideoSDK meeting rooms via API |
| `agent_dispatcher.py` | Dispatch agents into rooms via API |
