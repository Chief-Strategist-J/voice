from dataclasses import dataclass
from typing import Optional

@dataclass
class VoiceAgentConfig:
    meeting_id: str
    token: str
    openai_api_key: Optional[str] = None
    google_api_key: Optional[str] = None
    sarvam_api_key: Optional[str] = None
    deepgram_api_key: Optional[str] = None
    elevenlabs_api_key: Optional[str] = None
    anthropic_api_key: Optional[str] = None
    instructions: str = "You are a helpful voice assistant."
    voice_name: str = "alloy"
    model_name: str = "gpt-4o-realtime-preview"
    pipeline_mode: str = "realtime"

@dataclass
class AgentSessionInfo:
    session_id: str
    meeting_id: str
    status: str
    error_message: Optional[str] = None
