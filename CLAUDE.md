# CLAUDE.md

Guidance for Claude Code when working in this repository.

## Projektübersicht

XoL (X-Plane on Linux) ist eine bilinguale (Deutsch/Englisch) Dokumentationsseite für X-Plane 12 unter Linux. Gebaut mit MkDocs Material, gehostet auf https://emvisio.com/. Kein Applikationscode — nur Dokumentation und Build-Tooling.

## Wichtige Befehle

- **Dev-Server:** `mkdocs serve` (oder `./serve_dev.sh`)
- **Site bauen:** `mkdocs build` (Output: `site/`)
- **Deploy:** `./update_emvisio.sh <hostname>` — Dry Run mit `--dry`
- **RSS generieren:** `python scripts/generate_rss.py`
- **Python-Abhängigkeiten:** `pip install -r requirements.txt`

### Pip-Abhängigkeiten

Definiert in `requirements.txt`. Installation: `pip install -r requirements.txt`

## Architektur

### Inhaltsstruktur

- `docs/de/` — Deutsch (Standard), `docs/en/` — Englisch
- Jede Seite existiert in beiden Sprachen mit identischem Dateinamen
- i18n-Plugin (`mkdocs-static-i18n`) steuert die Sprachumschaltung

### Navigation

Definiert in `mkdocs.yml` unter `plugins > i18n > languages > nav`. Separate Navigationsbäume pro Sprache — neue Seiten müssen in **beide** eingetragen werden.

### Formatierung

**Pflicht:** Vor jeder Bearbeitung von `docs/`-Dateien `docs/MARKDOWN_RULES.txt` lesen und anwenden. Kernregeln:

- Leerzeile nach **jeder** Überschrift (auch `**Fett**`-Pseudo-Überschriften vor Listen)
- Kein Doppelpunkt am Ende von Überschriften, die mit einer Liste folgen
- Listen-Einrückung: 4 Spaces pro Ebene (0 → 4 → 8)
- Identische Formatierung in DE und EN
- Code-Blocks: `bash` für Shell-Befehle, `ini` für sysctl, kein Tag für Kernel/GRUB-Parameter

### Changelog-Regeln

`docs/{lang}/index.md` — "Letzte Änderungen" / "Recent Changes":

- Neue Einträge **über** alten (neuer Datumsblock `### YYYY-MM-DD` oben)
- Falls aktueller Tag bereits existiert: Einträge dort anfügen
- **Maximal 3 Datumsblöcke** behalten (die neuesten). Ältere Datumsblöcke komplett entfernen
- DE und EN müssen inhaltlich identisch (übersetzt) sein
- **Nur leser-relevante Content-Änderungen** — keine internen Repo-/Research-/Skill-/Config-Änderungen
- `index.md` wird immer zuletzt geändert (nach allen anderen Dateien)

### Video-Struktur

- `docs/assets/video/` ist ein **Symlink** auf ein NFS/SMB-Share (nicht im Git-Repo)
    - Linux: `/mnt/videos/XoL/video` (Share muss gemountet sein)
    - macOS: Pfad wird separat konfiguriert
- `de/` — deutsche Videos (nur in `docs/de/` verlinkt)
- `en/` — englische Videos (nur in `docs/en/` verlinkt)
- Keine Kreuz-Verlinkung zwischen Sprachen
- Videos werden **nicht** ins Git-Repo committed — neue Videos direkt auf dem Share ablegen
- `mkdocs build` löst den Symlink auf und kopiert die Dateien nach `site/`

---

## Dokumentations-Workflow

Jedes neue oder überarbeitete Thema durchläuft fünf Phasen. Der aktuelle Stand jedes Themas steht in `TODO.md`.

### Phase 1 — Recherche (`/research-topic`)

Skill startet mit Thema-Auswahl aus `TODO.md`, dann parallele Subagent-Recherche.

- Primärquellen: GitHub, offizielle Docs, Kernel-Docs, Arch Wiki
- Keine Foren, keine Drittanbieter-Blogposts
- Quellenaktualität: siehe [Inhaltliche Regeln](#inhaltliche-regeln)
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
- Quellenaktualität: siehe [Inhaltliche Regeln](#inhaltliche-regeln)
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
| `research/<kategorie>/` | Research-Papers nach Thema (Kategorien siehe unten) |
| `research/<kategorie>/LEKTORAT_<thema>.md` | Redaktionelle Bewertung (Brücke Recherche → Umsetzung) |
| `research/INDEX.md` | Thematischer Index aller Research-Dokumente |
| `research/AUDIT_FLOW.md` | Content-Audit Prozess (Flow, Template, Regeln, QS) |
| `research/AUDIT_STATUS.md` | Audit-Fortschritt + Zyklushistorie (lebende Datei) |
| `research/<kat>/AUDIT_<datei>.md` | Audit-Ergebnisse pro Kapitel |
| `research/glossar_check.log` | Glossar-Check Protokoll (Seite, Datum, Anzahl Änderungen) |
| `docs/MARKDOWN_RULES.txt` | Formatierungsregeln |
| `.claude/commands/` | Skill/Command-Definitionen (committed, von `.gitignore` ausgenommen) |
| `.claude/settings.local.json` | Permissions: Tool-Freigaben + WebFetch-Domain-Allowlist |

### Research-Kategorien

Zuordnung von Docs-Seiten zu `research/<kategorie>/`:

| Kategorie | Docs-Seiten |
|-----------|------------|
| `addons/` | `addon/*.md` |
| `audio/` | (Audio/PipeWire-Themen) |
| `display-server/` | `optimizations/displayserver.md`, `optimizations/displayserver_wayland.md`, `optimizations/displayserver_x11.md` |
| `performance_overview/` | `fundamentals/performance_overview.md` |
| `proton/` | `extensions/wine.md` |
| `systemtools/` | `system/systemtools.md` |
| `systemtuning/` | `system/systemtuning.md`, `system/index.md`, `optimizations/filesystem.md`, `optimizations/liquorix.md` |
| `szenerie/` | `scenery/scenery.md`, `scenery/scenery_components.md` |
| `xplane-config/` | `xplane/*.md` |
| `analyses/` | Querschnitts-Analysen (kein festes Docs-Mapping) |
| `notebooklm/` | NotebookLM-Skripte (Output von `/generate-notebooklm`) |

Bei neuen Themen: bestehende Kategorie verwenden oder neue anlegen. `research/INDEX.md` mitpflegen.

---

## Skills

### Commands (`.claude/commands/`)

| Skill | Phase | Beschreibung |
|-------|-------|-------------|
| `/research-topic` | 1 + 2 | Recherche, Lektorat, Plan. Startet NICHT die Umsetzung. |
| `/faktencheck` | 4 | Faktenprüfung gegen Primärquellen, Korrekturen, Quellenabschnitt. |
| `/audit` | 5 | Content Audit einer EN-Seite gemäß `research/AUDIT_FLOW.md`. |
| `/check-glossar` | nach Umsetzung | Glossar-Abdeckung prüfen, fehlende Verlinkungen ergänzen, Markdown-Check |
| `/embed-videos` | Umsetzung | MP4-Videos einbetten (Video-Seite + thematische Seiten), Poster generieren |
| `/generate-notebooklm` | nach Umsetzung | TTS-optimiertes Skript für Google NotebookLM Audio Overview erstellen |
| `/verify-commands` | nach Umsetzung | Dokumentierte Shell-Befehle interaktiv auf dem Debian-System testen |
| `/abschluss` | alle | Changelog in `index.md` (DE + EN) aktualisieren und Git-Commit erstellen |

---

## Inhaltliche Regeln

- **Quellenaktualität:** Nur Quellen ab 2024 aufwärts verwenden. Ältere Quellen nur, wenn keine aktuellere Alternative existiert und die Information nachweislich stabil ist (z.B. Kernel-Docs, POSIX-Standards).
- **Nur Linux-Spezifika:** Plattformunabhängige X-Plane-Einstellungen nicht dokumentieren
- **Versionsnummern minimieren:** Entscheidungsbaum in `research/AUDIT_FLOW.md` → Abschnitt "Versionsnummern". Kurzregel: Harte Mindestanforderungen und Verhaltens-Grenzen behalten, illustrative Versionen entfernen, Tabellen sind OK. Im Zweifel: Meta-Formulierung + Verifikationsbefehl.
- **Ausnahme:** Akademische Hintergrund-Blöcke (`??? abstract`) dürfen Versionsdetails enthalten
- **Quellenabschnitt** am Seitenende: nur offizielle, belastbare Quellen (max 5-8)
- **Anredekonvention DE:** Unpersönlicher Stil (Infinitiv, Passiv, „lassen sich") statt „Sie"-Anrede. Bereits umgestellt: `begin.md`, `docker.md`. Restliche Dateien schrittweise bei Gelegenheit umstellen. EN bleibt unverändert („you" ist stilistisch neutral).

## Git-Regeln

- Alles unter `research/` immer mitcommiten (Research-Papers, NotebookLM-Skripte, Audit-Dokumente)
- `.DS_Store` ist in `.gitignore`
- `.claude/*` ist in `.gitignore`, aber `!.claude/commands/` ist ausgenommen — Commands werden committed
- `site/` ist in `.gitignore` (Build-Output)

## Freigegebene Quellen

Domains in `.claude/settings.local.json` — nutzbar ohne Rückfrage:

- **Referenz:** en.wikipedia.org, de.wikipedia.org
- **Linux/Kernel:** docs.kernel.org, www.kernel.org, wiki.archlinux.org, lwn.net, man7.org, phoronix.com
- **Debian:** www.debian.org, wiki.debian.org, packages.debian.org, manpages.debian.org
- **Grafik/Vulkan:** docs.mesa3d.org, vulkan.org, registry.khronos.org
- **NVIDIA:** www.nvidia.com, download.nvidia.com, us.download.nvidia.com
- **Desktop/Wayland:** freedesktop.org, www.freedesktop.org, gitlab.freedesktop.org, pipewire.org, zamundaaa.github.io, davidjusto.com
- **X-Plane:** www.x-plane.com, developer.x-plane.com, forums.x-plane.org, store.steampowered.com
- **Projekte:** github.com, raw.githubusercontent.com, liquorix.net, xearthlayer.app, sourceforge.net
- **Flight Sim:** www.aiflygo.com, flightsimcoach.com, letsflyvfr.com, defkey.com
- **Suche:** WebSearch (unbeschränkt)
