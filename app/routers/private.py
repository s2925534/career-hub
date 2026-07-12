"""Private career-admin routes.

No authentication wired up yet (see docs/sso-integration-future.md and
docs/security.md) -- do not deploy this publicly before authentication exists.

Phase 2 fleshes out /profile and /preferences (candidate profile, job search
status, skills, CV/template uploads, and job preferences -- see
docs/profile-and-preferences.md). Jobs, applications, resume versions, and
public CV admin remain Phase 1 placeholders pending their own phases.
"""
from __future__ import annotations

from fastapi import APIRouter, Form, HTTPException, Request, UploadFile
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from app import profile_data, storage
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
def profile(request: Request, saved: str | None = None):
    _guard(request)
    return templates.TemplateResponse(
        request,
        "private/profile.html",
        {
            "page_title": "Profile",
            "profile": profile_data.get_candidate_profile(),
            "skills": profile_data.list_skills(),
            "documents": profile_data.list_documents(),
            "visibility_choices": profile_data.VISIBILITY_CHOICES,
            "saved": saved,
        },
    )


@router.post("/profile")
def profile_save(
    request: Request,
    name: str = Form(""),
    location: str = Form(""),
    work_rights: str = Form(""),
    currently_looking: str = Form("not_looking"),
    availability_start_date: str = Form(""),
    visa_details: str = Form(""),
    references_available: str = Form("unspecified"),
    portfolio_links: str = Form(""),
    github_link: str = Form(""),
    linkedin_link: str = Form(""),
    personal_site_link: str = Form(""),
):
    _guard(request)
    profile_data.update_candidate_profile(
        {
            "name": name.strip(),
            "location": location.strip(),
            "work_rights": work_rights.strip(),
            "currently_looking": currently_looking,
            "availability_start_date": availability_start_date.strip(),
            "visa_details": visa_details.strip(),
            "references_available": references_available,
            "portfolio_links": portfolio_links.strip(),
            "github_link": github_link.strip(),
            "linkedin_link": linkedin_link.strip(),
            "personal_site_link": personal_site_link.strip(),
        }
    )
    return RedirectResponse(url="/profile?saved=1", status_code=303)


@router.post("/profile/skills")
def skills_add(
    request: Request,
    name: str = Form(...),
    category: str = Form(""),
    visibility: str = Form("private"),
):
    _guard(request)
    name = name.strip()
    if name:
        if visibility not in profile_data.VISIBILITY_CHOICES:
            visibility = "private"
        profile_data.add_skill(name, category.strip(), visibility)
    return RedirectResponse(url="/profile?saved=1#skills", status_code=303)


@router.post("/profile/skills/{skill_id}/delete")
def skills_delete(request: Request, skill_id: int):
    _guard(request)
    profile_data.delete_skill(skill_id)
    return RedirectResponse(url="/profile#skills", status_code=303)


# Uploads are capped well above any real resume/cover-letter size to avoid an
# oversized file silently exhausting disk under CAREER_HUB_BASE_PATH.
MAX_UPLOAD_BYTES = 20 * 1024 * 1024


@router.post("/profile/documents")
async def documents_upload(
    request: Request,
    kind: str = Form("other"),
    visibility: str = Form("private"),
    file: UploadFile | None = None,
):
    _guard(request)
    if file is not None and file.filename:
        content = await file.read(MAX_UPLOAD_BYTES + 1)
        if len(content) > MAX_UPLOAD_BYTES:
            raise HTTPException(status_code=413, detail="File too large")
        if kind not in storage.KIND_TO_SUBFOLDER:
            kind = "other"
        if visibility not in profile_data.VISIBILITY_CHOICES:
            visibility = "private"
        stored_path = storage.save_uploaded_document(kind, file.filename, content)
        profile_data.add_document(kind, file.filename, stored_path, visibility)
    return RedirectResponse(url="/profile?saved=1#documents", status_code=303)


@router.post("/profile/documents/{document_id}/delete")
def documents_delete(request: Request, document_id: int):
    _guard(request)
    profile_data.delete_document(document_id)
    return RedirectResponse(url="/profile#documents", status_code=303)


@router.get("/preferences", response_class=HTMLResponse)
def preferences(request: Request, saved: str | None = None):
    _guard(request)
    return templates.TemplateResponse(
        request,
        "private/preferences.html",
        {
            "page_title": "Preferences",
            "preferences": profile_data.get_preferences(),
            "saved": saved,
        },
    )


@router.post("/preferences")
def preferences_save(
    request: Request,
    target_role_titles: str = Form(""),
    target_seniority: str = Form(""),
    target_salary_min: str = Form(""),
    target_salary_max: str = Form(""),
    minimum_salary: str = Form(""),
    preferred_locations: str = Form(""),
    work_mode: str = Form("any"),
    industries: str = Form(""),
    preferred_companies: str = Form(""),
    excluded_companies: str = Form(""),
    required_technologies: str = Form(""),
    preferred_technologies: str = Form(""),
    excluded_technologies: str = Form(""),
    max_commute_minutes: str = Form(""),
):
    _guard(request)

    def _int_or_none(value: str) -> int | None:
        value = value.strip()
        return int(value) if value.isdigit() else None

    profile_data.update_preferences(
        {
            "target_role_titles": target_role_titles.strip(),
            "target_seniority": target_seniority.strip(),
            "target_salary_min": _int_or_none(target_salary_min),
            "target_salary_max": _int_or_none(target_salary_max),
            "minimum_salary": _int_or_none(minimum_salary),
            "preferred_locations": preferred_locations.strip(),
            "work_mode": work_mode,
            "industries": industries.strip(),
            "preferred_companies": preferred_companies.strip(),
            "excluded_companies": excluded_companies.strip(),
            "required_technologies": required_technologies.strip(),
            "preferred_technologies": preferred_technologies.strip(),
            "excluded_technologies": excluded_technologies.strip(),
            "max_commute_minutes": _int_or_none(max_commute_minutes),
        }
    )
    return RedirectResponse(url="/preferences?saved=1", status_code=303)


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
