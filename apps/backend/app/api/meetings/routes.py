from arq.connections import RedisSettings
from fastapi import APIRouter, Depends
from app.api.meetings.schemas import MeetJoinIn
from app.api.auth.utils.isSignedin import verify_clerk_user
from arq import create_pool
import os
from dotenv import load_dotenv

load_dotenv()

redis_dsn = os.getenv("REDIS_URL", "redis://minutesai-redis:6379")

meet_router = APIRouter(prefix='/meet')

@meet_router.post('/join')
async def join_meet(request:MeetJoinIn,auth_user=Depends(verify_clerk_user)):

    meeting_job_queue = await create_pool(RedisSettings.from_dsn(redis_dsn))

    await meeting_job_queue.enqueue_job("join_meeting",{
        "meet-link":request.link
    })
    