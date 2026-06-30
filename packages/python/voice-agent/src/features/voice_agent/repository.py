from typing import Dict, Optional
from .types import AgentSessionInfo

class VoiceAgentRepository:
    def __init__(self) -> None:
        self._sessions: Dict[str, AgentSessionInfo] = {}

    def save_session(self, session: AgentSessionInfo) -> None:
        self._sessions[session.session_id] = session

    def get_session(self, session_id: str) -> Optional[AgentSessionInfo]:
        return self._sessions.get(session_id)

    def delete_session(self, session_id: str) -> None:
        if session_id in self._sessions:
            del self._sessions[session_id]
