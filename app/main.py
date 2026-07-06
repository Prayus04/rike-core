from fastapi import FastAPI

from app.api.health import router as healthRouter
from app.api.chat import router as chatRouter
from app.api.models import router as modelsRouter
from app.api.memory import router as memoryRouter
from app.services.memory_service import initialize_memory_database


app = FastAPI(
    title="Rike Core",
    description="Central AI service for Project Rike",
    version="0.1.0"
)


@app.on_event("startup")
async def startup():
    initialize_memory_database()


app.include_router(healthRouter)
app.include_router(chatRouter)
app.include_router(modelsRouter)
app.include_router(memoryRouter)
