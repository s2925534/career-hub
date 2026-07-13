"""Data access for resume/CV versioning -- Phase 7. See
docs/resume-versioning.md and ADR-010 in docs/decision-log.md.

Two version tables:
- resume_versions (ResumeVersion): a snapshot of structured profile data,
  one of which can be flagged the job-application default.
- public_cv_versions (PublicCvPageVersion): a snapshot of exactly what the
  public CV site renders. The public site (app/routers/public.py) only ever
  reads the currently live row here -- never live profile edits directly --
  per ADR-010. Publishing and rollback are both just "flag this row live".

Plain SQL, no ORM -- consistent with the rest of the app.
"""
from __future__ import annotations

import json
import sqlite3
from typing import Any

from app import profile_data, public_profile_data
from app.db import get_connection


def build_resume_snapshot() -> dict[str, Any]:
    """Everything a resume/application-default version should capture --
    candidate identity plus all structured profile content, regardless of
    visibility (this snapshot is for private use, e.g. application prep)."""
    candidate = profile_data.get_candidate_profile()
    public = public_profile_data.get_public_profile()
    return {
        "name": candidate["name"],
        "location": candidate["location"],
        "work_rights": candidate["work_rights"],
        "headline": public["headline"],
        "summary": public["summary"],
        "skills": [dict(s) for s in profile_data.list_skills()],
        "work_experiences": [dict(e) for e in public_profile_data.list_work_experiences()],
        "projects": [dict(p) for p in public_profile_data.list_projects()],
    }


def build_public_cv_snapshot() -> dict[str, Any]:
    """Only public-visible fields -- exactly what the public CV site may
    render. See app/public_profile_data.py PUBLIC_VISIBILITIES."""
    public = public_profile_data.get_public_profile()
    return {
        "public_name": public["public_name"],
        "headline": public["headline"],
        "summary": public["summary"],
        "region": public["region"],
        "contact_method": public["contact_method"],
        "github_link": public["github_link"],
        "linkedin_link": public["linkedin_link"],
        "portfolio_links": public["portfolio_links"],
        "skills": [dict(s) for s in public_profile_data.list_public_skills()],
        "work_experiences": [dict(e) for e in public_profile_data.list_public_work_experiences()],
        "projects": [dict(p) for p in public_profile_data.list_public_projects()],
    }


def list_resume_versions() -> list[sqlite3.Row]:
    with get_connection() as conn:
        return conn.execute("SELECT * FROM resume_versions ORDER BY created_at DESC").fetchall()


def get_resume_version(version_id: int) -> sqlite3.Row | None:
    with get_connection() as conn:
        return conn.execute("SELECT * FROM resume_versions WHERE id = ?", (version_id,)).fetchone()


def create_resume_version(label: str, source: str = "manual") -> int:
    with get_connection() as conn:
        cursor = conn.execute(
            "INSERT INTO resume_versions (label, source, data) VALUES (?, ?, ?)",
            (label, source, json.dumps(build_resume_snapshot())),
        )
        conn.commit()
        return cursor.lastrowid


def set_application_default(version_id: int) -> None:
    with get_connection() as conn:
        conn.execute("UPDATE resume_versions SET is_application_default = 0")
        conn.execute(
            "UPDATE resume_versions SET is_application_default = 1, updated_at = datetime('now') "
            "WHERE id = ?",
            (version_id,),
        )
        conn.commit()


def archive_resume_version(version_id: int) -> None:
    with get_connection() as conn:
        conn.execute(
            "UPDATE resume_versions SET archived = 1, updated_at = datetime('now') WHERE id = ?",
            (version_id,),
        )
        conn.commit()


def list_public_cv_versions() -> list[sqlite3.Row]:
    with get_connection() as conn:
        return conn.execute("SELECT * FROM public_cv_versions ORDER BY created_at DESC").fetchall()


def get_public_cv_version(version_id: int) -> sqlite3.Row | None:
    with get_connection() as conn:
        return conn.execute(
            "SELECT * FROM public_cv_versions WHERE id = ?", (version_id,)
        ).fetchone()


def get_live_public_cv_version() -> sqlite3.Row | None:
    with get_connection() as conn:
        return conn.execute("SELECT * FROM public_cv_versions WHERE is_live = 1").fetchone()


def create_public_cv_version(label: str, source: str = "manual") -> int:
    with get_connection() as conn:
        cursor = conn.execute(
            "INSERT INTO public_cv_versions (label, source, data) VALUES (?, ?, ?)",
            (label, source, json.dumps(build_public_cv_snapshot())),
        )
        conn.commit()
        return cursor.lastrowid


def publish_public_cv_version(version_id: int) -> None:
    """Marks this version live -- the only way a change reaches the public
    site (ADR-010). Publishing an older version again is how rollback works."""
    with get_connection() as conn:
        conn.execute("UPDATE public_cv_versions SET is_live = 0")
        conn.execute(
            "UPDATE public_cv_versions SET is_live = 1, published_at = datetime('now'), "
            "updated_at = datetime('now') WHERE id = ?",
            (version_id,),
        )
        conn.commit()
