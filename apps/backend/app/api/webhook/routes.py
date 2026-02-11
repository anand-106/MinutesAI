import pprint
from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from app.db.get_db import get_db

webhook_router  = APIRouter(prefix="/webhook")


@webhook_router.post('/google-calendar')
async def google_calender_webhook(req:Request,db:Session=Depends(get_db)):

    headers = dict(req.headers)
    print("HEADERS:")
    print(headers)


    body = await req.body()
    print("RAW BODY:")
    print(body)


    try:
        json_body = await req.json()
        print("JSON BODY:")
        print(json_body)
    except:
        print("No JSON body")

    return {"status": "received"}