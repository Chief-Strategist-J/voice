import asyncio
import logging
from typing import Optional
from videosdk.agents import Agent, AgentSession, Pipeline, JobContext
from videosdk.agents.plugins import OpenAIRealtime, OpenAIRealtimeConfig

from .types import SIPAgentConfig, SIPCallStatus
from .repository import SIPAgentRepository

logger = logging.getLogger(__name__)

class VideoSDKSIPAgent(Agent):
    def __init__(self, instructions: str):
        super().__init__(instructions=instructions)

    async def on_enter(self) -> None:
        await self.session.say("Thank you for calling. How can I assist you today?")

    async def terminate_call(self) -> None:
        await self.hangup()


class SIPAgentService:
    def __init__(self, repository: SIPAgentRepository):
        self.repository = repository

    async def start_sip_session(self, config: SIPAgentConfig, ctx: JobContext) -> SIPCallStatus:
        try:
            model_config = OpenAIRealtimeConfig(
                api_key=config.openai_api_key,
                voice=config.voice_name,
                model=config.model_name
            )
            model = OpenAIRealtime(config=model_config)
            pipeline = Pipeline(llm=model)
            agent = VideoSDKSIPAgent(instructions=config.instructions)
            await ctx.connect()
            session = AgentSession(agent=agent, pipeline=pipeline, context=ctx)
            await session.start()
            call_status = SIPCallStatus(
                call_id=ctx.job_id,
                room_id=config.room_id,
                status="active"
            )
            self.repository.save_call(call_status)
            return call_status
        except Exception as e:
            call_status = SIPCallStatus(
                call_id=ctx.job_id if hasattr(ctx, 'job_id') else "unknown",
                room_id=config.room_id,
                status="failed",
                error_message=str(e)
            )
            return call_status
