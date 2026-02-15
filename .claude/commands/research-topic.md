# Research Topic

Recherchiert ein Thema aus `TODO.md` und erstellt Research-Paper + Lektorat. Deckt Phase 1 (Recherche) und Phase 2 (Lektorat & Plan) des Dokumentations-Workflows ab. Startet NICHT die Umsetzung.

## Argumente

`$ARGUMENTS`: Thema-Keyword oder Dateiname aus `TODO.md`

| Aufruf | Beschreibung |
|--------|-------------|
| `/research-topic mesa` | Recherchiert das Thema Mesa/AMD-Grafiktreiber |
| `/research-topic input_devices.md` | Recherchiert Eingabegeraete unter Linux |
| `/research-topic` | Ohne Argument: TODO.md oeffnen und Thema vorschlagen |

---

## Pre-Flight

| Voraussetzung | Pruefung | Schwere |
|---------------|---------|---------|
| Argument gesetzt oder TODO.md vorhanden | `$ARGUMENTS` oder `TODO.md` lesbar | Blocker |
| Thema in TODO.md identifizierbar | Keyword matcht einen Eintrag | Blocker |
| Thema noch nicht abgeschlossen | Status ist `offen` oder `recherchiert` | Warnung |
| Research-Verzeichnis existiert | `research/<kategorie>/` existiert (sonst anlegen) | Auto-fix |

Bei Blocker: Fehlermeldung ausgeben und abbrechen.

---

## Phase 1 — Thema aufloesen

### 1.1 TODO.md lesen

```
Read: TODO.md
```

1. Thema-Keyword gegen Eintraege in `TODO.md` matchen
2. Status pruefen: `offen` → voller Durchlauf (Phase 2 + 3). `recherchiert` → nur Phase 3 (Lektorat). `geplant` oder hoeher → Warnung ausgeben
3. Falls kein Argument: Die naechsten 3 offenen Themen nach Prioritaet vorschlagen (AskUserQuestion)

### 1.2 Bestehende Dokumentation lesen

Falls bereits eine Seite unter `docs/en/` existiert:

```
Read: docs/en/<dateiname>.md
Read: docs/de/<dateiname>.md
```

Bestehenden Inhalt als Ausgangsbasis fuer die Recherche erfassen.

### 1.3 Bestehende Research-Papers lesen

```
Glob: research/**/*<thema>*.md
```

Falls bereits Papers existieren: Lesen und als Basis verwenden, nicht duplizieren.

---

## Phase 2 — Recherche (parallele Subagents)

### 2.1 Quellenstrategie

Primaerquellen in Reihenfolge der Zuverlaessigkeit:

1. **Offizielle Projektdokumentation** (kernel.org, mesa3d.org, developer.x-plane.com)
2. **GitHub-Repositories** (READMEs, Changelogs, Issues, Commit-Messages)
3. **Arch Wiki** (umfassendste Linux-Dokumentation)
4. **Debian-spezifisch** (wiki.debian.org, packages.debian.org, manpages.debian.org)
5. **Man-Pages** (man7.org)

**Nicht verwenden:** Foren-Posts, Drittanbieter-Blogposts, YouTube-Transkripte, ChatGPT-generierte Inhalte.

**Quellenaktualitaet:** Nur Quellen ab 2024 aufwaerts. Aeltere nur bei nachweislich stabiler Information (Kernel-Docs, POSIX-Standards).

### 2.2 Parallele Recherche-Subagents

**2-3 Subagents** starten (Task-Tool mit subagent_type=general-purpose), aufgeteilt nach Themenblöcken:

- **Agent A — Technische Grundlagen:** Architektur, Spezifikationen, Debian-Aspekte
- **Agent B — Praxis und X-Plane:** Konfiguration, Kompatibilitaet, Diagnose
- **Agent C (optional):** Hardware-Unterschiede, Performance, Alternativen

Jeder Subagent:

- WebSearch fuer aktuelle Informationen
- WebFetch fuer freigegebene Domains (siehe `.claude/settings.local.json`)
- Liefert: Fakten, Konfigurationsbeispiele, Befehle, Quellen-URLs

### 2.3 Research-Paper schreiben

**Datei:** `research/<kategorie>/<thema>.md`

**Struktur:**

```markdown
# <Thema> — Research Paper

**Datum:** YYYY-MM-DD
**Quellen:** <Anzahl> Primaerquellen verifiziert
**Zielseite:** `docs/en/<dateiname>.md`

---

## Zusammenfassung

<3-5 Saetze: Was wurde recherchiert, was sind die Kernerkenntnisse?>

## <Unterthema 1>

<Fakten, Konfiguration, Befehle. Jede Behauptung mit Quelle belegt.>

## <Unterthema N>

...

## Quellen

| # | Quelle | Domain | Datum | Relevanz |
|---|--------|--------|-------|----------|
| 1 | <Titel> | <domain> | YYYY-MM | HOCH/MITTEL |
```

### 2.4 INDEX.md aktualisieren

```
Read: research/INDEX.md
```

Neues Paper in den passenden Kategorie-Abschnitt eintragen:

```markdown
- <kategorie>/<dateiname>.md -> <zielseite>.md
```

### 2.5 Status aktualisieren

In `TODO.md` den Status des Themas auf `recherchiert` setzen.

---

## Phase 3 — Lektorat

### 3.1 Bestehende Doku analysieren

Falls eine Seite bereits existiert:

- Welche Abschnitte sind bereits vorhanden?
- Was ist korrekt, was veraltet, was fehlt?
- Welche Querverweise existieren?

### 3.2 Lektorat-Dokument schreiben

**Datei:** `research/<kategorie>/LEKTORAT_<thema>.md`

**Struktur:**

```markdown
# Lektorat: <dateiname>.md — Redaktionelle Empfehlungen

Dieses Dokument ist das Briefing fuer die Umsetzung (Phase 3).

---

## Zielgruppe und Leitfrage

**Leser:** Linux-Nutzer mit X-Plane-Erfahrung, grundlegende Linux-Kenntnisse.
**Leitfrage:** Wuerde ein Linux-Nutzer das selbst herausfinden? Wenn ja → weglassen.

---

## Abschnitt-fuer-Abschnitt-Bewertung

### <Abschnitt>

**Empfehlung:** UEBERNEHMEN / KURZ HALTEN / WEGLASSEN

| Unterthema | Mehrwert? | Empfehlung |
|------------|-----------|------------|
| ... | HOCH/MITTEL/GERING | Konkrete Handlungsempfehlung |

**Redaktionelle Entscheidung:** <Begruendung>
```

Jedes Unterthema wird bewertet auf:

- **Relevanz:** Linux-spezifisch? Oder plattformunabhaengig?
- **Mehrwert:** Findet der Leser das woanders? Oder ist das unser Alleinstellungsmerkmal?
- **Haltbarkeit:** Wird das beim naechsten Release veralten? Versionsnummern nach Entscheidungsbaum.
- **Quellen-Qualitaet:** Primaerquelle oder Hoerensagen?

### 3.3 Plan in TODO.md festhalten

Den Eintrag in `TODO.md` aktualisieren:

- Status: `offen` → `geplant`
- Gliederung der geplanten Seite eintragen
- Research-Paper und Lektorat verlinken

---

## Phase 4 — Ergebnisse vorlegen

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
RESEARCH TOPIC: <Thema>
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

RECHERCHE:
├─ Subagents:       <Anzahl>
├─ Quellen gesamt:  <Anzahl>
├─ Quellen HOCH:    <Anzahl>
└─ Research-Paper:  research/<kat>/<datei>.md

LEKTORAT:
├─ Abschnitte bewertet: <Anzahl>
├─ UEBERNEHMEN:         <Anzahl>
├─ KURZ HALTEN:         <Anzahl>
├─ WEGLASSEN:           <Anzahl>
└─ Lektorat-Datei:      research/<kat>/LEKTORAT_<datei>.md

PLAN:
├─ Zielseite:  docs/en/<datei>.md
├─ Status:     geplant
└─ TODO.md:    aktualisiert

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**SKILL ENDET HIER.** Umsetzung erst nach expliziter User-Freigabe.

---

## Hinweise

- **Keine Umsetzung:** Dieser Skill schreibt keine Dokumentationsseiten. Er liefert nur die Grundlage.
- **EN first:** Research-Paper in Deutsch, aber EN-Quellen bevorzugen
- **Keine Foren/Blogs:** Nur Primaerquellen (offizielle Docs, GitHub, Kernel-Docs, Arch Wiki)
- **Quellenaktualitaet:** Nur ab 2024, aeltere nur bei stabiler Information
- **Versionsnummern:** Entscheidungsbaum in `research/AUDIT_FLOW.md` beachten
- **INDEX.md pflegen:** Jedes neue Paper muss im Index eingetragen werden
- **Kein Commit:** Der Commit erfolgt ueber `/abschluss`
