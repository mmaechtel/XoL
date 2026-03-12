# Check Glossar

Prueft eine Dokumentationsseite auf Glossar-Abdeckung, fehlende Verweise und Markdown-Konformitaet. Arbeitet bilingual (EN first, dann DE).

## Argumente

`$ARGUMENTS`: Dateiname der zu pruefenden Seite (ohne Pfad, ohne Sprachprefix)

| Aufruf | Beschreibung |
|--------|-------------|
| `/check-glossar begin.md` | Prueft `docs/en/begin.md` + `docs/de/begin.md` |
| `/check-glossar xplane/config.md` | Prueft `docs/en/xplane/config.md` + DE-Gegenstueck |

---

## Pre-Flight

| Voraussetzung | Pruefung | Schwere |
|---------------|---------|---------|
| Argument gesetzt | `$ARGUMENTS` darf nicht leer sein | Blocker |
| EN-Seite existiert | `docs/en/$ARGUMENTS` muss existieren | Blocker |
| DE-Seite existiert | `docs/de/$ARGUMENTS` muss existieren | Blocker |
| Glossare existieren | `docs/en/glossary.md` + `docs/de/glossary.md` | Blocker |

Bei Blocker: Fehlermeldung ausgeben und abbrechen.

---

## Phase 1 — Log pruefen

**Logdatei:** `research/glossar_check.log`

1. Falls die Logdatei existiert, pruefen ob `$ARGUMENTS` bereits gecheckt wurde
2. Falls ja: Datum des letzten Checks anzeigen und User fragen ob erneut geprüft werden soll
3. Falls nein oder User bestaetigt: Weiter mit Phase 2

**Log-Format** (eine Zeile pro Check):

```
YYYY-MM-DD  <dateiname>  <anzahl_neue_begriffe>  <anzahl_fixes>
```

---

## Phase 2 — Bestandsaufnahme

### 2.1 Glossare einlesen

1. `docs/en/glossary.md` lesen — alle `### Begriffname` Eintraege extrahieren
2. `docs/de/glossary.md` lesen — alle `### Begriffname` Eintraege extrahieren
3. Mapping erstellen: EN-Begriff ↔ DE-Begriff (ueber Position/Reihenfolge)

### 2.2 Seiten einlesen

1. `docs/en/$ARGUMENTS` vollstaendig lesen
2. `docs/de/$ARGUMENTS` vollstaendig lesen

### 2.3 Vorhandene Glossar-Verweise erfassen

Alle Links der Form `[Text](../glossary.md#anchor)` oder `[Text](glossary.md#anchor)` in beiden Seiten identifizieren.

---

## Phase 3 — Glossar-Abdeckung analysieren

### 3.1 Bereits verlinkte Begriffe

Fuer jede Seite (EN + DE) auflisten:

- Welche Glossar-Begriffe sind bereits verlinkt?
- Sind die Anchors korrekt (stimmt `#anchor` mit der tatsaechlichen Ueberschrift im Glossar ueberein)?
- Gibt es tote Links (Anchor existiert nicht im Glossar)?

### 3.2 Fehlende Verlinkungen

Fuer jeden Glossar-Begriff pruefen:

- Kommt der Begriff (oder sein Kern-Keyword) im Seitentext vor?
- Ist er NICHT als Glossar-Link formatiert?
- → Diese Begriffe als "fehlende Verlinkung" melden

**Regeln:**

- Nur die ERSTE Verwendung eines Begriffs pro Seite muss verlinkt sein
- Begriffe in Code-Bloecken (`backticks` oder ```code fences```) nicht verlinken
- Begriffe in Ueberschriften nicht verlinken
- Begriffe die Teil eines bereits verlinkten Textes sind, nicht doppelt melden

### 3.3 Wichtige Begriffe ohne Glossar-Eintrag

Die Seite inhaltlich analysieren und zentrale technische Begriffe identifizieren, die:

- Wiederholt auf der Seite verwendet werden
- Fuer das Verstaendnis der Seite relevant sind
- Noch KEINEN Glossar-Eintrag haben
- Linux-spezifisch oder X-Plane-spezifisch sind (keine Allgemeinbegriffe)

**Nicht vorschlagen:**

- Allgemeinwissen (SSD, RAM, CPU, GPU — es sei denn, es gibt einen X-Plane-spezifischen Aspekt)
- Begriffe die nur einmal beilaeufig erwaehnt werden
- Begriffe die bereits durch einen anderen Glossar-Eintrag abgedeckt sind

---

## Phase 4 — Ergebnisse vorlegen

Dem User eine strukturierte Uebersicht praesentieren:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
GLOSSAR-CHECK: <dateiname>
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

VERLINKTE BEGRIFFE:
├─ EN: <anzahl> Glossar-Links
└─ DE: <anzahl> Glossar-Links

PROBLEME:
├─ Tote Links: <anzahl> (Anchor existiert nicht)
├─ Fehlende Verlinkungen: <anzahl> (Begriff kommt vor, ist aber nicht verlinkt)
└─ DE/EN Asymmetrie: <anzahl> (Link in einer Sprache, aber nicht in der anderen)

VORSCHLAEGE NEUE GLOSSAR-BEGRIFFE:
│  <Nr>. <Begriff> — <Kurzbeschreibung warum relevant>
│  ...

FEHLENDE VERLINKUNGEN (bereits im Glossar, aber nicht verlinkt):
│  <Nr>. <Begriff> in Zeile <x> (EN) / Zeile <y> (DE)
│  ...
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## Phase 5 — User-Entscheidung

Per AskUserQuestion den User fragen:

1. **Neue Glossar-Begriffe:** Welche der vorgeschlagenen Begriffe sollen ins Glossar aufgenommen werden?
2. **Fehlende Verlinkungen:** Sollen alle fehlenden Verlinkungen automatisch ergaenzt werden?
3. **Tote Links:** Sollen tote Links automatisch repariert oder entfernt werden?

---

## Phase 6 — Umsetzung

### 6.1 Neue Glossar-Begriffe einfuegen

Fuer jeden freigegebenen Begriff:

1. EN-Definition schreiben und in `docs/en/glossary.md` alphabetisch einsortieren
2. DE-Definition schreiben und in `docs/de/glossary.md` alphabetisch einsortieren
3. Sicherstellen dass die Eintraege in beiden Sprachen identische Struktur haben
4. Anchor-Name aus der `### Ueberschrift` ableiten

### 6.2 Fehlende Verlinkungen ergaenzen

Fuer jede freigegebene Verlinkung:

1. Relativen Pfad anhand der Verzeichnistiefe bestimmen:
   - Seite in `docs/{lang}/*.md` → `../glossary.md#anchor`
   - Seite in `docs/{lang}/xplane/*.md` → `../../glossary.md#anchor`
   - Seite in `docs/{lang}/addon/*.md` → `../../glossary.md#anchor`
   - Seite in `docs/{lang}/flight_operations/*.md` → `../../glossary.md#anchor`
2. In der EN-Seite: Erste Verwendung des Begriffs als `[Begriff](<pfad>#anchor)` formatieren
3. In der DE-Seite: Entsprechende Stelle mit DE-Anchor verlinken
4. Nur die ERSTE Nennung verlinken, nicht jede

### 6.3 Tote Links reparieren

1. Anchor korrigieren falls der Begriff im Glossar existiert (Tippfehler)
2. Link entfernen falls der Begriff nicht im Glossar existiert und kein neuer Eintrag erstellt wird

---

## Phase 7 — Markdown-Check

Gemaess `SKILL_RULES.md` → **Markdown-Check**.

---

## Phase 8 — Abschluss

### 8.1 Build pruefen

Gemaess `SKILL_RULES.md` → **Build pruefen**.

### 8.2 Log aktualisieren

Eintrag in `research/glossar_check.log` schreiben:

```
YYYY-MM-DD  <dateiname>  <anzahl_neue_begriffe>  <anzahl_fixes>
```

### 8.3 Zusammenfassung

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
GLOSSAR-CHECK ABGESCHLOSSEN: <dateiname>
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

AENDERUNGEN:
├─ Neue Glossar-Begriffe: <anzahl> (EN + DE)
├─ Verlinkungen ergaenzt: <anzahl>
├─ Tote Links repariert:  <anzahl>
└─ Markdown-Fixes:        <anzahl>

DATEIEN GEAENDERT:
├─ docs/en/glossary.md
├─ docs/de/glossary.md
├─ docs/en/<dateiname>
├─ docs/de/<dateiname>
└─ research/glossar_check.log
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**NICHT committen.** Der Commit erfolgt ueber `/abschluss`.

---

## Hinweise

- Gemaess `SKILL_RULES.md` → **EN first — DE nachziehen**
- **Alphabetische Sortierung:** Glossar-Eintraege muessen alphabetisch sortiert bleiben
- **Keine Allgemeinbegriffe:** Nur Linux-spezifische oder X-Plane-spezifische Begriffe aufnehmen
- **Erste Nennung:** Nur die erste Verwendung eines Begriffs auf einer Seite verlinken
- **Keine Links in Code-Bloecken:** Begriffe innerhalb von Backticks oder Code Fences nicht verlinken
- **Keine Links in Ueberschriften:** Glossar-Links gehoeren in den Fliesstext, nicht in H2/H3/H4
- **Markdown-Check:** Gemaess `SKILL_RULES.md` → automatisch, ohne Rueckfrage
- **Pfadtiefe beachten:** Glossar-Links muessen die Verzeichnistiefe der Seite beruecksichtigen (siehe Phase 6.2)

### Link-Prioritaet: Glossar vs. Seiten-Link vs. externer Link

Wenn ein Begriff sowohl einen Glossar-Eintrag als auch einen Seiten- oder externen Link haben koennte, gelten folgende Regeln:

1. **Bestehende Links nie ersetzen.** Seiten-Links (`[System Tuning](systemtuning.md)`) und externe Links (`[Debian](https://debian.org)`) werden nicht durch Glossar-Links ersetzt. Sie dienen der Navigation bzw. als Quellenreferenz.

2. **Erste Erwaehnung → Glossar-Link.** Wenn ein Begriff zum ersten Mal auftaucht und noch keinen Link hat → Glossar-Link setzen. Der Glossar-Link erklaert den Begriff (Definition).

3. **Spaetere Erwaehnung → Seiten-Link.** Wenn derselbe Begriff spaeter im Kontext einer Vertiefung erwaehnt wird → Seiten-Link setzen (Navigation zur ausfuehrlichen Erklaerung).

4. **Erste Erwaehnung ist bereits Seiten-Link:** Wenn die erste Erwaehnung eines Begriffs als Seiten-Link formatiert ist (z.B. in einem Bullet "behandelt in [Liquorix Kernel](liquorix.md)"), dann:
   - Gibt es eine FRUEHERE, unverlinkte Erwaehnung desselben Begriffs auf der Seite? → Diese fruehere Stelle bekommt den Glossar-Link
   - Gibt es keine fruehere Erwaehnung? → Seiten-Link behalten (Seite > Glossar, wenn die Seite das Thema ausfuehrlich behandelt)

5. **Nie doppelt verlinken.** Ein Wort traegt maximal einen Link. Keine Konstrukte wie `[Mesa](glossary.md#mesa)([Details](mesa.md))`.

6. **Ueber-Verlinkung vermeiden.** Nicht jeden bekannten Begriff zwanghaft verlinken. Begriffe die im Kontext klar verstaendlich sind (z.B. "Vulkan" im Satz "OpenGL-zu-Vulkan-Uebersetzung" wo Zink bereits verlinkt ist) muessen nicht zusaetzlich verlinkt werden.
