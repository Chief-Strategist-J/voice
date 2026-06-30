import os
from dotenv import load_dotenv
from videosdk.agents import WorkerJob, Options, JobContext, RoomOptions
from src.agent import build_session

load_dotenv()

async def entrypoint(ctx: JobContext):
    session = await build_session(ctx)
    await session.start()

def make_context():
    return JobContext(room_options=RoomOptions(
        room_id=os.getenv("VIDEOSDK_MEETING_ID", "default_meeting"),
        auth_token=os.getenv("VIDEOSDK_TOKEN"),
        name="SIP Voice Agent"
    ))

if __name__ == "__main__":
    job = WorkerJob(
        entrypoint=entrypoint,
        jobctx=make_context,
        options=Options(
            agent_id="sip-voice-agent",
            max_processes=5,
            register=True,
            log_level="INFO"
        )
    )
    job.start()
