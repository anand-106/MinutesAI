from uuid import UUID
from sqlalchemy.orm import Session
from typing_extensions import List
from arq.connections import RedisSettings
from fastapi import APIRouter, Depends, HTTPException
from app.api.meetings.schemas import GetMeetingsOut, MeetJoinIn
from app.api.auth.utils.isSignedin import ClerkUser, verify_clerk_user
from arq import create_pool
from app.db.get_db import get_db
import os
from dotenv import load_dotenv
from app.db.models import Meeting, Status, User
from app.s3.s3 import get_s3_presigned_url

load_dotenv()

redis_dsn = os.getenv("REDIS_URL", "redis://minutesai-redis:6379")

meet_router = APIRouter(prefix='/meetings')

@meet_router.post('/join')
async def join_meet(request:MeetJoinIn,auth_user:ClerkUser=Depends(verify_clerk_user),db:Session=Depends(get_db)):

    if not request.link.startswith("https://meet.google.com/"):
        raise HTTPException(500,"Enter a valid google meet url")
    
    user:User = db.query(User).filter(User.external_auth_id == auth_user.clerk_user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    meeting_row = Meeting(bucket="minutesai-storage",status=Status.not_started,user_id=user.id,link=request.link)

    db.add(meeting_row)
    db.commit()
    db.refresh(meeting_row)

    meeting_job_queue = await create_pool(RedisSettings.from_dsn(redis_dsn))

    await meeting_job_queue.enqueue_job("join_meeting",{
        "user_id":str(user.id),
        "meet-link":request.link,
        "meeting_id":meeting_row.id,
    })

    return {
        "meeting_id":meeting_row.id,
        "meet_link":meeting_row.link
    }


@meet_router.get("/",response_model=List[GetMeetingsOut])
def get_meetings(auth_user:ClerkUser=Depends(verify_clerk_user),db:Session=Depends(get_db)):

    try:
        user = db.query(User).filter(User.external_auth_id == auth_user.clerk_user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        meetings = db.query(Meeting).filter(Meeting.user_id == user.id).all()
        return meetings
    except Exception as e:
        print(e)
        raise HTTPException(500,f"Error getting meetings")

@meet_router.get('/{meeting_id}',response_model=GetMeetingsOut)
def get_meeting(meeting_id:UUID,auth_user:ClerkUser=Depends(verify_clerk_user),db:Session=Depends(get_db)):

    try:
        user = db.query(User).filter(User.external_auth_id == auth_user.clerk_user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        meeting = db.query(Meeting).filter(Meeting.user_id == user.id, Meeting.id == meeting_id).first()
        if not meeting:
            raise HTTPException(status_code=404, detail="Meeting not found")
        return meeting
    except Exception as e:
        print(e)
        raise HTTPException(500,f"Error getting meeting")

@meet_router.get('/{meeting_id}/presigned')
def get_presigned_url(meeting_id:UUID,auth_user:ClerkUser=Depends(verify_clerk_user),db:Session=Depends(get_db)):

        try:
            user = db.query(User).filter(User.external_auth_id == auth_user.clerk_user_id).first()
            if not user:
                raise HTTPException(status_code=404, detail="User not found")

            meeting = db.query(Meeting).filter(Meeting.user_id == user.id, Meeting.id == meeting_id).first()
            if not meeting:
                raise HTTPException(status_code=404, detail="Meeting not found")
            url = get_s3_presigned_url(key=meeting.key,content_type="video/mp4")

            return {
                "url":url
            }
        except Exception as e:
            print(e)
            raise HTTPException(500,f"Error getting meeting")