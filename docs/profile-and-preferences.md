# Profile and Preferences

Career Hub separates a private **candidate profile** (everything relevant to your job search)
from a public **public profile** (only what you've approved for the CV site). This document is
the planning reference for both, plus job preferences and visibility rules. See
[`docs/security.md`](security.md) for how these are protected and
[`docs/public-cv-site.md`](public-cv-site.md) for how the public subset is published.

## Candidate Profile Fields (Private)

1. Name
2. Location
3. Work rights
4. Current job-search status (looking / not looking / passively open)
5. Target role titles
6. Target seniority
7. Target salary range
8. Preferred locations
9. Remote/hybrid/on-site preference
10. Industries
11. Preferred companies
12. Excluded companies
13. Required technologies
14. Preferred technologies
15. Excluded technologies
16. Minimum salary
17. Maximum commute tolerance
18. Visa/work authorization details
19. Availability/start date
20. CV versions (references to `ResumeVersion` records)
21. Cover letter templates
22. Screening question answers
23. References availability
24. Portfolio links
25. GitHub/LinkedIn/personal site links

## Public Profile Fields

1. Public display name
2. Public headline
3. Public professional summary
4. Public location or region (may be less precise than private location)
5. Public contact method
6. Public GitHub link
7. Public LinkedIn link
8. Public portfolio links
9. Public skills
10. Public selected projects
11. Public work history
12. Public education
13. Public research profile (if enabled)
14. Public downloadable CV version
15. Public SEO metadata

## Job Search Status

A single field on the candidate profile: `currently_looking` (boolean or enum: looking / open /
not looking). This gates:

- Whether job matching runs prominently on the dashboard.
- Whether guarded auto-apply (future) can activate at all — see
  [`docs/auto-apply-guardrails.md`](auto-apply-guardrails.md).

## Job Preferences (`JobPreference`)

Structured preferences used by the matching engine (see
[`docs/application-workflow.md`](application-workflow.md) and Phase 4 in
[`docs/phase-plan.md`](phase-plan.md)): target titles, seniority, salary range, locations,
remote/hybrid/on-site, industries, preferred/excluded companies, required/preferred/excluded
technologies, minimum salary, maximum commute.

## Auto-Apply Eligibility Fields

Fields specifically relevant to future guarded auto-apply eligibility (Phase 12):

- `currently_looking = true`
- Auto-apply explicitly enabled by the user
- Strict preference thresholds defined (minimum match score)
- No unresolved excluded-technology or excluded-company conflicts
- Truthful, complete screening answers on file for any question the target source requires

See [`docs/auto-apply-guardrails.md`](auto-apply-guardrails.md) for the full gating logic.

## Exclusions

Two dedicated exclusion lists, both first-class (not just "negative preferences"):

- **Excluded companies** — jobs from these companies are never surfaced as high-confidence
  matches, and are always excluded from any future auto-apply consideration.
- **Excluded technologies** — jobs requiring these are flagged and scored down; used as an
  explicit "reason for rejection" signal (see [`docs/application-workflow.md`](application-workflow.md)).

## Profile Truthfulness Rules

- Career Hub must never generate or publish a claim about qualifications, experience, skills,
  work rights, salary expectations, location, or identity that isn't explicitly stored and
  approved by the user.
- Draft content (cover letters, tailoring notes, public bios) is always derived from stored
  profile data — never invented — and is always subject to human review before use.
- This rule applies identically to manually written content and any future AI-assisted content
  (see [`docs/ai-integration-future.md`](ai-integration-future.md)).

## CV/Template Handling

- CV versions, cover letter templates, and screening-answer templates are stored as first-class,
  versioned records (`ResumeVersion`, template files under
  `${CAREER_HUB_BASE_PATH}/templates`), not ad-hoc uploads.
- See [`docs/resume-versioning.md`](resume-versioning.md) for the full versioning model.

## Public/Private Visibility Rules

Every profile item (a work experience entry, a skill, a project, a resume version, etc.) carries
a `VisibilitySetting`:

| Visibility | Meaning |
|---|---|
| Private only | Never shown outside the authenticated admin app |
| Public CV site | Shown on the public CV site once published |
| Job applications only | Used to prepare applications, never published publicly |
| Both public and applications | Shown publicly and used in application prep |
| Archived | Retained for history but excluded from active use and publishing |

Public routes only ever query data whose visibility includes "Public CV site" — see
[`docs/architecture.md`](architecture.md) §4 and [`docs/security.md`](security.md).
