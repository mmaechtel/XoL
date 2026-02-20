# Review-Cycle

Fuehrt den kompletten Pruefzyklus fuer eine Dokumentationsseite durch: Faktencheck, technisches Lektorat und konsolidierter Bericht. Aendert keine Dateien — liefert nur den Bericht als Entscheidungsgrundlage.

## Argumente

`$ARGUMENTS`: Dateiname der zu pruefenden Seite (ohne Pfad, ohne Sprachprefix)

| Aufruf | Beschreibung |
|--------|-------------|
| `/review-cycle nvidia.md` | Prueft `docs/en/nvidia.md` + DE-Gegenstueck |
| `/review-cycle linux/system/systemtuning.md` | Prueft `docs/en/linux/system/systemtuning.md` + DE |

---

## Pre-Flight

| Voraussetzung | Pruefung | Schwere |
|---------------|---------|---------|
| Argument gesetzt | `$ARGUMENTS` darf nicht leer sein | Blocker |
| EN-Seite existiert | `docs/en/$ARGUMENTS` muss existieren | Blocker |
| DE-Seite existiert | `docs/de/$ARGUMENTS` muss existieren | Blocker |

Bei Blocker: Fehlermeldung ausgeben und abbrechen.

---

## Phase 1 — Vorbereitung

### 1.1 Seiten einlesen

```
Read: docs/en/$ARGUMENTS  (Pruefgrundlage)
Read: docs/de/$ARGUMENTS  (Konsistenzcheck)
```

### 1.2 Research-Papers laden

Research-Papers laden gemaess `SKILL_RULES.md` → **Research-Papers laden**.

### 1.3 Pruefbare Behauptungen extrahieren

Gemaess `SKILL_RULES.md` → **Behauptungen extrahieren**.

Zusaetzlich Halluzinations-Erkennung:

- Erfundene Features, CLI-Flags oder Konfigurationsparameter
- Nicht existierende Pfade oder Dateien
- Erfundene Paketnamen oder Tools
- Falsche Defaults oder Zahlenwerte ohne Beleg
- Plausible aber falsche Kausalitaeten

---

## Phase 2 — Faktencheck (parallele Subagents)

### 2.1 Quellenstrategie

Gemaess `SKILL_RULES.md` → **Quellenstrategie**.

**Zeitfokus:** Quellen ab 2025 bevorzugen. Aeltere Quellen nur akzeptieren wenn keine aktuellere Alternative existiert und die Information nachweislich stabil ist (Kernel-Docs, POSIX-Standards, stabile APIs).

### 2.2 Parallele Pruefung

Gemaess `SKILL_RULES.md` → **Parallele Verifikation (Subagents)**.

Behauptungen in thematische Gruppen aufteilen und als parallele Subagents starten (Task-Tool mit subagent_type=general-purpose). Jeder Subagent:

- Prueft seine Behauptungsgruppe gegen Primaerquellen (WebSearch, WebFetch)
- Belegt jedes Finding mit Direkt-Zitat oder konkretem Datenpunkt
- Prueft alle Quell-URLs auf Erreichbarkeit und Aktualitaet

### 2.3 Bewertung

Pro Behauptung eine Bewertung vergeben:

| Bewertung | Bedeutung |
|-----------|-----------|
| **OK** | Korrekt und angemessen |
| **WARN** | Technisch nicht falsch, aber ungenau/unvollstaendig/veraltet |
| **FAIL** | Falsch oder irrefuehrend, muss korrigiert werden |
| **HALLUZINIERT** | Keine Primaerquelle auffindbar — wahrscheinlich KI-generiert |
| **N/V** | Nicht verifizierbar (keine oeffentliche Quelle) |

### 2.4 Faktencheck-Ergebnisse zusammenfassen

Alle Subagent-Ergebnisse in eine strukturierte Liste konsolidieren:

- FAIL/HALLUZINIERT: Zeile, Behauptung, Befund, Korrekturvorschlag
- WARN: Zeile, Behauptung, Befund
- OK: Kurztabelle (Behauptung + Quelle)
- Quell-URLs: Status (erreichbar/veraltet/fehlerhaft)

---

## Phase 3 — Technisches Lektorat

Direkt nach dem Faktencheck die Rolle eines erfahrenen Lektors fuer technische Dokumentation einnehmen. Die EN-Seite von Anfang bis Ende lesen und bewerten.

### 3.1 MARKDOWN_RULES.txt lesen

```
Read: docs/MARKDOWN_RULES.txt
```

### 3.2 Pruefkriterien

| Aspekt | Frage |
|--------|-------|
| Struktur & Flow | Logischer Aufbau? Klare Gliederung? Abschnitte proportional? |
| Klarheit | Verstaendlich fuer erfahrene Linux-User? Fachbegriffe erklaert/verlinkt? |
| Praegnanz | Unnoetige Redundanz? Textwall? Padding? |
| Schreibqualitaet | Passiv-Uebernutzung? Vage Formulierungen? Fehlende Handlungsanweisungen? |
| X-Plane-Spezifik | Fokus auf X-Plane oder zu generisch/lehrbuchhaft? |
| Umsetzbarkeit | Kann der Leser Schritt fuer Schritt folgen? |
| Konsistenz | Formatierung einheitlich? DE/EN strukturidentisch? |
| MARKDOWN_RULES | Admonitions, Tabellen, Strukturelemente-Wechsel, Listen-Einrueckung? |
| Stil-Angleichung | Gleicher Lesefluss wie bereits reviewte Seiten? |

### 3.3 Stil-Angleichung an Referenzseiten

Die Seite muss sich stilistisch in die bereits reviewten Seiten einfuegen. Referenzseiten fuer Stil und Lesefluss:

- `begin.md` — Einstiegsseite, klarer Aufbau
- `nvidia.md` — Technische Optimierung, Bullet-Praeambel, Code-Praxis-Wechsel
- `systemtools.md` — Werkzeug-Katalog, Tabellen-orientiert
- `systemtuning.md` — Dual-Profil-Ansatz, Admonitions, Vergleichstabellen

Konkret pruefen:

- **Einleitungsstil:** Einordnender Einstiegssatz der den Zweck der Seite klaert (wie nvidia.md, systemtools.md)
- **Prose-Tabelle-Code-Wechsel:** Abwechslung zwischen Fliesstext, Tabellen und Code-Bloecken (nicht nur Textwaelle)
- **Admonitions:** Sinnvoller Einsatz von `!!! tip`, `!!! warning`, `??? abstract` (max 3-4 pro Seite)
- **Trennlinien:** `---` zwischen Hauptabschnitten (vor Sources, vor Further Reading)
- **Sources-Abschnitt:** Am Seitenende, max 5-8 offizielle Quellen
- **Further Reading:** Tabelle mit verwandten Seiten am Ende

### 3.3 Bewertung

Findings in drei Prioritaeten einteilen:

- **HIGH** — Muss korrigiert werden (Fehler, Strukturprobleme, fehlende Inhalte)
- **MEDIUM** — Sollte korrigiert werden (Klarheit, Konsistenz, Praegnanz)
- **LOW** — Kann verbessert werden (Feinschliff, Stil)

---

## Phase 4 — Konsolidierter Bericht

Faktencheck und Lektorat zu einem einzigen Bericht zusammenfuehren. **Nur HIGH- und wichtige MEDIUM-Findings aufnehmen.** LOW wird weggelassen.

### 4.1 Bericht ausgeben

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
REVIEW-CYCLE: <dateiname>
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

FAKTENCHECK:
├─ Geprueft:      <Anzahl>
├─ OK:            <Anzahl>
├─ WARN:          <Anzahl>
├─ FAIL:          <Anzahl>
├─ HALLUZINIERT:  <Anzahl>
└─ N/V:           <Anzahl>

LEKTORAT:
├─ HIGH:   <Anzahl>
├─ MEDIUM: <Anzahl>
└─ LOW:    <Anzahl>

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

GEPLANTE AENDERUNGEN (nur HIGH + wichtige MEDIUM):

| # | Typ | Zeile(n) | Aenderung |
|---|-----|----------|-----------|
| 1 | FALSCH/VERALTET/UNGENAU/STRUKTUR | <Zeile> | <Kurzbeschreibung> |
| ... | | | |

STRUKTURELLE EMPFEHLUNGEN:
│  <Nur wenn substanzielle Umstrukturierung noetig>

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## Hinweise

- **Nur Bericht:** Dieser Skill aendert KEINE Dateien. Er liefert nur den Pruefbericht.
- **Umsetzung separat:** Nach dem Bericht entscheidet der User, welche Aenderungen umgesetzt werden. Die Umsetzung erfolgt manuell oder ueber andere Skills.
- **EN first:** Analyse basiert auf der EN-Seite. DE wird auf Konsistenz geprueft, nicht separat analysiert.
- **Gemeinsame Regeln:** `SKILL_RULES.md` gilt (Quellenstrategie, Behauptungen extrahieren, Parallele Verifikation).
- **Quellenaktualitaet:** Nur Quellen ab 2024. Aeltere nur bei nachweislich stabiler Information.
- **Kein Commit:** Dieser Skill committet nicht und aendert keine Dateien.
- **Parallelisierung:** Faktencheck-Subagents MUESSEN parallel laufen (nicht sequentiell). Lektorat erfolgt nach dem Faktencheck.
