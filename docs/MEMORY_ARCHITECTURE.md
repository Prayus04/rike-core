# Memory Architecture

Rike currently uses SQLite conversation memory.

## Current Memory Type

The current implementation stores recent conversation history by `conversation_id`.

This is useful for:

- Remembering context inside a conversation
- Reviewing previous messages
- Keeping lightweight persistent chat history

It is not yet semantic long-term memory.

## Database Location

Container path:

```text
/data/rike_memory.db
```

Host path:

```text
/srv/storage/docker-data/rike-core/rike_memory.db
```

## Current Table

```text
conversation_messages
├── id INTEGER PRIMARY KEY AUTOINCREMENT
├── conversation_id TEXT NOT NULL
├── role TEXT NOT NULL
├── message TEXT NOT NULL
├── model TEXT
└── created_at DATETIME DEFAULT CURRENT_TIMESTAMP
```

## How Chat Uses Memory

When memory is enabled:

```text
1. User message is stored.
2. Recent conversation messages are fetched.
3. Prompt is built using recent history.
4. Ollama generates a response.
5. Assistant response is stored.
```

## Future Semantic Memory

Future semantic memory should add:

- Embeddings with `nomic-embed-text`
- Vector search
- Memory summaries
- Preference storage
- Long-term retrieval by meaning
