from clerk_backend_api import Clerk
import os
from dotenv import load_dotenv

load_dotenv()

clerk = Clerk(bearer_auth=os.getenv("CLERK_SECRET_KEY"))

async def get_google_token(user_id:str):

    tokens = await clerk.users.get_o_auth_access_token_async(user_id=user_id,provider="google")

    if not tokens  or len(tokens) == 0:
        raise Exception("Oauth not found...")
    
    print(tokens[0].token)
    return tokens[0].token


import asyncio

if __name__ == "__main__":
    asyncio.run(get_google_token("user_38Sm6SDOejq7KboSKrAXQsjW3ic"))