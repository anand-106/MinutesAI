import os
from fastapi import Request, HTTPException, Depends
from clerk_backend_api import Clerk
from clerk_backend_api.security import AuthenticateRequestOptions
from dotenv import load_dotenv
import jwt
from pydantic import BaseModel

load_dotenv()

clerk = Clerk(bearer_auth=os.getenv("CLERK_SECRET_KEY"))

class ClerkUser(BaseModel):
    clerk_user_id:str

async def verify_clerk_user(request: Request)->ClerkUser:
    auth_header = request.headers.get("authorization")
    if not auth_header:
        print(e)
        raise HTTPException(status_code=401, detail="Missing Authorization header")

    try:
        auth_state = clerk.authenticate_request(
            request,
            AuthenticateRequestOptions(authorized_parties=["http://localhost:3000","http://127.0.0.1:3000"])
        )
    except Exception as e:
        print(e)
        raise HTTPException(status_code=401, detail=f"Invalid Clerk token: {e}")

    if not auth_state.is_signed_in:
        print(f"no auth state {auth_state}")
        raise HTTPException(status_code=401, detail="User not signed in")

    user_id = auth_state.payload["sub"]
    return ClerkUser(clerk_user_id=user_id)



