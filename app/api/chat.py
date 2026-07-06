from fastapi import APIRouter, HTTPException

from app.models.chat import ChatRequest, ChatResponse
from app.services.chat_service import chat


router = APIRouter(tags=["Chat"])


@router.post("/chat", response_model=ChatResponse)
async def chatEndpoint(request: ChatRequest):
    try:
        result = chat(
            message=request.message,
            model=request.model,
            conversation_id=request.conversation_id,
            use_memory=request.use_memory
        )

        return ChatResponse(**result)

    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error))
