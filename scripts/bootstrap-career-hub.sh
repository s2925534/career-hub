#!/usr/bin/env bash
# Bootstraps a local/LAN deployment: creates folders, then starts Docker Compose.
#
# Safe by design:
#   - Never deletes anything.
#   - Reminds you that public internet exposure is deployer-managed, not this script's job.
#
# Usage: scripts/bootstrap-career-hub.sh

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "${REPO_ROOT}"

if [ ! -f ".env" ]; then
  echo "WARNING: .env not found. Copying .env.example to .env with placeholder values." >&2
  cp .env.example .env
  echo "Edit .env before relying on this for anything beyond local testing (especially APP_SECRET_KEY)." >&2
fi

set -a
# shellcheck disable=SC1091
source ".env"
set +a

echo "==> Creating persistent folders"
"${REPO_ROOT}/scripts/create-folders.sh"

echo "==> Starting Docker Compose"
docker compose up -d --build

CAREER_HUB_HTTP_PORT="${CAREER_HUB_HTTP_PORT:-8088}"
HEALTH_URL="http://localhost:${CAREER_HUB_HTTP_PORT}/health"

echo "==> Waiting for the web app to become healthy"
attempts=0
max_attempts=30
until curl -fsS "${HEALTH_URL}" >/dev/null 2>&1; do
  attempts=$((attempts + 1))
  if [ "${attempts}" -ge "${max_attempts}" ]; then
    echo "Timed out waiting for ${HEALTH_URL}. Check 'docker compose logs career-hub'." >&2
    exit 1
  fi
  sleep 1
done

echo ""
echo "Career Hub is up."
echo "Local access:      http://localhost:${CAREER_HUB_HTTP_PORT}/"
echo "Health check:      ${HEALTH_URL}"
echo ""
echo "Reminder: public internet exposure (DNS, Cloudflare, tunnels, certs, reverse proxy) is"
echo "handled by an external deployer (e.g. ../synology-site-deployer), not by this script."
echo "See docs/deployer-integration.md."
