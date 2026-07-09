# Public CV Site

The public side of Career Hub: an SEO-friendly professional profile that helps people discover
you, understand your background, and get in touch — built entirely from data you've explicitly
approved for publication.

## Purpose

Give recruiters, hiring managers, collaborators, and anyone else who finds you a clean,
fast, accurate, and discoverable public professional profile — without exposing any of your
private job-search activity.

## Personal Example

Personal public CV hostname example: `cv.veloso.dev`. Generic form: `cv.example.com`. See
[`docs/reverse-proxy-domain.md`](reverse-proxy-domain.md) for the full hostname model.

## Public/Private Data Separation

The public CV site only ever renders:

- `PublicProfile` fields (see [`docs/profile-and-preferences.md`](profile-and-preferences.md)).
- The currently-published `PublicCvPageVersion` snapshot (not live/draft profile edits).
- Individual profile items (`WorkExperience`, `Skill`, `Project`, `Education`, `Certification`,
  `Publication`) whose `VisibilitySetting` includes public visibility.

It never renders: application history, target/excluded companies, salary expectations, private
notes, screening answers, draft cover letters, application status, match scores, or any
unpublished CV version. See [`docs/security.md`](security.md) for the enforcement model.

## Public Pages

1. `/` — public profile home
2. `/experience` — work history
3. `/projects` — selected public projects
4. `/research` — research/academic profile, only if `ENABLE_RESEARCH_PROFILE`
5. `/skills` — public skills
6. `/contact` — contact page or contact instructions
7. `/download/cv` — approved public CV download
8. `/sitemap.xml`
9. `/robots.txt`

## SEO Goals

Unique titles, meta descriptions, canonical URLs, Open Graph/Twitter cards, Schema.org `Person`
and `ProfilePage` structured data, a sitemap, a robots.txt, clean URLs, mobile-friendly and
fast-loading pages. Full detail in [`docs/seo-strategy.md`](seo-strategy.md).

## Public Profile Data

See the "Public Profile Fields" list in
[`docs/profile-and-preferences.md`](profile-and-preferences.md) — public display name, headline,
summary, region, contact method, GitHub/LinkedIn/portfolio links, skills, selected projects,
work history, education, optional research profile, downloadable CV, SEO metadata.

## Approval Workflow

Publishing is always an explicit action:

1. Edit structured profile data in the private admin app.
2. Generate/preview a new `PublicCvPageVersion` draft.
3. Review the draft.
4. Explicitly publish it — only then does it become the live public version.

No edit to private profile data automatically appears on the public site. See
[`docs/resume-versioning.md`](resume-versioning.md) for the versioning mechanics and ADR-010 in
[`docs/decision-log.md`](decision-log.md) for the reasoning.

## Rollback Workflow

Every publish creates a new version; the prior live version is retained and can be restored as
the live version at any time. See [`docs/resume-versioning.md`](resume-versioning.md).

## Contact Options

- MVP: a simple "contact instructions" block (e.g. "email me at ...") — no form, no spam surface.
- Future (`ENABLE_CONTACT_FORM`): an actual contact form with spam protection, storing submitted
  messages privately as `ContactMessage` records — never publicly visible, never auto-replied
  to without review.

## Deployer Routing Assumptions

The public CV hostname is routed to this app by the external deployer exactly like the private
hostname (same container, different `Host` header) — see
[`docs/deployer-integration.md`](deployer-integration.md) and
[`docs/reverse-proxy-domain.md`](reverse-proxy-domain.md). The public CV site requires no
authentication and must remain reachable even if the private admin app's auth backend (local or
future SSO) is temporarily unavailable, since they are logically independent route groups within
the same process.
