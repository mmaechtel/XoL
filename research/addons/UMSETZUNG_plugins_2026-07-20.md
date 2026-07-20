# Umsetzungsstand: Plugin-Faktencheck

**Datum:** 2026-07-20
**Branch:** `faktencheck-plugins-2026-07`
**Stand:** 13 von 46 Seiten umgesetzt, 15 Commits, Working Tree sauber

---

## Wo weitermachen

Die naechste Seite ist `docs/en/addon/flylua_scripts/simloadmanager.md`.

Alle Eingangsdaten liegen im Session-Scratchpad:

| Datei | Inhalt |
|-------|--------|
| `diff-data.json` | 154 bestaetigte Findings mit Zitat, Beleg, Quell-URL, Korrekturtext |
| `cluster-final.json` | 103 Entscheidungen (Titel, Frage, Empfehlung, Tragweite, Zeilen) |
| `umsetzen.json` | dieselben 103 minus der zurueckgestellten KabinXP-Entscheidung |
| `umsetzen-pages.json` | Seitenliste in Bearbeitungsreihenfolge |
| `triage-final.json` | Bucket AUTO/REVIEW je Finding |
| `auto-per-page.json` | die 17 AUTO-Findings nach Seite |
| `forum-evidence.md` | Browser-Volltext der 14 x-plane.org-Seiten |

Pfad: `/tmp/claude-1000/-home-maechtel-Work-Git-XoL/<session>/scratchpad/`

**Achtung:** Das Scratchpad ist sessiongebunden. Ist es weg, muss der Faktencheck neu laufen — dann ueber `/faktencheck-bulk addon`. Die Review-Seite liegt unter
`https://claude.ai/code/artifact/aa32a2fa-7ad1-476e-9b2f-93367c99232c`.

---

## Erledigt (13 Seiten)

| Seite | Kern der Aenderung |
|-------|--------------------|
| `cockpit/anyairline.md` | Linux-Build bringt kein FFmpeg mit (Aussage war falsch); Open-Beta-Status |
| `cockpit/avitab.md` | komplett auf TeamAvitab-Fork; PDF-Crash-Abschnitt entfaellt (14 Zeilen) |
| `cockpit/kabinxp.md` | unbelegter Entwicklername ersetzt |
| `cockpit/linuxtrack.md` | Qt6/CMake-Build-Deps; GUI-Verbot zu Empfehlung; Install-Tab korrigiert |
| `cockpit/opentrack.md` | unbelegte Freeze-Behauptung durch echten Grund ersetzt (2 Stellen) |
| `cockpit/terrainradar.md` | Stagnation seit v1.31; 12.3-Aussage praezisiert |
| `cockpit/xcamera.md` | Kompatibilitaetszusatz; falsche Quellen (OpenTrack) ersetzt |
| `cockpit/xchecklist.md` | sw_remark-Mechanismus an 2 Stellen korrigiert; Bezugsquelle |
| `cockpit/xpwalkaround.md` | Beta-Status, Skydiving-Feature, Windows-Vorbehalt zu SimpleWalkaround |
| `flylua_scripts/3drainspeedstop.md` | erfundener AGL-Bezug an 2 Stellen entfernt |
| `flylua_scripts/rain_rate.md` | Nutzen auf den Zweck des Autors umgestellt |
| `flylua_scripts/sges.md` | unbelegter Ablageort der Updater-Konfiguration entfernt |
| `flylua_scripts/simbrief_simple_ofp.md` | zwei unbelegte Feature-Bullets gestrichen |

---

## Offen (33 Seiten)

`cockpit` 1 (`xtextureextractor`) · `flylua_scripts` 4 (`simloadmanager`,
`simreaperxp`, `simscreenoverlay`, `xproturb`) · `kvm` 3 · `scenery_addons` 5 ·
`scripting` 2 · `sounds` 2 · `toliss` 4 · `tools` 6 · `traffic` 6

Fuer die naechsten fuenf Seiten sind die Zielzeilen bereits ermittelt —
`simloadmanager` Z17/21/36/55, `simreaperxp` Z23/37/39, `simscreenoverlay` Z22,
`xproturb` Z41, `xtextureextractor` Z15/23/24.

---

## Arbeitsregeln fuer die Fortsetzung

1. **Eine Seite pro Commit**, EN und DE gemeinsam. Kein Parallelbetrieb — ausdrueckliche Vorgabe des Betreibers.
2. **AUTO-Findings mitfuehren.** Sie stehen NICHT in den Entscheidungskarten, sondern in `auto-per-page.json`. Sie waeren bei LinuxTrack beinahe verlorengegangen.
3. **Entscheidungen mit `empfehlung: nein` nicht umsetzen** — im Commit vermerken, dass und warum sie ausbleiben.
4. **Folgestellen mitziehen.** Wenn eine Korrektur eine zweite Stelle derselben Seite widersprüchlich zurueckliesse, diese mitaendern und im Commit nennen (bisher: AviTab Chart-Pfad Z51, OpenTrack Einleitungssatz Z23, Xchecklist Linux-Abschnitt Z51).
5. **Kontrolle nach jeder Seite:** Zeilenzahl EN gegen DE, dann `mkdocs build` (muss ohne Warning/Error durchlaufen).
6. **Kein Inhaltsverlust.** Nur streichen, wo die Entscheidung es ausdruecklich vorsieht.

---

## Zurueckgestellt

**`cockpit/kabinxp.md` — Linux-Hinweis auf Fat-Plugin-Layout.** Die Pruefung
schreibt selbst, dass niemand den Archivinhalt verifiziert hat, dass es fuer den
Dateinamen keine Quelle gibt und dass die bisherige Formulierung "nicht schlicht
falsch" ist. Eine unbelegte Aussage durch eine andere zu ersetzen waere das
Gegenteil eines Faktenchecks. Wird nur auf ausdrueckliche Anweisung nachgezogen.

---

## Am Ende faellig

- Changelog in `docs/de/index.md` und `docs/en/index.md`: **ein** komprimierter Sammeleintrag, keine Einzelliste. Maximal 3 Datumsbloecke, `index.md` zuletzt aendern.
- Abschliessender `mkdocs build`.
- Merge nach `main` bzw. Abschluss ueber `/abschluss`.

---

## Abweichungen von der Empfehlung

`cockpit/xpwalkaround.md`: Der Windows-Vorbehalt zu SimpleWalkaround wurde
aufgenommen, obwohl die Empfehlung "nein" lautete — auf ausdrueckliche Vorgabe
des Betreibers.

---

## Bekannte Einschraenkung

`docs/assets/video` ist ein Symlink auf `/mnt/videos/XoL/video`. Ist das Share
nicht gemountet, bricht `mkdocs build` mit `FileNotFoundError` ab. Das ist kein
Fehler der Aenderungen.
