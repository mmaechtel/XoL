# Faktencheck Bulk

Prueft einen ganzen Seitenbereich gegen Primaerquellen und legt das Ergebnis als HTML-Review-Seite zur Freigabe vor. Aendert waehrend der Pruefung **keine** Dateien.

Fuer eine einzelne Seite `/faktencheck` verwenden — dieser Skill lohnt ab etwa 10 Seiten.

## Argumente

`$ARGUMENTS`: Verzeichnis unter `docs/en/` (ohne Sprachprefix)

| Aufruf | Prueft |
|--------|--------|
| `/faktencheck-bulk addon` | alle Seiten unter `docs/en/addon/` |
| `/faktencheck-bulk linux/system` | alle Seiten unter `docs/en/linux/system/` |

---

## Kostenrahmen

Ein Lauf ueber 47 Seiten kostet nach Erfahrung **rund 1 Mio Tokens**. Vor dem Start dem User die Seitenzahl nennen und bestaetigen lassen, wenn es mehr als 20 Seiten sind.

Die haeufigsten Kostenfallen — alle im Ablauf unten bereits vermieden:

- Mehrere getrennte Laeufe statt einem. Pruefung, Buendelung und Tragweite gehoeren in **ein** Agenten-Schema.
- Ein AUTO/REVIEW-Triage-Pass. Bringt nichts, die Tragweite leistet dasselbe billiger.
- Blinde WebFetch-Versuche gegen gesperrte Domains.

---

## Phase 0 — Vorbereitung (Hauptthread, kein Workflow)

### 0.1 Seitenliste bilden

```bash
find docs/en/$ARGUMENTS -name "*.md" ! -name "index.md" | sort
```

`index.md` bleibt aussen vor — Uebersichtsseiten haben keine eigenen Faktenaussagen.

### 0.2 Quellenlage klaeren

Seiten ohne GitHub-Repo ermitteln:

```bash
for f in <seiten>; do grep -qi 'github.com' "$f" || echo "$f"; done
```

Fuer diese Seiten haengt der Upstream-Stand an Foren oder Herstellerseiten.

### 0.3 Gesperrte Quellen per Browser einsammeln

`forums.x-plane.org` und `store.x-plane.org` liefern auf WebFetch **immer 403** (Cloudflare). Google Cache existiert nicht mehr, Wayback deckt nur einen Teil ab. Details: Memory `x-plane-org-403`.

Deshalb **vor** dem Workflow, seriell im Hauptthread:

1. `Skill(claude-in-chrome)` aufrufen, Tools per ToolSearch in **einem** Aufruf laden.
2. URLs aus den betroffenen Seiten extrahieren.
3. Mit `browser_batch` je Seite `navigate` + `get_page_text` — fuenf bis sechs URLs pro Batch.
4. Liefert eine Forum-Seite statt der Beschreibung eine User-Review, `?tab=about` anhaengen.
5. Volltext als `<scratchpad>/forum-evidence.md` ablegen, pro Plugin ein Abschnitt mit URL, Stand/Changelog-Datum und den belegten Aussagen.

Nicht erreichbare Seiten dort unter „NICHT BELEGBAR" auflisten — die Agenten stufen sie als `NV` ein statt zu raten.

---

## Phase 1 — Pruefung und Buendelung (ein Workflow)

Ein Agent pro Seite, danach adversarische Gegenpruefung der harten Findings. Der Agent liefert Findings **und** Buendelung in einem Schema.

### 1.1 Schema

```
findings[]:  severity (FAIL|HALLUZINIERT|WARN|VERSION_ENTFERNEN|NV)
             category (deprecation|features|installation|links|version|kompatibilitaet)
             line, claim (woertliches Zitat), evidence (Direktzitat der Quelle),
             source_url, correction (Ersatztext oder "ENTFERNEN")
entscheidungen[]: titel, frage, empfehlung (ja|nein), begruendung,
             tragweite (hoch|mittel|niedrig), zeilen[]
```

**Buendelungsregel:** Zwei Findings gehoeren zusammen, wenn eine einzige Ja/Nein-Antwort beide erledigt (typisch: ein Upstream-Wechsel zieht Download-Link, Pfad, Warnhinweis und Quelle gemeinsam mit). Sie bleiben getrennt, wenn der User das eine bejahen und das andere verneinen koennte, ohne dass die Seite widerspruechlich wird.

**Tragweite:** `hoch` = Empfehlung, Linux-Tauglichkeit oder Deprecation aendert sich · `mittel` = spuerbare inhaltliche Korrektur · `niedrig` = Detailpraezisierung.

### 1.2 Pflichtregeln im Agenten-Prompt

Alle vier gehoeren woertlich hinein, sonst kommen unbrauchbare Findings zurueck:

- **Versionsnummern:** Keine aktuellen Release-Versionen nennen. Beschreibung auf neuen Stand bringen, Ueberholtes ersatzlos streichen, keine Versionshistorie erzaehlen. Eine Nummer bleibt nur als Entscheidungsgrenze (zwei Produktlinien, XP11-vs-XP12, Deprecation, Stagnationssignal). Memory: `plugin-versionskonvention`.
- **Linux-only:** Windows-/macOS-Findings unterdruecken. Die `Platforms:`-Zeile bleibt unberuehrt, ausser die Linux-Angabe darin ist falsch.
- **403 ist kein toter Link.** Niemals ein Finding der Kategorie `links` auf einen 403 stuetzen, keine Wiederholungsversuche.
- **Nichts dazuschreiben:** Korrekturen ersetzen bestehenden Text, keine neuen Abschnitte, Seiten werden nicht laenger.

Dazu die Belegpflicht: jedes Finding braucht Direktzitat plus URL, sonst wird es nicht gemeldet. Gesperrte Domains siehe `MEMORY.md`.

### 1.3 Gegenpruefung

Jedes `FAIL` und `HALLUZINIERT` geht an einen Skeptiker mit dem Auftrag zu **widerlegen**, `effort: high`, im Zweifel verworfen. Erfahrungswert: etwa jedes fuenfte Finding faellt weg, und die Begruendungen decken Abhaengigkeiten zwischen Fundstellen derselben Seite auf.

### 1.4 Technische Fallen

- `args` kommt als JSON-String an: `typeof args === 'string' ? JSON.parse(args) : args`
- Ergebnisse landen in `journal.jsonl` des Transkript-Verzeichnisses. Haengt ein Agent, laesst sich daraus direkt weiterarbeiten, statt auf den Lauf zu warten.

---

## Phase 2 — Selbstwiderspruchs-Check (Hauptthread, gratis)

Ja-Empfehlungen markieren, deren eigene Begruendung ein Hedge-Wort enthaelt oder die auf einem `NV`-Finding fussen:

```
spekulativ · nicht verifiziert · keine quelle · nicht belegt · unbelegt ·
vermutlich · angekuendigt · nur an einem · zwei lesarten · nicht zwingend ·
grenzwertig · nicht schlicht falsch · unsicher
```

Treffer bekommen `unsicher: "<gefundene Woerter>"` und in der Review-Seite ein eigenes Badge samt Filter. Im letzten Lauf: 18 von 87, darunter ein klarer Fehlgriff (empfohlene Aenderung auf ausdruecklich unverifizierter Grundlage).

Vorsicht bei der Deutung: Bezieht sich „unbelegt" auf das, was **gestrichen** wird, ist die Aenderung unbedenklich. Kritisch ist nur, wenn die **neue** Aussage schwach belegt ist.

---

## Phase 3 — Review-Seite

```bash
python3 scripts/build_review_page.py <findings.json> <decisions.json> <out.html> "<Titel>"
```

Erzeugt eine self-contained HTML-Seite: nach Tragweite sortiert, startet auf `hoch`, Diffs eingeklappt, Tastatur `j`/`k`/`y`/`n`/`m`/`Enter`, Stand in `localStorage`, Filter `unsicher` und `offen`.

„Abweichungen kopieren" oeffnet ein Feld mit dem markierten Text und versucht zusaetzlich die Zwischenablage — die ist nicht in jedem Kontext erlaubt, und ein stiller Fehlschlag laesst den User im Glauben, er haette kopiert. Das Feld ist der verlaessliche Weg, die Zwischenablage die Bequemlichkeit.

Der Rueckkanal ist bewusst manuell: Die Seite ist statisch und schickt nichts zurueck. Der User fuegt den Text in den Chat ein. Alles, was nicht in der Liste steht, gilt als bestaetigt.

### Validierung — laeuft automatisch, nicht umgehen

Das Skript prueft sich am Ende selbst und bricht mit Exit-Code 2 ab, wenn etwas nicht stimmt: JS-Syntax per `node --check`, Vorhandensein der vom Script erwarteten Element-IDs, gerenderte Karten, nicht aufgeloeste CSS-Escapes.

**Warum das eingebaut ist:** Ein Syntaxfehler im `<script>`-Block legt die komplette Seite lahm — Klicks, Tastatur, Filter, alles —, ohne dass man der Seite etwas ansieht. Sie sieht korrekt aus und reagiert nur nicht. Im ersten Lauf hat genau das drei Nachbesserungsrunden gekostet, weil am sichtbaren CSS herumkuriert wurde statt den Code einmal auszufuehren.

Ursache war eine Escape-Sequenz ueber zwei Ebenen: `\n` im Python-Quelltext des Generators wurde beim Erzeugen zu einem echten Zeilenumbruch und zerriss das Stringliteral. Deshalb ist der JS-Block im Generator ein **Raw-String** (`js = r"""..."""`) — beim Bearbeiten so lassen.

Bei Abbruch: Fehlermeldung lesen, Generator korrigieren, erneut bauen. **Niemals eine Seite veroeffentlichen, die die Validierung nicht bestanden hat.**

Per `Artifact` veroeffentlichen und dem User die URL geben. Er meldet nur die Abweichungen zurueck — alles Uebrige gilt als bestaetigt.

---

## Phase 4 — Umsetzung

Erst **nach** der Rueckmeldung des Users.

1. **EN** aendern, Entscheidung fuer Entscheidung. Abgelehnte auslassen, markierte vorher besprechen.
2. **DE** 1:1 angleichen (`SKILL_RULES.md` → EN first). DE-Anrede: unpersoenlicher Stil.
3. Markdown-Check gemaess `docs/MARKDOWN_RULES.txt` auf beide Sprachen.
4. `mkdocs build` — muss fehlerfrei durchlaufen.
5. Changelog in `docs/{de,en}/index.md` als **ein** komprimierter Sammeleintrag, nicht als Einzelliste. Maximal 3 Datumsbloecke. `index.md` immer zuletzt.

**Kein Commit** — der erfolgt ueber `/abschluss`.

---

## Hinweise

- Gemeinsame Regeln: `SKILL_RULES.md` (Quellenstrategie, EN first, Markdown-Check, Build)
- Referenzplattform: Debian Stable/Testing
- Der Bericht in `research/<kategorie>/` bleibt die Langfassung mit Belegen; die HTML-Seite ist die Freigabe-Oberflaeche, kein Ersatz
