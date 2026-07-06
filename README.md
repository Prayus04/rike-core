# Project Rike

Project Rike is a self-hosted local AI platform built on a Debian server. It uses Docker Compose, FastAPI, Ollama, local language models, a controlled model registry, and SQLite conversation memory.

## Current Stage

Rike is currently in Phase 3: Intelligence.

Completed:

- Debian server foundation
- Docker and Portainer setup
- Rike Core FastAPI service
- Ollama container with GPU support
- Local model registry
- SQLite conversation memory

## Main Services

| Service | Purpose | Port |
|---|---|---|
| `rike-core` | FastAPI orchestration service | `8000` |
| `ollama` | Local AI model runtime | `11434` |
| `portainer` | Container management UI | configured separately |

## Quick Start

```bash
cd /opt/rike/rike-core
docker compose up -d --build
```

Check health:

```bash
curl http://localhost:8000/health
```

API docs:

```text
http://SERVER_IP:8000/docs
```

## Documentation

- `docs/SETUP_GUIDE.md`
- `docs/SOFTWARE_ARCHITECTURE.md`
- `docs/API_REFERENCE.md`
- `docs/MODEL_REGISTRY.md`
- `docs/MEMORY_ARCHITECTURE.md`
- `docs/OPERATIONS.md`
