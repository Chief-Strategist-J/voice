import os
from videosdk.agents import Agent, AgentSession, Pipeline, JobContext
from videosdk.agents.plugins import OpenAISTT, OpenAILLM, OpenAITTS, SileroVAD

class OpenAICascadeAgent(Agent):
    def __init__(self):
        super().__init__(
            instructions=os.getenv("INSTRUCTIONS", "You are a helpful voice assistant.")
        )

    async def on_enter(self) -> None:
        await self.session.say("Hello! How can I help you today?")

async def build_session(ctx: JobContext) -> AgentSession:
    openai_key = os.getenv("OPENAI_API_KEY", "")
    pipeline = Pipeline(
        stt=OpenAISTT(api_key=openai_key),
        llm=OpenAILLM(api_key=openai_key, model=os.getenv("MODEL_NAME", "gpt-4o")),
        tts=OpenAITTS(api_key=openai_key),
        vad=SileroVAD()
    )
    agent = OpenAICascadeAgent()
    await ctx.connect()
    return AgentSession(agent=agent, pipeline=pipeline, context=ctx)
