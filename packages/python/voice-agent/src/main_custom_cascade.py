import asyncio
import os
import logging
from dotenv import load_dotenv
from videosdk.agents import WorkerJob, Options, JobContext, RoomOptions

from .features.voice_agent.index import VoiceAgentConfig, VoiceAgentService, VoiceAgentRepository

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

repository = VoiceAgentRepository()
service = VoiceAgentService(repository)

async def entrypoint(ctx: JobContext):
    meeting_id = os.getenv("VIDEOSDK_MEETING_ID", "default_meeting")
    token = os.getenv("VIDEOSDK_TOKEN", "")
    
    config = VoiceAgentConfig(
        meeting_id=meeting_id,
        token=token,
        deepgram_api_key=os.getenv("DEEPGRAM_API_KEY"),
        elevenlabs_api_key=os.getenv("ELEVENLABS_API_KEY"),
        anthropic_api_key=os.getenv("ANTHROPIC_API_KEY"),
        pipeline_mode="custom_cascade"
    )
    await service.start_agent_session(config, ctx)

def make_context():
    room_options = RoomOptions(
        room_id=os.getenv("VIDEOSDK_MEETING_ID", "default_meeting"),
        auth_token=os.getenv("VIDEOSDK_TOKEN"),
        name="Custom Cascade Agent"
    )
    return JobContext(room_options=room_options)

if __name__ == "__main__":
    options = Options(
        agent_id="voice-agent-custom-cascade",
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
