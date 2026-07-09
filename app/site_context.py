"""Determines whether a request should be treated as hitting the private
career-admin site or the public CV site, based on the Host header.

See docs/reverse-proxy-domain.md and docs/architecture.md section 1: both
hostnames can point at the same container in the MVP, distinguished by Host.

For local development, the configured domains (CAREER_HUB_PRIVATE_DOMAIN /
CAREER_HUB_PUBLIC_CV_DOMAIN) usually won't match the Host you're actually
using (e.g. "localhost:8088"). In that case both route groups are served so
you can exercise the whole app without configuring two local hostnames --
this permissive fallback never applies once the request Host matches one of
the configured production domains, at which point only that domain's route
group is served.
"""
from __future__ import annotations

from enum import Enum

from fastapi import Request

from app.config import settings


class Site(str, Enum):
    PRIVATE = "private"
    PUBLIC = "public"
    UNKNOWN = "unknown"  # neither configured domain matched (e.g. local dev)


def _host_without_port(request: Request) -> str:
    host = request.headers.get("host", "")
    return host.split(":", 1)[0]


def resolve_site(request: Request) -> Site:
    host = _host_without_port(request)
    if host == settings.private_domain:
        return Site.PRIVATE
    if host == settings.public_cv_domain:
        return Site.PUBLIC
    return Site.UNKNOWN


def is_private_allowed(request: Request) -> bool:
    site = resolve_site(request)
    return site in (Site.PRIVATE, Site.UNKNOWN)


def is_public_allowed(request: Request) -> bool:
    site = resolve_site(request)
    return site in (Site.PUBLIC, Site.UNKNOWN)
