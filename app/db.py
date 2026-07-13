"""Minimal SQLite setup for the Phase 1 code foundation.

Creates the database file and placeholder tables (see schema.sql) under
CAREER_HUB_BASE_PATH/database if they don't already exist. No ORM yet --
later phases can introduce SQLAlchemy models once the real schema is designed.
"""
from __future__ import annotations

import sqlite3
from contextlib import contextmanager
from pathlib import Path
from typing import Iterator

from app.config import settings

SCHEMA_PATH = Path(__file__).parent / "schema.sql"


def init_db() -> None:
    db_path = settings.database_path
    db_path.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(db_path) as conn:
        conn.executescript(SCHEMA_PATH.read_text())
        # candidate_profile and preferences are singletons (id=1) so forms always
        # have a row to load/update -- see docs/profile-and-preferences.md.
        conn.execute("INSERT OR IGNORE INTO candidate_profile (id) VALUES (1)")
        conn.execute("INSERT OR IGNORE INTO preferences (id) VALUES (1)")
        conn.execute("INSERT OR IGNORE INTO public_profile (id) VALUES (1)")
        conn.commit()


@contextmanager
def get_connection() -> Iterator[sqlite3.Connection]:
    db_path = settings.database_path
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()
