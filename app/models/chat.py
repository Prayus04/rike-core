from pydantic import BaseModel
from typing import Optional


class ChatRequest(BaseModel):
    message: str
    model: Optional[str] = None
    conversation_id: str = "default"
    use_memory: bool = True


class ChatResponse(BaseModel):
    response: str
    model: str
    conversation_id: str
