#!/usr/bin/env python3
"""Generate llms.txt from the EN navigation in mkdocs.yml and page frontmatter.

Usage (from repo root):  python3 scripts/generate_llms.py [--check]

--check  verifies every generated URL against site/ (run after `mkdocs build`)
"""
import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
MKDOCS = ROOT / "mkdocs.yml"
DOCS = ROOT / "docs"
OUT = ROOT / "llms.txt"

HEADER = """# XoL — X-Plane on Linux

> Comprehensive documentation for running and optimizing X-Plane 12 on Linux. Covers system tuning, GPU drivers, display server selection, scenery management, ATC procedures, and a catalog of Linux-compatible addons and plugins.

- Website: https://xol.emvisio.de/
- Languages: English, German
- License: CC BY 4.0
- Source: https://github.com/mmaechtel/XoL
"""


class Loader(yaml.SafeLoader):
    """SafeLoader that ignores mkdocs-specific tags (!ENV, !!python/name:...)."""


Loader.add_multi_constructor("!", lambda loader, suffix, node: None)
Loader.add_multi_constructor("tag:yaml.org,2002:python/", lambda loader, suffix, node: None)


def load_config():
    with MKDOCS.open(encoding="utf-8") as fh:
        cfg = yaml.load(fh, Loader=Loader)
    site_url = cfg["site_url"].rstrip("/") + "/"
    i18n = next(p["i18n"] for p in cfg["plugins"] if isinstance(p, dict) and "i18n" in p)
    en = next(lang for lang in i18n["languages"] if lang["locale"] == "en")
    return site_url, en["nav"]


def frontmatter(md_path):
    text = md_path.read_text(encoding="utf-8")
    meta = {}
    m = re.match(r"---\n(.*?)\n---\n", text, re.S)
    if m:
        meta = yaml.safe_load(m.group(1)) or {}
    if "title" not in meta:
        h1 = re.search(r"^# (.+)$", text, re.M)
        raw = h1.group(1).strip() if h1 else md_path.stem
        meta["title"] = re.sub(r"[*_`]", "", raw)
    return meta


def page_line(site_url, rel_md, label=None):
    if not rel_md.endswith(".md") or "://" in rel_md:
        return None, None  # external link or anchor — not a page
    md_path = DOCS / rel_md
    meta = frontmatter(md_path)
    title = label or meta["title"]
    desc = (meta.get("description") or "").strip()
    url = site_url + rel_md[:-3] + ".html"
    return f"- [{title}]({url}): {desc}" if desc else f"- [{title}]({url})", url


def walk(items, site_url, depth, out, urls):
    """items: list of str | {label: str} | {label: [..]}"""
    for item in items:
        if isinstance(item, str):
            line, url = page_line(site_url, item)
            if line:
                out.append(line)
                urls.append(url)
            continue
        (label, value), = item.items()
        if isinstance(value, str):
            line, url = page_line(site_url, value, label)
            if line:
                out.append(line)
                urls.append(url)
        else:
            out.append("")
            out.append(f"{'#' * min(depth, 6)} {label}")
            out.append("")
            walk(value, site_url, depth + 1, out, urls)


def generate():
    site_url, nav = load_config()
    out, urls = [HEADER], []
    walk(nav, site_url, 2, out, urls)
    listed = {u[len(site_url):-5] + ".md" for u in urls}
    extra = sorted(
        str(p.relative_to(DOCS)) for p in (DOCS / "en").rglob("*.md")
        if str(p.relative_to(DOCS)) not in listed
    )
    if extra:
        out += ["", "## Other pages", ""]
        for rel_md in extra:
            line, url = page_line(site_url, rel_md)
            out.append(line)
            urls.append(url)
    text = "\n".join(out).rstrip("\n") + "\n"
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text, urls


def check(urls, site_url):
    site = ROOT / "site"
    missing = [u for u in urls if not (site / u[len(site_url):]).exists()]
    for u in missing:
        print(f"MISSING in site/: {u}", file=sys.stderr)
    print(f"{len(urls) - len(missing)}/{len(urls)} URLs found in site/")
    return not missing


def main():
    text, urls = generate()
    if "--check" in sys.argv:
        site_url, _ = load_config()
        if not check(urls, site_url):
            sys.exit("llms.txt not written — build site/ first (mkdocs build)")
    OUT.write_text(text, encoding="utf-8")
    print(f"wrote {OUT.relative_to(ROOT)} with {len(urls)} pages")


if __name__ == "__main__":
    main()
