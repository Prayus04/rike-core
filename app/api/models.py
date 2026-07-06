from fastapi import APIRouter, HTTPException

from app.models.model import ModelNameRequest
from app.services.model_service import (
    get_installed_ollama_models,
    get_registered_models,
    get_enabled_models,
    get_default_model,
    set_default_model,
    sync_models_from_ollama,
    enable_model,
    disable_model
)

router = APIRouter(prefix="/models", tags=["Models"])


@router.get("/installed")
async def installed_models():
    return {
        "installed_models": get_installed_ollama_models()
    }


@router.get("/registered")
async def registered_models():
    return {
        "registered_models": get_registered_models()
    }


@router.get("/enabled")
async def enabled_models():
    return {
        "enabled_models": get_enabled_models()
    }


@router.get("/default")
async def default_model():
    return {
        "default_chat_model": get_default_model()
    }


@router.post("/default")
async def update_default_model(request: ModelNameRequest):
    try:
        model = set_default_model(request.model)
        return {
            "default_chat_model": model
        }

    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error))


@router.post("/sync")
async def sync_models():
    return sync_models_from_ollama()


@router.post("/enable")
async def enable_registered_model(request: ModelNameRequest):
    try:
        model = enable_model(request.model)
        return {
            "enabled_model": model
        }

    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error))


@router.post("/disable")
async def disable_registered_model(request: ModelNameRequest):
    try:
        model = disable_model(request.model)
        return {
            "disabled_model": model
        }

    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error))
