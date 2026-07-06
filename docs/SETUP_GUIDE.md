# Project Rike Setup Guide

This guide documents the requirements and steps needed to run Project Rike up to the current Phase 3 state.

## 1. Current Project State

Project Rike currently includes:

- Debian server foundation
- Docker Engine and Docker Compose
- Portainer CE
- NVIDIA driver and CUDA support
- Ollama container
- Rike Core FastAPI container
- Controlled model registry
- SQLite conversation memory

Current development stage:

```text
Phase 3: Intelligence
```

Implemented Phase 3 items:

- Ollama deployed with GPU acceleration
- Rike Core connected to Ollama
- Model configuration and registry added
- SQLite memory for conversations added

Not yet implemented:

- Streaming responses
- Semantic memory
- Tool router
- WebUI container
- Authentication
- Reverse proxy
- Remote access through Tailscale

---

## 2. Hardware Requirements

Current target hardware:

```text
CPU: Intel Core i5-8400
GPU: GTX 1050 Ti 4GB
RAM: 12 GB DDR4
Primary SSD: 256 GB ext4
Secondary HDD: 1 TB ext4 mounted at /srv/storage
```

The system is designed for lightweight local models first. Larger models should be tested carefully because of the 4 GB VRAM limit.

---

## 3. Host Software Requirements

Required host software:

```text
Debian 13
Docker Engine
Docker Compose
Git
curl
wget
nano or vim
jq
tree
tmux
NVIDIA driver
CUDA Toolkit
NVIDIA Persistence Daemon
OpenSSH Server
Portainer CE
```

Recommended monitoring tools:

```text
htop
btop
nvtop
smartmontools
lm-sensors
ncdu
```

---

## 4. Required Directory Layout

Infrastructure repositories and Compose files live under:

```text
/opt/rike
```

Persistent data lives under:

```text
/srv/storage/docker-data
```

Important folders:

```text
/opt/rike/rike-core
/opt/rike/ollama
/srv/storage/docker-data/rike-core
/srv/storage/docker-data/ollama
```

Do not store runtime data, databases, model files, or service state directly inside `/opt/rike`.

---

## 5. Docker Network

Create the shared Docker network:

```bash
docker network create rike-network
```

Rike Core and Ollama should both be attached to this network.

---

## 6. Ollama Setup

Create folders:

```bash
sudo mkdir -p /opt/rike/ollama
sudo mkdir -p /srv/storage/docker-data/ollama
sudo chown -R $USER:$USER /opt/rike/ollama
sudo chown -R $USER:$USER /srv/storage/docker-data/ollama
cd /opt/rike/ollama
```

Example `compose.yml`:

```yaml
services:
  ollama:
    image: ollama/ollama:latest
    container_name: ollama
    restart: unless-stopped
    ports:
      - "11434:11434"
    volumes:
      - /srv/storage/docker-data/ollama:/root/.ollama
    networks:
      - rike-network
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: all
              capabilities: [gpu]

networks:
  rike-network:
    external: true
```

Start Ollama:

```bash
docker compose up -d
```

Check status:

```bash
docker compose ps
curl http://localhost:11434/api/tags
```

---

## 7. Pull Initial Models

Current recommended models:

```bash
docker exec -it ollama ollama pull llama3.2:1b
docker exec -it ollama ollama pull llama3.2:3b
docker exec -it ollama ollama pull qwen2.5:3b
```

Optional future models:

```bash
docker exec -it ollama ollama pull deepseek-r1:1.5b
docker exec -it ollama ollama pull nomic-embed-text
```

---

## 8. Rike Core Setup

Create folders:

```bash
sudo mkdir -p /opt/rike/rike-core
sudo mkdir -p /srv/storage/docker-data/rike-core
sudo chown -R $USER:$USER /opt/rike/rike-core
sudo chown -R $USER:$USER /srv/storage/docker-data/rike-core
cd /opt/rike/rike-core
```

Expected structure:

```text
/opt/rike/rike-core
├── app/
│   ├── api/
│   ├── core/
│   ├── models/
│   ├── services/
│   └── main.py
├── Dockerfile
├── compose.yml
├── requirements.txt
├── README.md
├── .env
├── .env.example
└── .gitignore
```

---

## 9. Rike Core Requirements

`requirements.txt`:

```txt
fastapi
uvicorn[standard]
python-dotenv
pydantic-settings
requests
```

---

## 10. Rike Core Environment

`.env.example`:

```env
RIKE_ENV=development
RIKE_HOST=0.0.0.0
RIKE_PORT=8000
RIKE_DATA_DIR=/data

OLLAMA_BASE_URL=http://ollama:11434
OLLAMA_MODEL=llama3.2:1b
```

Create the real `.env`:

```bash
cp .env.example .env
```

---

## 11. Rike Core Compose File

`compose.yml`:

```yaml
services:
  rike-core:
    build: .
    container_name: rike-core
    restart: unless-stopped
    env_file:
      - .env
    ports:
      - "8000:8000"
    volumes:
      - /srv/storage/docker-data/rike-core:/data
    networks:
      - rike-network

networks:
  rike-network:
    external: true
```

---

## 12. Run Rike Core

From:

```bash
cd /opt/rike/rike-core
```

Build and start:

```bash
docker compose up -d --build
```

Check status:

```bash
docker compose ps
docker logs -f rike-core
```

---

## 13. Model Registry

Rike stores model registry data at:

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

Sync installed Ollama models into Rike:

```bash
curl -X POST http://localhost:8000/models/sync
```

Enable a model:

```bash
curl -X POST http://localhost:8000/models/enable \
  -H "Content-Type: application/json" \
  -d '{"model":"llama3.2:3b"}'
```

Set default model:

```bash
curl -X POST http://localhost:8000/models/default \
  -H "Content-Type: application/json" \
  -d '{"model":"llama3.2:3b"}'
```

---

## 14. SQLite Memory

Rike stores conversation memory at:

```text
/data/rike_memory.db
```

Host path:

```text
/srv/storage/docker-data/rike-core/rike_memory.db
```

Current table:

```text
conversation_messages
├── id
├── conversation_id
├── role
├── message
├── model
└── created_at
```

This is conversation memory only. Semantic memory comes later.

---

## 15. Test Commands

Health check:

```bash
curl http://localhost:8000/health
```

Basic chat:

```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message":"Hello Rike."}'
```

Chat with a specific model:

```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message":"Hello from Qwen.","model":"qwen2.5:3b"}'
```

Chat with memory:

```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{
    "conversation_id":"test",
    "message":"My favorite project is Rike. Remember that."
  }'
```

Ask from the same conversation:

```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{
    "conversation_id":"test",
    "message":"What is my favorite project?"
  }'
```

View memory:

```bash
curl http://localhost:8000/memory/test
```

Clear memory:

```bash
curl -X DELETE http://localhost:8000/memory/test
```

---

## 16. API Docs

FastAPI Swagger UI:

```text
http://SERVER_IP:8000/docs
```

---

## 17. Git Workflow

From:

```bash
cd /opt/rike/rike-core
```

Use:

```bash
git status
git add .
git commit -m "Add model registry and SQLite conversation memory"
```

---

## 18. Next Setup Tasks

Recommended next implementation order:

```text
1. Better Ollama error handling
2. Streaming chat responses
3. Model metadata editing
4. Memory summaries
5. Semantic memory with nomic-embed-text
6. Tool router
7. Open WebUI container
8. Homepage dashboard
9. Tailscale
10. Caddy reverse proxy
```
