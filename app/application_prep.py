"""Application preparation helpers -- Phase 5. See docs/application-workflow.md
and the example templates in examples/application-templates/.

Cover letter drafts, screening answers, and the application checklist are all
built live from stored, truthful profile/preferences/job data -- never
fabricated. Where a fact isn't stored (e.g. work history, which Career Hub
doesn't model yet), the draft says so explicitly rather than inventing
content, per docs/profile-and-preferences.md ("Profile Truthfulness Rules").
"""
from __future__ import annotations

from typing import Any

_CONTACT_FIELDS = ["personal_site_link", "linkedin_link", "github_link", "portfolio_links"]


def _contact_line(profile: Any) -> str:
    for field in _CONTACT_FIELDS:
        value = (profile[field] or "").strip()
        if value:
            return value
    return "[Add a contact link in your profile]"


def build_cover_letter_draft(job: Any, profile: Any, match: dict) -> str:
    name = (profile["name"] or "").strip() or "[Add your name in /profile]"
    job_title = job["title"] or "this role"
    company = job["company"] or "your company"
    highlight = match["match_reasons"][0].rstrip(".") if match["match_reasons"] else None

    lines = [
        "Dear Hiring Team,",
        "",
        f"I'm writing to apply for the {job_title} role at {company}.",
    ]
    if highlight:
        lines.append(f"{highlight}, which I believe aligns well with what you're looking for in this role.")
    else:
        lines.append("[Add a professional summary or skills in your profile to personalize this paragraph.]")
    lines += [
        "",
        "[Add a paragraph about your most relevant recent experience -- work history "
        "isn't tracked in Career Hub yet.]",
        "",
        "I'd welcome the opportunity to discuss how I could contribute to your team.",
        "",
        "Sincerely,",
        name,
        _contact_line(profile),
    ]
    return "\n".join(lines)


def build_application_checklist(job: Any, profile: Any, documents: list[Any], match: dict) -> list[dict]:
    has_cv = any(d["kind"] == "cv" for d in documents)
    has_cover_letter = any(d["kind"] == "cover_letter" for d in documents)
    profile_complete = bool((profile["name"] or "").strip() and (profile["work_rights"] or "").strip())
    return [
        {"label": "Candidate profile has name and work rights set", "done": profile_complete},
        {"label": "CV document uploaded", "done": has_cv},
        {"label": "Cover letter template uploaded (or draft below reviewed)", "done": has_cover_letter},
        {"label": "Job reviewed against preferences (match score computed)", "done": match["band"] != "unscored"},
        {"label": "Screening answers reviewed for gaps", "done": profile_complete},
    ]


def build_screening_answers(profile: Any, preferences: Any) -> list[dict]:
    salary_answer = None
    salary_min = preferences["target_salary_min"]
    salary_max = preferences["target_salary_max"]
    minimum_salary = preferences["minimum_salary"]
    if salary_min and salary_max:
        salary_answer = f"{salary_min:,}-{salary_max:,} (negotiable within this range)"
    elif salary_min:
        salary_answer = f"From {salary_min:,} (negotiable)"
    elif salary_max:
        salary_answer = f"Up to {salary_max:,} (negotiable)"
    elif minimum_salary:
        salary_answer = f"{minimum_salary:,}+ (negotiable)"

    return [
        {
            "question": "Are you legally authorized to work in this country?",
            "source": "candidate_profile.work_rights",
            "answer": (profile["work_rights"] or "").strip() or None,
        },
        {
            "question": "What is your expected salary?",
            "source": "preferences.target_salary_min / target_salary_max / minimum_salary",
            "answer": salary_answer,
        },
        {
            "question": "When can you start?",
            "source": "candidate_profile.availability_start_date",
            "answer": (profile["availability_start_date"] or "").strip() or None,
        },
        {
            "question": "Do you require visa sponsorship?",
            "source": "candidate_profile.visa_details",
            "answer": (profile["visa_details"] or "").strip() or None,
        },
    ]
