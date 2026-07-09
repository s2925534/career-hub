# Phase Plan

Career Hub is built incrementally. Each phase should be committed and pushed once its checklist
items are implemented and validated. See [`TODO.md`](../TODO.md) for the live, checkbox-tracked
version of this plan — this document explains the *intent* of each phase; `TODO.md` tracks
*status*.

- **Phase 0 — Planning and documentation foundation.** Establish the README, architecture,
  decision log, security, compliance, and all planning docs before any executable code exists.
- **Phase 1 — MVP code foundation.** `.env.example`, `.gitignore`, Docker Compose, a minimal
  FastAPI app with placeholder routes, minimal SQLite schema, and operational scripts
  (create-folders, bootstrap, health-check, backup).
- **Phase 2 — Candidate profile and preferences.** Forms and storage for the candidate profile,
  job-search status, preferences, skills, target roles, salary/location/remote preferences,
  preferred/excluded companies, and visibility planning.
- **Phase 3 — Job tracker.** Manual job entry, pasted job descriptions, job URLs, list/detail
  views, status workflow, notes, follow-up dates.
- **Phase 4 — Job matching and ranking.** Rule-based scoring by title, skills, location, salary,
  remote preference, company, and exclusions, with human-readable match/rejection reasons. No AI.
- **Phase 5 — Application preparation.** Cover letter drafts, CV tailoring notes, screening
  answer templates, application checklists, a ready-to-apply queue, manual apply tracking.
- **Phase 6 — Public CV site planning and MVP.** Public/private profile split, public pages
  (home, experience, skills, projects, contact), SEO metadata, sitemap, robots.txt, deployer
  notes for the public CV domain.
- **Phase 7 — Resume generation and versioning.** Generate a resume from structured profile data,
  store versions, mark public/application-default versions, regenerate drafts when a new job is
  added, require approval before publishing, support rollback.
- **Phase 8 — Email/job alert ingestion.** Manual import of pasted email alert text first; a
  future, securely designed Gmail/IMAP integration later. No credential storage until that design
  exists.
- **Phase 9 — Platform integrations.** Adapter placeholders and research for SEEK, LinkedIn Jobs,
  and Indeed, using only official/approved access; employer career-page adapters where permitted.
  No prohibited scraping ever.
- **Phase 10 — SSO integration.** OIDC login against a self-hosted identity provider, with local
  auth retained as a fallback; admin user and roles.
- **Phase 11 — AI-assisted applications and CV generation.** Local/AI-assisted cover letter
  drafts, CV tailoring notes, public CV summaries, SEO descriptions, job-description
  summarization, and profile comparison — always draft-first, never auto-submitting or
  auto-publishing.
- **Phase 12 — Guarded auto-apply future.** Auto-apply remains disabled by default; allow-listed
  sources only, an approval queue, full audit logging, a pause/kill switch, a "currently looking"
  gate, a strict matching threshold, and a hard rule against deceptive answers.
- **Phase 13 — Advanced CV outputs.** PDF and DOCX generation, ATS-friendly text export,
  role-targeted CV variants, AI-assisted wording improvements, SEO-friendly public bio generation.
- **Phase 14 — Reporting and job-search dashboard.** Application volume, match quality, response
  rate, interview rate, company pipeline, follow-up reminders, CSV/PDF export.
- **Phase 15 — Hardening and production readiness.** Backups, restore tests, a security review,
  an SSO review, an audit review, error monitoring, dependency version pinning.

Each phase ends with: implement → validate → update `TODO.md` → commit → push.
