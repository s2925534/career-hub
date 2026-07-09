# Future Flags

Full catalog of feature flags — current and future — that gate Career Hub's capabilities. Flags
default to the safest/most conservative value; enabling most of these is a deliberate,
documented decision, not an accident of upgrading. See [`.env.example`](../.env.example) for the
subset already wired into Phase 1, and the relevant doc for each flag's full rationale.

| Flag | Purpose |
|---|---|
| `ENABLE_DEPLOYER_DOMAIN_MANAGEMENT` | Allow an external deployer to manage DNS, Cloudflare, tunnel, reverse proxy, certs, and hostname exposure. |
| `ENABLE_PUBLIC_JOBS_DOMAIN` | Expose the private jobs app through a deployer-managed private career domain. |
| `ENABLE_PUBLIC_CV_SITE` | Expose the public SEO-friendly CV/resume website through a deployer-managed public CV domain. |
| `ENABLE_PUBLIC_PRIVATE_PROFILE_SPLIT` | Keep private job-search/application data separate from public CV/profile data. |
| `ENABLE_PUBLIC_CV_SEO` | Add SEO metadata, Open Graph tags, structured data, sitemap, robots.txt, canonical URLs, and clean public pages. |
| `ENABLE_REVIEW_BEFORE_PUBLICATION` | Require review and approval before publishing changes to the public CV site. |
| `ENABLE_CV_VERSIONING` | Track CV/resume versions: public, application, draft, role-targeted, and archived. |
| `ENABLE_AUTO_RESUME_UPDATE_ON_NEW_JOB` | When a new job/role is added, update the structured profile and generate an updated CV draft. |
| `ENABLE_CV_PDF_EXPORT` | Generate a downloadable public PDF resume. |
| `ENABLE_CV_DOCX_EXPORT` | Generate a downloadable DOCX resume. |
| `ENABLE_ATS_RESUME_EXPORT` | Generate an ATS-friendly resume text or PDF. |
| `ENABLE_ROLE_TARGETED_RESUME` | Generate tailored resume versions for specific target roles. |
| `ENABLE_CONTACT_FORM` | Allow visitors to contact the user through the public CV site, with spam protection and private storage. |
| `ENABLE_PUBLIC_PROJECT_PORTFOLIO` | Show selected public projects on the public CV site. |
| `ENABLE_RESEARCH_PROFILE` | Show selected research/academic material on the public CV site. |
| `ENABLE_SCHEMA_ORG_PERSON` | Add structured Person/ProfilePage schema for discoverability. |
| `ENABLE_SSO_AUTH` | Use an external/self-hosted SSO identity provider. |
| `ENABLE_LOCAL_AUTH` | Use local login for MVP. |
| `ENABLE_AI_ASSISTED_APPLICATIONS` | Use AI to summarize jobs, explain matches, draft cover letters, and prepare CV tailoring notes. |
| `ENABLE_LOCAL_AI_PROVIDER` | Integrate with a local AI or Ollama-compatible endpoint. |
| `ENABLE_AI_ASSISTED_CV_GENERATION` | Use AI to draft resume updates, public profile wording, SEO bios, and role-targeted resume variants, always requiring review. |
| `ENABLE_EMAIL_ALERT_INGESTION` | Import job alerts from email with user approval. |
| `ENABLE_GMAIL_INGESTION` | Future Gmail ingestion, only once credentials and scopes are handled securely. |
| `ENABLE_PLATFORM_API_INTEGRATIONS` | Use official or approved APIs for job platforms. |
| `ENABLE_SEEK_INTEGRATION` | Future SEEK integration, only through official or approved access. |
| `ENABLE_LINKEDIN_JOBS_INTEGRATION` | Future LinkedIn integration, only through official or approved access. |
| `ENABLE_INDEED_INTEGRATION` | Future Indeed integration, only through official or approved access. |
| `ENABLE_EMPLOYER_CAREER_PAGE_IMPORT` | Import direct employer career page jobs where permitted. |
| `ENABLE_JOB_MATCHING_RULES` | Rule-based matching engine. |
| `ENABLE_AI_JOB_MATCHING` | AI-assisted matching, layered on top of the rule-based engine. |
| `ENABLE_APPLICATION_QUEUE` | Queue jobs that are ready for user review. |
| `ENABLE_AUTO_APPLY` | Future guarded auto-apply, disabled by default. |
| `ENABLE_AUTO_APPLY_APPROVAL_REQUIRED` | Require approval before submission. |
| `ENABLE_AUTO_APPLY_ALLOWED_SOURCES` | Only allow auto-apply for approved sources. |
| `ENABLE_AUTO_APPLY_AUDIT_LOG` | Log all application actions. |
| `ENABLE_AUTO_APPLY_KILL_SWITCH` | Allow immediate pause/disable of all auto-apply actions. |
| `ENABLE_PORTABLE_LOCAL_MODE` | Allow Career Hub to run locally on any computer for testing, without being tied to the NAS. |
| `ENABLE_POSTGRES_PRODUCTION_DB` | Upgrade from SQLite to PostgreSQL if needed. |
| `ENABLE_REPORTING_DASHBOARD` | Track application count, response rate, interviews, offers, follow-ups, and public CV visits if analytics are added. |
| `ENABLE_EXPORTS` | Export applications, resume versions, and reports to CSV/PDF. |
| `ENABLE_BACKUP_AUTOMATION` | Automate backups of database, uploads, templates, generated CVs, exports, and audit logs. |

Flags actually wired into Phase 1's `.env.example` (a smaller, MVP-relevant subset of the above,
using slightly different names where the MVP concept is narrower than the future flag) are
listed in [`.env.example`](../.env.example) — see `ENABLE_LOCAL_AUTH`, `ENABLE_SSO_AUTH`,
`ENABLE_PUBLIC_CV_SITE`, `ENABLE_PUBLIC_CV_SEO`, `ENABLE_AI_ASSIST`, `ENABLE_EMAIL_INGESTION`,
`ENABLE_PLATFORM_API_INTEGRATIONS`, and the `ENABLE_AUTO_APPLY*`/`AUTO_APPLY_*` group.
