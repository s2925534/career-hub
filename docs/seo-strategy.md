# SEO Strategy

SEO plan for the public CV site only. The private admin app is never indexed and should always
be excluded from search engines (see [`docs/reverse-proxy-domain.md`](reverse-proxy-domain.md)
and [`docs/security.md`](security.md)).

## Page Titles

Each public page has a unique, descriptive `<title>` (e.g. "Jane Doe — Senior Backend Engineer"),
generated from `PublicProfile` and `SeoMetadata` records, not a single site-wide title reused
everywhere.

## Meta Descriptions

Each public page has a unique meta description summarizing that page's content, sourced from
`SeoMetadata`, with a sane default derived from the public professional summary if a page-specific
one isn't set.

## Canonical URLs

Every public page emits a canonical `<link rel="canonical">` pointing at
`CAREER_HUB_PUBLIC_CV_EXTERNAL_URL` plus that page's clean path, so the app never has to guess
its own externally-visible URL from request headers.

## Open Graph

`og:title`, `og:description`, `og:type` (`profile` for the home page), `og:url`, `og:image`
(a public profile photo/avatar if provided).

## Twitter/X Cards

`twitter:card` (`summary` or `summary_large_image`), `twitter:title`, `twitter:description`,
`twitter:image`, mirroring the Open Graph data.

## Schema.org Person

The public profile home page emits `schema.org/Person` structured data (JSON-LD): name,
jobTitle, url, sameAs (GitHub/LinkedIn/portfolio links), and address/region if the user has
chosen to make location public.

## Schema.org ProfilePage

Wraps the `Person` data in a `schema.org/ProfilePage` node where appropriate, per Schema.org
guidance for personal profile pages.

## Sitemap

`/sitemap.xml` lists every public page (home, experience, projects, research if enabled, skills,
contact) with `lastmod` derived from the currently published `PublicCvPageVersion`'s publish date.

## Robots.txt

`/robots.txt` allows all crawling of the public CV hostname's public pages, and — critically —
this file only ever exists on the public CV hostname. The private hostname should not be
discoverable via a permissive robots.txt; it relies on authentication and not being linked
publicly, and a future enhancement may add an explicit `Disallow: /` robots.txt on the private
hostname as defense in depth.

## Clean URLs

No file extensions, no query-string-driven content pages, no session/tracking parameters in
canonical URLs — see the page list in [`docs/public-cv-site.md`](public-cv-site.md).

## Performance

Server-rendered Jinja2 templates keep the public site fast by default (no client-side rendering
required for content to appear); minimize blocking assets, and prefer plain CSS/minimal JS on
public pages so they stay fast even on modest self-hosted hardware.

## Accessibility

Semantic HTML (proper heading hierarchy, `<nav>`, `<main>`, `<article>`), meaningful `alt` text
on any images, sufficient color contrast, and keyboard-navigable interactive elements (the
contact form, once it exists).
