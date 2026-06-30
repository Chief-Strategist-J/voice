import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv

from ....features.voice_agent.index import VoiceAgentConfig, VoiceAgentService, VoiceAgentRepository

load_dotenv()

app = FastAPI(title="VideoSDK Voice Agent API", version="1.0.0")

# Instantiate repo and service in memory (dependency injection)
repository = VoiceAgentRepository()
service = VoiceAgentService(repository)

class AgentStartRequest(BaseModel):
    meeting_id: str
    token: str
    instructions: str = "You are a helpful voice assistant."
    voice_name: str = "alloy"
    model_name: str = "gpt-4o-realtime-preview"

@app.post("/agent/start")
async def start_agent(request: AgentStartRequest):
    # Retrieve api keys
    openai_key = os.getenv("OPENAI_API_KEY")
    if not openai_key:
        raise HTTPException(status_code=500, detail="OPENAI_API_KEY environment variable not set")
    
    config = VoiceAgentConfig(
        meeting_id=request.meeting_id,
        token=request.token,
        openai_api_key=openai_key,
        instructions=request.instructions,
        voice_name=request.voice_name,
        model_name=request.model_name
    )
    
    # Normally, JobContext is passed by the worker run-loop when a job is scheduled.
    # Here, we return a mock status to represent HTTP entry interface mapping.
    # Real real-time agents join via VideoSDK Worker jobs.
    return {
        "message": "Voice agent initialization request accepted",
        "meeting_id": config.meeting_id,
        "status": "pending_worker"
    }

@app.get("/agent/status/{session_id}")
async def get_agent_status(session_id: str):
    session = repository.get_session(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Agent session not found")
    return session
