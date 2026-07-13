"""Data access for manual apply tracking -- the Phase 5 data model. See
docs/application-workflow.md.

Plain SQL, no ORM -- consistent with app/db.py, app/profile_data.py, and
app/jobs_data.py. One application row per job for the MVP (upserted by
job_id) -- see schema.sql.
"""
from __future__ import annotations

import sqlite3
from typing import Any

from app.db import get_connection

APPLICATION_FIELDS = [
    "application_date",
    "application_url",
    "contact_person",
    "outcome",
    "notes",
    "follow_up_date",
]

OUTCOME_CHOICES = ["pending", "interview", "offer", "rejected", "withdrawn"]


def get_application_by_job(job_id: int) -> sqlite3.Row | None:
    with get_connection() as conn:
        return conn.execute("SELECT * FROM applications WHERE job_id = ?", (job_id,)).fetchone()


def upsert_application(job_id: int, fields: dict[str, Any]) -> None:
    columns = [f for f in APPLICATION_FIELDS if f in fields]
    with get_connection() as conn:
        existing = conn.execute("SELECT id FROM applications WHERE job_id = ?", (job_id,)).fetchone()
        if existing:
            assignments = ", ".join(f"{c} = :{c}" for c in columns)
            conn.execute(
                f"UPDATE applications SET {assignments}, updated_at = datetime('now') WHERE job_id = :job_id",
                {**fields, "job_id": job_id},
            )
        else:
            insert_columns = ["job_id"] + columns
            placeholders = ", ".join(f":{c}" for c in insert_columns)
            conn.execute(
                f"INSERT INTO applications ({', '.join(insert_columns)}) VALUES ({placeholders})",
                {**fields, "job_id": job_id},
            )
        conn.commit()


def list_applications_with_jobs() -> list[sqlite3.Row]:
    with get_connection() as conn:
        return conn.execute(
            """
            SELECT applications.*, jobs.title AS job_title, jobs.company AS job_company
            FROM applications
            JOIN jobs ON jobs.id = applications.job_id
            ORDER BY applications.application_date DESC, applications.created_at DESC
            """
        ).fetchall()
