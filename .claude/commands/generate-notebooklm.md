# Generate NotebookLM-Skript

Erstellt eine TTS-optimierte Markdown-Datei fuer Google NotebookLM Audio Overview (Deep Dive, zwei Hosts). Quellenbasis: XoL-Dokumentation (docs/en/) und Research-Papers (research/).

## Argumente

`$ARGUMENTS`: Thema + optionaler Modus

| Aufruf | Modus | Beschreibung | Laenge |
|--------|-------|-------------|--------|
| `/generate-notebooklm display server` | **summary** | Themenuebersicht (Standard) | ~15 Min. |
| `/generate-notebooklm system tuning qa` | **qa** | Q&A-Diskussion, Fragen aus Content generiert | ~10 Min. |
| `/generate-notebooklm xplane config topic:Shader Cache` | **topic** | Schwerpunkt auf ein Unterthema | ~7-10 Min. |

**Modus-Erkennung:**
- Kein Modus-Argument → `summary`
- Letztes Argument = `qa` → `qa`
- Letztes Argument beginnt mit `topic:` → `topic` (alles nach dem Doppelpunkt = Unterthema)
- Alles davor = Thema-Keyword

---

## Pre-Flight

| Voraussetzung | Pruefung | Schwere |
|---------------|---------|---------|
| Thema aufloesbar | Mindestens eine passende Datei in `docs/en/` oder `research/` | ⛔ Blocker |
| Content ausreichend | Mindestens 100 Zeilen Quellmaterial geladen | ⛔ Blocker |
| Output-Verzeichnis | `research/notebooklm/` existiert (sonst anlegen) | Auto-fix |

Bei ⛔ Blocker: AskUserQuestion — "Thema nicht gefunden. Abbrechen oder alternatives Thema waehlen?"

---

## Konzept

Der Skill analysiert XoL-Dokumentation und Research-Papers zu einem Thema und erstellt daraus eine TTS-optimierte Datei fuer Google NotebookLM. Je nach Modus unterscheiden sich Fokus, Laenge und Struktur:

**summary** (Standard): Umfassende Themenuebersicht. Zwei Hosts diskutieren Hintergrund, Konfiguration und praktische Empfehlungen. Primaeres Deliverable fuer Zuhoerer die ein Thema vollstaendig verstehen wollen.

**qa**: Frage-Antwort-Diskussion. Fragen werden aus dem Content generiert — typische Entscheidungsfragen, Troubleshooting-Szenarien und Konzeptverstaendnis. Ideal zur gezielten Wiederholung.

**topic**: Vertiefung eines einzelnen Unterthemas. Fokussiert auf einen Aspekt, dafuer gruendlicher als die Gesamtuebersicht. Ideal fuer spezifische Problemstellungen.

---

## Skill-Spezifikation

| Eigenschaft | summary | qa | topic |
|-------------|---------|-----|-------|
| **Source** | Docs + Research (komplett) | Docs + Research (komplett) | Docs + Research (Subset) |
| **Output** | `NOTEBOOKLM_<thema>_summary.md` | `NOTEBOOKLM_<thema>_qa.md` | `NOTEBOOKLM_<thema>_topic_<sub>.md` |
| **Ziel-Woerter** | ~2000-2500 (~15 Min.) | ~1300-1700 (~10 Min.) | ~1000-1500 (~7-10 Min.) |

### NotebookLM Audio-Format

In NotebookLM beim Generieren des Audio Overview immer **Deep Dive** auswaehlen. Zwei Hosts fuehren eine natuerliche Diskussion — genau dafuer sind alle drei Modi optimiert.

---

## Phase 0: Thema aufloesen + Content laden

### 0.1 Thema-Keyword zu Dateien aufloesen

Vier Suchstrategien in dieser Reihenfolge:

**1. docs/en/ Dateinamen durchsuchen:**
```
Glob: docs/en/**/*.md → Dateinamen gegen Thema-Keyword matchen
→ Treffer direkt als docs_files uebernehmen
```

**2. research/INDEX.md durchsuchen:**
```
Read: research/INDEX.md
→ Kategorie-Ueberschriften und Dateinamen gegen Thema-Keyword matchen
→ Zugehoerige docs/en/ Seiten und research/ Papers identifizieren
```

**3. mkdocs.yml Navigation durchsuchen:**
```
Read: mkdocs.yml
→ Navigation-Eintraege gegen Thema-Keyword matchen
→ Zugehoerige Dateinamen extrahieren
```

**4. research/ Dateinamen-Suche (Fallback):**
```
Glob: research/**/*.md → Dateinamen gegen Thema-Keyword matchen
```

**Ergebnis:** Liste von Dateien, aufgeteilt in:
- `docs_files`: Dokumentationsseiten aus `docs/en/`
- `research_files`: Research-Papers und Lektorate aus `research/`

**Bei Ambiguitaet:** AskUserQuestion mit gefundenen Optionen.

### 0.2 Dokumentationsseiten laden

```
Read: docs/en/<datei>.md (fuer jede identifizierte Seite)
→ Vollstaendig laden
→ Kapitelstruktur verstehen (Ueberschriften, Abschnitte, Konfigurationsbeispiele)
```

EN-Seiten als Arbeitsbasis — das Skript wird auf Deutsch generiert, aber EN ist strukturell identisch und naeher an den englischen Primaerquellen.

### 0.3 Research-Papers laden

```
Read: research/<kat>/<datei>.md (fuer jedes identifizierte Paper)
→ Nur Typ Research und Lektorat laden
→ NICHT laden: AUDIT_*, FAKTENCHECK_* (sind Pruefprotokolle, kein Content)
```

Research-Papers liefern technische Tiefe und Hintergrund. Sie ergaenzen die Docs-Seiten, ersetzen sie nicht.

### 0.4 Content-Zusammenfassung

Nach dem Laden eine interne Bestandsaufnahme:
- Welche Konzepte werden in den Docs behandelt?
- Welche zusaetzlichen Details liefern die Research-Papers?
- Wo gibt es Widersprueche? (→ Docs haben Vorrang, Research nur wenn neuere Primaerquelle)

**Modus `topic`:** Alle Dateien laden, aber fuer die Generierung nur die zum Unterthema passenden Abschnitte verwenden. Der Rest dient als Kontext.

---

## Phase 1: Planung (modusabhaengig)

### Modus `summary`: Themen-Outline

Ein internes Planungsdokument (wird NICHT geschrieben, nur als Arbeitsgrundlage genutzt):

1. **KERN** = Konzepte und Konfigurationen die jeder Linux-X-Plane-Nutzer kennen sollte
2. **KUERZBAR** = Zusaetzliche Tools, Varianten, Edge Cases
3. **WEGLASSEN** = Reine Referenz-Informationen (Befehlslisten, Tabellen), History

Zeitplan fuer 15 Minuten:
- 00:00-02:00 — Einstieg: Warum ist das Thema fuer X-Plane unter Linux relevant?
- 02:00-12:00 — Kernkonzepte (3-4 Bloecke)
- 12:00-15:00 — Zusammenfassung und Empfehlungen

### Modus `qa`: Fragengenerierung

Keine vorhandenen Fragen — stattdessen aus dem Content generieren:

**Schritt 1 — Fragentypen identifizieren:**
1. **Entscheidungsfragen**: "Wayland oder X11 — wann was?" / "Welcher CPU-Governor?"
2. **Troubleshooting**: "Frame Times schwanken — woran liegt's?" / "Kein Vulkan unter Wayland?"
3. **Konzeptverstaendnis**: "Was macht der Shader-Cache genau?" / "Warum IRQ-Affinitaet?"
4. **Best Practice**: "Was sind die ersten drei Schritte nach der Linux-Installation fuer X-Plane?"

**Schritt 2 — 6-8 Fragen auswaehlen:**
- Gleichmaessige Verteilung ueber die Docs-Abschnitte
- Mix aus Einsteiger- und Fortgeschrittenen-Fragen (ca. 2/3 : 1/3)
- Bevorzugt Entscheidungs- und Verstaendnisfragen, weniger reine Fakten
- Reihenfolge: Grundlagen → Vertiefung

### Modus `topic`: Unterthema eingrenzen

1. Das angegebene Unterthema im geladenen Content identifizieren
2. Relevante Abschnitte markieren
3. Angrenzende Konzepte identifizieren (fuer Kontext)
4. Entscheiden: Welche Tiefe ist in 7-10 Minuten erreichbar?

---

## Phase 2: NotebookLM-Skript generieren

### 2.1 TTS-Regeln (KRITISCH — gelten fuer ALLE Modi)

| Regel | Grund | Beispiel |
|-------|-------|---------|
| **Keine Code-Bloecke** | TTS liest Syntax-Zeichen vor | `cpupower frequency-set -g performance` → "den Befehl cpupower frequency-set mit der Option g performance" |
| **Keine Hex-Adressen** | TTS liest Ziffern einzeln | `0x200000` → "zweihunderttausend hexadezimal" |
| **Zahlen als Woerter** | Dezimalpunkt-Verwirrung | `16384` → "sechzehntausenddreihundertvierundachtzig" |
| **Keine Tabellen** | TTS liest Pipe-Zeichen | Tabelle → Fliesstext |
| **Keine ASCII-Diagramme** | TTS liest Sonderzeichen | Diagramm → verbale Beschreibung |
| **Keine Markdown-Formatierung** | Bold/Italic stoeren TTS | `**Bold**` → einfacher Text |
| **Keine Meta-Instruktionen** | NotebookLM liest ALLES vor | Gehoert in Audio Customization Box |
| **Keine Quellenangaben** | Werden vorgelesen | Keine "_Quelle: ..."_ Zeilen |
| **Keine Emojis/Symbole** | TTS-Artefakte | Kein ⚠️, ✅ etc. |
| **Echte Umlaute** | TTS-Aussprache | ä/ö/ü verwenden, NICHT ae/oe/ue |
| **Keine Listen/Aufzaehlungen** | TTS liest Aufzaehlungszeichen | Stattdessen Fliesstext mit Uebergaengen |

### 2.2 Gemeinsame Generierungsregeln (alle Modi)

**Inhaltlich:**
- **Docs + Research sind die einzigen Quellen.** Keine Konzepte erfinden
- **Befehle verbal beschreiben**: Verhalten und Zweck in Worten erklaeren
- **Konfigurationen erklaeren**: Nicht auflisten, sondern den Effekt beschreiben
- **X-Plane-Bezug herstellen**: Jedes technische Konzept mit dem Nutzen fuer X-Plane verbinden

**Sprache:**
- **Deutsch mit englischen Fachbegriffen** — Linux/X-Plane-Terminologie beibehalten
- Echte Umlaute (ä, ö, ü)
- Fliesstext in natuerlichem Gespraechston
- Direkte Ansprache erlaubt ("Stellen Sie sich vor...", "Betrachten wir...")
- Kurze Saetze bevorzugen
- Englische Fachbegriffe werden von NotebookLM korrekt englisch ausgesprochen

**Format:**
- Reines Markdown: Nur `#` und `##` Ueberschriften + Fliesstext
- Keine YAML-Frontmatter, Wikilinks, Callouts, Bold, Italic
- Keine Fussnoten, Quellenangaben, Kommentare

### 2.3 Modus `summary`: Themenuebersicht

**Ziel:** ~2000-2500 Woerter (~15 Min.)

**Struktur:**
```
# {Thema auf Deutsch} — {Untertitel}

## {Abschnitt 1: Einstieg/Motivation}
{Fliesstext: Warum ist das Thema fuer X-Plane auf Linux relevant?}

## {Abschnitt 2-N: Kernkonzepte}
{Fliesstext: Technische Konzepte erklaeren, Konfigurationen beschreiben,
praktische Empfehlungen einweben. Uebergaenge als natuerliche Saetze.}

## {Letzter Abschnitt: Zusammenfassung / Empfehlungen}
{Fliesstext: Kernpunkte zusammenfassen. Konkrete Empfehlungen.}
```

**Spezifische Regeln:**
- **Nur KERN-Inhalte** aus dem Outline. KUERZBAR nur wenn es den Fluss verbessert
- **Roter Faden**: Jeder Abschnitt beginnt mit "Warum?" bevor das "Was?" kommt
- **Motivation vor Konfiguration**: Erst das Problem, dann die Loesung
- **Uebergaenge**: Natuerliche Ueberleitungen zwischen Abschnitten
- **Rhetorische Fragen**: Max. 3-5, sofort beantworten
- **Empfehlungen**: Am Ende konkrete, umsetzbare Ratschlaege

### 2.4 Modus `qa`: Experten-Diskussion

**Ziel:** ~1300-1700 Woerter (~10 Min.)

**Grundidee:** Das Skript liest sich wie eine lebhafte Diskussion zwischen Linux-Enthusiasten die X-Plane fliegen. Die generierten Fragen liefern den inhaltlichen Fokus, aber die Darstellung ist ein Fachgespraech: Einer wirft eine Frage auf, der andere erklaert, beide ergaenzen sich, hinterfragen Annahmen und verbinden Konzepte.

**Struktur:**
```
# {Thema} — Eine Diskussion

## {Themenbereich 1}
{Einstieg: Ein Gespraechspartner wirft ein Problem oder eine Beobachtung auf.
Der andere greift auf, erklaert den Hintergrund, bringt einen praktischen
Tipp ein. Die generierten Fragen werden als natuerliche Gespraechsanlaesse
eingewebt, nicht als Frage-Antwort abgearbeitet.}

## {Themenbereich 2}
{Natuerlicher Uebergang: Ein Gedanke aus dem vorherigen Block fuehrt
zum naechsten Thema.}

## {Abschluss}
{Gemeinsames Fazit: Was sind die wichtigsten Erkenntnisse?
Was sollte man als Erstes ausprobieren?}
```

**Spezifische Regeln:**
- **Diskussion, keine Vorlesung**: Kein Frage-Antwort-Muster. Behauptungen, Ergaenzungen, Einwaende, Beispiele
- **Keine expliziten Sprecher-Labels**: Kein "Host A sagt...". Fliesstext mit wechselnden Perspektiven — NotebookLM verteilt automatisch auf zwei Hosts
- **Fragen einweben**: Die generierten Fragen sind Rohmaterial. Ihre Kernaussagen muessen im Text auftauchen, aber umformuliert als Diskussionsbeitraege
- **Thematischer Fluss**: Themengruppen bestimmen die Abschnitte. Innerhalb eines Abschnitts fliessen Konzepte ineinander
- **Spannung durch Perspektiven**: Einer betont die elegante Loesung, der andere sieht die Fallstricke. Einer vereinfacht, der andere praezisiert
- **Schwierigkeit steigern**: Grundlegendes zuerst, Feinheiten spaeter

### 2.5 Modus `topic`: Schwerpunktthema

**Ziel:** ~1000-1500 Woerter (~7-10 Min.)

**Struktur:**
```
# {Unterthema} — Vertiefung

## Warum ist {Unterthema} wichtig?
{Fliesstext: Einordnung im Themen-Kontext. Warum lohnt sich
ein genauerer Blick auf genau diesen Aspekt?}

## {Kernaspekt 1}
{Fliesstext: Tiefere Erklaerung als in der Themenuebersicht.
Hier darf mehr ins Detail gegangen werden.}

## {Kernaspekt 2}
{Weitere Vertiefung. Szenarien, Was-waere-wenn, Konfigurationsbeispiele.}

## Einordnung
{Wie haengt das Unterthema mit dem Rest zusammen?
Was sollte man als Naechstes anschauen?}
```

**Spezifische Regeln:**
- **Fokus statt Breite**: Nur das angegebene Unterthema, dafuer gruendlicher
- **Mehr Detail erlaubt**: Szenarien und Erklaerungen duerfen laenger sein
- **Kontext herstellen**: Am Anfang kurz einordnen
- **Am Ende vernetzen**: Zusammenhaenge zu anderen Aspekten
- **Laenge variabel**: Einfache Themen kuerzer (800), komplexe laenger (1500)

---

## Phase 2.6: Dateiablage

### Verzeichnis

```
research/notebooklm/
```

Falls das Verzeichnis nicht existiert: anlegen.

### Dateinamen

| Modus | Dateiname |
|-------|-----------|
| summary | `NOTEBOOKLM_<thema>_summary.md` |
| qa | `NOTEBOOKLM_<thema>_qa.md` |
| topic | `NOTEBOOKLM_<thema>_topic_<unterthema>.md` |

`<thema>` und `<unterthema>`: Leerzeichen durch Bindestriche, Kleinbuchstaben. Beispiel: `topic:Shader Cache` → `NOTEBOOKLM_xplane-config_topic_shader-cache.md`

### Kein Ueberschreiben

Bestehende Dateien werden NICHT ueberschrieben. Falls die Target-Datei existiert:
- Suffix erweitern: `_v2.md`, `_v3.md` etc.
- Versionsnummer hochzaehlen

---

## Phase 3: Qualitaetspruefung

### 3.1 Fachliche Pruefung

| Kriterium | Pruefung |
|-----------|---------|
| **Faktische Korrektheit** | Stimmen alle Aussagen mit Docs/Research ueberein? |
| **Keine Erfindungen** | Wird etwas behauptet, das nicht in den Quellen steht? |
| **Vollstaendigkeit** | summary: Alle Kernkonzepte abgedeckt? qa: Antworten korrekt? topic: Thema erschoepfend? |
| **Befehle korrekt** | Stimmen erwaehnte Befehle und Pfade mit den Docs ueberein? |
| **Terminologie** | Werden Fachbegriffe korrekt und konsistent verwendet? |

### 3.2 TTS-Pruefung

| Kriterium | Pruefung |
|-----------|---------|
| **Keine Code-Bloecke** | Kein ``` oder Inline-Code? |
| **Keine Zahlen als Ziffern** | Alle Zahlen als Woerter? |
| **Keine Tabellen/Diagramme** | Kein Pipe, kein ASCII-Art? |
| **Keine Listen** | Keine Aufzaehlungszeichen (-, *, 1.)? |
| **Keine Meta-Instruktionen** | Nichts das NotebookLM als Anweisung statt Content liest? |
| **Echte Umlaute** | ä/ö/ü statt ae/oe/ue? |
| **Keine Sonderzeichen** | Keine Emojis, keine Symbole? |
| **Keine Markdown-Formatierung** | Kein Bold, Italic, Links? |

Bei Befunden: Direkt korrigieren, nicht nur melden.

### 3.3 Rechtschreib- und Akronym-Pruefung

**Rechtschreibung:**
- Deutsche Woerter: Tippfehler, fehlende Buchstaben
- Englische Fachbegriffe: Korrekte Schreibweise
- Grammatik: Kasus, Kongruenz, Satzbau

**Akronyme:**
- Jedes Akronym beim ersten Vorkommen aufloesen
- Pruefung gegen den geladenen Content: Stimmt die Aufloesung?
- Unbekannte Akronyme entfernen

Bei Befunden: Direkt korrigieren.

---

## Phase 4: Zusammenfassung

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
NOTEBOOKLM [{MODUS}]: {Thema}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

MODUS: {summary / qa / topic:{Unterthema}}

CONTENT-QUELLEN:
├─ Docs:       {X} Seiten geladen ({Dateinamen})
└─ Research:   {Y} Papers geladen ({Dateinamen})

{Nur bei qa:}
FRAGENGENERIERUNG:
├─ Generiert:  {G} Fragen
├─ Ausgewaehlt: {S} Fragen
└─ Typen-Mix:  {E} Entscheidung, {T} Troubleshooting, {K} Konzept

NOTEBOOKLM-DATEI:
├─ Abschnitte: {A}
├─ Woerter:    ~{W} (Ziel: {Zielbereich})
├─ Geschaetzte Audio-Laenge: ~{M} Min.
└─ Datei:      research/notebooklm/{Dateiname}

QUALITAETSPRUEFUNG:
├─ Fachlich:   {OK / Befunde auflisten}
├─ TTS:        {OK / Befunde auflisten}
└─ Rechtschreibung/Akronyme: {OK / Befunde + Korrekturen auflisten}

AUDIO OVERVIEW CUSTOMIZATION (in NotebookLM einfuegen):
  {Aussprachehilfen fuer ungewoehnliche Begriffe, falls noetig}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## Hinweise

- **Kein Review-Zyklus**: Dieses Skill generiert direkt ohne interaktives Review
- **Kein Ueberschreiben**: Bestehende Dateien bleiben erhalten
- **Quellen nur aus XoL**: Nur geladene Docs und Research verwenden, keine externen Quellen hinzuerfinden
- **Debian-Kontext**: Referenzplattform ist Debian Stable/Testing — Befehle und Paketnamen entsprechend
- **Versionsnummern**: Entscheidungsbaum aus research/AUDIT_FLOW.md beachten — im Zweifel weglassen
- **Audio Customization**: Aussprachehilfen gehoeren NICHT in die NotebookLM-Datei, sondern in die Zusammenfassung

---

## Phase 5: Output-Verzeichnis oeffnen

Nach Abschluss das Output-Verzeichnis im Dateimanager oeffnen:

```bash
open research/notebooklm/
```
