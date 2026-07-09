"""Public CV site placeholder routes.

Phase 1 scope only: static placeholder content proving the route group and
templates work. Real structured content lands in Phase 6/7 -- see
docs/public-cv-site.md and docs/phase-plan.md.
"""
from __future__ import annotations

from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.site_context import is_public_allowed

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


def _guard(request: Request) -> None:
    if not is_public_allowed(request):
        raise HTTPException(status_code=404)


@router.get("/", response_class=HTMLResponse)
def public_home(request: Request):
    _guard(request)
    return templates.TemplateResponse(
        request, "public/home.html", {"page_title": "Public CV Home"}
    )


@router.get("/experience", response_class=HTMLResponse)
def public_experience(request: Request):
    _guard(request)
    return templates.TemplateResponse(
        request, "public/experience.html", {"page_title": "Experience"}
    )


@router.get("/skills", response_class=HTMLResponse)
def public_skills(request: Request):
    _guard(request)
    return templates.TemplateResponse(
        request, "public/skills.html", {"page_title": "Skills"}
    )


@router.get("/projects", response_class=HTMLResponse)
def public_projects(request: Request):
    _guard(request)
    return templates.TemplateResponse(
        request, "public/projects.html", {"page_title": "Projects"}
    )


@router.get("/contact", response_class=HTMLResponse)
def public_contact(request: Request):
    _guard(request)
    return templates.TemplateResponse(
        request, "public/contact.html", {"page_title": "Contact"}
    )
