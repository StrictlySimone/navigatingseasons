# Handover — Navigating Seasons website

This document is for Fran. It explains what the site is, what's already
done, what's still outstanding, and how to make changes yourself using
Claude Code — no coding knowledge needed.

**If you'd rather have this read to you or explained**, open Claude Code in
this folder (or point it at this repository) and say something like:
"Read HANDOVER.md and explain it to me" or "Read HANDOVER.md, then help me
update my fees." Claude Code can read this file directly and act on it.

## What's live right now

The site is finished and published at:

**https://navigatingseasons.co.uk**

You're a collaborator on the GitHub repository, so you (and your own
Claude Code) can push changes directly — no need to go through Simone.

## What's on the site

Ten pages: Home, About Me, How I Can Help, How I Work, Services & Fees,
Qualifications, Crisis Support, Privacy Policy, Contact (with a working
enquiry form and FAQ), and a Thank You page after someone submits the form.
There's also a custom "page not found" page if a link is ever mistyped or
goes out of date.

- **Light and dark mode.** Dark is the default; there's a toggle in the top
  right of every page. It remembers your choice.
- **The contact form works.** It's sent through a free service called
  FormSubmit, straight to info@navigatingseasons.co.uk. Because it's a
  free third-party service, it doesn't offer a data protection agreement
  and holds messages for up to 30 days — this is disclosed on the Privacy
  Policy page. When you reply to an enquiry email from your inbox, it will
  go straight back to the person who wrote in — no extra steps.
- **Accessibility was a priority throughout, not an afterthought.** Every
  page has a skip-to-content link, a visible focus outline on anything you
  can tab to, real heading structure, and color contrast checked against
  WCAG AA (the standard screen readers and low-vision users rely on) —
  actually measured, not eyeballed. Every image has real alt text. Nothing
  on the site is conveyed by color alone.
- **No address is published anywhere on the site** — only a phone number,
  email, a Google Business Profile link, and your LinkedIn.
- **Crisis Support page** has current, correct helpline numbers — Samaritans,
  Shout, NHS 111, Mind Infoline, CALM, The Mix. If any of these numbers or
  services ever change, that page should be updated straight away — it's
  the one part of the site where being current genuinely matters.

## Making changes yourself with Claude Code

You don't need to touch code directly. Talk to Claude Code the way you'd
explain a change to Simone, for example:

- "Change my session fee on the Services & Fees page to £55."
- "Add a paragraph to my About Me page about the CPD course I just finished."
- "Update the Mind Infoline hours on the Crisis Support page."

Claude Code will make the edit, show you what changed, and — once you're
happy — commit and push it, which is what actually publishes it to the
live site (usually within a minute or two).

**Before any change goes live, you can always ask Claude Code to describe
the change in plain words first**, e.g. "tell me what you're about to
change before you do it."

**A few things worth being careful with** — not because Claude Code will
get them wrong, but because they're the parts of the site where an error
would matter most:

- Crisis helpline numbers and hours
- Your BACP/accreditation registration numbers
- The Privacy Policy wording
- Session fees and cancellation policy

For any of these, it's worth double-checking the exact wording (or asking
Simone to sanity-check) before publishing.

## Still outstanding

Just one small thing: **`assets/images/card.jpg`** is referenced for how
the site previews when shared as a link (e.g. in a text message or on
Facebook), but doesn't exist yet. Cosmetic only — the site works fully
without it.

## If something looks broken

Tell Simone, or describe what you're seeing to Claude Code and ask it to
investigate — it can look at the live site and the code side by side.
