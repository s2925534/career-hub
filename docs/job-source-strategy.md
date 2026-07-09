# Job Source Strategy

How Career Hub finds out about jobs, phased from "always safe" to "future, gated on official
access". See [`docs/compliance-and-platform-rules.md`](compliance-and-platform-rules.md) for the
hard rules behind every item here.

## Always-Safe Sources (MVP)

1. **Manual job entry** — you type in title, company, URL, description yourself.
2. **Pasted job descriptions** — copy-paste text from a posting you're viewing.
3. **Saved job URLs** — store a link for reference; no crawling/scraping of the target site.
4. **Email job alerts** — manually paste the text of an alert email you received (Phase 8);
   no mailbox access is required for this path.
5. **RSS feeds where available** — a publisher's own RSS feed, fetched as the publisher intends.
6. **Official APIs where available** — any platform that publishes a job-search API for this
   purpose.

## Permitted-With-Care Sources (later phases)

7. **Employer career pages where permitted** — respecting `robots.txt` and terms of service;
   low-volume, user-initiated fetches only, never bulk crawling.
8. **Recruitment agency feeds where permitted** — same standard as #7.

## Gated Future Integrations (Phase 9, official/approved access only)

9. **Future SEEK integration** — only through an official or explicitly approved API/partner
   access. Until such access exists, this stays a documented adapter placeholder, not working
   code.
10. **Future LinkedIn integration** — same standard as #9.
11. **Future Indeed integration** — same standard as #9.

## Explicitly Out of Scope, Always

12. **No prohibited scraping** of any platform whose terms disallow it.
13. **No logged-in scraping** — automating actions inside an authenticated session on a platform
    that hasn't explicitly permitted it.
14. **No CAPTCHA bypass** under any circumstance.
15. **No fake accounts** on any platform, ever.

## Why This Order

Sources 1–6 require no automation against a third party at all, or use a channel the source
publishes specifically for programmatic consumption — there is no compliance risk. Sources 7–8
require care but are common, permitted patterns. Sources 9–11 are the ones users most want, but
also the ones most likely to violate a platform's terms if built without official cooperation —
so they are deliberately deferred until that cooperation exists, and shipped only as
placeholders/documentation until then. See
[`docs/architecture.md`](architecture.md) §7 for the adapter pattern these will follow, and
[`docs/future-flags.md`](future-flags.md) for the flags that gate each one.
