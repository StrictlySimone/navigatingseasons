#!/usr/bin/env python3
"""Checks the basics every public page needs. Run from the repo root: python3 scripts/check_head.py

Looks at: title, description, canonical, og/twitter tags, robots, one h1, image alt text,
internal links, the homepage link style, and that sitemap.xml lists every indexable page.
"""
import glob, os, re, sys
from html.parser import HTMLParser
import xml.dom.minidom as minidom

ROOT = os.getcwd()
BASE = "https://" + open("CNAME").read().strip()
REQUIRE_ROBOTS = False  # Fran's pages rely on the default (index); only 404 and thank-you carry noindex
HOME_AS_SLASH = False   # this site links to index.html; its canonical URLs are already correct
SKIP_DIRS = {".git", ".agents", ".claude", "node_modules", "anti-slop"}
problems = []

def bad(page, msg):
    problems.append(f"{page}: {msg}")

class Page(HTMLParser):
    def __init__(self):
        super().__init__()
        self.title = ""; self.in_title = False
        self.meta = {}; self.canonical = None
        self.h1 = 0; self.imgs = []; self.links = []
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "title": self.in_title = True
        elif tag == "meta":
            k = a.get("name") or a.get("property")
            if k: self.meta[k] = a.get("content", "")
        elif tag == "link" and a.get("rel") == "canonical": self.canonical = a.get("href")
        elif tag == "h1": self.h1 += 1
        elif tag == "img": self.imgs.append(a)
        elif tag == "a" and a.get("href"): self.links.append(a["href"])
    def handle_endtag(self, tag):
        if tag == "title": self.in_title = False
    def handle_data(self, d):
        if self.in_title: self.title += d

pages = []
for path in glob.glob("**/*.html", recursive=True):
    if set(path.split(os.sep)) & SKIP_DIRS: continue
    pages.append(path)

try:
    sitemap = minidom.parse("sitemap.xml").toxml()
except Exception as e:
    sitemap = ""; bad("sitemap.xml", f"does not parse: {e}")
if os.path.exists("feed.xml"):
    try: minidom.parse("feed.xml")
    except Exception as e: bad("feed.xml", f"does not parse: {e}")

titles = {}; descs = {}
for path in sorted(pages):
    html = open(path, encoding="utf-8").read()
    p = Page(); p.feed(html)
    robots = p.meta.get("robots", "")
    noindex = "noindex" in robots
    url = BASE + "/" + ("" if path == "index.html" else path)
    if REQUIRE_ROBOTS and not robots: bad(path, "no robots meta tag")
    if not p.title.strip(): bad(path, "no <title>")
    if not p.meta.get("description"): bad(path, "no meta description")
    if noindex:
        if url in sitemap: bad(path, "is noindex but is in sitemap.xml")
    else:
        if p.canonical != url: bad(path, f"canonical is {p.canonical!r}, expected {url!r}")
        if url not in sitemap: bad(path, "missing from sitemap.xml")
        for k in ("og:title", "og:description", "og:url", "og:image", "twitter:title", "twitter:description"):
            if not p.meta.get(k): bad(path, f"missing {k}")
        if p.meta.get("og:url") and p.meta["og:url"] != url: bad(path, f"og:url is {p.meta['og:url']!r}")
        if p.h1 != 1: bad(path, f"{p.h1} <h1> elements, expected 1")
        titles.setdefault(p.title.strip(), []).append(path)
        descs.setdefault(p.meta.get("description", ""), []).append(path)
    for im in p.imgs:
        if "alt" not in im: bad(path, f"image without alt: {im.get('src')}")
    if BASE.startswith("https://www.") and re.search(r"https?://(?!www\.)" + re.escape(BASE[len("https://www."):]), html): bad(path, "uses the bare domain, not www")
    for href in p.links:
        if HOME_AS_SLASH and href in ("index.html", "./index.html", "/index.html"): bad(path, "links to index.html, use /")
        if re.match(r"^([a-z][a-z0-9+.-]*:|#)", href): continue
        target = href.split("#")[0].split("?")[0]
        if not target: continue
        fs = os.path.join(os.path.dirname(path), target) if not target.startswith("/") else target.lstrip("/")
        if target == "/" : continue
        if not os.path.exists(fs) and not os.path.exists(fs + ".html"): bad(path, f"broken link: {href}")
    for im in p.imgs:
        s = im.get("src", "")
        if s and not s.startswith(("http", "data:")):
            fs = os.path.join(os.path.dirname(path), s) if not s.startswith("/") else s.lstrip("/")
            if not os.path.exists(fs): bad(path, f"missing image file: {s}")
for t, ps in titles.items():
    if len(ps) > 1: bad(", ".join(ps), "share the same <title>")
for d, ps in descs.items():
    if len(ps) > 1: bad(", ".join(ps), "share the same description")

if problems:
    print("\n".join(problems)); print(f"\n{len(problems)} problem(s)."); sys.exit(1)
print(f"All checks passed ({len(pages)} pages).")
