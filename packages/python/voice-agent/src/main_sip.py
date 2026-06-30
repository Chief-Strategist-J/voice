import asyncio
import os
import logging
from dotenv import load_dotenv
from videosdk.agents import WorkerJob, Options, JobContext, RoomOptions

from .features.sip_agent.service import SIPAgentService
from .features.sip_agent.repository import SIPAgentRepository
from .features.sip_agent.types import SIPAgentConfig

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

repository = SIPAgentRepository()
service = SIPAgentService(repository)

async def entrypoint(ctx: JobContext):
    room_id = os.getenv("VIDEOSDK_MEETING_ID", "default_room")
    token = os.getenv("VIDEOSDK_TOKEN", "")
    openai_key = os.getenv("OPENAI_API_KEY", "")
    
    config = SIPAgentConfig(
        room_id=room_id,
        token=token,
        openai_api_key=openai_key
    )
    
    await service.start_sip_session(config, ctx)

def make_context():
    room_options = RoomOptions(
        room_id=os.getenv("VIDEOSDK_MEETING_ID", "default_room"),
        auth_token=os.getenv("VIDEOSDK_TOKEN"),
        name="VideoSDK SIP Telephony Agent"
    )
    return JobContext(room_options=room_options)

if __name__ == "__main__":
    options = Options(
        agent_id="sip-agent-service",
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
