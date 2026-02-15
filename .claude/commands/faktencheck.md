# Faktencheck

Prueft eine fertig umgesetzte Dokumentationsseite gegen Primaerquellen. Korrigiert Fehler in DE + EN, bereinigt Versionsnummern und ergaenzt einen Quellenabschnitt am Seitenende. Entspricht Phase 4 des Dokumentations-Workflows.

## Argumente

`$ARGUMENTS`: Dateiname der zu pruefenden Seite (ohne Pfad, ohne Sprachprefix)

| Aufruf | Beschreibung |
|--------|-------------|
| `/faktencheck nvidia.md` | Prueft `docs/en/nvidia.md` + DE-Gegenstueck |
| `/faktencheck xplane/config.md` | Prueft `docs/en/xplane/config.md` + DE |

---

## Pre-Flight

| Voraussetzung | Pruefung | Schwere |
|---------------|---------|---------|
| Argument gesetzt | `$ARGUMENTS` darf nicht leer sein | Blocker |
| EN-Seite existiert | `docs/en/$ARGUMENTS` muss existieren | Blocker |
| DE-Seite existiert | `docs/de/$ARGUMENTS` muss existieren | Blocker |
| Status mindestens `umgesetzt` | Eintrag in `TODO.md` pruefen | Warnung |

Bei Blocker: Fehlermeldung ausgeben und abbrechen.

---

## Phase 1 — Bestandsaufnahme

### 1.1 Seiten einlesen

```
Read: docs/en/$ARGUMENTS  (Pruefgrundlage — Quellen sind englisch)
Read: docs/de/$ARGUMENTS  (wird spaeter angeglichen)
```

### 1.2 Research-Papers lesen

Research-Papers laden gemaess `SKILL_RULES.md` → **Research-Papers laden**.

### 1.3 Pruefbare Behauptungen extrahieren

Gemaess `SKILL_RULES.md` → **Behauptungen extrahieren**.

### 1.4 Halluzinations-Erkennung

Besondere Aufmerksamkeit auf typische KI-Halluzinationsmuster:

- **Erfundene Features oder Optionen:** Plausibel klingende Funktionen, CLI-Flags oder Konfigurationsparameter die es nicht gibt
- **Nicht existierende Pfade oder Dateien:** Konfigurationspfade die logisch erscheinen, aber auf keinem realen System existieren
- **Erfundene Paketnamen oder Tools:** Tools die es nicht gibt oder die verwechselt werden
- **Falsche Defaults oder Zahlenwerte:** Konkrete Werte (Schwellenwerte, Speichergroessen, Prozentwerte) die nirgends belegt sind
- **Plausible aber falsche Kausalitaeten:** "X fuehrt zu Y" — klingt logisch, ist aber nicht belegt oder sogar falsch
- **Zusammengewuerfelte Informationen:** Korrekte Einzelfakten aus verschiedenen Kontexten die falsch kombiniert werden

**Pruefstrategie:** Wenn eine Behauptung sehr spezifisch und detailliert ist, aber keine Primaerquelle gefunden werden kann, ist das ein starkes Indiz fuer eine KI-Halluzination. Solche Stellen als **HALLUZINIERT** bewerten — sofort entfernen oder durch belegbare Fakten ersetzen.

---

## Phase 2 — Verifikation (parallele Subagents)

### 2.1 Quellenstrategie

Gemaess `SKILL_RULES.md` → **Quellenstrategie**.

### 2.2 Parallele Pruefung

Gemaess `SKILL_RULES.md` → **Parallele Verifikation (Subagents)**.

Zusaetzlich: Jedes Finding mit Direkt-Zitat oder konkretem Datenpunkt belegen.

### 2.3 Bewertung

Pro Behauptung eine Bewertung vergeben:

| Bewertung | Bedeutung |
|-----------|-----------|
| **OK** | Korrekt und angemessen |
| **WARN** | Technisch nicht falsch, aber ungenau/unvollstaendig/veraltet |
| **FAIL** | Falsch oder irrefuehrend, muss korrigiert werden |
| **HALLUZINIERT** | Keine Primaerquelle auffindbar — wahrscheinlich KI-generiert. Sofort entfernen oder ersetzen |
| **N/V** | Nicht verifizierbar (keine oeffentliche Quelle) |

---

## Phase 3 — Faktencheck-Dokument schreiben

**Datei:** `research/<kategorie>/FAKTENCHECK_<dateiname>.md`

**Struktur:**

```markdown
# Faktencheck: <Seitenname> (EN + DE)

**Datum:** YYYY-MM-DD
**Gepruefte Seiten:** `<dateiname_en>`, `<dateiname_de>`
**Primaerquellen verifiziert:** <Liste der Domains>

---

## Fehler (<Anzahl>) — Korrekturbedarf

### 1. <Kurzbezeichnung>
**Datei:** `<dateiname>:<zeile>`
**Behauptung:** <Zitat aus der Seite>
**Befund:** <Was die Primaerquelle sagt, mit Direkt-Zitat>
**Korrektur:** <Konkrete Formulierung fuer die Korrektur>

## Nuancen (<Anzahl>) — verbesserbar, aber akzeptabel

### N. <Kurzbezeichnung>
**Datei:** `<dateiname>:<zeile>`
**Befund:** <Was ungenau ist und warum>

## Korrekt (<Anzahl>) — keine Aenderung noetig

| # | Behauptung | Quelle |
|---|------------|--------|
```

---

## Phase 4 — Ergebnisse vorlegen

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
FAKTENCHECK: <dateiname>
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

BEHAUPTUNGEN:
├─ Geprueft:      <Anzahl>
├─ OK:            <Anzahl>
├─ WARN:          <Anzahl>
├─ FAIL:          <Anzahl>
├─ HALLUZINIERT:  <Anzahl>
└─ N/V:           <Anzahl>

FEHLER (Korrekturbedarf):
│  1. <Kurzbezeichnung> (Zeile <N>)
│  2. ...

NUANCEN (verbesserbar):
│  1. <Kurzbezeichnung> (Zeile <N>)
│  2. ...

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

Per AskUserQuestion den User fragen:

1. **Halluzinationen:** HALLUZINIERT-Findings werden entfernt oder ersetzt (Default: alle)
2. **Fehler:** Welche FAIL-Findings sollen korrigiert werden? (Default: alle)
3. **Nuancen:** Welche WARN-Findings sollen verbessert werden?
4. **N/V:** Behauptungen belassen oder entfernen?

---

## Phase 5 — Korrekturen umsetzen

### 5.1 EN-Seite korrigieren

Fuer jedes freigegebene Finding:

1. Korrektur in `docs/en/$ARGUMENTS` einarbeiten
2. Gegen das Finding gegenlesen (keine neuen Fehler einfuehren)

### 5.2 DE-Seite anpassen

Gemaess `SKILL_RULES.md` → **EN first — DE nachziehen**. `docs/de/$ARGUMENTS` entsprechend angleichen.

### 5.3 Versionsnummern bereinigen

Gemaess `SKILL_RULES.md` → **Versionsnummern bereinigen**.

### 5.4 Quellenabschnitt ergaenzen

Am Ende beider Seiten (EN + DE) einen Quellenabschnitt einfuegen:

```markdown
## Sources / Quellen

- [<Titel>](<URL>) — <Kurzbeschreibung>
```

Nur offizielle, belastbare Quellen. Maximal 5-8 Eintraege.

---

## Phase 6 — Abschluss

### 6.1 Markdown-Check

Gemaess `SKILL_RULES.md` → **Markdown-Check**.

### 6.2 Build pruefen

Gemaess `SKILL_RULES.md` → **Build pruefen**.

### 6.3 TODO.md aktualisieren

Status des Themas auf `geprueft` setzen.

### 6.4 Zusammenfassung

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
FAKTENCHECK ABGESCHLOSSEN: <dateiname>
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

KORREKTUREN:
├─ HALLUZINIERT entfernt: <Anzahl>
├─ FAIL korrigiert:       <Anzahl>
├─ WARN verbessert:       <Anzahl>
├─ Versionen bereinigt:   <Anzahl>
└─ Quellen ergaenzt:      <Anzahl>

DATEIEN GEAENDERT:
├─ docs/en/<dateiname>
├─ docs/de/<dateiname>
├─ research/<kat>/FAKTENCHECK_<dateiname>.md
└─ TODO.md

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**NICHT committen.** Der Commit erfolgt ueber `/abschluss`.

---

## Hinweise

- **Gemeinsame Regeln:** `SKILL_RULES.md` gilt (Quellenstrategie, EN first, Versionsnummern, Markdown-Check, Build)
- **Belegpflicht:** Jedes FAIL/WARN braucht ein Direkt-Zitat, nicht nur eine URL.
- **Referenzplattform:** Debian Stable/Testing. Distributionsabweichungen sind kein Fehler.
- **Kein Commit:** Der Commit erfolgt ueber `/abschluss`.
