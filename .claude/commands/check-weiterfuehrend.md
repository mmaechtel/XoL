# Check Weiterfuehrende Kapitel

Prueft alle Nicht-Index-Seiten in einem Verzeichnis auf das Vorhandensein und die Qualitaet des Abschnitts `## Weiterfuehrende Kapitel`. Arbeitet als Senior Technical Editor: liest den gesamten Docs-Bestand, versteht die thematischen Zusammenhaenge und schlaegt nur Querverweise vor, die fuer den Leser der jeweiligen Seite tatsaechlich nuetzlich sind.

## Argumente

`$ARGUMENTS`: Verzeichnispfad relativ zu `docs/de/`

| Aufruf | Beschreibung |
|--------|-------------|
| `/check-weiterfuehrend linux/system` | Prueft alle Nicht-Index-Dateien in `docs/de/linux/system/` |
| `/check-weiterfuehrend fundamentals/performance` | Prueft `docs/de/fundamentals/performance/` |
| `/check-weiterfuehrend addon/cockpit` | Prueft `docs/de/addon/cockpit/` |

---

## Pre-Flight

| Voraussetzung | Pruefung | Schwere |
|---------------|---------|---------|
| Argument gesetzt | `$ARGUMENTS` darf nicht leer sein | Blocker |
| Verzeichnis existiert | `docs/en/$ARGUMENTS/` und `docs/de/$ARGUMENTS/` muessen existieren | Blocker |
| Dateien vorhanden | Mindestens eine `.md`-Datei (nicht `index.md`) im EN-Verzeichnis | Blocker |

Bei Blocker: Fehlermeldung ausgeben und abbrechen.

---

## Phase 1 — Gesamtkontext aufbauen

### 1.1 Zielverzeichnis erfassen

Alle `.md`-Dateien in `docs/en/$ARGUMENTS/` auflisten. `index.md` ausschliessen. Diese Dateien sind die **Pruefkandidaten**. Die gesamte Analyse laeuft auf den EN-Seiten (Fachbegriffe sind eindeutiger). DE wird erst in Phase 6 angeglichen.

### 1.2 Site-weite Themenkarte erstellen

Um fundierte Vorschlaege machen zu koennen, muss der gesamte Docs-Bestand bekannt sein. Die `mkdocs.yml` Navigation einlesen — sie enthaelt alle Seiten mit ihren Nav-Labels und hierarchischen Zuordnungen.

Zusaetzlich die Section-Index-Dateien (`index.md`) der Hauptsektionen lesen, da diese inhaltliche Zusammenfassungen enthalten:

- `docs/en/fundamentals/performance/index.md`
- `docs/en/linux/system/index.md`
- `docs/en/linux/optimizations/index.md`
- `docs/en/linux/extensions/index.md`
- `docs/en/xplane/setup_diagnose/index.md`
- `docs/en/scenery/index.md`
- `docs/en/addon/index.md`
- `docs/en/flight_operations/index.md`

Das ergibt eine mentale Karte: welche Seite behandelt welches Thema, in welcher Sektion.

### 1.3 Pruefkandidaten einlesen

Jeden Pruefkandidaten vollstaendig lesen (EN-Version). Dabei erfassen:

- H1-Titel und H2-Abschnitte (Themenstruktur)
- Bereits vorhandene interne Links (wohin verweist die Seite schon?)
- Vorhandener `## Further Reading`-Abschnitt (oder Varianten: `## Further Chapters`, `## Related`)
- Vorhandener `## Sources`-Abschnitt (bleibt unangetastet)
- Kernthema der Seite in einem Satz

---

## Phase 2 — Analyse pro Datei

Fuer jeden Pruefkandidaten eine der drei Bewertungen vergeben:

### Fall A: Abschnitt vorhanden und korrekt

`## Weiterfuehrende Kapitel` existiert, enthaelt 4-7 relative Links, und die verlinkten Seiten sind thematisch passend.

**Aktion:** Als OK markieren.

### Fall B: Abschnitt vorhanden, aber problematisch

Der Abschnitt existiert, hat aber Maengel:

- Zu wenige Links (unter 4)
- Zu viele Links (ueber 8 — dann ist es eine Linkliste, kein kuratierter Verweis)
- Falsches Tabellenformat: Muss immer 3 Spalten haben (EN: `Topic | Page | Focus`, DE: `Thema | Seite | Schwerpunkt`). 2-Spalten-Tabellen oder Aufzaehlungslisten sind nicht konform.
- Falscher Abschnittstitel: EN muss `## Further Reading` sein, DE muss `## Weiterfuehrende Kapitel` sein. Varianten wie "Weiterführend", "Further Chapters", "Related" sind nicht konform.
- Thematisch unpassende Links (Seite X hat keinen inhaltlichen Bezug)
- Tote relative Links (Zieldatei existiert nicht)
- Doppelungen (gleiche Seite mehrfach verlinkt)
- Links auf index.md oder glossary.md (gehoeren nicht hierhin)

**Aktion:** Konkrete Korrekturvorschlaege formulieren.

### Fall C: Abschnitt fehlt

Kein `## Weiterfuehrende Kapitel` (oder Variante) vorhanden.

**Aktion:** 6-7 thematisch passende Querverweise vorschlagen. Falls weniger sinnvolle Ziele existieren, entsprechend weniger vorschlagen — keine Fantasie-Verweise erfinden.

---

## Phase 3 — Vorschlaege formulieren

### Auswahlkriterien fuer Querverweise

Ein guter Querverweis erfuellt mindestens eines dieser Kriterien:

1. **Thematische Naehe:** Die Zielseite behandelt ein verwandtes Thema (z.B. systemtuning.md → systemtools.md)
2. **Vertiefung:** Die Zielseite erklaert einen Aspekt ausfuehrlicher (z.B. performance_overview.md → cpu_ram.md)
3. **Voraussetzung:** Die Zielseite beschreibt etwas, das fuer das aktuelle Thema relevant ist (z.B. nvidia.md → displayserver_wayland.md)
4. **Naechster Schritt:** Die Zielseite beschreibt den logischen Folgeschritt (z.B. liquorix.md → systemtuning.md)
5. **Gegenueberstellung:** Die Zielseite behandelt eine Alternative oder einen Vergleich (z.B. autoortho.md → xearthlayer.md)

### Was NICHT vorgeschlagen werden soll

- `index.md`-Seiten (Section Indexes)
- `glossary.md` (dafuer gibt es Glossar-Links im Text)
- `about.md`, `videos.md`, `intro.md` (Meta-Seiten)
- Seiten ohne inhaltlichen Bezug (kein Querverweis nur um 6 zu erreichen)
- Seiten die bereits im Fliesstext der aktuellen Seite verlinkt sind (Vermeidung von Dopplung — nur pruefen ob es ZUSAETZLICHE sinnvolle Verweise gibt)

### Format der Vorschlaege

Jeder Vorschlag enthaelt:

- Relativen Link (korrekte Pfadtiefe!)
- Nav-Label der Zielseite
- Einzeilige Begruendung warum dieser Verweis fuer den Leser nuetzlich ist

Beispiel:

```markdown
## Weiterfuehrende Kapitel

| Thema | Seite | Schwerpunkt |
|---|---|---|
| Kernel-Tuning | [Kernel-Tuning](../../linux/system/systemtuning.md) | CPU-Governor, IRQ-Pinning, Kernel-Parameter |
| Liquorix | [Liquorix Kernel](../../linux/optimizations/liquorix.md) | Low-Latency-Kernel und PDS-Scheduler |
```

---

## Phase 4 — Bericht

Fuer das gesamte Verzeichnis einen strukturierten Bericht ausgeben:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
CHECK WEITERFUEHRENDE KAPITEL: {verzeichnis}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

GEPRUEFT: {N} Dateien

OK ({Anzahl}):
├─ datei1.md — {Anzahl} Links, alle passend
└─ datei2.md — {Anzahl} Links, alle passend

KORREKTURBEDARF ({Anzahl}):
├─ datei3.md — {Problem}: {Details}
│   Vorschlag: {Korrektur}
└─ datei4.md — {Problem}: {Details}
    Vorschlag: {Korrektur}

FEHLT ({Anzahl}):
├─ datei5.md — Vorschlag:
│   | Thema | Seite | Schwerpunkt |
│   |---|---|---|
│   | ... | ... | ... |
└─ datei6.md — Vorschlag:
    | Thema | Seite | Schwerpunkt |
    |---|---|---|
    | ... | ... | ... |

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## Phase 5 — User-Entscheidung

Per AskUserQuestion den User fragen:

1. **Vorschlaege pruefen:** Welche der vorgeschlagenen Aenderungen sollen umgesetzt werden?
2. **Optionen:** Alle umsetzen / Einzeln auswaehlen / Keine (nur Bericht)

---

## Phase 6 — Umsetzung (nach Freigabe)

### 6.1 Abschnitt einfuegen oder korrigieren

Fuer jede freigegebene Datei:

1. **EN-Seite** (`docs/en/...`) lesen
2. **EN-Seite** bearbeiten: `## Further Reading` Abschnitt einfuegen oder korrigieren
   - Position: am Ende der Seite, aber VOR einem eventuellen `## Quellen` / `## Sources` Abschnitt
   - Falls `## Quellen` existiert: `## Weiterfuehrende Kapitel` davor einfuegen, mit `---` Trennlinie dazwischen
   - Falls kein `## Quellen`: `---` Trennlinie + `## Further Reading` am Ende
3. **DE-Seite** (`docs/de/...`) bearbeiten: `## Weiterfuehrende Kapitel` analog einfuegen
   - Gleiche Struktur, gleiche Zielseiten, uebersetzter Text

### 6.2 Tabellenformat

```markdown
---

## Weiterfuehrende Kapitel

| Thema | Seite | Schwerpunkt |
|---|---|---|
| {Thema} | [{Label}]({relativer-link}) | {Schwerpunkt} |
```

EN-Variante:

```markdown
---

## Further Reading

| Topic | Page | Focus |
|---|---|---|
| {Topic} | [{Label}]({relative-link}) | {Focus} |
```

### 6.3 Relative Links

Pfadtiefe anhand des Verzeichnisses berechnen:

- `docs/{lang}/thema.md` → `thema.md` oder `verz/datei.md`
- `docs/{lang}/linux/system/` → `../../fundamentals/performance/latency.md`
- `docs/{lang}/fundamentals/performance/` → `../../linux/system/systemtuning.md`

Immer die korrekte Anzahl `../` verwenden. Keine absoluten Pfade.

---

## Phase 7 — Verifikation

Gemaess `SKILL_RULES.md` → **Build pruefen**.

Zusaetzlich: `python3 scripts/check_links.py` ausfuehren um relative Links zu validieren.

---

## Phase 8 — Zusammenfassung

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
CHECK WEITERFUEHRENDE KAPITEL ABGESCHLOSSEN: {verzeichnis}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

AENDERUNGEN:
├─ Abschnitte eingefuegt: {Anzahl} (EN + DE)
├─ Abschnitte korrigiert: {Anzahl} (EN + DE)
└─ Unveraendert (OK):     {Anzahl}

DATEIEN GEAENDERT:
├─ docs/en/...
├─ docs/de/...
└─ (Liste)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**NICHT committen.** Der Commit erfolgt ueber `/abschluss`.

---

## Hinweise

- **EN first:** Abschnitt zuerst in EN einfuegen/korrigieren, dann DE nachziehen
- **Keine Fantasie-Verweise:** Nur Seiten vorschlagen die tatsaechlich existieren und thematisch passen. Lieber 4 gute als 7 erzwungene Verweise.
- **Nicht mit Quellen verwechseln:** `## Weiterfuehrende Kapitel` verweist auf andere Docs-Seiten (intern). `## Quellen` verweist auf externe URLs. Beides kann koexistieren.
- **Glossar ist kein Ziel:** Glossar-Verlinkungen gehoeren in den Fliesstext, nicht in die Weiterfuehrenden Kapitel.
- **Bestehende Fliesstext-Links beachten:** Wenn die Seite bereits im Text auf eine andere Seite verlinkt, kann diese trotzdem in den Weiterfuehrenden Kapiteln erscheinen — der Zweck ist ein anderer (kuratierte Uebersicht vs. kontextuelle Erwaehnung).
- **Kein Auto-Commit:** `/abschluss` separat ausfuehren.
