# Umsetzungsstand: Plugin-Faktencheck

**Datum:** 2026-07-26 (begonnen 2026-07-20)
**Branch:** `faktencheck-plugins-2026-07`
**Stand:** 22 von 46 Seiten umgesetzt, Working Tree sauber

---

## Prompt fuer die naechste Session

> Setze den Plugin-Faktencheck auf Branch `faktencheck-plugins-2026-07` fort.
> Stand und Arbeitsregeln: `research/addons/UMSETZUNG_plugins_2026-07-20.md`.
> Rohdaten (Findings, Entscheidungen, AUTO-Liste): `research/addons/faktencheck-2026-07-20/`
> — Format und Extraktions-Rezept im dortigen README. Naechste Seite:
> `docs/en/addon/scenery_addons/lst.md`. Pro Seite: Findings + Entscheidungen +
> AUTO per Skript ziehen, EN zuerst aendern, DE angleichen, Zeilenzahl EN==DE
> pruefen, `mkdocs build`, ein Commit pro Seite. Entscheidungen mit
> `empfehlung: nein` nicht umsetzen, aber im Commit vermerken.
> Token-sparsam: nur Zielstellen der Seiten lesen (grep + Read mit offset).

## Wo weitermachen

Die naechste Seite ist `docs/en/addon/scenery_addons/lst.md`.
Die Findings zu den restlichen `scenery_addons`-Seiten (lst, noaa_weather,
xa-snow, xroad) sind bereits extrahiert und unauffaellig bis auf:
lst Z14 (XP11) hat `empfehlung: nein`; bei xa-snow ist der Ersatz-Paketname
`libcurl3t64-gnutls` trixie-spezifisch (Formulierung beachten).

Alle Eingangsdaten liegen versioniert in `research/addons/faktencheck-2026-07-20/`
(Dateibeschreibung und Extraktions-Rezept: dortiges README). Die Review-Seite liegt unter
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
| `flylua_scripts/simloadmanager.md` | Flugzeugliste/Q4XP/Features aktualisiert; XP11 bewusst nicht |
| `flylua_scripts/simreaperxp.md` | Cloud-Shadow praezisiert; Repo statt Releases; Dateiname |
| `flylua_scripts/simscreenoverlay.md` | Menuepfad um Plugins-Praefix ergaenzt ("window" bewusst nicht) |
| `flylua_scripts/xproturb.md` | Wetter-Integration + Turbulenz-Vorwarnung ergaenzt |
| `cockpit/xtextureextractor.md` | Stagnationshinweis; Play-Store-Halluzination; JDK-Voraussetzung |
| `kvm/mobiflight.md` | Netzwerk-Split: Connector kann nur 127.0.0.1, UDP-Relay Pflicht |
| `kvm/myfs_flights.md` | Connector statt erfundenem Plugin mit IP-Einstellung |
| `kvm/sayintentions.md` | P3D v6 raus, 650+ neutralisiert, Traffic Injection gestrichen; Entourage bewusst nicht |
| `scenery_addons/aep.md` | v2-Stand: XP12-only, AEP Live, Payware-Installation, VRAM |

---

## Offen (24 Seiten)

`scenery_addons` 4 (`lst`, `noaa_weather`, `xa-snow`, `xroad`) ·
`scripting` 2 · `sounds` 2 · `toliss` 4 · `tools` 6 · `traffic` 6

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
