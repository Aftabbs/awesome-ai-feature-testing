"""
propose_pr.py — Convert an issue using the 'add a tool' template into a PR-ready
diff against `data/tools.csv`. Run by `.github/workflows/propose-pr.yml` whenever
a new issue with the `add-tool` label is filed.

The workflow then either opens a draft PR (if maintainer approval) or comments
the proposed CSV diff on the issue for review.
"""

from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TOOLS_CSV = ROOT / "data" / "tools.csv"


FIELDS = ["tool_id", "name", "url", "categories", "license", "description"]


def parse_issue_body(body: str) -> dict[str, str]:
    """Issues are expected to use the markdown form template:
    ## Tool name: ...
    ## URL: ...
    ## Categories: chatbot, rag, ...
    ## License: MIT
    ## Description: ...

    Parser is permissive — accepts headers in any order.
    """
    out: dict[str, str] = {}
    for header_re, key in [
        (r"^##\s*Tool\s*name\s*:?\s*(.+)$", "name"),
        (r"^##\s*URL\s*:?\s*(.+)$", "url"),
        (r"^##\s*Categories\s*:?\s*(.+)$", "categories"),
        (r"^##\s*License\s*:?\s*(.+)$", "license"),
        (r"^##\s*Description\s*:?\s*(.+)$", "description"),
    ]:
        m = re.search(header_re, body, flags=re.MULTILINE | re.IGNORECASE)
        if m:
            out[key] = m.group(1).strip()
    return out


def slugify(name: str) -> str:
    s = re.sub(r"[^a-zA-Z0-9]+", "-", name).strip("-").lower()
    return s


def existing_tool_ids() -> set[str]:
    with TOOLS_CSV.open(encoding="utf-8") as fp:
        return {row["tool_id"] for row in csv.DictReader(fp)}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--issue-json", required=True, help="Path to JSON file containing the issue {title, body}")
    parser.add_argument("--out", required=True, help="Path to write the proposed CSV row JSON")
    args = parser.parse_args()

    payload = json.loads(Path(args.issue_json).read_text(encoding="utf-8"))
    parsed = parse_issue_body(payload.get("body") or "")

    if "name" not in parsed:
        print("Issue body missing 'Tool name' header; can't propose a row.")
        return 1

    tool_id = slugify(parsed["name"])
    existing = existing_tool_ids()
    if tool_id in existing:
        print(f"tool_id '{tool_id}' already exists; reject duplicate.")
        return 1

    row = {
        "tool_id": tool_id,
        "name": parsed.get("name", ""),
        "url": parsed.get("url", ""),
        "categories": parsed.get("categories", ""),
        "license": parsed.get("license", ""),
        "description": parsed.get("description", ""),
    }

    Path(args.out).write_text(json.dumps(row, indent=2), encoding="utf-8")
    print(f"Proposed row written to {args.out}")
    print(json.dumps(row, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
