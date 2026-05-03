"""
refresh_index.py — Weekly: enrich data/tools.csv with current GitHub stats.

Reads `data/tools.csv` (the curated index) and writes back the same file with
fresh stars / last-commit / archived fields populated from the GitHub API.

Designed to run via .github/workflows/refresh.yml on a Sunday cron.

Usage:
    python scripts/refresh_index.py           # in-place refresh
    python scripts/refresh_index.py --check   # report drift, do not write

Authentication: set GITHUB_TOKEN env var to avoid the unauthenticated
60-req/hour rate limit. The workflow provides ${{ secrets.GITHUB_TOKEN }}.
"""

from __future__ import annotations

import argparse
import csv
import os
import re
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parent.parent
TOOLS_CSV = ROOT / "data" / "tools.csv"

GH_REPO_RE = re.compile(r"https?://github\.com/([^/]+/[^/?#]+)")


def gh_repo_from_url(url: str) -> str | None:
    m = GH_REPO_RE.match(url or "")
    if not m:
        return None
    return m.group(1).removesuffix(".git").rstrip("/")


def gh_get(path: str, token: str | None) -> dict | None:
    headers = {"Accept": "application/vnd.github+json", "User-Agent": "awesome-ai-feature-testing/refresh"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    req = Request(f"https://api.github.com{path}", headers=headers)
    try:
        with urlopen(req, timeout=15) as rsp:
            import json
            return json.loads(rsp.read().decode("utf-8"))
    except HTTPError as e:
        if e.code in (403, 429):
            print(f"  rate-limited at {path}; sleeping 30s")
            time.sleep(30)
            return gh_get(path, token)
        if e.code == 404:
            return None
        print(f"  HTTP {e.code} on {path}: {e.reason}")
        return None
    except URLError as e:
        print(f"  network error on {path}: {e}")
        return None


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="Report drift; do not write")
    args = parser.parse_args()

    token = os.environ.get("GITHUB_TOKEN")
    if not token:
        print("warning: GITHUB_TOKEN not set; rate limit will be 60 req/h")

    rows: list[dict] = []
    with TOOLS_CSV.open(newline="", encoding="utf-8") as fp:
        reader = csv.DictReader(fp)
        for row in reader:
            rows.append(row)

    fieldnames = list(rows[0].keys())
    for f in ("stars", "last_pushed", "archived", "fetched_at"):
        if f not in fieldnames:
            fieldnames.append(f)

    drift = 0
    for row in rows:
        repo = gh_repo_from_url(row.get("url", ""))
        if not repo:
            continue
        print(f"{row['tool_id']:>26}  {repo}")
        info = gh_get(f"/repos/{repo}", token)
        if not info:
            continue
        new_stars = str(info.get("stargazers_count", ""))
        new_pushed = info.get("pushed_at", "") or ""
        new_archived = "true" if info.get("archived") else "false"

        if row.get("stars") != new_stars or row.get("last_pushed") != new_pushed or row.get("archived") != new_archived:
            drift += 1

        row["stars"] = new_stars
        row["last_pushed"] = new_pushed
        row["archived"] = new_archived
        row["fetched_at"] = datetime.now(timezone.utc).isoformat(timespec="seconds")

        time.sleep(0.2)  # be polite to the API

    if args.check:
        print(f"\nDrift detected on {drift} of {len(rows)} rows.")
        return 1 if drift else 0

    with TOOLS_CSV.open("w", newline="", encoding="utf-8") as fp:
        writer = csv.DictWriter(fp, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"\nRefreshed {len(rows)} rows; drift on {drift}.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
