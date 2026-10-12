# Notes for Claude Code

Simone and Fran both edit this site with Claude Code. Read `README.md` for
how the site is built and `HANDOVER.md` for how content changes are made
(adding articles in particular). Fran isn't a developer: explain changes in
plain words.

## Before every commit

Run:

```bash
python3 scripts/check_site.py --fix
```

This updates the `<lastmod>` dates in `sitemap.xml` for any page you
changed, and adds new pages to it. It also checks that every public page is
in `llms.txt`, that articles have structured data, and that seasonal
notices have sensible dates. Fix anything it reports, then commit
`sitemap.xml` with the change. The same check runs on GitHub
(`.github/workflows/check-site.yml`) after every push.

## Keep llms.txt in step with the site

`llms.txt` is the summary AI tools (ChatGPT, Claude, Perplexity and others)
read about the practice. When you add a page, add a line for it under
`## Pages`. When a page's purpose, fees, specialisms, availability or
closure dates change, update the matching line or note. Keep it factual
and in the same style.

## New articles

Follow the steps in `HANDOVER.md`, and also:

- Copy the `application/ld+json` Article block from
  `navigating-counselling-autumn-2026.html` into the new page's `<head>`.
  Update `headline`, `description`, `url`, `mainEntityOfPage` and
  `datePublished`/`dateModified` (the day it's published).
  When an article's text is later edited, update its `dateModified`.
- Every article links to `crisis-support.html` if it touches on distress.

## Seasonal notices (Christmas closure and similar)

Time-limited notices are written into the page with `hidden`,
`data-show-from` and `data-show-until` (YYYY-MM-DD, inclusive), for example:

```html
<aside class="crisis-banner seasonal-notice" data-show-from="2026-11-16" data-show-until="2027-01-03" hidden>
	<strong>Christmas and New Year</strong>
	...
</aside>
```

`assets/site.js` shows them only between those dates, so they switch on
and off without anyone editing the page. Don't guess dates: confirm closure
dates with Fran or Simone. When dates change, update every page carrying
the notice (contact, services-and-fees, crisis-support) and the matching
note in `llms.txt`.

## Seasonal reminders

`.github/seasonal-calendar.json` lists the dates the site prepares for
(Bonfire Night, Christmas, the next seasonal article and so on). Every
Monday, `.github/workflows/seasonal-reminders.yml` opens a GitHub issue,
labelled `seasonal-reminder`, for each event coming up, with ideas and a
checklist. If you're asked to work on one, read that issue's checklist.
To add or change an event, edit the JSON (the `_about` field explains the
format), then check the result with
`python3 scripts/seasonal_reminders.py --dry-run --date YYYY-MM-DD`.

Seasonal writing is Fran's voice: draft only when asked, and use her text
as supplied when she gives it. Keep the tone supportive rather than salesy,
and stick to what she actually offers: online and telephone counselling,
ages 16+, UK-wide.

## Facts not to change without checking

Crisis helpline numbers and hours, BACP/accreditation details, fees and the
cancellation policy, and the privacy policy wording (see `README.md`).
