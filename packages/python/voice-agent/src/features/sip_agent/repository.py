from typing import Dict, Optional
from .types import SIPCallStatus

class SIPAgentRepository:
    def __init__(self) -> None:
        self._calls: Dict[str, SIPCallStatus] = {}

    def save_call(self, call: SIPCallStatus) -> None:
        self._calls[call.call_id] = call

    def get_call(self, call_id: str) -> Optional[SIPCallStatus]:
        return self._calls.get(call_id)

    def delete_call(self, call_id: str) -> None:
        if call_id in self._calls:
            del self._calls[call_id]
