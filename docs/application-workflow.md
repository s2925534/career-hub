# Application Workflow

How a job goes from "noticed" to "applied" (and beyond) in Career Hub. See
[`docs/job-source-strategy.md`](job-source-strategy.md) for where jobs come from and
[`docs/auto-apply-guardrails.md`](auto-apply-guardrails.md) for the future automated path.

## Manual Workflow (MVP)

1. Add a job manually, or paste a job URL/description.
2. Career Hub parses whatever structured details it can from the pasted text (title, company,
   location — best-effort, no external calls).
3. The job is ranked against your profile/preferences (Phase 4); you see a match score and a
   plain-language explanation.
4. Career Hub generates an application checklist for the job.
5. Career Hub generates tailored CV notes based on your stored profile and the job's requirements.
6. Career Hub generates a draft cover letter from your templates and the job details.
7. You track status manually as one of: `interested`, `drafting`, `ready_to_apply`, `applied`,
   `rejected`, `interview`, `offer`, `archived`.
8. You apply on the employer/platform's own site yourself, then mark the job as `applied` in
   Career Hub.
9. Career Hub stores: application date, application URL, notes, contact person, follow-up date,
   and eventual outcome.

## Application Statuses

`interested` → `drafting` → `ready_to_apply` → `applied` → (`interview` → `offer`) | `rejected` |
`archived` (terminal, reachable from any state).

## Ready-to-Apply Queue

Jobs marked `ready_to_apply` surface in a dedicated queue view, so you can batch through the
final review-and-submit step without hunting through the full job tracker.

## Follow-Up Tracking

Each `Application` may carry a `follow_up_date`. The dashboard (Phase 14) surfaces applications
whose follow-up date has arrived, so nothing silently goes stale.

## Future Assisted Workflow (Phase 9–12, allowed sources only)

1. Import a job from an allowed source (official API / permitted feed).
2. Rank it exactly as in the manual workflow.
3. Generate the same application pack (CV notes, cover letter, checklist).
4. Queue it for approval instead of leaving it in your general backlog.
5. You review the generated pack.
6. You approve it.
7. Career Hub either opens the official application URL for you to complete manually, or — only
   for sources with an official, approved submission API — submits through that API.
8. The action is logged to the audit trail.
9. Career Hub stores the confirmation/result.

This is "assisted", not "auto" — a human approves every submission at this stage. See
[`docs/auto-apply-guardrails.md`](auto-apply-guardrails.md) for what additionally has to be true
before any submission can happen without a per-application approval click.

## Audit Log

Every generated application pack, every status change driven by an automated adapter, and every
submission (assisted or, eventually, guarded-auto) is written to the append-only `AuditLog` —
see [`docs/security.md`](security.md).
