"""Build the terminal-style images on the GitHub profile from the public
contribution calendar. Standard library only, so the daily GitHub Action needs
no installs.

    python scripts/build_profile.py

Writes assets/contributions.svg, assets/stats.svg and assets/whoami.svg.
"""
from __future__ import annotations

import datetime as dt
import html
import re
import urllib.request
from collections import OrderedDict
from pathlib import Path

USER = "abhishekvtiwari"
ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / "assets"

BG, PANEL, LINE = "#0d1117", "#161b22", "#30363d"
TEXT, MUTED, GREEN = "#e6edf3", "#8b949e", "#3fb950"
LEVELS = ["#161b22", "#0e4429", "#006d32", "#26a641", "#39d353"]
MONO = "ui-monospace, SFMono-Regular, Consolas, 'Liberation Mono', Menlo, monospace"


def fetch_calendar() -> "OrderedDict[dt.date, tuple[int, int]]":
    req = urllib.request.Request(f"https://github.com/users/{USER}/contributions",
                                 headers={"User-Agent": "profile-builder"})
    page = urllib.request.urlopen(req, timeout=30).read().decode("utf-8")
    cells = re.findall(r'data-date="(\d{4}-\d{2}-\d{2})"\s+id="([^"]+)"\s+data-level="(\d)"', page)
    tips = dict(re.findall(r'<tool-tip[^>]*for="([^"]+)"[^>]*>([^<]+)</tool-tip>', page))
    days = {}
    for date, cid, level in cells:
        m = re.match(r"(\d[\d,]*) contribution", tips.get(cid, ""))
        days[dt.date.fromisoformat(date)] = (int(m.group(1).replace(",", "")) if m else 0, int(level))
    return OrderedDict(sorted(days.items()))


def stats(days):
    dates = list(days)
    counts = [days[d][0] for d in dates]
    total = sum(counts)
    active = sum(1 for c in counts if c)
    best_i = max(range(len(counts)), key=lambda i: counts[i]) if counts else 0
    # longest and current streaks
    longest = run = 0
    longest_span = run_start = None
    for d, c in zip(dates, counts):
        if c:
            run_start = d if run == 0 else run_start
            run += 1
            if run > longest:
                longest, longest_span = run, (run_start, d)
        else:
            run = 0
    current = 0
    i = len(counts) - 1
    if i >= 0 and counts[i] == 0:      # today not counted yet: the streak may still be alive
        i -= 1
    end = dates[i] if i >= 0 else None
    while i >= 0 and counts[i]:
        current += 1
        i -= 1
    cur_span = (dates[i + 1], end) if current else None
    months = OrderedDict()
    for d, c in zip(dates, counts):
        key = (d.year, d.month)
        months[key] = months.get(key, 0) + c
    return {"total": total, "active": active, "days": len(dates), "best": counts[best_i] if counts else 0,
            "best_day": dates[best_i] if counts else None, "avg": total / active if active else 0,
            "longest": longest, "longest_span": longest_span, "current": current, "cur_span": cur_span,
            "months": list(months.items())[-12:]}


def fmt(d):
    return d.strftime("%b %-d") if hasattr(d, "strftime") and not __import__("os").name == "nt" else d.strftime("%b %#d")


def window(width, height, title, body):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}">'
            f'<rect width="{width}" height="{height}" rx="12" fill="{BG}" stroke="{LINE}"/>'
            f'<circle cx="20" cy="18" r="5.5" fill="#ff5f57"/><circle cx="38" cy="18" r="5.5" fill="#febc2e"/>'
            f'<circle cx="56" cy="18" r="5.5" fill="#28c840"/>'
            f'<text x="{width / 2}" y="22" text-anchor="middle" fill="{MUTED}" font-family="{MONO}" font-size="11">{html.escape(title)}</text>'
            f'<line x1="0" y1="34" x2="{width}" y2="34" stroke="{LINE}"/>{body}</svg>')


def contributions_svg(days, s):
    cell, gap = 13, 3
    dates = list(days)
    first = dates[0]
    start = first - dt.timedelta(days=(first.weekday() + 1) % 7)   # weeks start on Sunday, like GitHub
    weeks = ((dates[-1] - start).days // 7) + 1
    left, top = 46, 64
    width = left + weeks * (cell + gap) + 30
    height = top + 7 * (cell + gap) + 46
    out, last_month = [], None
    for d, (count, level) in days.items():
        w = (d - start).days // 7
        r = (d.weekday() + 1) % 7
        x, y = left + w * (cell + gap), top + r * (cell + gap)
        out.append(f'<rect x="{x}" y="{y}" width="{cell}" height="{cell}" rx="3" fill="{LEVELS[level]}">'
                   f'<title>{count} on {d.isoformat()}</title></rect>')
        if r == 0 and d.month != last_month and d.day <= 7:
            out.append(f'<text x="{x}" y="{top - 10}" fill="{MUTED}" font-family="{MONO}" font-size="11">{d.strftime("%b")}</text>')
            last_month = d.month
    for r, name in ((1, "Mon"), (3, "Wed"), (5, "Fri")):
        out.append(f'<text x="10" y="{top + r * (cell + gap) + 10}" fill="{MUTED}" font-family="{MONO}" font-size="11">{name}</text>')
    legend_y = top + 7 * (cell + gap) + 22
    out.append(f'<text x="{left}" y="{legend_y + 4}" fill="{TEXT}" font-family="{MONO}" font-size="13" font-weight="700">'
               f'{s["total"]:,} contributions in the last year</text>')
    lx = width - 30 - 5 * (cell + gap) - 70
    out.append(f'<text x="{lx}" y="{legend_y + 4}" fill="{MUTED}" font-family="{MONO}" font-size="11">Less</text>')
    for i, c in enumerate(LEVELS):
        out.append(f'<rect x="{lx + 36 + i * (cell + gap)}" y="{legend_y - 7}" width="{cell}" height="{cell}" rx="3" fill="{c}"/>')
    out.append(f'<text x="{lx + 36 + 5 * (cell + gap) + 4}" y="{legend_y + 4}" fill="{MUTED}" font-family="{MONO}" font-size="11">More</text>')
    return window(width, height, f"{USER}@github: ~ $ ./contributions.sh", "".join(out))


def stats_svg(s):
    W, H = 470, 520
    tiles = [
        ("current streak", f'{s["current"]}', "days", f'{fmt(s["cur_span"][0])} - {fmt(s["cur_span"][1])}' if s["cur_span"] else "start one today", True),
        ("longest streak", f'{s["longest"]}', "days", f'{fmt(s["longest_span"][0])} - {fmt(s["longest_span"][1])}' if s["longest_span"] else "", False),
        ("contributions", f'{s["total"]:,}', "", "in the last year", False),
        ("active days", f'{s["active"]}', f'/ {s["days"]}', f'{round(100 * s["active"] / s["days"]) if s["days"] else 0}% of the year', False),
        ("best day", f'{s["best"]}', "", fmt(s["best_day"]) if s["best_day"] else "", False),
        ("avg / active day", f'{s["avg"]:.1f}', "", "contributions", False),
    ]
    body = []
    tw, th = 205, 74
    for i, (label, big, unit, sub, accent) in enumerate(tiles):
        x, y = 20 + (i % 2) * (tw + 20), 50 + (i // 2) * (th + 14)
        body.append(f'<rect x="{x}" y="{y}" width="{tw}" height="{th}" rx="8" fill="{PANEL}" stroke="{LINE}"/>'
                    f'<text x="{x + 12}" y="{y + 20}" fill="{MUTED}" font-family="{MONO}" font-size="11">$ {label}</text>'
                    f'<text x="{x + 12}" y="{y + 50}" fill="{GREEN if accent else TEXT}" font-family="{MONO}" font-size="26" font-weight="700">{big}'
                    f'<tspan fill="{MUTED}" font-size="12" font-weight="400"> {unit}</tspan></text>'
                    f'<text x="{x + 12}" y="{y + 66}" fill="{MUTED}" font-family="{MONO}" font-size="10">{html.escape(sub)}</text>')
    cy, ch = 320, 180
    body.append(f'<rect x="20" y="{cy}" width="{W - 40}" height="{ch}" rx="8" fill="{PANEL}" stroke="{LINE}"/>'
                f'<text x="32" y="{cy + 20}" fill="{MUTED}" font-family="{MONO}" font-size="11">$ contributions / month</text>')
    months = s["months"]
    peak = max((v for _, v in months), default=0) or 1
    bw = (W - 80) / max(len(months), 1)
    for i, ((y, m), v) in enumerate(months):
        h = 110 * v / peak
        bx = 40 + i * bw
        top = cy + 150 - h
        colour = "#39d353" if v == peak and v else "#26a641"
        body.append(f'<rect x="{bx + 4:.1f}" y="{top:.1f}" width="{bw - 8:.1f}" height="{max(h, 2):.1f}" rx="2" fill="{colour}"/>'
                    f'<text x="{bx + bw / 2:.1f}" y="{cy + 168}" text-anchor="middle" fill="{MUTED}" font-family="{MONO}" font-size="10">{dt.date(y, m, 1).strftime("%b")[0]}</text>')
        if v == peak and v:
            body.append(f'<text x="{bx + bw / 2:.1f}" y="{top - 5:.1f}" text-anchor="middle" fill="{TEXT}" font-family="{MONO}" font-size="10" font-weight="700">{v:,}</text>')
    return window(W, H, f"{USER}@github: ~ $ ./stats.sh", "".join(body))


def whoami_svg():
    W, H = 470, 520
    lines = [
        ("$ whoami", TEXT, True),
        ("Abhishek Tiwari", GREEN, True),
        ("Data Analyst · Founder of Compounza", TEXT, False),
        ("", None, False),
        ("$ cat building.txt", TEXT, True),
        ("compounza.in: books and portfolio", MUTED, False),
        ("projects for careers in data", MUTED, False),
        ("", None, False),
        ("$ ls shelf/", TEXT, True),
        ("interview-readiness-book/  1,226 Q", MUTED, False),
        ("analyst-to-architect/      3 vols", MUTED, False),
        ("portfolio-projects/        16", MUTED, False),
        ("", None, False),
        ("$ cat stack.txt", TEXT, True),
        ("SQL · Python · pandas · Power BI", MUTED, False),
        ("Excel/VBA · scikit-learn · FastAPI", MUTED, False),
        ("React · PostgreSQL · Git", MUTED, False),
        ("", None, False),
        ("$ echo $CONTACT", TEXT, True),
        ("abhishekvtiwari008@gmail.com", MUTED, False),
    ]
    body, y = [], 64
    for text, colour, bold in lines:
        if text:
            weight = "700" if bold else "400"
            body.append(f'<text x="24" y="{y}" fill="{colour}" font-family="{MONO}" font-size="14" font-weight="{weight}" xml:space="preserve">{html.escape(text)}</text>')
        y += 22
    body.append(f'<rect x="24" y="{y - 14}" width="9" height="16" fill="{GREEN}"><animate attributeName="opacity" values="1;0;1" dur="1.2s" repeatCount="indefinite"/></rect>')
    return window(W, H, f"{USER}@github: ~ $ whoami", "".join(body))


def main():
    ASSETS.mkdir(exist_ok=True)
    days = fetch_calendar()
    s = stats(days)
    (ASSETS / "contributions.svg").write_text(contributions_svg(days, s), encoding="utf-8")
    (ASSETS / "stats.svg").write_text(stats_svg(s), encoding="utf-8")
    (ASSETS / "whoami.svg").write_text(whoami_svg(), encoding="utf-8")
    print(f'{s["total"]} contributions, {s["active"]} active days, current streak {s["current"]}, longest {s["longest"]}')


if __name__ == "__main__":
    main()
