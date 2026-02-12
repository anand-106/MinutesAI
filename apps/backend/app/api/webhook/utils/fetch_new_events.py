from datetime import datetime, timezone
import httpx
from app.db.models import CalendarWebhook
from app.api.auth.utils.get_google_token import get_google_token


async def fetch_new_events(webhook:CalendarWebhook,clerk_id:str):

    token = await get_google_token(clerk_id)

    headers = {
        "Authorization": f"Bearer {token}"
    }

    params = {
        "syncToken": webhook.sync_token
    }

    async with httpx.AsyncClient() as client:
        res = await client.get(
            "https://www.googleapis.com/calendar/v3/calendars/primary/events",
            headers=headers,
            params=params
        )

    if res.status_code == 410:
        webhook.sync_token = None
        raise

    events = res.json()

    sync_token = events.get("nextSyncToken")

    meetings = []

    for itm in events.get("items", []):

        conferenceData = itm.get("conferenceData")
        if not conferenceData:
            continue
        entryPoints = itm["conferenceData"]["entryPoints"]

        start_time = itm["start"]["dateTime"]
        dt_local = datetime.fromisoformat(start_time)
        dt_utc = dt_local.astimezone(timezone.utc)

        for ep in entryPoints:
            if ep["entryPointType"] == "video":

                meetings.append(
                    {
                        "url":ep["uri"],
                        "start_time":dt_utc,
                        "sync_token":sync_token
                    }
                )

    return meetings