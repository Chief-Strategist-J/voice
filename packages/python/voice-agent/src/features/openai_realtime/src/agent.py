import os
from videosdk.agents import Agent, AgentSession, Pipeline, JobContext
from videosdk.agents.plugins import OpenAIRealtime, OpenAIRealtimeConfig, SileroVAD

class OpenAIRealtimeAgent(Agent):
    def __init__(self):
        super().__init__(
            instructions=os.getenv("INSTRUCTIONS", "You are a helpful voice assistant.")
        )

    async def on_enter(self) -> None:
        await self.session.say("Hello! How can I help you today?")

async def build_session(ctx: JobContext) -> AgentSession:
    config = OpenAIRealtimeConfig(
        api_key=os.getenv("OPENAI_API_KEY", ""),
        voice=os.getenv("VOICE_NAME", "alloy"),
        model=os.getenv("MODEL_NAME", "gpt-4o-realtime-preview")
    )
    model = OpenAIRealtime(config=config)
    pipeline = Pipeline(llm=model, vad=SileroVAD())
    agent = OpenAIRealtimeAgent()
    await ctx.connect()
    return AgentSession(agent=agent, pipeline=pipeline, context=ctx)
