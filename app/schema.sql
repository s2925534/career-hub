-- Career Hub schema.
--
-- career_profile, resume_versions, public_cv_versions, contact_messages,
-- seo_metadata (used read-only for optional per-page overrides, no admin UI
-- yet), and audit_log are still intentionally minimal placeholder tables (id,
-- timestamps, and a flexible JSON `data` column where applicable) -- they
-- belong to later phases (7) and haven't been designed yet. See
-- docs/phase-plan.md.
--
-- candidate_profile, preferences, and skills were promoted to fully modeled
-- columns in Phase 2, per docs/profile-and-preferences.md. jobs was promoted
-- in Phase 3, applications in Phase 5 (both per docs/application-workflow.md),
-- and public_profile/work_experiences/projects in Phase 6, per
-- docs/public-cv-site.md.
--
-- NOTE: this project has no migration tooling yet (pre-1.0, no real user data).
-- If you have a local SQLite file from before Phase 2, delete it and let
-- init_db() recreate it rather than trying to migrate in place.

CREATE TABLE IF NOT EXISTS career_profile (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    data TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL DEFAULT (datetime('now')),
    updated_at TEXT NOT NULL DEFAULT (datetime('now'))
);

-- Singleton (id=1, seeded by init_db()) -- Career Hub is single-user for the MVP.
CREATE TABLE IF NOT EXISTS candidate_profile (
    id INTEGER PRIMARY KEY CHECK (id = 1),
    name TEXT NOT NULL DEFAULT '',
    location TEXT NOT NULL DEFAULT '',
    work_rights TEXT NOT NULL DEFAULT '',
    currently_looking TEXT NOT NULL DEFAULT 'not_looking', -- looking | open | not_looking
    availability_start_date TEXT NOT NULL DEFAULT '',
    visa_details TEXT NOT NULL DEFAULT '',
    references_available TEXT NOT NULL DEFAULT 'unspecified', -- yes | no | unspecified
    portfolio_links TEXT NOT NULL DEFAULT '',
    github_link TEXT NOT NULL DEFAULT '',
    linkedin_link TEXT NOT NULL DEFAULT '',
    personal_site_link TEXT NOT NULL DEFAULT '',
    created_at TEXT NOT NULL DEFAULT (datetime('now')),
    updated_at TEXT NOT NULL DEFAULT (datetime('now'))
);

-- Singleton (id=1, seeded by init_db()), like candidate_profile/preferences --
-- deliberately a separate table from candidate_profile so private-only fields
-- (work rights, visa details, target salary, ...) can never leak onto the
-- public CV site by accident. See docs/public-cv-site.md.
CREATE TABLE IF NOT EXISTS public_profile (
    id INTEGER PRIMARY KEY CHECK (id = 1),
    public_name TEXT NOT NULL DEFAULT '',
    headline TEXT NOT NULL DEFAULT '',
    summary TEXT NOT NULL DEFAULT '',
    region TEXT NOT NULL DEFAULT '',
    contact_method TEXT NOT NULL DEFAULT '',
    github_link TEXT NOT NULL DEFAULT '',
    linkedin_link TEXT NOT NULL DEFAULT '',
    portfolio_links TEXT NOT NULL DEFAULT '',
    created_at TEXT NOT NULL DEFAULT (datetime('now')),
    updated_at TEXT NOT NULL DEFAULT (datetime('now'))
);

-- Singleton (id=1, seeded by init_db()) -- the JobPreference model used by the
-- future rule-based matching engine (Phase 4).
CREATE TABLE IF NOT EXISTS preferences (
    id INTEGER PRIMARY KEY CHECK (id = 1),
    target_role_titles TEXT NOT NULL DEFAULT '',
    target_seniority TEXT NOT NULL DEFAULT '',
    target_salary_min INTEGER,
    target_salary_max INTEGER,
    minimum_salary INTEGER,
    preferred_locations TEXT NOT NULL DEFAULT '',
    work_mode TEXT NOT NULL DEFAULT 'any', -- remote | hybrid | onsite | any
    industries TEXT NOT NULL DEFAULT '',
    preferred_companies TEXT NOT NULL DEFAULT '',
    excluded_companies TEXT NOT NULL DEFAULT '',
    required_technologies TEXT NOT NULL DEFAULT '',
    preferred_technologies TEXT NOT NULL DEFAULT '',
    excluded_technologies TEXT NOT NULL DEFAULT '',
    max_commute_minutes INTEGER,
    created_at TEXT NOT NULL DEFAULT (datetime('now')),
    updated_at TEXT NOT NULL DEFAULT (datetime('now'))
);

-- visibility: private | public_cv | applications_only | both | archived --
-- see docs/profile-and-preferences.md ("Public/Private Visibility Rules").
CREATE TABLE IF NOT EXISTS work_experiences (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    company TEXT NOT NULL DEFAULT '',
    title TEXT NOT NULL DEFAULT '',
    location TEXT NOT NULL DEFAULT '',
    employment_type TEXT NOT NULL DEFAULT '',
    start_date TEXT NOT NULL DEFAULT '',
    end_date TEXT NOT NULL DEFAULT '',
    summary TEXT NOT NULL DEFAULT '',
    technologies TEXT NOT NULL DEFAULT '',
    visibility TEXT NOT NULL DEFAULT 'private',
    created_at TEXT NOT NULL DEFAULT (datetime('now')),
    updated_at TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS skills (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    category TEXT NOT NULL DEFAULT '',
    -- private | public_cv | applications_only | both | archived -- see
    -- docs/profile-and-preferences.md "Public/Private Visibility Rules".
    visibility TEXT NOT NULL DEFAULT 'private',
    created_at TEXT NOT NULL DEFAULT (datetime('now')),
    updated_at TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS projects (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL DEFAULT '',
    description TEXT NOT NULL DEFAULT '',
    url TEXT NOT NULL DEFAULT '',
    technologies TEXT NOT NULL DEFAULT '',
    visibility TEXT NOT NULL DEFAULT 'private',
    created_at TEXT NOT NULL DEFAULT (datetime('now')),
    updated_at TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS resume_versions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    version_type TEXT NOT NULL DEFAULT 'draft',
    data TEXT NOT NULL DEFAULT '{}',
    is_live INTEGER NOT NULL DEFAULT 0,
    created_at TEXT NOT NULL DEFAULT (datetime('now')),
    updated_at TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS public_cv_versions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    data TEXT NOT NULL DEFAULT '{}',
    is_live INTEGER NOT NULL DEFAULT 0,
    published_at TEXT,
    created_at TEXT NOT NULL DEFAULT (datetime('now')),
    updated_at TEXT NOT NULL DEFAULT (datetime('now'))
);

-- source: manual | pasted | url. status: see docs/application-workflow.md
-- ("Application Statuses") -- interested | drafting | ready_to_apply | applied |
-- interview | offer | rejected | archived.
CREATE TABLE IF NOT EXISTS jobs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL DEFAULT '',
    company TEXT NOT NULL DEFAULT '',
    location TEXT NOT NULL DEFAULT '',
    url TEXT NOT NULL DEFAULT '',
    description TEXT NOT NULL DEFAULT '',
    source TEXT NOT NULL DEFAULT 'manual',
    status TEXT NOT NULL DEFAULT 'interested',
    notes TEXT NOT NULL DEFAULT '',
    follow_up_date TEXT,
    created_at TEXT NOT NULL DEFAULT (datetime('now')),
    updated_at TEXT NOT NULL DEFAULT (datetime('now'))
);

-- outcome: pending | interview | offer | rejected | withdrawn. One row per job
-- for the MVP (upserted by job_id when the user records a manual apply) --
-- see docs/application-workflow.md. follow_up_date here is a post-application
-- reminder, distinct from jobs.follow_up_date which covers pre-application
-- reminders (e.g. "check back on this listing").
CREATE TABLE IF NOT EXISTS applications (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    job_id INTEGER NOT NULL REFERENCES jobs(id),
    application_date TEXT,
    application_url TEXT NOT NULL DEFAULT '',
    contact_person TEXT NOT NULL DEFAULT '',
    outcome TEXT NOT NULL DEFAULT 'pending',
    notes TEXT NOT NULL DEFAULT '',
    follow_up_date TEXT,
    created_at TEXT NOT NULL DEFAULT (datetime('now')),
    updated_at TEXT NOT NULL DEFAULT (datetime('now'))
);

-- kind: cv | cover_letter | other. Uploaded via /profile (Phase 2 placeholder --
-- full template/version management lands in Phase 7, see docs/resume-versioning.md).
CREATE TABLE IF NOT EXISTS documents (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    kind TEXT NOT NULL DEFAULT 'other',
    original_filename TEXT NOT NULL DEFAULT '',
    file_path TEXT NOT NULL,
    visibility TEXT NOT NULL DEFAULT 'private',
    created_at TEXT NOT NULL DEFAULT (datetime('now')),
    updated_at TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS contact_messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    email TEXT,
    message TEXT,
    created_at TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS seo_metadata (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    page_path TEXT NOT NULL UNIQUE,
    title TEXT,
    description TEXT,
    created_at TEXT NOT NULL DEFAULT (datetime('now')),
    updated_at TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS audit_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    event_type TEXT NOT NULL,
    detail TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL DEFAULT (datetime('now'))
);
