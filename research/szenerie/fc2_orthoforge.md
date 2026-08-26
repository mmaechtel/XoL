# Faktencheck Bereich 2 — ortho4xp.md: Installation/Versionen, OrthoForge, Pre-baked Daten, Sources

Datei: `docs/en/scenery/orthophotography/ortho4xp.md`
Prüfdatum: 2026-08-03

---

## B2-01 Codeberg-Retirement-Zitat

Behauptung (Z. 29): *"The Codeberg repository states: \"Due to changes in Codeberg policy, this repo will soon be deleted and hosted at https://xpconnect.me/orthoforge.html\". Use the project page as the entry point; any Codeberg link will break without notice."*

Urteil: BESTÄTIGT (Zitat wörtlich), mit Einschränkung

Beleg: https://codeberg.org/xbard/OrthoForge — Repo-Beschreibung: "Due to changes in Codeberg policy, this repo will soon be deleted and hosted at https://xpconnect.me/orthoforge.html" (abgerufen 2026-08-03). Repo existiert weiterhin und ist aktiv: letzter Commit 2026-07-28 18:36 UTC, "fix(console): encode build output as UTF-8 so non-Latin-1 OSM names cannot kill a build". Die Projektseite https://xpconnect.me/orthoforge.html ist erreichbar (HTTP 200), verlinkt aber selbst weiterhin ausschließlich auf Codeberg: "Get the repo from codeberg.org/xbard/OrthoForge (git clone, or the Download ZIP link)" — es gibt auf xpconnect.me keinen eigenen Download.

Tragweite: mittel

Vorschlag: Warnkasten beibehalten, aber den Halbsatz „Use the project page as the entry point" präzisieren, weil die Projektseite den Download nicht ersetzt: „Use the project page as the entry point; it points to the current source location. Der Download läuft derzeit weiterhin über Codeberg."

---

## B2-02 Lizenz, Maintainer, Herkunft, Credits

Behauptung (Z. 23–24): *"GPL v3, maintained by xbard"* / *"Started as the English fork of ORTHO4XP_V3 by Roland (Ypsos) and is now developed independently; changes are no longer synchronized with any upstream Ortho4XP branch. The project credits Oscar Pilote (original Ortho4XP), shred86 (1.40 line) and Roland/Ypsos (V3 architecture)"*

Urteil: BESTÄTIGT

Beleg:
- https://xpconnect.me/orthoforge.html — "Free & Open Source GPL v3"; "OrthoForge began as the English fork of Roland (Ypsos)'s ORTHO4XP_V3 and is now developed independently — it no longer tracks an upstream." (abgerufen 2026-08-03)
- https://codeberg.org/xbard/OrthoForge/raw/branch/main/README.md, Abschnitt Credits: "| Original Ortho4XP | Oscar Pilote |", "| 1.40 line | Shred86 |", "| V3 modern architecture | Roland (Ypsos) with Claude (Anthropic) |" (abgerufen 2026-08-03)
- Maintainer xbard: Codeberg-Namespace `xbard`, Ko-fi-Link https://ko-fi.com/xbard auf der Projektseite.

Tragweite: niedrig

Vorschlag: keine Änderung

---

## B2-03 „XP12 water and material paths are the default, not an option"

Behauptung (Z. 25): *"Targets X-Plane 12 — the XP12 water and material paths are the default, not an option"*

Urteil: Wasser BESTÄTIGT, Material FALSCH

Beleg:
- Wasser: https://codeberg.org/xbard/OrthoForge/raw/branch/main/docs/cfg-reference.md — "| `water_tech` | str | 'XP12' | 'Water tech type. XP12 uses native X-Plane 12 water rendering (WATER_COLOR_MASK). XP11 + bathy is no longer supported in V2.'" Ebenso `water_tech=XP12` in `OrthoForge.cfg.example`. (abgerufen 2026-08-03) → hier trifft „default, not an option" zu.
- Material: https://codeberg.org/xbard/OrthoForge/raw/branch/main/docs/xp12-materials.md — "**Status: shipped in v1.1, off by default.**" und "| `-1` (default), or any negative | Off. Nothing is written — byte-identical to older builds. |" (abgerufen 2026-08-03). Der XP12-Materialpfad (`terrain_super_roughness`/`SUPER_ROUGHNESS`) ist also genau das Gegenteil: eine Option, die standardmäßig aus ist.

Tragweite: mittel

Vorschlag: „Targets X-Plane 12 — the XP12 water path is the default and the XP11 path is gone; the XP12 terrain materials are available as an opt-in setting."

---

## B2-04 Python 3.10 als Mindestversion

Behauptung (Z. 43): *"Requires Python 3.10 or newer."*

Urteil: BESTÄTIGT

Beleg: https://xpconnect.me/orthoforge/installation.html, Tabelle „System requirements": Zeile Python, Spalte Minimum: "3.10"; Spalte Recommended: "3.12 or 3.13 (3.14 also works, see note)" (abgerufen 2026-08-03).

Anmerkung ohne Widerspruch zur Behauptung: `OrthoForge_Setup_Linux.sh` installiert in der Praxis Python 3.12 („python3.12 python3.12-venv python3-pip python3-tk p7zip-full"), und `setup_venv.sh` wird u. a. für Distributionen beworben, „that don't ship Python 3.12" (README Z. 74). 3.10 bleibt die dokumentierte harte Untergrenze.

Tragweite: niedrig

Vorschlag: keine Änderung

---

## B2-05 Linux-Setup: Skripte, PEP 668, --system-site-packages, tkinter/Pillow-Tk, GDAL, Distributionen

Behauptung (Z. 42–45): *"`OrthoForge_Setup_Linux.sh` runs a guided setup; `setup_venv.sh` is the plain-shell alternative for distributions with a locked-down system pip (PEP 668) and needs no root"* / *"The build runs from a virtual environment created with `--system-site-packages`, so it inherits system-installed tkinter and the optional GDAL bindings"* / *"Distribution packages needed beforehand: tkinter and Pillow's Tk bindings. GDAL is optional — the elevation path prefers rasterio"* / *"Setup is documented for Fedora, Debian/Ubuntu, Arch and openSUSE Tumbleweed"*

Urteil: BESTÄTIGT

Beleg:
- Beide Skripte existieren im Repo-Root: `OrthoForge_Setup_Linux.sh`, `setup_venv.sh` (Codeberg API contents, 2026-08-03).
- PEP 668 / kein Root: README Z. 74 — "For distros that lock system-level pip (Arch/CachyOS, PEP 668) or that don't ship Python 3.12, two small scripts do the whole thing inside the OrthoForge folder and touch nothing outside it"; installation.html: "no-GUI, no-sudo alternative for locked-pip distros (Arch / CachyOS and other PEP 668 setups)".
- venv + Systempakete: https://xpconnect.me/orthoforge.html — "sudo dnf install -y python3-tkinter python3-pillow-tk gdal-devel python3-gdal python3-devel" gefolgt von "python3 -m venv --system-site-packages venv".
- GDAL optional: installation.html, Tabelle System requirements, Zeile GDAL, Minimum: "not required (rasterio is bundled)", Recommended: "System `gdal` only if you want the `osgeo` fallback".
- Distributionen: installation.html — "Fedora 44 with Python 3.13" (Primärplattform), "Ubuntu 22.04+, Debian 12+, Arch, openSUSE Tumbleweed".
(alle abgerufen 2026-08-03)

Einschränkung, niedrig: `--system-site-packages` ist auf der Projektseite explizit im Fedora-Handpfad gezeigt, nicht als universelle Eigenschaft jedes Setups. Die Formulierung „The build runs from a virtual environment created with `--system-site-packages`" verallgemeinert leicht.

Tragweite: niedrig

Vorschlag: optional „The recommended manual path creates the virtual environment with `--system-site-packages`, so it inherits …"

---

## B2-06 Tabelle „What OrthoForge does differently" — alle vier Zeilen

Behauptung (Z. 35–38): pre-baked OSM gegen Rate-Limits; getrennte Land-/Seabed-Quellen über `custom_dem_search_dirs`/`custom_bathy_search_dirs`; abgestufte Flughafen-Zoomstufe statt einzelnem `cover_zl`-Schritt; XP12-Materialparameter inkl. Terrain-Rauheit in der Tile-Konfiguration.

Urteil: BESTÄTIGT (alle vier)

Beleg (alle abgerufen 2026-08-03):
- OSM/Rate-Limit: https://xpconnect.me/orthoforge.html — "Pre-baked OSM data source: ready-made per-tile OSM layers (coastline, water, roads, airports) from the OrthoForge data server, so covered tiles never hit an Overpass rate limit. Europe first, with automatic fallback to Overpass elsewhere."
- Land/Seabed getrennt: ebd. — "Separate land and seabed DEM sources — surveyed bathymetry kept apart from the land mesh, so land from Sonny's DTM and seabed from an INFOMAR composite never collide." Schlüssel `custom_dem_search_dirs` und `custom_bathy_search_dirs` sind beide in `OrthoForge.cfg.example` vorhanden.
- Abgestufter Flughafen-Zoom: docs/cfg-reference.md, `cover_airports_with_highres` — "\"Progressive\" auto-computes graduated ZL zones along the runway axes, stepping down from cover_zl at the runway to default_zl far out (see cover_screen_res, cover_fov, cover_fpa; cover_extent only applies to airports without runway data)."
- XP12-Rauheit: docs/xp12-materials.md — "OrthoForge can write an X-Plane 12 `SUPER_ROUGHNESS` value into every land `.ter` file it builds, controlled by one cfg key (`terrain_super_roughness`)."

Tragweite: niedrig

Vorschlag: keine Änderung. (Falls B2-03 umformuliert wird, passt Zeile 4 der Tabelle unverändert dazu — sie behauptet korrekt nur „exposes".)

---

## B2-07 Pre-baked OSM: Format, Handhabung, Abdeckung, Lizenz

Behauptung (Z. 493–497): maximale Straßendetailtiefe, lokal filterbar; Abdeckung unvollständig, Europa zuerst, Rückfall auf Overpass; bzip2-komprimiertes OSM-XML unter `OSM_data/<block>/<tile>/`, unverändert ablegen, nicht umbenennen, nicht entpacken; ODbL; kostenlos ohne Account.

Urteil: BESTÄTIGT

Beleg: https://xpconnect.me/orthoforge-data.html (abgerufen 2026-08-03) —
- "Ready-made OSM vector layers for Ortho4XP and OrthoForge."
- "The road layers are baked at the maximum road level, so Ortho4XP filters them down to whatever your own road_level setting is."
- "Anything not covered here still falls back to Overpass automatically, so nothing breaks."
- Format "standard OSM 0.6 XML, bzip2"; "Each file lands at OSM_data/<block>/<tile>/<tile>_<layer>.osm.bz2"; "Do not rename or unzip the .osm.bz2 files, and keep the folder names"
- "OSM data © OpenStreetMap contributors, ODbL."
- "Free for anyone, no account needed."
Abdeckung: Seite nennt "Europe first, growing"; README Z. 105 konkretisiert: "**Live coverage** (currently Ireland, 26 tiles, growing)".

Kleiner Detailfehler, niedrig: Die Doku listet die Layer als „(airports, roads, coastline, water)". Die Quelle nennt fünf Layer — `airports`, `big_roads`, `small_roads`, `coastline`, `water` — und das README zusätzlich `rail`.

Tragweite: niedrig

Vorschlag: „(airports, big and small roads, coastline, water)" — sonst keine Änderung.

---

## B2-08a Sonny-Spiegel: „authorised", Auflösungen, Format, Quelle der 0,5″-Daten

Behauptung (Z. 501): *"The same site hosts an authorised mirror of Sonny's elevation data, offered as standard SRTM-style `.hgt` tiles at 3″, 1″ and — for the United States, rebuilt from USGS 3DEP — 0.5″."*

Urteil: BESTÄTIGT

Beleg: https://xpconnect.me/sonny.html (abgerufen 2026-08-03) — "Mirrored with permission, no login"; "Redistributed here unmodified, with credit to Sonny"; "LiDAR elevation tiles at 0.5, 1 and 3 arcsec"; "One .hgt per 1° tile, delivered as a small .zip"; "Tiles shown in purple are our own 0.5″ bakes from the USGS 3D Elevation Program (3DEP)". Die Zuordnung der Doku ist korrekt: die 0,5″-Daten stammen NICHT von Sonny, sondern sind eigene Bakes des Spiegelbetreibers aus USGS 3DEP, nur für die USA. Gegenprobe bei Sonny selbst: https://sonny.4lima.de deckt ausschließlich Europa ab ("collect, edit and publish Digital Terrain Models of Europe", Länderliste Österreich … Vereinigtes Königreich) — Sonny hat also gar keine US-Daten.

Tragweite: niedrig

Vorschlag: keine Änderung

---

## B2-08b Sonny-Spiegel: „CC BY 4.0 and attributed to Sonny either way"

Behauptung (Z. 503): *"The data is CC BY 4.0 and attributed to Sonny either way."*

Urteil: FALSCH

Beleg: https://xpconnect.me/sonny.html (abgerufen 2026-08-03) — "Licensed CC BY 4.0"; die Namensnennung ist aber quellenabhängig: Sonnys Kacheln "carry the same credit", die eigenen US-Bakes verlangen "Elevation data courtesy of the U.S. Geological Survey 3D Elevation Program (3DEP)". Der Halbsatz „attributed to Sonny either way" steht damit im direkten Widerspruch zur Quelle — genau die 0,5″-US-Kacheln, die der Satz zwei Zeilen vorher korrekt als USGS-Ableitung ausweist, sind eben nicht Sonny zuzuschreiben.

Tragweite: mittel

Vorschlag: „The data is CC BY 4.0. Sonny's tiles are attributed to Sonny; the US 0.5″ bakes carry the USGS 3DEP credit instead."

---

## B2-08c Sonny-Spiegel: kein Link auf die Spiegelseite

Behauptung (Z. 499–503): Der ganze Abschnitt „Sonny DTM mirror" beschreibt einen Dienst auf „the same site", nennt aber keine URL; verlinkt wird nur https://sonny.4lima.de (die Originalquelle) und weiter oben https://xpconnect.me/orthoforge-data.html (die OSM-Seite).

Urteil: FALSCH (Lücke)

Beleg: Der Spiegel liegt auf einer eigenen Seite, https://xpconnect.me/sonny.html (HTTP 200, abgerufen 2026-08-03). https://xpconnect.me/orthoforge-data.html enthält ausweislich seiner Links (Codeberg, Datenserver, Ko-fi) und Überschriften ("Pre-baked OSM Data Tiles", "What this is", "Tiles covered", "Total size", "Layers / tile", "Data version", "Browse & download", "Selection", "How to use them") keinerlei DEM-, Sonny- oder HGT-Inhalte. Der Leser kann den beschriebenen Spiegel aus der Seite heraus also nicht erreichen.

Tragweite: mittel

Vorschlag: Am Ende des Absatzes ergänzen: „[Sonny DTM mirror](https://xpconnect.me/sonny.html)".

---

## B2-09 shred86-Fork: gepflegt? „recommended"? „better performance and more features"? Binaries?

Behauptung (Z. 16–20): *"**shred86's fork** (recommended)"*, *"Contains numerous improvements and new features"*, *"[Binaries for various operating systems]"*; ferner Z. 520: *"The shred86 fork offers better performance and more features"*.

Urteil: BESTÄTIGT (Projekt lebt), Wertung „better performance" UNBELEGBAR

Beleg (abgerufen 2026-08-03):
- GitHub API `repos/shred86/Ortho4XP`: `archived: false`, `pushed_at: 2026-07-04T18:12:26Z`; letzter Commit auf `master` 2026-05-01 ("Merge pull request #88 from shred86/dev").
- Releases: v1.40.13 vom 2026-05-01, davor v1.40.12 (2026-04-04), v1.40.11 (2025-10-30). Also laufende Releases, kein stagnierendes Projekt.
- Wiki: https://github.com/shred86/Ortho4XP/wiki/Installation (HTTP 200), zuletzt bearbeitet "Jun 8, 2026"; bietet vorgebaute Binaries für "Windows 10/11", "macOS 26", "Debian 13", "Arch Linux (2025.10.01)". (Anmerkung: die Binaries hängen nicht als GitHub-Release-Assets — alle Releases seit v1.40.04 haben leere Asset-Listen — sondern werden über die Wiki-Seite verteilt. Der Doku-Link zeigt korrekt aufs Wiki.)
- Vergleich Upstream: `oscarpilote/Ortho4XP` letzter Commit 2026-03-14 ("Update OSM provider configuration (#301)"), davor 2024-02-23 — der Fork ist tatsächlich der aktivere Zweig.
- Für „offers better performance" liegt keine Messung oder Herstelleraussage vor; das Wiki/README behauptet Performance nicht ausdrücklich.

Tragweite: niedrig (die Empfehlung selbst ist tragfähig)

Vorschlag: Z. 520 entschärfen zu „The shred86 fork is the actively maintained line and carries more features than the original" — Performance-Behauptung streichen, da unbelegt.

---

## B2-10 Sources — URL-Auflösung und Herausgeberangaben

Behauptung (Z. 570–575): sechs Quellenzeilen.

Urteil: 5× BESTÄTIGT, 1× FALSCH (Beschreibung), 1× UNBELEGBAR (Erreichbarkeit)

Beleg (HTTP-Prüfung 2026-08-03):
- https://github.com/oscarpilote/Ortho4XP → 200, Herausgeber Oscar Pilote korrekt (Repo-Owner `oscarpilote`). BESTÄTIGT
- https://github.com/shred86/Ortho4XP/wiki → 200, Herausgeber shred86 korrekt. BESTÄTIGT
- https://xpconnect.me/orthoforge.html → 200, „xbard, independently developed successor" korrekt (siehe B2-02). BESTÄTIGT
- https://xpconnect.me/orthoforge-data.html → 200, aber die Beschreibung „OrthoForge project, OSM and DEM mirrors" ist FALSCH: die Seite führt ausschließlich pre-baked OSM. Der DEM-/Sonny-Spiegel liegt auf https://xpconnect.me/sonny.html. Tragweite mittel.
- https://sonny.4lima.de → 200, „Sonny, elevation datasets for Europe" korrekt: "collect, edit and publish Digital Terrain Models of Europe", Lizenz "Creative Commons Attribution 4.0 (CC BY 4.0)". BESTÄTIGT
- https://forums.x-plane.org/index.php?/forums/forum/310-ortho4xp/ → HTTP 403 für automatisierte Zugriffe (bekannte Blockade, siehe Repo-Regel). Ob das Unterforum 310 noch existiert und noch „Ortho4XP" heißt, ist damit nicht überprüfbar. UNBELEGBAR.

Tragweite: mittel (nur die orthoforge-data-Zeile)

Vorschlag: Zeile 573 aufteilen bzw. korrigieren:
`- [Pre-baked OSM tiles](https://xpconnect.me/orthoforge-data.html) — OrthoForge project, ready-made OSM layers`
`- [Sonny DTM mirror](https://xpconnect.me/sonny.html) — OrthoForge project, mirrored elevation data`

---

## B2-11 Original von Oscar Pilote — „the original version with basic features"

Behauptung (Z. 12–14): *"**Original version** by Oscar Pilote … The original version with basic features"*

Urteil: BESTÄTIGT, mit Aktualitätsanmerkung

Beleg: GitHub API `repos/oscarpilote/Ortho4XP`, 2026-08-03: `archived: false`, `pushed_at: 2026-03-14T11:28:07Z`. Commit-Historie: 2026-03-14 "Update OSM provider configuration (#301)", davor 2024-02-23. Also seit Anfang 2024 praktisch nur noch ein einzelner Wartungs-Commit. Repo trägt keine SPDX-Lizenzangabe (`license: null` in der API), obwohl die Ableger GPL v3 als Ursprungslizenz nennen — für diese Seite ohne Folge.

Tragweite: niedrig

Vorschlag: keine Änderung (die Seite empfiehlt bereits den Fork)

---

## B2-12 Abschnitt „Installation Methods"

Behauptung (Z. 49–65): Binaries herunterladen/entpacken/ausführen; manuelle Installation mit Python 3.x und `pip install -r requirements.txt`; Linux-Alternativen Docker und pyenv.

Urteil: BESTÄTIGT

Beleg: `requirements.txt` existiert in beiden Repos (Codeberg/GitHub contents API, 2026-08-03). https://raw.githubusercontent.com/shred86/Ortho4XP/master/requirements.txt listet u. a. `numpy`, `pillow`, `pyproj`, `requests`, `Rtree`, `shapely`, `scikit-fmm` sowie plattformabhängige `gdal`-Pins. Binaries: siehe B2-09, https://github.com/shred86/Ortho4XP/wiki/Installation — "The download will contain the Ortho4XP application and a folder labeled `_internal` that contains all of the dependencies and files used by Ortho4XP." Docker- und pyenv-Verweise sind reposinterne Links.

Anmerkung ohne eigenen Befund: Das Wiki nennt für die manuelle Windows-Installation "Python 3.13.5"; die Doku sagt nur „Python 3.x" — das ist keine Falschaussage und entspricht der Repo-Regel zu Versionsnummern.

Tragweite: niedrig

Vorschlag: keine Änderung

---

# Zusammenfassung

| Urteil | Anzahl |
|---|---|
| BESTÄTIGT | 8 (B2-01, B2-02, B2-04, B2-05, B2-06, B2-07, B2-08a, B2-09, B2-11, B2-12 — davon B2-01/B2-05/B2-07/B2-09 mit Einschränkung) |
| FALSCH | 4 (B2-03 Materialhälfte, B2-08b, B2-08c, B2-10 Teilzeile) |
| VERALTET | 0 |
| UNBELEGBAR | 1 (forums.x-plane.org, 403; zusätzlich die unbelegte Performance-Wertung in Z. 520) |

Tragweite hoch: keine. Der Leser läuft nirgends in eine Sackgasse — Codeberg lebt, der shred86-Fork lebt, alle Quellen-URLs lösen auf.
