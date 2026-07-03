import os
from videosdk.agents import Agent, AgentSession, Pipeline, JobContext
from videosdk.agents.plugins import OpenAISTT, OpenAILLM, OpenAITTS, SileroVAD

class SIPVoiceAgent(Agent):
    def __init__(self):
        super().__init__(
            instructions=os.getenv("INSTRUCTIONS", "You are a helpful phone voice assistant.")
        )

    async def on_enter(self) -> None:
        await self.session.say("Hello! You have reached the voice assistant. How can I help?")

    async def on_exit(self) -> None:
        pass

async def build_session(ctx: JobContext) -> AgentSession:
    openai_key = os.getenv("OPENAI_API_KEY", "")
    pipeline = Pipeline(
        stt=OpenAISTT(api_key=openai_key),
        llm=OpenAILLM(api_key=openai_key, model=os.getenv("MODEL_NAME", "gpt-4o")),
        tts=OpenAITTS(api_key=openai_key),
        vad=SileroVAD()
    )
    agent = SIPVoiceAgent()
    # No ctx.connect() here and no `context=` kwarg -- AgentSession has no
    # such param, it discovers the active JobContext itself. runner.py's
    # entrypoint calls ctx.run_until_shutdown(session, ...), which connects,
    # starts the session, and blocks until the call actually ends.
    return AgentSession(agent=agent, pipeline=pipeline)
