# Career Hub

A self-hosted career management hub: track your job search, prepare tailored applications,
manage resume/CV versions, and publish a public, SEO-friendly CV/resume site — all from data
you own, running on your own infrastructure.

> **Status:** Phase 0 (planning) / early Phase 1 (minimal code foundation). Not production-ready.

## Developer

Pedro Veloso — pedro@veloso.dev

## What This Is

Career Hub is a generic, open-source, self-hostable application. It is **not** tied to any
specific person, company, or domain. The examples in this repo use generic placeholder
hostnames (`jobs.example.com`, `cv.example.com`) — swap them for your own. Where you see
`jobs.veloso.dev` / `cv.veloso.dev` in a doc, that's one maintainer's own personal deployment,
called out explicitly as a "personal example," never as a default. Nothing in the code, package
name, or documentation should be read as "only works for veloso.dev". If you find such a
reference, it's a bug — please report or fix it.

Career Hub has two faces:

- **Private side** (example host: `jobs.example.com`) — an authenticated admin app where you
  manage your candidate profile, job preferences, tracked jobs, application pipeline, and
  resume/CV versions.
- **Public side** (example host: `cv.example.com`) — a public, SEO-friendly CV/resume/profile
  site that only shows what you've explicitly approved for publication.

## What This Project Does

- Lets you define a candidate profile and job-search preferences.
- Tracks jobs you're interested in (manual entry, pasted job descriptions, saved links).
- Ranks/matches jobs against your profile with an explainable, rule-based score.
- Helps you prepare applications: tailored CV notes, draft cover letters, checklists.
- Tracks application status end-to-end (interested → applied → interview → offer/rejected).
- Manages multiple resume/CV versions (draft, public, application-default, role-targeted, archived).
- Publishes an approved subset of your profile as a public, SEO-friendly CV/resume site.
- Keeps an audit trail of generated applications and public-CV publication events.

## What This Project Does Not Do

- It does **not** scrape LinkedIn, SEEK, Indeed, or any other platform behind a login or in a
  way that violates their terms of service.
- It does **not** create fake accounts, bypass CAPTCHAs, evade bot detection, or bypass rate
  limits on any platform.
- It does **not** submit job applications automatically in the MVP. Every generated application
  is draft-first and requires your explicit review and approval.
- It does **not** implement Cloudflare, DNS, tunnels, reverse proxy routing, or certificate
  management. That is handled by a separate deployer project (see below).
- It does **not** publish unapproved profile or resume changes to the public CV site.
- It does **not** fabricate qualifications, experience, skills, work rights, salary
  expectations, location, or identity. Generated content is always derived from data you
  explicitly stored and approved.

## Why Assisted-Apply First, Not Auto-Apply

Automating job applications across third-party platforms without their cooperation risks
violating platform terms of service, damaging your standing with employers, and producing
low-quality or inaccurate applications. This project starts with a **manual, assisted workflow**:
you add jobs, the system ranks and helps you prepare materials, and you decide what to submit
and when. A future **guarded auto-apply** mode is planned (see
[`docs/auto-apply-guardrails.md`](docs/auto-apply-guardrails.md)), but it will only ever apply to
allowed sources (official APIs, approved integrations, direct employer pages that permit
automation), will require explicit opt-in and strict matching thresholds, and will always be
logged and auditable.

## Why Public CV Publishing Requires Approval

Your private career data (target companies, salary expectations, recruiter notes, application
history, draft cover letters, internal match scores) must never leak onto a public page. To keep
that boundary reliable, publishing to the public CV site is a deliberate, reviewed action, not a
side effect of editing your profile. See [`docs/public-cv-site.md`](docs/public-cv-site.md) and
[`docs/security.md`](docs/security.md).

## Architecture (Text Diagram)

```
                          ┌─────────────────────────────────────┐
                          │        ../synology-site-deployer     │
                          │  (DNS, Cloudflare, tunnels, certs,   │
                          │   reverse proxy, NAS deploy paths)   │
                          └───────────────┬───────────────────────┘
                                          │ routes by hostname
                 ┌────────────────────────┼────────────────────────┐
                 │                        │                        │
        https://jobs.example.com                          https://cv.example.com
        (private, authenticated)                          (public, SEO-friendly)
                 │                        │                        │
                 └────────────┬───────────┘                        │
                              ▼                                    ▼
                    ┌───────────────────────────────────────────────────┐
                    │              Career Hub web app (this repo)        │
                    │  FastAPI app, single container for MVP             │
                    │  - Private routes: profile, preferences, jobs,     │
                    │    applications, resume versions, public-CV admin  │
                    │  - Public routes: CV home, experience, skills,     │
                    │    projects, contact, sitemap.xml, robots.txt      │
                    └───────────────────────┬─────────────────────────┘
                                             ▼
                                 ┌───────────────────────┐
                                 │  SQLite (MVP)          │
                                 │  CAREER_HUB_BASE_PATH  │
                                 │  (uploads, generated,  │
                                 │   exports, backups,    │
                                 │   audit log)           │
                                 └───────────────────────┘
```

## Deployer-Managed Domains

This repo assumes an external deployer (in this maintainer's case,
[`../synology-site-deployer`](../synology-site-deployer)) owns DNS, Cloudflare, tunnels,
certificates, and reverse proxy routing. Career Hub only needs to:

- Bind to a configurable host/port (`CAREER_HUB_BIND_HOST`, `CAREER_HUB_HTTP_PORT`).
- Expose a `/health` endpoint.
- Respect the hostnames it's told about (`CAREER_HUB_PRIVATE_DOMAIN`, `CAREER_HUB_PUBLIC_CV_DOMAIN`)
  for generating correct absolute URLs, canonical links, and sitemaps.

See [`docs/deployer-integration.md`](docs/deployer-integration.md) and
[`docs/reverse-proxy-domain.md`](docs/reverse-proxy-domain.md).

## No Fixed Synology Volume Path

This project never assumes `/volume1` or any other fixed NAS path. All persistent data lives
under a single configurable `CAREER_HUB_BASE_PATH` variable. When deployed manually, point it at
any folder. When deployed via a NAS deployer, the deployer decides the final path. See
[`docs/deployer-integration.md`](docs/deployer-integration.md).

## Security & Compliance Warning

Career Hub stores sensitive personal and career data (profile details, salary expectations,
application history, uploaded documents). Read [`docs/security.md`](docs/security.md) and
[`docs/compliance-and-platform-rules.md`](docs/compliance-and-platform-rules.md) before deploying
or extending this project, especially before enabling any future auto-apply, AI, or platform
integration features.

## Phase Overview

Development proceeds in phases, from planning docs through MVP code to future integrations
(SSO, local AI, platform APIs, guarded auto-apply). See [`docs/phase-plan.md`](docs/phase-plan.md)
and [`TODO.md`](TODO.md) for the full breakdown and current status.

## Documentation Index

| Doc | Purpose |
|---|---|
| [`docs/architecture.md`](docs/architecture.md) | System architecture, current and future |
| [`docs/phase-plan.md`](docs/phase-plan.md) | Full phase breakdown (Phase 0–15) |
| [`docs/decision-log.md`](docs/decision-log.md) | Architecture decision records |
| [`docs/security.md`](docs/security.md) | Security model and practices |
| [`docs/compliance-and-platform-rules.md`](docs/compliance-and-platform-rules.md) | Legal/ethical/platform-terms rules |
| [`docs/deployer-integration.md`](docs/deployer-integration.md) | How this repo is consumed by a NAS deployer |
| [`docs/reverse-proxy-domain.md`](docs/reverse-proxy-domain.md) | Domain/hostname routing assumptions |
| [`docs/job-source-strategy.md`](docs/job-source-strategy.md) | Where jobs come from, and what's off-limits |
| [`docs/profile-and-preferences.md`](docs/profile-and-preferences.md) | Candidate/public profile & preferences model |
| [`docs/application-workflow.md`](docs/application-workflow.md) | Manual and assisted application workflow |
| [`docs/auto-apply-guardrails.md`](docs/auto-apply-guardrails.md) | Guardrails for future guarded auto-apply |
| [`docs/public-cv-site.md`](docs/public-cv-site.md) | Public CV/resume site plan |
| [`docs/resume-versioning.md`](docs/resume-versioning.md) | Resume/CV version model |
| [`docs/seo-strategy.md`](docs/seo-strategy.md) | SEO plan for the public CV site |
| [`docs/ai-integration-future.md`](docs/ai-integration-future.md) | Future local/AI-assisted features |
| [`docs/sso-integration-future.md`](docs/sso-integration-future.md) | Future SSO/OIDC integration |
| [`docs/troubleshooting.md`](docs/troubleshooting.md) | Common problems and fixes |
| [`docs/future-flags.md`](docs/future-flags.md) | Full catalog of feature flags, current and future |

## License

MIT. See [`LICENSE`](LICENSE). Free to use, modify, and self-host, with no warranties —
the software is provided "as is", without warranty of any kind, express or implied.
Contributions and forks for other people's own career hubs are welcome.
