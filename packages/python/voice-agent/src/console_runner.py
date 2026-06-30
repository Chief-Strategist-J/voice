import sys
import asyncio
import os
from dotenv import load_dotenv

load_dotenv()

from videosdk.agents.console_mode import setup_console_room_client_for_ctx
from videosdk.agents import JobContext, RoomOptions

class MockCtx:
    def __init__(self, room_id, token):
        self.videosdk_auth = token
        self.room_options = RoomOptions(room_id=room_id)

async def main():
    room_id = os.getenv("VIDEOSDK_MEETING_ID", "default_room")
    token = os.getenv("VIDEOSDK_TOKEN", "")
    
    if not token:
        print("Please configure VIDEOSDK_TOKEN in your environment or .env file.")
        sys.exit(1)
        
    ctx = MockCtx(room_id, token)
    loop = asyncio.get_event_loop()
    
    cleanup = await setup_console_room_client_for_ctx(ctx, room_id, loop)
    
    try:
        while True:
            await asyncio.sleep(1)
    except KeyboardInterrupt:
        print("Stopping console agent...")
    finally:
        await cleanup()

if __name__ == "__main__":
    asyncio.run(main())
