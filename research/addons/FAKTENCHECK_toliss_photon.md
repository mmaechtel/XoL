# Faktencheck: ToLiss Photon (EN + DE)

**Datum:** 2026-08-16
**Geprüfte Seiten:** `docs/{en,de}/addon/toliss/toliss_photon.md`
**Primärquellen:** forums.x-plane.org/files/file/100717 (Downloadseite), github.com/ischmal/toliss-photon-lighting (Quellcode, README, Release-Assets, Build-Workflow)

---

## Hinweis zur Quellenlage

x-plane.org blockiert WebFetch mit HTTP 403; die Downloadseite wurde über die Chrome-Automatisierung gelesen. Anders als bei den meisten Addons existiert hier eine zweite, härtere Quelle: das Projekt ist Open Source (GPL-3.0), sodass README, Installer-Quellcode und der Release-Workflow direkt geprüft werden konnten. Die Linux-Angaben auf der Doku-Seite stammen überwiegend aus dieser zweiten Quelle, nicht aus der Forumsbeschreibung.

Der Mod ist neu (erste Veröffentlichung Juli 2026, laufende Updates). Versionsnummern stehen der Konvention entsprechend nicht auf der Seite.

## Bestätigt

| # | Behauptung | Beleg |
|---|------------|-------|
| 1 | Entwickler schmal, Cockpitbeleuchtung von Gus Rodrigues mit Genehmigung integriert | README „Credits": „interior (cockpit) lighting is entirely the work of GusRodrigues … included here with his permission" |
| 2 | Unterstützt A319, A320 (CEO/NEO), A321 (CEO/NEO), A330-900 | README „Supported Aircraft" |
| 3 | GPL-3.0 | `LICENSE` im Repo, README „Usage": „licensed under the GNU General Public License v3.0" |
| 4 | Natives Plugin, kein XPPython3/FlyWithLua nötig | README „Components": „compiled native plugin, so it needs no XPPython3, FlyWithLua, or other add-on" |
| 5 | Billboards vs. Spill Lights, fehlende Richtung als Ursache des flachen Erscheinungsbilds | README „How it Works" |
| 6 | Richtung für jedes Licht außer oberem/unterem Beacon | README „How it Works": „specifies a light direction for everything except the upper and lower beacons" |
| 7 | Plugin überschreibt pro Frame die Helligkeits-Datarefs des Simulators für Beacon/Strobe, ersetzt Sinus-Blende | README „How it Works": „runs a function every frame that overrides specific DataRefs set by ToLiss"; `plugin.cpp:577`, `plugin.cpp:589` |
| 8 | Fünf Profile Classic / Hybrid LED / Full LED / Auto / Custom, neun Einzellichter | README „Available Light Profiles" (acht); `plugin.cpp:111`+`124` — Positionslichter als neunte Kategorie |
| 9 | Cockpitsatz: Old Halogen / New Halogen / LED, nicht für A330-900 | README „Interior (Cockpit) Lighting": „Not available for the A330-900" |
| 10 | Einstellungen pro Livery gespeichert, Umschalten im geladenen Flugzeug | Forumsseite „General" |
| 11 | Farbcharakteristik Halogen/LED/Xenon inkl. Pinkstich des Xenon-Beacons | README „Color Effects" |
| 13 | Linux-Release als `.tar.gz`, x86_64 | Release-Asset `ToLissPhoton-Installer-v0.9-Linux.tar.gz`; Workflow-Matrix `{ os: ubuntu-latest, arch: lin_x64 }` — kein ARM-Job |
| 14 | Installer und `data/` müssen zusammenbleiben, `chmod +x`, Autoerkennung von X-Plane 12 | `build/readme.py`, Linux-Zweig der Installationsschritte |
| 15 | Schwarzes Fenster → `photon-installer-console` oder `--software` | Am Forum-Download geprüft: Konsolen-Binary liegt bei, `./photon-installer --help` führt `--tui` und `--software` |
| 16 | Ordnerauswahl über `zenity`, sonst `kdialog`, sonst Pfad eintippen | `src/native/src/installer/platform.cpp:207-222`, `platform.h:90-94` |
| 17 | Installer deinstalliert und stellt Originaldateien zurück | README „Interior": „Uninstalling puts all of it back"; `screens.cpp`: „Uninstall complete — original ToLiss lighting restored" |
| 18 | Reihenfolge: erst Wing-Mod, dann Photon; bei RealWings werden dessen Lichtobjekte gepatcht, bei Durantula eine passende Variante eingespielt | Forumsseite Schritt 3; `core/patch_realwings.h:5-7`, `core/wingmod.h:15-16` |
| 19 | SkunkCrafts-Update setzt die OBJs zurück, Versionsmarker erkennt das | `src/native/src/core/marker.h`: „an aircraft update (SkunkCrafts) reverted the OBJ to stock out from under us" |
| 20 | Backups unter `Photon Backup Files/` | `marker.h` (Bookkeeping in `Photon Backup Files/`) |
| 21 | Gus' Paket von Hand nach Photon installiert überschreibt die Außenlichter | README: „his package contains its own exterior light object, which would overwrite Photon's and silently revert the exterior mod" |
| 22 | Performance: Cockpitlicht und Backlight erzeugen zusätzliche Spill Lights und kosten GPU-Zeit; vereinfachter Modus fasst die Panel-Flutlichter zusammen | README „Reduced light count"; `plugin.cpp:2988-3014` (Settings-Tab, Abschnitt „Performance") |

## Bewusst nicht übernommen

- **Versionsnummern und Changelog-Einträge:** Plugin-Versionskonvention — die Seite beschreibt den Funktionsstand, nicht die Release-Historie. Betrifft insbesondere „neu in v0.9"-Formulierungen der Forumsseite.
- **Roadmap (A340-Support, FCU-Farben, SkunkCrafts-Integration):** Ankündigungen ohne Umsetzungsstand.
- **Bekanntes Problem A321-Bugfahrwerk/Landing-Billboards:** versionsgebundener Einzelfall, laut Entwickler in Bearbeitung. Nicht aufgenommen, um die Seite nicht an einen Releasestand zu binden.
- **Testerliste und Discord-Community:** ohne Nutzwert für die Doku.
- **„painstakingly adjusted by hand" / Qualitätsaussagen des Entwicklers:** nicht prüfbar, die Seite beschreibt stattdessen den technischen Mechanismus.
- **Zusammenspiel mit [Bay's Lighting Mod](../../docs/en/addon/scenery_addons/bays_lighting_mod.md):** beide verändern Flugzeug-Positions- und Beacon-Lichter, aber auf unterschiedlichen Ebenen (Texturen/Sprites global vs. OBJ des ToLiss). Keine Quelle äußert sich zum Parallelbetrieb — daher kein Hinweis auf der Seite statt einer Vermutung.
- **Genaue Laufzeitabhängigkeiten des Linux-GUI-Installers:** inzwischen am ausgelieferten Binary geprüft (fontconfig/freetype dynamisch, X11/GL per `dlopen`, libstdc++ statisch). Die Seite nennt weiterhin nur den Ausweg (`--software`, Konsolenvariante) statt einer Paketliste — siehe „Nicht übernommene Ergänzungen".

## Linux-Relevanz

Die Seite ist trotz „Flugzeug-Mod" für XoL einschlägig: Der Installer bringt eine eigene Linux-Binärvariante mit, das GUI-Problem (schwarzes Fenster auf VM/Remote/alten Treibern) trifft genau die hier dokumentierten Setups, und die Ordnerauswahl hängt an `zenity`/`kdialog`, die auf einem schlanken Desktop fehlen können. Plattformunabhängige Teile (Lichtprofile, Farbcharakteristik) sind knapp gehalten und dienen der Einordnung des Mods.

---

## Gegenprüfung 2026-08-16 (vier parallele Prüfstränge)

Nach dem Erstentwurf wurden Mechanik, Linux-Installer, Luftfahrtangaben und Sprache getrennt gegengeprüft. Ergebnis:

### Entfernt statt korrigiert

- **A320-Lichthistorie (Jahreszahlen 2015/2022, MFRL):** Der Absatz stammte aus der Entwicklerdarstellung und hielt der Prüfung gegen Airbus-Primärquellen nicht stand. Im Airbus-Dokument „A320 Aircraft Characteristics — Airport and Maintenance Planning" fehlt MFRL in der Ausgabe 03/2022 vollständig und erscheint erst mit der Revision 05/2023; Airbus rollt es laut eigener Newsroom-Meldung 2026 noch über STEP4 auf die neo-Familie aus. Zudem war LED-Außenbeleuchtung beim A320neo bereits ab EIS 2016 Serie. Der Absatz wurde ersatzlos gestrichen — Serienstände realer Airbus-Muster sind nicht Gegenstand dieser Dokumentation.
- **Benchmark-Aussage des Entwicklers** („keine messbare Auswirkung von Außenlichtern und Bildschirmeffekten"): im Quellcode nicht belegt, das Performance-Werkzeug des Plugins formuliert die Erwartung ausdrücklich als Vermutung (`plugin.cpp:8250`). Entfernt, statt sie als Entwicklerzitat zu führen.
- **Vergleich früher CEO gegen aktuellen NEO:** setzte reale Flottenausstattung voraus. Ersetzt durch eine Aussage über die Wahlmöglichkeiten des Mods.

### Präzisiert

| Punkt | Vorher | Jetzt | Beleg |
|-------|--------|-------|-------|
| Datarefs | „überschreibt die Intensitäts-Datarefs von ToLiss" | überschreibt die Helligkeits-Datarefs des Simulators, die ToLiss selbst bespielt | `plugin.cpp:577`, `plugin.cpp:589` („ToLiss's ExternalLightBrightnesses array is READ-ONLY to other plugins") |
| Custom-Kategorien | acht Lichter | neun, inklusive Positionslichter | `plugin.cpp:111` (`NCAT = 9`), `plugin.cpp:124` (`"nav"`) |
| Cockpit-Varianten | „sehr warmweiß, neutralweiß, kaltweiß" | warmes Orange, helleres Amber, Kaltweiß | README „Interior (Cockpit) Lighting" |
| Wing-Mods | „patcht deren Dateien" | patcht nur die Lichtobjekte von RealWings; für Durantula wird eine passend gebaute Variante eingespielt | `core/patch_realwings.h:5-7`, `core/wingmod.h:15-16` |
| Displayleuchten | als Teil der Cockpitbeleuchtung geführt | eigener Punkt, unabhängig vom Cockpit-Mod und auch auf dem A330-900 | `core/constants.cpp:86-92` (`ScreensAirframes()` enthält a339) |

### Bestätigt gegen das tatsächliche Download-Paket

Die Linux-Angaben wurden am ausgelieferten Archiv geprüft, nicht nur am Quellcode. Wichtig dabei: Das GitHub-Release hängt hinter dem Forum-Download zurück. Im Forum-Paket liegen `photon-installer` **und** `photon-installer-console`; `./photon-installer --help` führt `--tui` (Textmodus für SSH/headless) und `--software` (CPU-Rendering, wörtlich „Use this if the installer window opens BLACK or blank") auf. Die Angaben der Seite treffen damit den Download, den sie verlinkt. Ebenfalls am Paket bestätigt: `.tar.gz`, gesetztes Ausführungsrecht, `data/`-Layout mit `plugin/ToLissPhoton/lin_x64/`, kein ARM-Build.

### Offen

- **Abschaltbarkeit der Cockpitbeleuchtung:** Die Seite sagt, beide Effekte ließen sich reduzieren oder ganz abschalten. Im Settings-Tab abschaltbar ist ausweislich `plugin.cpp:2992` nur die Display-Hintergrundbeleuchtung; für die Cockpitbeleuchtung gibt es dort den vereinfachten Modus (`plugin.cpp:3014`) und einen Helligkeitsregler mit Untergrenze 1.0 (`core/patch_intensity.h:44`). Wird am laufenden Simulator gegengeprüft, bevor die Formulierung geändert wird. Zugang: X-Plane-Menü Plugins → ToLiss Photon → eine beliebige Zeile öffnet das Plugin-Fenster, Reiter „Settings".

### Nicht übernommene Ergänzungen

Aus der Installer-Prüfung belegt, aber (noch) nicht auf der Seite: die Autoerkennung durchsucht nur Home, `/opt`, `/usr/local` und Steam-Bibliotheken, sodass eine Installation auf einem zweiten Datenträger von Hand angegeben werden muss (`XPLANE_ROOT` oder `--xplane-root`, `core/detect.cpp`); X-Plane muss beim Installieren geschlossen sein (Prozessprüfung auf `X-Plane-x86_64`, `core/detect.h:47-51`); es gibt einen vollständig nicht-interaktiven CLI-Modus; der GUI-Installer braucht fontconfig/freetype und lädt X11/GL nach, libstdc++ ist statisch gelinkt.
