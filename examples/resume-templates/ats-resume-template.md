# Example: ATS-Friendly Resume Template (Future, Phase 13)

A planning example of the plain-text/simple-formatting structure an ATS-friendly export
(`ENABLE_ATS_RESUME_EXPORT`) would follow — no tables, columns, images, or graphics, just linear
text with clear section headers, so applicant-tracking systems can parse it reliably.

```
{{candidate_name}}
{{location}} | {{contact_method}} | {{portfolio_link}} | {{linkedin_link}} | {{github_link}}

SUMMARY
{{professional_summary}}

SKILLS
{{skills_comma_separated_list}}

EXPERIENCE
{{work_experience.title}}, {{work_experience.company}} — {{work_experience.location}}
{{work_experience.start_date}} - {{work_experience.end_date_or_"Present"}}
- {{work_experience.achievement_1}}
- {{work_experience.achievement_2}}

EDUCATION
{{education.degree}}, {{education.institution}} — {{education.end_date}}

CERTIFICATIONS
{{certification.name}} — {{certification.issuer}} ({{certification.date}})
```

Not part of the MVP — see Phase 13 in [`docs/phase-plan.md`](../../docs/phase-plan.md) and
[`docs/resume-versioning.md`](../../docs/resume-versioning.md) for scope boundaries.
