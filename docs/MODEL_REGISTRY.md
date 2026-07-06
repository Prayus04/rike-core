# Model Registry

The model registry controls which Ollama models Rike is allowed to use.

## Why This Exists

Rike should not blindly accept any model name from a chat request. Models must be installed, synced, reviewed, and enabled before use.

## Lifecycle

```text
Installed in Ollama
    ↓
Synced into Rike
    ↓
Registered but disabled
    ↓
Manually enabled
    ↓
Available for chat
```

## Registry File

Container path:

```text
/data/models.json
```

Host path:

```text
/srv/storage/docker-data/rike-core/models.json
```

Example:

```json
{
  "default_chat_model": "llama3.2:1b",
  "models": [
    {
      "name": "llama3.2:1b",
      "enabled": true,
      "purpose": "general",
      "notes": "Default lightweight chat model."
    }
  ]
}
```

## Current / Planned Models

| Model | Role | Status |
|---|---|---|
| `llama3.2:1b` | Lightweight default chat | Enabled |
| `llama3.2:3b` | Stronger general chat | Testing |
| `qwen2.5:3b` | Coding and reasoning | Testing |
| `deepseek-r1:1.5b` | Reasoning and planning | Planned |
| `nomic-embed-text` | Semantic memory embeddings | Future |

## Add a New Model

Pull into Ollama:

```bash
docker exec -it ollama ollama pull MODEL_NAME
```

Sync into Rike:

```bash
curl -X POST http://localhost:8000/models/sync
```

Review:

```bash
curl http://localhost:8000/models/registered
```

Enable:

```bash
curl -X POST http://localhost:8000/models/enable \
  -H "Content-Type: application/json" \
  -d '{"model":"MODEL_NAME"}'
```

Set as default:

```bash
curl -X POST http://localhost:8000/models/default \
  -H "Content-Type: application/json" \
  -d '{"model":"MODEL_NAME"}'
```
