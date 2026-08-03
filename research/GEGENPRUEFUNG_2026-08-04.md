# Adversarische Gegenprüfung — 2026-08-04

Gegenstand: die fünf Seitenpaare aus `WORK_ORDER_gegenpruefung_2026-08-04.md`.
Methode: neun Agenten mit Widerlegungsauftrag (nicht Bestätigungsauftrag), plus
Browser-Automatisierung für `forums.x-plane.org`. Belege durchgehend mit Pfad +
Zeilennummer oder URL + wörtlichem Zitat. Im Zweifel gilt „nicht gesichert".

Primärbelege: lokale Ortho4XP-Installation `/mnt/xplane_data/docker/Ortho4XP/`
(die relevanten `src/`-Dateien wurden gegen `shred86/Ortho4XP@master` als
byte-identisch verifiziert; nur `O4_OSM_Utils.py` trägt einen lokalen Patch),
lokale X-Plane-12.4.3-Installation, lokale X-World-Pro-Installation, Repos,
Herstellerseiten.

---

## Teil A — Widerlegt oder zu korrigieren

### A1 Ortho4XP — Parameter

| # | Seitenaussage | Befund | Beleg |
|---|---|---|---|
| A1.1 | `masking_mode` „Which texture the mask blends toward" | **Widerlegt.** Keine Textur beteiligt. `sand`/`rocks`/`3steps` sind drei Blur-/Blend-**Algorithmen**, die eine 8-Bit-Graustufen-Alphamaske erzeugen | `O4_Mask_Utils.py:648` `def blur_mask(img_array, tile, sea_level):`, Zweige `:666`, `:681`, `:730`; `O4_Cfg_Vars.py:240` „A selection of three tentative masking algorithms" |
| A1.2 | `road_level=1` „motorways, primary and secondary roads, railway lines" | **Unvollständig.** `trunk` fehlt | `O4_Vector_Map.py:261-268`: `motorway`, `trunk`, `primary`, `secondary`, `railway=rail`, `railway=narrow_gauge` |
| A1.3 | Global-only-Liste (8 Schlüssel) | **Unvollständig.** `list_app_vars` hat 16 Einträge; es fehlen `check_tms_response`, `http_timeout`, `max_connect_retries`, `max_baddata_retries`, `ovl_exclude_pol`, `ovl_exclude_net` | `O4_Cfg_Vars.py:364-380` |
| A1.4 | `custom_dem` „requires GDAL" | **Zu absolut.** `.hgt` liest numpy direkt; GDAL nur für Nicht-HGT-Raster. Auch EPSG:4269 wird akzeptiert | `O4_DEM_Utils.py:443-465`, `:504`, `:536-537` („let's be blind about 4269") |
| A1.5 | `custom_dem` „areas it does not cover are mapped to elevation 0" | **Widerlegt** (es ist der Upstream-Hint, nicht das Verhalten). Abfragen werden in die Rasterausdehnung **geklemmt** → Fortsetzung des Randwerts | `O4_DEM_Utils.py:242-245` `x = max(x, self.x0); x = min(x, self.x1)`; `Utils/src/Triangle4XP.c:3571-3596` klemmt gar nicht |
| A1.6 | `apt_smoothing_pix` „Gaussian blur" | **Doku-treu, code-falsch.** Implementierung ist ein separabler Dreieckskern (Tent) | Hint `O4_Cfg_Vars.py:123` vs. `O4_DEM_Utils.py:932-952` `kernel = numpy.array(range(1, 2*(pix_width+1)))` |
| A1.7 | `limit_tris` „At `0` a hard limit of 5 million applies" | **Unvollständig.** Auch Werte ≥ 50 Mio. fallen auf 5 Mio. zurück | `O4_Mesh_Utils.py:643-647` `if max_tris <= 0 or max_tris >= 5e7: max_tris = 5e6` |
| A1.8 | Zeile 389: „`cover_extent`, **the radius** in kilometers … the covered surface roughly a hundredfold" | **Widerspricht der eigenen Zeile 164** („It is a margin, not a radius"). Bei einem Rand auf eine Bounding Box hängt der Flächenzuwachs von Größe und Form des Flughafens ab; „hundertfach" ist nicht haltbar | `O4_DSF_Utils.py:143-148` |
| A1.9 | `ratio_bathy` | Kernaussage **bestätigt** (siehe B), aber **fehlender Vorbehalt**: ohne `distance_masks_too=True` (Default `False`) bleibt `node_bathy = 255` und der Parameter ist wirkungslos; Ergebnis wird auf `[0.1, 1]` geklemmt, `0` ergibt also `0.1` | `O4_Bathymetry.py:190`, `:205-219`; `O4_Cfg_Vars.py:254-256` |
| A1.10 | `masks_width` „Width of the mask transition zone" | **Ungenau.** Upstream: „Maximum extent of the masks perpendicularly to the coastline"; in `rocks` wirkt effektiv die Hälfte | `O4_Cfg_Vars.py:231-235`; `O4_Mask_Utils.py:661-662` `blur_width = tile.masks_width / (2 * pxscal)` |
| A1.11 | `fill_nodata` | **Fehlender Vorbehalt**: auch bei `True` wird ein Raster mit zu vielen No-Data-Werten still genullt | `O4_DEM_Utils.py:51-61` („Dataset contains too much no_data to be filled.") |
| A1.12 | `min_area` „Contiguous water surfaces are merged **before** the area is computed" | Bestätigt, aber der Merge hängt an `clean_bad_geometries` (Default `True`) | `O4_Vector_Map.py:549-565` |

### A2 Ortho4XP — Datenquellen und Umfeld

| # | Seitenaussage | Befund | Beleg |
|---|---|---|---|
| A2.1 | „plus 0.5″ tiles for the United States" | **Teilweise falsch.** Der Mirror führt 0,5″ auch für die Alpen (Österreich, Schweiz) — Sonnys eigene Daten. Von 579 Kacheln zu `0.5s` sind 546 USGS, 33 alpin | `xpconnect.me/sonny/dem/manifest.json`; sonny.4lima.de: „For the alpine countries Austria and Switzerland only I also created finer models (0.5" and 10m)" |
| A2.2 | „The mirror is a convenience copy limited to what the OrthoForge project has staged. sonny.4lima.de remains the canonical source with the complete coverage" | **Widerlegt.** Der Mirror ist bei den 546 US-3DEP-Kacheln eine **Obermenge** — die gibt es auf sonny.4lima.de gar nicht. (Die Mirror-Seite behauptet dasselbe falsch; wir haben den Fehler übernommen) | manifest.json + sonny.4lima.de (Europa-only) |
| A2.3 | OrthoForge-Setup „documented for Fedora, Debian/Ubuntu, Arch and **openSUSE Tumbleweed**" | **Widerlegt.** Quelle sagt „Fedora, Debian/Ubuntu, Arch and **macOS**". `INSTALL_PREREQUISITES.py` kennt nur `apt-get`/`dnf`/`pacman`, kein `zypper`. openSUSE steht nur als Nebenbemerkung | OrthoForge-README + orthoforge.html |
| A2.4 | „`XP11 + bathy` water is no longer supported **at all**" | **Zu absolut.** Quelle: „XP11 + bathy is no longer supported **in V2**" | `docs/cfg-reference.md:147` |
| A2.5 | Codeberg-Warnung als Repo-Aussage | **Fundstelle falsch.** Der Satz steht in der **Repo-Beschreibung**, nicht im README | codeberg.org API `repos/xbard/OrthoForge` |
| A2.6 | `1302 flatten 1`: „Many sceneries … were originally designed for X-Plane's old, flat mesh model … `1302 flatten 1` may be set" | **Kausal verdreht.** `flatten` wurde mit X-Plane 10.50 (2016) **eingeführt**, gerade weil das globale Flattening wegfiel — ein modernes Opt-in, kein Altlast-Flag | developer.x-plane.com/2016/03/per-airport-flattening/ |
| A2.7 | „**X-Plane 12** no longer offers the old ‚runways follow terrain contours' option" | **Widerlegt — falsche Version.** Entfernt mit **X-Plane 11** | developer.x-plane.com/2017/01/where-have-all-my-settings-gone/: „Runways Follow Contours: this is now always on; individual airports can be marked for flattening on a per-airport basis." |
| A2.8 | „often a larger surrounding area" | **Zu weich.** Laut Laminar immer | developer.x-plane.com/2007/10/how-flat-is-flat/: „a 'hard' flatten of an area including the airport and some surrounding area … destroys … a lot of surrounding terrain" (Quelle von 2007) |
| A2.9 | Forum-Link `…/forums/forum/310-ortho4xp/` (2×) | **Widerlegt.** ID 310 existiert nicht mehr und leitet auf Forum 4 „ScreenShots And videos" um. Richtig ist **322**. Die `index.php`-Form ist *nicht* veraltet — beide Formen lösen identisch auf und kanonisieren auf die kurze Form | Browser: 310 → canonical `/forums/forum/4-screenshots-and-videos/`; 322 → „Ortho4XP - X-Plane.Org Forum", HTTP 200 |
| A2.10 | „Download the appropriate version for your operating system" / „Binaries for various operating systems" | **Irreführend.** Es gibt keine GitHub-Release-Assets; das Wiki verlinkt **Google-Drive-Dateien** mit SHA-256, für genau vier Ziele: Windows x86-64, macOS ARM-64, Debian 13 x86-64, Arch x86-64 | Wiki `Installation`, Abschnitt „Download Links"; GitHub-API: alle Releases ohne Assets |

### A3 XPME

| # | Seitenaussage | Befund | Beleg |
|---|---|---|---|
| A3.1 | „The license terms name no refund policy — a refund has been granted case by case in the issue tracker, but do not count on it." | **Widerlegt.** Die Lizenzseite hat einen eigenen Abschnitt | aiflygo.com/docs/license/: `<h1 id="ask-for-refund">Ask for refund</h1>` … „The refund period is 7 days after I sent out the license." (schon im Wayback-Snapshot 2025-11-26). Der Fehler stammt aus `fc5_xpme.md` B5-06 — dort mitkorrigieren |
| A3.2 | „started before X-Plane **so that the virtual filesystem is mounted**" | **Unbelegte Begründung.** Reihenfolge ist belegt, die Begründung nicht. Anbieter begründet nur generisch: „This ensures that all operations performed by the Mod are completely cleaned up." | aiflygo.com `usage/`, `faq/` |
| A3.3 | „published under the **AIFlyGo brand**" | **Nicht herstellerbelegt.** „aiflygo" kommt auf den Seiten nur in der URL `k.aiflygo.com` vor; Seitentitel lauten „MSFS/XPlane Map Enhancement" | Volltext der vier Doku-Seiten |
| A3.4 | Basispakete aus „a modified Ortho4XP fork" | Herstelleraussage bestätigt, **aber** das verlinkte Fork-Repo `github.com/derekhe/Ortho4XP` liefert inzwischen 404 | GitHub-API |

### A4 XPAIS Marine Traffic

| # | Seitenaussage | Befund | Beleg |
|---|---|---|---|
| A4.1 | Callout-Titel „Show ships and balloons" | **Falscher UI-Name.** X-Plane 12.4.3 nennt die Einstellung `Draw boats and balloons` (Pref-Key `renopt_boats`). Entwickler und Tester benutzen im Forum die falsche Schreibweise — wir sollten den echten Namen nennen | Binary-Strings `X-Plane-x86_64` (zwei Installationen) |
| A4.2 | „the project documents its own boundaries clearly" + „No collision avoidance" / „No berth or port scripting" | **Sinn verdreht.** Im README stehen beide unter `## Design choices (not bugs)`: „Some things the original beta listed as ‚limitations' don't actually apply to a live-AIS renderer, and are left out on purpose". Die echten `## Known gaps (genuine)` sind andere (Passagierschiffe brauchen OpenSceneryX, Autotransporter bewusst gemischt, „Visuals untuned in-sim") | README |
| A4.3 | „without it ferries and liners fall back to **yacht hulls**" | **Widerlegt.** Liner (`L>=160`) und Fähren (`L>=50`) fallen auf einen Bulker-Rumpf zurück; nur Passagierboote unter 50 m auf `kYacht` | `ships.cpp:163-166` |
| A4.4 | „The X-Plane SDK is vendored in the repository, so no separate download is needed" | **Unvollständig.** Der Build holt zur Configure-Zeit IXWebSocket und nlohmann/json — Netzzugang nötig | README: „IXWebSocket and nlohmann/json are fetched at configure time" |
| A4.5 | Abgedruckter `config.ini`-Block | **Unvollständig.** Real gesetzt werden sieben Schlüssel; es fehlen `[Logging] Debug`, `Wakes`, `HideNoHeading` | `build.sh:38`, `config.cpp` |
| A4.6 | Menütabelle | **Unvollständig/ungenau.** `Show wakes` fehlt; der Eintrag heißt `Use OpenSceneryX ships (if installed)`; bei ausgeschaltetem Verkehr steht `Contacts: (off)` | `plugin.cpp:669-685` |
| A4.7 | „interpolates between two known AIS fixes **instead of extrapolating**" | **Zu absolut.** Am Leading Edge wird kurz und gedeckelt extrapoliert | README: „Only at the leading edge … does it briefly extrapolate, capped." |
| A4.8 | „There is no public dataref or SDK call to place a vessel at a given position" | **Zu absolut.** `sim/world/boat/{x,y,z}_mtr`, `heading_deg` sind unter `sim/operation/override/override_boats` schreibbar — aber nur für Träger und Fregatte, nicht für den Umgebungsverkehr | `DataRefs.txt` |
| A4.9 | „spawns synthetic boats stochastically along the density raster" | **Unbelegt** (Raster existiert; der Spawn-Algorithmus ist nirgends öffentlich dokumentiert). Als Entwickleraussage kennzeichnen oder abschwächen | — |
| A4.10 | „Coverage varies" / „Data quality" unter „the project documents its own boundaries" | **Unbelegt.** Beides steht weder im README noch im Code | — |
| A4.11 | XP AIS Traffic (nestasko) „closed-source" | **Unsicher.** Im Thread heißt es, das Projekt habe ein GitHub-Repo gehabt („now closed"). Die Dateiseite sagt zur Quelloffenheit nichts | Forum-Thread 348448, Beitrag Squirrel Dev 2026-06-16 |
| A4.12 | „Developer: CheckCanopy (xbard)" | Bestätigt, aber nur über das Forum: `CheckCanopy` ist der Forum-Handle, `xbard` der Codeberg-Account. Im Repo kommt „CheckCanopy" nicht vor | Thread-Autor |

### A5 ToLiss-Flügelmods

| # | Seitenaussage | Befund | Beleg |
|---|---|---|---|
| A5.1 | Durantula: „**New wing geometry** for the A319, A320 and A321" | **Falsch zusammengefasst.** Geliefert werden neue Klappen- und Klappenträger-Geometrie plus eine Animationsumstellung, keine neue Flügelgeometrie | Installer-README: „the new flaps / flap-track fairings and the wingflex add-on" |
| A5.2 | RealWings-Installer „same architecture as the Carda and Durantula ones" | **Widerlegt.** Der Durantula-Installer arbeitet durchgehend inhaltsbasiert; RealWings löscht die Carda-„kit"-TRIS und die A319-`engines.obj`-Zeilen über **fest codierte Zeilennummern** (`_CARDA_TRIS_TARGETS`), obwohl sein eigenes Changelog „no hard-coded line numbers" behauptet | `install_realwings.py` |
| A5.3 | Overlap-Warnung | **Bestätigt, aber zu vage.** Konkret: beide bearbeiten zusätzlich `Decals.obj`, die Lights-OBJ und die Carda-Triebwerks-OBJs; RealWings löscht die Carda-Kit-Zeile per Zeilennummer — nach einem Durantula-Lauf ist die Zeile verschoben, es kann also eine **andere, noch benötigte** TRIS-Zeile treffen. Kein Installer kennt den jeweils anderen (beide erkennen nur Carda). RealWings ersetzt die OBJ-Dateien übrigens nicht, sondern entfernt sie aus der `.acf` — Durantulas Änderungen laufen dann ins Leere | Grep über beide Installer: null Treffer auf den jeweils anderen Mod |
| A5.4 | Installationsbeschreibung RealWings | **Lückenhaft.** Fehlt: „If a livery ships its own RealWings textures, copy that livery's `objects/RealWings3XX/` folder into the matching livery folder" | Installer-README |
| A5.5 | „There is one download per type" | **Liest sich abschließend, ist es nicht.** Es gibt zusätzlich RealWings340 für die ToLiss A340-600 | forums.x-plane.org, Datei 99955 (HTTP 200, Titel bestätigt) |

### A6 X-World Pro — der schwerste Fund

| # | Seitenaussage | Befund | Beleg |
|---|---|---|---|
| A6.1 | Warnbox „Vegetation library needs a symlink on Linux", angehängt an den **Pro**-Abschnitt | **Widerlegt für Pro — und aktiv schädlich.** Pro liefert ein eigenes Linux-Skript, und der von uns genannte Link ist der falsche: Pro braucht `XP12_libs` → `Resources/default scenery` (das gesamte Verzeichnis) plus Saison-Links in `1200 forests/{spr,sum,fal,win}/` und `mod/Boats_1.dds` → `sim objects/ships/`. In der lokal installierten Pro-Bibliothek gibt es **kein** `1200 forests`-Element. Wer unserer Anweisung folgt, baut sich eine kaputte Installation und ignoriert dabei das mitgelieferte Skript | `simHeaven_X-WORLD-Pro_Library/README_IMPORTANT.txt:35-37` „B) Under Linux or Mac operating system / Run the file ‚install_Pro_Linux_Mac.sh'"; vorhandene Datei `install_XWP_Linux_Mac.sh`; lokal: `simHeaven_X-WORLD-Pro_Library/XP12_libs -> …/Resources/default scenery/` |
| A6.2 | Pro braucht die Vegetationsbibliothek der freien Linie | **Widerlegt.** Handbuch S. 6: „You need to install ‚simHeaven_X-WORLD-Pro_Library', no other library is required." | Handbuch |
| A6.3 | „they link to them" / `.bat` legt einen Symlink an | **Ungenau.** `mklink /J` ist eine Junction; das Pro-Batch **kopiert** zusätzlich `mod\{spr,sum,fal,win}\*.*` nach `1200 forests` | `set_link_WIN.bat`, `install_XWP_WIN.bat` |
| A6.4 | „X-Plane **aborts loading**" | **Widerlegt.** `E/SCN: Failed to find resource …` ist eine nicht-fatale Log-Zeile; die SimHeaven-FAQ spricht ebenfalls nur von Fehlermeldungen | lokale `Log.txt`; simheaven.com/faq |
| A6.5 | „it removes the content reductions the free versions carry" / „Full VFR data instead of the reduced set used in the free X-World packages" | **Unbelegt.** Keine SimHeaven-Quelle nennt die freien Pakete reduziert; die freie Linie hat eine eigene `-1-vfr`-Ebene. Vermutlich Fehllesung von „reduced world bundle" — das ist der **Preis**. Handbuch rahmt Pro additiv: „introduces new concepts that allow for a much greater variety of objects" | Handbuch; simheaven.com |
| A6.6 | „Complete network layers … **which the free packages omit or trim heavily**" | **Teilweise falsch.** Pro teilt in `11-net1-aerials / 12-net2-ships / 13-net3-roads`, die freie Linie hat eine kombinierte `-8-network`-Ebene. Neu sind Schiffs- und Bahnverkehr; „omit" trifft für Straßen nicht zu | lokale Installation beider Linien; Handbuch |
| A6.7 | „road traffic moving at **region-appropriate speeds**" | **Falsche Größe.** Regionsabhängig ist die **Dichte**: „Traffic density that adapts to the environment, such as urban or rural areas, and to the time of day". Zu Geschwindigkeiten nur: „Cars and trucks travelling at different speeds" | Handbuch |
| A6.8 | „derived from OpenStreetMap and **Microsoft Building Footprints**, the same data foundation the free packages use" | **Für Pro unbelegt.** Das Pro-Handbuch nennt Microsoft nirgends, sondern „advanced global building datasets" und dankt „@ueid – global building footprints". Nur die freie Linie nennt Microsoft ausdrücklich | Handbuch vs. simheaven.com/xp12-sceneries/ |
| A6.9 | scenery_packs-Reihenfolge | **Unvollständig.** Das Installationsskript nennt `GLOBAL_AIRPORTS` als eigene Stufe 3. Nebenbei: das Handbuch (S. 7) widerspricht sich selbst und setzt Regionalszenerien unter die Pro-Ebenen | `install_XWP_Linux_Mac.sh` |
| A6.10 | „SimHeaven does not document running X-World Pro and a free X-World package … side by side" | **Formal richtig, aber als Autorität formuliert.** Die Schlussfolgerung ist plausibel, sollte aber als Schlussfolgerung kenntlich sein | — |

---

## Teil B — Bestätigt (Widerlegung gescheitert)

### B1 Die sechs „bereits selbst verifizierten" Punkte

| Punkt | Ergebnis |
|---|---|
| `skip_downloads` umschließt `skip_converts` | **Bestätigt.** `O4_Tile_Utils.py:213-217` — `if not skip_downloads:` → `download_thread.start()` → `if not skip_converts:` verschachtelt darin |
| `cover_extent` ist ein Rand um die Bounding Box, kein Radius | **Bestätigt.** `O4_DSF_Utils.py:143-148` erweitert alle vier Seiten der Bounding Box, danach Rundung auf Texturgrenzen |
| `LOAD_CENTER` schreibt `4096` fest | **Bestätigt.** `O4_DSF_Utils.py:296-302` |
| `magick identify -verbose` gibt keine Mipmap-Anzahl aus | nicht erneut geprüft (unstrittig, kein Widerspruch aufgetaucht) |
| OrthoForge-Defaults identisch außer `water_tech=XP12` | **Bestätigt.** `docs/cfg-reference.md`: `default_zl 16` (L187), `mesh_zl 19` (L66), `mask_zl 14` (L91), `cover_zl 18` (L143), `water_tech 'XP12'` (L147) |
| **`default_website` heißt `Arc`, nicht `ES`** | **Widerlegt — die Prämisse selbst ist falsch.** Der Default ist `""`: `O4_Cfg_Vars.py:268` `"default_website": {"type": str, "default": "", …}`. Die Zeichenkette `"Arc"` kommt im ganzen Fork außerhalb von `Providers/` nicht vor; der einzige harte Fallback ist `O4_GUI_Utils.py:389` `self.default_website.set("BI")`. `Arc` ist ein **Provider-Code** (`Providers/Global/Arc.lay`), nicht der Vorgabewert. **Die Seite steht bereits richtig — nicht ändern.** |

### B2 Ortho4XP — Parameter

`ratio_bathy` als Bathymetrie-Multiplikator (nicht Transparenz), Default `1.0`,
Bereich `[0,1]`: bestätigt (`O4_Cfg_Vars.py:315-319`, `O4_Bathymetry.py:8-14`,
`O4_DSF_Utils.py:872-873` — wird als DSF-Vertex-Koordinate geschrieben, nicht als
Alpha). Vorbehalt siehe A1.9.

`masking_mode=3steps` mit `masks_width` als `[a,b,c]` in Metern, a = Übergang von
undurchsichtig zu `ratio_water`, b = Zone konstanter Transparenz, c = Ausblenden:
bestätigt, Reihenfolge und Bedeutung stimmen (`O4_Mask_Utils.py:730-782`,
`sea_level` aus `ratio_water` bei `:71-72`, Metereinheit über `:664`).

`masking_mode=rocks` „abrupter" statt „für alpine Ufer": bestätigt, doppelt —
halbe Breite (`:661-662`) und explizite Versteilerung („nonlinear transform to
make the transition quicker at the shore … gamma = 2.5", `:711-713`). Von
„alpin" steht nirgends etwas.

`road_level` kumulativ, Stufen 2–5 wie beschrieben, `secondary` schon in `1`,
Cache-Hinweis zu `small_roads.osm`: bestätigt (`O4_Vector_Map.py:288-299`).
Einzige Lücke: `trunk` (A1.2).

`imprint_masks_to_dds` Default `False` im Fork, **`True`** bei oscarpilote:
bestätigt (`O4_Cfg_Vars.py:247-249` vs. oscarpilote `O4_Config_Utils.py:244-246`).

`custom_overlay_src_alternate` und `max_download_slots` als fork-only: bestätigt
(beide fehlen bei oscarpilote vollständig; unbekannte Schlüssel werden dort mit
„Global config file contains an invalid line" verworfen). `max_download_slots`
ist zudem tatsächlich global-only.

Weiter bestätigt: kein `zoomlevel`/`provider`-Schlüssel; `mesh_zl` 19 mit
Wertebereich 16–20 und Deckelung der Bild-Zoomstufe; `min_angle` 10.0 mit der
Wasser-/Land-Unterscheidung; `sea_smoothing_mode`-Semantik zero/mean/none;
`mask_zl` 14 mit nur 14/15/16; `use_masks_for_inland` False; `ratio_water` 0.25.

**Das `seq`-Skript ist korrekt.** Ortho4XP bildet Verzeichnisnamen über
`O4_File_Names.py:41-44` (`floor(lat/10)*10`, `zfill(3)` bzw. `zfill(4)`). Die
648 nötigen Namen wurden vollständig aufgezählt und mit dem, was
`seq -90 10 80` × `seq -180 10 170` samt der `printf`-Regeln erzeugt, verglichen:
symmetrische Differenz leer. `+90`/`+180` werden nie gebraucht.

### B3 Datenquellen

sonny.4lima.de deckt Europa ab („SONNY's LiDAR DIGITAL TERRAIN MODELS of
EUROPE"): bestätigt. Die 0,5″-US-Kacheln tragen USGS-3DEP-Zuschreibung:
bestätigt, wörtlich („Elevation data courtesy of the U.S. Geological Survey 3D
Elevation Program (3DEP)"). CC BY 4.0 mit Sonny-Nennung an beiden Stellen:
bestätigt. `orthoforge-data.html` führt ausschließlich OSM (vier Abschnitte, kein
Höhenmaterial): bestätigt — die DEM liegen auf `sonny.html`. Alle Detailaussagen
zu den vorgebackenen OSM-Kacheln (Cache-Format, maximale Straßendetailstufe,
`OSM_data/<block>/<tile>/`, bzip2, nicht umbenennen/entpacken, ODbL, kostenlos
ohne Konto): bestätigt.

OrthoForge: GPL v3, xbard, Ursprung als englischer Fork von Rolands ORTHO4XP_V3,
Python ≥ 3.10, `OrthoForge.cfg.example` als Preset mit `min_angle=0.5`,
`limit_tris=50.0`, `cover_extent=5.0` und ohne automatisches Einlesen: bestätigt.

`1302 flatten 1` als Schreibweise: bestätigt — 629 Vorkommen in der
XP12-Standard-`apt.dat`, ausschließlich in dieser Form. Nicht deprecated.
*Aber:* der Schlüssel `flatten` steht **nicht** in der offiziellen 1302-Liste der
apt.dat-Spezifikation; belegt ist er über die ausgelieferten Daten und über WEDs
„Always Flatten". Das Hinzufügen als Reparatur ist die dokumentierte Absicht
(developer.x-plane.com/2016/03/per-airport-flattening/).

### B4 XPME

Bestätigt: Preise 5 $/30 Tage und 40 $/365 Tage (aus dem JS-Chunk der
Bestellseite — der Vorbehalt „confirm the current figures there" ist berechtigt),
eine Lizenz pro PC und hardwaregebunden, Umzug per Benutzername und E-Mail,
kommerzielle Nutzung nur mit schriftlicher Genehmigung, PayPal/Buy Me a Coffee,
WinFSP/FUSE-T/FUSE 3, ZL16-Basispakete, Cloudflare + `aria2`, Kartenquellen und
Free-Tier-Tabelle (alle sieben Zeilen wörtlich), .NET 10 + ASP.NET Core 10, die
`apt`-Zeile wörtlich, ~200 parallele Verbindungen, unregelmäßige Linux-Assets
(15 von 20 Releases; das neueste, 4.7.4 vom 2026-07-19, ohne Linux),
Ortho4XP/HD-Mesh als dokumentierte Konflikte, beide Linux-Issues wörtlich.

**Start-/Stoppreihenfolge bestätigt:** „Before launching the game, open the
X-Plane Map Enhancement application" … „To exit properly, you must close the game
first, then click ‚Stop'". Nur die Begründung ist unbelegt (A3.2).

**Lizenzen bestätigt:** AutoOrtho Apache-2.0 (sowohl `kubilus1/autoortho` als
auch der von uns dokumentierte Fork `ProgrammingDinosaur/autoortho4xplane`),
XEarthLayer MIT (`samsoir/xearthlayer`) — jeweils aus der LICENSE-Datei, nicht
nur aus dem API-Feld.

### B5 XPAIS — die Forum-Punkte sind geklärt

Archivierung bestätigt: `"archived": true, "archived_at":
"2026-07-07T15:15:41+02:00"`, letzter Commit `0ddc2473` vom
`2026-06-16T19:25:37+01:00`. Heute (2026-08-04) weiterhin archiviert.

Der Entwickler hat die README-Empfehlung im Thread **tatsächlich korrigiert** —
wörtlich, am 2026-06-15:

> „Leaving XP's traffic on actively hurts. Those synthetic boats have nothing to
> do with real traffic, so they'd ghost and duplicate right next to our real AIS
> vessels. That's a reason to keep ‚Show ships and balloons' off, not a way to
> borrow wakes. … ‚Show ships and balloons': confirmed, you can leave it off. Our
> vessels are plugin-instanced so they render regardless, and that also means we
> won't fight XP's own boats."

Auch der Tester korrigiert sich: „And I have to correct myself: X-Plane's ‚Show
ships and balloons' can also be off." Das README (Stand: „Keep ‚show ships and
balloons' enabled … they stop drawing") ist damit die ältere, überholte Aussage —
die Seite liegt inhaltlich richtig. Offen bleibt nur der UI-Name (A4.1).

Ebenfalls im Thread wörtlich bestätigt: „EHAM is a great test area. Around 3000
(!) contacts. Not so good of a test area is the Straight of Hormuz … because
there is no data."

Zum Windows-Projekt bestätigt: Dateiseite 100400, „Supported Platform: X-Plane
12 / Windows 64-bit", und die Autorenantwort „Linux and Mac support are
definitely on the roadmap … No ETA yet". Kein Linux-Build.

Weiter bestätigt: Zwei-Thread-Architektur mit `ais_client` ohne jeden
XPLM-Aufruf, 60-Sekunden-Versatz (`plugin.cpp:49` `kRenderDelay = 60.0`),
Rumpfauswahl nach AIS-Typcode und Abmessungen, GPL-3.0 (LICENSE-Datei), Linux/
XP12, kostenloser AISStream-Key, Build- und Installationsbefehle, Logpfad,
HDG-000-Filter standardmäßig aus, Wakes aus und auf X-Planes `wake.png`
verweisend, `shipping-lanes-for-boats.png` existiert.

### B6 ToLiss

Über den Browser wörtlich bestätigt: „Many thanks to @Giorgi_Z4 for modeling and
animating!" (Datei 88518) sowie die gesamte RealWings-Beschreibung (Datei 99352):
„Fully re-modelled wings with clean geometry", „Brand new 4K textures with high
texel density", „Substance 3d painter paintkit", „Fully compatible with Carda's
CFM/IAE engines", „Bonus: new window frames", „Currently only for X-Plane 12",
„This is a visual-only mod. It was made 100% by myself and @Durantula2405", „does
not contain any original files from Toliss aircrafts and it does not modify the
core structure/code".

Aus den Installer-Repos bestätigt: beide Durantula-Teile getrennt installierbar,
Flaps-Beschreibung inklusive Carda-/`engines.obj`-Fallback, Wingflex auf
`wing_tip_deflection_deg` samt Dämpfungswerten in der `.acf`, Paintkit-Handhabung,
inhaltsbasiertes Matching und `*.durantula.bak`, SkunkCrafts-Hinweis, alle
Linux-Binaries und Flags beider Installer, RealWings-Variantentabelle,
Zusammenführen der `CEO/`/`NEO/`-Ordner, GPL-3.0 für beide Installer.

Alle sieben Forum-Links der ToLiss-Seite und der XPAIS-Thread liefern HTTP 200
mit passendem Titel.

### B7 X-World Pro

Bestätigt: VFR-Linie für XP12 über den X-Plane.org-Store, einzeln oder als
vergünstigtes World-Bundle; die freien Pakete bleiben kostenlos und werden weiter
gepflegt; größere Objekt-, Vegetations- und Ackerbauvielfalt; animierter
Schornsteinrauch, Dampf und Geysire; weltweite Landmarks; Testszenerie mit
15 Kacheln („from +49+004 to +052+009", Ruhrgebiet, Luxemburg, Teile der
Niederlande, Belgiens und Frankreichs); Pro besteht aus Szenerie-Ebenen plus
`simHeaven_X-WORLD-Pro_Library`; Kopieren statt Verlinken verschwendet Platz und
veraltet bei Updates.

---

## Teil C — Nebenbefunde an den Belegdokumenten

Diese betreffen `research/`, nicht die Doku:

- `research/szenerie/fc5_xpme.md`, Punkt B5-06 hielt die Rückgabefrist für
  unbelegt und für eine Halluzination. Das ist der Ursprung des Fehlers A3.1 und
  gehört mitkorrigiert.
- `research/addons/FAKTENCHECK_toliss_mods.md`: fünf als README-Zitate geführte
  Belegstellen stehen so nicht in den aktuellen READMEs (Paraphrasen). Inhaltlich
  hält jeder Punkt, aber die Belegspalte ist nicht zitierfähig.
- Ebenda: `anim/winglex` wurde als „offenkundiger Tippfehler der Quelle"
  abgetan. Es ist der echte ToLiss-Bezeichner — der Installer matcht auf die
  literale Zeichenkette (`install_durantula.py:316`).
- `research/addons/FAKTENCHECK_xpais_marine_traffic.md` führt GPL-3.0 auf
  „Repo-Metadaten" zurück. Die Codeberg-API hat gar kein `license`-Feld (und
  erkennt die Sprache als „Pascal"). Beleg ist die LICENSE-Datei.

## Teil D — Statistik

| Kategorie | Anzahl |
|---|---|
| Geprüfte Einzelaussagen | rund 130 |
| Widerlegt oder wesentlich falsch | 12 |
| Unvollständig, zu absolut oder unbelegt | 30 |
| Bestätigt | der Rest |
| Davon Prämissen der Arbeitsanweisung selbst widerlegt | 1 (`default_website`) |
