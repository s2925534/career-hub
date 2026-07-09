# Example: Public Profile Home Page (`/`)

A planning mockup of the public CV site's home page content and SEO surface, combining the
public CV template with the SEO metadata described in
[`docs/seo-strategy.md`](../../docs/seo-strategy.md).

```
<title>Jane Doe — Senior Backend Engineer</title>
<meta name="description" content="Jane Doe is a Senior Backend Engineer specializing in
  distributed systems and developer tooling. Based in Melbourne, Australia.">
<link rel="canonical" href="https://cv.example.com/">
<meta property="og:title" content="Jane Doe — Senior Backend Engineer">
<meta property="og:type" content="profile">
<meta property="og:url" content="https://cv.example.com/">

<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "ProfilePage",
  "mainEntity": {
    "@type": "Person",
    "name": "Jane Doe",
    "jobTitle": "Senior Backend Engineer",
    "url": "https://cv.example.com/",
    "sameAs": [
      "https://github.com/janedoe",
      "https://www.linkedin.com/in/janedoe"
    ]
  }
}
</script>

---
# Jane Doe
### Senior Backend Engineer

Backend engineer with 8 years building distributed systems and internal developer tools.
Currently focused on platform reliability and API design.

📍 Melbourne, Australia   ✉️ hello@janedoe.example
🔗 GitHub · LinkedIn · Portfolio

[View Experience](/experience) · [Skills](/skills) · [Projects](/projects) · [Contact](/contact)
  · [Download CV](/download/cv)
```

This mockup only uses illustrative, fictional data — see
[`docs/public-cv-site.md`](../../docs/public-cv-site.md) for the real field/page model.
