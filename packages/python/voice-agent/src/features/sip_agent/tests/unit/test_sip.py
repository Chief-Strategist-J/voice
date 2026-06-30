import pytest
from unittest.mock import AsyncMock
from features.sip_agent.types import SIPAgentConfig, SIPCallStatus
from features.sip_agent.service import SIPAgentService
from features.sip_agent.repository import SIPAgentRepository

@pytest.mark.asyncio
async def test_start_sip_session_success():
    repository = SIPAgentRepository()
    service = SIPAgentService(repository)
    
    mock_ctx = AsyncMock()
    mock_ctx.job_id = "test-call-id"
    mock_ctx.connect = AsyncMock()
    
    config = SIPAgentConfig(
        room_id="test-room-id",
        token="test-token",
        openai_api_key="test-key"
    )
    
    result = await service.start_sip_session(config, mock_ctx)
    
    assert isinstance(result, SIPCallStatus)
    assert result.room_id == "test-room-id"

def test_sip_repository_operations():
    repository = SIPAgentRepository()
    
    call = SIPCallStatus(
        call_id="call-1",
        room_id="room-1",
        status="active"
    )
    
    repository.save_call(call)
    retrieved = repository.get_call("call-1")
    assert retrieved is not None
    assert retrieved.room_id == "room-1"
    
    repository.delete_call("call-1")
    assert repository.get_call("call-1") is None
