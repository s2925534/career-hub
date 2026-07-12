-- Career Hub schema.
--
-- career_profile, public_profile, work_experiences, projects, resume_versions,
-- public_cv_versions, jobs, applications, contact_messages, seo_metadata, and
-- audit_log are still intentionally minimal placeholder tables (id, timestamps,
-- and a flexible JSON `data` column) -- they belong to later phases (3, 6, 7)
-- and haven't been designed yet. See docs/phase-plan.md.
--
-- candidate_profile, preferences, and skills were promoted to fully modeled
-- columns in Phase 2, per docs/profile-and-preferences.md.
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

CREATE TABLE IF NOT EXISTS public_profile (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    data TEXT NOT NULL DEFAULT '{}',
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

CREATE TABLE IF NOT EXISTS work_experiences (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    data TEXT NOT NULL DEFAULT '{}',
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
    data TEXT NOT NULL DEFAULT '{}',
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

CREATE TABLE IF NOT EXISTS jobs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT,
    company TEXT,
    url TEXT,
    source TEXT NOT NULL DEFAULT 'manual',
    status TEXT NOT NULL DEFAULT 'interested',
    data TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL DEFAULT (datetime('now')),
    updated_at TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS applications (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    job_id INTEGER REFERENCES jobs(id),
    status TEXT NOT NULL DEFAULT 'interested',
    data TEXT NOT NULL DEFAULT '{}',
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
