from fastapi import APIRouter, Depends
from app.api.meetings.schemas import MeetJoinIn
from app.api.auth.utils.isSignedin import verify_clerk_user

meet_router = APIRouter(prefix='/meet')

@meet_router.post('/join')
def join_meet(request:MeetJoinIn,auth_user=Depends(verify_clerk_user)):

    print(request.link)