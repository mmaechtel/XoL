# CLAUDE.md

Guidance for Claude Code when working in this repository.

## Project Overview

XoL (X-Plane on Linux) is a bilingual (German/English) documentation site for running X-Plane 12 on Linux. Built with MkDocs Material, hosted at https://emvisio.com/. No application code — only documentation content and build tooling.

## Key Commands

- **Dev server:** `mkdocs serve` (or `./serve_dev.sh`)
- **Build site:** `mkdocs build` (outputs to `site/`)
- **Deploy:** `./update_emvisio.sh <hostname>` — dry run with `--dry`
- **Generate RSS:** `python scripts/generate_rss.py`
- **Python:** via `pyenv` — die `.python-version` im Repo-Root erzwingt automatisch die richtige Version

### Pip-Abhängigkeiten

Folgende Module müssen installiert sein (`pip install`):

```
mkdocs
mkdocs-material
mkdocs-material-extensions
mkdocs-static-i18n
mkdocs-git-revision-date-localized-plugin
mkdocs-publisher
pymdown-extensions
pillow
```

## Architecture

### Content Structure

- `docs/de/` — German (default), `docs/en/` — English
- Every page exists in both languages with identical filename
- i18n plugin (`mkdocs-static-i18n`) handles language switching

### Navigation

Defined in `mkdocs.yml` under `plugins > i18n > languages > nav`. Separate nav trees per locale — new pages must be added to **both**.

### Formatting

Rules in `docs/MARKDOWN_RULES.txt`: no colon at end of headings before lists, 4-space indent per level, blank line after every heading, consistent DE/EN formatting. Code blocks: `bash` for shell commands, `ini` for sysctl, no tag for kernel/GRUB parameters.

### Changelog

`docs/{lang}/index.md` — "Letzte Änderungen" / "Recent Changes". New entries **above** old ones. Never delete history.

---

## Dokumentations-Workflow

Jedes neue oder überarbeitete Thema durchläuft vier Phasen. Der aktuelle Stand jedes Themas steht in `TODO.md`.

### Phase 1 — Recherche (`/research-topic`)

Skill startet mit Thema-Auswahl aus `TODO.md`, dann parallele Subagent-Recherche.

- Primärquellen: GitHub, offizielle Docs, Kernel-Docs, Arch Wiki
- Keine Foren, keine Drittanbieter-Blogposts
- Ergebnis: Research-Paper in `research/<kategorie>/<thema>.md`

### Phase 2 — Lektorat & Plan (`/research-topic`)

Gleicher Skill-Durchlauf, direkt nach der Recherche.

- Bestehende Doku analysieren, Plan erstellen
- Lektorat-Dokument: `research/<kategorie>/LEKTORAT_<thema>.md`
  - Bewertet Relevanz, Mehrwert, Haltbarkeit jeder Information
  - Kennzeichnet versionsspezifische Inhalte
  - Bewertet Quellen-Qualität
- Plan wird in `TODO.md` beim Thema festgehalten
- **Skill endet hier. Umsetzung erst nach User-Freigabe.**

### Phase 3 — Umsetzung (manuell)

Wird vom User explizit gestartet, nicht durch einen Skill.

- DE- und EN-Seiten schreiben (parallel, gleiche Struktur)
- Bestehende Seiten anpassen (Querverweise, Glossar)
- `mkdocs.yml` Navigation aktualisieren (beide Sprachbäume)
- `docs/{lang}/index.md` Changelog ergänzen
- `mkdocs build` zur Prüfung

### Phase 4 — Faktencheck (`/faktencheck`)

Eigener Skill, wird nach der Umsetzung aufgerufen.

- EN-Seite als Prüfgrundlage (Quellen sind englisch)
- Parallele Verifikation aller Behauptungen gegen Primärquellen
- Korrekturen in DE + EN
- Versionsspezifika bereinigen (Meta-Formulierungen statt Versionsnummern)
- Quellenabschnitt am Seitenende ergänzen
- URL-Analyse der freigegebenen Domains

### Phase 5 — Content Audit (`/audit`)

Systematische Nachprüfung bestehender EN-Seiten. Arbeitsplan: `research/AUDIT_FLOW.md`.

- 27 Kapitel in 5 Runden, EN first, DE-Angleichung nach jeder Runde
- Jedes Kapitel: Deep Analysis → Expert Review → User-Review → Korrekturen
- Audit-Output pro Kapitel: `research/<kategorie>/AUDIT_<dateiname>.md`
- 4 Prüfdimensionen: FAK (Fakten), AKT (Aktualität/Haltbarkeit), REL (Relevanz), DET (Detailgrad)
- Quellenaktualität nach Typ differenziert (nicht pauschal), Versionsnummern nach Entscheidungsbaum
- Referenzplattform: Debian Stable/Testing
- **Startbefehl:** `Audit <dateiname> gemäß research/AUDIT_FLOW.md`

### Status-Modell

Jedes Thema in `TODO.md` hat einen Status:

| Status | Bedeutung | Nächster Schritt |
|--------|-----------|------------------|
| `offen` | Noch nicht begonnen | `/research-topic` |
| `recherchiert` | Research-Paper liegt vor | Lektorat (Teil von `/research-topic`) |
| `geplant` | Lektorat + Plan fertig | Phase 3 nach User-Freigabe |
| `umgesetzt` | DE + EN geschrieben | `/faktencheck` |
| `geprüft` | Faktencheck abgeschlossen | Commit + fertig |

---

## Dateistruktur

| Pfad | Zweck |
|------|-------|
| `TODO.md` | Themen-Backlog mit Status. Nur **was** und **wo stehen wir**. |
| `research/<kategorie>/` | Research-Papers nach Thema (siehe `research/INDEX.md`) |
| `research/<kategorie>/LEKTORAT_<thema>.md` | Redaktionelle Bewertung (Brücke Recherche → Umsetzung) |
| `research/INDEX.md` | Thematischer Index aller Research-Dokumente |
| `research/AUDIT_FLOW.md` | Content-Audit Prozess (Flow, Template, Regeln, QS) |
| `research/AUDIT_STATUS.md` | Audit-Fortschritt + Zyklushistorie (lebende Datei) |
| `research/<kat>/AUDIT_<datei>.md` | Audit-Ergebnisse pro Kapitel |
| `docs/MARKDOWN_RULES.txt` | Formatierungsregeln |
| `.claude/skills/` | Skill-Definitionen (nicht committed, `.gitignore`) |
| `.claude/settings.local.json` | Freigegebene WebFetch-Domains |

---

## Skills

| Skill | Phase | Beschreibung |
|-------|-------|-------------|
| `/research-topic` | 1 + 2 | Recherche, Lektorat, Plan. Startet NICHT die Umsetzung. |
| `/faktencheck` | 4 | Faktenprüfung gegen Primärquellen, Korrekturen, Quellenabschnitt. |
| `/abschluss` | alle | Changelog in `index.md` (DE + EN) aktualisieren und Git-Commit erstellen. |
| `/audit` | 5 | Content Audit einer EN-Seite gemäß `research/AUDIT_FLOW.md`. |

---

## Inhaltliche Regeln

- **Nur Linux-Spezifika:** Plattformunabhängige X-Plane-Einstellungen nicht dokumentieren
- **Versionsnummern minimieren:** Entscheidungsbaum in `research/AUDIT_FLOW.md` → Abschnitt "Versionsnummern". Kurzregel: Harte Mindestanforderungen und Verhaltens-Grenzen behalten, illustrative Versionen entfernen, Tabellen sind OK. Im Zweifel: Meta-Formulierung + Verifikationsbefehl.
- **Ausnahme:** Akademische Hintergrund-Blöcke (`??? abstract`) dürfen Versionsdetails enthalten
- **Quellenabschnitt** am Seitenende: nur offizielle, belastbare Quellen (max 5-8)

## Freigegebene Quellen

Domains in `.claude/settings.local.json` — nutzbar ohne Rückfrage:

- **Linux/Kernel:** docs.kernel.org, wiki.archlinux.org, lwn.net
- **Debian:** wiki.debian.org, packages.debian.org, manpages.debian.org
- **Grafik/Vulkan:** docs.mesa3d.org, vulkan.org, registry.khronos.org
- **Desktop:** freedesktop.org, pipewire.org
- **X-Plane:** www.x-plane.com, developer.x-plane.com
- **Projekte:** github.com, liquorix.net, xearthlayer.app
- **Suche:** WebSearch (unbeschränkt)
