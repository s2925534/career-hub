"""Private career-admin placeholder routes.

Phase 1 scope only: static placeholder content proving the route group and
templates work, with no authentication wired up yet (local auth lands in a
later Phase 1 follow-up / Phase 2 -- see docs/sso-integration-future.md and
docs/security.md). Do not deploy this publicly before authentication exists.
"""
from __future__ import annotations

from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.site_context import is_private_allowed

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


def _guard(request: Request) -> None:
    if not is_private_allowed(request):
        raise HTTPException(status_code=404)


@router.get("/dashboard", response_class=HTMLResponse)
def dashboard(request: Request):
    _guard(request)
    return templates.TemplateResponse(
        request, "private/dashboard.html", {"page_title": "Dashboard"}
    )


@router.get("/profile", response_class=HTMLResponse)
def profile(request: Request):
    _guard(request)
    return templates.TemplateResponse(
        request, "private/profile.html", {"page_title": "Profile"}
    )


@router.get("/preferences", response_class=HTMLResponse)
def preferences(request: Request):
    _guard(request)
    return templates.TemplateResponse(
        request, "private/preferences.html", {"page_title": "Preferences"}
    )


@router.get("/jobs", response_class=HTMLResponse)
def jobs(request: Request):
    _guard(request)
    return templates.TemplateResponse(
        request, "private/jobs.html", {"page_title": "Jobs"}
    )


@router.get("/applications", response_class=HTMLResponse)
def applications(request: Request):
    _guard(request)
    return templates.TemplateResponse(
        request, "private/applications.html", {"page_title": "Applications"}
    )


@router.get("/resume/versions", response_class=HTMLResponse)
def resume_versions(request: Request):
    _guard(request)
    return templates.TemplateResponse(
        request, "private/resume_versions.html", {"page_title": "Resume Versions"}
    )


@router.get("/public-cv/admin", response_class=HTMLResponse)
def public_cv_admin(request: Request):
    _guard(request)
    return templates.TemplateResponse(
        request, "private/public_cv_admin.html", {"page_title": "Public CV Admin"}
    )
