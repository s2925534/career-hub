# Example: Screening Answers Template

A planning example of how screening question answers are stored and reused. Answers are always
sourced from stored, truthful profile data — see "Profile Truthfulness Rules" in
[`docs/profile-and-preferences.md`](../../docs/profile-and-preferences.md).

```
Question: Are you legally authorized to work in this country?
Stored answer source: candidate_profile.work_rights
Answer: {{work_rights_statement}}

Question: What is your expected salary?
Stored answer source: candidate_profile.target_salary_range
Answer: {{target_salary_range}} (or: "Negotiable within {{target_salary_range}}")

Question: When can you start?
Stored answer source: candidate_profile.availability_start_date
Answer: {{availability_start_date}}

Question: Do you require visa sponsorship?
Stored answer source: candidate_profile.visa_authorization_details
Answer: {{visa_authorization_details}}
```

If a required question cannot be answered truthfully from stored profile data, Career Hub routes
the application to manual completion rather than guessing or fabricating an answer — this applies
identically to the manual MVP workflow and any future assisted/auto-apply workflow (see
[`docs/auto-apply-guardrails.md`](../../docs/auto-apply-guardrails.md)).
