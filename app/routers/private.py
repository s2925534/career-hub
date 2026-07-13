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

from app import application_prep, applications_data, jobs_data, matching, profile_data, storage
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
    preferences = profile_data.get_preferences()
    skills = profile_data.list_skills()
    job_rows = jobs_data.list_jobs()
    jobs_with_matches = [
        {"job": job, "match": matching.score_job(job, preferences, skills)} for job in job_rows
    ]
    return templates.TemplateResponse(
        request,
        "private/jobs.html",
        {
            "page_title": "Jobs",
            "jobs_with_matches": jobs_with_matches,
            "source_choices": jobs_data.SOURCE_CHOICES,
        },
    )


@router.post("/jobs")
def jobs_create(
    request: Request,
    title: str = Form(""),
    company: str = Form(""),
    location: str = Form(""),
    url: str = Form(""),
    description: str = Form(""),
    source: str = Form("manual"),
):
    _guard(request)
    if source not in jobs_data.SOURCE_CHOICES:
        source = "manual"
    job_id = jobs_data.create_job(
        {
            "title": title.strip(),
            "company": company.strip(),
            "location": location.strip(),
            "url": url.strip(),
            "description": description.strip(),
            "source": source,
        }
    )
    return RedirectResponse(url=f"/jobs/{job_id}", status_code=303)


@router.get("/jobs/{job_id}", response_class=HTMLResponse)
def job_detail(request: Request, job_id: int, saved: str | None = None):
    _guard(request)
    job = jobs_data.get_job(job_id)
    if job is None:
        raise HTTPException(status_code=404)
    profile = profile_data.get_candidate_profile()
    documents = profile_data.list_documents()
    match = matching.score_job(job, profile_data.get_preferences(), profile_data.list_skills())
    return templates.TemplateResponse(
        request,
        "private/job_detail.html",
        {
            "page_title": job["title"] or "Job",
            "job": job,
            "match": match,
            "status_choices": jobs_data.STATUS_CHOICES,
            "checklist": application_prep.build_application_checklist(job, profile, documents, match),
            "cover_letter_draft": application_prep.build_cover_letter_draft(job, profile, match),
            "application": applications_data.get_application_by_job(job_id),
            "outcome_choices": applications_data.OUTCOME_CHOICES,
            "saved": saved,
        },
    )


@router.post("/jobs/{job_id}")
def job_update(
    request: Request,
    job_id: int,
    title: str = Form(""),
    company: str = Form(""),
    location: str = Form(""),
    url: str = Form(""),
    description: str = Form(""),
    status: str = Form("interested"),
    notes: str = Form(""),
    follow_up_date: str = Form(""),
):
    _guard(request)
    if jobs_data.get_job(job_id) is None:
        raise HTTPException(status_code=404)
    if status not in jobs_data.STATUS_CHOICES:
        status = "interested"
    jobs_data.update_job(
        job_id,
        {
            "title": title.strip(),
            "company": company.strip(),
            "location": location.strip(),
            "url": url.strip(),
            "description": description.strip(),
            "status": status,
            "notes": notes.strip(),
            "follow_up_date": follow_up_date.strip() or None,
        },
    )
    return RedirectResponse(url=f"/jobs/{job_id}?saved=1", status_code=303)


@router.post("/jobs/{job_id}/apply")
def job_apply(
    request: Request,
    job_id: int,
    application_date: str = Form(""),
    application_url: str = Form(""),
    contact_person: str = Form(""),
    outcome: str = Form("pending"),
    notes: str = Form(""),
    follow_up_date: str = Form(""),
):
    _guard(request)
    if jobs_data.get_job(job_id) is None:
        raise HTTPException(status_code=404)
    if outcome not in applications_data.OUTCOME_CHOICES:
        outcome = "pending"
    applications_data.upsert_application(
        job_id,
        {
            "application_date": application_date.strip() or None,
            "application_url": application_url.strip(),
            "contact_person": contact_person.strip(),
            "outcome": outcome,
            "notes": notes.strip(),
            "follow_up_date": follow_up_date.strip() or None,
        },
    )
    jobs_data.update_job(job_id, {"status": "applied"})
    return RedirectResponse(url=f"/jobs/{job_id}?saved=1#apply", status_code=303)


@router.get("/applications", response_class=HTMLResponse)
def applications(request: Request):
    _guard(request)
    profile = profile_data.get_candidate_profile()
    preferences = profile_data.get_preferences()
    return templates.TemplateResponse(
        request,
        "private/applications.html",
        {
            "page_title": "Applications",
            "ready_to_apply": jobs_data.list_jobs_by_status("ready_to_apply"),
            "applied": applications_data.list_applications_with_jobs(),
            "screening_answers": application_prep.build_screening_answers(profile, preferences),
        },
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
