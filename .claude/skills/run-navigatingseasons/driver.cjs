// REPL driver for navigatingseasons (static HTML/CSS/JS site, no build step).
// Launches a local static file server + headless Chromium, then exposes a
// REPL of commands so an agent can navigate/click/screenshot the live pages.
// CommonJS on purpose: Playwright is a global install resolved via
// NODE_PATH, which only works for require(), not ESM import - see SKILL.md.
const { chromium } = require('playwright');
const { spawn } = require('node:child_process');
const readline = require('node:readline');
const fs = require('node:fs');
const path = require('node:path');

const UNIT_DIR = path.resolve(__dirname, '../../..');
const PORT = process.env.NS_PORT || '8900';
const BASE_URL = `http://localhost:${PORT}`;
const SHOT_DIR = process.env.SCREENSHOT_DIR || '/tmp/shots';
fs.mkdirSync(SHOT_DIR, { recursive: true });

let server = null;
let browser = null;
let page = null;

async function waitForServer(url, timeoutMs = 10000) {
  const start = Date.now();
  while (Date.now() - start < timeoutMs) {
    try {
      const res = await fetch(url);
      if (res.ok || res.status === 404) return true;
    } catch {}
    await new Promise(r => setTimeout(r, 200));
  }
  return false;
}

const COMMANDS = {
  async launch() {
    if (browser) return console.log('already launched');
    server = spawn('python3', ['-m', 'http.server', PORT, '--directory', UNIT_DIR], {
      stdio: 'ignore',
    });
    const up = await waitForServer(BASE_URL + '/index.html');
    if (!up) return console.log('ERROR: static server did not come up on', BASE_URL);

    browser = await chromium.launch({
      executablePath: process.env.PW_CHROMIUM || '/opt/pw-browsers/chromium',
      headless: false,
      args: ['--headless=new'],
    });
    page = await browser.newPage({ viewport: { width: 1200, height: 900 } });
    // This sandbox's network policy blocks Google Fonts; Chromium takes
    // ~12s to hard-fail that connection, and since the <link rel="stylesheet">
    // is parser-blocking, EVERY navigation (goto/reload) stalls that long
    // waiting on it. Abort it at the route level so navigation is instant -
    // this only affects font loading (falls back to the CSS font stack),
    // not layout or any other behavior.
    await page.route('**://fonts.googleapis.com/**', route => route.abort());
    await page.route('**://fonts.gstatic.com/**', route => route.abort());
    page.on('console', m => { if (m.type() === 'error') console.log('[console error]', m.text()); });
    page.on('pageerror', e => console.log('[page error]', e.message));
    await page.goto(BASE_URL + '/index.html', { waitUntil: 'domcontentloaded' });
    console.log('launched. serving', UNIT_DIR, 'at', BASE_URL);
  },

  async nav(pathName) {
    if (!page) return console.log('ERROR: launch first');
    const url = BASE_URL + '/' + (pathName || 'index.html').replace(/^\//, '');
    await page.goto(url, { waitUntil: 'domcontentloaded' });
    console.log('nav ->', url);
  },

  async ss(name) {
    if (!page) return console.log('ERROR: launch first');
    const f = path.join(SHOT_DIR, (name || `ss-${Date.now()}`) + '.png');
    await page.screenshot({ path: f, fullPage: true });
    console.log('screenshot:', f);
  },

  async viewport(spec) {
    if (!page) return console.log('ERROR: launch first');
    const [w, h] = (spec || '1200x900').split('x').map(Number);
    await page.setViewportSize({ width: w, height: h });
    console.log('viewport ->', w, 'x', h);
  },

  async click(sel) {
    if (!page) return console.log('ERROR: launch first');
    try { await page.click(sel, { timeout: 5000 }); console.log('click', sel, '-> OK'); }
    catch (e) { console.log('click', sel, '-> ERROR:', e.message.split('\n')[0]); }
  },

  async 'click-text'(text) {
    if (!page) return console.log('ERROR: launch first');
    const r = await page.evaluate(t => {
      const els = [...document.querySelectorAll('a, button, [role="button"]')];
      const el = els.find(e => e.textContent?.trim() === t) ?? els.find(e => e.textContent?.includes(t));
      if (!el) return 'NOT_FOUND';
      el.click(); return 'OK: ' + el.tagName;
    }, text);
    console.log('click-text', JSON.stringify(text), '->', r);
  },

  async fill(sel, ...rest) {
    if (!page) return console.log('ERROR: launch first');
    const value = rest.join(' ');
    try { await page.fill(sel, value); console.log('fill', sel, '->', JSON.stringify(value)); }
    catch (e) { console.log('fill', sel, '-> ERROR:', e.message.split('\n')[0]); }
  },

  async wait(sel) {
    if (!page) return console.log('ERROR: launch first');
    try { await page.waitForSelector(sel, { timeout: 10000 }); console.log('found:', sel); }
    catch { console.log('TIMEOUT:', sel); }
  },

  async eval(expr) {
    if (!page) return console.log('ERROR: launch first');
    try { console.log(JSON.stringify(await page.evaluate(expr))); }
    catch (e) { console.log('ERROR:', e.message); }
  },

  async text(sel) {
    if (!page) return console.log('ERROR: launch first');
    console.log(await page.evaluate(
      s => (s ? document.querySelector(s) : document.body)?.innerText ?? '(null)',
      sel || null));
  },

  // --- project-specific: this site's actual interactive surface ---

  // Dark/light toggle lives at #theme-toggle; icon+label are CSS/JS driven
  // off html[data-theme]. Useful for visually diffing both themes.
  async theme(which) {
    if (!page) return console.log('ERROR: launch first');
    if (which === 'dark' || which === 'light') {
      await page.evaluate(t => localStorage.setItem('ns-theme', t), which);
      await page.reload({ waitUntil: 'domcontentloaded' });
      console.log('theme ->', which, '(reloaded)');
    } else {
      const cur = await page.evaluate(() => document.documentElement.getAttribute('data-theme'));
      console.log('current theme:', cur, '(pass "dark" or "light" to set)');
    }
  },

  // Mobile nav collapses behind #nav-toggle under 760px viewport width.
  async 'menu-toggle'() {
    if (!page) return console.log('ERROR: launch first');
    const r = await page.evaluate(() => {
      const btn = document.getElementById('nav-toggle');
      if (!btn) return 'NOT_FOUND (viewport may be >=760px wide, or page has no nav)';
      btn.click();
      return 'expanded=' + btn.getAttribute('aria-expanded');
    });
    console.log('menu-toggle ->', r);
  },

  // The contact form (contact.html) posts to FormSubmit - this fills it
  // without submitting, so a screenshot can confirm layout/validation
  // without actually sending an email.
  async 'fill-contact-form'() {
    if (!page) return console.log('ERROR: launch first');
    if (!page.url().includes('contact.html')) await COMMANDS.nav('contact.html');
    await page.fill('#first-name', 'Test');
    await page.fill('#last-name', 'User');
    await page.fill('#email', 'test@example.com');
    await page.fill('#phone', '07000000000');
    await page.fill('#subject', 'Smoke test');
    await page.fill('#message', 'Driver smoke test - not a real enquiry.');
    console.log('fill-contact-form -> OK (not submitted)');
  },

  async quit() {
    if (browser) await browser.close().catch(() => {});
    if (server) server.kill();
    browser = null; page = null; server = null;
  },
  help() { console.log('commands:', Object.keys(COMMANDS).join(', ')); },
};

const stdin = fs.createReadStream(null, { fd: fs.openSync('/dev/stdin', 'r') });
const rl = readline.createInterface({ input: stdin, output: process.stdout, prompt: 'driver> ' });

rl.on('line', async line => {
  const [cmd, ...rest] = line.trim().split(/\s+/);
  if (!cmd) return rl.prompt();
  const fn = COMMANDS[cmd];
  if (!fn) { console.log('unknown:', cmd, '- try: help'); return rl.prompt(); }
  try { await fn(...rest); } catch (e) { console.log('ERROR:', e.message); }
  if (cmd === 'quit') { rl.close(); process.exit(0); }
  rl.prompt();
});
rl.on('close', async () => { await COMMANDS.quit(); process.exit(0); });

console.log('navigatingseasons driver - "help" for commands, "launch" to start');
rl.prompt();
