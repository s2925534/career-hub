#!/usr/bin/env bash
# Creates a timestamped, non-destructive backup of Career Hub's persistent data.
#
# Safe by design:
#   - Never deletes or overwrites existing backups.
#   - Never modifies the source data it backs up (read-only copy).
#
# Usage: scripts/backup-career-hub.sh

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "${REPO_ROOT}"

if [ -f ".env" ]; then
  set -a
  # shellcheck disable=SC1091
  source ".env"
  set +a
fi

CAREER_HUB_BASE_PATH="${CAREER_HUB_BASE_PATH:-}"

if [ -z "${CAREER_HUB_BASE_PATH}" ]; then
  echo "ERROR: CAREER_HUB_BASE_PATH is empty. Refusing to back up." >&2
  exit 1
fi

CAREER_HUB_BASE_PATH="${CAREER_HUB_BASE_PATH%/}"
timestamp="$(date +%Y%m%d-%H%M%S)"
backup_dir="${CAREER_HUB_BASE_PATH}/backups/${timestamp}"

mkdir -p "${backup_dir}"

sources=(
  "database"
  "uploads"
  "templates"
  "generated/resumes"
  "public/cv"
  "exports"
  "audit"
)

echo "Backing up to ${backup_dir}"
for source in "${sources[@]}"; do
  src_path="${CAREER_HUB_BASE_PATH}/${source}"
  if [ -d "${src_path}" ]; then
    dest_path="${backup_dir}/${source}"
    mkdir -p "$(dirname "${dest_path}")"
    cp -R "${src_path}" "${dest_path}"
    echo "  copied: ${source}"
  else
    echo "  skipped (missing): ${source}"
  fi
done

echo "Done. Backup stored at: ${backup_dir}"
echo "See scripts/restore-notes.md for how to restore from a backup."
