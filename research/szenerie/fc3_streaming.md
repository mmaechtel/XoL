# Faktencheck Bereich 3 — "Building Packages for Ortho Streaming" + Profil "Ortho Streaming Package Settings"

Datei: `/home/maechtel/Work/Git/XoL/docs/en/scenery/orthophotography/ortho4xp.md`
Lokaler Install: `/mnt/xplane_data/docker/Ortho4XP` (Fork von shred86 v1.40.13, Commit `0d50ffb`)
Beobachtete Kachel: `/mnt/xplane_data/docker/Ortho4XP/Tiles/zOrtho4XP_+00+032`

---

## B3-01 skip_downloads / skip_converts — das Zusammenspiel ist falsch dargestellt
Behauptung (Zeile 328–335): "Two settings switch them off: `skip_downloads=True` / `skip_converts=True` … Both default to `False`. Left at the default, a package build downloads and converts gigabytes of imagery …"
Ebenso Zeile 322: "`skip_downloads` and `skip_converts` are the two settings that turn a normal build into a mesh-and-terrain-only build."
Ebenso Zeile 215: "The two that matter most are `skip_downloads` and `skip_converts`, which suppress the imagery download and the DDS conversion."
Ebenso Zeile 355: "A `.ter` file from a tile built with `skip_downloads=True` and `skip_converts=True`"

Urteil: ÜBERZOGEN (Teilaussage FALSCH)

Beleg 1 — Hint, wortgleich in allen drei Codebasen:
`/mnt/xplane_data/docker/Ortho4XP/src/O4_Cfg_Vars.py:43` = shred86 `src/O4_Cfg_Vars.py:43` = oscarpilote `src/O4_Config_Utils.py:54` —
"Will only build the DSF and TER files but not the textures (neither download nor convert). This could be useful in cases where imagery cannot be shared."

Beleg 2 — Hint `skip_converts`, `O4_Cfg_Vars.py:49` (identisch upstream, oscarpilote `O4_Config_Utils.py:60`) —
"Imagery will be downloaded but not converted from jpg to dds. Some user prefer to postprocess imagery with third party softwares prior to the dds conversion. In that case Step 3 needs to be run a second time after the retouch work."

Beleg 3 — Kontrollfluss, `/mnt/xplane_data/docker/Ortho4XP/src/O4_Tile_Utils.py:213–216` (identisch shred86 `O4_Tile_Utils.py:213–216`; oscarpilote `O4_Tile_Utils.py:124–127`):
```
    if not skip_downloads:
        download_thread.start()
        download_launched = True
        if not skip_converts:
```
Der `skip_converts`-Zweig ist **in** den `skip_downloads`-Zweig geschachtelt. Bei `skip_downloads=True` wird der Convert-Zweig nie erreicht — `skip_converts` ist dann wirkungslos.

Bewertung: `skip_downloads=True` **allein** erzeugt bereits das Paket aus Mesh und Terrain-Definitionen ohne Bilddaten. `skip_converts=True` trägt dazu **nichts** bei; es ist redundant (schadet aber auch nicht). Umgekehrt gilt die Warnung, die die Seite implizit gibt, in verschärfter Form: Wer nur `skip_converts=True` setzt und `skip_downloads` auf `False` lässt, lädt die Gigabytes weiterhin herunter — genau der Fall, den das Kapitel vermeiden will. Die Seite formuliert die beiden als gleichrangiges Paar und verschleiert damit, welcher der beiden der wirksame Schalter ist.

Tragweite: hoch

Vorschlag (Zeile 328–335 ersetzen):
> Der entscheidende Schalter ist einer:
> ```ini
> skip_downloads=True
> ```
> Er unterdrückt Download **und** Konvertierung — der Hint in der Konfiguration sagt: *"Will only build the DSF and TER files but not the textures (neither download nor convert)."* Im Code ist die Konvertierung im Download-Zweig geschachtelt (`O4_Tile_Utils.py`), sie kann ohne Download gar nicht anlaufen.
>
> `skip_converts=True` wird häufig zusätzlich gesetzt und schadet nicht, ist bei aktivem `skip_downloads` aber wirkungslos. Allein gesetzt bewirkt es das Gegenteil des Gewünschten: die Bilddaten werden weiterhin heruntergeladen, nur nicht nach DDS konvertiert. Wer die Gigabytes sparen will, muss `skip_downloads` setzen — `skip_converts` allein genügt nicht.

Analog Zeile 322 und Zeile 215 anpassen. Zeile 355 kann als Beschreibung der beobachteten Kachel stehen bleiben (dort waren tatsächlich beide gesetzt, siehe `Ortho4XP.cfg:45–46`).

---

## B3-02 Global statt per Tile
Behauptung (Zeile 347): "`skip_downloads` and `skip_converts` exist only in the global `Ortho4XP.cfg`. They are **not** written to the generated per-tile `Tiles/zOrtho4XP_+dd+ddd/Ortho4XP_+dd+ddd.cfg` files and cannot be overridden there."
Ebenso Zeile 349: "Most other build parameters, including `default_zl`, `cover_zl`, `cover_extent`, `mask_zl`, `masking_mode` and `water_tech`, *are* per-tile and are recorded in each tile's config."

Urteil: BESTÄTIGT

Beleg 1 — die schreibende Liste, `/mnt/xplane_data/docker/Ortho4XP/src/O4_Config_Utils.py:271`:
`            for var in list_tile_vars:` — `write_to_config()` iteriert ausschließlich `list_tile_vars`.

Beleg 2 — `O4_Cfg_Vars.py:441–448`:
```
list_tile_vars = (
    list_vector_vars
    + list_mesh_vars
    + list_mask_vars
    + list_dsf_vars
    + list_other_vars
    + ["default_website", "default_zl", "zone_list"]
)
```
`skip_downloads`/`skip_converts` stehen stattdessen in `list_app_vars` (`O4_Cfg_Vars.py:363–381`, Zeilen 367/368) und werden über `write_global_cfg()` (`O4_Config_Utils.py:1186–1206`) ausschließlich in die globale Datei geschrieben.

Beleg 3 — oscarpilote identisch: `list_tile_vars` in `src/O4_Config_Utils.py:423–430` ohne die beiden; `skip_downloads`/`skip_converts` in `list_app_vars:358–359`; `write_to_config` (`:598`) iteriert `for var in list_tile_vars`.

Beleg 4 — shred86 `src/O4_Cfg_Vars.py:367–368` identisch mit lokalem Install (Diff der Zeilen 355–450 beider Dateien: identisch).

Beleg 5 — Praxis: `/mnt/xplane_data/docker/Ortho4XP/Ortho4XP.cfg:45–46` enthält `skip_downloads=True` / `skip_converts=True`; `Tiles/zOrtho4XP_+00+032/Ortho4XP_+00+032.cfg` enthält beide nicht.

Zum Zusatz "cannot be overridden there": faktisch korrekt. Der Tile-Reader (`O4_Config_Utils.py:207–239`) würde eine solche Zeile zwar auf `self.skip_downloads` setzen, aber `O4_Tile_Utils` liest ein Modul-Global (`O4_Tile_Utils.py:20–21`, gesetzt aus der globalen Config über `set_global_variables`, `O4_Config_Utils.py:105–124`) — das Tile-Attribut wird nirgends ausgewertet.

Tragweite: mittel
Vorschlag: keine Änderung.

---

## B3-03 Der `.ter`-Vertrag
Behauptung (Zeile 371): "The `BASE_TEX_NOWRAP` path names the exact DDS file the streaming layer has to deliver at runtime — provider code and zoom level are part of the filename (`_BI17.dds`). The package does not merely suggest a resolution; it demands one specific file per terrain definition."

Urteil: BESTÄTIGT

Beleg 1 — X-Plane-Spezifikation, https://developer.x-plane.com/article/terrain-type-ter-file-format-specification/ —
"BASE_TEX — This specifies the base texture for the terrain." und
"BASE_TEX_NOWRAP — X-PLANE 820: This is the same as the BASE_TEX command, except that texture wrapping is turned off. With texture wrapping, a texture will naturally repeat. With wrapping off, the edge color is extended indefinitely. You will need the no-wrapping tex commands when using orthophotos that tile; they guarantee that filtering does not introduce artifacts across terrain borders."
→ Ein Dateiname, kein Suchmuster. "demands one specific file per terrain definition" ist korrekt und nicht überzogen.

Beleg 2 — dieselbe Quelle, LOAD_CENTER: "This command estabishes that this texture will be used at a certain location, specified by the lat/lon taken to be the texture's center. By also specifying the approximate terrain size when placed (in meters) and textures size (in pixels), X-Plane will load the texture with variable resolution based on the general distance from the user to the texture. … A texture that uses LOAD_CENTER should only be referenced once by one art resource per DSF tile. For optimal performance, the texture should be in DDS format, so that reloads at lower resolution are fast."
→ Stützt die Aussage zusätzlich: die Zuordnung ist als 1:1 gedacht.

Beleg 3 — BORDER_TEX, dieselbe Quelle: "This specifies an additional border texture to be used as an alpha mask. If this command is present, a separate alpha mask is used, otherwise it is not."

Beleg 4 — WET, dieselbe Quelle: "X-PLANE 802: This command declares terrain to be wet. Without this command, all terrain is land. When this command is added, the terrain behaves like water. This command only affects the physics model; visually the terrain is rendered as normal."

Beleg 5 — Provider-Code und ZL im Dateinamen sind Ortho4XP-Konvention, `/mnt/xplane_data/docker/Ortho4XP/src/O4_File_Names.py:437–447`:
```
    else:
        file_name = (
            str(til_y_top) + "_" + str(til_x_left) + "_" + provider_code + str(zoomlevel) + "." + file_ext
        )
```
Provider `BI` existiert als `Providers/Global/BI.lay`.

Tragweite: niedrig
Vorschlag: keine Änderung.

---

## B3-03b `LOAD_CENTER_BORDER`, `DECAL_LIB`, `NO_SHADOW` fehlen in der offiziellen Spezifikation
Behauptung: keine — die Seite zeigt diese Zeilen im Beispiel (Zeilen 364, 366, 368), macht aber keine Aussage über sie.
Urteil: BESTÄTIGT (keine Falschaussage), aber Hinweis
Beleg: https://developer.x-plane.com/article/terrain-type-ter-file-format-specification/ — die Zeichenketten `LOAD_CENTER_BORDER`, `DECAL_LIB`, `DECAL` und `NO_SHADOW` kommen im gesamten Dokument 0-mal vor (geprüft per Volltext-Extraktion). Die Spezifikationsseite ist gegenüber X-Plane 12 nicht nachgeführt.
Tragweite: niedrig
Vorschlag: Optional ein Halbsatz nach dem Codeblock: "Nicht alle Zeilen des Beispiels sind in der offiziellen `.ter`-Spezifikation dokumentiert — `LOAD_CENTER_BORDER`, `DECAL_LIB` und `NO_SHADOW` fehlen dort; die Seite ist auf dem Stand vor X-Plane 12." Kein Muss.

---

## B3-04 Die Zahlen 752 / 559 / 193 / 118
Behauptung (Zeile 375): "Of its 752 `.ter` files, 559 reference `_BI17` and 193 reference `_BI18` — the base zoom level across most of the tile, the higher cover zoom level confined to the airport surroundings. Those are numbers from one observed tile, an illustration of the mechanism rather than a target ratio — the split depends entirely on `cover_extent` and on how many airports the tile contains."
Behauptung (Zeile 377): "Its `textures/` directory holds 118 files against those 752 terrain definitions."

Urteil: BESTÄTIGT

Beleg 1 — Nachgezählt in `/mnt/xplane_data/docker/Ortho4XP/Tiles/zOrtho4XP_+00+032`:
`.ter`-Dateien: 752. Mit `_BI17.dds`: 559. Mit `_BI18.dds`: 193. 559 + 193 = 752. `textures/`: 118 Dateien.

Beleg 2 — Konfiguration der Kachel, `Tiles/zOrtho4XP_+00+032/Ortho4XP_+00+032.cfg`:
`default_zl=17` (Z. 43), `cover_zl=18` (Z. 31), `cover_extent=6.0` (Z. 30), `cover_airports_with_highres=ICAO` (Z. 29).

Beleg 3 — Nachrechnung der Erklärung. Die Kachel enthält 5 Flugplätze (`Data+00+032.apt`, Pickle-Dict): HUEN, HUKJ, HUKC, HUNA (alle `key_type=icao`) und "Kigo airstrip" (`key_type=name`, wegen `cover_airports_with_highres=ICAO` ausgeschlossen). Mit den tatsächlichen Boundary-Bounds, `cover_extent=6.0` km Rand und Rasterung auf 16×16-ZL18-Kacheln (`O4_DSF_Utils.py:145–152`) ergibt die Rechnung 170 verschiedene ZL18-Texturen; beobachtet sind 146 verschiedene `_BI18`-Dateinamen (die Differenz erklärt sich durch Wasserflächen des Victoriasees um HUEN, für die keine Ortho-Terrains gebaut werden). Die Erklärung "confined to the airport surroundings" ist damit quantitativ konsistent, nicht nur plausibel.

Beleg 4 — Die Einschränkung "depends entirely on `cover_extent` and on how many airports the tile contains" ist korrekt, wobei genau genommen auch die **Größe** der Flugplatzflächen eingeht (siehe B3-06).

Tragweite: niedrig
Vorschlag: keine Änderung. Optional präzisieren: "on how many airports the tile contains **and how large they are**".

---

## B3-05 "imagery largely absent" ist zu vorsichtig — sie ist vollständig abwesend
Behauptung (Zeile 377): "That is the expected picture of a mesh-only build: terrain definitions complete, imagery largely absent."

Urteil: ÜBERZOGEN (in die falsche Richtung — untertrieben und dadurch irreführend)

Beleg — Auszählung von `Tiles/zOrtho4XP_+00+032/textures/`: alle 118 Dateien haben die Endung `.png`, **keine einzige `.dds`**. Die Namen folgen dem Muster `65168_77184_ZL17.png` (71× `ZL17.png`, 47× `ZL18.png`) — das ist das BORDER_TEX-Namensschema ohne Provider-Code, nicht das DDS-Schema mit Provider-Code. Gegenprobe: die `.ter`-Dateien referenzieren 118 verschiedene `BORDER_TEX`-Dateien — exakt die 118 vorhandenen Dateien. Es sind Wassermasken, keine Bilddaten.

Die aktuelle Formulierung legt nahe, ein Teil der Bilddaten sei doch vorhanden. Tatsächlich ist der Befund schärfer und stützt die Kernaussage des Kapitels besser: null Bilddaten, dafür der vollständige Satz Masken.

Tragweite: mittel
Vorschlag (Zeile 377 ersetzen):
> Its `textures/` directory holds 118 files against those 752 terrain definitions — and not one of them is a `.dds`. All 118 are the `.png` water masks the terrain definitions reference via `BORDER_TEX`, exactly one per referenced mask. That is the expected picture of a mesh-only build: terrain definitions and masks complete, imagery absent entirely.

---

## B3-06 `cover_extent` ist kein Radius
Behauptung (Zeile 395): "The widest spread is in `cover_extent`, the radius in kilometers around an airport that receives high-resolution coverage."

Urteil: FALSCH

Beleg 1 — Hint, `/mnt/xplane_data/docker/Ortho4XP/src/O4_Cfg_Vars.py:281` (identisch shred86; oscarpilote gleichlautend):
"The extent (in km) past the airport boundary taken into account for higher ZL. Note that for VRAM efficiency higher ZL textures are fully used on their whole extent as soon as part of them are needed."

Beleg 2 — Code, `/mnt/xplane_data/docker/Ortho4XP/src/O4_DSF_Utils.py:143–152`:
```
            (xmin, ymin, xmax, ymax) = dico_airports[airport]["boundary"].bounds
            # extension
            xmin -= 1000 * tile.cover_extent * GEO.m_to_lon(tile.lat)
            xmax += 1000 * tile.cover_extent * GEO.m_to_lon(tile.lat)
            ymax += 1000 * tile.cover_extent * GEO.m_to_lat
            ymin -= 1000 * tile.cover_extent * GEO.m_to_lat
            # round off to texture boundaries at tile.cover_zl zoomlevel
```
Es ist ein **Rand um die Bounding-Box der Flugplatzfläche**, anschließend auf Texturgrenzen aufgerundet — ein Rechteck, kein Kreis, und kein Radius von einem Punkt aus. Für einen 3 km langen Flughafen deckt `cover_extent=0.5` eine ~4×3-km-Fläche ab, nicht einen 0,5-km-Kreis.

Tragweite: hoch (es ist der als "single strongest lever" bezeichnete Parameter; die falsche Semantik führt zu falschen Größenerwartungen)
Vorschlag (Zeile 395 Anfang ersetzen):
> The widest spread is in `cover_extent`, the margin in kilometers added **past the airport boundary** before the high-resolution zone is snapped up to whole texture tiles. It is a buffer around the airport's footprint, not a radius from a point — a large airport therefore receives a much larger high-resolution zone than a small one at the same setting.

---

## B3-07 "radius grows twelvefold and the covered surface roughly a hundredfold"
Behauptung (Zeile 395): "Between `0.5` and `6.0` km the radius grows twelvefold and the covered surface roughly a hundredfold."

Urteil: FALSCH

Beleg 1 — Reine Arithmetik: 6.0 / 0.5 = 12. Bei rein quadratischer Skalierung wäre die Fläche 12² = **144**-fach, nicht "roughly a hundredfold". 144 als "roughly a hundredfold" zu runden ist eine Abweichung von 31 % nach unten.

Beleg 2 — Der quadratische Ansatz gilt aber ohnehin nur für einen punktförmigen Flugplatz. Nach `O4_DSF_Utils.py:143–148` ist die abgedeckte Fläche (B + 2e)·(H + 2e) mit B/H = Ausdehnung der Flugplatzfläche. Nachgerechnet mit den vier ICAO-Flugplätzen der Kachel +00+032 (Bounds aus `Data+00+032.apt`):
- `cover_extent=0.5` → Summe der Bounding-Boxen ≈ 28,0 km²
- `cover_extent=6.0` → Summe der Bounding-Boxen ≈ 716,2 km²
- Faktor ≈ **25,6**

Der reale Faktor liegt also bei rund 26, das theoretische Maximum (punktförmiger Flugplatz) bei 144. "Roughly a hundredfold" trifft weder das eine noch das andere.

Tragweite: mittel
Vorschlag (Zeile 395 Fortsetzung ersetzen):
> Between `0.5` and `6.0` km the margin grows twelvefold. The covered area grows less than the naive twelvefold-squared — the airport's own footprint is already in the box, so the factor depends on airport size: for four medium airports in one observed tile the covered area grew by roughly 25×, with 144× the theoretical ceiling for a point-sized airport. Either way it is the single strongest lever on package size, on the number of high-resolution texture requests a busy terminal area produces, and on how often the scenery changes zoom level between base and airport texture.

---

## B3-08 Tabellenwerte "Streaming profile" / Defaults
Behauptung (Zeilen 385–393): Tabelle mit `mask_zl` "14 (default)", `masking_mode` "sand (default)", `ratio_water` "0.25 (default)", `road_level` "1 (default)", `masks_width` "100 (default)".

Urteil: BESTÄTIGT

Beleg — `/mnt/xplane_data/docker/Ortho4XP/src/O4_Cfg_Vars.py`:
- Z. 225–229 `"mask_zl": { "type": int, "default": 14, "values": (14, 15, 16), …}`
- Z. 231–234 `"masks_width": { "type": list, "default": 100, …}`
- Z. 236–239 `"masking_mode": { "type": str, "default": "sand", "values": ["sand", "rocks", "3steps"], …}`
- `ratio_water` default 0.25
- Z. 125–129 `"road_level": { "type": int, "default": 1, "values": (0,1,2,3,4,5), …}`

Beleg — Produktivwerte, `/mnt/xplane_data/docker/Ortho4XP/Ortho4XP.cfg`: `road_level=3` (Z. 2), `mask_zl=16` (Z. 21), `masks_width=25` (Z. 22), `masking_mode=rocks` (Z. 23), `cover_extent=6.0` (Z. 30), `cover_zl=18` (Z. 31), `ratio_water=0.5` (Z. 34). Alle sieben Tabellenzeilen stimmen mit der beobachteten Konfiguration überein.

Anmerkung: `mask_zl=16` ist der Höchstwert des zulässigen Bereichs `(14, 15, 16)` — das könnte man erwähnen.

Tragweite: niedrig
Vorschlag: keine Änderung. Optional: "`mask_zl=16` is the highest value the parameter accepts."

---

## B3-09 mask_zl / masks_width und masking_mode=rocks
Behauptung (Zeile 399): "a higher `mask_zl` with a narrower `masks_width` produces finer but tighter coastlines, `masking_mode=rocks` suits alpine and rocky shorelines better than the `sand` default"

Urteil: erster Teil BESTÄTIGT, zweiter Teil UNBELEGBAR

Beleg für Teil 1 — `O4_Cfg_Vars.py:229`:
"The zoomlevel at which the (sea) water masks are built. Masks are used for alpha channel, and this channel usually requires less resolution than the RGB ones, the reason for this (VRAM saving) parameter. If the coastline and elevation data are very detailed, it might be interesting to lift this parameter up so that the masks can reproduce this complexity."
und `O4_Cfg_Vars.py:234`:
"Maximum extent of the masks perpendicularly to the coastline (rough definition). NOTE: The value is now in meters, it used to be in ZL14 pixel size in earlier verions, the scale is roughly one to ten between both."
→ Höheres `mask_zl` = feinere Maske ("reproduce this complexity"), niedrigeres `masks_width` = schmalerer Übergangsstreifen ("Maximum extent … perpendicularly to the coastline"). "finer but tighter" ist eine korrekte Zusammenfassung.

Fehlender Beleg für Teil 2 — `O4_Cfg_Vars.py:240`, der einzige Hint zu `masking_mode`:
"A selection of three tentative masking algorithms (still looking for the Holy Grail...). The first two (sand and rocks) requires masks_width to be a single value; the third one (3steps) requires a list of the form [a,b,c] for masks width: … The transition with rocks is more abrupt than with sand."
Der Quelltext sagt ausschließlich, dass der Übergang **abrupter** ist. Von alpinen oder felsigen Ufern steht dort nichts; die Zuordnung ist eine Interpretation des Parameternamens, nicht eine belegte Eigenschaft. Auch in der Upstream-Wiki-Dokumentation kein Beleg gefunden.

Tragweite: mittel
Vorschlag (zweiter Halbsatz von Zeile 399 ersetzen):
> `masking_mode=rocks` makes the shoreline transition more abrupt than the `sand` default — the configuration's own description says only that, nothing about which terrain it suits; the name is suggestive, not a documented guarantee.

---

## B3-10 "road_level=3 adds secondary road networks"
Behauptung (Zeile 399): "and `road_level=3` adds secondary road networks at the cost of more vector data per tile."

Urteil: FALSCH

Beleg — `/mnt/xplane_data/docker/Ortho4XP/src/O4_Cfg_Vars.py:129`:
"Allows to level the mesh along roads and railways. Zero means nothing such is included; \"1\" looks for banking ways among motorways, primary and secondary roads and railway tracks; \"2\" adds tertiary roads; \"3\" brings residential and unclassified roads; \"4\" takes service roads, and 5 finishes with tracks. Purge the small_roads.osm cached data if you change your mind in between the levels 2-5."

Sekundärstraßen ("secondary roads") sind bereits im **Default** `road_level=1` enthalten. Level 3 fügt gegenüber Level 1 die **Tertiär-, Wohn- und unklassifizierten** Straßen hinzu. Die Seite beschreibt damit einen Zugewinn, den man ohnehin schon hat, und lässt den tatsächlichen Zugewinn weg.

Zweitens beschreibt der Parameter nicht das Zeichnen von Straßen, sondern das **Einebnen des Meshes entlang** von Straßen ("Allows to level the mesh along roads and railways") — die Formulierung "adds secondary road networks" suggeriert zusätzlichen Straßeninhalt in der Szenerie, den Ortho4XP hier nicht erzeugt.

Tragweite: mittel
Vorschlag (letzter Halbsatz von Zeile 399 ersetzen):
> and `road_level=3` extends the mesh levelling along roads from the default (motorways, primary and secondary roads, railways) down to tertiary, residential and unclassified roads, at the cost of more vector data per tile.

---

## B3-11 Die Artefakt-Aussage
Behauptung (Zeile 403): "That is a package-size and consistency argument, not a remedy for visual artifacts — those usually originate in texture encoding rather than in the scenery package, and no zoom-level choice removes them."

Urteil: UNBELEGBAR

Beleg (Negativbefund): Für die Kausalaussage "those usually originate in texture encoding" existiert weder im Repository noch in den geprüften Quellen ein Nachweis.
- Kein Beleg im Repo: `grep -rni "artefact|artifact"` über `docs/en/` und `research/` liefert keine einzige Fundstelle, die diese Aussage stützt. Der Entwurf `research/szenerie/draft_B_streaming_en.md:81` enthält denselben Satz — als Text, nicht als Beleg.
- Kein Beleg in Ortho4XP: die Hints zu `default_zl`, `cover_zl`, `mask_zl` und `imprint_masks_to_dds` treffen keine Aussage über die Herkunft visueller Artefakte.
- Kein Beleg bei Laminar: die `.ter`-Spezifikation erwähnt "artifacts" nur einmal, und zwar in genau umgekehrter Richtung — dort geht es um Filterartefakte, die durch `BASE_TEX_NOWRAP` **vermieden** werden: "You will need the no-wrapping tex commands when using orthophotos that tile; they guarantee that filtering does not introduce artifacts across terrain borders." (https://developer.x-plane.com/article/terrain-type-ter-file-format-specification/). Das ist ein Artefakt, das sehr wohl im Szeneriepaket entsteht bzw. dort verhindert wird — es widerspricht dem Wörtchen "usually" eher, als es zu stützen.
- `forums.x-plane.org` als naheliegende Erfahrungsquelle blockt (403), wurde auftragsgemäß nicht herangezogen.

Die Aussage ist eine unbelegte Verallgemeinerung mit dem Verstärker "usually", der eine Häufigkeitsangabe behauptet, für die keine Erhebung existiert. Zeile 401 auf derselben Seite sagt selbst: "These are configuration values seen in practice, not benchmark results." — der Artefaktsatz durchbricht genau diese Selbstbeschränkung.

Tragweite: mittel
Vorschlag (Zeile 403 zweiten Halbsatz ersetzen):
> That is a package-size and consistency argument. It is not a fix for visual artefacts: no zoom-level choice in the package removes them, because the streaming layer produces the imagery and encodes it at runtime. Where such artefacts do come from is outside what this build step controls, and this page makes no claim about it.

---

## B3-12 Das Profil "Ortho Streaming Package Settings"
Behauptung (Zeilen 307–320): zwölf Zeilen `default_zl=16`, `default_website=BI`, `mesh_zl=19`, `min_angle=10.0`, `curvature_tol=2.0`, `water_tech=XP12`, `cover_airports_with_highres=ICAO`, `cover_zl=17`, `cover_extent=0.5`, `imprint_masks_to_dds=False`, `skip_downloads=True`, `skip_converts=True`.

Urteil: BESTÄTIGT (alle zwölf gültig, kein Widerspruch)

Beleg — jeder Key existiert in `O4_Cfg_Vars.py` mit passendem Typ und, wo definiert, zulässigem Wert:
- `default_zl` Z. 269 `{"type": int, "default": 16}` — 16 ok
- `default_website` Z. 268 `{"type": str, "default": ""}` — `BI` existiert als `Providers/Global/BI.lay`
- `mesh_zl` Z. 166–170, `"values": (16, 17, 18, 19, 20)` — 19 ok
- `min_angle` default 10.0 (Wert = Default), `curvature_tol` default 2.0 (Wert = Default) — gültig, aber redundant
- `water_tech` Z. 293–297, `"values": ("XP12", "XP11 + bathy")` — `XP12` ok; Default ist `XP11 + bathy`, die Angabe ist also nötig
- `cover_airports_with_highres` Z. 271–276, `"values": ("False", "True", "ICAO", "Existing")` — `ICAO` ok
- `cover_zl` Z. 283–286 `{"type": int, "default": 18}` — 17 ok
- `cover_extent` Z. 278–281 `{"type": float, "default": 1.0}` — 0.5 ok
- `imprint_masks_to_dds` Z. 247–250 `{"type": bool, "default": False}` — ok (Default, wie die Seite Z. 343 selbst sagt)
- `skip_downloads` / `skip_converts` Z. 39–50 `{"type": bool, "default": False}` — ok

Kein Widerspruch `cover_zl=17` gegen `mesh_zl=19`: `mesh_zl` ist eine Obergrenze, kein Sollwert — Hint Z. 170: "The mesh will be preprocessed to accept later any combination of imageries up to and including a zoomlevel equal to mesh_zl. Lower value could save a few tens of thousands triangles, but put a limitation on the maximum allowed imagery zoomlevel." Mit `mesh_zl=19` ≥ `cover_zl=17` ≥ `default_zl=16` ist die Reihenfolge korrekt; für ein Streaming-Paket ist der Puffer bis 19 sogar sinnvoll, weil die Streaming-Schicht höhere Zoomstufen liefern kann als das Paket beim Bau vorsah.

Kein Widerspruch `cover_zl=17` gegen `default_zl=16`: Hint Z. 286 — "Note that if the cover_zl is lower than the zoomlevel which would otherwise be applied on a specific zone, the latter is used." 17 > 16, also greift `cover_zl`.

Tragweite: niedrig
Vorschlag: keine Änderung. Optional: `min_angle=10.0` und `curvature_tol=2.0` sind exakt die Defaults — entweder streichen oder als "left at the default deliberately" kennzeichnen, damit sie nicht als Empfehlung gegenüber dem Default gelesen werden.

---

## B3-13 Begleitaussagen des Profils (Zeile 322)
Behauptung (Zeile 322): "`default_website=BI` is not merely informational here: the provider code is written into every texture filename the terrain definitions request (`..._BI17.dds`), so it has to match what the streaming layer serves."
Behauptung (Zeile 373): "A package built with `BI` asks for `_BI17.dds`, and a layer configured for a different provider will not answer that name."

Urteil: BESTÄTIGT

Beleg — `/mnt/xplane_data/docker/Ortho4XP/src/O4_File_Names.py:437–447` (siehe B3-03, Beleg 5): der Provider-Code geht unverändert in den Dateinamen ein. Gegenprobe an der Kachel: alle 752 `.ter`-Dateien referenzieren `_BI17.dds` oder `_BI18.dds`, passend zu `default_website=BI` in `Ortho4XP_+00+032.cfg:42`.

Tragweite: niedrig
Vorschlag: keine Änderung.

---

# Zusammenfassung

| Urteil | Anzahl | Befunde |
|---|---|---|
| BESTÄTIGT | 6 | B3-02, B3-03 (+B3-03b), B3-04, B3-08, B3-12, B3-13 |
| FALSCH | 3 | B3-06, B3-07, B3-10 |
| ÜBERZOGEN | 2 | B3-01, B3-05 |
| UNBELEGBAR | 2 | B3-09 (Teilaussage), B3-11 |
| VERALTET | 0 | — |

Tragweite hoch: B3-01, B3-06
Tragweite mittel: B3-05, B3-07, B3-09, B3-10, B3-11
Tragweite niedrig: B3-02 (mittel), B3-03, B3-03b, B3-04, B3-08, B3-12, B3-13

Am lokalen Install wurde ausschließlich gelesen; keine Datei geändert, kein Build gestartet. Keine Repo-Datei geändert.
