"""
check_links.py — Verify all markdown links in the repo resolve.

Walks all *.md files; collects http(s) links; HEADs each (falls back to GET).
Reports broken links with file + line context. Exits non-zero on any failure.

Usage:
    python scripts/check_links.py
"""

from __future__ import annotations

import re
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parent.parent

MD_LINK_RE = re.compile(r"\[[^\]]*\]\((https?://[^)\s]+)\)")
SKIP_PREFIXES = ("https://img.shields.io",)


def collect_links() -> list[tuple[Path, int, str]]:
    out: list[tuple[Path, int, str]] = []
    for md in ROOT.rglob("*.md"):
        if any(part.startswith(".") for part in md.relative_to(ROOT).parts):
            continue
        if "node_modules" in md.parts or "site" in md.parts:
            continue
        for i, line in enumerate(md.read_text(encoding="utf-8", errors="ignore").splitlines(), start=1):
            for m in MD_LINK_RE.finditer(line):
                url = m.group(1).rstrip(".,);")
                if url.startswith(SKIP_PREFIXES):
                    continue
                out.append((md, i, url))
    return out


def head(url: str) -> int:
    req = Request(url, method="HEAD", headers={"User-Agent": "awesome-ai-feature-testing/link-check"})
    try:
        with urlopen(req, timeout=10) as rsp:
            return rsp.status
    except HTTPError as e:
        if e.code in (405, 403):
            req2 = Request(url, headers={"User-Agent": "awesome-ai-feature-testing/link-check"})
            try:
                with urlopen(req2, timeout=10) as rsp:
                    return rsp.status
            except (HTTPError, URLError):
                return e.code
        return e.code
    except URLError:
        return 0


def main() -> int:
    links = collect_links()
    print(f"Checking {len(links)} unique links across the repo.")

    seen: dict[str, int] = {}
    failures: list[tuple[Path, int, str, int]] = []

    urls = {url for _, _, url in links}
    with ThreadPoolExecutor(max_workers=16) as ex:
        futures = {ex.submit(head, u): u for u in urls}
        for fut in as_completed(futures):
            u = futures[fut]
            status = fut.result()
            seen[u] = status

    for path, line, url in links:
        status = seen.get(url, 0)
        if status >= 400 or status == 0:
            failures.append((path, line, url, status))

    if failures:
        print()
        print("BROKEN LINKS")
        for path, line, url, status in failures:
            rel = path.relative_to(ROOT)
            print(f"  {rel}:{line}  [{status or 'connection-error'}]  {url}")
        return 1

    print("All links resolved.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
