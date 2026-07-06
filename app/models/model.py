from pydantic import BaseModel
from typing import List, Optional


class RegisteredModel(BaseModel):
    name: str
    enabled: bool = False
    purpose: str = "unknown"
    notes: Optional[str] = None


class ModelRegistry(BaseModel):
    default_chat_model: str
    models: List[RegisteredModel]


class ModelNameRequest(BaseModel):
    model: str
