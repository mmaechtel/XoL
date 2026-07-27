# Faktencheck-Daten Plugin-Seiten (2026-07-20)

Rohdaten des Massen-Faktenchecks ueber die 47 Seiten unter `docs/en/addon/`.
Aus dem sessiongebundenen Scratchpad hierher gesichert, damit die Umsetzung
auch nach einem Sessionwechsel fortgesetzt werden kann.

Umsetzungsstand und Arbeitsregeln: `../UMSETZUNG_plugins_2026-07-20.md`

---

## Dateien

| Datei | Inhalt |
|-------|--------|
| `diff-data.json` | 154 bestaetigte Findings. Pro Seite ein Objekt mit `page`, `upstream` und `findings[]`. Jedes Finding: `line`, `severity`, `category`, `claim` (woertliches Ist-Zitat), `evidence` (Direktzitat der Quelle), `source_url`, `correction` (Ersatztext oder `ENTFERNEN`). |
| `cluster-final.json` | 103 Entscheidungen. Pro Eintrag `page`, `titel`, `frage`, `empfehlung` (ja/nein), `begruendung`, `tragweite` (hoch/mittel/niedrig), `zeilen[]` und ggf. `unsicher`. |
| `umsetzen.json` | Dieselben Entscheidungen minus der zurueckgestellten KabinXP-Entscheidung (102). **Das ist die Arbeitsgrundlage.** |
| `umsetzen-pages.json` | Seitenliste in Bearbeitungsreihenfolge. |
| `triage-final.json` | Bucket `AUTO` oder `REVIEW` je Finding, mit Begruendung. |
| `auto-per-page.json` | Die 17 AUTO-Findings nach Seite und Zeile. |
| `refuted.json` | 18 Findings, die die adversarische Gegenpruefung verworfen hat. Bereits aus `diff-data.json` entfernt — nur zur Nachvollziehbarkeit. |
| `forum-evidence.md` | Browser-Volltext von 14 x-plane.org-Seiten. Primaerquelle fuer die Forum-only-Plugins, weil WebFetch dort 403 liefert. |

---

## Wichtige Eigenheiten

**AUTO-Findings stehen nicht in den Entscheidungen.** `cluster-final.json` und
`umsetzen.json` enthalten ausschliesslich REVIEW-Findings. Die 17 AUTO-Eintraege
muessen aus `auto-per-page.json` separat mitgefuehrt werden — sie waeren bei
LinuxTrack beinahe verlorengegangen.

**Zwei Zeilenverweise gehen ins Leere.** `cockpit/xchecklist.md` Z15 und Z51
werden in Entscheidungen genannt, haben aber keinen Eintrag in `diff-data.json`.
Beide Stellen wurden bei der Umsetzung inhaltlich mitbehandelt.

**Die Review-Seite** liegt unter
`https://claude.ai/code/artifact/aa32a2fa-7ad1-476e-9b2f-93367c99232c` und wird
aus `diff-data.json` + `cluster-final.json` erzeugt:

```bash
python3 scripts/build_review_page.py \
  research/addons/faktencheck-2026-07-20/diff-data.json \
  research/addons/faktencheck-2026-07-20/cluster-final.json \
  /tmp/review.html "Plugin-Faktencheck — Freigabe"
```

---

## Kleines Rezept

Findings einer Seite anzeigen:

```bash
python3 -c "
import json, sys
p = sys.argv[1]
d = {x['page']: x for x in json.load(open('research/addons/faktencheck-2026-07-20/diff-data.json'))}
for f in d[p]['findings']:
    print(f\"Z{f['line']} [{f['severity']}] {f['claim']}\")
    print(f\"  -> {f['correction']}\")
" docs/en/addon/tools/xorganizer.md
```
