# Example: Public CV Template (Web Page Version)

A planning example of the structure the public CV home page (`/`) renders from a published
`PublicCvPageVersion`. See [`docs/public-cv-site.md`](../../docs/public-cv-site.md) and
[`docs/seo-strategy.md`](../../docs/seo-strategy.md).

```
# {{public_display_name}}
### {{public_headline}}

{{public_professional_summary}}

📍 {{public_location_or_region}}   ✉️ {{public_contact_method}}
🔗 GitHub: {{public_github_link}}   LinkedIn: {{public_linkedin_link}}   Portfolio: {{public_portfolio_links}}

## Experience
- {{work_experience.title}} — {{work_experience.company}} ({{work_experience.start_date}} – {{work_experience.end_date_or_"Present"}})
  {{work_experience.public_summary}}

## Skills
{{public_skills_list}}

## Selected Projects
- {{project.name}} — {{project.public_description}} ({{project.link}})

## Education
- {{education.degree}}, {{education.institution}} ({{education.end_date}})

[Download CV]({{public_downloadable_cv_url}})
```

Only fields whose `VisibilitySetting` includes public visibility ever populate this template —
see "Public/Private Visibility Rules" in
[`docs/profile-and-preferences.md`](../../docs/profile-and-preferences.md).
