#!/usr/bin/env python3
"""Open a GitHub issue for each seasonal event whose reminder date has arrived.

Reads .github/seasonal-calendar.json. Run by the seasonal-reminders GitHub
Action every Monday; can also be run by hand:

    python3 scripts/seasonal_reminders.py --dry-run                  # what would open today
    python3 scripts/seasonal_reminders.py --dry-run --date 2026-10-12

An issue opens once the event is within 'remind_days_before' days and stays
the only one for that event that year (it isn't opened again, even if closed).
Creating issues needs the GitHub CLI (`gh`), which the Action provides.
"""

import argparse
import datetime
import json
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CALENDAR = ROOT / ".github" / "seasonal-calendar.json"
LABEL = "seasonal-reminder"
MONTHS = ["january", "february", "march", "april", "may", "june", "july",
          "august", "september", "october", "november", "december"]
WEEKDAYS = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
ORDINALS = {"first": 1, "second": 2, "third": 3, "fourth": 4}


def easter(year):
    """Easter Sunday (Gregorian), Anonymous Gregorian algorithm."""
    a, b, c = year % 19, year // 100, year % 100
    d, e = b // 4, b % 4
    f = (b + 8) // 25
    g = (b - f + 1) // 3
    h = (19 * a + b - d - g + 15) % 30
    i, k = c // 4, c % 4
    l = (32 + 2 * e + 2 * i - h - k) % 7
    m = (a + 11 * h + 22 * l) // 451
    month = (h + l - 7 * m + 114) // 31
    day = (h + l - 7 * m + 114) % 31 + 1
    return datetime.date(year, month, day)


def resolve(when, year):
    when = when.strip().lower()
    if m := re.fullmatch(r"(\d{2})-(\d{2})", when):
        return datetime.date(year, int(m[1]), int(m[2]))
    if m := re.fullmatch(r"easter([+-]\d+)", when):
        return easter(year) + datetime.timedelta(days=int(m[1]))
    if m := re.fullmatch(r"(first|second|third|fourth|last) (\w+) of (\w+)", when):
        weekday, month = WEEKDAYS.index(m[2]), MONTHS.index(m[3]) + 1
        if m[1] == "last":
            day = datetime.date(year + month // 12, month % 12 + 1, 1) - datetime.timedelta(days=1)
            return day - datetime.timedelta(days=(day.weekday() - weekday) % 7)
        first = datetime.date(year, month, 1)
        first += datetime.timedelta(days=(weekday - first.weekday()) % 7)
        return first + datetime.timedelta(weeks=ORDINALS[m[1]] - 1)
    raise ValueError(f"Don't understand 'when': {when!r}")


def due_events(events, today):
    for event in events:
        for year in (today.year, today.year + 1):
            date = resolve(event["when"], year)
            remind = date - datetime.timedelta(days=event.get("remind_days_before", 21))
            if remind <= today < date:
                yield event, date


def title_for(event, date):
    return f"Seasonal: {event['name']} ({date.day} {date:%B %Y})"


def body_for(event, date, today):
    lines = [
        f"**{event['name']}** is on **{date:%A} {date.day} {date:%B %Y}**, "
        f"{(date - today).days} days from when this reminder opened.",
        "",
        f"**Why it matters:** {event['why']}",
        "",
    ]
    if event.get("ideas"):
        lines += ["**Ideas for the website**"] + [f"- {idea}" for idea in event["ideas"]] + [""]
    lines += ["**Checklist**"]
    lines += [f"- [ ] {task}" for task in event.get("tasks", [])]
    if event.get("ideas"):
        lines += [
            "- [ ] Decide whether to write something for this (it's fine to skip it)",
            "- [ ] If writing something: publish it at least three weeks before the date so Google can find it",
            "- [ ] Keep the tone supportive, not salesy, and link to the Crisis Support page",
            "- [ ] Share it on Google Business Profile and LinkedIn",
        ]
    lines += [
        "- [ ] Run `python3 scripts/check_site.py --fix` before publishing (Claude Code does this for you; see CLAUDE.md)",
        "",
        "To work on this with Claude Code, say something like: "
        f"\"Read CLAUDE.md, then help me with the '{event['name']}' seasonal reminder.\"",
        "",
        "_Opened automatically from `.github/seasonal-calendar.json`. Close this issue when you're done, or if you're skipping it this year._",
    ]
    return "\n".join(lines)


def gh(*args):
    return subprocess.run(["gh", *args], cwd=ROOT, capture_output=True, text=True, check=True).stdout


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--date", help="pretend today is YYYY-MM-DD")
    parser.add_argument("--dry-run", action="store_true", help="print issues instead of opening them")
    args = parser.parse_args()
    today = datetime.date.fromisoformat(args.date) if args.date else datetime.date.today()

    events = json.loads(CALENDAR.read_text(encoding="utf-8"))["events"]
    due = list(due_events(events, today))
    if not due:
        print("No seasonal reminders due.")
        return

    existing = set()
    if not args.dry_run:
        gh("label", "create", LABEL, "--color", "6C7C59",
           "--description", "Automatic seasonal website reminder", "--force")
        issues = json.loads(gh("issue", "list", "--label", LABEL, "--state", "all",
                               "--limit", "1000", "--json", "title"))
        existing = {issue["title"] for issue in issues}

    for event, date in due:
        title = title_for(event, date)
        if title in existing:
            print(f"already open or done: {title}")
            continue
        body = body_for(event, date, today)
        if args.dry_run:
            print(f"--- would open: {title}\n{body}\n")
        else:
            gh("issue", "create", "--title", title, "--body", body, "--label", LABEL)
            print(f"opened: {title}")


if __name__ == "__main__":
    main()
