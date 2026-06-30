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
        await self.session.say("Hello, I am your voice assistant. How can I help you today?")


class VoiceAgentService:
    def __init__(self, repository: VoiceAgentRepository):
        self.repository = repository

    async def start_agent_session(self, config: VoiceAgentConfig, ctx: JobContext) -> AgentSessionInfo:
        try:
            model_config = OpenAIRealtimeConfig(
                api_key=config.openai_api_key,
                voice=config.voice_name,
                model=config.model_name
            )
            model = OpenAIRealtime(config=model_config)
            pipeline = Pipeline(llm=model)
            agent = VideoSDKVoiceAgent(instructions=config.instructions)
            await ctx.connect()
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
            session_info = AgentSessionInfo(
                session_id=ctx.job_id if hasattr(ctx, 'job_id') else "unknown",
                meeting_id=config.meeting_id,
                status="failed",
                error_message=str(e)
            )
            return session_info
