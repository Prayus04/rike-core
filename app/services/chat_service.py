import requests

from app.core.config import settings
from app.services.model_service import get_default_model, validate_model
from app.services.memory_service import (
    save_message,
    get_conversation_history
)


def build_prompt(message: str, conversation_id: str):
    history = get_conversation_history(
        conversation_id=conversation_id,
        limit=10
    )

    if not history:
        return message

    history_text = ""

    for item in history:
        role = item["role"]
        content = item["message"]
        history_text += f"{role}: {content}\n"

    prompt = f"""
You are Rike, a local self-hosted AI assistant.

Use the conversation history below for context.

Conversation history:
{history_text}

Current user message:
user: {message}

Assistant response:
"""

    return prompt.strip()


def chat(
    message: str,
    model: str | None = None,
    conversation_id: str = "default",
    use_memory: bool = True
):
    selected_model = model or get_default_model()
    validate_model(selected_model)

    if use_memory:
        save_message(
            conversation_id=conversation_id,
            role="user",
            message=message,
            model=selected_model
        )

        prompt = build_prompt(
            message=message,
            conversation_id=conversation_id
        )

    else:
        prompt = message

    payload = {
        "model": selected_model,
        "prompt": prompt,
        "stream": False
    }

    response = requests.post(
        f"{settings.ollamaBaseUrl}/api/generate",
        json=payload,
        timeout=120
    )

    response.raise_for_status()

    data = response.json()
    assistant_response = data.get("response", "")

    if use_memory:
        save_message(
            conversation_id=conversation_id,
            role="assistant",
            message=assistant_response,
            model=selected_model
        )

    return {
        "response": assistant_response,
        "model": selected_model,
        "conversation_id": conversation_id
    }
