from fastapi import FastAPI

from app.api.health import router as healthRouter
from app.api.chat import router as chatRouter

app = FastAPI(
    title="Rike Core",
    description="Central AI service for Project Rike",
    version="0.1.0"
)

app.include_router(healthRouter)
app.include_router(chatRouter)
