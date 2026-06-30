import pytest
from unittest.mock import AsyncMock
from features.voice_agent.types import VoiceAgentConfig, AgentSessionInfo
from features.voice_agent.service import VoiceAgentService
from features.voice_agent.repository import VoiceAgentRepository

@pytest.mark.asyncio
async def test_start_agent_session_success():
    repository = VoiceAgentRepository()
    service = VoiceAgentService(repository)
    
    mock_ctx = AsyncMock()
    mock_ctx.job_id = "test-job-id"
    mock_ctx.connect = AsyncMock()
    
    config = VoiceAgentConfig(
        meeting_id="test-meeting-id",
        token="test-token",
        openai_api_key="test-key"
    )
    
    result = await service.start_agent_session(config, mock_ctx)
    
    assert isinstance(result, AgentSessionInfo)
    assert result.meeting_id == "test-meeting-id"

def test_repository_operations():
    repository = VoiceAgentRepository()
    
    session = AgentSessionInfo(
        session_id="session-1",
        meeting_id="meeting-1",
        status="running"
    )
    
    repository.save_session(session)
    retrieved = repository.get_session("session-1")
    assert retrieved is not None
    assert retrieved.meeting_id == "meeting-1"
    
    repository.delete_session("session-1")
    assert repository.get_session("session-1") is None
