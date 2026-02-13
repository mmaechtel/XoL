# Audit

Fuehrt einen Content Audit einer EN-Dokumentationsseite durch gemaess `research/AUDIT_FLOW.md`. Prueft auf Faktenrichtigkeit, Aktualitaet, Relevanz und Detailgrad. Entspricht Phase 5 des Dokumentations-Workflows.

## Argumente

`$ARGUMENTS`: Dateiname der zu auditierenden Seite (ohne Pfad, ohne Sprachprefix)

| Aufruf | Beschreibung |
|--------|-------------|
| `/audit nvidia.md` | Auditiert `docs/en/nvidia.md` |
| `/audit xplane/performance.md` | Auditiert `docs/en/xplane/performance.md` |

---

## Pre-Flight

| Voraussetzung | Pruefung | Schwere |
|---------------|---------|---------|
| Argument gesetzt | `$ARGUMENTS` darf nicht leer sein | Blocker |
| EN-Seite existiert | `docs/en/$ARGUMENTS` muss existieren | Blocker |
| AUDIT_FLOW.md vorhanden | `research/AUDIT_FLOW.md` muss existieren | Blocker |
| AUDIT_STATUS.md vorhanden | `research/AUDIT_STATUS.md` muss existieren | Blocker |
| Kapitel im Audit-Plan | `$ARGUMENTS` muss in AUDIT_STATUS.md gelistet sein | Warnung |

Bei Blocker: Fehlermeldung ausgeben und abbrechen.

---

## Phase 0 — Kontext laden

### 0.1 Prozess-Definition lesen

```
Read: research/AUDIT_FLOW.md
```

Die Audit-Tabelle, Bewertungsskala, Typ-Codes und Regeln aus AUDIT_FLOW.md sind verbindlich.

### 0.2 Fortschritt pruefen

```
Read: research/AUDIT_STATUS.md
```

- Pruefen ob das Kapitel bereits (teilweise) auditiert wurde
- Falls Deep Analysis bereits vorhanden: User fragen ob erneut oder fortsetzen

### 0.3 Audit-Typ bestimmen

| Bedingung | Typ | Aufwand |
|-----------|-----|---------|
| Kapitel in Runde 2 (config.md, displayserver*.md) | **Kurzcheck** | ~25% eines Full Audit |
| Kapitel in anderen Runden | **Full Audit** | S/M/L je nach Zeilenumfang |

Fuer Kurzchecks: Kurzcheck-Protokoll aus AUDIT_FLOW.md anwenden.

---

## Phase 1 — Deep Analysis (Schritt 1)

### 1.1 EN-Seite lesen

```
Read: docs/en/$ARGUMENTS
```

Seite vollstaendig erfassen: Struktur, Ueberschriften, Abschnitte, Konfigurationsbeispiele.

### 1.2 Bestehende Research-Papers laden

```
Glob: research/**/*<thema>*.md
```

Vorhandene Papers als Kontext laden (Research, Lektorat, vorherige Faktenchecks).

### 1.3 Pruefbare Behauptungen extrahieren

Aus der EN-Seite alle pruefbaren Aussagen identifizieren (Kriterien aus AUDIT_FLOW.md):

**Extrahieren:**

- Konkrete Befehle und ihre beschriebene Wirkung
- Konfigurationswerte und ihre behauptete Auswirkung
- Kausalaussagen, Kompatibilitaetsaussagen, Vergleichsaussagen
- Voraussetzungen und Abhaengigkeiten

**Nicht pruefen:**

- Allgemeinwissen, subjektive Wertungen, UI-Beschreibungen
- Wiederholungen bereits anderswo gepruefter Aussagen

### 1.4 Gegen Primaerquellen pruefen (parallele Subagents)

Fuer thematische Gruppen von Behauptungen parallele Subagents starten:

- WebSearch fuer aktuelle Informationen
- WebFetch fuer freigegebene Domains
- Quellenaktualitaet nach Typ differenziert (Tabelle aus AUDIT_FLOW.md)
- Jedes FAIL/WARN mit Direkt-Zitat aus der Quelle belegen
- Nicht verifizierbare Claims als N/V markieren

### 1.5 Audit-Tabelle erstellen

**Kopf:**

| Feld | Wert |
|------|------|
| **Datei** | `docs/en/$ARGUMENTS` |
| **Titel** | <Seitentitel> |
| **Zeilen** | <Anzahl> |
| **Aufwand** | S / M / L |
| **Audit-Datum** | YYYY-MM-DD |
| **Gesamtbewertung** | A / B / C / D |

**Detail-Tabelle:**

| # | Zeile | Abschnitt | Behauptung | Typ | Bewertung | Quelle / Beleg | Empfehlung | Entscheidung |
|---|-------|-----------|------------|-----|-----------|----------------|------------|:------------:|

**Typ-Codes:** FAK (Fakten), AKT (Aktualitaet), REL (Relevanz), DET (Detailgrad)
**Bewertungen:** OK, WARN, FAIL, N/V

### 1.6 Gesamtnote vergeben

| Note | Bedeutung |
|------|-----------|
| A | Korrekt, vollstaendig, gut strukturiert — keine Aenderungen noetig |
| B | Im Kern korrekt, kleinere Ungenauigkeiten oder Luecken |
| C | Teilweise fehlerhaft oder veraltet, Ueberarbeitung noetig |
| D | Grundlegende Probleme, Neuschreiben einzelner Abschnitte noetig |

---

## Phase 2 — Expert Review (Schritt 2)

Zweiter Durchgang mit Fokus auf Struktur und Vollstaendigkeit:

### 2.1 Struktur-Review

| Aspekt | Bewertung | Anmerkung |
|--------|-----------|-----------|
| Fehlende Themen | — | Nur melden wenn fuer Kernziel der Seite unverzichtbar |
| Ueberfluessiges | — | Nicht Linux-spezifisch? Gehoert woanders hin? |
| Zielgruppe | — | Passt Detailgrad zur Zielgruppe? |
| Struktur | — | Logische Reihenfolge? Gute H2/H3-Gliederung? |
| Querverweise | — | Links zu anderen Seiten korrekt und vollstaendig? |
| Markdown/Format | — | Einhaltung der MARKDOWN_RULES.txt? |

### 2.2 Empfehlungen ergaenzen

Empfehlungen in der Audit-Tabelle ergaenzen. Die Entscheidung-Spalte bleibt leer (wird vom User in Schritt 3 gefuellt).

### 2.3 Audit-Dokument schreiben

**Datei:** `research/<kategorie>/AUDIT_<dateiname>.md`

Kopf, Detail-Tabelle, Struktur-Review und Gesamtbewertung zusammenfassen.

---

## Phase 3 — Ergebnisse vorlegen (Schritt 3)

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
AUDIT: <dateiname>
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

GESAMTBEWERTUNG: <A/B/C/D>

BEHAUPTUNGEN:
├─ Geprueft:  <Anzahl>
├─ OK:        <Anzahl>
├─ WARN:      <Anzahl>
├─ FAIL:      <Anzahl>
└─ N/V:       <Anzahl>

FAIL-FINDINGS:
│  1. <Kurzbezeichnung> (Zeile <N>) — <Empfehlung>
│  2. ...

WARN-FINDINGS:
│  1. <Kurzbezeichnung> (Zeile <N>) — <Empfehlung>
│  2. ...

STRUKTUR-REVIEW:
│  <Zusammenfassung der wichtigsten Empfehlungen>

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

Per AskUserQuestion den User fragen:

1. **FAIL-Findings:** Alle korrigieren? (Default: ja)
2. **WARN-Findings:** Welche verbessern?
3. **Struktur-Empfehlungen:** Welche umsetzen?

---

## Phase 4 — Korrekturen umsetzen (Schritt 4)

### 4.1 EN-Seite korrigieren

Freigegebene Aenderungen in `docs/en/$ARGUMENTS` einarbeiten:

1. Jede Korrektur gegen das entsprechende Audit-Finding gegenlesen
2. Keine neuen Fehler einfuehren
3. Versionsnummern nach Entscheidungsbaum bereinigen

### 4.2 Markdown-Check

`docs/MARKDOWN_RULES.txt` auf die EN-Seite anwenden. Verstoesse automatisch korrigieren.

### 4.3 Build pruefen

```
Bash: mkdocs build
```

### 4.4 Fortschritts-Tracker aktualisieren

In `research/AUDIT_STATUS.md` die entsprechenden Felder mit Datum fuellen.

### 4.5 Zusammenfassung

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
AUDIT ABGESCHLOSSEN: <dateiname>
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

GESAMTBEWERTUNG: <Note>

KORREKTUREN:
├─ FAIL korrigiert:        <Anzahl>
├─ WARN verbessert:        <Anzahl>
├─ Versionen bereinigt:    <Anzahl>
├─ Struktur-Aenderungen:   <Anzahl>
└─ Markdown-Fixes:         <Anzahl>

DATEIEN GEAENDERT:
├─ docs/en/<dateiname>
├─ research/<kat>/AUDIT_<dateiname>.md
└─ research/AUDIT_STATUS.md

NAECHSTES KAPITEL: #<N> <dateiname>

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**NICHT committen.** Der Commit erfolgt ueber `/abschluss`.

**Hinweis:** DE-Angleichung erfolgt erst nach Abschluss einer kompletten Runde (nicht pro Kapitel). Das naechste Kapitel kann sofort auditiert werden.

---

## Hinweise

- **EN first:** Audit immer auf der EN-Seite. DE-Angleichung erst nach Abschluss der Runde.
- **AUDIT_FLOW.md ist verbindlich:** Alle Regeln, Templates und Bewertungsskalen aus der Prozess-Definition gelten.
- **Primaerquellen:** Nur offizielle Docs, Kernel-Docs, Arch Wiki, GitHub. Keine Foren/Blogs.
- **Quellenaktualitaet:** Nach Informationstyp differenziert (Tabelle in AUDIT_FLOW.md).
- **Belegpflicht:** FAIL/WARN-Findings brauchen Direkt-Zitate, nicht nur URLs. Sonst N/V.
- **Referenzplattform:** Debian Stable/Testing. Distributionsabweichungen sind kein Fehler.
- **Vollstaendigkeits-Bremse:** Fehlende Themen nur melden wenn fuer Kernziel unverzichtbar.
- **Versionsnummern:** Entscheidungsbaum in AUDIT_FLOW.md beachten.
- **Sitzungs-Management:** Output nach `research/<kat>/AUDIT_<datei>.md` persistieren bevor die Sitzung endet.
- **Kein Commit:** Der Commit erfolgt ueber `/abschluss`.
