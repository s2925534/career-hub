"""File storage helpers for uploaded documents (CVs, cover letter templates,
other profile assets). See docs/deployer-integration.md for the persistent
folder layout under CAREER_HUB_BASE_PATH.
"""
from __future__ import annotations

import re
import uuid
from pathlib import Path

from app.config import settings

KIND_TO_SUBFOLDER = {
    "cv": "uploads/cv",
    "cover_letter": "uploads/cover-letters",
    "other": "uploads/profile-assets",
}

_SAFE_CHARS = re.compile(r"[^A-Za-z0-9._-]+")


def _safe_filename(original_filename: str) -> str:
    name = Path(original_filename).name  # strip any directory components
    name = _SAFE_CHARS.sub("_", name) or "upload"
    return f"{uuid.uuid4().hex[:12]}_{name}"


def save_uploaded_document(kind: str, original_filename: str, content: bytes) -> str:
    """Writes the file under CAREER_HUB_BASE_PATH/uploads/<kind folder>/ and
    returns the path stored in the documents table (relative to base_path)."""
    subfolder = KIND_TO_SUBFOLDER.get(kind, KIND_TO_SUBFOLDER["other"])
    target_dir = settings.base_path / subfolder
    target_dir.mkdir(parents=True, exist_ok=True)

    filename = _safe_filename(original_filename)
    target_path = target_dir / filename
    target_path.write_bytes(content)

    return f"{subfolder}/{filename}"
