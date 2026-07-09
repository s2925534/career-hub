# Resume/CV Versioning

Career Hub treats resumes/CVs as versioned artifacts derived from structured profile data, not
as one-off uploaded files. This document is the planning reference for that model. See
[`docs/public-cv-site.md`](public-cv-site.md) for how the public version is published and
[`docs/profile-and-preferences.md`](profile-and-preferences.md) for the underlying profile data.

## Resume Version Types

- **Draft version** — a generated or in-progress version not yet designated for any specific use.
- **Public CV version** — the version currently published on the public CV site
  (`PublicCvPageVersion`, one live at a time).
- **Job application default version** — the version used by default when preparing new
  applications (`ResumeVersion` flagged as application-default).
- **Role-targeted version** — a variant tailored to a specific target role/title (future,
  `ENABLE_ROLE_TARGETED_RESUME`).
- **Archived version** — retained for history, excluded from active use.

## How New Jobs Update the Structured Profile

1. You add a new `WorkExperience` (new job/role) in the private admin area: company, title,
   start date, location, employment type, role summary, technologies, responsibilities,
   achievements, and a visibility setting (private / public CV / both).
2. Career Hub updates the structured `CareerProfile` immediately — this is just normal profile
   data entry, not a publishing action.

## How New Jobs Generate Resume Drafts

3. Career Hub generates a new **draft** `ResumeVersion` reflecting the updated profile
   (`ENABLE_AUTO_RESUME_UPDATE_ON_NEW_JOB`).
4. If the new role is marked public-visible, Career Hub also generates a draft
   `PublicCvPageVersion` reflecting the change — still a draft, not yet live.

## Approval Before Publication

5. You review the generated draft(s).
6. You explicitly approve/publish a draft to promote it to the live public version or the
   application-default version (`ENABLE_REVIEW_BEFORE_PUBLICATION`). Nothing is published
   automatically, regardless of how the draft was generated (manual edit or future AI
   assistance — see [`docs/ai-integration-future.md`](ai-integration-future.md)).

## Rollback

7. Publishing a new version never deletes the previous one — it simply changes which version is
   flagged "live". Rolling back means re-flagging a prior version as live
   (`ENABLE_CV_VERSIONING`), which is itself an audited action.

## MVP Scope

The MVP supports manual editing of structured CV/profile data and generation of a single public
web page from that data (Phase 6–7). It does **not** attempt PDF/DOCX/ATS/role-targeted output
generation yet — those are Phase 13 (`ENABLE_CV_PDF_EXPORT`, `ENABLE_CV_DOCX_EXPORT`,
`ENABLE_ATS_RESUME_EXPORT`, `ENABLE_ROLE_TARGETED_RESUME`). Building the full output matrix
before the structured-data foundation and approval workflow exist would be premature.

## Future Outputs (Phase 13, not required for MVP)

1. Web page profile (MVP scope)
2. Downloadable PDF resume
3. Downloadable DOCX resume, if practical
4. Plain text resume
5. ATS-friendly resume version
6. Role-targeted resume versions
7. Public short bio
8. Public long bio
