from datetime import datetime, timedelta, timezone
import pprint
from arq import create_pool
from arq.connections import RedisSettings
from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from app.db.get_db import get_db
from app.db.models import CalendarWebhook, Meeting, Status
from dotenv import load_dotenv
import os
from app.api.webhook.utils.fetch_new_events import fetch_new_events

load_dotenv()

webhook_router  = APIRouter(prefix="/webhook")

WEBHOOK_SECRET=os.getenv("WEBHOOK_SECRET")
redis_dsn = os.getenv("REDIS_URL", "redis://minutesai-redis:6379")

@webhook_router.post('/google-calendar')
async def google_calender_webhook(req:Request,db:Session=Depends(get_db)):

    headers = dict(req.headers)

    pprint.pprint(headers)
    
    webhook_token = headers.get("x-goog-channel-token")
    channel_id = headers.get("x-goog-channel-id")
    resource_id = headers.get("x-goog-resource-id")
    resource_uri = headers.get("x-goog-resource-uri")
    resource_state = headers.get("x-goog-resource-state")

    if resource_state != "exists":
        return {"status": "ignored"}

    if webhook_token != WEBHOOK_SECRET:
        raise HTTPException(403,"Invalid request")

    webhook = db.query(CalendarWebhook).filter(CalendarWebhook.channel_id==channel_id,CalendarWebhook.resource_id==resource_id,CalendarWebhook.resource_uri==resource_uri).first()


    if not webhook:
        raise HTTPException(404,"WebHook not found.")
    

    events = await fetch_new_events(webhook,webhook.user.external_auth_id)

    meeting_job_queue = await create_pool(RedisSettings.from_dsn(redis_dsn))

    sync_token = None

    for evnt in events:

        existing = (
            db.query(Meeting)
            .filter(
                Meeting.user_id == webhook.user_id,
                Meeting.link == evnt["url"],   
            )
            .first()
        )

        if existing:
            continue

        scheduled_at = evnt["start_time"] - timedelta(minutes=2)
        now_utc = datetime.now(timezone.utc)

        if scheduled_at <= now_utc:
            continue

        meeting_row= Meeting(user_id=webhook.user_id,link=evnt["url"],status=Status.not_started)
        db.add(meeting_row)
        db.commit()
        db.refresh(meeting_row)

        sync_token=evnt["sync_token"]

        await meeting_job_queue.enqueue_job(
            "join_meeting",
            {
                "user_id": str(webhook.user_id),
                "meet-link": meeting_row.link,
                "meeting_id": meeting_row.id,
            },
            _defer_until=scheduled_at,
        )
    
    webhook.sync_token = sync_token
    db.commit()

    return {"status": "received"}