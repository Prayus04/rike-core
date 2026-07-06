# API Reference

Base URL:

```text
http://SERVER_IP:8000
```

Swagger UI:

```text
http://SERVER_IP:8000/docs
```

## Health

### `GET /health`

Checks whether Rike Core is running.

Example:

```bash
curl http://localhost:8000/health
```

## Chat

### `POST /chat`

Sends a message to Rike Core.

Example:

```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message":"Hello Rike."}'
```

With model:

```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message":"Hello Qwen.","model":"qwen2.5:3b"}'
```

With memory:

```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"conversation_id":"test","message":"Remember that this project is Rike."}'
```

## Models

### `GET /models/installed`

Lists models installed in Ollama.

### `GET /models/registered`

Lists models registered in Rike.

### `GET /models/enabled`

Lists models enabled for chat.

### `POST /models/sync`

Syncs installed Ollama models into Rike's registry.

### `POST /models/enable`

Enables a registered model.

```bash
curl -X POST http://localhost:8000/models/enable \
  -H "Content-Type: application/json" \
  -d '{"model":"llama3.2:3b"}'
```

### `POST /models/disable`

Disables a registered model.

### `GET /models/default`

Gets the default chat model.

### `POST /models/default`

Sets the default chat model.

## Memory

### `GET /memory/{conversation_id}`

Returns stored messages for a conversation.

### `POST /memory`

Manually stores a memory message.

### `DELETE /memory/{conversation_id}`

Deletes all messages for a conversation.
