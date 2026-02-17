#!/usr/bin/env python3
"""Check all relative markdown links in docs/ for broken targets."""

import re
import sys
from pathlib import Path

DOCS_DIR = Path(__file__).resolve().parent.parent / "docs"
LINK_RE = re.compile(r'\]\(([^)]+)\)')


def check_links():
    broken = []

    for md_file in sorted(DOCS_DIR.rglob("*.md")):
        for i, line in enumerate(md_file.read_text().splitlines(), 1):
            for match in LINK_RE.finditer(line):
                target = match.group(1)
                if target.startswith(("http", "#", "/", "mailto")):
                    continue
                path_part = target.split("#")[0]
                if not path_part:
                    continue
                resolved = (md_file.parent / path_part).resolve()
                if not resolved.exists():
                    rel_source = md_file.relative_to(DOCS_DIR)
                    broken.append(f"{rel_source}:{i} → {target}")

    if broken:
        print(f"Found {len(broken)} broken link(s):\n")
        for b in broken:
            print(f"  {b}")
        return 1
    else:
        print("All relative links OK.")
        return 0


if __name__ == "__main__":
    sys.exit(check_links())
