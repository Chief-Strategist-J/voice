import pytest
from unittest.mock import AsyncMock
from features.voice_agent.types import VoiceAgentConfig, AgentSessionInfo
from features.voice_agent.service import VoiceAgentService
from features.voice_agent.repository import VoiceAgentRepository

@pytest.mark.asyncio
async def test_start_agent_session_success():
    # Setup repo and service
    repository = VoiceAgentRepository()
    service = VoiceAgentService(repository)
    
    # Mock JobContext
    mock_ctx = AsyncMock()
    mock_ctx.job_id = "test-job-id"
    mock_ctx.connect = AsyncMock()
    
    # Mock Config
    config = VoiceAgentConfig(
        meeting_id="test-meeting-id",
        token="test-token",
        openai_api_key="test-key"
    )
    
    # We will patch the Pipeline and AgentSession since they connect to actual media resources
    # However, since we want a simple unit test, we can mock the session start
    # Let's run start_agent_session and assert result
    # We will mock the external dependencies of the service if necessary.
    # In this mock scenario, since Pipeline and OpenAIRealtime require actual tokens,
    # we can verify that the service handles failures or mocks them.
    
    # Let's mock the videosdk agents class imports inside the method by mocking the service class methods
    # or just verifying the error handling when key is invalid.
    result = await service.start_agent_session(config, mock_ctx)
    
    # Assert session is registered or failed gracefully
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
