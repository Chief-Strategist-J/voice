from dataclasses import dataclass
from typing import Optional

@dataclass
class SIPAgentConfig:
    room_id: str
    token: str
    openai_api_key: str
    instructions: str = "You are a customer service representative."
    voice_name: str = "shimmer"
    model_name: str = "gpt-4o-realtime-preview"

@dataclass
class SIPCallStatus:
    call_id: str
    room_id: str
    status: str
    error_message: Optional[str] = None
