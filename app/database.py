import json
import sqlite3
import uuid
from datetime import datetime, timezone
from pathlib import Path

DB_PATH = Path("notice_negotiator.db")


def get_connection() -> sqlite3.Connection:
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def init_db() -> None:
    with get_connection() as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS scenarios (
                id TEXT PRIMARY KEY,
                payload TEXT NOT NULL,
                score INTEGER NOT NULL,
                created_at TEXT NOT NULL
            )
            """
        )
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS feedback (
                id TEXT PRIMARY KEY,
                scenario_id TEXT NOT NULL,
                outcome TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
            """
        )
        connection.commit()


def save_scenario(payload: dict, score: int) -> str:
    scenario_id = str(uuid.uuid4())
    created_at = datetime.now(timezone.utc).isoformat()

    with get_connection() as connection:
        connection.execute(
            """
            INSERT INTO scenarios (id, payload, score, created_at)
            VALUES (?, ?, ?, ?)
            """,
            (scenario_id, json.dumps(payload), score, created_at),
        )
        connection.commit()

    return scenario_id


def save_feedback(scenario_id: str, outcome: str) -> str:
    feedback_id = str(uuid.uuid4())
    created_at = datetime.now(timezone.utc).isoformat()

    with get_connection() as connection:
        connection.execute(
            """
            INSERT INTO feedback (id, scenario_id, outcome, created_at)
            VALUES (?, ?, ?, ?)
            """,
            (feedback_id, scenario_id, outcome, created_at),
        )
        connection.commit()

    return feedback_id
