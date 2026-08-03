# Faktencheck Bereich 4 — Altbestand ortho4xp.md (LiDAR, Ortho Patches, Notes, Further Reading)

Datei: `/home/maechtel/Work/Git/XoL/docs/en/scenery/orthophotography/ortho4xp.md`
Referenz-Quellcode: `/mnt/xplane_data/docker/Ortho4XP/` — `src/O4_Version.py`: `version='1.40.13'` (= shred86-Fork-Versionslinie)

---

## B4-01 Bash-Skript Namensformat — korrekt

Behauptung (Z. 449-479, Skript `create_link_name` + Schleifen):
```
for lat in $(seq -80 10 80); do
    for lon in $(seq -180 10 180); do
```
mit `printf "+%02d"` / `printf "%03d"` (lat) und `printf "+%03d"` / `printf "%04d"` (lon).

Urteil: BESTÄTIGT (Namensformat), mit kleiner Lücke (siehe B4-02)

Beleg: `/mnt/xplane_data/docker/Ortho4XP/src/O4_File_Names.py:41-44` —
```
def round_latlon(lat, lon):
    strlatround = "{:+.0f}".format(floor(lat / 10) * 10).zfill(3)
    strlonround = "{:+.0f}".format(floor(lon / 10) * 10).zfill(4)
    return strlatround + strlonround
```
und `O4_File_Names.py:299-301` — `base_file_name` = `os.path.join(Elevation_dir, round_latlon(lat, lon), hem_latlon(lat, lon))`, `O4_File_Names.py:26` — `Elevation_dir = resource_path("Elevation_data")`.

Verifikation: Skript nachgebaut und ausgeführt (629 Namen), gegen alle 648 von `round_latlon()` für lat -90..89 / lon -180..179 erzeugten Verzeichnisnamen abgeglichen. **Kein einziger falsch formatierter Name.** Beispiele beidseitig identisch: `+40+000`, `-40-070`, `+00+000`, `-10-010`, `-80-180`.

Tragweite: hoch (weil Gegenteil behauptet werden könnte) — Ergebnis aber Entwarnung
Vorschlag: keine Änderung am Namensformat.

---

## B4-02 Skript deckt das Breitenband -90 nicht ab, erzeugt 17 tote Links bei +180

Behauptung (Z. 472-473): „Latitudes: -80° to +80° in 10° steps" / „Longitudes: -180° to +180° in 10° steps"

Urteil: FALSCH (unvollständig)

Beleg: Vergleich der Skriptausgabe (629 Namen) mit `round_latlon()`-Sollmenge (648):
- fehlend: 36 Verzeichnisse `-90+000` … `-90-180` — `floor(-85/10)*10 = -90`, d. h. jede Kachel südlich von 80°S landet in einem Band, das das Skript nie anlegt.
- überzählig: 17 Verzeichnisse `+00+180` … `-80+180`; `floor(lon/10)*10 = 180` tritt nur bei exakt lon=180 auf, das nie eine Kachel-Untergrenze ist.

Tragweite: mittel (Antarktis-Kacheln; ohne Sonny-Bezug, aber das Skript wird als „alle notwendigen Verzeichnisse" verkauft)
Vorschlag: `seq -90 10 80` und `seq -180 10 170`, Kommentare entsprechend anpassen; Satz „creates all necessary directories" bleibt dann korrekt.

---

## B4-03 sonny.4lima.de — erreichbar, aber „various regions" beschreibt es falsch

Behauptung (Z. 419): „The LiDAR data from [sonny.4lima.de](https://sonny.4lima.de) offers high resolution and accuracy for various regions."

Urteil: VERALTET/ungenau

Beleg: https://sonny.4lima.de — Seitentitel „Sonny's LiDAR Digital Terrain Models of **Europe**"; Abdeckung ausschließlich europäische Staaten plus zugehörige Inselgebiete (Island, Färöer, Grönland, Azoren, Madeira, Kanaren, Svalbard, Jan Mayen); Auflösungen 0.5″/1″/3″ als `.hgt` (SRTM-Format) sowie 10 m/20 m/50 m als GeoTIFF; Lizenz „Creative Commons Attribution 4.0 (CC BY 4.0)". Charakterisierung der Daten: „precise LiDAR elevation sources" aus „Airborne Laserscan", besser als „ASTER, ALOS, COPERNICUS or SRTM" „especially in wooded areas, steep rocky terrain or narrow valleys".
Gegenprobe Alternative: Copernicus DEM EEA-10 (https://dataspace.copernicus.eu/explore-data/data-collections/copernicus-contributing-missions/collections-description/COP-DEM) ist ein **DSM** (Oberflächenmodell inkl. Vegetation/Gebäude), nicht DTM — als Ersatz für Mesh-Bau also schlechter. Sonny bleibt 2026 die richtige Empfehlung.

Tragweite: mittel
Vorschlag: „The LiDAR-derived digital terrain models from [sonny.4lima.de](https://sonny.4lima.de) cover Europe — including Iceland, Greenland, the Azores, Madeira, the Canaries and Svalbard — at 3″, 1″ and, for the Alpine countries, 0.5″ resolution, distributed as SRTM-style `.hgt` files under CC BY 4.0. Outside Europe they are not an option; there is no equivalent DTM of that quality." Die Empfehlung selbst bleibt.

---

## B4-04 Aerosoft-Forumslink — lädt, ist aber von Januar 2023

Behauptung (Z. 438): „Scripts like [this one](https://forum.aerosoft.com/index.php?/topic/175397-h%C3%B6hendaten-f%C3%BCr-ortho4xp/#findComment-1102723) can help"

Urteil: VERALTET (funktional, aber unter der 2024-Quellenregel unzulässig)

Beleg: https://forum.aerosoft.com/index.php?/topic/175397-höhendaten-für-ortho4xp/ — Thread „Höhendaten für Ortho4XP", erster Beitrag 28. Januar 2023, letzter Beitrag 29. Januar 2023. Eröffnungsbeitrag: „Ich benötige Hilfe beim ersten Arbeiten mit Ortho4XP: Ist es sinnvoll, notwendig, Höhendaten aus HD Mesh Scenery v4 zu integrieren." Inhalt: Empfehlung, statt HD Mesh v4 Sonny-Daten zu nehmen, plus ein Python-Sortierskript.

Bewertung: Die Seite lebt und der Rat ist sachlich nicht falsch, aber (a) Quelle von 2023, (b) deutschsprachiges Forum als Beleg auf der EN-Seite, (c) inhaltlich redundant zum direkt darunter stehenden eigenen Skript. Kein technischer Irrtum, aber verzichtbar.

Tragweite: mittel
Vorschlag: Link streichen; der Satz wird zu „Extract the files into the Ortho4XP directory and sort the tiles into the appropriate `Elevation_data` subdirectories — the directory name is the 10°×10° block, e.g. `+40+000` for N47 E008." Damit steht die Regel im Text statt in einem Fremdlink.

---

## B4-05 `flatten 1` steht in keiner offiziellen apt.dat-Spezifikation

Behauptung (Z. 507): „In the `apt.dat` file, the flag `flatten 1` may be set. This flag causes the scenery itself, and often a larger surrounding area, to be rendered completely flat."

Urteil: teils BESTÄTIGT (Existenz und Wirkung), teils UNBELEGBAR (Reichweite „larger surrounding area"), Darstellung VERALTET

Beleg:
- Offizielle apt.dat 12.00-Spezifikation, https://developer.x-plane.com/article/airport-data-apt-dat-12-00-file-format-specification/ — die dokumentierten 1302-Metadaten-Keys sind `icao_id, faa_id, iata_id, city_id, country_id, region_id, local_id, local_authority, transition_alt, transition_level, gui_3d, is_oilrig, allows_circuits`. **`flatten` ist nicht darunter.** Der einzige Treffer für „flatten": „130 Airport boundary — Boundary for future terrain 'flattening'".
- APT-1100-Spezifikation (PDF, Rev. 16-Nov-2021), https://developer.x-plane.com/wp-content/uploads/2021/11/XP-APT-1100-Spec_rev_16_11_2021.pdf — `pdftotext`-Volltextsuche nach „flatten" ergibt genau **eine** Zeile: `130      Airport boundary          Boundary for future terrain 'flattening'`. Kein `1302 flatten`-Eintrag.
- Dass X-Plane 12 den Key trotzdem auswertet, belegt https://github.com/Starlux531/X-Plane-12-Airport-Flatten-Tool (erstellt 2025-07-14, letzter Push 2025-07-31): „It automatically edits the apt.dat file and batch adds/removes `1302 flatten 1` lines to manage airport terrain flattening" — „to resolve terrain issues caused by the official removal of the 'Runways follow terrain contours' option".

Konsequenz: `flatten 1` ist ein **undokumentierter Legacy-Key** — er heißt korrekt `1302 flatten 1` (Zeilencode 1302, Metadatenzeile), nicht „the flag `flatten 1`". Die Aussage, er lasse „often a larger surrounding area" flach werden, ist durch keine Spezifikation gedeckt; die Spezifikation kennt für die Ausdehnung nur die 130-Airport-Boundary. Und: unter X-Plane 12 ist das Setzen des Keys inzwischen der **empfohlene Workaround** für den Wegfall von „Runways follow terrain contours" — das Entfernen ist also nicht mehr pauschal der Rat, sondern eine Abwägung.

Tragweite: hoch
Vorschlag: Zeilencode ergänzen und die Wirkungsangabe entschärfen — „Some sceneries carry a `1302 flatten 1` metadata line in `apt.dat`. The key is not part of the official apt.dat specification (neither the 1100 nor the 12.00 revision list it among the 1302 keys), but X-Plane still honours it and flattens the airport terrain. Since X-Plane 12 removed the global 'Runways follow terrain contours' option, the key cuts both ways: removing it lets the airport follow an Ortho4XP mesh, adding it is the usual fix when a scenery's objects no longer sit on the ground." — plus Hinweis, dass eigene Änderungen an `apt.dat` bei jedem Gateway-/Scenery-Update überschrieben werden.

---

## B4-06 „The shred86 fork offers better performance and more features"

Behauptung (Z. 520): „The shred86 fork offers better performance and more features"

Urteil: teils UNBELEGBAR („better performance"), teils BESTÄTIGT („more features")

Beleg:
- Der Fork ist nicht stagniert: GitHub-API `repos/shred86/Ortho4XP` — `pushed_at` 2026-07-04, `updated_at` 2026-07-31, `archived: false`, 90 Sterne, 9 offene Issues.
- README (https://raw.githubusercontent.com/shred86/Ortho4XP/master/README.md) belegt Features: „Code changes to enable using PyInstaller to bundle Ortho4XP and its dependencies into a single package", getrennte Config-Tabs (Tile/Global/Application), „Reset to Global"/„Reset to Defaults", neuer Key `max_download_slots` für parallele Imagery-Downloads, Symlink-Erstellung für den Overlays-Ordner, Retry bei fehlgeschlagenen Downloads.
- **Keine** Aussage im README zu Laufzeit-/Durchsatzvorteilen. `max_download_slots` ist die einzige performancenahe Änderung, und die betrifft nur den Download, nicht Mesh oder DDS-Kompression.

Tragweite: mittel
Vorschlag: „The shred86 fork adds packaging (PyInstaller binaries), a reworked configuration UI and a `max_download_slots` setting for parallel imagery downloads; the mesh and texture pipeline is unchanged, so it is not faster per se." — die Performance-Behauptung ersatzlos streichen.

---

## B4-07 „Using an SSD can significantly reduce processing time"

Behauptung (Z. 528): „Using an SSD can significantly reduce processing time"

Urteil: UNBELEGBAR

Beleg: Keine Quelle ab 2024 mit Messwerten auffindbar; die verlinkte Zielseite `docs/en/linux/optimizations/filesystem.md` enthält laut `grep -i "ortho4xp\|tile generation"` **keinen einzigen Treffer** zu Ortho4XP oder Tile-Generierung, kann die Behauptung also auch intern nicht stützen. Sachlich ist der Flaschenhals bei Ortho4XP das Herunterladen der Imagery und die DDS-Kompression (CPU), nicht der Datenträger — belegbar ist nur der Speicherbedarf, nicht der Zeitgewinn.

Tragweite: mittel
Vorschlag: entweder konkretisieren („the finished tiles live better on an SSD because X-Plane streams them at runtime — the build itself is bound by download bandwidth and DDS compression") oder streichen. Die übrigen drei Punkte des Abschnitts (Zoomlevel/Fläche, Überlastung, `skip_downloads`/`skip_converts`) sind unbedenklich.

---

## B4-08 `magick identify -verbose` zeigt die Mipmap-Anzahl NICHT

Behauptung (Z. 540): „Verify it after a batch run rather than assuming it — `magick identify -verbose file.dds` reports the mipmap count, which should be one level per halving down to 1x1."

Urteil: FALSCH

Beleg: lokal nachgemessen mit ImageMagick 7.1.1-43 Q16 (`magick -version`):
```
magick -size 512x512 gradient:red-blue -define dds:mipmaps=9 -define dds:compression=dxt1 t.dds
magick -size 512x512 gradient:red-blue -define dds:mipmaps=0 -define dds:compression=dxt1 nom.dds
```
- `magick identify -verbose t.dds` → 140 Zeilen Ausgabe, `grep -ic mipmap` = **0**. Kein Feld nennt Mipmaps.
- Beide Dateien liefern bei `identify -verbose` identische relevante Felder: `Geometry: 512x512+0+0`, `Compression: DXT1`.
- `magick identify 't.dds[0-9]'` liefert nur **eine** Szene — die Mipmaps werden nicht als weitere Bilder ausgewiesen.
- Dass die Mipmaps tatsächlich vorhanden sind, zeigt erst der DDS-Header: `dwMipMapCount` an Byte-Offset 28 ist `10` für `t.dds` und `1` für `nom.dds` (Dateigrößen 174904 B vs. 131200 B).

Tragweite: hoch (die Anweisung liefert dem Leser eine Scheinprüfung — mit und ohne Mipmaps sieht die Ausgabe gleich aus)
Vorschlag: Prüfmethode ersetzen —
```bash
# dwMipMapCount steht im DDS-Header an Byte-Offset 28
python3 -c "import struct,sys;print(struct.unpack('<I',open(sys.argv[1],'rb').read(32)[28:])[0])" file.dds
```
Alternativ genügt der Dateigrößen-Vergleich: eine vollständige Mipmap-Kette macht eine DXT-Datei rund 1/3 größer als die reine Basisebene.

---

## B4-09 LOAD_CENTER: die Pixelgröße im .ter bleibt beim Verkleinern auf 4096 stehen

Behauptung (Z. 540): „That last point is the one that matters: X-Plane's `LOAD_CENTER` mechanism picks a mipmap level by distance, so a texture rescaled without a complete chain would break distance-based resolution."

Urteil: teils BESTÄTIGT, in der Schwerpunktsetzung aber FALSCH

Beleg:
- Spezifikation https://developer.x-plane.com/article/terrain-type-ter-file-format-specification/ — „This command estabishes that this texture will be used at a certain location, specified by the lat/lon taken to be the texture's center. By also specifying the approximate terrain size when placed (in meters) and **textures size (in pixels)**, X-Plane will load the texture with variable resolution based on the general distance from the user to the texture." Beispiel: `LOAD_CENTER 42.70321 -72.34234 4000 1024`.
- Die Spezifikation spricht **nicht** von Mipmap-Level-Auswahl, sondern von einem Nachladen der Textur in variabler Auflösung; die Pixelgröße ist ein **Argument des Befehls**.
- Ortho4XP schreibt diese Pixelgröße **fest verdrahtet als 4096** — `/mnt/xplane_data/docker/Ortho4XP/src/O4_DSF_Utils.py:296-303`:
```
f.write(
    "LOAD_CENTER "
    + "{:.5f}".format(lat_med)
    ...
    + str(texture_approx_size)
    + " 4096\n"
)
```
Wer die DDS mit `mogrify -resize 2048x2048` halbiert, lässt in jeder `terrain/*.ter` die Angabe `4096` stehen. Die `.ter`-Dateien behaupten danach die doppelte Auflösung der tatsächlich vorhandenen Textur.

Tragweite: hoch
Vorschlag: Der Absatz muss den Schwerpunkt wechseln — nicht die Mipmap-Kette ist der kritische Punkt (die baut ImageMagick nachweislich mit), sondern die `.ter`-Deklaration. Ergänzen:
„Ortho4XP hardcodes the texture size in the `.ter` files — `LOAD_CENTER <lat> <lon> <meters> 4096`. Halving the DDS without touching the `.ter` leaves X-Plane with a declared size that no longer matches the file, so the `.ter` files have to be rewritten in the same pass:
```bash
sed -i 's/ 4096$/ 2048/' terrain/*.ter
```"
(Hinweis: `LOAD_CENTER_BORDER` in `O4_DSF_Utils.py:324-333` trägt eine abgeleitete, kleinere Größe `4096 // 2**(zoomlevel - mask_zl)` und darf nicht pauschal mitersetzt werden — ein `sed` auf Zeilenende `4096` trifft nur die Basiszeile.)

---

## B4-10 2048×2048 als Zielgröße für X-Plane 12

Behauptung (Z. 537): „Halving the edge length quarters the file size, and 2048x2048 is a reasonable compromise between visual quality and storage requirements."

Urteil: BESTÄTIGT (technisch zulässig), aber ohne den Kontext irreführend

Beleg: Ortho4XP-Texturen sind 4096×4096 (`O4_DSF_Utils.py:293` — `GEO.webmercator_pixel_size(lat_med, zoomlevel) * 4096`). Eine Halbierung auf 2048 entspricht exakt einem Zoomlevel weniger — dasselbe Ergebnis erreicht man verlustfrei und ohne Nachbearbeitung, indem man `default_zl` um 1 senkt und die Kachel direkt kleiner baut. Die Nachbearbeitung ist nur für **bereits gebaute** Kacheln sinnvoll.

Tragweite: mittel
Vorschlag: Satz ergänzen: „For tiles not yet built, lowering `default_zl` by one achieves the same result without a rescaling pass — this section is for reclaiming space on tiles that already exist."

---

## B4-11 shred86-Wiki existiert und hat Inhalt

Behauptung (Z. 548): „Consult the [shred86 fork documentation](https://github.com/shred86/Ortho4XP/wiki)"

Urteil: BESTÄTIGT

Beleg: https://github.com/shred86/Ortho4XP/wiki — vorhandene Seiten: Home, Basic Setup, Beyond Basics, Development, FAQ, Installation, User Interface & Settings. Home-Seite zuletzt bearbeitet 6. Juni 2024 (17 Revisionen), Inhalt vorhanden: Ortho4XP „builds the base mesh and ground texture using elevation data and orthophoto imagery."

Tragweite: niedrig
Vorschlag: keine Änderung. (Anmerkung: Stand Juni 2024 — bei künftigen Audits als Stale-Risiko im Auge behalten, da der Code selbst bis 2026-07 weiterentwickelt wird.)

---

## B4-12 forums.x-plane.org — veraltete URL-Struktur

Behauptung (Z. 549 und Z. 575): `https://forums.x-plane.org/index.php?/forums/forum/310-ortho4xp/`

Urteil: VERALTET

Beleg: Kein Abruf (403, wie vorgegeben). Belegt über aktuelle Suchtreffer derselben Domain, die durchgehend die kurze Form ohne `index.php?/` verwenden: `https://forums.x-plane.org/forums/topic/165525-sonnys-lidar-digital-terrain-models-of-europe/` und `https://forums.x-plane.org/files/file/96241-simple-flatten-manager-beta-cli-017/`. Die `index.php?/`-Form stammt aus der alten IPB-Konfiguration und wird nur noch per Redirect bedient.

Tragweite: niedrig
Vorschlag: beide Vorkommen auf `https://forums.x-plane.org/forums/forum/310-ortho4xp/` kürzen.

---

## B4-13 Basic Usage: es gibt keinen Button „Build"

Behauptung (Z. 82, Basic Usage Schritt 3): „Click "Build" to start the process"

Urteil: FALSCH

Beleg: `/mnt/xplane_data/docker/Ortho4XP/src/O4_GUI_Utils.py` — die Buttons im Hauptfenster heißen (Zeilen 301, 305, 314, 323, 327):
```
301: text="Assemble Vector data",
305: text="Triangulate 3D Mesh"
314: text=" Draw Water Masks  "
323: text=" Build Imagery/DSF ",
327: text="    All in one     ", command=self.build_all
```
Ein Button „Build" existiert nicht. Der Ein-Klick-Weg ist „All in one"; „Build Imagery/DSF" ist nur der letzte von vier Schritten. Ebenso heißen die Eingabefelder „Imagery:" und „Zoom Level:" (Z. 209, 224), nicht „imagery source" / „desired zoom level".

Tragweite: mittel
Vorschlag: „3. Click **All in one** to run the full chain (vector data → mesh → water masks → imagery/DSF), or step through the four buttons individually — `Assemble Vector data`, `Triangulate 3D Mesh`, `Draw Water Masks`, `Build Imagery/DSF` — when only part of the build needs to be repeated."

---

## B4-14 Basic Usage: Startbefehl und Provider

Behauptung (Z. 74-81): `python Ortho4XP.py`, Imagery-Quellen „e.g., Bing, Google, Here"

Urteil: BESTÄTIGT

Beleg: `/mnt/xplane_data/docker/Ortho4XP/Ortho4XP.py` existiert im Wurzelverzeichnis. `Providers/Global/` enthält `BI.lay` (Bing), `GO2.lay` (Google), `Here.lay`, ferner `Arc.lay`, `Arc@.lay`, `EOX.lay`, `OSM.lay`, `SEA.lay`, `USA2.lay`.

Tragweite: niedrig
Vorschlag: keine Änderung.

---

## B4-15 Further Reading — Focus-Spalte

Behauptung (Z. 555-564, 8 Zeilen — der Auftrag nennt sechs, die Tabelle hat acht)

Urteil: 7× BESTÄTIGT, 1× ungenau

Beleg (jeweils `description:`-Frontmatter bzw. Überschriften der Zielseite):
- AutoOrtho / „Streaming alternative to static generation" — `autoortho.md:2`: „AutoOrtho streams satellite imagery into X-Plane in real time via FUSE… and Ortho4XP comparison." BESTÄTIGT
- XEarthLayer / „Rust-based streaming alternative" — `xearthlayer.md:6`: „**XEarthLayer** is a Rust-based alternative to AutoOrtho for streaming orthophoto textures in X-Plane 12." BESTÄTIGT
- XPME / „Closed-source freemium streaming, conflicts with Ortho4XP tiles" — `xpme.md:99`: „Ortho4XP and X-Plane HD Mesh Scenery override XPME's base packages and are named as known conflicts"; `xpme.md:119`: „| Combinable with Ortho4XP tiles | No — documented conflict |". BESTÄTIGT
- How Streaming Works / „What the streaming layer contributes at runtime" — `how_streaming_works.md:2`: „the DSF→.ter→DDS texture chain, FUSE virtual filesystem, streaming pipeline, cache architecture". BESTÄTIGT
- Static + Streaming / „Combining Ortho4XP with streaming solutions" — `static_plus_streaming.md:4`: „# Combining Static Orthophotos with Streaming". BESTÄTIGT
- Scenery Components / „scenery_packs.ini load order" — `scenery_components.md:57`: „## The scenery_packs.ini Load Order". BESTÄTIGT
- Orthophotography / „Overview of static and streaming approaches" — `orthophotography_intro.md:2`: „Static generation vs. ortho streaming for X-Plane ground textures." BESTÄTIGT
- **Filesystem / „SSD performance for tile generation and storage"** — `filesystem.md:2`: „Filesystem optimization for X-Plane on Linux: NVMe SSD setup, Ext4/Btrfs/XFS comparison, mount options, RAID-0 configuration, and backup strategies." `grep -i "ortho4xp\|tile generation" filesystem.md` → **keine Treffer**. Die Seite behandelt SSDs allgemein, nicht Tile-Generierung. ungenau

Tragweite: niedrig
Vorschlag: Focus-Spalte der Filesystem-Zeile zu „NVMe/SSD setup, filesystem choice and mount options for the storage the tiles live on" ändern.

---

## Zusammenfassung

| Urteil | Anzahl |
|---|---|
| BESTÄTIGT | 4 (B4-01, B4-11, B4-14, B4-15 überwiegend) |
| FALSCH | 4 (B4-02, B4-08, B4-09 Schwerpunkt, B4-13) |
| VERALTET | 4 (B4-03, B4-04, B4-05 Darstellung, B4-12) |
| UNBELEGBAR | 2 (B4-06 Performance-Teil, B4-07) |

Tragweite hoch: B4-05, B4-08, B4-09 (B4-01 hoch geprüft, Ergebnis Entwarnung)
Tragweite mittel: B4-02, B4-03, B4-04, B4-06, B4-07, B4-10, B4-13
Tragweite niedrig: B4-11, B4-12, B4-14, B4-15
