# Navigating Seasons — site rebuild

Rebuild of navigatingseasons.co.uk (Frances Palmer-Thompson's BACP-accredited
counselling practice), migrated off Carrd onto plain HTML/CSS/JS for GitHub
Pages. This repo is private, under Simone's (the son's) GitHub account, for
now — see "Still open" below for the plan to hand it to Fran.

## What's here

```
index.html
assets/
  main.css           original Carrd stylesheet, unchanged
  dark-mode.css       dark theme, scoped under html[data-theme="dark"]
  enhancements.css    skip-link, theme-toggle button, focus-visible, reduced-motion
  site.js             theme toggle + hash-based section routing (replaces Carrd's main.js)
  noscript.css        original, unchanged
  images/             image01.png (Fran's photo) through image06.png
```

## Fixed since the Carrd export

- Footer copyright year: removed dead `<unloaded-script>` blocks, gave all
  10 footer instances a shared `.footer-dynamic-line` class updated once by
  `site.js` (the original used a duplicated `id`, which `getElementById`
  can't handle).
- Several `mailto:` links and one FAQ link pointed at `navigatingseasons.com`
  instead of `.co.uk`.
- `main.js` (Carrd's own runtime) wasn't part of the export — replaced with
  `site.js`, a small custom script handling section show/hide by URL hash,
  including a `#supervision` alias that scrolls to the Clinical Supervision
  callout nested inside Services and Fees.
- Added `:focus-visible` outlines site-wide (the original only styled focus
  for form fields — this site serves a counsellor who is registered blind
  and clients who may also have visual impairments, so this matters more
  than usual).
- Added `prefers-reduced-motion` handling.
- Added a skip-to-content link (`#site-main`), matching the pattern used on
  flownarrate.com: absolutely positioned off-screen, first focusable element
  in the body, visible on focus.

## Dark mode

`main.css` has no CSS custom properties — every color is a literal hex code.
Rather than edit the 7600-line file in place, every color declaration was
extracted with a real CSS parser (`tinycss2`) and mapped into
`dark-mode.css`, scoped under `html[data-theme="dark"]`.

| Token | Light | Dark |
|---|---|---|
| Page background | `#6C7C59` | `#171D14` |
| Primary text | `#151515` | `#EDEAE0` |
| Secondary text | `#474747` | `#B7B29F` |
| Muted text | `#B3B3B3` | `#A8AD9A` |
| Borders | `#F3F2ED` | `#4A5540` |
| Card overlay | `rgba(255,255,255,.129)` | `rgba(0,0,0,.38)` |
| Solid callout card | `rgba(255,255,255,.898)` | `rgba(15,18,13,.94)` |
| Accent | `#1CCBD6` | unchanged |

The cream "Free 25 Minute Discovery Call" button is left unchanged in dark
mode on purpose — it's self-contained and works on any background, and
keeping it bright gives the page one confident, unmissable accent.

Toggle defaults to the visitor's OS `prefers-color-scheme`, remembers an
override in `localStorage` (`ns-theme`), and applies before first paint to
avoid a flash of the wrong theme.

## Still open

1. **`assets/images/card.jpg`** — referenced only in the page's JSON-LD
   schema (`//navigatingseasons.co.uk/assets/images/card.jpg`), used for
   social/schema previews. Not part of any export. Needs supplying.
2. **Contact form** — still `action="#"`. Needs a Formspree (or similar)
   endpoint before it can send anything; Carrd's own form backend doesn't
   survive export.
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
