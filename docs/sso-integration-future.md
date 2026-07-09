# SSO Integration (Future)

Career Hub's MVP uses simple local authentication (`ENABLE_LOCAL_AUTH=true`,
`ENABLE_SSO_AUTH=false`). This document plans the future SSO integration (Phase 10).

## Intended Integration

OIDC login against a self-hosted identity provider (e.g. `auth.example.com`), toggled by
`ENABLE_SSO_AUTH`, with the relevant issuer/client configuration in `SSO_ISSUER_URL`,
`SSO_CLIENT_ID`, `SSO_CLIENT_SECRET`.

## OIDC Login

Career Hub redirects to the configured issuer for login, then validates the returned ID
token/access token itself against that issuer — it does not trust a reverse-proxy-injected
identity header as a substitute for token validation (see
[`docs/reverse-proxy-domain.md`](reverse-proxy-domain.md)), so a misconfigured proxy can't
silently grant access.

## Local Auth Fallback

`ENABLE_LOCAL_AUTH` and `ENABLE_SSO_AUTH` are independent flags; local auth can remain available
as a fallback (e.g. for the admin account) even after SSO is enabled, or be disabled entirely
once SSO is trusted as the sole login path — this is a deployment-time choice, not a hardcoded
one.

## Admin/User Roles

MVP is single-user (one admin account). SSO integration is the natural point to introduce actual
roles (e.g. admin vs. read-only) if Career Hub ever needs to support more than one person
managing the same instance — not required for the personal-use MVP.

## Session Handling

Sessions are managed by Career Hub itself (signed session cookie, using `APP_SECRET_KEY`),
established after a successful OIDC exchange or local login. Session lifetime and renewal
behavior should be conservative by default (short-lived, explicit re-auth) given the
sensitivity of the data behind it.

## Protecting Private Routes

All private/admin routes (`/profile`, `/preferences`, `/jobs`, `/applications`,
`/resume/versions`, `/seo`, `/dashboard`, etc.) require an authenticated session, whether that
session came from local auth or SSO. This check happens at the application routing layer, not
only via the reverse proxy — see [`docs/reverse-proxy-domain.md`](reverse-proxy-domain.md).

## Public CV Routes Stay Public

The public CV site's routes never require authentication, regardless of SSO configuration —
SSO only ever adds protection to the private side, never removes public accessibility of the CV
site. See [`docs/public-cv-site.md`](public-cv-site.md).
