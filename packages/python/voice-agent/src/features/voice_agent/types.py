from dataclasses import dataclass
from typing import Optional, Dict, Any

@dataclass
class VoiceAgentConfig:
    """Configuration options for initiating a Voice Agent session."""
    meeting_id: str
    token: str
    openai_api_key: str
    instructions: str = "You are a helpful voice assistant."
    voice_name: str = "alloy"  # Default OpenAI Realtime voice
    model_name: str = "gpt-4o-realtime-preview"

@dataclass
class AgentSessionInfo:
    """Status info returned for a running agent session."""
    session_id: str
    meeting_id: str
    status: str
    error_message: Optional[str] = None
