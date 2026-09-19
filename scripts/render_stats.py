"""Render a contribution grid + language bar as one SVG.

Self-hosted on purpose: the public github-readme-stats instance is paused and
its card renders as a broken image, so nothing here depends on a third party.
Colours are neutral greys that read on GitHub's light and dark themes alike.
"""

import json
import os
import subprocess
import sys
from datetime import datetime, timedelta, timezone

USER = "ahtishamdilawar"
ACCENT = "#f05a28"
MUTED = "#8b949e"
OUT = os.path.join(os.path.dirname(__file__), "..", "stats.svg")

# coursework noise, not what the repos are actually about
SKIP_LANGS = {"Jupyter Notebook", "CSS", "HTML", "R", "TeX", "Batchfile", "Makefile"}

CAL_QUERY = """
query($login:String!, $from:DateTime!, $to:DateTime!) {
  user(login:$login) {
    contributionsCollection(from:$from, to:$to) {
      contributionCalendar {
        totalContributions
        weeks { contributionDays { date contributionCount weekday } }
      }
    }
  }
}
"""

LANG_QUERY = """
query($login:String!) {
  user(login:$login) {
    repositories(first:100, isFork:false, ownerAffiliations:OWNER, privacy:PUBLIC) {
      nodes { languages(first:10) { edges { size node { name } } } }
    }
  }
}
"""


def graphql(query, **variables):
    payload = json.dumps({"query": query, "variables": variables})
    token = os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN")
    if token:
        import urllib.request

        req = urllib.request.Request(
            "https://api.github.com/graphql",
            data=payload.encode(),
            headers={"Authorization": f"bearer {token}", "Content-Type": "application/json"},
        )
        with urllib.request.urlopen(req) as resp:
            body = json.load(resp)
    else:
        gh = os.environ.get("GH_PATH", "gh")
        proc = subprocess.run(
            [gh, "api", "graphql", "--input", "-"],
            input=payload, capture_output=True, text=True, encoding="utf-8",
        )
        if proc.returncode != 0:
            sys.exit(proc.stderr)
        body = json.loads(proc.stdout)
    if "errors" in body:
        sys.exit(json.dumps(body["errors"]))
    return body["data"]


def contributions():
    to = datetime.now(timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0)
    frm = to - timedelta(days=364)
    # "from" is a keyword, so the variables go in as a dict
    cal = graphql(CAL_QUERY, **{
        "login": USER,
        "from": frm.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "to": to.strftime("%Y-%m-%dT%H:%M:%SZ"),
    })["user"]["contributionsCollection"]["contributionCalendar"]
    return cal["totalContributions"], cal["weeks"]


def languages():
    totals = {}
    for repo in graphql(LANG_QUERY, login=USER)["user"]["repositories"]["nodes"]:
        for edge in repo["languages"]["edges"]:
            name = edge["node"]["name"]
            if name in SKIP_LANGS:
                continue
            totals[name] = totals.get(name, 0) + edge["size"]
    ranked = sorted(totals.items(), key=lambda kv: -kv[1])[:5]
    grand = sum(size for _, size in ranked) or 1
    return [(name, size / grand) for name, size in ranked]


CELL, GAP = 11, 3
STEP = CELL + GAP
PAD_LEFT, PAD_TOP = 30, 22


def render():
    total, weeks = contributions()
    langs = languages()

    grid_w = len(weeks) * STEP - GAP
    grid_bottom = PAD_TOP + 7 * STEP - GAP
    bar_y = grid_bottom + 34
    height = bar_y + 44

    out = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{PAD_LEFT + grid_w + 8}" '
        f'height="{height}" viewBox="0 0 {PAD_LEFT + grid_w + 8} {height}" '
        f'font-family="ui-monospace, SFMono-Regular, Menlo, monospace">',
        f'<style>text{{fill:{MUTED};font-size:9px}} .h{{font-size:10px}}</style>',
    ]

    # month labels, one per month at the week it starts
    seen = set()
    for i, week in enumerate(weeks):
        day = week["contributionDays"][0]
        month = day["date"][:7]
        if month in seen:
            continue
        seen.add(month)
        if i == 0 or i > len(weeks) - 3:
            continue
        label = datetime.strptime(day["date"], "%Y-%m-%d").strftime("%b").lower()
        out.append(f'<text x="{PAD_LEFT + i * STEP}" y="{PAD_TOP - 8}">{label}</text>')

    for row, label in ((1, "mon"), (3, "wed"), (5, "fri")):
        out.append(f'<text x="0" y="{PAD_TOP + row * STEP + CELL - 2}">{label}</text>')

    for i, week in enumerate(weeks):
        for day in week["contributionDays"]:
            count = day["contributionCount"]
            x = PAD_LEFT + i * STEP
            y = PAD_TOP + day["weekday"] * STEP
            if count == 0:
                fill, opacity = MUTED, "0.14"
            else:
                # fixed buckets; scaling to the busiest day flattens a normal week
                level = sum(count > t for t in (2, 5, 9))
                fill, opacity = ACCENT, ("0.32", "0.55", "0.78", "1")[level]
            out.append(
                f'<rect x="{x}" y="{y}" width="{CELL}" height="{CELL}" rx="2" '
                f'fill="{fill}" fill-opacity="{opacity}"/>'
            )

    out.append(
        f'<text class="h" x="{PAD_LEFT}" y="{grid_bottom + 18}">'
        f'{total:,} contributions in the last year</text>'
    )

    x = float(PAD_LEFT)
    for idx, (_, share) in enumerate(langs):
        w = share * grid_w
        opacity = ("1", "0.78", "0.58", "0.4", "0.26")[idx]
        out.append(
            f'<rect x="{x:.1f}" y="{bar_y}" width="{max(w - 2, 1):.1f}" height="7" rx="3" '
            f'fill="{ACCENT}" fill-opacity="{opacity}"/>'
        )
        x += w

    x = float(PAD_LEFT)
    for idx, (name, share) in enumerate(langs):
        opacity = ("1", "0.78", "0.58", "0.4", "0.26")[idx]
        out.append(
            f'<rect x="{x:.1f}" y="{bar_y + 19}" width="7" height="7" rx="2" '
            f'fill="{ACCENT}" fill-opacity="{opacity}"/>'
            f'<text x="{x + 11:.1f}" y="{bar_y + 26}">{name.lower()} {share * 100:.0f}%</text>'
        )
        x += len(name) * 5.6 + 46

    out.append("</svg>")
    with open(OUT, "w", encoding="utf-8") as fh:
        fh.write("\n".join(out))
    print(f"wrote {OUT}: {total:,} contributions, {len(langs)} languages")


if __name__ == "__main__":
    render()
