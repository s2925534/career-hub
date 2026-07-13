"""SEO metadata helpers for the public CV site -- Phase 6. See
docs/seo-strategy.md.

Optional per-page overrides live in the `seo_metadata` table (page_path,
title, description); everything else falls back to a default computed from
the public profile at request time. No private admin UI to edit seo_metadata
yet -- that's a natural Phase 7 follow-up once resume/CV versioning exists.
"""
from __future__ import annotations

import sqlite3
from typing import Any

from app.config import settings
from app.db import get_connection


def get_seo_override(page_path: str) -> sqlite3.Row | None:
    with get_connection() as conn:
        return conn.execute(
            "SELECT * FROM seo_metadata WHERE page_path = ?", (page_path,)
        ).fetchone()


def build_seo(
    page_path: str, default_title: str, default_description: str, og_type: str = "website"
) -> dict[str, Any]:
    override = get_seo_override(page_path)
    title = (override["title"] if override else None) or default_title
    description = (override["description"] if override else None) or default_description
    base = settings.public_cv_external_url.rstrip("/")
    canonical = base if page_path == "/" else base + page_path
    return {"title": title, "description": description, "canonical": canonical, "og_type": og_type}
