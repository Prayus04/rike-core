from fastapi import APIRouter

from app.services.chat_service import chat

router = APIRouter(tags=["Chat"])


@router.post("/chat")
async def chatEndpoint():

    response = chat()

    return {
        "response": response
    }
