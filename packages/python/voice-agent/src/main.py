import asyncio
import os
import logging
from dotenv import load_dotenv
from videosdk.agents import WorkerJob, JobContext

from .features.voice_agent.index import VoiceAgentConfig, VoiceAgentService, VoiceAgentRepository

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Repository and Service instances
repository = VoiceAgentRepository()
service = VoiceAgentService(repository)

async def entrypoint(ctx: JobContext):
    """Worker job callback function triggered when VideoSDK assigns a task."""
    logger.info(f"Worker job starting for ID: {ctx.job_id}")
    
    # Retrieve configuration from environment or context parameters
    meeting_id = os.getenv("VIDEOSDK_MEETING_ID", "default_meeting")
    token = os.getenv("VIDEOSDK_TOKEN", "")
    openai_key = os.getenv("OPENAI_API_KEY", "")
    
    config = VoiceAgentConfig(
        meeting_id=meeting_id,
        token=token,
        openai_api_key=openai_key
    )
    
    # Delegate job execution to the feature service
    await service.start_agent_session(config, ctx)

if __name__ == "__main__":
    logger.info("Starting VideoSDK Voice Agent Worker...")
    job = WorkerJob(job_func=entrypoint)
    job.start()
