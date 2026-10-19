# antislop audit 001: follow-up (19 October 2026)

Simone asked for all findings to be fixed. Below is what changed, and what
still needs input from Simone or Fran.

## Fixed

1. **Dark-mode label on the green band.** It's white in both themes now
   (5.24:1, was 1.92:1).
2. **Footer credit.** Removed the fade (6.44:1 in light mode, was 3.63:1).
3. **Form boxes.** New `--field-border` colour on form fields only: at least
   3.55:1 against the form and the field in both themes (was 1.32:1 and
   1.47:1).
4. **® changed to ©** in the footer on all 14 pages.
5. **Long dashes removed** from all page text:
   - The 39 page titles (tab, Google, social cards) now use "|".
   - The FormSubmit note under the contact form and the matching sentence in
     the privacy policy now use a full stop. The wording is otherwise the
     same.
   - The autoreply email now signs off "Fran" instead of "— Fran".
6. **Tap targets.** Every button, menu link, form field and footer link is at
   least 44px tall now: the menu button, Light/Dark, Contact, the brand link
   and the underlined text links. The text links use an invisible tap area, so
   they look the same.
7. **Top menu.** On wide screens (over 1180px), the links sit on one row under
   the name, with Contact and Light/Dark at the right; the header is 155px,
   down from about 185px. At 1180px and below, the menu button is used, so
   tablets and small laptops no longer get three ragged rows.
9. **Arrows** removed from all 11 underlined links (index, about, 404).
10. **Shadows.** Cards, list items, notices and the supervision box are flat
    now, with a thin edge. Only the contact form keeps its shadow, to mark it
    as the place to act. The drop shadow on Fran's photo is gone too.
11. **Section labels.**
    - They're typed in normal case now, and the style turns them into
      capitals, so screen readers read words. They look the same.
    - Cut the two that repeated their page heading ("ABOUT ME" above "About
      Fran", "ARTICLES" above "Articles").
    - The two hero badges are in normal case, with a thin edge so they stand
      out from the background.
12. **🤎 heart: kept.** It isn't decoration. `HANDOVER.md` documents a heart
    for each season (🤎 💙 🩷 💛) as part of the series design, and Fran
    signs the article "Fran 🤎". It's hidden from screen readers and the
    season is always written in words, so it passes.

## Still needs Simone or Fran

8. **`DESIGN.md`.** antislop won't let Claude invent the site's design
   direction. Answer a few questions (the feel of the site, the colours and
   fonts and why, the mood), and Claude will write your answers into
   `DESIGN.md`.
13. **Home page section shape.** Making the sections less alike is a design
    choice, and it should follow `DESIGN.md`. Left as it is for now.
14. **The green blob behind Fran's photo.** Kept, with its shadow removed.
    Its reason (for example, an organic seasonal motif) should be written in
    `DESIGN.md` in your words.

## How it was checked

- All 14 pages at 360, 390, 600, 820, 1024, 1180, 1181, 1280, 1440 and 1920
  pixels wide. No sideways scrolling, and no control shorter than 44px.
- Light/Dark toggle switches both ways and updates its label.
- The menu opens, closes with Escape, and its links navigate (checked at
  1024px).
- An empty contact form is stopped by the browser with "Please fill out this
  field".
- Tab order follows the page: skip link, name, menu links, Contact,
  Light/Dark, then the page content.
- No script errors on any page.
- `python3 scripts/check_site.py --fix` passes.
