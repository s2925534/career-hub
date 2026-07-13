"""Data access for the public CV site's structured content -- the Phase 6
data model. See docs/public-cv-site.md and docs/profile-and-preferences.md
("Public Profile Fields").

Plain SQL, no ORM -- consistent with the rest of the app. public_profile is a
singleton (id=1), like candidate_profile/preferences. work_experiences and
projects are lists with a visibility column, like skills -- PUBLIC_VISIBILITIES
is what the public site routes filter on.
"""
from __future__ import annotations

import sqlite3
from typing import Any

from app.db import get_connection

PUBLIC_PROFILE_FIELDS = [
    "public_name",
    "headline",
    "summary",
    "region",
    "contact_method",
    "github_link",
    "linkedin_link",
    "portfolio_links",
]

WORK_EXPERIENCE_FIELDS = [
    "company",
    "title",
    "location",
    "employment_type",
    "start_date",
    "end_date",
    "summary",
    "technologies",
    "visibility",
]

PROJECT_FIELDS = ["name", "description", "url", "technologies", "visibility"]

PUBLIC_VISIBILITIES = ("public_cv", "both")


def get_public_profile() -> sqlite3.Row:
    with get_connection() as conn:
        return conn.execute("SELECT * FROM public_profile WHERE id = 1").fetchone()


def update_public_profile(fields: dict[str, Any]) -> None:
    columns = [f for f in PUBLIC_PROFILE_FIELDS if f in fields]
    assignments = ", ".join(f"{c} = :{c}" for c in columns)
    with get_connection() as conn:
        conn.execute(
            f"UPDATE public_profile SET {assignments}, updated_at = datetime('now') WHERE id = 1",
            fields,
        )
        conn.commit()


def list_work_experiences() -> list[sqlite3.Row]:
    with get_connection() as conn:
        return conn.execute(
            "SELECT * FROM work_experiences ORDER BY start_date DESC, created_at DESC"
        ).fetchall()


def list_public_work_experiences() -> list[sqlite3.Row]:
    placeholders = ", ".join("?" for _ in PUBLIC_VISIBILITIES)
    with get_connection() as conn:
        return conn.execute(
            f"SELECT * FROM work_experiences WHERE visibility IN ({placeholders}) "
            "ORDER BY start_date DESC",
            PUBLIC_VISIBILITIES,
        ).fetchall()


def add_work_experience(fields: dict[str, Any]) -> None:
    columns = [f for f in WORK_EXPERIENCE_FIELDS if f in fields]
    placeholders = ", ".join(f":{c}" for c in columns)
    with get_connection() as conn:
        conn.execute(
            f"INSERT INTO work_experiences ({', '.join(columns)}) VALUES ({placeholders})",
            fields,
        )
        conn.commit()


def delete_work_experience(experience_id: int) -> None:
    with get_connection() as conn:
        conn.execute("DELETE FROM work_experiences WHERE id = ?", (experience_id,))
        conn.commit()


def list_projects() -> list[sqlite3.Row]:
    with get_connection() as conn:
        return conn.execute("SELECT * FROM projects ORDER BY created_at DESC").fetchall()


def list_public_projects() -> list[sqlite3.Row]:
    placeholders = ", ".join("?" for _ in PUBLIC_VISIBILITIES)
    with get_connection() as conn:
        return conn.execute(
            f"SELECT * FROM projects WHERE visibility IN ({placeholders}) ORDER BY created_at DESC",
            PUBLIC_VISIBILITIES,
        ).fetchall()


def add_project(fields: dict[str, Any]) -> None:
    columns = [f for f in PROJECT_FIELDS if f in fields]
    placeholders = ", ".join(f":{c}" for c in columns)
    with get_connection() as conn:
        conn.execute(
            f"INSERT INTO projects ({', '.join(columns)}) VALUES ({placeholders})",
            fields,
        )
        conn.commit()


def delete_project(project_id: int) -> None:
    with get_connection() as conn:
        conn.execute("DELETE FROM projects WHERE id = ?", (project_id,))
        conn.commit()


def list_public_skills() -> list[sqlite3.Row]:
    placeholders = ", ".join("?" for _ in PUBLIC_VISIBILITIES)
    with get_connection() as conn:
        return conn.execute(
            f"SELECT * FROM skills WHERE visibility IN ({placeholders}) ORDER BY category, name",
            PUBLIC_VISIBILITIES,
        ).fetchall()
