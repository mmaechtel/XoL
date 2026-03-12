# CLAUDE.md

Guidance for Claude Code when working in this repository.

## Wichtige Befehle

- **Dev-Server:** `mkdocs serve` (oder `./serve_dev.sh`)
- **Site bauen:** `mkdocs build` (Output: `site/`)
- **Deploy:** `./update_emvisio.sh <hostname>` — Dry Run mit `--dry`
- **RSS generieren:** `python scripts/generate_rss.py`
- **Python-Abhängigkeiten:** `pip install -r requirements.txt`

## Architektur

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
- **Auf das Wesentliche komprimieren:** Pro Datumsblock nur das Neue hervorheben (neue Seiten, neue Abschnitte, größere Erweiterungen). Kleine Änderungen wie Link-Korrekturen, Faktencheck-Anpassungen, Formatierung oder inhaltliche Feinarbeit nicht einzeln aufführen — sie sind Teil der Hauptänderung
- `index.md` wird immer zuletzt geändert (nach allen anderen Dateien)

### Video-Struktur

- `docs/assets/video/` ist ein **Symlink** auf ein NFS/SMB-Share (nicht im Git-Repo)
    - Linux: `/mnt/videos/XoL/video` (Share muss gemountet sein)
    - macOS: Pfad wird separat konfiguriert
- `de/` — deutsche Videos (nur in `docs/de/` verlinkt), `en/` — englische Videos (nur in `docs/en/` verlinkt)
- Keine Kreuz-Verlinkung zwischen Sprachen
- Videos werden **nicht** ins Git-Repo committed — neue Videos direkt auf dem Share ablegen

---

## Inhaltliche Regeln

- **EN first:** Alle Analyse, Recherche und Bearbeitung beginnt mit der EN-Version. DE wird anschließend angeglichen. Details in `SKILL_RULES.md`.
- **Quellenaktualität:** Nur Quellen ab 2024 aufwärts. Ältere nur bei nachweislich stabiler Information (Kernel-Docs, POSIX-Standards).
- **Nur Linux-Spezifika:** Plattformunabhängige X-Plane-Einstellungen nicht dokumentieren
- **Versionsnummern minimieren:** Entscheidungsbaum in `research/AUDIT_FLOW.md`. Kurzregel: Harte Mindestanforderungen behalten, illustrative Versionen entfernen. Akademische `??? abstract`-Blöcke sind ausgenommen.
- **Quellenabschnitt** am Seitenende: nur offizielle, belastbare Quellen (max 5-8)
- **Anredekonvention DE:** Unpersönlicher Stil (Infinitiv, Passiv, „lassen sich") statt „Sie"-Anrede. EN bleibt unverändert.
- **Freigegebene Quellen/Domains:** siehe `SKILL_RULES.md` + `.claude/settings.local.json`

## Git-Regeln

- Alles unter `research/` immer mitcommiten
- `.claude/*` ist in `.gitignore`, aber `!.claude/commands/` ist ausgenommen — Commands werden committed
- `site/` ist in `.gitignore` (Build-Output)

## Workflow & Research

- **Dokumentations-Workflow** (5 Phasen): Themen-Status in `TODO.md`, Prozessdetails in den jeweiligen Skills
- **Research-Kategorien:** Zuordnung Docs ↔ Research in `research/INDEX.md`
