from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.auth.routes import auth_router
from app.api.meetings.routes import meet_router
from app.api.webhook.routes import webhook_router

from contextlib import asynccontextmanager
from app.db.models import Base
from app.db.session import engine

@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield

app = FastAPI(lifespan=lifespan)

app.add_middleware(CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(meet_router)
app.include_router(webhook_router)

@app.get('/health')
def health():
    return {"status":"ok"}