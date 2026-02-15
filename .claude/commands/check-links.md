# Check Links

Prueft alle externen Links auf einer deutschen Dokumentationsseite. Nicht funktionierende Links werden recherchiert und korrigiert. Nach Korrektur der DE-Seite wird die EN-Seite nachgezogen.

## Argumente

`$ARGUMENTS`: Dateiname der zu pruefenden Seite (ohne Pfad, ohne Sprachprefix)

| Aufruf | Beschreibung |
|--------|-------------|
| `/check-links addon/xa-snow.md` | Prueft `docs/de/addon/xa-snow.md` |
| `/check-links nvidia.md` | Prueft `docs/de/nvidia.md` |

---

## Pre-Flight

| Voraussetzung | Pruefung | Schwere |
|---------------|---------|---------|
| Argument gesetzt | `$ARGUMENTS` darf nicht leer sein | Blocker |
| DE-Seite existiert | `docs/de/$ARGUMENTS` muss existieren | Blocker |
| EN-Seite existiert | `docs/en/$ARGUMENTS` muss existieren | Warnung (nur DE pruefen) |

Bei Blocker: Fehlermeldung ausgeben und abbrechen.

---

## Phase 1 — Links extrahieren

1. **DE-Seite lesen:**
```
Read: docs/de/$ARGUMENTS
```

2. **Externe Links extrahieren:**
   Alle URLs finden, die mit `http://` oder `https://` beginnen. Sowohl Markdown-Links `[text](url)` als auch nackte URLs erfassen.

3. **Interne Links ignorieren:**
   Links zu anderen Docs-Seiten (relative Pfade wie `flywithlua.md`, `../glossary.md#term`) werden uebersprungen.

4. **Link-Liste ausgeben:**
   Nummerierte Liste aller gefundenen externen Links mit Zeilennummer und Linktext.

---

## Phase 2 — Links pruefen

Jeden externen Link pruefen. **Parallel** wo moeglich (mehrere WebFetch-Aufrufe gleichzeitig).

### Pruefmethode

Fuer jeden Link:

1. **WebFetch** mit dem Prompt: "Does this page exist and load correctly? Return the page title and a one-sentence summary of the content."
2. **Ergebnis bewerten:**
   - **OK:** Seite laedt, Inhalt passt zum Linktext
   - **Redirect:** Seite leitet um — neue URL notieren
   - **404/Fehler:** Seite nicht erreichbar
   - **Inhalt passt nicht:** Seite laedt, aber Inhalt stimmt nicht mit dem Linktext ueberein (z.B. Repo umgezogen, Datei umbenannt)

### Sonderfaelle

- **GitHub-Links:** `gh api` bevorzugen (schneller, authentifiziert):
  ```bash
  gh api repos/{owner}/{repo} --jq '.full_name, .archived, .html_url'
  ```
  Bei Releases: `gh api repos/{owner}/{repo}/releases/latest --jq '.tag_name, .html_url'`

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

GEPRÜFT: {N} externe Links

✓ OK ({Anzahl}):
├─ [Linktext](url) — Zeile {n}
├─ ...
└─ ...

✗ DEFEKT ({Anzahl}):
├─ [Linktext](url) — Zeile {n}
│   Problem: {404 / Redirect / Inhalt passt nicht}
│   Vorschlag: {neue URL oder "entfernen"}
├─ ...
└─ ...

⚠ WARNUNG ({Anzahl}):
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

2. **DE-Seite korrigieren:**
   Defekte Links durch die freigegebenen Replacements ersetzen.

3. **EN-Seite nachziehen:**
   - EN-Seite lesen: `docs/en/$ARGUMENTS`
   - Dieselben URLs finden und durch die korrigierten ersetzen
   - Falls der Link in der EN-Seite nicht vorkommt oder anders formuliert ist: manuell anpassen

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

- **Kein Auto-Commit:** Der Skill erstellt keine Git-Commits. `/abschluss` separat ausfuehren.
- **Nur externe Links:** Interne Links (zu anderen Docs-Seiten) werden nicht geprueft.
- **Rate Limiting:** Bei vielen Links nicht alle gleichzeitig pruefen — max. 4-5 parallele WebFetch-Aufrufe.
- **Quellenabschnitt beachten:** Links im `## Quellen` / `## Sources`-Abschnitt besonders sorgfaeltig pruefen — diese sind die Referenzen fuer die gesamte Seite.
