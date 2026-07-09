#!/usr/bin/env bash
# Creates the persistent folder layout under CAREER_HUB_BASE_PATH.
#
# Safe by design:
#   - Never deletes anything.
#   - Refuses to run with an empty CAREER_HUB_BASE_PATH.
#   - Never assumes a Synology volume path (/volume1, etc).
#   - Idempotent: safe to re-run any time.
#
# See docs/deployer-integration.md for the full folder list this mirrors.

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

# Load .env if present, without overriding already-exported variables.
if [ -f "${REPO_ROOT}/.env" ]; then
  set -a
  # shellcheck disable=SC1091
  source "${REPO_ROOT}/.env"
  set +a
fi

CAREER_HUB_BASE_PATH="${CAREER_HUB_BASE_PATH:-}"

if [ -z "${CAREER_HUB_BASE_PATH}" ]; then
  echo "ERROR: CAREER_HUB_BASE_PATH is empty. Refusing to create folders." >&2
  echo "Set it in .env or export it before running this script." >&2
  exit 1
fi

echo "Using CAREER_HUB_BASE_PATH=${CAREER_HUB_BASE_PATH}"

folders=(
  "database"
  "uploads"
  "uploads/cv"
  "uploads/cover-letters"
  "uploads/job-descriptions"
  "uploads/profile-assets"
  "uploads/public-cv-assets"
  "generated"
  "generated/resumes"
  "generated/public-cv"
  "generated/seo"
  "exports"
  "exports/applications"
  "exports/reports"
  "exports/resumes"
  "backups"
  "logs"
  "templates"
  "templates/cover-letters"
  "templates/screening-answers"
  "templates/resumes"
  "templates/public-cv"
  "job-sources"
  "job-sources/imports"
  "job-sources/email-alerts"
  "audit"
  "public"
  "public/cv"
  "public/sitemap"
)

for folder in "${folders[@]}"; do
  target="${CAREER_HUB_BASE_PATH%/}/${folder}"
  if [ -d "${target}" ]; then
    echo "  exists:  ${folder}"
  else
    mkdir -p "${target}"
    echo "  created: ${folder}"
  fi
done

echo "Done. Folder layout is ready under ${CAREER_HUB_BASE_PATH}"
