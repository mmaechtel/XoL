# Check Links

Prueft alle externen Links auf einer Dokumentationsseite (EN first). Nicht funktionierende Links werden recherchiert und korrigiert. Korrekturen werden in EN + DE synchron angewendet.

## Argumente

`$ARGUMENTS`: Dateiname der zu pruefenden Seite (ohne Pfad, ohne Sprachprefix)

| Aufruf | Beschreibung |
|--------|-------------|
| `/check-links addon/xa-snow.md` | Prueft `docs/en/addon/xa-snow.md` + DE-Gegenstueck |
| `/check-links nvidia.md` | Prueft `docs/en/nvidia.md` + DE-Gegenstueck |

---

## Pre-Flight

| Voraussetzung | Pruefung | Schwere |
|---------------|---------|---------|
| Argument gesetzt | `$ARGUMENTS` darf nicht leer sein | Blocker |
| EN-Seite existiert | `docs/en/$ARGUMENTS` muss existieren | Blocker |
| DE-Seite existiert | `docs/de/$ARGUMENTS` muss existieren | Warnung (nur EN pruefen) |

Bei Blocker: Fehlermeldung ausgeben und abbrechen.

---

## Phase 1 — Links extrahieren

1. **EN-Seite lesen:**
```
Read: docs/en/$ARGUMENTS
```

2. **DE-Seite parallel lesen:**
```
Read: docs/de/$ARGUMENTS
```

3. **Externe Links extrahieren (aus beiden Seiten):**
   Alle URLs finden, die mit `http://` oder `https://` beginnen. Sowohl Markdown-Links `[text](url)` als auch nackte URLs erfassen. Links aus beiden Seiten zusammenfuehren (Duplikate nur einmal pruefen).

4. **Interne Links ignorieren:**
   Links zu anderen Docs-Seiten (relative Pfade wie `flywithlua.md`, `../glossary.md#term`) werden uebersprungen.

5. **Link-Liste ausgeben:**
   Nummerierte Liste aller gefundenen externen Links mit Zeilennummer, Sprache (EN/DE/beide) und Linktext.

---

## Phase 2 — Links pruefen

Jeden externen Link pruefen. **Parallel** wo moeglich (max. 4-5 gleichzeitige Aufrufe).

### Pruefmethode

Fuer jeden Link:

1. **GitHub-Links:** `gh api` bevorzugen (schneller, authentifiziert):
   ```bash
   gh api repos/{owner}/{repo} --jq '.full_name, .archived, .html_url'
   ```
   Bei Releases: `gh api repos/{owner}/{repo}/releases/latest --jq '.tag_name, .html_url'`

2. **Andere Links:** WebFetch mit dem Prompt: "Does this page exist and load correctly? Return the page title and a one-sentence summary of the content."

3. **Ergebnis bewerten:**
   - **OK:** Seite laedt, Inhalt passt zum Linktext
   - **Redirect:** Seite leitet um — neue URL notieren
   - **404/Fehler:** Seite nicht erreichbar
   - **Inhalt passt nicht:** Seite laedt, aber Inhalt stimmt nicht mit dem Linktext ueberein (z.B. Repo umgezogen, Datei umbenannt)

### Sonderfaelle

- **Domains ohne WebFetch-Freigabe:** Falls WebFetch eine Permission-Abfrage ausloest, alternativ per `Bash: curl -sI <url> | head -5` nur den HTTP-Status pruefen
- **forums.x-plane.org:** WebFetch verwenden, auf Redirect oder "File not found" pruefen
- **Banned Domains:** Domains aus MEMORY.md (steamcommunity.com, questions.x-plane.com etc.) als problematisch markieren, aber trotzdem pruefen ob der spezifische Link funktioniert

---

## Phase 3 — Defekte Links recherchieren

Fuer jeden defekten oder fragwuerdigen Link:

1. **WebSearch** nach dem Thema/Projekt + "X-Plane" oder dem erwarteten Inhalt
2. **Korrekte URL identifizieren:**
   - Repo umgezogen? → neue GitHub-URL
   - Seite umstrukturiert? → neuer Pfad
   - Projekt eingestellt? → Archiv-Link oder Hinweis
3. **Replacement-URL vorschlagen**

---

## Phase 4 — Bericht

Am Ende einen uebersichtlichen Bericht ausgeben:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
CHECK LINKS: {dateiname}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

GEPRÜFT: {N} externe Links (EN: {n1}, DE: {n2}, beide: {n3})

OK ({Anzahl}):
├─ [Linktext](url) — Zeile {n}
├─ ...
└─ ...

DEFEKT ({Anzahl}):
├─ [Linktext](url) — Zeile {n} ({EN/DE/beide})
│   Problem: {404 / Redirect / Inhalt passt nicht}
│   Vorschlag: {neue URL oder "entfernen"}
├─ ...
└─ ...

WARNUNG ({Anzahl}):
├─ [Linktext](url) — Zeile {n}
│   Hinweis: {z.B. "Repo archiviert", "Redirect auf andere Domain"}
└─ ...
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## Phase 5 — Korrekturen anwenden (nach User-Freigabe)

**Erst nach Rueckfrage beim User** die Korrekturen anwenden.

1. **User fragen:**
   AskUserQuestion mit den vorgeschlagenen Korrekturen — einzeln oder gesammelt bestaetigen lassen.

2. **EN-Seite korrigieren:**
   Defekte Links durch die freigegebenen Replacements ersetzen.

3. **DE-Seite nachziehen:**
   - Dieselben URLs in der DE-Seite finden und durch die korrigierten ersetzen
   - Falls der Link in der DE-Seite nicht vorkommt oder anders formuliert ist: manuell anpassen

4. **Keine weiteren Aenderungen:**
   Nur Links korrigieren — keinen Text, keine Struktur, keine Formatierung aendern.

---

## Phase 6 — Verifikation

Nach den Korrekturen die reparierten Links nochmals pruefen (WebFetch oder gh api), um sicherzustellen, dass die neuen URLs funktionieren.

---

## Phase 7 — Protokoll fuehren

Nach Abschluss der Pruefung (auch wenn keine Korrekturen noetig waren) das Ergebnis in `research/LINKCHECK_STATUS.md` festhalten.

### Datei anlegen (falls nicht vorhanden)

```markdown
# Link-Check Status

| Seite | Links | OK | Defekt | Korrigiert | Datum |
|-------|-------|----|--------|------------|-------|
```

### Zeile anfuegen oder aktualisieren

```markdown
| {dateiname} | {Anzahl Links} | {Anzahl OK} | {Anzahl Defekt} | {Anzahl korrigiert} | {YYYY-MM-DD} |
```

- Falls die Seite bereits in der Tabelle steht: **Zeile ersetzen** (nicht doppelt eintragen)
- Sortierung: alphabetisch nach Seitenname

---

## Hinweise

- **EN first:** Pruefung startet mit der EN-Seite (konsistent mit allen anderen Skills). DE-Links werden parallel erfasst.
- **Kein Auto-Commit:** Der Skill erstellt keine Git-Commits. `/abschluss` separat ausfuehren.
- **Nur externe Links:** Interne Links (zu anderen Docs-Seiten) werden nicht geprueft.
- **Rate Limiting:** Max. 4-5 parallele WebFetch-Aufrufe. Bei Domains ohne Freigabe auf `curl -sI` ausweichen.
- **Quellenabschnitt beachten:** Links im `## Quellen` / `## Sources`-Abschnitt besonders sorgfaeltig pruefen — diese sind die Referenzen fuer die gesamte Seite.
