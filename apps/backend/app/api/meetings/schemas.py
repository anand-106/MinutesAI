from pydantic import BaseModel, ConfigDict

from app.db.models import Status


class MeetJoinIn(BaseModel):
    link:str

class GetMeetingsOut(BaseModel):
    key:str
    link:str
    upload_id:str
    status:Status

    model_config=ConfigDict(from_attributes=True)