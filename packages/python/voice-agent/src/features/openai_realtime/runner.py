import asyncio
import os
import logging
from dotenv import load_dotenv
from videosdk.agents import WorkerJob, Options, JobContext, RoomOptions
from videosdk.agents import Agent, AgentSession, Pipeline
from videosdk.agents.plugins import OpenAIRealtime, OpenAIRealtimeConfig

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class VideoSDKVoiceAgent(Agent):
    def __init__(self, instructions: str):
        super().__init__(instructions=instructions)

    async def on_enter(self) -> None:
        await self.session.say("Hello, I am your OpenAI Realtime voice assistant. How can I help you today?")

async def entrypoint(ctx: JobContext):
    openai_key = os.getenv("OPENAI_API_KEY", "")
    instructions = os.getenv("INSTRUCTIONS", "You are a helpful voice assistant.")
    voice_name = os.getenv("VOICE_NAME", "alloy")
    model_name = os.getenv("MODEL_NAME", "gpt-4o-realtime-preview")
    
    model_config = OpenAIRealtimeConfig(
        api_key=openai_key,
        voice=voice_name,
        model=model_name
    )
    model = OpenAIRealtime(config=model_config)
    pipeline = Pipeline(llm=model)
    
    agent = VideoSDKVoiceAgent(instructions=instructions)
    await ctx.connect()
    session = AgentSession(agent=agent, pipeline=pipeline, context=ctx)
    await session.start()

def make_context():
    room_options = RoomOptions(
        room_id=os.getenv("VIDEOSDK_MEETING_ID", "default_meeting"),
        auth_token=os.getenv("VIDEOSDK_TOKEN"),
        name="OpenAI Realtime Agent"
    )
    return JobContext(room_options=room_options)

if __name__ == "__main__":
    options = Options(
        agent_id="voice-agent-openai-realtime",
        max_processes=5,
        register=True,
        log_level="INFO"
    )
    job = WorkerJob(
        entrypoint=entrypoint,
        jobctx=make_context,
        options=options
    )
    job.start()
