from uuid import UUID
from arq.connections import RedisSettings
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api.meetings.schemas import MeetJoinIn
from app.api.auth.utils.isSignedin import verify_clerk_user
from arq import create_pool
from app.db.get_db import get_db
import os
from dotenv import load_dotenv

from app.db.models import Meeting, Status, User

load_dotenv()

redis_dsn = os.getenv("REDIS_URL", "redis://minutesai-redis:6379")

meet_router = APIRouter(prefix='/meet')

@meet_router.post('/join')
async def join_meet(request:MeetJoinIn,auth_user=Depends(verify_clerk_user),db:Session=Depends(get_db)):

    if not request.link.startswith("https://meet.google.com/"):
        raise HTTPException(500,"Enter a valid google meet url")
    
    user:User = db.query(User).filter(User.external_auth_id == auth_user["clerk_user_id"]).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    meeting_row = Meeting(bucket="minutesai-storage",status=Status.not_started,user_id=user.id,link=request.link)

    db.add(meeting_row)
    db.commit()
    db.refresh(meeting_row)

    meeting_job_queue = await create_pool(RedisSettings.from_dsn(redis_dsn))

    await meeting_job_queue.enqueue_job("join_meeting",{
        "meet-link":request.link,
        "meeting_id":meeting_row.id,
    })

    return {
        "meeting_id":meeting_row.id,
        "meet_link":meeting_row.link
    }
    