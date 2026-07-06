from fastapi import APIRouter

from app.models.memory import (
    MemoryCreateRequest,
    ConversationHistoryResponse
)
from app.services.memory_service import (
    save_message,
    get_conversation_history,
    clear_conversation
)


router = APIRouter(prefix="/memory", tags=["Memory"])


@router.get("/{conversation_id}", response_model=ConversationHistoryResponse)
async def get_memory(conversation_id: str):
    messages = get_conversation_history(conversation_id)

    return ConversationHistoryResponse(
        conversation_id=conversation_id,
        messages=messages
    )


@router.post("")
async def create_memory(request: MemoryCreateRequest):
    saved_message = save_message(
        conversation_id=request.conversation_id,
        role=request.role,
        message=request.message,
        model=request.model
    )

    return {
        "saved_message": saved_message
    }


@router.delete("/{conversation_id}")
async def delete_memory(conversation_id: str):
    deleted_count = clear_conversation(conversation_id)

    return {
        "conversation_id": conversation_id,
        "deleted_messages": deleted_count
    }
