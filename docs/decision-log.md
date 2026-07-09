# Decision Log

Architecture Decision Record (ADR) style log. Each entry: context, decision, consequences.
Newest entries at the bottom.

## ADR-001: Project and repository name

**Context:** Needed a name that describes the product, not the maintainer's personal domain.

**Decision:** Name the project and repository `career-hub`.

**Consequences:** Package names, container names, and default env values use `career-hub` /
`CAREER_HUB_*`, never a personal name or domain.

## ADR-002: Keep the project generic and MIT-friendly

**Context:** This repo should be reusable by anyone self-hosting their own career tooling, not
just the original maintainer.

**Decision:** License as MIT. Avoid hardcoding any person's name, domain, or branding into code,
package metadata, or docs. Personal deployment details only ever appear as clearly labeled
"personal example" values.

**Consequences:** Every doc that mentions `jobs.veloso.dev` / `cv.veloso.dev` also shows the
generic `jobs.example.com` / `cv.example.com` form and says so explicitly.

## ADR-003: Personal domains are examples only

**Context:** The maintainer has real hostnames they intend to deploy to, but the repo must not
assume any specific person's domain.

**Decision:** Use `jobs.veloso.dev` as the maintainer's personal private deployment example and
`cv.veloso.dev` as their personal public CV deployment example, always alongside the generic
`*.example.com` equivalents.

**Consequences:** `.env.example` defaults to `example.com`-style placeholders; personal values
live only in the maintainer's own untracked `.env` and in "personal example" callouts in docs.

## ADR-004: FastAPI + SQLite for the MVP

**Context:** Needed a backend/database stack that is simple, runs well on a Synology NAS or a
plain laptop, and doesn't require an extra database service for a single-user MVP.

**Decision:** Use Python FastAPI for the backend and server-rendered Jinja2 templates (HTMX if
useful) for the frontend. Use SQLite as the MVP database, with a documented future option to move
to PostgreSQL (`ENABLE_POSTGRES_PRODUCTION_DB`) if concurrency or multi-user needs grow.

**Consequences:** No database container is required for MVP deployment. `DATABASE_URL` is
already structured as a standard SQLAlchemy-style URL so switching to Postgres later is a config
change, not a rewrite.

## ADR-005: Cloudflare/exposure stays in the deployer project

**Context:** The maintainer already has a working, tested deployment automation project,
[`../synology-site-deployer`](../../synology-site-deployer), that owns Cloudflare, DNS, tunnels,
certificates, and reverse proxy routing for all their self-hosted apps.

**Decision:** Career Hub never implements Cloudflare/DNS/tunnel/certificate automation. It only
provides a Docker Compose file, environment variables, a `/health` endpoint, and documentation
describing expected ports/routes/hostnames, consumed by `synology-site deploy`.

**Consequences:** This repo has no Cloudflare API credentials, no DNS logic, and no tunnel code,
by design — see [`docs/deployer-integration.md`](deployer-integration.md).

## ADR-006: No hardcoded Synology volume paths

**Context:** The maintainer's other project manages NAS volume placement; this repo should stay
portable across NAS, local Docker, and future Linux server deployments.

**Decision:** All persistent paths derive from a single `CAREER_HUB_BASE_PATH` variable, default
`./data/career-hub` for local/manual use. No code or Compose file ever references `/volume1` or
similar.

**Consequences:** The deployer can mount `CAREER_HUB_BASE_PATH` at whatever path it chooses;
Career Hub does not need to know or care.

## ADR-007: Manual/imported jobs before any scraping

**Context:** Automated scraping of logged-in job platforms risks violating their terms of
service and is legally/ethically risky.

**Decision:** MVP job sources are manual entry, pasted job descriptions/URLs, and (later) manual
import of pasted email alert text and public RSS/API sources. See
[`docs/job-source-strategy.md`](job-source-strategy.md).

**Consequences:** No scraping code exists in this repo. Platform integrations are deferred to
Phase 9 and gated on official/approved access.

## ADR-008: Official APIs / permitted integrations only

**Context:** Same as ADR-007 — this extends the rule to any future platform integration, not
just the MVP.

**Decision:** SEEK, LinkedIn Jobs, Indeed, and similar platform integrations will only ever be
built against an official API or an explicitly approved/permitted access method. No adapter may
automate a logged-in session, bypass CAPTCHAs, bypass rate limits, or create fake accounts.

**Consequences:** See [`docs/compliance-and-platform-rules.md`](compliance-and-platform-rules.md)
and [`docs/auto-apply-guardrails.md`](auto-apply-guardrails.md).

## ADR-009: Auto-apply disabled by default

**Context:** Fully automated job applications carry legal, ethical, and reputational risk if
done carelessly.

**Decision:** `ENABLE_AUTO_APPLY=false` by default, and the MVP does not submit any application
without explicit manual user action. Guarded auto-apply is a documented future phase (Phase 12)
with strict allow-lists, approval queues, audit logging, and a kill switch.

**Consequences:** No code path in the MVP can submit a job application on the user's behalf.

## ADR-010: Review required before public CV publishing

**Context:** Private career data (target companies, salary expectations, application history)
must never leak onto the public CV site, and public-facing career claims must always be accurate.

**Decision:** Publishing to the public CV site is always an explicit, reviewed action
(`ENABLE_REVIEW_BEFORE_PUBLICATION`), producing a new `PublicCvPageVersion`, never a live mirror
of in-progress profile edits.

**Consequences:** See [`docs/resume-versioning.md`](resume-versioning.md) and
[`docs/public-cv-site.md`](public-cv-site.md).

## ADR-011: SSO deferred to a self-hosted identity provider

**Context:** MVP needs *some* auth to protect private routes, but building a full SSO/OIDC
integration up front would slow down the planning-first approach this project is taking.

**Decision:** Use simple local authentication for MVP (`ENABLE_LOCAL_AUTH=true`), with a future,
optional OIDC integration against a self-hosted identity provider such as `auth.example.com`
(`ENABLE_SSO_AUTH`), documented in [`docs/sso-integration-future.md`](sso-integration-future.md).

**Consequences:** MVP auth is intentionally minimal (single admin user, hashed password) — not a
general-purpose multi-tenant auth system.

## ADR-012: Local AI deferred and optional

**Context:** AI can help draft cover letters, tailor CVs, and summarize job descriptions, but
should not be a dependency for the MVP to function, and must never be trusted to submit or
publish content unattended.

**Decision:** AI integration (`ENABLE_AI_ASSIST`, `ENABLE_LOCAL_AI_PROVIDER`) is deferred to
Phase 11, targeting a local Ollama-compatible endpoint (e.g. `ai.example.com`) or another
configurable provider, always producing drafts that require human review.

**Consequences:** See [`docs/ai-integration-future.md`](ai-integration-future.md).
