# Navigating Seasons — site rebuild

Rebuild of navigatingseasons.co.uk (Frances Palmer-Thompson's BACP-accredited
counselling practice), migrated off Carrd onto a hand-built multi-page site
for GitHub Pages. This repo is private, under Simone's (the son's) GitHub
account, for now — see "Still open" below for the plan to hand it to Fran.

## What's here

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
assets/
  site.css                All styling: tokens, type, layout, components
  site.js                 Theme toggle + footer year
  images/                 image01.png (Fran's photo) through image06.png
```

This used to be a single `index.html` built from a Carrd export, with every
"page" a hidden/shown `<section>` behind hash routing (`#aboutme`,
`#contact`, ...) and Carrd's generated `container-component`/`text-component
instance-N` class soup. It's now a real multi-page site — separate HTML
files, real `<nav>` links, no hash routing, no page-builder markup. Nothing
about the switch changed any factual content (fees, accreditation numbers,
crisis contacts, privacy policy wording); it only changed structure and
visual design.

## Design system

Typefaces: **Lora** (headings, serif), **Karla** (body, sans), **IBM Plex
Mono** (small kicker labels), all via Google Fonts.

| Token | Light | Dark |
|---|---|---|
| Background | `#F7F4EC` | `#171D14` |
| Panel / card | `#FFFFFF` | `#1E2618` |
| Panel tint (callouts) | `#FBF3E7` | `#232C1C` |
| Ink (text) | `#211F1A` | `#F0EDE6` |
| Ink, soft | `#5C5850` | `#ABA89C` |
| Accent | `#A85B1E` | `#E0A458` |
| Accent, strong | `#8B4A17` | `#F0BC7A` |
| Focus ring (accessibility only) | `#1CCBD6` | `#1CCBD6` |

All tokens are CSS custom properties in `assets/site.css`, redefined under
`html[data-theme="dark"]`. Everything else (buttons, cards, nav, tables,
forms) is built from those tokens rather than hardcoded colors, so a palette
change is a token edit, not a hunt through the file.

Earlier drafts used an olive-tinted grey (`#2E3324`) as the main text color,
which read as muddy rather than a clean near-black — fixed to a true
neutral (`#211F1A`). A CSS specificity bug also briefly made every button's
text render the same color as its own background (invisible) in dark mode
only, caused by an overly-specific `html[data-theme="dark"] a` selector
beating component-level color rules; removed in favor of letting the
already-theme-aware `--accent`/`--accent-strong` variables do that work.

Dark mode is the default (not tied to OS preference); the toggle remembers
an override in `localStorage` (`ns-theme`) and applies via an inline
`<head>` script before first paint, so there's no flash of the wrong theme.

## Accessibility

- Skip-to-content link, first focusable element on every page.
- `:focus-visible` outlines (cyan, reserved for that purpose only) on every
  interactive element.
- `prefers-reduced-motion` respected.
- Real `<nav>`, `<main>`, heading hierarchy, and `aria-current="page"` on
  the active nav link — no more content only distinguished by CSS opacity
  (the previous single-page version hid inactive sections with
  `opacity: 0` alone, which still left them in the accessibility tree —
  the entire reason to move to real pages instead of JS-toggled sections).
- Crisis-support content is a full page, linked from every page's footer.

## Still open

1. **`assets/images/card.jpg`** — referenced only in the homepage's JSON-LD
   schema, used for social/schema previews. Not part of any export. Needs
   supplying.
2. **Contact form** — still `action="#"` (see the `TODO` comment in
   `contact.html`). Needs a Formspree (or similar) endpoint before it can
   send anything; Carrd's own form backend doesn't survive export.
3. **Ownership handoff** — plan is to move this to Fran's own GitHub
   account, made public (required for free GitHub Pages), once it's ready
   to go live. DNS: point navigatingseasons.co.uk at GitHub's four A
   records plus a `www` CNAME.
4. **Claude MCP connector for Fran** — no native GitHub connector in
   claude.ai yet; needs a custom MCP connector (e.g. the official GitHub MCP
   server) authenticated with a fine-grained PAT scoped to this repo, so she
   can edit content by talking to Claude rather than through GitHub's UI.

## Working notes

- This is a live client site for a practising counsellor — crisis contacts,
  fees, accreditation numbers, and privacy policy wording are factual
  content, not up for stylistic editing.
- Fran is registered blind — prioritize real accessibility (contrast, focus
  states, semantic HTML, no reliance on color alone) over visual polish.
