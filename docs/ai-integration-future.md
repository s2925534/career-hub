# AI Integration (Future)

Career Hub's MVP ships with **no AI integration** (`ENABLE_AI_ASSIST=false`,
`AI_PROVIDER=none`). This document plans how AI assistance will be added later, and the rules it
must follow when it is.

## Intended Integration

A configurable AI backend (`AI_PROVIDER`, `AI_BASE_URL`) — most likely a local
Ollama-compatible endpoint (e.g. `ai.example.com`, `ENABLE_LOCAL_AI_PROVIDER`) so career data
never has to leave the user's own infrastructure, though the design should not preclude a
different provider if a user chooses one.

## Planned AI-Assisted Features (Phase 11)

1. **Job description summarization** — condense a long posting into key points.
2. **Match explanation** — turn the rule-based match score (Phase 4) into readable prose,
   without changing the underlying score or its inputs.
3. **Cover letter drafting** — draft a cover letter from the job details and the user's stored
   profile/templates.
4. **CV tailoring notes** — suggest which stored experience/skills to emphasize for a given job.
5. **Public CV wording** — suggest phrasing for the public profile summary/bio.
6. **SEO bio generation** — draft short/long public bios optimized for readability and SEO.
7. **Screening answer drafting** — draft answers to screening questions, always sourced from
   stored, truthful profile data.

## Hard Rules

- **Human review required.** Every AI-generated artifact (cover letter, tailoring note, public
  bio, SEO copy, screening answer draft) is a draft. None of it is submitted to an application
  or published to the public CV site without explicit human approval — the same approval gates
  described in [`docs/application-workflow.md`](application-workflow.md) and
  [`docs/resume-versioning.md`](resume-versioning.md) apply identically to AI-generated and
  human-written drafts.
- **No hallucinated qualifications.** AI drafting is constrained to the user's own stored profile
  data (experience, skills, achievements). It must not invent qualifications, experience,
  employers, dates, or skills that aren't already present in the structured profile. Prompts
  supplied to the AI backend should include only the user's real stored data as source material.
- **No AI in the critical path of submission or publication.** AI assistance only ever produces
  drafts for the existing approval-gated workflows; it never gains a separate, ungated path to
  submit an application or publish a page.
- **Matching stays rule-based first.** AI-assisted job matching (`ENABLE_AI_JOB_MATCHING`) is
  explicitly a later addition on top of the rule-based engine (Phase 4), not a replacement for
  it — see [`docs/decision-log.md`](decision-log.md) and
  [`docs/phase-plan.md`](phase-plan.md) Phase 4.

## Data Handling

Since career and application data is sensitive (see [`docs/security.md`](security.md)), the
preferred AI integration path is a **local** model endpoint under the user's own control, so
prompts containing profile data don't need to leave their infrastructure. Any future
non-local AI provider option must be opt-in and clearly documented as sending data off-box.
