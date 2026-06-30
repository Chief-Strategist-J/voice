import asyncio
import logging
from typing import Optional
from videosdk.agents import Agent, AgentSession, Pipeline, JobContext
from videosdk.agents.plugins import OpenAIRealtime, OpenAIRealtimeConfig

from .types import VoiceAgentConfig, AgentSessionInfo
from .repository import VoiceAgentRepository

logger = logging.getLogger(__name__)

class VideoSDKVoiceAgent(Agent):
    def __init__(self, instructions: str):
        super().__init__(instructions=instructions)

    async def on_enter(self) -> None:
        logger.info("Voice Agent entered the meeting room.")
        await self.session.say("Hello, I am your voice assistant. How can I help you today?")


class VoiceAgentService:
    """Service to handle the creation and lifecycle of VideoSDK voice agents."""
    
    def __init__(self, repository: VoiceAgentRepository):
        self.repository = repository

    async def start_agent_session(self, config: VoiceAgentConfig, ctx: JobContext) -> AgentSessionInfo:
        """Starts a real-time voice agent session using OpenAI Realtime model and VideoSDK."""
        try:
            # Configure OpenAI Realtime plugin
            model_config = OpenAIRealtimeConfig(
                api_key=config.openai_api_key,
                voice=config.voice_name,
                model=config.model_name
            )
            model = OpenAIRealtime(config=model_config)
            
            # Setup Pipeline (Realtime Mode is automatically set when llm is provided)
            pipeline = Pipeline(llm=model)
            
            # Initialize custom agent
            agent = VideoSDKVoiceAgent(instructions=config.instructions)
            
            # Connect the context to join the VideoSDK room
            await ctx.connect()
            
            # Bind session and start it
            session = AgentSession(agent=agent, pipeline=pipeline, context=ctx)
            await session.start()
            
            session_info = AgentSessionInfo(
                session_id=ctx.job_id,
                meeting_id=config.meeting_id,
                status="running"
            )
            self.repository.save_session(session_info)
            return session_info
            
        except Exception as e:
            logger.exception("Failed to start voice agent session")
            session_info = AgentSessionInfo(
                session_id=ctx.job_id if hasattr(ctx, 'job_id') else "unknown",
                meeting_id=config.meeting_id,
                status="failed",
                error_message=str(e)
            )
            return session_info
