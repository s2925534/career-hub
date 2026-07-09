#!/usr/bin/env bash
# Checks that the local Career Hub deployment is healthy. Read-only: never
# starts, stops, or modifies anything.
#
# Usage: scripts/health-check.sh

set -uo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "${REPO_ROOT}"

pass=0
fail=0

check() {
  local description="$1"
  local status="$2" # 0 = pass, non-zero = fail
  if [ "${status}" -eq 0 ]; then
    echo "  [PASS] ${description}"
    pass=$((pass + 1))
  else
    echo "  [FAIL] ${description}"
    fail=$((fail + 1))
  fi
}

warn() {
  echo "  [WARN] $1"
}

echo "== Career Hub health check =="

if [ ! -f ".env" ]; then
  warn ".env not found (using defaults / .env.example values only)"
else
  set -a
  # shellcheck disable=SC1091
  source ".env"
  set +a
fi

# Docker
docker info >/dev/null 2>&1
check "Docker is available and running" $?

# Docker Compose
docker compose version >/dev/null 2>&1
check "Docker Compose is available" $?

# Web app container
container_status="$(docker compose ps --status running --services 2>/dev/null | grep -x "career-hub")"
[ -n "${container_status}" ]
check "career-hub container is running" $?

# Health endpoint
CAREER_HUB_HTTP_PORT="${CAREER_HUB_HTTP_PORT:-8088}"
curl -fsS "http://localhost:${CAREER_HUB_HTTP_PORT}/health" >/dev/null 2>&1
check "GET /health responds on port ${CAREER_HUB_HTTP_PORT}" $?

# Required folders
CAREER_HUB_BASE_PATH="${CAREER_HUB_BASE_PATH:-./data/career-hub}"
[ -d "${CAREER_HUB_BASE_PATH}/database" ]
check "database folder exists under ${CAREER_HUB_BASE_PATH}" $?

echo ""
echo "== Summary: ${pass} passed, ${fail} failed =="
if [ "${fail}" -gt 0 ]; then
  exit 1
fi
