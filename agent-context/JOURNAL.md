# career-hub: session journal

Curated, newest-first record of what each session or notable commit did,
and why. Committed in-repo so it travels with a clone: a checkout on any
machine, or a remote Claude session working from GitHub, gets the working
context without anyone's local `~/.claude` state.

This is the curated half of a two-tier journal. The verbatim half,
`agent-context/journal-verbatim/VERBATIM_INDEX.md`, is gitignored: the
tracked `.githooks/post-commit` hook appends one row per commit (hash,
subject, time, newest local transcript) and prints a reminder to add an
entry here.

Each entry: what changed, why, and what a future session should know before
touching the same area. Use judgement; record decisions, milestones and
gotchas, not every mechanical commit.

See also `agent-context/COORDINATION.md` for open notes between local and
remote sessions.

---

## 2026-10-04: fastapi and starlette security upgrade

Bumped fastapi 0.115.6 to 0.142.2 and added an explicit pin for starlette
1.7.0 (previously pulled in transitively at 0.41.3). pip-audit reported 7
starlette advisories (14 rows), the newest fixed only in starlette 1.3.1, so
the 1.x major was required; fastapi 0.115.x caps starlette below 0.42.
Starlette is now pinned directly so the fix cannot silently regress through
fastapi's open-ended `starlette>=0.46.0` range. The app already used the
`lifespan` handler and the request-first `TemplateResponse(request, name,
ctx)` signature, so no code changes were needed. Verified with an end to end
smoke run (every GET and POST route, file upload, publish flow, host-based
404 guard) against uvicorn before and after: status codes, redirects and
normalised response bodies were identical. There is no automated test suite
yet.

## 2026-10-03: journal set up

Added this journal, the verbatim-index hook (`.githooks/post-commit`) and
the agent working context pointer in `CLAUDE.md`. Earlier history lives
only in `git log`; when a past decision becomes relevant, summarise it here.
