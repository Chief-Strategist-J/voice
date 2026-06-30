import asyncio
import os
import logging
from dotenv import load_dotenv
from videosdk.agents import WorkerJob, Options, JobContext, RoomOptions
from videosdk.agents import Agent, AgentSession, Pipeline
from videosdk.agents.plugins import SarvamAISTT, SarvamAILLM, SarvamAITTS, SileroVAD

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class VideoSDKVoiceAgent(Agent):
    def __init__(self, instructions: str):
        super().__init__(instructions=instructions)

    async def on_enter(self) -> None:
        await self.session.say("Hello, I am your Sarvam Cascade voice assistant. How can I help you today?")

async def entrypoint(ctx: JobContext):
    sarvam_key = os.getenv("SARVAM_API_KEY", "")
    instructions = os.getenv("INSTRUCTIONS", "You are a helpful voice assistant.")
    
    stt = SarvamAISTT(api_key=sarvam_key)
    llm = SarvamAILLM(api_key=sarvam_key, instructions=instructions)
    tts = SarvamAITTS(api_key=sarvam_key)
    pipeline = Pipeline(
        stt=stt,
        llm=llm,
        tts=tts,
        vad=SileroVAD()
    )
    
    agent = VideoSDKVoiceAgent(instructions=instructions)
    await ctx.connect()
    session = AgentSession(agent=agent, pipeline=pipeline, context=ctx)
    await session.start()

def make_context():
    room_options = RoomOptions(
        room_id=os.getenv("VIDEOSDK_MEETING_ID", "default_meeting"),
        auth_token=os.getenv("VIDEOSDK_TOKEN"),
        name="Sarvam Cascade Agent"
    )
    return JobContext(room_options=room_options)

if __name__ == "__main__":
    options = Options(
        agent_id="voice-agent-sarvam-cascade",
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
