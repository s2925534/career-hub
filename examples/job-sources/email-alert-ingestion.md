# Example: Email Alert Ingestion (Manual Import, Phase 8)

Phase 8 supports manually pasting the text of a job alert email you received — no mailbox
access, no credential storage. This is a planning example, not live data or working code yet.

```
Pasted alert text:
"""
New jobs matching "Backend Engineer, Remote":
1. Senior Backend Engineer — Example Co — Remote (AU) — https://example-co.com/careers/123
2. Platform Engineer — Another Co — Sydney, NSW — https://another-co.com/jobs/456
"""

Result: Career Hub creates draft Job records for each detected posting (title, company,
location, URL best-effort parsed from the pasted text), left in `interested` status for you to
review and complete.
```

Future (not in MVP, and only once a secure credential-storage design exists): optional
Gmail/IMAP ingestion (`ENABLE_GMAIL_INGESTION`) to fetch alert emails automatically, still ending
in the same "draft Job records for review" outcome — never an auto-apply trigger by itself. See
[`docs/job-source-strategy.md`](../../docs/job-source-strategy.md).
