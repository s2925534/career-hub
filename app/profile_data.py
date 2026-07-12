"""Data access for the candidate profile, preferences, skills, and uploaded
documents -- the Phase 2 private data model. See docs/profile-and-preferences.md.

Plain SQL, no ORM -- consistent with the rest of the Phase 1 foundation (see
app/db.py). candidate_profile and preferences are singletons (id=1).
"""
from __future__ import annotations

import sqlite3
from typing import Any

from app.db import get_connection

CANDIDATE_PROFILE_FIELDS = [
    "name",
    "location",
    "work_rights",
    "currently_looking",
    "availability_start_date",
    "visa_details",
    "references_available",
    "portfolio_links",
    "github_link",
    "linkedin_link",
    "personal_site_link",
]

PREFERENCES_FIELDS = [
    "target_role_titles",
    "target_seniority",
    "target_salary_min",
    "target_salary_max",
    "minimum_salary",
    "preferred_locations",
    "work_mode",
    "industries",
    "preferred_companies",
    "excluded_companies",
    "required_technologies",
    "preferred_technologies",
    "excluded_technologies",
    "max_commute_minutes",
]

VISIBILITY_CHOICES = ["private", "public_cv", "applications_only", "both", "archived"]


def get_candidate_profile() -> sqlite3.Row:
    with get_connection() as conn:
        return conn.execute("SELECT * FROM candidate_profile WHERE id = 1").fetchone()


def update_candidate_profile(fields: dict[str, Any]) -> None:
    columns = [f for f in CANDIDATE_PROFILE_FIELDS if f in fields]
    assignments = ", ".join(f"{c} = :{c}" for c in columns)
    with get_connection() as conn:
        conn.execute(
            f"UPDATE candidate_profile SET {assignments}, updated_at = datetime('now') WHERE id = 1",
            fields,
        )
        conn.commit()


def get_preferences() -> sqlite3.Row:
    with get_connection() as conn:
        return conn.execute("SELECT * FROM preferences WHERE id = 1").fetchone()


def update_preferences(fields: dict[str, Any]) -> None:
    columns = [f for f in PREFERENCES_FIELDS if f in fields]
    assignments = ", ".join(f"{c} = :{c}" for c in columns)
    with get_connection() as conn:
        conn.execute(
            f"UPDATE preferences SET {assignments}, updated_at = datetime('now') WHERE id = 1",
            fields,
        )
        conn.commit()


def list_skills() -> list[sqlite3.Row]:
    with get_connection() as conn:
        return conn.execute("SELECT * FROM skills ORDER BY category, name").fetchall()


def add_skill(name: str, category: str, visibility: str) -> None:
    with get_connection() as conn:
        conn.execute(
            "INSERT INTO skills (name, category, visibility) VALUES (?, ?, ?)",
            (name, category, visibility),
        )
        conn.commit()


def delete_skill(skill_id: int) -> None:
    with get_connection() as conn:
        conn.execute("DELETE FROM skills WHERE id = ?", (skill_id,))
        conn.commit()


def list_documents() -> list[sqlite3.Row]:
    with get_connection() as conn:
        return conn.execute("SELECT * FROM documents ORDER BY created_at DESC").fetchall()


def add_document(kind: str, original_filename: str, file_path: str, visibility: str) -> None:
    with get_connection() as conn:
        conn.execute(
            "INSERT INTO documents (kind, original_filename, file_path, visibility) VALUES (?, ?, ?, ?)",
            (kind, original_filename, file_path, visibility),
        )
        conn.commit()


def delete_document(document_id: int) -> sqlite3.Row | None:
    with get_connection() as conn:
        row = conn.execute("SELECT * FROM documents WHERE id = ?", (document_id,)).fetchone()
        conn.execute("DELETE FROM documents WHERE id = ?", (document_id,))
        conn.commit()
        return row
