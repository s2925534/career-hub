"""Data access for the job tracker -- the Phase 3 data model. See
docs/application-workflow.md.

Plain SQL, no ORM -- consistent with app/db.py and app/profile_data.py.
"""
from __future__ import annotations

import sqlite3
from typing import Any

from app.db import get_connection

JOB_FIELDS = [
    "title",
    "company",
    "location",
    "url",
    "description",
    "source",
    "status",
    "notes",
    "follow_up_date",
]

SOURCE_CHOICES = ["manual", "pasted", "url"]

STATUS_CHOICES = [
    "interested",
    "drafting",
    "ready_to_apply",
    "applied",
    "interview",
    "offer",
    "rejected",
    "archived",
]


def list_jobs() -> list[sqlite3.Row]:
    with get_connection() as conn:
        return conn.execute("SELECT * FROM jobs ORDER BY created_at DESC").fetchall()


def get_job(job_id: int) -> sqlite3.Row | None:
    with get_connection() as conn:
        return conn.execute("SELECT * FROM jobs WHERE id = ?", (job_id,)).fetchone()


def list_jobs_by_status(status: str) -> list[sqlite3.Row]:
    with get_connection() as conn:
        return conn.execute(
            "SELECT * FROM jobs WHERE status = ? ORDER BY created_at DESC", (status,)
        ).fetchall()


def create_job(fields: dict[str, Any]) -> int:
    columns = [f for f in JOB_FIELDS if f in fields]
    placeholders = ", ".join(f":{c}" for c in columns)
    with get_connection() as conn:
        cursor = conn.execute(
            f"INSERT INTO jobs ({', '.join(columns)}) VALUES ({placeholders})",
            fields,
        )
        conn.commit()
        return cursor.lastrowid


def update_job(job_id: int, fields: dict[str, Any]) -> None:
    columns = [f for f in JOB_FIELDS if f in fields]
    assignments = ", ".join(f"{c} = :{c}" for c in columns)
    with get_connection() as conn:
        conn.execute(
            f"UPDATE jobs SET {assignments}, updated_at = datetime('now') WHERE id = :id",
            {**fields, "id": job_id},
        )
        conn.commit()
