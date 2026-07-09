# Security

Career Hub stores sensitive personal and career data. This document describes the security
model for the MVP and the assumptions later phases must preserve.

## Secrets Handling

- No real secrets are ever committed to this repository. `.env.example` contains placeholders
  only (e.g. `APP_SECRET_KEY=change-me-generate-a-long-random-secret`).
- `APP_SECRET_KEY` must be a long, random, unique value per deployment. Generate one with, e.g.,
  `openssl rand -hex 32` or `python -c "import secrets; print(secrets.token_hex(32))"`.
- SSO client secrets, AI provider keys, and any future platform API credentials follow the same
  rule: placeholders in `.env.example`, real values only in an untracked `.env`.

## `.env` Handling

- `.env` is listed in `.gitignore` and must never be committed.
- Only `.env.example` (safe placeholders) is tracked in Git.
- Scripts (`bootstrap-career-hub.sh`, `health-check.sh`, `backup-career-hub.sh`) load `.env` if
  present but never print its contents, and never fail silently if secrets are missing — they
  warn.

## Profile Privacy

- Candidate profile data (target companies, excluded companies, salary expectations, work
  rights, visa details, private notes) is private-only by default. See the visibility model in
  [`docs/profile-and-preferences.md`](profile-and-preferences.md).
- Nothing is exposed on the public CV site unless a field's `VisibilitySetting` is explicitly set
  to include public visibility.

## CV/Cover Letter Privacy

- Uploaded and generated CVs, cover letters, and screening answers are stored under
  `${CAREER_HUB_BASE_PATH}/uploads` and `${CAREER_HUB_BASE_PATH}/generated`, both private by
  default.
- A CV version is only served on the public CV site if explicitly marked as the published public
  version (see [`docs/resume-versioning.md`](resume-versioning.md)).

## Public/Private Profile Separation

Data that must **never** be published automatically to the public CV site:

1. Job application history
2. Target companies
3. Excluded companies
4. Salary expectations
5. Private notes
6. Recruiter notes
7. Screening answers
8. Draft cover letters
9. Application status
10. Job search strategy
11. Internal match scores
12. Any uploaded private CV version, unless explicitly selected for publication
13. Personal documents
14. Internal audit logs
15. Job platform credentials or tokens

Public routes must only ever query fields/tables explicitly marked public-visible. This is
enforced structurally (public route handlers only read `PublicProfile` / published
`PublicCvPageVersion` data), not by filtering private fields at render time.

## Job Platform Credential Warning

Career Hub does not store job platform (LinkedIn, SEEK, Indeed, etc.) passwords or session
cookies in the MVP or in any currently planned phase, except where an **official, approved API
integration** explicitly requires a credential (e.g. an OAuth token issued by that platform's own
developer program) and a secure storage design (encryption at rest, scoped access, rotation) has
been implemented first. See [`docs/compliance-and-platform-rules.md`](compliance-and-platform-rules.md).

## Public Exposure Rules

- Public exposure (making `jobs.example.com` or `cv.example.com` reachable from the internet) is
  handled entirely by the external deployer project, never by this repo.
- This repo defaults to local/LAN-only operation (`PUBLIC_EXPOSURE=false`, `DEPLOY_MODE=local_only`).
- Only the Career Hub web app's single HTTP endpoint should ever be exposed. The database file,
  logs, backups, and internal storage folders must never be exposed publicly.
- This project must never expose Synology DSM or SSH. Those are entirely out of scope and must
  remain the deployer's and the NAS's own responsibility.

## Audit Log

- Every generated and submitted application action is recorded in an append-only `AuditLog`.
- Every public CV publication event (publish, rollback) is recorded in the same audit log.
- The audit log is private-only and stored under `${CAREER_HUB_BASE_PATH}/audit`.

## Auto-Apply Risk

Guarded auto-apply (Phase 12) is the highest-risk future feature in this project: submitting
applications on the user's behalf carries legal (platform ToS), reputational (bad applications),
and ethical (deceptive answers) risk if implemented carelessly. It is disabled by default and
must ship with an allow-list, an approval queue, full audit logging, and a kill switch before it
can be enabled. See [`docs/auto-apply-guardrails.md`](auto-apply-guardrails.md).

## Public CV Publishing Risk

Publishing incorrect, stale, or overly detailed information to a public, indexed website is a
lower-severity but real risk (reputational, or leaking information you'd rather keep private).
Mitigated by requiring explicit review/approval before publish (ADR-010) and by rollback support.

## SSO Future

When `ENABLE_SSO_AUTH` lands, private/admin routes will validate OIDC tokens against the
configured issuer (`SSO_ISSUER_URL`) directly in the app — not merely trust a reverse-proxy
header — so that a misconfigured proxy cannot silently disable authentication. See
[`docs/sso-integration-future.md`](sso-integration-future.md).

## Backup and Restore

- `scripts/backup-career-hub.sh` creates timestamped, non-destructive backups of the database,
  uploads, templates, generated resumes, public CV assets, exports, and audit logs under
  `${CAREER_HUB_BASE_PATH}/backups`.
- Restore is a manual, deliberate process (see `scripts/restore-notes.md`) — there is no
  automatic destructive restore in this project.
- Backups themselves are not currently encrypted or automatically shipped off-box; if you back up
  to remote storage, ensure that storage is itself access-controlled and, ideally, encrypted.

## Account Recovery

- MVP local auth is single-admin. If the admin password is lost, recovery requires direct access
  to the host/container to reset it (e.g. re-running a password-set script against the SQLite
  database) — there is no email-based password reset in the MVP, since there is no outbound
  email integration yet.
- Once SSO is integrated, account recovery follows the identity provider's own recovery flow.
