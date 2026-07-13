"""Public CV site routes -- Phase 6. See docs/public-cv-site.md,
docs/seo-strategy.md, and docs/profile-and-preferences.md ("Public Profile
Fields").

Renders only public_profile plus WorkExperience/Project/Skill rows whose
visibility includes public_cv -- see app/public_profile_data.py
PUBLIC_VISIBILITIES. Never renders anything from the private candidate
profile, jobs, applications, or matching data. No auth (see docs/security.md)
-- this site is meant to be freely crawlable.
"""
from __future__ import annotations

import json

from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import HTMLResponse, PlainTextResponse, Response
from fastapi.templating import Jinja2Templates

from app import public_profile_data
from app.config import settings
from app.seo import build_seo
from app.site_context import is_public_allowed

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


def _guard(request: Request) -> None:
    if not is_public_allowed(request):
        raise HTTPException(status_code=404)


def _display_name(profile) -> str:
    return profile["public_name"] or "Public CV"


@router.get("/", response_class=HTMLResponse)
def public_home(request: Request):
    _guard(request)
    profile = public_profile_data.get_public_profile()
    name = _display_name(profile)
    title = f"{name} — {profile['headline']}" if profile["headline"] else name
    seo = build_seo(
        "/", title, profile["summary"] or "Public professional profile.", og_type="profile"
    )
    schema = {
        "@context": "https://schema.org",
        "@type": "ProfilePage",
        "mainEntity": {
            "@type": "Person",
            "name": profile["public_name"] or None,
            "jobTitle": profile["headline"] or None,
            "url": seo["canonical"],
            "sameAs": [
                link
                for link in (profile["github_link"], profile["linkedin_link"], profile["portfolio_links"])
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
            "profile": profile,
            "skills": public_profile_data.list_public_skills(),
        },
    )


@router.get("/experience", response_class=HTMLResponse)
def public_experience(request: Request):
    _guard(request)
    name = _display_name(public_profile_data.get_public_profile())
    seo = build_seo("/experience", f"Experience — {name}", f"{name}'s work history.")
    return templates.TemplateResponse(
        request,
        "public/experience.html",
        {
            "page_title": "Experience",
            "seo": seo,
            "experiences": public_profile_data.list_public_work_experiences(),
        },
    )


@router.get("/skills", response_class=HTMLResponse)
def public_skills(request: Request):
    _guard(request)
    name = _display_name(public_profile_data.get_public_profile())
    seo = build_seo("/skills", f"Skills — {name}", f"{name}'s skills.")
    return templates.TemplateResponse(
        request,
        "public/skills.html",
        {"page_title": "Skills", "seo": seo, "skills": public_profile_data.list_public_skills()},
    )


@router.get("/projects", response_class=HTMLResponse)
def public_projects(request: Request):
    _guard(request)
    name = _display_name(public_profile_data.get_public_profile())
    seo = build_seo("/projects", f"Projects — {name}", f"Selected projects by {name}.")
    return templates.TemplateResponse(
        request,
        "public/projects.html",
        {"page_title": "Projects", "seo": seo, "projects": public_profile_data.list_public_projects()},
    )


@router.get("/contact", response_class=HTMLResponse)
def public_contact(request: Request):
    _guard(request)
    profile = public_profile_data.get_public_profile()
    name = _display_name(profile)
    seo = build_seo("/contact", f"Contact — {name}", f"How to contact {name}.")
    return templates.TemplateResponse(
        request,
        "public/contact.html",
        {"page_title": "Contact", "seo": seo, "profile": profile},
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
