# Faktencheck Bereich 1 — ortho4xp.md, "Important Parameters" + "Recommended Settings"

Geprüfte Datei: `docs/en/scenery/orthophotography/ortho4xp.md`, Zeilen 84–322.
Prüfdatum: 2026-08-03.

## Quellenlage (Vorbemerkung)

| Quelle | Datei mit `cfg_vars` | Version | Stand |
|---|---|---|---|
| oscarpilote/Ortho4XP, Branch `master` (Default-Branch lt. GitHub-API) | `src/O4_Config_Utils.py` — **`src/O4_Cfg_Vars.py` existiert dort nicht** (Tree-API, `truncated: false`) | `src/O4_Version.py` → `version='1.40'` | letzter Push 2026-03-14 |
| shred86/Ortho4XP, Branch `master` (Default-Branch lt. GitHub-API) | `src/O4_Cfg_Vars.py` (+ `src/O4_Config_Utils.py` für das Laden) | `version='1.40.13'` | letzter Push 2026-07-04 |
| lokaler Fork `/mnt/xplane_data/docker/Ortho4XP/src/O4_Cfg_Vars.py` | — | `version='1.40.13'` | 2026-05-01 |
| OrthoForge, codeberg.org/xbard/OrthoForge, Branch `main` | `src/O4_Config_Utils.py`, Referenz `docs/cfg-reference.md` (auto-generiert) | v1.0 beta | letzter Push 2026-07-28 |

Wichtig: `diff /mnt/xplane_data/docker/Ortho4XP/src/O4_Cfg_Vars.py <raw shred86 master>` → **identisch**.
Der lokale Fork ist also byte-gleich mit shred86/master; er ist keine unabhängige Bestätigung für oscarpilote.

Das Codeberg-Repo von OrthoForge ist entgegen der Ankündigung auf der Projektseite weiterhin
aktiv (API `updated_at: 2026-07-28`), und https://xpconnect.me/orthoforge.html verweist selbst
darauf: *"Get the repo from codeberg.org/xbard/OrthoForge"*. (Betrifft Zeile 29 — außerhalb
meines Prüfbereichs, nur als Hinweis.)

---

## Gesamttabelle der Vorgabewerte

Alle Werte aus dem Quelltext extrahiert (AST-Parse von `cfg_vars` / `cfg_app_vars` + `cfg_tile_vars`).
Rein numerische Typunterschiede (`1` vs. `1.0`, `4` vs `4.0` — beide über `"type": float` verarbeitet)
sind keine Abweichungen und unten nicht markiert.

| Parameter | Seite | oscarpilote 1.40 | shred86 1.40.13 | lokaler Fork | Bewertung |
|---|---|---|---|---|---|
| `custom_scenery_dir` | `""` | `""` | `""` | `""` | ok |
| `custom_overlay_src` | `""` | `""` | `""` | `""` | ok |
| `custom_overlay_src_alternate` | `""` | **Key existiert nicht** | `""` | `""` | fork-only |
| `default_website` | `""` | `""` | `""` | `""` | ok |
| `default_zl` | `16` | `16` | `16` | `16` | ok |
| `mesh_zl` | `19` | `19` | `19` | `19` | ok |
| `min_angle` | `10.0` | `10` | `10.0` | `10.0` | ok |
| `curvature_tol` | `2.0` | `2` | `2.0` | `2.0` | ok |
| `apt_curv_tol` | `0.5` | `0.5` | `0.5` | `0.5` | ok |
| `apt_curv_ext` | `0.5` | `0.5` | `0.5` | `0.5` | ok |
| `coast_curv_tol` | `1.0` | `1` | `1.0` | `1.0` | ok |
| `coast_curv_ext` | `0.5` | `0.5` | `0.5` | `0.5` | ok |
| `limit_tris` | `3.0` | `3` | `3.0` | `3.0` | ok |
| `apt_smoothing_pix` | `8` | `8` | `8` | `8` | ok |
| `road_level` | `1` | `1` | `1` | `1` | ok |
| `road_banking_limit` | `0.5` | `0.5` | `0.5` | `0.5` | ok |
| `lane_width` | `4.0` | `4` | `4.0` | `4.0` | ok |
| `terrain_casts_shadows` | `True` | `True` | `True` | `True` | ok |
| `use_decal_on_terrain` | `False` | `False` | `False` | `False` | ok |
| `normal_map_strength` | `1.0` | `1` | `1.0` | `1.0` | ok |
| `overlay_lod` | `25000` | `25000` | `25000` | `25000` | ok |
| `cover_airports_with_highres` | `False` | `'False'` | `'False'` | `'False'` | ok |
| `cover_zl` | `18` | `18` | `18` | `18` | ok |
| `cover_extent` | `1.0` | `1` | `1.0` | `1.0` | ok |
| `mask_zl` | `14` | `14` | `14` | `14` | ok |
| `masks_width` | `100` | `100` | `100` | `100` | ok |
| `masking_mode` | `sand` | `'sand'` | `'sand'` | `'sand'` | ok |
| `use_masks_for_inland` | `False` | `False` | `False` | `False` | ok |
| **`imprint_masks_to_dds`** | **`False`** | **`True`** | `False` | `False` | **Abweichung** |
| `sea_smoothing_mode` | `zero` | `'zero'` | `'zero'` | `'zero'` | ok |
| `water_smoothing` | `10` | `10` | `10` | `10` | ok |
| `ratio_water` | `0.25` | `0.25` | `0.25` | `0.25` | ok |
| `ratio_bathy` | `1.0` | `1.0` | `1.0` | `1.0` | ok (Beschreibung falsch, s. B1-06) |
| `min_area` | `0.001` | `0.001` | `0.001` | `0.001` | ok |
| `max_area` | `200.0` | `200` | `200.0` | `200.0` | ok |
| `sea_texture_blur` | `0.0` | `0` | `0.0` | `0.0` | ok |
| `water_tech` | `XP11 + bathy` | `'XP11 + bathy'` | `'XP11 + bathy'` | `'XP11 + bathy'` | ok |
| `custom_dem` | `""` | `""` | `""` | `""` | ok |
| `fill_nodata` | `True` | `True` | `True` | `True` | ok |
| `skip_downloads` | `False` | `False` | `False` | `False` | ok |
| `skip_converts` | `False` | `False` | `False` | `False` | ok |
| `max_download_slots` | (nur genannt) | **Key existiert nicht** | `1` | `1` | fork-only |
| `max_convert_slots` | (nur genannt) | `4` | `4` | `4` | ok |
| `verbosity` / `cleaning_level` / `overpass_server_choice` | (nur genannt) | `1` / `1` / `'random'` | `1` / `1` / `overpass_server_default` | dito | ok |

Ergebnis: **von 39 auf der Seite mit Zahlenwert dokumentierten Defaults stimmt genau einer nicht
mit oscarpilote überein** (`imprint_masks_to_dds`), plus zwei Parameter, die es bei oscarpilote gar
nicht gibt.

---

## B1-01 `default_website=ES` als ESRI-Provider

Behauptung (Zeile 107): "| `default_website` | `""` | Imagery source, e.g. `BI` (Bing), `GO2` (Google), `ES` (ESRI) |"
Ebenfalls betroffen: alle vier Profile in "Recommended Settings" verwenden `default_website=BI` (korrekt) — der Fehler steckt nur in der Tabellenzeile.

Urteil: FALSCH

Beleg: Es existiert in keinem der beiden Repositories ein Provider `ES`. Vollständiger Inhalt von
`Providers/Global/` (GitHub Tree-API, `recursive=1`, `truncated:false`, Branch `master`, abgerufen 2026-08-03):

- shred86: `Arc.lay`, `Arc@.lay`, `BI.lay`, `EOX.lay`, `GO2.lay`, `Here.lay`, `OSM.lay`, `SEA.lay`, `USA2.lay`
- oscarpilote: dieselben plus `EOX2.lay`, `Mapbox.lay`, `Maxar.lay`

Der ESRI/ArcGIS-Provider heißt `Arc`:
https://raw.githubusercontent.com/shred86/Ortho4XP/master/Providers/Global/Arc.lay —
`"url_template=http://services.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{zoom}/{y}/{x}"` (Stand: master, 2026-08-03)

Zum Vergleich Bing: `Providers/Global/BI.lay` — `"url_template=http://r{switch:0,1,2,3}.ortho.tiles.virtualearth.net/tiles/a{quadkey}.jpeg?g=136"`

Tragweite: hoch — `default_website=ES` führt nicht zu einem Fallback, sondern der Provider-Code
landet in Texturnamen und Provider-Lookup; der Build bricht ab bzw. liefert keine Imagery.

Vorschlag: "Imagery source, e.g. `BI` (Bing), `GO2` (Google), `Arc` (ESRI World Imagery)".

---

## B1-02 OrthoForge-Kasten: vier von fünf angeblich abweichenden Vorgabewerten sind identisch

Behauptung (Zeilen 217–229, Kastentitel): "Same key names in OrthoForge, different defaults" mit der Tabelle
`default_zl` 16→18, `mesh_zl` 19→20, `mask_zl` 14→18, `cover_zl` 18→19, `water_tech` XP11 + bathy→XP12.

Urteil: FALSCH (für vier der fünf Zeilen)

Beleg 1 — die auto-generierte cfg-Referenz von OrthoForge selbst
(https://codeberg.org/xbard/OrthoForge/raw/branch/main/docs/cfg-reference.md, Branch `main`,
Repo-Stand 2026-07-28; Kopfzeile: *"This page is **auto-generated** from `src/O4_Config_Utils.py` by `tools/gen_cfg_docs.py`."*):

- "| `default_zl` | int | 16 | '' |"
- "| `mesh_zl` | int | 19 | 'The mesh will be preprocessed to accept later any combination of imageries up to and including a zoomlevel equal to mesh_zl. …' |"
- "| `mask_zl` | int | 14 | 'The zoomlevel at which the (sea) water masks are built. …' |"
- "| `cover_zl` | int | 18 | 'The zoomlevel with which to cover the airports zone when high_zl_airports is set. …' |"
- "| `water_tech` | str | 'XP12' | 'Water tech type. XP12 uses native X-Plane 12 water rendering (WATER_COLOR_MASK). XP11 + bathy is no longer supported in V2.' |"

Beleg 2 — Quelltext https://codeberg.org/xbard/OrthoForge/raw/branch/main/src/O4_Config_Utils.py:
`"mesh_zl": {"type": int, "default": 19, "values": (16, 17, 18, 19, 20), …}`,
`"mask_zl": {"type": int, "default": 14, "values": (14, 15, 16, 17, 18, 19, 20), …}`,
`"water_tech": {"type": str, "default": "XP12", "values": ("XP12",), …}`

Beleg 3 — die Zahlen der Seite stammen offenkundig aus `OrthoForge.cfg.example`
(https://codeberg.org/xbard/OrthoForge/raw/branch/main/OrthoForge.cfg.example): dort steht
`mesh_zl=20`, `mask_zl=18`, `cover_zl=19`, `default_zl=18`, `water_tech=XP12`. Das ist eine
mitgelieferte **Beispiel-/Preset-Datei**, kein Default. OrthoForge kopiert sie nicht automatisch:
`src/O4_Config_Utils.py` fängt eine fehlende Konfiguration ab mit
`print("No global config file found. Reverting to default values.")` — es fällt auf die
`cfg_vars`-Defaults zurück, nicht auf die `.example`.

Zusatz: `OrthoForge.cfg.example` weicht in weit mehr als fünf Schlüsseln vom Ortho4XP-Default ab
(`min_angle=0.5`, `limit_tris=50.0`, `road_level=3`, `apt_smoothing_pix=16`, `ratio_water=0.75`,
`sea_smoothing_mode=mean`, `cover_extent=5.0`, `use_decal_on_terrain=True`, `fill_nodata=False`,
`imprint_masks_to_dds=True`, `masks_width=[25]`, `overlay_lod=15000.0`) — die Fünferliste ist also
auch als Beschreibung der Beispieldatei unvollständig.

Tragweite: hoch — der Kasten warnt vor einem Effekt ("noticeably longer build times and larger
tiles"), den die OrthoForge-Defaults gar nicht erzeugen; wer die Beispieldatei benutzt, bekommt
dagegen zwölf statt fünf abweichende Werte, darunter `min_angle=0.5` und `limit_tris=50`, die
weit drastischer wirken als die genannten Zoomlevel.

Vorschlag: Kastentitel und Tabelle umstellen auf: OrthoForge übernimmt die Ortho4XP-Defaults
weitgehend unverändert; die einzige Abweichung im Default ist `water_tech=XP12` (XP11-Wasser wird
nicht mehr unterstützt). Die mitgelieferte `OrthoForge.cfg.example` ist dagegen ein
Hochdetail-Preset (`default_zl=18`, `mesh_zl=20`, `mask_zl=18`, `cover_zl=19`, `min_angle=0.5`,
`limit_tris=50`, `cover_extent=5.0`) und bedeutet deutlich längere Bauzeiten — sie wird aber nicht
automatisch aktiv.

---

## B1-03 `imprint_masks_to_dds` Vorgabewert gilt nicht für das Originalprojekt

Behauptung (Zeile 174): "| `imprint_masks_to_dds` | `False` | Bakes the masks into the DDS textures. …"

Urteil: FALSCH für oscarpilote (BESTÄTIGT für shred86 und den lokalen Fork)

Beleg: https://raw.githubusercontent.com/oscarpilote/Ortho4XP/master/src/O4_Config_Utils.py, Zeilen 244–248
(Version `1.40`, Branch `master`, abgerufen 2026-08-03):

```
    "imprint_masks_to_dds": {
        "type": bool,
        "default": True,
```

Gegenprobe shred86: https://raw.githubusercontent.com/shred86/Ortho4XP/master/src/O4_Cfg_Vars.py — `"imprint_masks_to_dds": {"type": bool, "default": False, …}` (Version `1.40.13`).

Tragweite: mittel — wer mit dem Originalprojekt baut und den Wert nicht setzt, bekommt DXT5-Texturen
mit doppelter Dateigröße statt der auf der Seite versprochenen DXT1-Basis. Kein Abbruch, aber die
Paketgröße verdoppelt sich für maskierte Kacheln. Für das Ortho-Streaming-Profil (Zeile 317) ist der
Wert ohnehin explizit gesetzt, dort folgenlos.

Vorschlag: Default-Spalte auf `False` (shred86) / `True` (oscarpilote) aufspalten oder eine Fußnote:
"Im Originalprojekt oscarpilote/Ortho4XP ist der Vorgabewert `True`."

---

## B1-04 Quellenangabe `src/O4_Cfg_Vars.py` trifft auf das Originalprojekt nicht zu

Behauptung (Zeile 86): "The defaults below are the ones defined in `src/O4_Cfg_Vars.py`."

Urteil: FALSCH (für oscarpilote), BESTÄTIGT (für shred86)

Beleg: GitHub Tree-API https://api.github.com/repos/oscarpilote/Ortho4XP/git/trees/master?recursive=1
(`"truncated": false`, abgerufen 2026-08-03) listet unter `src/` u. a. `src/O4_Config_Utils.py`,
aber **keine** Datei `src/O4_Cfg_Vars.py`. Bei oscarpilote steht das `cfg_vars`-Dict inline in
`src/O4_Config_Utils.py` ab Zeile 16 (`cfg_vars = {`). shred86 hat es in
`src/O4_Cfg_Vars.py` ausgelagert (dort `cfg_app_vars` Zeile 16, `cfg_tile_vars` Zeile 118,
`cfg_vars = {**cfg_app_vars, **cfg_tile_vars, **cfg_global_tile_vars}` Zeile 361).

Tragweite: mittel — Leser, die die Angabe im Originalprojekt nachschlagen wollen, finden die Datei nicht.

Vorschlag: "The defaults below are those of the shred86 fork (`src/O4_Cfg_Vars.py`); in the original
project by oscarpilote the same table lives inline in `src/O4_Config_Utils.py`."

---

## B1-05 `custom_overlay_src_alternate` und `max_download_slots` existieren nur im Fork

Behauptung (Zeile 106): "| `custom_overlay_src_alternate` | `""` | Fallback path, used when the first source has no data for a tile |"
Behauptung (Zeile 215): "Also global-only: `verbosity`, `cleaning_level`, `max_download_slots`, `max_convert_slots`, …"

Urteil: BESTÄTIGT für shred86 / lokalen Fork, FALSCH für oscarpilote

Beleg: In https://raw.githubusercontent.com/oscarpilote/Ortho4XP/master/src/O4_Config_Utils.py kommen
beide Namen nicht vor; `list_app_vars` (Zeilen 354–369) lautet dort vollständig:

```
list_app_vars = [
    "verbosity", "cleaning_level", "overpass_server_choice",
    "skip_downloads", "skip_converts", "max_convert_slots",
    "check_tms_response", "http_timeout", "max_connect_retries",
    "max_baddata_retries", "ovl_exclude_pol", "ovl_exclude_net",
    "custom_scenery_dir", "custom_overlay_src",
]
```

shred86 (`src/O4_Cfg_Vars.py`, Zeilen 363–381) enthält dieselbe Liste plus `max_download_slots`
und `custom_overlay_src_alternate`. Hint dort: `max_download_slots` — *"Each orthophoto being
constructed uses 16 threads for network requests by default … increasing it to 2 will result in 32
threads"* (Default `1`); `custom_overlay_src_alternate` — *"If sceneries with overlays are not
found in custom_overlay_src, set an alternate directory to search."*

Konsequenz bei oscarpilote: Die Zeile wird beim Laden abgefangen und verworfen —
`osc_Config_Utils.py` Zeilen 476–478: `except: UI.lvprint(1, "Global config file contains an
invalid line:", line)`.

Tragweite: mittel — stillschweigend wirkungslos im Originalprojekt (nur eine Log-Zeile).

Vorschlag: Beide Einträge als fork-spezifisch kennzeichnen, z. B. "(shred86 fork only)".
Zusätzlich: der Vorgabewert von `max_download_slots` (`1`) fehlt auf der Seite ganz.

---

## B1-06 `ratio_bathy` als Transparenz beschrieben

Behauptung (Zeile 178): "| `ratio_bathy` | `1.0` | Same principle for the bathymetry (sea bed) |"
Kontext Zeile 177: `ratio_water` = "Transparency of the ortho overlay over inland water".

Urteil: FALSCH

Beleg: `src/O4_Cfg_Vars.py` (shred86 master) bzw. `src/O4_Config_Utils.py` (oscarpilote master),
Eintrag `ratio_bathy`, hint: *"Bathymetry multiplier for near shore vertices. In the range [0,1]."*
Der Hint für `ratio_water` lautet dagegen ausführlich über Transparenz:
*"…The parameter ratio_water (values between 0 and 1) determines how much transparency is applied
to the orthophoto. At zero, the orthophoto is fully opaque…"* — die beiden folgen also gerade nicht
demselben Prinzip.

Tragweite: mittel — irreführend, aber der Default `1.0` bleibt korrekt und der Parameter wird in
keinem Profil verstellt.

Vorschlag: "| `ratio_bathy` | `1.0` | Multiplier for the bathymetric depth at near-shore vertices, `0`–`1` |"

---

## B1-07 `masking_mode=3steps`: Bedeutung von `b`, dritter Wert `c` fehlt

Behauptung (Zeile 184): "`masking_mode=3steps` turns the coastal transition into a staged one and
expects `masks_width` as a list `[a,b,c]`, where `a` is the length in meters of a first transition
from fully opaque imagery at the shoreline to `ratio_water` transparency, and `b` is the second
transition zone."

Urteil: FALSCH (Teilaussage zu `b`), unvollständig (zu `c`)

Beleg: hint zu `masking_mode` (identisch in oscarpilote master und shred86 master):
*"…the third one (3steps) requires a list of the form [a,b,c] for masks width: "a" is the length in
meters of a first transition from plain imagery at the shoreline towards ratio_water transparency,
"b" is the second extent zone where transparency level is kept constant equal to ratio_water, and
"c" is the last extent where the masks eventually fade to nothing. The transition with rocks is more
abrupt than with sand."*

`b` ist also die Zone **konstanter** Transparenz, kein zweiter Übergang; `c` ist der eigentliche
Ausblendbereich und fehlt auf der Seite ganz.

Tragweite: mittel — `3steps` wird in keinem der vier Profile verwendet, aber wer es einsetzt,
dimensioniert `b` falsch.

Vorschlag: "…`a` is the length in meters of a first transition from fully opaque imagery at the
shoreline to `ratio_water` transparency, `b` the zone in which that transparency stays constant,
and `c` the final zone over which the mask fades to nothing. The `rocks` transition is more abrupt
than `sand`."

---

## B1-08 `cover_extent` als Radius um den Flugplatz

Behauptung (Zeile 162): "| `cover_extent` | `1.0` | Radius of the high-resolution zone around each airport, in km |"
Behauptung (Zeile 164): "…values from `0.5` to `6.0` are all plausible, a twelvefold difference in radius and roughly a hundredfold in covered area per airport."

Urteil: FALSCH (Beschreibung), UNBELEGBAR (Wertebereich und Flächenfaktor)

Beleg: hint zu `cover_extent` (oscarpilote master / shred86 master):
*"The extent (in km) past the airport boundary taken into account for higher ZL. Note that for VRAM
efficiency higher ZL textures are fully used on their whole extent as soon as part of them are
needed."* — es ist ein Puffer **über die Flugplatzgrenze hinaus**, kein Radius um einen Punkt. Der
Eintrag hat kein `"values"`-Feld, es gibt also keinen im Code hinterlegten zulässigen Bereich; für
"0.5 bis 6.0 sind alle plausibel" und den Flächenfaktor ~100 existiert keine Quelle. Da die
Vergrößerung ein Puffer um ein Polygon ist, ist der Flächenzuwachs zudem nicht quadratisch.

Tragweite: mittel — die Fehlbeschreibung führt zu falscher Größenschätzung, bricht aber nichts.

Vorschlag: "| `cover_extent` | `1.0` | How far past the airport boundary the high-resolution zone
extends, in km |" — und den Satz in Zeile 164 auf eine belegbare Aussage kürzen ("`cover_extent` is
the main lever on package size: the buffer is applied around the whole airport outline, and because
higher-ZL textures are used over their full extent as soon as any part is needed, small increases
add a disproportionate amount of texture data" — letzteres direkt aus dem Hint).

---

## B1-09 `min_angle` als "strongest single lever"

Behauptung (Zeile 126): "`min_angle` is the strongest single lever on mesh quality and one of the
first values worth adjusting. … Raising `min_angle` and lowering `curvature_tol` both increase the
triangle count, so `limit_tris` acts as the ceiling."

Urteil: teils BESTÄTIGT, teils UNBELEGBAR

Beleg (bestätigt, `curvature_tol`): hint zu `curvature_tol`: *"This parameter is intrinsically
linked the mesh final density. Mesh refinement is mostly based on curvature computations on the
elevation data (the exact decision rule can be found in _ triunsuitable() _ in
Utils/Triangle4XP.c). A higher curvature tolerance yields fewer triangles."* — bestätigt zugleich
Zeile 118 ("Higher values produce **fewer** triangles").

Beleg (bestätigt, Semantik `min_angle`): hint: *"The mesh algorithm will try to not have mesh
triangles with (smallest for water / second smallest for regular land) angle less than the value
(in deg) of min_angle."* — deckt Zeile 117 wörtlich.

Unbelegbar: Die Rangaussage "strongest single lever on mesh quality" und die Behauptung, ein höheres
`min_angle` erhöhe die Dreieckszahl, stehen in keinem Hint und in keiner offiziellen Doku der beiden
Repos. (Plausibel aus der Triangle-Refinement-Theorie, aber nicht belegt.)

Tragweite: niedrig — Formulierungsfrage, keine falsche Zahl.

Vorschlag: Rangaussage streichen oder abschwächen ("`min_angle` and `curvature_tol` are the two
levers that decide mesh density"). Für den Dreieckszuwachs bei steigendem `min_angle` einen Beleg
nachliefern oder als Erfahrungswert kennzeichnen.

---

## B1-10 Zulässige Wertebereiche

Behauptungen: `mesh_zl` "permitted values `16`–`20`" (Z. 116); `road_level` "`0`–`5`" (Z. 132);
`cover_airports_with_highres` `False`/`True`/`ICAO`/`Existing` (Z. 160, implizit);
`mask_zl` "Permitted values are only `14`, `15` and `16`" (Z. 170);
`masking_mode` "`sand`, `rocks` or `3steps`" (Z. 172);
`sea_smoothing_mode` `zero`/`mean`/`none` (Z. 175, 188–190);
`ratio_water` "`0`–`1`" (Z. 177); `mesh_zl=16` "lowest permitted value" (Z. 301);
`mask_zl=16` "finest permitted mask resolution" (Z. 277).

Urteil: BESTÄTIGT (alle, für beide Upstreams)

Beleg (Werte aus dem `"values"`-Feld, identisch in oscarpilote `src/O4_Config_Utils.py` und
shred86 `src/O4_Cfg_Vars.py`, jeweils Branch `master`, abgerufen 2026-08-03):

- `"mesh_zl": … "values": (16, 17, 18, 19, 20)`
- `"mask_zl": … "values": (14, 15, 16)`
- `"road_level": … "values": (0, 1, 2, 3, 4, 5)`
- `"masking_mode": … "values": ["sand", "rocks", "3steps"]`
- `"sea_smoothing_mode": … "values": ["zero", "mean", "none"]`
- `"cover_airports_with_highres": … "values": ("False", "True", "ICAO", "Existing")`
- `"water_tech": … "values": ("XP12", "XP11 + bathy")`
- `ratio_water` hint: *"(values between 0 and 1)"*

Nur als Hinweis für den OrthoForge-Kasten: dort ist `mask_zl` auf `(14, 15, 16, 17, 18, 19, 20)`
erweitert und `cover_airports_with_highres` um `"Progressive"` ergänzt
(https://codeberg.org/xbard/OrthoForge/raw/branch/main/src/O4_Config_Utils.py).

Tragweite: niedrig (keine Änderung nötig)

Vorschlag: keine Änderung.

---

## B1-11 `zoomlevel`, `provider`, `custom_build_dir`, `custom_overlay_dir` sind keine Config-Keys

Behauptung (Zeile 110): "There is no `zoomlevel` and no `provider` key — those names appear in older
documentation and in internal code, but a config file containing them is parsed without them taking
effect. Use `default_zl` and `default_website` instead."

Urteil: BESTÄTIGT (für beide Upstreams)

Beleg 1 — keiner der Namen ist Schlüssel in `cfg_vars`. Vollständiger Schlüsselsatz per AST-Parse:
oscarpilote 58 Einträge, shred86 60 (`cfg_app_vars` + `cfg_tile_vars`, dazu 41 automatisch
generierte `global_*`-Duplikate). `zoomlevel` und `provider` kommen in beiden Dateien nur als
Fließtext in Hints und als Funktionsparameter vor (z. B. `src/O4_DSF_Utils.py`
`(zoomlevel, provider_code) = dico_tmp[masks_im.getpixel((x, y))]`).

Beleg 2 — Verhalten bei unbekanntem Schlüssel, oscarpilote `src/O4_Config_Utils.py` Zeilen 450–478:

```
            (var, value) = line.split("=")
            …
            target = (cfg_vars[var]["module"] + "." + var if "module" in cfg_vars[var] else var)
            …
        except:
            UI.lvprint(1, "Global config file contains an invalid line:", line)
            pass
```

Der `KeyError` aus `cfg_vars[var]` wird geschluckt — die Zeile bleibt folgenlos. shred86 verhält
sich identisch (`src/O4_Config_Utils.py` Zeilen 106–124, `set_global_variables()` greift ebenfalls
auf `cfg_vars[var]` zu).

Beleg 3 — `custom_build_dir` ist kein Config-Key, sondern ein GUI-Eingabefeld bzw.
Konstruktor-Argument: oscarpilote `src/O4_Config_Utils.py` Zeile 486
`def __init__(self, lat, lon, custom_build_dir):` und Zeile 977
`custom_build_dir = self.parent.custom_build_dir_entry.get()`.
`custom_overlay_dir` existiert in keinem der beiden Repos überhaupt — der reale Key heißt
`custom_overlay_src`.

Einschränkung: streng genommen wird die Zeile nicht "geräuschlos" ignoriert, sondern erzeugt bei
`verbosity >= 1` die Meldung "Global config file contains an invalid line: …".

Tragweite: niedrig

Vorschlag: Optional präzisieren: "…is silently dropped at load time (Ortho4XP only logs
'Global config file contains an invalid line')". Ebenso könnte `custom_build_dir` als
GUI-Feld-statt-Config-Key erwähnt werden, falls Leser danach suchen.

---

## B1-12 Semantik-Aussagen, die sich wörtlich mit den Upstream-Hints decken

Urteil: BESTÄTIGT (beide Upstreams identisch, sofern nicht anders vermerkt)

| Seite | Beleg (hint, oscarpilote `O4_Config_Utils.py` = shred86 `O4_Cfg_Vars.py`) |
|---|---|
| Z. 116 `mesh_zl` "Also caps the imagery zoom level that can be used on the tile later" | *"The mesh will be preprocessed to accept later any combination of imageries up to and including a zoomlevel equal to mesh_zl. Lower value could save a few tens of thousands triangles, but put a limitation on the maximum allowed imagery zoomlevel."* |
| Z. 123 `limit_tris` "in millions. At `0` a hard limit of 5 million applies" | *"If non zero, approx upper bound _in millions_ on the number of final triangles in the mesh. Note: When 0 we impose a hard limit of 5M, to keep X-Plane comfortable. For high resolution DEMS you _should_ use it."* — deckt auch Z. 126 "Set it explicitly whenever a high-resolution DEM is in use" |
| Z. 133 `road_banking_limit` "in meters — measured as the height difference between a point on the road centerline and the nearest point at the road edge" | *"How much sloped does a roads need to be to be in order to be included in the mesh levelling process. The value is in meters, measuring the height difference between a point in the center of a road node and its closest point on the side of the road."* |
| Z. 136–143 `road_level`-Stufen kumulativ | *"Zero means nothing such is included; "1" looks for banking ways among motorways, primary and secondary roads and railway tracks; "2" adds tertiary roads; "3" brings residential and unclassified roads; "4" takes service roads, and 5 finishes with tracks."* |
| Z. 145 "cached `small_roads.osm` has to be discarded" | *"Purge the small_roads.osm cached data if you change your mind in between the levels 2-5."* |
| Z. 151 `terrain_casts_shadows` | *"If unset, the terrain itself will not cast (but still receive!) shadows. This option is only meaningful if scenery shadows are opted for in the X-Plane graphics settings."* |
| Z. 152 `use_decal_on_terrain` | *"Terrain files for all but water triangles will contain the maquify_1_green_key.dcl decal directive. The effect is noticeable at very low altitude and helps to overcome the orthophoto blur at such levels. Can be slightly distracting at higher altitude."* |
| Z. 153 `normal_map_strength` | *"Orthophotos by essence already contain the part of the shading burned in … This option allows to tweak the normal coordinates of the mesh in the DSF to avoid "overshading", but it has side effects on the way X-Plane computes scenery shadows. Used to be 0.3 by default in earlier versions, the default is now 1 which means exact normals."* |
| Z. 154 `overlay_lod` | *"Distance until which overlay imageries (that is orthophotos over water) are drawn. Lower distances have a positive impact on frame rate and VRAM usage, and IFR flyers will probably need a higher value than VFR ones."* |
| Z. 160 `cover_airports_with_highres` (`ICAO`, `Existing`) | *"…Can be limited to airports with an ICAO code for tiles with so many airports. Exceptional: use "Existing" to (try to) derive custom zl zones from the textures directory of an existing tile."* |
| Z. 171 `masks_width` "In older versions this was counted in ZL14 pixels, roughly a factor of 10" | *"NOTE: The value is now in meters, it used to be in ZL14 pixel size in earlier verions, the scale is roughly one to ten between both."* |
| Z. 173 `use_masks_for_inland` "Expensive in VRAM and, per the upstream hint, probably not worth the effort" | *"…This is VRAM expensive and presumably not really worth the price."* |
| Z. 174 `imprint_masks_to_dds` DXT5-statt-DXT1-Abwägung | *"Will apply masking directly to dds textures (at the Build Imagery/DSF step) rather than using external png files. This doubles the file size of masked textures (dxt5 vs dxt1) but reduce the overall VRAM footprint (a matter of choice!)"* — Formulierung "a trade-off, not a clear improvement either way" trifft *"(a matter of choice!)"* |
| Z. 176 `water_smoothing` | *"Number of smoothing passes over all inland water triangles (sequentially set to their mean elevation)."* |
| Z. 177 `ratio_water` "At `0` the ortho image is fully opaque" | *"At zero, the orthophoto is fully opaque and X-Plane water cannot be seen; at 1 the orthophoto is fully transparent…"* |
| Z. 179 `min_area` "Contiguous water surfaces are merged **before** the area is computed" | *"Minimum area (in km^2) a water patch needs to be in order to be included in the mesh as such. Contiguous water patches are merged before area computation."* |
| Z. 180 `max_area` | *"Any water patch larger than this quantity (in km^2) will be masked like the sea."* |
| Z. 181 `sea_texture_blur` | *"For layers of type "mask" in combined providers imageries, determines the extent (in meters) of the blur radius applied. This allows to smoothen some sea imageries where the wave or reflection pattern was too much present."* |
| Z. 184 Aufbau Inland-Wasser (zwei Ebenen) | *"Inland water rendering is made of two layers: one bottom layer of "X-Plane water" and one overlay layer of orthophoto with constant level of transparency applied."* |
| Z. 188–190 `sea_smoothing_mode` inkl. "from a DEM resolution of 10 m and finer" und "unrealistic cliff edges" | *"Zero means that all nodes of sea triangles are set to zero elevation. With mean, some kind of smoothing occurs (triangles are levelled one at a time to their mean elevation), None (a value mostly appropriate for DEM resolution of 10m and less), positive altitudes of sea nodes are kept intact, only negative ones are brought back to zero, this avoids to create unrealistic vertical cliffs if the coastline vector data was lower res."* |
| Z. 196/199 `custom_dem` (EPSG:4326, GDAL, nicht abgedeckte Bereiche → 0, Inseln) | *"Path to an elevation data file to be used instead of the default Viewfinderpanoramas.org ones (J. de Ferranti). The raster must be in geopgraphical coordinates (EPSG:4326) but the extent need not match the tile boundary (requires Gdal). Regions of the tile that are not covered by the raster are mapped to zero altitude (can be useful for high resolution data over islands in particular)."* |
| Z. 197/199 `fill_nodata` | *"When set, the no_data values in the raster will be filled by a nearest neighbour algorithm. If unset, they are turned into zero (can be useful for rasters with no_data over the whole oceanic part or partial LIDAR data)."* |
| Z. 120/122 `apt_curv_ext` / `coast_curv_ext` "in km" | *"Extent (in km) around the airports where apt_curv_tol applies."* / *"Extent (in km) around the coastline where coast_curv_tol applies."* |
| Z. 124 `apt_smoothing_pix` | *"How much gaussian blur is applied to the elevation raster for the look up of altitude over airports. Unit is the elevation raster pixel size."* |
| Z. 134 `lane_width` | *"Width (in meters) to be used for buffering that part of the road network that requires leveling."* |
| Z. 105 `custom_overlay_src` "one level **above** `Earth nav data`" | *"The directory containing the sceneries with the overlays you would like to extract. You need to select the level of directory just _ABOVE_ Earth nav data."* |
| Z. 104 `custom_scenery_dir` "not a build target" | *"Your X-Plane Custom Scenery. Used only for "1-click" creation (or deletion) of symbolic links from Ortho4XP tiles to there."* |
| Z. 279 "`cover_zl=19` requires `mesh_zl` to be at least `19`" / Z. 255 "`mesh_zl=19` leaves enough headroom that `cover_zl=18` is not capped" / Z. 301 "`mesh_zl=16` … capping the imagery zoom level accordingly" | folgt aus dem `mesh_zl`-Hint (s. o.). Anmerkung: Es gibt keine Laufzeitprüfung dafür — `grep mesh_zl` in `O4_Config_Utils.py` zeigt außer Definition und Listeneintrag keinen Validierungscode. |
| Z. 215 `skip_downloads` / `skip_converts` | *"Will only build the DSF and TER files but not the textures (neither download nor convert)…"* / *"Imagery will be downloaded but not converted from jpg to dds…"* — beide in `cfg_app_vars`/`list_app_vars`, also tatsächlich global-only |

Tragweite: niedrig

Vorschlag: keine Änderung.

---

## B1-13 Global/Per-Tile-Abschnitt: Liste vollständig, aber `global_*`-Mechanik des Forks fehlt

Behauptung (Zeilen 211–215): "Most of the parameters above are written into each tile's own config
… A few are only read from the global `Ortho4XP.cfg` and never appear in a tile config. … Also
global-only: `verbosity`, `cleaning_level`, `max_download_slots`, `max_convert_slots`,
`overpass_server_choice`, `custom_scenery_dir`, `custom_overlay_src` and
`custom_overlay_src_alternate`."

Urteil: BESTÄTIGT (mit Ergänzung)

Beleg: shred86 `src/O4_Cfg_Vars.py` Zeilen 363–381, `list_app_vars` enthält genau:
`verbosity, cleaning_level, overpass_server_choice, skip_downloads, skip_converts,
max_download_slots, max_convert_slots, check_tms_response, http_timeout, max_connect_retries,
max_baddata_retries, ovl_exclude_pol, ovl_exclude_net, custom_scenery_dir, custom_overlay_src,
custom_overlay_src_alternate`. Die Aufzählung der Seite ist damit korrekt, lässt aber
`check_tms_response`, `http_timeout`, `max_connect_retries`, `max_baddata_retries`,
`ovl_exclude_pol`, `ovl_exclude_net` weg (die Seite sagt "Also global-only", nicht "vollständig" —
kein Fehler, nur unvollständig).

Ergänzung zur Beruhigung für Zeile 233 ("The profiles below are complete config fragments and can be
pasted into `Ortho4XP.cfg` as they are"): Der shred86-Fork führt intern ein `global_`-Präfix ein
(`src/O4_Cfg_Vars.py` Z. 6 `global_prefix = "global_"`, Z. 354–359 `cfg_global_tile_vars`), die
Konfigurationsdatei selbst verwendet es aber **nicht**. `src/O4_Config_Utils.py` Zeilen 114–121:

```
            (var, value) = line.split("=", 1)
            value = config_compatibility(value)
            # Set all tile and app config variables
            set_global_variables(var, value)
            # Set all global tile config variables
            var = global_prefix + var
            set_global_variables(var, value)
```

und beim Schreiben Zeilen 1194–1197: *"# Remove global prefix since the cfg file doesn't use it"*.
Unpräfixierte Schlüssel in `Ortho4XP.cfg` funktionieren also in beiden Projekten — die vier Profile
sind in dieser Hinsicht korrekt.

Tragweite: niedrig

Vorschlag: keine Änderung.

---

## B1-14 Profile: rechnerische Nebenaussagen

Behauptungen: Z. 277 "`curvature_tol=1.0` halves the tolerance"; Z. 301 "`min_area=0.1` … a
hundredfold increase over the default"; Z. 301 "`cover_zl=16` matches the base zoom level plus one";
Z. 277 "`mask_zl=16` is the finest permitted mask resolution"; Z. 301 "`mesh_zl=16` is the lowest
permitted value".

Urteil: BESTÄTIGT

Beleg: Defaults `curvature_tol = 2.0` → 1.0 = Halbierung; `min_area = 0.001` → 0.1 = Faktor 100;
Performance-Profil setzt `default_zl=15`, `cover_zl=16` = +1; `"mask_zl": … "values": (14, 15, 16)`;
`"mesh_zl": … "values": (16, 17, 18, 19, 20)`. Alle aus
https://raw.githubusercontent.com/shred86/Ortho4XP/master/src/O4_Cfg_Vars.py bzw.
https://raw.githubusercontent.com/oscarpilote/Ortho4XP/master/src/O4_Config_Utils.py
(Branch `master`, abgerufen 2026-08-03).

Anmerkung ohne Beleg (nicht auf der Seite behauptet, nur zur Kenntnis): Bei `masking_mode=rocks`
(High-Resolution-Profil) muss `masks_width` ein Einzelwert sein — `masks_width=25` erfüllt das.

Tragweite: niedrig

Vorschlag: keine Änderung.

---

## B1-15 Nicht dokumentierte, aber vorhandene Parameter (Vollständigkeitshinweis)

Kein Fehler auf der Seite, nur zur Einordnung: Der Quelltext beider Upstreams kennt neben den
dokumentierten noch `max_levelled_segs` (200000), `water_simplification` (0), `clean_bad_geometries`
(True), `iterate` (0), `distance_masks_too` (False), `masks_use_DEM_too` (False),
`masks_custom_extent` (""), `zone_list` ([]), `check_tms_response` (True), `http_timeout` (10),
`max_connect_retries` (5), `max_baddata_retries` (5), `ovl_exclude_pol` ([0]), `ovl_exclude_net`
([]). Die Seite trifft eine Auswahl und beansprucht keine Vollständigkeit.

Umgekehrt gilt: **kein** auf der Seite dokumentierter Parameter ist upstream entfallen. Neu
hinzugekommen (nur shred86): `custom_overlay_src_alternate`, `max_download_slots` (siehe B1-05).

Urteil: BESTÄTIGT (keine entfallenen Parameter)

Beleg: Mengenvergleich der `cfg_vars`-Schlüssel beider Repos (AST-Parse, s. o.): oscarpilote 58,
shred86 60 Basisschlüssel; Differenz genau die beiden genannten Fork-Ergänzungen.

Tragweite: niedrig

Vorschlag: keine Änderung.

---

## Bilanz

| Urteil | Anzahl |
|---|---|
| FALSCH | 6 (B1-01, B1-02, B1-03, B1-04, B1-05, B1-06, B1-07 — davon B1-03/B1-04/B1-05 nur bezogen auf oscarpilote, B1-08 teilweise) |
| BESTÄTIGT | 7 (B1-10, B1-11, B1-12, B1-13, B1-14, B1-15 sowie der Großteil von B1-09) |
| UNBELEGBAR | 2 (B1-08 Wertebereich/Flächenfaktor, B1-09 Rangaussage) |
| VERALTET | 0 |

Nicht prüfbar / offen:

- `forums.x-plane.org` wurde weisungsgemäß nicht abgerufen; falls einzelne Aussagen der Seite von
  dort stammen, sind sie unbelegt geblieben. Im geprüften Bereich habe ich keine erkannt.
- Das Laufzeitverhalten (tatsächliche Dreieckszahlen bei geändertem `min_angle`, tatsächlicher
  Effekt von `cover_extent` auf die Paketgröße) wurde nicht gemessen, nur gegen Hints geprüft.
- Der shred86-Wiki-Inhalt (`https://github.com/shred86/Ortho4XP/wiki`) wurde nicht ausgewertet — der
  Quelltext ist die härtere Quelle und war für alle Defaults ausreichend.
