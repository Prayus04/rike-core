# Operations

This file contains basic operational notes for maintaining Project Rike.

## Check Containers

```bash
docker ps
docker compose ps
```

## Rike Core Logs

```bash
docker logs -f rike-core
```

## Ollama Logs

```bash
docker logs -f ollama
```

## Restart Rike Core

```bash
cd /opt/rike/rike-core
docker compose restart
```

## Rebuild Rike Core

```bash
cd /opt/rike/rike-core
docker compose up -d --build
```

## Restart Ollama

```bash
cd /opt/rike/ollama
docker compose restart
```

## Check Installed Models

```bash
curl http://localhost:11434/api/tags
```

## Check Rike Health

```bash
curl http://localhost:8000/health
```

## Data to Back Up

Important persistent data:

```text
/srv/storage/docker-data/rike-core
/srv/storage/docker-data/ollama
/srv/storage/docker-data/portainer
```

Important infrastructure files:

```text
/opt/rike
```

## Recommended Backup Priority

1. `/opt/rike`
2. `/srv/storage/docker-data/rike-core`
3. `/srv/storage/docker-data/portainer`
4. Other service data
5. Ollama models if storage allows

Ollama models can be re-downloaded, so they are lower priority than Rike Core memory and configuration.

## Update Policy

- Host OS security updates: monthly
- Docker image updates: manually validate first
- Infrastructure changes: commit with Git
- Major changes: document in `docs/`
