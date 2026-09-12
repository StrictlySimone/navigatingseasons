---
name: run-navigatingseasons
description: Build, run, and drive the navigatingseasons.co.uk static site. Use when asked to start the site, take a screenshot of it, test the theme toggle or mobile menu, fill the contact form, or otherwise interact with its pages.
---

This is a static multi-page HTML/CSS/JS site — no build step, no
framework, no `package.json`. For agent use, drive it via the
Playwright REPL at `.claude/skills/run-navigatingseasons/driver.cjs`,
which starts a local static file server and a headless Chromium
against it.

All commands below assume your shell's current directory is already
the repo root (this is where Claude Code auto-loads this skill from).

## Prerequisites

Chromium and Playwright are already installed in this container:

- Chromium binary: `/opt/pw-browsers/chromium`
- Playwright package: globally installed at `/opt/node22/lib/node_modules/playwright`

The driver is CommonJS (`.cjs`) specifically so it can resolve that
global install via `NODE_PATH` — see Gotchas.

No `npm install` needed; there is nothing to build.

## Run (agent path)

```bash
NODE_PATH=/opt/node22/lib/node_modules node .claude/skills/run-navigatingseasons/driver.cjs
```

Wrap in tmux for interactive use — this is the exact sequence used to
verify the driver:

```bash
tmux new-session -d -s ns -x 200 -y 50
tmux send-keys -t ns 'NODE_PATH=/opt/node22/lib/node_modules node .claude/skills/run-navigatingseasons/driver.cjs' Enter
timeout 15 bash -c 'until tmux capture-pane -t ns -p | grep -q "driver>"; do sleep 0.3; done'
tmux send-keys -t ns 'launch' Enter
timeout 20 bash -c 'until tmux capture-pane -t ns -p | grep -q "launched\."; do sleep 0.2; done'
tmux send-keys -t ns 'ss home' Enter
timeout 5 bash -c 'until tmux capture-pane -t ns -p | grep -q "screenshot:"; do sleep 0.1; done'
tmux capture-pane -t ns -p
```

Screenshots land in `/tmp/shots/` (override with `SCREENSHOT_DIR`). The
static server runs on port 8900 (override with `NS_PORT`).

### Commands

| command | what it does |
|---|---|
| `launch` | start the static server + browser, load the home page |
| `nav <path>` | go to `<path>.html` (e.g. `nav contact.html`) |
| `ss [name]` | full-page screenshot → `/tmp/shots/<name>.png` |
| `viewport <WxH>` | resize viewport, e.g. `viewport 390x800` for mobile |
| `click <css-sel>` | click an element |
| `click-text <text>` | click the link/button containing this text |
| `fill <css-sel> <text>` | fill an input/textarea |
| `wait <css-sel>` | wait up to 10s for an element to appear |
| `eval <js>` | evaluate JS in the page, print the JSON result |
| `text [css-sel]` | print `innerText` of an element (or `body`) |
| `theme` | print the current theme; `theme dark` / `theme light` sets it and reloads |
| `menu-toggle` | click the mobile hamburger nav (only visible under 760px width) |
| `fill-contact-form` | fills every field on `contact.html` with placeholder values, without submitting |
| `quit` | close the browser and stop the static server |

## Run (human path)

```bash
python3 -m http.server 8900
```

Then open `http://localhost:8900/index.html` in a real browser.
Useless in a headless container — this is what the driver does for you.

## Gotchas

- **Google Fonts is blocked by this container's network policy, and
  the failure is slow, not instant.** Every page links
  `fonts.googleapis.com` for Lora/Karla. In this sandbox that request
  gets `ERR_CONNECTION_RESET` after ~12 seconds, and because the
  `<link rel="stylesheet">` tag is parser-blocking, `domcontentloaded`
  (and `load`, and `networkidle`) all stall for that same ~12s on
  *every single navigation* — confirmed by timing `goto`/`reload`
  directly (12.5s each). The driver aborts both
  `fonts.googleapis.com` and `fonts.gstatic.com` at the route level
  before the first navigation, which turns that into an instant
  `ERR_FAILED` instead — navigations dropped from ~12.5s to under
  100ms. This only affects font loading (the CSS fallback stack
  kicks in); it doesn't change layout or behavior. If you write a
  new script against this site instead of using the driver, apply
  the same `page.route(...).abort()` or you'll pay the same 12s tax
  on every `goto`/`reload`.
- **Playwright is CommonJS-only here.** It's a global install
  resolved via `NODE_PATH`, which Node's ESM loader does not honor —
  `import { chromium } from 'playwright'` in a `.mjs` file fails with
  `ERR_MODULE_NOT_FOUND` even with `NODE_PATH` set, while
  `require('playwright')` in `.cjs` resolves fine. That's why the
  driver is `driver.cjs`, not `.mjs`.
- **The mobile hamburger menu (`#nav-toggle`) only exists in the DOM
  as a *visible, clickable* control under a 760px viewport** — the
  CSS media query hides it above that width. `menu-toggle` will
  report `NOT_FOUND` at desktop widths; `viewport 390x800` first.
- **The contact form has grown fields since this driver was written**
  (a "Preferred Contact Method" and "How Did You Hear About Me?"
  dropdown were added by another session mid-way through this repo's
  history). `fill-contact-form` only fills the required text fields;
  the optional selects keep their defaults, which is fine for a
  layout/smoke screenshot but means it won't exercise those dropdowns.
