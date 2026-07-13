"""Public CV site routes -- Phase 6/7. See docs/public-cv-site.md,
docs/seo-strategy.md, docs/resume-versioning.md, and ADR-010 in
docs/decision-log.md.

As of Phase 7, every page here renders the currently *live* PublicCvPageVersion
snapshot (app/resume_data.py) -- never live profile edits directly. Publishing
a new snapshot from /resume/versions is the only way a change reaches this
site; until something is published, these pages show an "unpublished" empty
state. No auth (see docs/security.md) -- this site is meant to be freely
crawlable.
"""
from __future__ import annotations

import json
from typing import Any

from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import HTMLResponse, PlainTextResponse, Response
from fastapi.templating import Jinja2Templates

from app import resume_data
from app.config import settings
from app.seo import build_seo
from app.site_context import is_public_allowed

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


def _guard(request: Request) -> None:
    if not is_public_allowed(request):
        raise HTTPException(status_code=404)


def _live_snapshot() -> dict[str, Any]:
    version = resume_data.get_live_public_cv_version()
    return json.loads(version["data"]) if version else {}


@router.get("/", response_class=HTMLResponse)
def public_home(request: Request):
    _guard(request)
    snapshot = _live_snapshot()
    name = snapshot.get("public_name") or "Public CV"
    headline = snapshot.get("headline") or ""
    title = f"{name} — {headline}" if headline else name
    seo = build_seo(
        "/", title, snapshot.get("summary") or "Public professional profile.", og_type="profile"
    )
    schema = {
        "@context": "https://schema.org",
        "@type": "ProfilePage",
        "mainEntity": {
            "@type": "Person",
            "name": snapshot.get("public_name") or None,
            "jobTitle": headline or None,
            "url": seo["canonical"],
            "sameAs": [
                link
                for link in (
                    snapshot.get("github_link"),
                    snapshot.get("linkedin_link"),
                    snapshot.get("portfolio_links"),
                )
                if link
            ],
        },
    }
    return templates.TemplateResponse(
        request,
        "public/home.html",
        {
            "page_title": name,
            "seo": seo,
            "schema_json": json.dumps(schema),
            "profile": snapshot,
            "skills": snapshot.get("skills", []),
        },
    )


@router.get("/experience", response_class=HTMLResponse)
def public_experience(request: Request):
    _guard(request)
    snapshot = _live_snapshot()
    name = snapshot.get("public_name") or "Public CV"
    seo = build_seo("/experience", f"Experience — {name}", f"{name}'s work history.")
    return templates.TemplateResponse(
        request,
        "public/experience.html",
        {"page_title": "Experience", "seo": seo, "experiences": snapshot.get("work_experiences", [])},
    )


@router.get("/skills", response_class=HTMLResponse)
def public_skills(request: Request):
    _guard(request)
    snapshot = _live_snapshot()
    name = snapshot.get("public_name") or "Public CV"
    seo = build_seo("/skills", f"Skills — {name}", f"{name}'s skills.")
    return templates.TemplateResponse(
        request,
        "public/skills.html",
        {"page_title": "Skills", "seo": seo, "skills": snapshot.get("skills", [])},
    )


@router.get("/projects", response_class=HTMLResponse)
def public_projects(request: Request):
    _guard(request)
    snapshot = _live_snapshot()
    name = snapshot.get("public_name") or "Public CV"
    seo = build_seo("/projects", f"Projects — {name}", f"Selected projects by {name}.")
    return templates.TemplateResponse(
        request,
        "public/projects.html",
        {"page_title": "Projects", "seo": seo, "projects": snapshot.get("projects", [])},
    )


@router.get("/contact", response_class=HTMLResponse)
def public_contact(request: Request):
    _guard(request)
    snapshot = _live_snapshot()
    name = snapshot.get("public_name") or "Public CV"
    seo = build_seo("/contact", f"Contact — {name}", f"How to contact {name}.")
    return templates.TemplateResponse(
        request,
        "public/contact.html",
        {"page_title": "Contact", "seo": seo, "profile": snapshot},
    )


@router.get("/sitemap.xml")
def sitemap(request: Request):
    _guard(request)
    base = settings.public_cv_external_url.rstrip("/")
    paths = ["/", "/experience", "/skills", "/projects", "/contact"]
    urls = "\n".join(f"  <url><loc>{base}{p}</loc></url>" for p in paths)
    xml = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        f"{urls}\n"
        "</urlset>\n"
    )
    return Response(content=xml, media_type="application/xml")


@router.get("/robots.txt")
def robots(request: Request):
    _guard(request)
    base = settings.public_cv_external_url.rstrip("/")
    body = f"User-agent: *\nAllow: /\nSitemap: {base}/sitemap.xml\n"
    return PlainTextResponse(body)
