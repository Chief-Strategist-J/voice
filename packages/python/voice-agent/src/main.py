import asyncio
import os
import logging
from dotenv import load_dotenv
from videosdk.agents import WorkerJob, JobContext

from .features.voice_agent.index import VoiceAgentConfig, VoiceAgentService, VoiceAgentRepository

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

repository = VoiceAgentRepository()
service = VoiceAgentService(repository)

async def entrypoint(ctx: JobContext):
    meeting_id = os.getenv("VIDEOSDK_MEETING_ID", "default_meeting")
    token = os.getenv("VIDEOSDK_TOKEN", "")
    openai_key = os.getenv("OPENAI_API_KEY", "")
    
    config = VoiceAgentConfig(
        meeting_id=meeting_id,
        token=token,
        openai_api_key=openai_key
    )
    
    await service.start_agent_session(config, ctx)

if __name__ == "__main__":
    job = WorkerJob(job_func=entrypoint)
    job.start()
