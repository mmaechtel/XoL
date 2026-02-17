# SEO Check

Prueft und ergaenzt SEO-relevante Metadaten fuer alle Dokumentationsseiten. Hauptaufgabe: fehlende `description`-Frontmatter generieren.

## Argumente

`<verzeichnis>`: Optionaler Verzeichnispfad relativ zu `docs/en/`. Ohne Argument: gesamte Doku.

| Aufruf | Beschreibung |
|--------|-------------|
| `/seo-check` | Prueft alle Seiten |
| `/seo-check linux/system` | Prueft nur `docs/en/linux/system/` |
| `/seo-check addon/cockpit` | Prueft nur `docs/en/addon/cockpit/` |

---

## Pre-Flight

| Voraussetzung | Pruefung | Schwere |
|---------------|---------|---------|
| Verzeichnis existiert | Falls angegeben, muss `docs/en/<verzeichnis>/` existieren | Blocker |
| robots.txt vorhanden | Datei `robots.txt` im Projekt-Root | Warnung |
| llms.txt vorhanden | Datei `llms.txt` im Projekt-Root | Warnung |

---

## Phase 1 — Bestandsaufnahme

### 1.1 Dateien erfassen

Alle `.md`-Dateien im Zielverzeichnis (oder gesamte `docs/en/`) auflisten. `index.md` Dateien MIT einschliessen (auch sie brauchen Descriptions).

### 1.2 Frontmatter pruefen

Jede EN-Datei lesen und klassifizieren:

**Fall A: description vorhanden und gut**

```yaml
---
description: Concise, unique description under 160 characters
---
```

Kriterien fuer "gut":
- Zwischen 50 und 160 Zeichen
- Nicht identisch mit dem Site-weiten Default
- Beschreibt den spezifischen Seiteninhalt

**Fall B: description vorhanden aber mangelhaft**

- Zu kurz (unter 50 Zeichen)
- Zu lang (ueber 160 Zeichen)
- Generisch / nicht seitenspezifisch

**Fall C: description fehlt**

Kein `description:`-Feld im Frontmatter, oder kein Frontmatter vorhanden.

---

## Phase 2 — Descriptions generieren

Fuer jede Datei in Fall B oder C:

### 2.1 Seite lesen und verstehen

- H1-Titel und H2-Abschnitte erfassen
- Kernthema in einem Satz zusammenfassen
- Zielgruppe beruecksichtigen (erfahrene Linux-User, X-Plane-Piloten)

### 2.2 Description formulieren

Regeln:
- **EN:** 120-155 Zeichen, beschreibt was der Leser auf der Seite findet
- **DE:** Sinngleich, nicht 1:1 Uebersetzung, gleicher Zeichenbereich
- Beginnt mit dem Kernthema, nicht mit "This page..." oder "Diese Seite..."
- Enthaelt 1-2 relevante Keywords natuerlich eingebaut
- Aktive Sprache, kein Marketing-Sprech

Beispiele:

```
EN: "CPU governor, IRQ affinity, kernel parameters, and vm.swappiness — practical tuning guide for low-latency X-Plane performance on Linux."
DE: "CPU-Governor, IRQ-Affinitaet, Kernel-Parameter und vm.swappiness — praktischer Tuning-Leitfaden fuer latenzarme X-Plane-Performance unter Linux."
```

```
EN: "Compare X11 and Wayland for X-Plane 12 — performance benchmarks, VRR support, and session-specific configuration on Debian."
DE: "X11 und Wayland fuer X-Plane 12 im Vergleich — Performance-Benchmarks, VRR-Unterstuetzung und session-spezifische Konfiguration unter Debian."
```

---

## Phase 3 — Bericht

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SEO CHECK: {verzeichnis oder "alle"}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

INFRA:
├─ robots.txt:  {OK | FEHLT}
├─ llms.txt:    {OK | FEHLT}
└─ JSON-LD:     {OK | FEHLT}

GEPRUEFT: {N} Dateien

OK ({Anzahl}):
├─ datei1.md — "{description}" ({Zeichen} chars)
└─ datei2.md — "{description}" ({Zeichen} chars)

KORREKTURBEDARF ({Anzahl}):
├─ datei3.md — {Problem}: "{aktuelle description}"
│   Vorschlag EN: "{neue description}"
│   Vorschlag DE: "{neue description}"
└─ ...

FEHLT ({Anzahl}):
├─ datei4.md — Thema: {Kernthema}
│   Vorschlag EN: "{description}"
│   Vorschlag DE: "{description}"
└─ ...

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## Phase 4 — User-Entscheidung

Per AskUserQuestion:

1. Welche Vorschlaege umsetzen?
2. Optionen: Alle / Einzeln auswaehlen / Keine (nur Bericht)

---

## Phase 5 — Umsetzung (nach Freigabe)

### 5.1 Frontmatter einfuegen oder aktualisieren

Fuer jede freigegebene Datei:

**EN-Seite** (`docs/en/...`):

- Falls Frontmatter existiert: `description:` Feld hinzufuegen oder aktualisieren
- Falls kein Frontmatter: Block am Dateianfang einfuegen:
  ```yaml
  ---
  description: {generierte description}
  ---
  ```

**DE-Seite** (`docs/de/...`):

- Gleiche Struktur, deutsche Description
- Falls die DE-Datei bereits anderes Frontmatter hat (z.B. `title:`, `tags:`): `description:` dort einfuegen

### 5.2 Bestehende Frontmatter-Felder

Vorhandene Felder (`title:`, `tags:`, etc.) NICHT aendern. Nur `description:` hinzufuegen oder aktualisieren.

---

## Phase 6 — Verifikation

Gemaess `SKILL_RULES.md` → **Build pruefen**.

Zusaetzlich: Stichprobenartig 3 gebaute HTML-Seiten pruefen ob `<meta name="description">` den neuen Wert enthaelt.

---

## Phase 7 — Zusammenfassung

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SEO CHECK ABGESCHLOSSEN: {verzeichnis}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

AENDERUNGEN:
├─ Descriptions eingefuegt: {Anzahl} (EN + DE)
├─ Descriptions korrigiert: {Anzahl} (EN + DE)
└─ Unveraendert (OK):      {Anzahl}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**NICHT committen.** Der Commit erfolgt ueber `/abschluss`.

---

## Hinweise

- **EN first:** Descriptions zuerst in EN formulieren, dann DE nachziehen
- **Keine Duplikate:** Jede Description muss einzigartig sein — keine Copy-Paste zwischen Seiten
- **Keywords natuerlich:** Nicht keyword-stuffen, aber relevante Begriffe einbauen (z.B. "X-Plane", "Linux", seitenspezifische Begriffe)
- **Index-Seiten:** Auch index.md Dateien brauchen Descriptions — sie beschreiben die Sektion
- **Glossar/About:** Auch Meta-Seiten brauchen Descriptions
- **Kein Auto-Commit:** `/abschluss` separat ausfuehren
