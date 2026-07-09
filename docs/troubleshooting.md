# Troubleshooting

Common problems and how to approach them. This grows as real issues are found; treat it as a
living document.

## Cannot reach the app

- Confirm the container is running: `docker compose ps`.
- Confirm `CAREER_HUB_BIND_HOST` and `CAREER_HUB_HTTP_PORT` match what you're trying to reach —
  `0.0.0.0` binds all interfaces, `127.0.0.1` only the local machine.
- If reaching it through a deployer-managed hostname, confirm the deployer's tunnel/reverse
  proxy is actually routing to this container/port — that's outside this repo's control, see
  [`docs/deployer-integration.md`](deployer-integration.md).

## Database not created

- Confirm `CAREER_HUB_BASE_PATH/database` exists and is writable — run
  `scripts/create-folders.sh` if unsure.
- Confirm `DATABASE_URL` points at a path under `CAREER_HUB_BASE_PATH` that the container can
  write to (matching volume mount in `docker-compose.yml`).

## Permission issues on `CAREER_HUB_BASE_PATH`

- The container process needs read/write access to every folder under `CAREER_HUB_BASE_PATH`.
  On Linux/NAS hosts, check ownership matches the UID/GID the container runs as.
- Never work around this with `chmod -R 777`; fix ownership instead.

## Port already in use

- Change `CAREER_HUB_HTTP_PORT` in `.env` and restart, or find and stop whatever else is bound
  to that port (`lsof -i :PORT` on macOS/Linux).

## `.env` not loaded

- Confirm a `.env` file (copied from `.env.example`) actually exists next to `docker-compose.yml`
  — Compose only auto-loads a file literally named `.env` in the same directory.
- Scripts under `scripts/` also expect `.env` in the repo root; check for a warning about a
  missing `.env` in their output.

## Deployer integration issues

- Confirm the deployer is pointed at this repo's actual `docker-compose.yml` and `.env`, not a
  scaffolded copy.
- Confirm the port and health-check path passed to the deployer match `CAREER_HUB_HTTP_PORT` and
  `/health`. See [`docs/deployer-integration.md`](deployer-integration.md).

## Public domain not routing

- This is almost always a deployer-side DNS/Cloudflare/tunnel configuration issue, not something
  fixable inside this repo — see [`docs/deployer-integration.md`](deployer-integration.md).
- Confirm `CAREER_HUB_PUBLIC_CV_EXTERNAL_URL` matches the actual public hostname so generated
  links/canonicals are correct once routing does work.

## Private/public domain mixed up

- Confirm `CAREER_HUB_PRIVATE_DOMAIN` and `CAREER_HUB_PUBLIC_CV_DOMAIN` are set to different
  values and match what the deployer is actually routing to each hostname.
- If both hostnames render the same content, check the `Host`-header-based routing logic in the
  app — see [`docs/architecture.md`](architecture.md) §1.

## Login problems

- MVP uses local auth; confirm `ENABLE_LOCAL_AUTH=true` and that you're using the admin
  credentials set up during bootstrap.
- If SSO is enabled later and login loops or fails, check `SSO_ISSUER_URL` reachability and
  clock skew between the app and the identity provider (OIDC tokens are time-sensitive).

## File upload problems

- Confirm the relevant `uploads/` subfolder exists and is writable (see
  [`docs/deployer-integration.md`](deployer-integration.md) for the full folder list).
- Check for a reverse-proxy body-size limit if uploads fail only through the deployer-managed
  hostname but work when hitting the container directly.

## Job parsing problems

- Job description parsing from pasted text is best-effort; if fields aren't extracted correctly,
  fill them in manually — this is expected in the MVP, not a bug to chase down. No AI-based
  parsing exists yet (see [`docs/ai-integration-future.md`](ai-integration-future.md)).

## Matching score seems wrong

- The matching engine is rule-based and explainable (Phase 4) — check the "reason for
  match"/"reason for rejection" output first; it should point at exactly which preference
  drove the score.
- Confirm your `JobPreference` data (target titles, required/excluded technologies, salary
  range) is actually filled in as expected.

## Public CV not updating

- Confirm you actually **published** the draft — editing profile data alone never updates the
  live public site; see [`docs/resume-versioning.md`](resume-versioning.md).
- Check the audit log for the most recent publish event.

## Resume version rollback

- Rollback re-flags a previous version as live; it does not delete any version. If a rollback
  doesn't seem to have taken effect, confirm you rolled back the right target (public vs.
  application-default version are tracked independently).

## Auto-apply disabled or blocked

- This is expected until Phase 12 ships — `ENABLE_AUTO_APPLY=false` by default and no MVP
  code path submits applications automatically. See
  [`docs/auto-apply-guardrails.md`](auto-apply-guardrails.md) for exactly what has to be true
  before it can ever run.
