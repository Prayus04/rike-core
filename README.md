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

## Planned Features

Project Rike is under active development. The current focus is building a modular, self-hosted AI platform with a strong software engineering foundation. Planned features include:

### AI & Intelligence
- Streaming responses from Ollama
- Semantic memory using embedding models
- Long-term memory and preference management
- Automatic model selection based on task type
- Support for additional local language models

### Tool Integration
- Modular tool routing system
- Notes and knowledge management
- Calendar integration
- Weather and web information tools
- Local system monitoring and diagnostics

### Infrastructure
- Open WebUI integration
- Homepage dashboard
- Caddy reverse proxy with HTTPS
- Tailscale remote access
- Automated backups and recovery workflows
- Improved logging and monitoring

### Platform Improvements
- Expanded REST API
- Comprehensive unit and integration testing
- Continuous Integration (GitHub Actions)
- Performance profiling and optimization
- Improved error handling and resilience
- Complete developer and API documentation
