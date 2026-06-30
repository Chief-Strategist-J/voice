from dataclasses import dataclass
from typing import Optional

@dataclass
class VoiceAgentConfig:
    meeting_id: str
    token: str
    openai_api_key: str
    instructions: str = "You are a helpful voice assistant."
    voice_name: str = "alloy"
    model_name: str = "gpt-4o-realtime-preview"

@dataclass
class AgentSessionInfo:
    session_id: str
    meeting_id: str
    status: str
    error_message: Optional[str] = None
