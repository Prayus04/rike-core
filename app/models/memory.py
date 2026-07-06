from pydantic import BaseModel
from typing import List, Optional


class MemoryMessage(BaseModel):
    id: int
    conversation_id: str
    role: str
    message: str
    model: Optional[str] = None
    created_at: str


class MemoryCreateRequest(BaseModel):
    conversation_id: str = "default"
    role: str
    message: str
    model: Optional[str] = None


class ConversationHistoryResponse(BaseModel):
    conversation_id: str
    messages: List[MemoryMessage]
