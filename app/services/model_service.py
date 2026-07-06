import json
import requests
from pathlib import Path

from app.core.config import settings
from app.models.model import ModelRegistry, RegisteredModel


MODEL_REGISTRY_PATH = Path("/data/models.json")


def load_model_registry() -> ModelRegistry:
    if not MODEL_REGISTRY_PATH.exists():
        registry = ModelRegistry(
            default_chat_model="llama3.2:1b",
            models=[
                RegisteredModel(
                    name="llama3.2:1b",
                    enabled=True,
                    purpose="general",
                    notes="Default lightweight chat model."
                )
            ]
        )
        save_model_registry(registry)

    data = json.loads(MODEL_REGISTRY_PATH.read_text())
    return ModelRegistry(**data)


def save_model_registry(registry: ModelRegistry):
    MODEL_REGISTRY_PATH.write_text(
        json.dumps(registry.model_dump(), indent=2)
    )


def get_installed_ollama_models():
    response = requests.get(
        f"{settings.ollamaBaseUrl}/api/tags",
        timeout=30
    )

    response.raise_for_status()

    data = response.json()

    return [
        model["name"]
        for model in data.get("models", [])
    ]


def get_registered_models():
    registry = load_model_registry()
    return registry.models


def get_enabled_models():
    registry = load_model_registry()
    return [
        model.name
        for model in registry.models
        if model.enabled
    ]


def get_default_model():
    registry = load_model_registry()
    return registry.default_chat_model


def validate_model(model_name: str):
    registry = load_model_registry()

    for model in registry.models:
        if model.name == model_name and model.enabled:
            return model_name

    raise ValueError(f"Model is not enabled or registered: {model_name}")


def set_default_model(model_name: str):
    validate_model(model_name)

    registry = load_model_registry()
    registry.default_chat_model = model_name
    save_model_registry(registry)

    return model_name


def sync_models_from_ollama():
    registry = load_model_registry()
    installed_models = get_installed_ollama_models()

    registered_names = {
        model.name
        for model in registry.models
    }

    added_models = []

    for model_name in installed_models:
        if model_name not in registered_names:
            registry.models.append(
                RegisteredModel(
                    name=model_name,
                    enabled=False,
                    purpose="unknown",
                    notes="Synced from Ollama. Review before enabling."
                )
            )
            added_models.append(model_name)

    save_model_registry(registry)

    return {
        "installed_models": installed_models,
        "added_models": added_models,
        "registered_models": registry.models
    }


def enable_model(model_name: str):
    registry = load_model_registry()

    for model in registry.models:
        if model.name == model_name:
            model.enabled = True
            save_model_registry(registry)
            return model

    raise ValueError(f"Model is not registered: {model_name}")


def disable_model(model_name: str):
    registry = load_model_registry()

    if registry.default_chat_model == model_name:
        raise ValueError("Cannot disable the default chat model.")

    for model in registry.models:
        if model.name == model_name:
            model.enabled = False
            save_model_registry(registry)
            return model

    raise ValueError(f"Model is not registered: {model_name}")
