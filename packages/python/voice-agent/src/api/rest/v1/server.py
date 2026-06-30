import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv

from features.voice_agent.index import VoiceAgentConfig, VoiceAgentService, VoiceAgentRepository
from shared.utils.room_creator import create_videosdk_room

load_dotenv()

app = FastAPI(title="VideoSDK Voice Agent API", version="1.0.0")

repository = VoiceAgentRepository()
service = VoiceAgentService(repository)

class AgentStartRequest(BaseModel):
    meeting_id: str
    token: str
    instructions: str = "You are a helpful voice assistant."
    voice_name: str = "alloy"
    model_name: str = "gpt-4o-realtime-preview"

@app.post("/room/create")
async def create_room():
    token = os.getenv("VIDEOSDK_TOKEN")
    if not token:
        raise HTTPException(status_code=500, detail="VIDEOSDK_TOKEN environment variable not set")
    
    room_id = create_videosdk_room(token)
    if not room_id:
        raise HTTPException(status_code=500, detail="Failed to create VideoSDK room")
        
    return {"roomId": room_id}

@app.post("/agent/start")
async def start_agent(request: AgentStartRequest):
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
