#!/usr/bin/env python3
"""Check the site's search-engine and AI-search housekeeping.

Run from the repository root:

    python3 scripts/check_site.py          # check only
    python3 scripts/check_site.py --fix    # also update sitemap.xml dates

It checks that:
  - every public page is listed in sitemap.xml and llms.txt
  - sitemap.xml has no entries for pages that no longer exist
  - each page's <lastmod> in sitemap.xml is at least as recent as the page's
    last change (so Google knows to look at it again)
  - every Navigating Counselling article has Article structured data and a
    card on articles.html
  - all structured data (JSON-LD) is valid JSON
  - seasonal notices have sensible dates, and flags ones that have expired

--fix updates <lastmod> dates and adds missing pages to sitemap.xml. It
can't write llms.txt descriptions for you; it tells you what's missing.

Uses only the Python standard library and git.
"""

import datetime
import json
import re
import subprocess
import sys
from pathlib import Path

SITE = "https://navigatingseasons.co.uk/"
ROOT = Path(__file__).resolve().parent.parent
# Pages that exist but shouldn't be in search results.
NOT_PUBLIC = {"404.html", "thank-you.html"}
ARTICLE_GLOB = "navigating-counselling-*.html"

errors = []
warnings = []


def url_for(page):
    return SITE if page == "index.html" else SITE + page


def last_changed(page):
    """Date the page last changed: today if it has uncommitted edits,
    otherwise the date of the last commit that touched it."""
    today = datetime.date.today().isoformat()
    try:
        dirty = subprocess.run(
            ["git", "status", "--porcelain", "--", page],
            cwd=ROOT, capture_output=True, text=True, check=True,
        ).stdout.strip()
        if dirty:
            return today
        committed = subprocess.run(
            ["git", "log", "-1", "--format=%as", "--", page],
            cwd=ROOT, capture_output=True, text=True, check=True,
        ).stdout.strip()
        return committed or today
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None


def json_ld_blocks(html, page):
    blocks = []
    for raw in re.findall(r'<script type="application/ld\+json">(.*?)</script>', html, re.S):
        try:
            blocks.append(json.loads(raw))
        except json.JSONDecodeError as e:
            errors.append(f"{page}: structured data (JSON-LD) is not valid JSON: {e}")
    return blocks


def main():
    fix = "--fix" in sys.argv[1:]
    today = datetime.date.today().isoformat()

    pages = sorted(p.name for p in ROOT.glob("*.html") if p.name not in NOT_PUBLIC)
    sitemap_path = ROOT / "sitemap.xml"
    sitemap = sitemap_path.read_text(encoding="utf-8")
    llms = (ROOT / "llms.txt").read_text(encoding="utf-8")

    entries = dict(re.findall(r"<loc>(.*?)</loc>\s*<lastmod>(.*?)</lastmod>", sitemap))
    page_urls = {url_for(p): p for p in pages}

    # Sitemap: stale entries, missing pages, out-of-date lastmod.
    for loc in entries:
        if loc not in page_urls:
            errors.append(f"sitemap.xml lists {loc}, but that page doesn't exist. Remove it.")

    new_dates = {}
    for page in pages:
        url = url_for(page)
        changed = last_changed(page)
        if url not in entries:
            msg = f"{page} is missing from sitemap.xml."
            if fix:
                new_dates[url] = changed or today
            else:
                errors.append(msg + " Run: python3 scripts/check_site.py --fix")
            continue
        if changed and entries[url] < changed:
            if fix:
                new_dates[url] = changed
            else:
                errors.append(
                    f"sitemap.xml says {page} last changed {entries[url]}, but it changed on "
                    f"{changed}. Run: python3 scripts/check_site.py --fix"
                )

    if fix and new_dates:
        for url, date in new_dates.items():
            if url in entries:
                sitemap = re.sub(
                    r"(<loc>" + re.escape(url) + r"</loc>\s*<lastmod>)[^<]*(</lastmod>)",
                    r"\g<1>" + date + r"\g<2>",
                    sitemap,
                )
            else:
                block = f"\t<url>\n\t\t<loc>{url}</loc>\n\t\t<lastmod>{date}</lastmod>\n\t</url>\n"
                sitemap = sitemap.replace("</urlset>", block + "</urlset>")
            print(f"fixed: sitemap.xml {url} -> {date}")
        sitemap_path.write_text(sitemap, encoding="utf-8")

    # llms.txt: every public page should be described for AI tools.
    for page in pages:
        if "(" + url_for(page) + ")" not in llms:
            errors.append(
                f"{page} is missing from llms.txt. Add a line under '## Pages' like:\n"
                f"    - [Page title]({url_for(page)}): One sentence on what the page covers."
            )

    # Structured data, articles, and seasonal notices.
    articles_html = (ROOT / "articles.html").read_text(encoding="utf-8")
    for page in pages:
        html = (ROOT / page).read_text(encoding="utf-8")
        blocks = json_ld_blocks(html, page)

        if Path(page).match(ARTICLE_GLOB):
            article = next((b for b in blocks if b.get("@type") in ("Article", "BlogPosting")), None)
            if article is None:
                errors.append(
                    f"{page} has no Article structured data. Copy the JSON-LD block from "
                    f"navigating-counselling-autumn-2026.html and update it for this article."
                )
            else:
                if article.get("url") != url_for(page):
                    errors.append(f"{page}: Article structured data 'url' should be {url_for(page)}")
                for field in ("headline", "datePublished", "author"):
                    if not article.get(field):
                        errors.append(f"{page}: Article structured data is missing '{field}'.")
            if f'href="{page}"' not in articles_html:
                errors.append(f"{page} isn't linked from articles.html. Add a card for it.")

        for start, end in re.findall(r'data-show-from="([^"]*)"\s+data-show-until="([^"]*)"', html):
            if not (re.fullmatch(r"\d{4}-\d{2}-\d{2}", start) and re.fullmatch(r"\d{4}-\d{2}-\d{2}", end)):
                errors.append(f"{page}: seasonal notice dates must be YYYY-MM-DD (got {start} / {end}).")
            elif start > end:
                errors.append(f"{page}: seasonal notice shows from {start} but ends earlier, on {end}.")
            elif end < today:
                warnings.append(
                    f"{page}: a seasonal notice ended on {end} and is now always hidden. "
                    f"Remove it, or update its dates and wording for this year."
                )

    for w in warnings:
        print(f"warning: {w}")
    for e in errors:
        print(f"error: {e}")
    if errors:
        print(f"\n{len(errors)} problem(s) found.")
        return 1
    print("All checks passed." + (f" ({len(warnings)} warning(s))" if warnings else ""))
    return 0


if __name__ == "__main__":
    sys.exit(main())
