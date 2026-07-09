# Compliance and Platform Rules

Career Hub is designed to help with job search and applications **without** violating job
platform terms of service or engaging in deceptive automation. These rules apply to every phase
of this project, including all future integrations.

## Hard Rules

1. **Do not scrape platforms in violation of their terms of service.** If a platform's terms
   prohibit scraping, this project must not scrape it, regardless of technical feasibility.
2. **Do not automate logged-in platform sessions unless explicitly allowed.** Automating actions
   inside an authenticated session on a third-party platform is only acceptable when that
   platform's own terms or official API explicitly permit it.
3. **Do not bypass CAPTCHAs.** Any CAPTCHA encountered is a signal to stop, not a puzzle to solve
   programmatically.
4. **Do not bypass rate limits.** Respect published or observed rate limits on any external
   service.
5. **Do not create fake accounts.** All integrations operate under the user's own, real,
   authorized account/API credentials.
6. **Do not misrepresent qualifications.** Generated CVs, cover letters, screening answers, and
   public profile content must never claim experience, skills, qualifications, work rights,
   salary expectations, location, or identity that isn't explicitly stored and approved by the
   user.
7. **Do not submit applications without an allowed workflow.** In the MVP, that means no
   automated submission at all — every application is submitted manually by the user. In future
   phases, it means only through an approved assisted or guarded auto-apply workflow (see
   [`docs/auto-apply-guardrails.md`](auto-apply-guardrails.md)).

## Platform-Specific Rule

SEEK, LinkedIn, Indeed, and similar platforms must only ever be integrated with through:

- An **official API** (e.g. a published partner/developer API with proper authentication), or
- An **approved integration** (explicit partner/affiliate access granted by the platform).

Absent either, no integration with that platform is built, regardless of user demand. This
applies to job import, job matching data, and especially application submission.

## Allowed MVP Paths

These are always compliant, since they involve no automation against a third-party platform:

- Manual job entry (typing in a job's details yourself).
- User-pasted job descriptions (copy-pasting text you already have permission to view).
- Manually saved job URLs (a link is just a link; the system does not crawl it without the
  user's data-fetch action being a simple, low-volume, terms-respecting fetch of a single public
  page the user explicitly requested).
- Public RSS/API feeds where the source publishes them for this exact purpose.

## Direct Employer Applications

When a job posting links directly to an employer's own career page (not a third-party platform),
this project should respect that employer site's terms of service and `robots.txt`. Direct
employer integrations (Phase 9) are only automated where the employer's site or ATS explicitly
allows it.

## Audit Logging for Automated Actions

Any future action that is automated (an official-API job import, an approved-workflow
application submission) must be recorded in the `AuditLog` with what was done, when, against
which source, and under which user approval — see [`docs/security.md`](security.md) and
[`docs/auto-apply-guardrails.md`](auto-apply-guardrails.md).

## What To Do If a Feature Would Require Breaking These Rules

If a desired feature (e.g. "auto-apply on SEEK") cannot be built without violating a platform's
terms of service, the correct outcome is to **not build it** — document it as blocked in
[`docs/job-source-strategy.md`](job-source-strategy.md) and wait for an official/approved access
path, rather than implementing a workaround.
