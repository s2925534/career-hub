# Architecture

This document describes Career Hub's architecture: the MVP as it exists (or is about to exist),
and the future shape as later phases land. See [`docs/phase-plan.md`](phase-plan.md) for the
phase breakdown and [`docs/decision-log.md`](decision-log.md) for the reasoning behind key choices.

## 1. MVP Architecture

Single Docker container running a FastAPI app, backed by SQLite, storing files on a configurable
persistent path.

```
┌────────────────────────────────────────────────────────┐
│ Career Hub container                                    │
│                                                          │
│  FastAPI app                                             │
│   ├─ Private routes (host: CAREER_HUB_PRIVATE_DOMAIN)   │
│   │   /profile /preferences /jobs /applications          │
│   │   /resume/versions /seo /dashboard ...                │
│   ├─ Public routes (host: CAREER_HUB_PUBLIC_CV_DOMAIN)   │
│   │   / /experience /skills /projects /contact            │
│   │   /download/cv /sitemap.xml /robots.txt               │
│   └─ /health                                              │
│                                                          │
│  SQLite database  ──────────────┐                        │
│  Jinja2 templates                │                        │
│                                  ▼                        │
│                    ${CAREER_HUB_BASE_PATH}/               │
│                      database/ uploads/ generated/         │
│                      exports/ backups/ logs/ templates/     │
│                      job-sources/ audit/ public/            │
└────────────────────────────────────────────────────────┘
```

Both the private admin app and the public CV site are served by the **same container** in the
MVP, distinguished by the `Host` header (or path prefix as a fallback in local dev without two
hostnames). This keeps the MVP simple; splitting into separate containers is a documented future
option (see §9), not a requirement.

Private and public route groups are implemented as clearly separated router modules so that:
- Private routes always require authentication.
- Public routes never read tables/fields marked private-only (see visibility model in
  [`docs/profile-and-preferences.md`](profile-and-preferences.md)).

## 2. Deployer-Managed Public Exposure Architecture

Career Hub never talks to Cloudflare, DNS providers, or certificate authorities. An external
deployer — this maintainer's is [`../synology-site-deployer`](../../synology-site-deployer) —
is responsible for all of that. Career Hub's only obligations to make this work:

- Bind to a single configurable host/port.
- Expose `/health` for the deployer's health checks.
- Generate correct absolute URLs (canonical links, sitemap, Open Graph) using the configured
  external URLs (`CAREER_HUB_PRIVATE_EXTERNAL_URL`, `CAREER_HUB_PUBLIC_CV_EXTERNAL_URL`), not
  by inspecting request headers it can't trust.

```
Internet ──▶ Cloudflare ──▶ Tunnel ──▶ NAS reverse proxy ──▶ Career Hub container:PORT
                 (all owned and configured by the deployer, not this repo)
```

See [`docs/deployer-integration.md`](deployer-integration.md) and
[`docs/reverse-proxy-domain.md`](reverse-proxy-domain.md) for the full contract.

## 3. Private Jobs/Admin Architecture

- Authenticated (local auth in MVP; SSO later, see §5).
- Reads/writes: candidate profile, preferences, jobs, applications, resume versions, documents,
  audit log.
- Never renders on the public hostname.
- Rule-based job matching engine runs entirely server-side, synchronously, over locally stored
  data — no external calls in the MVP.

## 4. Public CV Site Architecture

- Read-only from the visitor's perspective, aside from an optional contact form
  (`ENABLE_CONTACT_FORM`).
- Renders only fields explicitly marked with a public-visible `VisibilitySetting`.
- Serves a single "published" `PublicCvPageVersion` snapshot, not live/draft profile edits —
  this is what makes the approval-before-publish rule enforceable (see
  [`docs/resume-versioning.md`](resume-versioning.md)).
- SEO surface: sitemap.xml, robots.txt, canonical URLs, Open Graph, Schema.org `Person` /
  `ProfilePage`. See [`docs/seo-strategy.md`](seo-strategy.md).

## 5. Future SSO Architecture

- `ENABLE_SSO_AUTH` toggles OIDC-based login against an external/self-hosted identity provider
  (e.g. `auth.example.com`), alongside a local-auth fallback (`ENABLE_LOCAL_AUTH`).
- Only private/admin routes are protected by SSO; the public CV site remains open to the
  internet with no login.
- Reverse-proxy-injected auth headers are **not** trusted for identity; the app performs its own
  OIDC token validation. See [`docs/sso-integration-future.md`](sso-integration-future.md).

## 6. Future AI-Assisted Architecture

- `ENABLE_AI_ASSIST` / `ENABLE_LOCAL_AI_PROVIDER` route requests to a configurable AI backend
  (`AI_PROVIDER`, `AI_BASE_URL`) — e.g. a local Ollama-compatible endpoint at `ai.example.com`.
- AI involvement is limited to drafting: job summaries, match explanations, cover letter drafts,
  CV tailoring notes, SEO bio copy. Every AI-generated artifact is a draft requiring human review
  before it affects an application or public page.
- No AI call is ever in the critical path of submitting an application or publishing a page.
  See [`docs/ai-integration-future.md`](ai-integration-future.md).

## 7. Future Platform Integration Architecture

- Adapter pattern: one adapter per platform (SEEK, LinkedIn Jobs, Indeed, direct employer career
  pages), each gated by its own flag (`ENABLE_SEEK_INTEGRATION`, etc.) and implemented only
  against an official API or an explicitly approved/permitted access method.
- No adapter performs logged-in scraping, CAPTCHA bypass, or credential storage beyond what an
  official integration explicitly requires and securely supports.
- Adapters only ever produce `Job` records for ranking/tracking, or (later, guarded) submit
  through an approved channel — never both without the guardrails in §8.
  See [`docs/job-source-strategy.md`](job-source-strategy.md).

## 8. Future Guarded Auto-Apply Architecture

- Disabled by default (`ENABLE_AUTO_APPLY=false`).
- Requires: profile marked "currently looking", explicit opt-in, an allow-listed source, a
  strict match-score threshold, and no deceptive screening answers.
- Every candidate action passes through an approval queue before submission unless the platform
  is an approved official-API integration explicitly configured for unattended submission — and
  even then, every action is logged to an append-only audit trail with a hard kill switch.
  See [`docs/auto-apply-guardrails.md`](auto-apply-guardrails.md).

## 9. Resume Versioning Architecture

- `ResumeVersion` and `PublicCvPageVersion` are versioned, immutable-once-published records tied
  to the structured `CareerProfile` data at the time of generation.
- Adding a `WorkExperience` (new job) triggers a draft regeneration, never an automatic publish.
- Only an explicit "publish" action promotes a draft to the live public version; the previous
  live version remains available for rollback.
  See [`docs/resume-versioning.md`](resume-versioning.md).

## Future Option: Splitting Private and Public Into Separate Containers

The MVP intentionally keeps one container serving both hostnames to minimize operational
complexity. If the private admin surface grows heavy (e.g. background workers, AI calls) while
the public CV site needs to stay lightweight and fast for SEO, splitting into
`career-hub-admin` and `career-hub-public` containers sharing the same SQLite/Postgres database
is a reasonable future evolution. This is not required for MVP and should only be done with a
clear justification (see [`docs/decision-log.md`](decision-log.md)).
