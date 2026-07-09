# Auto-Apply Guardrails

Guarded auto-apply is the highest-risk future capability in Career Hub (Phase 12). This document
is the contract that any implementation of it must satisfy. If a proposed change would violate
any rule here, do not implement it — revisit the design instead.

## Baseline

- **Auto-apply is disabled by default** (`ENABLE_AUTO_APPLY=false`, `AUTO_APPLY_MODE=disabled`)
  in every fresh deployment, with no way to enable it accidentally via normal usage.
- The MVP (Phases 0–8) ships **no** auto-apply code path at all — this is purely a future-phase
  design contract until Phase 12.

## Required Gates (all must hold, every time, before any unattended submission)

1. **Currently looking.** The candidate profile's job-search status must be explicitly set to
   "currently looking" (see [`docs/profile-and-preferences.md`](profile-and-preferences.md)).
2. **Explicit enablement.** The user must have explicitly turned on auto-apply — never on by
   default, never re-enabled silently after being paused.
3. **Allowed source only.** The job's source must be on the `AUTO_APPLY_ALLOWED_SOURCES` list
   (official APIs, approved partner integrations, or direct employer career pages that
   themselves permit automation). Anything on `AUTO_APPLY_BLOCKED_SOURCES` (e.g. LinkedIn, SEEK,
   Indeed absent an official API) is always excluded, regardless of any other setting.
4. **Strict matching threshold.** The job's match score (see
   [`docs/application-workflow.md`](application-workflow.md)) must meet a user-configured strict
   minimum before it is even eligible for the auto-apply path.
5. **Truthful profile answers only.** No auto-submitted application may include a screening
   answer, cover letter claim, or CV claim that isn't backed by explicitly stored, approved
   profile data. If a required question can't be answered truthfully from stored data, the
   application is routed to manual review instead of submitted.
6. **User approval required in early versions.** Until a source's own official workflow supports
   fully unattended submission safely, every application — even from an allowed source — is
   routed through the approval queue described in
   [`docs/application-workflow.md`](application-workflow.md), not submitted directly.
7. **Must not violate platform terms.** See
   [`docs/compliance-and-platform-rules.md`](compliance-and-platform-rules.md) — this overrides
   every other consideration.
8. **Must not bypass security controls.** No CAPTCHA solving, no rate-limit evasion, no
   credential storage beyond what an official integration explicitly requires and securely
   supports.
9. **Full audit trail.** Every action — considered, queued, approved, submitted, rejected,
   skipped, and why — is written to the append-only `AuditLog`.
10. **Pause/kill switch.** The user can immediately pause or fully disable auto-apply at any
    time, and that pause takes effect before the next action is considered — no in-flight
    submissions continue after a pause is requested for anything not already irreversibly
    submitted.

## Non-Negotiables

- Auto-apply never operates on a source the user hasn't explicitly allow-listed.
- Auto-apply never answers a screening question in a way that contradicts stored profile data.
- Auto-apply never suppresses or delays audit logging to "catch up later".
- A configuration error (e.g. an ambiguous or missing allow-list) fails closed — no eligible
  sources, not "all sources".

## Relationship to Assisted Apply

Guarded auto-apply is an evolution of the assisted workflow (Phase 9–11), not a replacement for
it. Even once auto-apply exists, the assisted, approval-required workflow remains available and
is the default for any source or job that doesn't clear every gate above.
