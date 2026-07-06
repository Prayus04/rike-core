import sqlite3
from pathlib import Path
from typing import Optional


MEMORY_DB_PATH = Path("/data/rike_memory.db")


def get_connection():
    connection = sqlite3.connect(MEMORY_DB_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def initialize_memory_database():
    MEMORY_DB_PATH.parent.mkdir(parents=True, exist_ok=True)

    with get_connection() as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS conversation_messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                conversation_id TEXT NOT NULL,
                role TEXT NOT NULL,
                message TEXT NOT NULL,
                model TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
            """
        )

        connection.execute(
            """
            CREATE INDEX IF NOT EXISTS idx_conversation_messages_conversation_id
            ON conversation_messages (conversation_id)
            """
        )


def save_message(
    conversation_id: str,
    role: str,
    message: str,
    model: Optional[str] = None
):
    initialize_memory_database()

    with get_connection() as connection:
        cursor = connection.execute(
            """
            INSERT INTO conversation_messages (
                conversation_id,
                role,
                message,
                model
            )
            VALUES (?, ?, ?, ?)
            """,
            (
                conversation_id,
                role,
                message,
                model
            )
        )

        message_id = cursor.lastrowid

        saved_message = connection.execute(
            """
            SELECT
                id,
                conversation_id,
                role,
                message,
                model,
                created_at
            FROM conversation_messages
            WHERE id = ?
            """,
            (message_id,)
        ).fetchone()

        return dict(saved_message)


def get_conversation_history(
    conversation_id: str = "default",
    limit: int = 20
):
    initialize_memory_database()

    with get_connection() as connection:
        rows = connection.execute(
            """
            SELECT
                id,
                conversation_id,
                role,
                message,
                model,
                created_at
            FROM conversation_messages
            WHERE conversation_id = ?
            ORDER BY id DESC
            LIMIT ?
            """,
            (
                conversation_id,
                limit
            )
        ).fetchall()

        messages = [
            dict(row)
            for row in rows
        ]

        messages.reverse()

        return messages


def clear_conversation(conversation_id: str = "default"):
    initialize_memory_database()

    with get_connection() as connection:
        cursor = connection.execute(
            """
            DELETE FROM conversation_messages
            WHERE conversation_id = ?
            """,
            (conversation_id,)
        )

        return cursor.rowcount
