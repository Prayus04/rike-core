# Software Architecture

Project Rike is a self-hosted local AI platform built around Docker, FastAPI, Ollama, and persistent local storage.

## Architectural Goals

- Privacy-first local AI
- Minimal host operating system
- Docker-first deployment
- Persistent data separated from infrastructure code
- Modular services
- Controlled model registry
- Progressive memory architecture

## System Context

```text
User / WebUI
    |
    v
Rike Core API
    |
    |-- Model Registry
    |-- Conversation Memory
    |-- Future Tool Router
    |
    v
Ollama
    |
    v
Local Models
```

## Main Components

| Component | Purpose |
|---|---|
| Rike Core | FastAPI orchestration layer |
| Ollama | Local model runtime |
| Model Registry | Controls which models Rike can use |
| SQLite Memory | Stores conversation history |
| Open WebUI | Planned primary interface |
| Portainer | Container management |

## Rike Core Layers

```text
API layer       HTTP endpoints
Service layer   business logic
Models layer    Pydantic schemas
Core layer      settings and logging
Persistence     SQLite and JSON files under /data
```

## Persistence

Runtime data is stored under:

```text
/srv/storage/docker-data
```

Infrastructure definitions and source files are stored under:

```text
/opt/rike
```

## Current Limitations

- No streaming responses yet
- No semantic memory yet
- No authentication yet
- No reverse proxy yet
- No Open WebUI container yet
- No tool router yet
