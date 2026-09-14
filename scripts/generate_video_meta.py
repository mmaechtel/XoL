#!/usr/bin/env python3
"""Collect VideoObject metadata for the videos pages.

Runs LOCALLY with the video share mounted (docs/assets/video -> share).
Reads the video cards from docs/{de,en}/videos.md, probes each MP4 with
ffprobe (duration), takes the upload date from the file mtime and writes
scripts/video_meta.json. Existing descriptions in that JSON are preserved,
so the file can be regenerated after adding videos without losing the
hand-written texts.

Usage (from repo root):  python3 scripts/generate_video_meta.py
"""
import json
import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
OUT = ROOT / "scripts" / "video_meta.json"
LANGS = ("de", "en")

CARD_SPLIT = '<div class="video-card"'
NAME = re.compile(r"^### (?P<name>.+)$", re.M)
POSTER = re.compile(r'poster="(?P<poster>[^"]+)"')
SRC = re.compile(r'<source src="(?P<src>[^"]+)"')


def probe_duration(path):
    res = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=nw=1:nk=1", str(path)],
        capture_output=True, text=True, check=True, timeout=60,
    )
    total = int(round(float(res.stdout.strip())))
    h, rem = divmod(total, 3600)
    m, s = divmod(rem, 60)
    return f"PT{h}H{m}M{s}S" if h else f"PT{m}M{s}S"


def site_path(rel_from_videos_md):
    """'../assets/video/en/X/X.mp4' -> 'assets/video/en/X/X.mp4' (URL-quoted)."""
    clean = rel_from_videos_md.removeprefix("../")
    return quote(clean, safe="/")


def _upload_datum(dt):
    """Mitternacht Ortszeit als ISO 8601 mit Zeitzonen-Offset.

    Google lehnt uploadDate ohne Offset ab (Search Console: "Zeitzone in
    Datum/Uhrzeit-Attribut 'uploadDate' fehlt")."""
    lokal = dt.astimezone().tzinfo
    return dt.replace(hour=0, minute=0, second=0, microsecond=0, tzinfo=lokal).isoformat()


def _mit_zeitzone(wert):
    """Alte Nur-Datum-Werte auf das volle Format heben, neue unveraendert lassen."""
    if not wert:
        return None
    if len(wert) == 10:
        return _upload_datum(datetime.fromisoformat(wert))
    return wert


def main():
    old = json.loads(OUT.read_text(encoding="utf-8")) if OUT.exists() else {}
    result = {}
    for lang in LANGS:
        md = (DOCS / lang / "videos.md").read_text(encoding="utf-8")
        previous = {v["contentUrl"]: v for v in old.get(lang, [])}
        cards = md.split(CARD_SPLIT)[1:]
        entries = []
        for card in cards:
            name, poster, src = NAME.search(card), POSTER.search(card), SRC.search(card)
            if not (name and poster and src):
                sys.exit(f"{lang}/videos.md: card without title/poster/source:\n{card[:200]}")
            src = src.group("src")
            mp4 = (DOCS / lang / src).resolve()
            if not mp4.exists():
                sys.exit(f"missing on share: {mp4}")
            content_url = site_path(src)
            prev = previous.get(content_url, {})
            mtime = _upload_datum(datetime.fromtimestamp(mp4.stat().st_mtime))
            entries.append({
                "name": name.group("name").strip(),
                "description": prev.get("description", ""),
                "contentUrl": content_url,
                "thumbnailUrl": site_path(poster.group("poster")),
                # first run: file mtime; later runs keep the recorded date stable
                "uploadDate": _mit_zeitzone(prev.get("uploadDate")) or mtime,
                "duration": probe_duration(mp4),
            })
        if len(entries) != md.count("<video "):
            sys.exit(f"{lang}/videos.md: parsed {len(entries)} cards but found {md.count('<video ')} <video> tags")
        result[lang] = entries
        print(f"{lang}: {len(entries)} videos")
    OUT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    empty = [f"{l}/{v['name']}" for l in LANGS for v in result[l] if not v["description"]]
    if empty:
        sys.exit("descriptions still empty (fill them in video_meta.json): " + ", ".join(empty))


if __name__ == "__main__":
    main()
