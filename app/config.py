"""Application configuration, loaded from environment variables.

See .env.example for the full list of variables and docs/deployer-integration.md
for how CAREER_HUB_BASE_PATH and the hostnames are expected to be supplied.
"""
from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()


def _bool_env(name: str, default: bool) -> bool:
    value = os.getenv(name)
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


@dataclass(frozen=True)
class Settings:
    private_domain: str = field(default_factory=lambda: os.getenv("CAREER_HUB_PRIVATE_DOMAIN", "jobs.example.com"))
    public_cv_domain: str = field(default_factory=lambda: os.getenv("CAREER_HUB_PUBLIC_CV_DOMAIN", "cv.example.com"))
    private_external_url: str = field(default_factory=lambda: os.getenv("CAREER_HUB_PRIVATE_EXTERNAL_URL", "https://jobs.example.com"))
    public_cv_external_url: str = field(default_factory=lambda: os.getenv("CAREER_HUB_PUBLIC_CV_EXTERNAL_URL", "https://cv.example.com"))

    base_path: Path = field(default_factory=lambda: Path(os.getenv("CAREER_HUB_BASE_PATH", "./data/career-hub")))

    http_port: int = field(default_factory=lambda: int(os.getenv("CAREER_HUB_HTTP_PORT", "8088")))
    bind_host: str = field(default_factory=lambda: os.getenv("CAREER_HUB_BIND_HOST", "0.0.0.0"))

    app_secret_key: str = field(default_factory=lambda: os.getenv("APP_SECRET_KEY", "change-me-generate-a-long-random-secret"))
    database_url: str = field(default_factory=lambda: os.getenv("DATABASE_URL", ""))

    deploy_mode: str = field(default_factory=lambda: os.getenv("DEPLOY_MODE", "local_only"))
    public_exposure: bool = field(default_factory=lambda: _bool_env("PUBLIC_EXPOSURE", False))

    enable_local_auth: bool = field(default_factory=lambda: _bool_env("ENABLE_LOCAL_AUTH", True))
    enable_sso_auth: bool = field(default_factory=lambda: _bool_env("ENABLE_SSO_AUTH", False))

    enable_public_cv_site: bool = field(default_factory=lambda: _bool_env("ENABLE_PUBLIC_CV_SITE", True))
    enable_public_cv_seo: bool = field(default_factory=lambda: _bool_env("ENABLE_PUBLIC_CV_SEO", True))

    enable_ai_assist: bool = field(default_factory=lambda: _bool_env("ENABLE_AI_ASSIST", False))
    enable_auto_apply: bool = field(default_factory=lambda: _bool_env("ENABLE_AUTO_APPLY", False))

    @property
    def database_path(self) -> Path:
        """Resolve the SQLite file path from DATABASE_URL (sqlite:///relative or
        sqlite:////absolute), falling back to a default under base_path."""
        prefix = "sqlite:///"
        if self.database_url.startswith(prefix):
            raw_path = self.database_url[len(prefix):]
            if raw_path:
                return Path(raw_path)
        return self.base_path / "database" / "career-hub.sqlite3"


settings = Settings()
