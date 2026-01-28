from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, ConfigDict

from app.db.models import Status


class MeetJoinIn(BaseModel):
    link:str

class GetMeetingsOut(BaseModel):
    id:UUID
    key:str
    link:str
    upload_id:str
    status:Status
    created_at:datetime
    duration_seconds:int

    model_config=ConfigDict(from_attributes=True)

class GetDialougesOut(BaseModel):
    id:UUID
    meeting_id:UUID
    speaker:str
    text:str
    start_time:int
    end_time:int
    sequence:int