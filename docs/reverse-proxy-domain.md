# Reverse Proxy and Domain Routing

Career Hub is a two-hostname application: one private, authenticated hostname for career
administration, and one public hostname for the SEO-friendly CV site. This document describes
the routing model and what a reverse proxy in front of Career Hub must preserve. It does **not**
implement any of this routing itself — see [`docs/deployer-integration.md`](deployer-integration.md).

## Generic Hostname Concept

- **Private hostname** (`CAREER_HUB_PRIVATE_DOMAIN`, generic example `jobs.example.com`):
  authenticated career admin — profile, preferences, jobs, applications, resume versions.
- **Public CV hostname** (`CAREER_HUB_PUBLIC_CV_DOMAIN`, generic example `cv.example.com`):
  public, unauthenticated, SEO-friendly CV/resume/profile site.

## Personal Examples

- Personal private hostname example: `jobs.veloso.dev`
- Personal public CV hostname example: `cv.veloso.dev`

These are one maintainer's own deployment choice. Alternative hostnames considered but not used
as defaults: `careers.veloso.dev`, `apply.veloso.dev`, `jobhunt.veloso.dev` (private);
`resume.veloso.dev`, `profile.veloso.dev`, `pedro.veloso.dev` (public). Anyone deploying this
project should pick their own.

## Intended Routing

```
https://jobs.example.com  ──▶  Career Hub container (private/admin route group, authenticated)
https://cv.example.com    ──▶  Career Hub container (public route group, unauthenticated)
```

Both hostnames may point at the same container/port in the MVP; the app distinguishes them by
the incoming `Host` header and serves the matching route group. See
[`docs/architecture.md`](architecture.md) §1.

## Domain Handling Belongs to the Deployer

DNS records, Cloudflare configuration, tunnels, and certificates for both hostnames are entirely
the deployer's responsibility. This repo does not implement Cloudflare automation, does not
request certificates, and does not manage DNS.

## Reverse Proxy Requirements

Whatever reverse proxy sits in front of Career Hub (Cloudflare Tunnel, Traefik, Nginx Proxy
Manager, etc., all deployer-managed) must:

- Preserve the original `Host` header (or forward it via `X-Forwarded-Host`) so Career Hub can
  tell the two hostnames apart.
- Preserve `X-Forwarded-Proto` so generated links use `https://` correctly.
- Not strip or rewrite the request path — Career Hub expects clean, unprefixed paths on both
  hostnames.
- Terminate TLS in front of Career Hub; the app itself serves plain HTTP.

## Future SSO Headers

When `ENABLE_SSO_AUTH` lands, Career Hub will validate OIDC tokens itself rather than trusting
any proxy-injected identity header, so no special proxy-side auth-header configuration is
required for SSO to work correctly — see
[`docs/sso-integration-future.md`](sso-integration-future.md). This will be documented further
once that phase is implemented.

## Private Routes Must Never Be Public

Regardless of reverse proxy configuration, the app itself must refuse to serve private/admin
routes when the request's effective hostname is the public CV domain. This is enforced at the
application routing layer, not solely by reverse-proxy configuration, so a deployer
misconfiguration cannot accidentally expose private data.
