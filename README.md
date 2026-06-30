# Voice Agent Platform

Real-time voice agent repository utilizing VideoSDK and OpenAI.

## Directory Structure

- packages/python/voice-agent/ : Python Voice Agent sub-package.
- policies/ : System guidelines, architectures, and development rules.

## Getting Started

1. Set up the virtual environment:
   ```bash
   python3 -m virtualenv .venv
   source .venv/bin/activate
   ```

2. Install dependencies and the package in editable mode:
   ```bash
   uv pip install -r requirements.txt
   ```

3. Setup environment variables in `.env`:
   ```env
   OPENAI_API_KEY=your_openai_api_key
   VIDEOSDK_MEETING_ID=your_meeting_id
   VIDEOSDK_TOKEN=your_videosdk_token
   ```

4. Run the REST API:
   ```bash
   uvicorn packages.python.voice-agent.src.api.rest.v1.server:app --host 0.0.0.0 --port 8000
   ```

5. Run the background worker:
   ```bash
   python packages/python/voice-agent/src/main.py
   ```

## Development and Testing

Run tests using:
```bash
PYTHONPATH=packages/python/voice-agent/src pytest packages/python/voice-agent/src/features/voice_agent/tests/
```
