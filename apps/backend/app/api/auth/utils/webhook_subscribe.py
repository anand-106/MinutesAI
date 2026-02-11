from datetime import datetime, timezone
from uuid import UUID
import httpx
from sqlalchemy.orm import Session
from app.api.auth.utils.get_google_token import get_google_token
from dotenv import load_dotenv
import os
from app.db.models import CalendarWebhook

load_dotenv()

WEBHOOK_SECRET=os.getenv("WEBHOOK_SECRET")

async def subscribe_to_calender_webhook(user_id:UUID,clerk_id:str,db:Session):

    token = await get_google_token(clerk_id)
    

    url = "https://www.googleapis.com/calendar/v3/calendars/primary/events/watch"

    headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json"
    }

    body = {
    "id": f"channel_{str(user_id)}",
    "type": "web_hook",
    "address": "https://likely-inspired-mite.ngrok-free.app/webhook/google-calendar",
    "token": WEBHOOK_SECRET
    }

    async with httpx.AsyncClient() as client:

        res = await client.post(url=url,headers=headers,json=body)

        if res.status_code != 200:
            raise Exception("Error subscribing to google calender")
        
        data = res.json()

        channel_id = data.get("id")
        resourceId = data.get("resourceId")
        resourceUri = data.get("resourceUri")

        expiration_ms = int(data.get("expiration"))
        expiration_dt = datetime.fromtimestamp(
            expiration_ms / 1000,
            tz=timezone.utc
        )
        
        webhook_row= CalendarWebhook(channel_id=channel_id,user_id=user_id,resource_id=resourceId,resource_uri=resourceUri,expiration=expiration_dt)
        db.add(webhook_row)
        db.commit()
        db.refresh(webhook_row)


        

