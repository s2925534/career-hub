# TODO

Status-tracked checklist for all phases. See [`docs/phase-plan.md`](docs/phase-plan.md) for the
narrative version of each phase's intent. Check items off as they're implemented, validated,
committed, and pushed.

## Phase 0: Planning and Documentation Foundation

- [x] Create README.
- [x] Create architecture document.
- [x] Create phase plan.
- [x] Create decision log.
- [x] Create security document.
- [x] Create compliance and platform rules document.
- [x] Create deployer integration notes.
- [x] Create reverse proxy/domain notes.
- [x] Create job source strategy.
- [x] Create profile and preferences document.
- [x] Create application workflow document.
- [x] Create auto-apply guardrails.
- [x] Create public CV site document.
- [x] Create resume versioning document.
- [x] Create SEO strategy document.
- [x] Create AI integration future notes.
- [x] Create SSO integration future notes.
- [x] Create troubleshooting guide.
- [x] Create future flags.
- [x] Create TODO with phases and checkboxes.
- [x] Validate docs.
- [x] Commit and push.

## Phase 1: MVP Code Foundation

- [x] `.env.example`.
- [x] `.gitignore`.
- [x] Docker Compose.
- [x] Basic FastAPI app or equivalent.
- [x] Basic SQLite database setup.
- [x] Folder creation script.
- [x] Bootstrap script.
- [x] Health check script.
- [x] Backup script.
- [x] Initial local-only startup.
- [x] Basic validation.
- [x] Commit and push.

## Phase 2: Candidate Profile and Preferences

- [ ] Candidate profile form.
- [ ] Job search status.
- [ ] Preferences form.
- [ ] Skills list.
- [ ] Target roles.
- [ ] Salary/location/remote preferences.
- [ ] Preferred and excluded companies.
- [ ] CV/template upload placeholders.
- [ ] Public/private visibility planning.
- [ ] Commit and push.

## Phase 3: Job Tracker

- [ ] Add job manually.
- [ ] Paste job description.
- [ ] Store job URL.
- [ ] Job list.
- [ ] Job detail page.
- [ ] Status workflow.
- [ ] Notes.
- [ ] Follow-up dates.
- [ ] Commit and push.

## Phase 4: Job Matching and Ranking

- [ ] Rule-based matching first.
- [ ] Score by title, skills, location, salary, remote, company, and exclusions.
- [ ] Show reason for match.
- [ ] Show reason for rejection.
- [ ] Do not use AI yet unless explicitly enabled later.
- [ ] Commit and push.

## Phase 5: Application Preparation

- [ ] Cover letter draft template.
- [ ] CV tailoring notes.
- [ ] Screening answer templates.
- [ ] Application checklist.
- [ ] Ready-to-apply queue.
- [ ] Manual apply tracking.
- [ ] Commit and push.

## Phase 6: Public CV Site Planning and MVP

- [ ] Public/private profile split.
- [ ] Public profile home page.
- [ ] Experience page.
- [ ] Skills page.
- [ ] Projects page.
- [ ] Contact page or contact instructions.
- [ ] SEO metadata.
- [ ] Sitemap.
- [ ] Robots.txt.
- [ ] Public/private visibility handling.
- [ ] Deployer notes for the public CV domain.
- [ ] Commit and push.

## Phase 7: Resume Generation and Versioning

- [ ] Generate resume from structured profile.
- [ ] Store resume versions.
- [ ] Mark one version as public.
- [ ] Mark one version as job-application default.
- [ ] Track changes when a new job is added.
- [ ] Require approval before publishing.
- [ ] Add rollback support.
- [ ] Commit and push.

## Phase 8: Email/Job Alert Ingestion

- [ ] Plan email ingestion.
- [ ] Allow manual import of email alert text.
- [ ] Future Gmail/IMAP integration if approved.
- [ ] No credential storage until secure design exists.
- [ ] Commit and push.

## Phase 9: Platform Integrations

- [ ] SEEK official/approved integration research and adapter placeholder.
- [ ] LinkedIn official/approved integration research and adapter placeholder.
- [ ] Indeed official/approved integration research and adapter placeholder.
- [ ] Employer career page adapter where permitted.
- [ ] No prohibited scraping.
- [ ] Commit and push.

## Phase 10: SSO Integration

- [ ] Integrate with a self-hosted SSO provider later.
- [ ] OIDC login.
- [ ] Local auth fallback.
- [ ] Admin user.
- [ ] User roles.
- [ ] Commit and push.

## Phase 11: AI-Assisted Applications and CV Generation

- [ ] Integrate with local AI service later.
- [ ] Generate cover letter drafts.
- [ ] Generate CV tailoring notes.
- [ ] Generate public CV summaries.
- [ ] Generate SEO profile descriptions.
- [ ] Summarise job descriptions.
- [ ] Compare job with candidate profile.
- [ ] Never submit or publish without approval.
- [ ] Commit and push.

## Phase 12: Guarded Auto-Apply Future

- [ ] Auto-apply disabled by default.
- [ ] Only allowed sources.
- [ ] Approval queue.
- [ ] Audit logging.
- [ ] User can pause/resume.
- [ ] User can set currently looking for job.
- [ ] Strict matching threshold.
- [ ] No deceptive answers.
- [ ] No prohibited automation.
- [ ] Commit and push.

## Phase 13: Advanced CV Outputs

- [ ] PDF generation.
- [ ] DOCX generation.
- [ ] ATS-friendly text version.
- [ ] Role-targeted CV variants.
- [ ] AI-assisted CV improvement.
- [ ] SEO-friendly public bio generation.
- [ ] Commit and push.

## Phase 14: Reporting and Job-Search Dashboard

- [ ] Application volume.
- [ ] Match quality.
- [ ] Response rate.
- [ ] Interview rate.
- [ ] Company pipeline.
- [ ] Follow-up reminders.
- [ ] Export CSV/PDF.
- [ ] Commit and push.

## Phase 15: Hardening and Production Readiness

- [ ] Backups.
- [ ] Restore test.
- [ ] Security review.
- [ ] SSO review.
- [ ] Audit review.
- [ ] Error monitoring.
- [ ] Version pinning.
- [ ] Commit and push.
