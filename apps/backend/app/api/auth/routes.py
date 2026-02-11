from datetime import timedelta
import os
from arq import create_pool
from arq.connections import RedisSettings
from dotenv import load_dotenv
from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from app.db.models import Meeting, Status, User
from app.db.get_db import get_db
from fastapi.exceptions import HTTPException

from app.api.meetings.utils.list_events import list_calender_events
from app.api.auth.utils.webhook_subscribe import subscribe_to_calender_webhook

load_dotenv()

redis_dsn = os.getenv("REDIS_URL", "redis://minutesai-redis:6379")

auth_router = APIRouter(prefix='/auth')

@auth_router.post('/clerk/signup')
async def clerk_signup(request:Request,db:Session=Depends(get_db)):

    payload = await request.json()

    data = payload["data"]
    id = data["id"]
    try:

        email = data["email_addresses"][0]["email_address"]
    except Exception as e:
        raise HTTPException(500,"No email Found")


    user = db.query(User).filter((User.external_auth_id ==id)|(User.email==email)).first()
    if not user:
        print("User not exists on db. adding user.")

        user = User(email=email,external_auth_id=id)
        db.add(user)
        db.commit()
        db.refresh(user)

        print("user added succesfully")
        events = await list_calender_events(id)
        meeting_job_queue = await create_pool(RedisSettings.from_dsn(redis_dsn))

        for evnt in events:

            meeting_row= Meeting(user_id=user.id,link=evnt["url"],status=Status.not_started)
            db.add(meeting_row)
            db.commit()
            db.refresh(meeting_row)

            await meeting_job_queue.enqueue_job("join_meeting",{
                "user_id":str(user.id),
                "meet-link":meeting_row.link,
                "meeting_id":meeting_row.id,
            },
            _defer_until=evnt["start_time"] - timedelta(minutes=2)
            )
        
        await subscribe_to_calender_webhook(user_id=user.id,clerk_id=user.external_auth_id,db=db)

    else:
        print("User already exists on db")

    return {
        "message": "User verified successfully",
        "clerk_user_id": id,
        "user": email,
    }


