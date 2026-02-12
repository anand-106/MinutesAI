from datetime import datetime, timezone
import httpx
from app.api.auth.utils.get_google_token import get_google_token


async def list_calender_events(user_id:str):

    token = await get_google_token(user_id)

    async with httpx.AsyncClient() as client:

        resp = await client.get(
            url="https://www.googleapis.com/calendar/v3/calendars/primary/events",
            headers={
                "Authorization": f"Bearer {token}"
            },
            params = {
                "singleEvents": True
            }
        )

        if resp.status_code !=200:
            raise Exception(f"Google API error: {resp.text}")
        
        events =  resp.json()

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
