# Navigating Seasons — website

Frances Palmer-Thompson's BACP-accredited counselling practice.

**Live at:** https://navigatingseasons.co.uk

## Structure

```
index.html                Home
about.html                About Me
how-i-can-help.html       Specialisms
how-i-work.html           Therapeutic approach
services-and-fees.html    Pricing, cancellation policy, clinical supervision
qualifications.html       Accreditations and training
crisis-support.html       24/7 crisis contacts
privacy-policy.html       UK GDPR privacy policy
contact.html              Contact form + FAQ
thank-you.html            Form submission landing page
404.html                  Custom "page not found" page
assets/
  site.css                All styling: tokens, type, layout, components
  site.js                 Theme toggle + footer year
  images/
CNAME                     Custom domain config for GitHub Pages
```

Static HTML/CSS, no build step, no framework. Hosted on GitHub Pages.

## Design system

Typefaces: **Lora** (headings), **Karla** (body), **IBM Plex Mono** (small
labels), via Google Fonts. All colors are CSS custom properties in
`assets/site.css`, redefined under `html[data-theme="dark"]` — dark mode is
the default, with a toggle that remembers the visitor's choice.

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
