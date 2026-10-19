# Navigating Seasons — website

Frances Palmer-Thompson's BACP-accredited counselling practice.

**Live at:** https://navigatingseasons.co.uk

## Structure

```
index.html                Home
about.html                About Me
how-i-can-help.html       Areas of work
how-i-work.html           Therapeutic approach
services-and-fees.html    Pricing, cancellation policy, supervision summary
clinical-supervision.html Clinical supervision: approach, fees, FAQs
qualifications.html       Accreditations and training
articles.html             Articles: the Navigating Counselling series
navigating-counselling-autumn-2026.html   Autumn 2026 article
crisis-support.html       24/7 crisis contacts
privacy-policy.html       UK GDPR privacy policy
contact.html              Contact form + FAQ
thank-you.html            Form submission landing page
404.html                  Custom "page not found" page
assets/
  site.css                All styling: tokens, type, layout, components
  site.js                 Theme toggle, footer year, mobile menu, dated seasonal notices
  images/
CNAME                     Custom domain config for GitHub Pages
robots.txt, sitemap.xml   Search engine crawl rules and page list
llms.txt                  Plain-text summary of the practice for AI tools
CLAUDE.md                 Standing instructions for Claude Code sessions
scripts/
  check_site.py           Checks sitemap/llms.txt/structured data (--fix updates sitemap dates)
  seasonal_reminders.py   Opens seasonal reminder issues from .github/seasonal-calendar.json
.github/workflows/        Runs the two scripts above on GitHub
```

Static HTML/CSS, no build step, no framework. Hosted on GitHub Pages.

## Design system

Typefaces: **Lora** (headings), **Karla** (body), **IBM Plex Mono** (small
labels), via Google Fonts. All colors are CSS custom properties in
`assets/site.css`, redefined under `html[data-theme="dark"]`. The site opens
in the visitor's device preference (`prefers-color-scheme`, light if unset),
with a toggle that remembers the visitor's choice. The inline theme script in
each page's `<head>` is allowlisted by SHA-256 hash in the CSP — if you edit
that script, recompute the hash and update it on every page.

## Accessibility

Contrast checked against WCAG AA, visible focus states throughout, skip-to-
content link, real semantic HTML and heading structure, alt text on every
image, `prefers-reduced-motion` respected. This is a standing requirement
for this site, not a one-off pass — keep it in mind for any future edit.

## Contact form

Submits via [FormSubmit](https://formsubmit.co) (free, no signup) to
info@navigatingseasons.co.uk, with a honeypot field, a spam-keyword
blacklist, and an auto-reply to the sender. Disclosed on the Privacy
Policy page, since FormSubmit is a third-party processor.

## Editing this site

See **`HANDOVER.md`** — written for Fran, and readable by a Claude Code
session for making content edits without touching code directly.

## Working notes

Crisis contacts, accreditation numbers, fees, and privacy policy wording
are factual content, not up for stylistic editing — verify before changing.

"Navigating Seasons" is a UK registered trademark (IPO), so the footer reads
"© year Navigating Seasons®": © for the site's copyright, ® for the name.
Keep both.
