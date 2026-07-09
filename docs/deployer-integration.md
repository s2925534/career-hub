# Deployer Integration

Career Hub is a **standalone** repository. It does not depend on any specific deployment
automation tool to run — `docker compose up` is always sufficient on its own. This document
describes how it is designed to integrate with an external NAS deployer, using this maintainer's
own [`../synology-site-deployer`](../../synology-site-deployer) as the reference integration.

## Division of Responsibility

| Concern | Owned by |
|---|---|
| DNS records | Deployer |
| Cloudflare configuration | Deployer |
| Cloudflare Tunnel | Deployer |
| TLS certificates | Deployer |
| Reverse proxy / hostname routing | Deployer |
| Final NAS deployment path | Deployer |
| Docker Compose file for the app | **This repo** |
| Environment variables | **This repo** |
| Ports and routes | **This repo** |
| Application documentation | **This repo** |

This repo never implements Cloudflare automation, DNS management, tunnel setup, or certificate
handling. It provides everything a deployer needs to run and route to it, and nothing more.

## Reference Deployer: `../synology-site-deployer`

The maintainer's existing deployer project supports a `deploy` command specifically for
**existing** projects that already own their Compose file (as opposed to its `create` command,
which scaffolds new apps). From that project's own docs: `deploy` uploads an existing project's
Compose file (+ optional `.env`) and starts it, working with either a fixed reverse-proxy port
(no port allocation/Cloudflare/health-check) or a standalone published port (port allocation +
health check + Cloudflare routing, same as `create`).

This is exactly the integration path Career Hub is built for:

```
synology-site deploy jobs.example.com \
  --compose-file docker-compose.yml \
  --env-file .env \
  --port "$CAREER_HUB_HTTP_PORT" \
  --health-path /health
```

(Command shape illustrative — see the deployer's own README for exact current flags.)

## What This Repo Provides

- `docker-compose.yml` — the Career Hub web app service, reading all configuration from `.env`.
- `.env.example` — every variable the app and its Compose file need, with safe placeholders.
- A `/health` endpoint for the deployer's health checks.
- Documentation of expected ports, routes, and hostnames (this doc and
  [`docs/reverse-proxy-domain.md`](reverse-proxy-domain.md)).

## Personal Hostname Examples

- Personal private hostname example: `jobs.veloso.dev`
- Personal public CV hostname example: `cv.veloso.dev`

These are this maintainer's own deployment choice, set via `CAREER_HUB_PRIVATE_DOMAIN` and
`CAREER_HUB_PUBLIC_CV_DOMAIN` in their own untracked `.env`. Anyone else deploying Career Hub
should use their own hostnames.

## Expected Internal Service

A single service, the Career Hub web app, listening on `CAREER_HUB_BIND_HOST:CAREER_HUB_HTTP_PORT`
inside the container/on the host network as configured by Compose. There is no separate database
service to expose for MVP (SQLite is a file, not a network service).

## What Must Never Be Exposed

- The SQLite database file, or any file under `${CAREER_HUB_BASE_PATH}`, must never be served
  directly over HTTP or otherwise made reachable from outside the container.
- Synology DSM must never be exposed through this project.
- SSH must never be exposed through this project.
- Only the single web app HTTP endpoint should ever be routed to by the deployer.

## Future SSO Note

When SSO lands (`ENABLE_SSO_AUTH`), the identity provider is expected to be a separate,
independently deployed service (e.g. `auth.example.com`), also fronted by the same deployer.
Career Hub validates OIDC tokens against that provider directly; the deployer's job remains
limited to routing hostnames, not brokering identity.

## How To Consume This Repo From a Deployer

1. Clone/pull this repo to wherever the deployer builds/reads Compose files from.
2. Copy `.env.example` to `.env` and fill in real values (domains, external URLs, a generated
   `APP_SECRET_KEY`, and `CAREER_HUB_BASE_PATH` pointed at the deployer's chosen persistent path).
3. Run `scripts/create-folders.sh` (or let the deployer run it) to create the persistent folder
   layout under `CAREER_HUB_BASE_PATH`.
4. Point the deployer's `deploy`-style command at this repo's `docker-compose.yml` and `.env`,
   passing the chosen port and `/health` as the health check path.
5. Let the deployer own DNS/Cloudflare/tunnel/certificate/reverse-proxy configuration for the
   two hostnames.
