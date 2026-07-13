"""Rule-based job matching engine -- Phase 4. See docs/phase-plan.md ("Phase 4")
and the "Job matching criteria" list in docs/profile-and-preferences.md.

Deliberately not AI-assisted (see docs/ai-integration-future.md): scores are
computed live from stored preferences/skills against the job's own fields
(title, company, location, pasted description), with a human-readable reason
for every point awarded or withheld. Nothing is persisted -- preferences and
skills change often enough, and jobs are few enough, that a live scan is
cheap and avoids stale cached scores.
"""
from __future__ import annotations

import re
from typing import Any

BAND_UNSCORED = "unscored"
BAND_EXCLUDED = "excluded"
BAND_POOR = "poor"
BAND_POSSIBLE = "possible"
BAND_STRONG = "strong"

_SALARY_RE = re.compile(r"\$?\s?(\d{2,3})\s?[kK]\b|\$\s?(\d{2,3},\d{3})\b")


def _terms(csv: str | None) -> list[str]:
    if not csv:
        return []
    return [t.strip().lower() for t in csv.split(",") if t.strip()]


def _contains_any(haystack: str, needles: list[str]) -> list[str]:
    haystack = haystack.lower()
    return [n for n in needles if n in haystack]


def _extract_salary(text: str) -> int | None:
    """Best-effort: find the first "$120,000" / "120k" style figure in free text."""
    match = _SALARY_RE.search(text or "")
    if not match:
        return None
    if match.group(1) is not None:
        return int(match.group(1)) * 1000
    return int(match.group(2).replace(",", ""))


def score_job(job: Any, preferences: Any, skills: list[Any]) -> dict:
    title = job["title"] or ""
    company = job["company"] or ""
    location = job["location"] or ""
    description = job["description"] or ""
    haystack = f"{title} {location} {description}".lower()

    target_titles = _terms(preferences["target_role_titles"])
    skill_names = [s["name"].lower() for s in skills if s["name"]]
    preferred_locations = _terms(preferences["preferred_locations"])
    work_mode = (preferences["work_mode"] or "any").lower()
    required_tech = _terms(preferences["required_technologies"])
    preferred_companies = _terms(preferences["preferred_companies"])
    excluded_companies = _terms(preferences["excluded_companies"])
    excluded_tech = _terms(preferences["excluded_technologies"])
    minimum_salary = preferences["minimum_salary"]

    has_criteria = bool(
        target_titles
        or skill_names
        or preferred_locations
        or work_mode != "any"
        or required_tech
        or preferred_companies
        or excluded_companies
        or excluded_tech
        or minimum_salary
    )
    if not has_criteria:
        return {
            "score": None,
            "band": BAND_UNSCORED,
            "match_reasons": [],
            "rejection_reasons": [
                "No preferences or skills set yet -- add some on /preferences "
                "and /profile#skills to enable matching."
            ],
        }

    company_lower = company.lower()
    if company_lower and any(c in company_lower for c in excluded_companies):
        return {
            "score": 0,
            "band": BAND_EXCLUDED,
            "match_reasons": [],
            "rejection_reasons": [f'Company "{company}" is on your excluded companies list.'],
        }

    hit_excluded_tech = _contains_any(haystack, excluded_tech)
    if hit_excluded_tech:
        return {
            "score": 0,
            "band": BAND_EXCLUDED,
            "match_reasons": [],
            "rejection_reasons": ["Mentions excluded technology: " + ", ".join(hit_excluded_tech) + "."],
        }

    score = 0
    match_reasons: list[str] = []
    rejection_reasons: list[str] = []

    hit_titles = _contains_any(title, target_titles)
    if target_titles:
        if hit_titles:
            score += 20
            match_reasons.append("Title matches target role: " + ", ".join(hit_titles) + ".")
        else:
            rejection_reasons.append("Title doesn't match any target role.")

    hit_skills = _contains_any(haystack, skill_names)
    if skill_names:
        if hit_skills:
            score += min(30, len(hit_skills) * 6)
            match_reasons.append("Mentions your skills: " + ", ".join(hit_skills) + ".")
        else:
            rejection_reasons.append("Doesn't mention any of your listed skills.")

    hit_locations = _contains_any(location, preferred_locations)
    if preferred_locations:
        if hit_locations:
            score += 15
            match_reasons.append("Location matches a preferred location: " + ", ".join(hit_locations) + ".")
        else:
            rejection_reasons.append("Location doesn't match any preferred location.")

    if work_mode != "any":
        if work_mode in haystack:
            score += 10
            match_reasons.append(f"Mentions {work_mode} work.")
        else:
            rejection_reasons.append(f"Doesn't mention {work_mode} work.")

    hit_required = _contains_any(haystack, required_tech)
    if required_tech:
        if len(hit_required) == len(required_tech):
            score += 15
            match_reasons.append("Mentions all required technologies: " + ", ".join(hit_required) + ".")
        elif hit_required:
            score += 7
            missing = [t for t in required_tech if t not in hit_required]
            match_reasons.append("Mentions some required technologies: " + ", ".join(hit_required) + ".")
            rejection_reasons.append("Missing required technology: " + ", ".join(missing) + ".")
        else:
            rejection_reasons.append(
                "Doesn't mention any required technology: " + ", ".join(required_tech) + "."
            )

    if preferred_companies and company_lower and any(c in company_lower for c in preferred_companies):
        score += 10
        match_reasons.append(f'"{company}" is on your preferred companies list.')

    parsed_salary = _extract_salary(description)
    if minimum_salary and parsed_salary is not None:
        if parsed_salary >= minimum_salary:
            score += 10
            match_reasons.append(
                f"Stated salary (~{parsed_salary:,}) meets your minimum ({minimum_salary:,})."
            )
        else:
            rejection_reasons.append(
                f"Stated salary (~{parsed_salary:,}) is below your minimum ({minimum_salary:,})."
            )

    score = max(0, min(100, score))
    if score >= 70:
        band = BAND_STRONG
    elif score >= 40:
        band = BAND_POSSIBLE
    else:
        band = BAND_POOR

    return {
        "score": score,
        "band": band,
        "match_reasons": match_reasons,
        "rejection_reasons": rejection_reasons,
    }
