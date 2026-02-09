# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

XoL (X-Plane on Linux) is a bilingual (German/English) documentation site for running X-Plane 12 on Linux. Built with MkDocs Material and hosted at https://emvisio.com/. The repo is the source for the entire site — there is no application code, just documentation content and build tooling.

## Key Commands

- **Dev server:** `mkdocs serve` (or `./serve_dev.sh` which also copies VATSIM routes)
- **Build site:** `mkdocs build` (outputs to `site/`)
- **Deploy:** `./update_emvisio.sh <hostname>` (rsync to remote) — dry run with `--dry` flag
- **Generate RSS:** `python scripts/generate_rss.py`

Python version: 3.12.8 (see `.python-version`)

## Architecture

### Content Structure

All documentation lives in `docs/` with parallel language folders:
- `docs/de/` — German (default language)
- `docs/en/` — English

Every content page exists in both `de/` and `en/` with the same filename. The i18n plugin (`mkdocs-pub-plugins` i18n) handles language switching using `docs_structure: folder`.

### Navigation

Navigation is defined entirely in `mkdocs.yml` under `plugins > i18n > languages > nav` — there are separate nav trees for each locale. When adding a new page, it must be added to **both** nav trees in `mkdocs.yml`.

### Plugins

The site uses these MkDocs plugins (configured in `mkdocs.yml`):
- **pub-blog** — blog functionality (posts in `docs/{lang}/blog/`)
- **pub-obsidian** — Obsidian compatibility (backlinks disabled)
- **i18n** — multi-language support with folder-based docs structure
- **git-revision-date-localized** — last-updated dates from git history

### Static Files

- `maps.html` / `Maps.html` — redirect pages copied into `site/` during deploy
- `vatsim_routes.html` — generated externally (from `ATC-Bookings` project), copied in during dev/deploy
- Blog images stored in `docs/assets/images/blog/`

### Markdown Extensions

Content uses Material for MkDocs extensions: admonitions, code highlighting with copy buttons, tabbed content, task lists, Mermaid diagrams, and emoji support. See `markdown_extensions` in `mkdocs.yml` for the full list.

### Formatting Rules

Markdown formatting rules are defined in `docs/MARKDOWN_RULES.txt`. Key points: no colon at end of headings before lists, list indentation in 4-space steps, blank line after every heading before a list, space after colons, consistent formatting across DE/EN.

### Research Sources

`research/` contains background papers used as source material for documentation pages. These are **not** published on the site — they serve as structured knowledge base for deriving documentation content (e.g., the systemtuning page was derived from two latency research papers).

### Changelog Convention

`docs/{lang}/index.md` contains a "Letzte Änderungen" / "Recent Changes" section. New entries are added **above** existing ones under the current date heading. Old entries are preserved as a running history.
