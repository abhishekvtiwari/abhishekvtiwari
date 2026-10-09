"""Build the whole GitHub profile from profile.yml.

    python scripts/build_profile.py

Reads   profile.yml                 (the only file you need to edit)
        your public contribution calendar on github.com
Writes  README.md                   (the profile page; never edit it by hand)
        assets/banner.svg           (the green banner)
        assets/whoami.svg           (the left terminal card)
        assets/stats.svg            (the right terminal card)
        assets/contributions.svg    (the heatmap)

A GitHub Action runs this every morning and whenever profile.yml, resume/ or
certificates/ change, so you only ever edit profile.yml and upload files.
"""
from __future__ import annotations

import datetime as dt
import html
import os
import re
import urllib.parse
import urllib.request
from collections import OrderedDict
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / "assets"
USER = "abhishekvtiwari"

BG, PANEL, LINE = "#0d1117", "#161b22", "#30363d"
TEXT, MUTED, GREEN = "#e6edf3", "#8b949e", "#3fb950"
LEVELS = ["#161b22", "#0e4429", "#006d32", "#26a641", "#39d353"]
MONO = "ui-monospace, SFMono-Regular, Consolas, 'Liberation Mono', Menlo, monospace"
SANS = "'Segoe UI', 'Helvetica Neue', Arial, sans-serif"

# Badge colour and logo for skills shields.io knows; anything else is grey.
BADGES = {
    "sql": ("336791", "postgresql"), "mysql": ("4479A1", "mysql"), "python": ("3776AB", "python"),
    "pandas": ("150458", "pandas"), "power bi": ("F2C811", "powerbi"), "excel": ("217346", "microsoftexcel"),
    "vba": ("217346", "microsoftexcel"), "scikit-learn": ("F7931E", "scikitlearn"), "fastapi": ("009688", "fastapi"),
    "react": ("20232A", "react"), "postgresql": ("336791", "postgresql"), "git": ("F05032", "git"),
    "tableau": ("E97627", "tableau"), "jira": ("0052CC", "jira"), "confluence": ("172B4D", "confluence"),
    "numpy": ("013243", "numpy"), "docker": ("2496ED", "docker"), "hackerrank": ("2EC866", "hackerrank"),
    "macros": ("217346", "microsoftexcel"), "powerpoint": ("B7472A", "microsoftpowerpoint"),
    "microsoft teams": ("6264A7", "microsoftteams"), "teams": ("6264A7", "microsoftteams"), "slack": ("4A154B", "slack"),
    "word": ("2B579A", "microsoftword"), "outlook": ("0078D4", "microsoftoutlook"), "sharepoint": ("0078D4", "microsoftsharepoint"),
    "notion": ("000000", "notion"), "clickup": ("7B68EE", "clickup"), "google sheets": ("34A853", "googlesheets"),
}
DARK_TEXT = {"F2C811", "F7931E"}


def load():
    with open(ROOT / "profile.yml", encoding="utf-8") as f:
        return yaml.safe_load(f)


# ------------------------------------------------------------ contributions
def fetch_calendar():
    req = urllib.request.Request(f"https://github.com/users/{USER}/contributions", headers={"User-Agent": "profile-builder"})
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
    total, active = sum(counts), sum(1 for c in counts if c)
    best_i = max(range(len(counts)), key=lambda i: counts[i]) if counts else 0
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
    current, i = 0, len(counts) - 1
    if i >= 0 and counts[i] == 0:          # today may simply not have started yet
        i -= 1
    end = dates[i] if i >= 0 else None
    while i >= 0 and counts[i]:
        current, i = current + 1, i - 1
    months = OrderedDict()
    for d, c in zip(dates, counts):
        months[(d.year, d.month)] = months.get((d.year, d.month), 0) + c
    return {"total": total, "active": active, "days": len(dates), "best": counts[best_i] if counts else 0,
            "best_day": dates[best_i] if counts else None, "avg": total / active if active else 0,
            "longest": longest, "longest_span": longest_span, "current": current,
            "cur_span": (dates[i + 1], end) if current else None, "months": list(months.items())[-12:]}


def short(d):
    return f"{d.strftime('%b')} {d.day}"


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
    start = dates[0] - dt.timedelta(days=(dates[0].weekday() + 1) % 7)
    weeks = ((dates[-1] - start).days // 7) + 1
    left, top = 46, 64
    width, height = left + weeks * (cell + gap) + 30, top + 7 * (cell + gap) + 46
    out, last_month = [], None
    for d, (count, level) in days.items():
        w, r = (d - start).days // 7, (d.weekday() + 1) % 7
        x, y = left + w * (cell + gap), top + r * (cell + gap)
        out.append(f'<rect x="{x}" y="{y}" width="{cell}" height="{cell}" rx="3" fill="{LEVELS[level]}"><title>{count} on {d.isoformat()}</title></rect>')
        if r == 0 and d.month != last_month and d.day <= 7:
            out.append(f'<text x="{x}" y="{top - 10}" fill="{MUTED}" font-family="{MONO}" font-size="11">{d.strftime("%b")}</text>')
            last_month = d.month
    for r, name in ((1, "Mon"), (3, "Wed"), (5, "Fri")):
        out.append(f'<text x="10" y="{top + r * (cell + gap) + 10}" fill="{MUTED}" font-family="{MONO}" font-size="11">{name}</text>')
    ly = top + 7 * (cell + gap) + 22
    out.append(f'<text x="{left}" y="{ly + 4}" fill="{TEXT}" font-family="{MONO}" font-size="13" font-weight="700">{s["total"]:,} contributions in the last year</text>')
    lx = width - 30 - 5 * (cell + gap) - 70
    out.append(f'<text x="{lx}" y="{ly + 4}" fill="{MUTED}" font-family="{MONO}" font-size="11">Less</text>')
    for i, c in enumerate(LEVELS):
        out.append(f'<rect x="{lx + 36 + i * (cell + gap)}" y="{ly - 7}" width="{cell}" height="{cell}" rx="3" fill="{c}"/>')
    out.append(f'<text x="{lx + 36 + 5 * (cell + gap) + 4}" y="{ly + 4}" fill="{MUTED}" font-family="{MONO}" font-size="11">More</text>')
    return window(width, height, f"{USER}@github: ~ $ ./contributions.sh", "".join(out))


def stats_svg(s):
    W, H = 470, 520
    tiles = [
        ("current streak", f'{s["current"]}', "days", f'{short(s["cur_span"][0])} - {short(s["cur_span"][1])}' if s["cur_span"] else "start one today", True),
        ("longest streak", f'{s["longest"]}', "days", f'{short(s["longest_span"][0])} - {short(s["longest_span"][1])}' if s["longest_span"] else "", False),
        ("contributions", f'{s["total"]:,}', "", "in the last year", False),
        ("active days", f'{s["active"]}', f'/ {s["days"]}', f'{round(100 * s["active"] / s["days"]) if s["days"] else 0}% of the year', False),
        ("best day", f'{s["best"]}', "", short(s["best_day"]) if s["best_day"] else "", False),
        ("avg / active day", f'{s["avg"]:.1f}', "", "contributions", False),
    ]
    body, tw, th = [], 205, 74
    for i, (label, big, unit, sub, accent) in enumerate(tiles):
        x, y = 20 + (i % 2) * (tw + 20), 50 + (i // 2) * (th + 14)
        body.append(f'<rect x="{x}" y="{y}" width="{tw}" height="{th}" rx="8" fill="{PANEL}" stroke="{LINE}"/>'
                    f'<text x="{x + 12}" y="{y + 20}" fill="{MUTED}" font-family="{MONO}" font-size="11">$ {label}</text>'
                    f'<text x="{x + 12}" y="{y + 50}" fill="{GREEN if accent else TEXT}" font-family="{MONO}" font-size="26" font-weight="700">{big}'
                    f'<tspan fill="{MUTED}" font-size="12" font-weight="400"> {unit}</tspan></text>'
                    f'<text x="{x + 12}" y="{y + 66}" fill="{MUTED}" font-family="{MONO}" font-size="10">{html.escape(sub)}</text>')
    cy = 320
    body.append(f'<rect x="20" y="{cy}" width="{W - 40}" height="180" rx="8" fill="{PANEL}" stroke="{LINE}"/>'
                f'<text x="32" y="{cy + 20}" fill="{MUTED}" font-family="{MONO}" font-size="11">$ contributions / month</text>')
    months = s["months"]
    peak = max((v for _, v in months), default=0) or 1
    bw = (W - 80) / max(len(months), 1)
    for i, ((y, m), v) in enumerate(months):
        h, bx = 110 * v / peak, 40 + i * bw
        top = cy + 150 - h
        body.append(f'<rect x="{bx + 4:.1f}" y="{top:.1f}" width="{bw - 8:.1f}" height="{max(h, 2):.1f}" rx="2" fill="{"#39d353" if v == peak and v else "#26a641"}"/>'
                    f'<text x="{bx + bw / 2:.1f}" y="{cy + 168}" text-anchor="middle" fill="{MUTED}" font-family="{MONO}" font-size="10">{dt.date(y, m, 1).strftime("%b")[0]}</text>')
        if v == peak and v:
            body.append(f'<text x="{bx + bw / 2:.1f}" y="{top - 5:.1f}" text-anchor="middle" fill="{TEXT}" font-family="{MONO}" font-size="10" font-weight="700">{v:,}</text>')
    return window(W, H, f"{USER}@github: ~ $ ./stats.sh", "".join(body))


# ------------------------------------------------------------ text helpers
def wrap(text, width):
    words, lines, cur = str(text).split(), [], ""
    for w in words:
        if len(cur) + len(w) + (1 if cur else 0) > width:
            lines.append(cur)
            cur = w
        else:
            cur = f"{cur} {w}" if cur else w
    return lines + ([cur] if cur else [])


def whoami_svg(p):
    W, H = 470, 520
    lines = [("$ whoami", TEXT, True), (p["name"], GREEN, True)]
    lines += [(l, TEXT, False) for l in wrap(p["role"], 46)]
    lines += [(f'@ {p["company"]}', TEXT, False), ("", None, False), ("$ cat skills.txt", TEXT, True)]
    for group, items in (p.get("skills") or {}).items():
        lines += [(l, MUTED, False) for l in wrap(f"{group}: " + " · ".join(items), 46)]
    c = p.get("compounza") or {}
    if c.get("show"):
        lines += [("", None, False), ("$ cat side-project.txt", TEXT, True),
                  (f'Compounza · {c.get("link", "").split("//")[-1]}', MUTED, False)]
    lines += [("", None, False), ("$ echo $CONTACT", TEXT, True), (p.get("email", ""), MUTED, False)]
    body, y = [], 64
    for text, colour, bold in lines:
        if y > H - 30:
            break
        if text:
            body.append(f'<text x="24" y="{y}" fill="{colour}" font-family="{MONO}" font-size="13.5" font-weight="{"700" if bold else "400"}" xml:space="preserve">{html.escape(text)}</text>')
        y += 21
    body.append(f'<rect x="24" y="{min(y, H - 24) - 13}" width="9" height="16" fill="{GREEN}"><animate attributeName="opacity" values="1;0;1" dur="1.2s" repeatCount="indefinite"/></rect>')
    return window(W, H, f"{USER}@github: ~ $ whoami", "".join(body))


def banner_svg(p):
    role = html.escape(p["role"], quote=False)
    role_caps = html.escape(p["role"].upper(), quote=False)
    company = html.escape(p["company"], quote=False)
    tag = wrap(p.get("tagline", ""), 58)[:2]
    tagline = "".join(f'<text x="72" y="{214 + i * 30}" fill="#c9d6cd" font-family="{SANS}" font-size="22">{html.escape(l)}</text>' for i, l in enumerate(tag))
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1280 340" width="1280" height="340" role="img" aria-label="{html.escape(p["name"])}, {role} at {company}">
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#04281a"/><stop offset="1" stop-color="#0b3d26"/></linearGradient>
    <radialGradient id="glow" cx="0.82" cy="0.35" r="0.55"><stop offset="0" stop-color="#4dd658" stop-opacity="0.28"/><stop offset="1" stop-color="#4dd658" stop-opacity="0"/></radialGradient>
    <pattern id="dots" width="22" height="22" patternUnits="userSpaceOnUse"><circle cx="2" cy="2" r="1.4" fill="#4dd658" fill-opacity="0.14"/></pattern>
  </defs>
  <rect width="1280" height="340" rx="22" fill="url(#bg)"/><rect width="1280" height="340" rx="22" fill="url(#dots)"/><rect width="1280" height="340" rx="22" fill="url(#glow)"/>
  <g fill="#4dd658">
    <rect x="890" y="236" width="34" height="54" rx="5" fill-opacity="0.35"/><rect x="938" y="214" width="34" height="76" rx="5" fill-opacity="0.45"/>
    <rect x="986" y="184" width="34" height="106" rx="5" fill-opacity="0.55"/><rect x="1034" y="146" width="34" height="144" rx="5" fill-opacity="0.68"/>
    <rect x="1082" y="98" width="34" height="192" rx="5" fill-opacity="0.82"/><rect x="1130" y="44" width="34" height="246" rx="5"/>
  </g>
  <polyline points="907,226 955,203 1003,172 1051,133 1099,84 1147,30" fill="none" stroke="#e3e1d3" stroke-width="3" stroke-linecap="round" stroke-dasharray="2 9"/>
  <text x="72" y="92" fill="#4dd658" font-family="{MONO}" font-size="16" letter-spacing="3">{role_caps}</text>
  <text x="70" y="164" fill="#ffffff" font-family="{SANS}" font-size="64" font-weight="800" letter-spacing="-1.5">{html.escape(p["name"])}</text>
  {tagline}
  <text x="72" y="300" fill="#93ac9b" font-family="{SANS}" font-size="18">@ <tspan fill="#e3e1d3" font-weight="700">{company}</tspan></text>
</svg>'''


# ------------------------------------------------------------ README
def badge(name):
    colour, logo = BADGES.get(name.lower(), ("555555", ""))
    label = urllib.parse.quote(name.replace("-", "--").replace("_", "__"))
    logo_part = f"&logo={logo}&logoColor={'black' if colour in DARK_TEXT else 'white'}" if logo else ""
    return f'<img src="https://img.shields.io/badge/{label}-{colour}?style=flat-square{logo_part}" alt="{html.escape(name)}">'


def link_for(value):
    """A file in this repository or a full web address."""
    if not value:
        return ""
    if value.startswith(("http://", "https://")):
        return value
    return urllib.parse.quote(value)


def readme(p, have_stats):
    L = []
    L.append(f'<!-- THIS FILE IS GENERATED from profile.yml by scripts/build_profile.py. Edit profile.yml, not this file. See GUIDE.md. -->')
    L.append(f'<p align="center"><img src="assets/banner.svg" alt="{html.escape(p["name"])}, {html.escape(p["role"], quote=False)} at {html.escape(p["company"], quote=False)}" width="100%"></p>\n')
    L.append(f'<h3 align="center">Hi, I\'m {html.escape(p.get("first_name", p["name"]))} 👋 · {html.escape(p["role"], quote=False)} at {html.escape(p["company"], quote=False)}</h3>\n')
    L.append(f'<p align="center">{html.escape(p.get("tagline", ""))}</p>\n')
    buttons = []
    if p.get("linkedin"):
        buttons.append(f'<a href="{p["linkedin"]}"><img src="https://img.shields.io/badge/LinkedIn-Connect-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white" alt="LinkedIn"></a>')
    if p.get("email"):
        buttons.append(f'<a href="mailto:{p["email"]}"><img src="https://img.shields.io/badge/Email-{urllib.parse.quote(p["email"].replace("-", "--"))}-c62828?style=for-the-badge&logo=gmail&logoColor=white" alt="Email"></a>')
    if p.get("resume"):
        buttons.append(f'<a href="{link_for(p["resume"])}"><img src="https://img.shields.io/badge/Resume-View-555555?style=for-the-badge&logo=readthedocs&logoColor=white" alt="Résumé"></a>')
    if p.get("website"):
        buttons.append(f'<a href="{p["website"]}"><img src="https://img.shields.io/badge/Compounza-{urllib.parse.quote(p["website"].split("//")[-1])}-167a45?style=for-the-badge" alt="Website"></a>')
    L.append('<p align="center">\n  ' + "\n  ".join(buttons) + '\n</p>\n')

    L.append(f'<h3 align="center"><code>{USER}@github ~ $ whoami</code></h3>\n')
    if have_stats:
        L.append('<p align="center">\n  <img src="assets/whoami.svg" alt="whoami card" width="49%">\n  <img src="assets/stats.svg" alt="Contribution stats" width="49%">\n</p>\n')
        L.append(f'<h3 align="center"><code>{USER}@github ~ $ ./contributions.sh</code></h3>\n')
        L.append('<p align="center"><img src="assets/contributions.svg" alt="Contribution calendar for the last year" width="100%"></p>\n')
    else:
        L.append('<p align="center"><img src="assets/whoami.svg" alt="whoami card" width="60%"></p>\n')

    L.append('---\n\n## 🙋 About me\n')
    L += [f"- {a}" for a in p.get("about") or []]
    L.append("")

    c = p.get("compounza") or {}
    if c.get("show"):
        L.append('## 🌱 My personal project: Compounza\n')
        L.append('<img src="assets/compounza-mark.png" alt="Compounza" width="64" align="right">\n')
        L.append(f'{c.get("story", "")}\n')
        L += [f"- {i}" for i in c.get("items") or []]
        if c.get("link"):
            L.append(f'\n**→ [{c["link"].split("//")[-1]}]({c["link"]})**')
        L.append("")

    if p.get("skills"):
        L.append('## 🛠️ Skills\n')
        L.append('<table>')
        for group, items in p["skills"].items():
            L.append(f'<tr><td><b>{html.escape(group)}</b></td><td>' + " ".join(badge(i) for i in items) + '</td></tr>')
        L.append('</table>\n')

    if p.get("achievements"):
        L.append('## 🏆 Achievements and certificates\n')
        L.append('| | Detail |\n|---|---|')
        for a in p["achievements"]:
            title = f'[{a["title"]}]({link_for(a["link"])})' if a.get("link") else a["title"]
            L.append(f'| **{title}** | {a.get("detail", "")} |')
        L.append("")

    if p.get("projects"):
        L.append('## 📌 Featured projects\n')
        L.append('| Project | What it is | Built with |\n|---|---|---|')
        for pr in p["projects"]:
            L.append(f'| [**{pr["name"]}**](https://github.com/{USER}/{pr["repo"]}) | {pr["what"]} | {pr.get("stack", "")} |')
        L.append("")

    L.append("## 🤝 Let's connect\n")
    bits = []
    if p.get("email"):
        bits.append(f'📫 **{p["email"]}**')
    if p.get("linkedin"):
        bits.append(f'💼 [LinkedIn]({p["linkedin"]})')
    if p.get("resume"):
        bits.append(f'📄 [Résumé]({link_for(p["resume"])})')
    if p.get("website"):
        bits.append(f'🌐 [{p["website"].split("//")[-1]}]({p["website"]})')
    L.append(" · ".join(bits) + "\n")
    L.append('<p align="center"><sub>Cards refresh every morning from the public contribution calendar · this page is built from <a href="profile.yml">profile.yml</a> · <a href="GUIDE.md">how to edit it</a></sub></p>')
    return "\n".join(L) + "\n"


def main():
    p = load()
    ASSETS.mkdir(exist_ok=True)
    (ASSETS / "banner.svg").write_text(banner_svg(p), encoding="utf-8")
    (ASSETS / "whoami.svg").write_text(whoami_svg(p), encoding="utf-8")
    have_stats = True
    try:
        days = fetch_calendar()
        s = stats(days)
        (ASSETS / "contributions.svg").write_text(contributions_svg(days, s), encoding="utf-8")
        (ASSETS / "stats.svg").write_text(stats_svg(s), encoding="utf-8")
        print(f'{s["total"]} contributions, {s["active"]} active days')
    except Exception as exc:  # the profile still builds if github.com is slow
        print("calendar not refreshed:", exc)
        have_stats = (ASSETS / "stats.svg").exists()
    (ROOT / "README.md").write_text(readme(p, have_stats), encoding="utf-8")
    print("README.md built")


if __name__ == "__main__":
    main()
