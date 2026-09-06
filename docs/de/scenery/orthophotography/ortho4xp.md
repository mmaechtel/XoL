---
title: "Ortho4XP unter Linux: Installation, OrthoForge, Parameter"
description: "Ortho4XP erzeugt hochauflösende Satelliten-Bodentexturen für X-Plane — Installation, OrthoForge, Parameter-Referenz und LiDAR unter Linux."
---
# Ortho4XP

Ortho4XP ist ein leistungsfähiges Werkzeug zur Erstellung von Orthofotos für X-Plane. Es ermöglicht die Generierung hochauflösender Bodentexturen aus Satellitenbildern und Höhendaten.

## Installation und Versionen

Ortho4XP ist in mehreren Versionen verfügbar:

1. **Originalversion** von Oscar Pilote:
    - [GitHub-Repository](https://github.com/oscarpilote/Ortho4XP)
    - Die ursprüngliche Version mit grundlegenden Funktionen

2. **Fork von shred86** (empfohlen):
    - [GitHub-Repository](https://github.com/shred86/Ortho4XP)
    - [Ausführliche Dokumentation](https://github.com/shred86/Ortho4XP/wiki)
    - Enthält zahlreiche Verbesserungen und neue Funktionen
    - [Fertige Pakete](https://github.com/shred86/Ortho4XP/wiki/Installation) für Windows, macOS (ARM) und Linux (Debian- und Arch-Build, x86-64)

3. **OrthoForge** (eigenständig entwickelter Nachfolger):
    - [Projektseite und Dokumentation](https://xpconnect.me/orthoforge.html) — GPL v3, gepflegt von xbard
    - Begann als englischer Fork des ORTHO4XP_V3 von Roland (Ypsos) und wird inzwischen eigenständig entwickelt; ein Abgleich mit einem Ortho4XP-Upstream findet nicht mehr statt. Das Projekt nennt Oscar Pilote (ursprüngliches Ortho4XP), shred86 (1.40er-Linie) und Roland/Ypsos (V3-Architektur) als Grundlage
    - Ausgerichtet auf X-Plane 12 — `XP11 + bathy` wird in der V2-Engine nicht mehr unterstützt. Die XP12-Materialzusätze wie die Terrain-Rauheit sind zuschaltbar und vorgabemäßig aus

!!! warning "Das OrthoForge-Quell-Repository wird abgebaut"

    In der Beschreibung des [Codeberg-Repositories](https://codeberg.org/xbard/OrthoForge) steht: *"Due to changes in Codeberg policy, this repo will soon be deleted and hosted at https://xpconnect.me/orthoforge.html"*. Es ist weiterhin der Ort, auf den die Projektseite zum Herunterladen verweist, und es wird weiterhin bespielt — der Link kann aber jederzeit wegbrechen, dauerhafter Einstieg ist die Projektseite.

**Was OrthoForge anders macht**

| Bereich | Unterschied |
|---|---|
| OSM-Download | Kann vorgefertigte OpenStreetMap-Layer von einem Spiegel laden, statt Overpass abzufragen. Das beseitigt die Rate-Limit-Wartezeiten, die große Stapelläufe dominieren — siehe [Vorgefertigte OSM- und DEM-Daten](#vorgefertigte-osm-und-dem-daten) |
| Höhendaten | Land- und Meeresbodenhöhen werden als getrennte Quellen konfiguriert (`custom_dem_search_dirs` / `custom_bathy_search_dirs`), ein hochauflösender Landdatensatz muss also nicht mehr mit der Bathymetrie in einer Datei zusammengeführt werden |
| Flughäfen | Die Zoomstufe der Flughafenabdeckung ist abgestuft statt einer einzelnen `cover_zl`-Stufe |
| XP12-Terrain | Macht die XP12-Materialparameter einschließlich der Terrain-Rauheit in der Kachel-Konfiguration zugänglich |

**Einrichtung unter Linux**

- `OrthoForge_Setup_Linux.sh` führt durch die Einrichtung; `setup_venv.sh` ist die reine Shell-Alternative für Distributionen mit gesperrtem System-pip (PEP 668) und benötigt keine Root-Rechte
- Erfordert Python 3.10 oder neuer. Der Build läuft in einer virtuellen Umgebung, die mit `--system-site-packages` angelegt wird und damit systemseitig installiertes tkinter sowie die optionalen GDAL-Bindings übernimmt, statt sie neu zu bauen
- Vorab benötigte Distributionspakete: tkinter und die Tk-Bindings von Pillow. GDAL ist optional — der Höhendatenpfad bevorzugt rasterio
- Das mitgelieferte `INSTALL_PREREQUISITES.py` deckt Fedora, Debian/Ubuntu, Arch und macOS ab. Auf anderen Distributionen sind die Pakete von Hand zu installieren

### Installationsmethoden

1. **Verwendung der fertigen Pakete (empfohlen)**:
    - Die Download-Links stehen auf der Installationsseite des Wikis, nicht auf der GitHub-Release-Seite — die Releases enthalten keine Dateianhänge. Sie verweisen auf Google Drive und nennen SHA-256-Prüfsummen
    - Das zum Betriebssystem passende Paket wählen, das Archiv entpacken
    - Die ausführbare Datei starten

2. **Manuelle Installation**:
    - Die gewünschte Version herunterladen
    - Sicherstellen, dass Python 3.x installiert ist
    - Die benötigten Python-Pakete installieren:

        ```bash
        pip install -r requirements.txt
        ```

3. **Alternative Installation für Linux**:
    - Installation mit Docker (siehe [Docker-Dokumentation](../../linux/extensions/docker.md))
    - Installation mit pyenv (siehe [pyenv-Dokumentation](../../linux/extensions/pyenv.md))

## Verwendung und Konfiguration

### Grundlegende Verwendung

1. Ortho4XP über die Python-Datei oder die ausführbare Datei starten:

    ```bash
    python Ortho4XP.py
    ```

2. Im Hauptfenster auswählen:
    - Das Zielgebiet (Kachel)
    - Die gewünschte Zoomstufe (ZL)
    - Die Bildquelle (z.B. Bing, Google, Here)

3. Den Bau starten. Die Oberfläche bietet die Schritte einzeln an — "Assemble Vector data", "Triangulate 3D Mesh", "Draw Water Masks", "Build Imagery/DSF" — oder "All in one", um sie nacheinander auszuführen

### Wichtige Parameter

Alle Einstellungen stehen in `Ortho4XP.cfg` im Ortho4XP-Verzeichnis. Beim Bau einer Kachel schreibt Ortho4XP die kachelspezifische Teilmenge dieser Schlüssel nach `Tiles/zOrtho4XP_+dd+ddd/Ortho4XP_+dd+ddd.cfg`. Eine fertige Kachel behält damit die Einstellungen, mit denen sie gebaut wurde, auch wenn sich die globale Konfiguration später ändert. Die folgenden Vorgabewerte sind die des shred86-Forks, definiert in `src/O4_Cfg_Vars.py`. Das Original von Oscar Pilote führt dieselben Definitionen inline in `src/O4_Config_Utils.py`; wo beide abweichen, steht es auf dieser Seite.

Die Parameter sind danach gruppiert, welche Frage sie beantworten:

| Gruppe | Beantwortet |
|---|---|
| Verzeichnisse und Bildquelle | Wohin die Kacheln geschrieben werden und welcher Anbieter die Bilddaten liefert |
| Mesh-Erzeugung | Wie dicht und wie gut geformt die Geländedreiecke sind |
| Straßen | Wie viel des Straßennetzes ins Gelände eingeebnet wird |
| Terrain-Darstellung | Schatten, Decals und Zeichenweite der Overlays |
| Hochauflösende Flughafenabdeckung | Wo die Szenerie auf eine höhere Zoomstufe wechselt |
| Masken und Wasser | Küstenlinien, Binnengewässer und ihre Transparenz |
| Höhendaten | Aus welchem Höhendatensatz das Mesh gebaut wird |

**Verzeichnisse und Bildquelle**

| Parameter | Vorgabe | Beschreibung |
|---|---|---|
| `custom_scenery_dir` | `""` | Ziel für das Anlegen und Entfernen symbolischer Links aus den Ortho4XP-Kacheln per Ein-Klick-Funktion — kein Build-Ziel |
| `custom_overlay_src` | `""` | Quelle für Overlay-Daten. Das Verzeichnis eine Ebene **über** `Earth nav data` auswählen |
| `custom_overlay_src_alternate` | `""` | Ausweichpfad, wird genutzt, wenn die erste Quelle für eine Kachel nichts liefert. Nur im shred86-Fork — das Original ignoriert ihn |
| `default_website` | `""` | Bildquelle, z.B. `BI` (Bing), `GO2` (Google), `Arc` (ESRI World Imagery). Die verfügbaren Kürzel sind die `.lay`-Dateien unter `Providers/` |
| `default_zl` | `16` | Basis-Zoomstufe der Orthotexturen |

Einen Schlüssel `zoomlevel` oder `provider` gibt es nicht — diese Namen tauchen in älterer Dokumentation und im internen Code auf, doch eine Konfigurationsdatei, die sie enthält, wird ohne Wirkung eingelesen. Stattdessen `default_zl` und `default_website` verwenden.

**Mesh-Erzeugung**

| Parameter | Vorgabe | Beschreibung |
|---|---|---|
| `mesh_zl` | `19` | Mesh-Auflösung, zulässige Werte `16`–`20`. Begrenzt zugleich die Zoomstufe der Bilddaten, die später auf der Kachel verwendet werden kann |
| `min_angle` | `10.0` | Minimaler Dreieckswinkel in Grad — der kleinste Winkel bei Wasserdreiecken, der zweitkleinste bei gewöhnlichen Landdreiecken |
| `curvature_tol` | `2.0` | Toleranz für die Geländekrümmung. Höhere Werte erzeugen **weniger** Dreiecke |
| `apt_curv_tol` | `0.5` | Krümmungstoleranz im Umfeld von Flughäfen |
| `apt_curv_ext` | `0.5` | Ausdehnung der Flughafen-Krümmungszone, in km |
| `coast_curv_tol` | `1.0` | Krümmungstoleranz entlang von Küstenlinien |
| `coast_curv_ext` | `0.5` | Ausdehnung der Küsten-Krümmungszone, in km |
| `limit_tris` | `3.0` | Obergrenze für die Dreieckszahl einer Kachel, in Millionen. Bei `0` — und ab einem Wert von 50 — gilt eine harte Grenze von 5 Millionen |
| `apt_smoothing_pix` | `8` | Stärke der Weichzeichnung auf dem Höhenraster für Höhenabfragen über Flughäfen, in Rasterpixeln |

`min_angle` ist der stärkste Einzelhebel auf die Mesh-Qualität und einer der ersten Werte, an denen sich eine Anpassung lohnt. Ein höherer Wert erzwingt besser geformte Dreiecke und beseitigt die schmalen Splitter, die Schattierungsartefakte und unruhige Pistenoberflächen verursachen; ein niedrigerer Wert ergibt ein gröberes, billigeres Mesh. Sowohl ein höheres `min_angle` als auch ein niedrigeres `curvature_tol` erhöhen die Dreieckszahl, weshalb `limit_tris` als Obergrenze wirkt. Beim Einsatz eines hochauflösenden DEM ist er ausdrücklich zu setzen — ein solcher Datensatz kann die Dreieckszahl sonst weit über das für die Kachel Nötige treiben.

**Straßen**

| Parameter | Vorgabe | Beschreibung |
|---|---|---|
| `road_level` | `1` | Wie viel des OSM-Straßennetzes ins Mesh eingeebnet wird, `0`–`5` |
| `road_banking_limit` | `0.5` | Wie stark eine Straße quergeneigt sein muss, damit sie überhaupt eingeebnet wird, in Metern — gemessen als Höhenunterschied zwischen einem Punkt auf der Straßenmitte und dem nächstgelegenen Punkt am Straßenrand |
| `lane_width` | `4.0` | Breite in Metern, mit der das Straßennetz für die Einebnung gepuffert wird |

Die Stufen von `road_level` bauen aufeinander auf:

- `0` — nichts
- `1` — Autobahnen, Trunk-, Primary- und Secondary-Straßen, Bahntrassen
- `2` — zusätzlich Tertiary-Straßen
- `3` — zusätzlich Residential und Unclassified
- `4` — zusätzlich Service Roads
- `5` — zusätzlich Tracks

Beim Wechsel zwischen den Stufen `2` und `5` muss die zwischengespeicherte `small_roads.osm` verworfen werden, sonst wird der zuvor gespeicherte Straßenbestand weiterverwendet.

**Terrain-Darstellung**

| Parameter | Vorgabe | Beschreibung |
|---|---|---|
| `terrain_casts_shadows` | `True` | Nur wirksam, wenn Szenerie-Schatten in den Grafikeinstellungen von X-Plane aktiviert sind. Terrain empfängt Schatten auch dann, wenn es keine wirft |
| `use_decal_on_terrain` | `False` | Legt die Decal-Direktive `maquify_1_green_key.dcl` auf alle Nicht-Wasser-Terrains. Wirkt der Unschärfe der Orthofotos in sehr niedriger Höhe entgegen, kann in größerer Höhe leicht stören |
| `normal_map_strength` | `1.0` | Orthofotos enthalten die Schattierung bereits eingebrannt; der Parameter dämpft die Normalen im DSF, um Überschattung entgegenzuwirken. Er wirkt sich zugleich darauf aus, wie X-Plane Szenerie-Schatten berechnet |
| `overlay_lod` | `25000` | Entfernung, bis zu der Overlay-Bilddaten (Orthofotos über Wasser) gezeichnet werden. Niedrigere Werte helfen Bildrate und VRAM; IFR-Flüge brauchen höhere Werte als VFR |

**Hochauflösende Flughafenabdeckung**

| Parameter | Vorgabe | Beschreibung |
|---|---|---|
| `cover_airports_with_highres` | `False` | `ICAO` deckt Flughäfen mit ICAO-Code in höherer Zoomstufe ab, `Existing` übernimmt die bereits in der Kachel vorhandenen Flughafenzonen |
| `cover_zl` | `18` | Zoomstufe innerhalb der hochauflösenden Zone |
| `cover_extent` | `1.0` | Wie weit die hochauflösende Zone über die Flugplatzgrenze hinausreicht, in km. Die Zone ist ein Rechteck um die Bounding-Box des Flugplatzes, nach außen auf ganze Texturen bei `cover_zl` aufgerundet |

`cover_extent` ist der wesentliche Hebel auf die Paketgröße. Es ist ein Rand, kein Radius: Ortho4XP nimmt die Bounding-Box der Flugplatzfläche, erweitert sie auf allen Seiten um diesen Abstand und rundet das Ergebnis nach außen auf ganze Texturen bei `cover_zl` auf. Wie viel Zusatzfläche dabei entsteht, hängt daher von Größe und Zuschnitt des Flugplatzes ab — ein großer Verkehrsflughafen wächst weit stärker als eine einzelne Piste. Der Wert bestimmt zugleich, wie oft die Szenerie zwischen Basistextur und Flughafentextur die Zoomstufe wechselt.

**Masken und Wasser**

| Parameter | Vorgabe | Beschreibung |
|---|---|---|
| `mask_zl` | `14` | Zoomstufe der Küsten-Transparenzmasken. Zulässig sind ausschließlich `14`, `15` und `16` |
| `masks_width` | `100` | Maximale Ausdehnung der Masken senkrecht zur Küstenlinie, in Metern. Im Modus `rocks` wirkt effektiv die Hälfte davon. In älteren Versionen wurde sie in ZL14-Pixeln gezählt, das entspricht etwa Faktor 10 |
| `masking_mode` | `sand` | Algorithmus für den Alpha-Übergang an der Küste — `sand`, `rocks` oder `3steps` |
| `use_masks_for_inland` | `False` | Verwendet Masken auch für Binnengewässer statt der konstanten `ratio_water`-Transparenz. VRAM-intensiv und laut Hinweis im Quellcode den Aufwand vermutlich nicht wert |
| `imprint_masks_to_dds` | `False` | Brennt die Masken in die DDS-Texturen ein. Verdoppelt die Dateigröße maskierter Texturen (DXT5 statt DXT1), senkt aber den VRAM-Bedarf — eine Abwägung, kein eindeutiger Gewinn. Das Original von Oscar Pilote steht hier auf `True` |
| `sea_smoothing_mode` | `zero` | Behandlung der Meereshöhe — siehe unten |
| `water_smoothing` | `10` | Anzahl der Glättungsdurchläufe über Binnengewässer-Dreiecke |
| `ratio_water` | `0.25` | Transparenz der Ortho-Überlagerung über Binnengewässern, `0`–`1`. Bei `0` ist das Orthofoto vollständig deckend |
| `ratio_bathy` | `1.0` | Multiplikator für die Bathymetrie an ufernahen Stützpunkten, Bereich `0`–`1`. Skaliert die modellierte Wassertiefe — keine Transparenz. Wirkt nur bei `distance_masks_too=True`, und das Ergebnis wird nach unten auf `0.1` begrenzt |
| `min_area` | `0.001` | Mindestgröße eines noch modellierten Gewässers, in km². Zusammenhängende Wasserflächen werden **vor** der Flächenberechnung zusammengefasst |
| `max_area` | `200.0` | Gewässer oberhalb dieser Größe werden wie Meer maskiert, in km² |
| `sea_texture_blur` | `0.0` | Weichzeichnungsradius in Metern für Layer vom Typ `mask` in kombinierten Anbieter-Bilddaten, um zu präsente Wellen- und Reflexionsmuster abzumildern |
| `water_tech` | `XP11 + bathy` | Generation der Wasserdarstellung — unter X-Plane 12 auf `XP12` setzen, siehe Hinweiskasten unten |

Binnengewässer werden als untere Lage X-Plane-Wasser mit einer darüberliegenden Ortho-Überlagerung konstanter Transparenz gezeichnet; `ratio_water` steuert diese Transparenz. `masking_mode=3steps` macht aus dem Küstenübergang einen gestuften Übergang und erwartet `masks_width` als Liste `[a,b,c]` in Metern: `a` ist ein erster Übergang von vollständig deckenden Bilddaten an der Uferlinie zur `ratio_water`-Transparenz, `b` eine Zone, die diese Transparenz hält, und `c` die abschließende Ausblendung.

Die Werte von `sea_smoothing_mode` unterscheiden sich deutlich:

- `zero` — alle Knoten von Meeresdreiecken werden auf Höhe 0 gezwungen
- `mean` — jedes Dreieck wird einzeln auf seine eigene Mittelhöhe gesetzt
- `none` — positive Höhen bleiben erhalten, nur negative werden auf 0 gezogen. Geeignet ab einer DEM-Auflösung von 10 m und feiner, vermeidet die unrealistischen Steilkanten, die die anderen Modi erzeugen können

**Höhendaten**

| Parameter | Vorgabe | Beschreibung |
|---|---|---|
| `custom_dem` | `""` | Pfad zu einem externen Höhenraster, das die Standarddaten von viewfinderpanoramas.org ersetzt |
| `fill_nodata` | `True` | Füllt No-Data-Werte per Nearest Neighbour. Ist die Option aus, werden sie zu 0. Ein Raster mit zu vielen No-Data-Werten wird auch bei eingeschalteter Option genullt |

`custom_dem` macht den Unterschied zwischen einem Build mit hochwertigen, LiDAR-basierten Höhendaten und einem Standard-Build aus. Das Raster muss in EPSG:4326 vorliegen (EPSG:4269 wird ebenfalls akzeptiert) und muss nicht mit der Kachelgrenze übereinstimmen — außerhalb seiner Ausdehnung wird die Höhenabfrage auf den nächstliegenden Randwert geklemmt, nicht auf null, was den Einsatz für hochauflösende Daten über einzelnen Inseln ermöglicht. `.hgt`-Dateien werden direkt gelesen, jedes andere Rasterformat benötigt GDAL. `fill_nodata` abzuschalten ist die passende Einstellung für Raster ohne Meeresabdeckung oder für unvollständige LiDAR-Datensätze. Die Datensätze sind regionsspezifisch und müssen gesondert beschafft werden — siehe [Integration von LiDAR-Daten](#integration-von-lidar-daten) weiter unten.

!!! warning "Unter X-Plane 12 `water_tech=XP12` setzen"

    Die Vorgabe von `water_tech` lautet `XP11 + bathy`. Eine mit der Vorgabe gebaute Kachel stellt Wasser so dar, wie X-Plane 11 es tat, auch wenn sie in X-Plane 12 geladen wird — der Unterschied zeigt sich in Spiegelungen, Wellenbewegung und im Übergang an der Uferlinie. Für X-Plane 12 muss der Wert ausdrücklich gesetzt werden:

    ```ini
    water_tech=XP12
    ```

    Die Einstellung wird pro Kachel gespeichert. Vor der Änderung gebaute Kacheln behalten das alte Verhalten, bis sie neu gebaut werden oder ihre `Ortho4XP_+dd+ddd.cfg` bearbeitet wird.

**Globale Einstellungen und Einstellungen pro Kachel**

Die meisten der obigen Parameter werden in die Konfiguration jeder einzelnen Kachel geschrieben und können daher von Kachel zu Kachel abweichen. Einige wenige werden ausschließlich aus der globalen `Ortho4XP.cfg` gelesen und erscheinen nie in einer Kachel-Konfiguration.

Die wichtigste ist `skip_downloads`, die den Bilddaten-Download und damit auch die DDS-Konvertierung unterdrückt. Sie steht vorgabemäßig auf `False`, und sie ist es, die aus Ortho4XP einen Erzeuger von Mesh-only-Paketen macht — siehe [Pakete für Ortho-Streaming bauen](#pakete-fur-ortho-streaming-bauen). Ebenfalls nur global, unter anderem: `verbosity`, `cleaning_level`, `max_download_slots`, `max_convert_slots`, `overpass_server_choice`, `custom_scenery_dir`, `custom_overlay_src`, `custom_overlay_src_alternate`, `check_tms_response`, `http_timeout`, `max_connect_retries`, `max_baddata_retries`, `ovl_exclude_pol` und `ovl_exclude_net`.

!!! note "Diese Parameter in OrthoForge"

    OrthoForge übernimmt die Schlüsselnamen von Ortho4XP unverändert und ergänzt lediglich weitere, und die eigene Konfigurationsreferenz nennt dieselben Vorgabewerte — `default_zl` `16`, `mesh_zl` `19`, `mask_zl` `14`, `cover_zl` `18`. Die obigen Tabellen gelten also unmittelbar.

    Ein Wert weicht ab, und zwar der unter X-Plane 12 entscheidende: `water_tech` steht vorgabemäßig auf `XP12`, und die OrthoForge-Dokumentation erklärt `XP11 + bathy` für nicht mehr unterstützt. Den Hinweiskasten zu `water_tech` weiter oben können OrthoForge-Nutzer also übergehen.

    Die mitgelieferte `OrthoForge.cfg.example` ist nicht die Vorgabe. Sie ist ein Preset mit deutlich aggressiveren Werten (darunter `min_angle=0.5`, `limit_tris=50`, `cover_extent=5.0`) und wird nicht automatisch gelesen — ohne globale Konfigurationsdatei greifen die oben genannten Vorgabewerte.

### Empfohlene Einstellungen

Die folgenden Profile sind vollständige Konfigurationsabschnitte und lassen sich unverändert in `Ortho4XP.cfg` einfügen. Alle setzen durchgängig `water_tech=XP12`, da die gesamte Seite von X-Plane 12 ausgeht.

#### Standard (ausgewogen)

```ini
default_zl=16
default_website=BI
mesh_zl=19
min_angle=10.0
curvature_tol=2.0
mask_zl=14
masking_mode=sand
masks_width=100
cover_airports_with_highres=ICAO
cover_zl=18
cover_extent=1.0
min_area=0.001
apt_smoothing_pix=8
road_level=1
water_tech=XP12
```

Das ist der Vorgabesatz mit eingeschalteter hochauflösender Flughafenabdeckung. `mesh_zl=19` lässt genug Spielraum, damit `cover_zl=18` nicht gedeckelt wird, und `cover_extent=1.0` hält die hochauflösende Zone auf dem Flughafen selbst statt auf seinem Umland.

#### Hochauflösend

```ini
default_zl=17
default_website=BI
mesh_zl=19
min_angle=15.0
curvature_tol=1.0
mask_zl=16
masking_mode=rocks
masks_width=25
cover_airports_with_highres=ICAO
cover_zl=19
cover_extent=3.0
min_area=0.0005
apt_smoothing_pix=4
road_level=3
water_tech=XP12
```

Jeder Wert bewegt sich in Richtung mehr Detail. `curvature_tol=1.0` halbiert die Toleranz und lässt das Mesh entsprechend feinerem Gelände folgen, `min_angle=15.0` hält die zusätzlichen Dreiecke gut geformt. `mask_zl=16` ist die feinste zulässige Maskenauflösung, `masks_width=25` verengt den Uferübergang passend dazu, und `apt_smoothing_pix=4` zeichnet das Höhenraster über Flughäfen weniger weich, sodass deren Gelände mehr von seiner tatsächlichen Form behält.

`cover_zl=19` setzt ein `mesh_zl` von mindestens `19` voraus. Bauzeit und Paketgröße steigen steil an — bei einem hochauflösenden `custom_dem` sollte ein ausdrückliches `limit_tris` hinzukommen, damit die Dreieckszahl begrenzt bleibt.

#### Performance-optimiert

```ini
default_zl=15
default_website=BI
mesh_zl=16
min_angle=5.0
curvature_tol=3.0
mask_zl=14
masking_mode=sand
masks_width=100
cover_airports_with_highres=ICAO
cover_zl=16
cover_extent=0.5
min_area=0.1
apt_smoothing_pix=16
road_level=1
water_tech=XP12
```

`curvature_tol=3.0` und `min_angle=5.0` senken beide die Dreieckszahl, und `mesh_zl=16` ist der niedrigste zulässige Wert, der damit zugleich die nutzbare Zoomstufe der Bilddaten deckelt. `min_area=0.1` nimmt kleine Teiche aus dem Wassermodell — das Hundertfache der Vorgabe, was einen großen Teil der Wassergeometrie und ihrer Masken entfernt. `cover_zl=16` entspricht der Basis-Zoomstufe plus eins, und `cover_extent=0.5` hält die hochauflösende Zone minimal, sodass Flughäfen erkennbar bleiben, ohne viel Texturvolumen hinzuzufügen.

#### Einstellungen für Ortho-Streaming-Pakete

Für Pakete, die einem Streaming-Layer Mesh und Terrain-Definitionen liefern, statt eigene Texturen mitzubringen:

```ini
default_zl=16
default_website=BI
mesh_zl=19
min_angle=10.0
curvature_tol=2.0
water_tech=XP12
cover_airports_with_highres=ICAO
cover_zl=17
cover_extent=0.5
imprint_masks_to_dds=False
skip_downloads=True
```

`default_zl=16` als Basis hält Paketgröße und Kachelzahl beherrschbar; der Streaming-Layer erzeugt die Bilddaten zur Laufzeit ohnehin neu, eine höhere Basis-Zoomstufe bringt zur Bauzeit also nichts. `default_website=BI` ist hier nicht bloß informativ: Der Anbietercode steht in jedem Texturdateinamen, den die Terrain-Definitionen anfordern (`..._BI17.dds`), und muss deshalb zu dem passen, was der Streaming-Layer ausliefert. `water_tech=XP12` ist unter X-Plane 12 unabhängig vom Profil zwingend. `skip_downloads` ist die Einstellung, die aus einem normalen Build einen reinen Mesh- und Terrain-Build macht; sie unterdrückt die DDS-Konvertierung gleich mit — siehe [Pakete für Ortho-Streaming bauen](#pakete-fur-ortho-streaming-bauen).

## Pakete für Ortho-Streaming bauen

Beim [Ortho-Streaming](../ortho_streaming/index.md) entstehen die Bodentexturen zur Laufzeit auf Anforderung — der Streaming-Layer lädt die Bilddaten, kodiert sie nach DDS und reicht sie über ein virtuelles Dateisystem an X-Plane weiter. Ein Paket für ein solches Setup muss deshalb nur liefern, was der Streaming-Layer **nicht** erzeugt: das **Mesh** und die **Terrain-Definitionen** (die DSF-Dateien unter `Earth nav data` und das Verzeichnis `terrain`). Bilddaten-Download und DDS-Konvertierung sind in diesem Ablauf reine Verschwendung.

Eine Einstellung erledigt das:

```ini
skip_downloads=True
```

Sie steht vorgabemäßig auf `False`. Bleibt sie so, lädt und konvertiert ein Paket-Build Gigabytes an Bilddaten, die der Streaming-Layer zur Laufzeit ersetzt und die anschließend verworfen werden — Stunden an Rechenzeit und Plattenplatz für nichts.

`skip_downloads` unterdrückt **beide** Schritte, nicht nur den Download: In der Bauschleife steckt die Konvertierungsstufe innerhalb der Download-Stufe, ohne Download gibt es also nichts zu konvertieren. Es gibt eine zweite Einstellung, `skip_converts`, und zu ihr greift man leicht versehentlich — allein gesetzt lädt sie weiterhin die vollständigen Bilddaten herunter und überspringt nur die Umwandlung von JPEG nach DDS. Das ist das Gegenteil dessen, was ein Streaming-Paket braucht. Beide zu setzen schadet nicht, aber `skip_downloads` ist der wirksame Schalter.

Eine dritte Einstellung gehört in dieselbe Gruppe:

```ini
imprint_masks_to_dds=False
```

Das ist bereits die Vorgabe, aber es ausdrücklich festzuhalten lohnt sich: Wassermasken in DDS-Dateien einzubrennen ist sinnlos, wenn die DDS-Dateien anderswo entstehen. Wurde die Einstellung in einer früher genutzten Konfiguration für einen herkömmlichen Build auf `True` gesetzt, ist sie zurückzusetzen.

!!! warning "Diese beiden sind globale Einstellungen, keine Einstellungen pro Kachel"

    `skip_downloads` und `skip_converts` existieren nur in der globalen `Ortho4XP.cfg`. Sie werden **nicht** in die erzeugten Kachel-Konfigurationen `Tiles/zOrtho4XP_+dd+ddd/Ortho4XP_+dd+ddd.cfg` geschrieben und lassen sich dort nicht überschreiben. Sie in einer Kachel-Konfiguration zu suchen und nicht zu finden bedeutet nicht, dass sie unwirksam wären — die globale Konfiguration prüfen.

Die meisten übrigen Build-Parameter, darunter `default_zl`, `cover_zl`, `cover_extent`, `mask_zl`, `masking_mode` und `water_tech`, gelten *sehr wohl* pro Kachel und werden in deren Konfiguration festgehalten. Das macht eine fertige Kachel aus ihrem eigenen Verzeichnis heraus reproduzierbar.

### Welche Parameter weiterhin wirken

Bilddaten zu überspringen macht die Bildeinstellungen nicht bedeutungslos — es macht sie verbindlich. `default_zl`, `cover_zl` und `default_website` sind fest in die Terrain-Definitionen eingebrannt, die der Build erzeugt, und diese Definitionen sind der Vertrag zwischen Paket und Streaming-Layer.

Eine `.ter`-Datei aus einer mit `skip_downloads=True` gebauten Kachel — hier eine mit `default_zl=17` und `cover_zl=18` gebaute, nicht mit den Profilwerten oben — sieht so aus:

```
A
800
TERRAIN

LOAD_CENTER 0.15381 32.71729 4891 4096
BASE_TEX_NOWRAP ../textures/65472_77440_BI17.dds
LOAD_CENTER_BORDER 0.15381 32.71729 4891 2048
BORDER_TEX ../textures/65472_77440_ZL17.png
DECAL_LIB lib/g10/decals/maquify_2_green_key.dcl
WET
NO_SHADOW
```

Der Pfad hinter `BASE_TEX_NOWRAP` benennt genau die DDS-Datei, die der Streaming-Layer zur Laufzeit liefern muss — Anbietercode und Zoomstufe sind Teil des Dateinamens (`_BI17.dds`). Das Paket schlägt keine Auflösung vor, es fordert je Terrain-Definition eine bestimmte Datei.

Deshalb ist die Wahl der Zoomstufe auch in einem Build ohne Bilddaten nicht beliebig, und deshalb muss `default_website` zu dem passen, was der Streaming-Layer tatsächlich ausliefert. Ein mit `BI` gebautes Paket fragt nach `_BI17.dds`, und ein auf einen anderen Anbieter eingestellter Layer beantwortet diesen Namen nicht.

Dieselbe Kachel zeigt, was `cover_zl` mit diesem Vertrag macht. Von ihren 752 `.ter`-Dateien verweisen 559 auf `_BI17` und 193 auf `_BI18` — die Basis-Zoomstufe über den größten Teil der Kachel, die höhere Cover-Zoomstufe auf das Flughafenumfeld beschränkt. Das sind Zahlen aus einer einzelnen beobachteten Kachel, eine Veranschaulichung des Mechanismus und kein Zielverhältnis — die Aufteilung hängt vollständig von `cover_extent` ab und davon, wie viele Flughäfen die Kachel enthält.

Ihr Verzeichnis `textures/` enthält 118 Dateien gegenüber diesen 752 Terrain-Definitionen — und keine einzige davon ist eine DDS. Es sind die PNG-Küstenmasken, passend zu genau 118 `BORDER_TEX`-Verweisen. Das ist das Bild eines Mesh-only-Builds: Terrain-Definitionen und Masken vollständig, Bilddaten gar nicht vorhanden.

Die Mesh-Parameter (`mesh_zl`, `min_angle`, `curvature_tol`, `limit_tris`) und die Masken-Parameter (`mask_zl`, `masks_width`, `masking_mode`) behalten ihre volle Wirkung, denn Mesh und Masken sind genau das, was das Paket enthält.

### Beobachtete Werte aus Produktiv-Konfigurationen

Das obige Streaming-Profil ist ein konservativer Ausgangspunkt. Tatsächlich im Einsatz befindliche Konfigurationen mit einem Streaming-Layer liegen stellenweise deutlich davon entfernt — die folgenden Werte stammen aus einem laufenden XEarthLayer-Setup:

| Parameter | Streaming-Profil | Beobachtet im Produktivbetrieb |
|---|---|---|
| `cover_extent` | `0.5` | `6.0` |
| `cover_zl` | `17` | `18` |
| `mask_zl` | `14` (Vorgabe) | `16` |
| `masking_mode` | `sand` (Vorgabe) | `rocks` |
| `ratio_water` | `0.25` (Vorgabe) | `0.5` |
| `road_level` | `1` (Vorgabe) | `3` |
| `masks_width` | `100` (Vorgabe) | `25` |

Die größte Spanne liegt bei `cover_extent`, dem Rand in Kilometern, der um die Bounding-Box des Flughafens gelegt wird. Zwischen `0.5` und `6.0` km wächst der Rand um das Zwölffache; wie viel Fläche das hinzufügt, hängt von Größe und Zuschnitt des Flugplatzes ab, ist aber in jedem Fall ein Vielfaches. Das macht ihn zum stärksten Einzelhebel auf die Paketgröße, auf die Zahl der hochauflösenden Texturanforderungen in einem belebten Nahverkehrsbereich und darauf, wie oft die Szenerie zwischen Basistextur und Flughafentextur die Zoomstufe wechselt.

Welches Ende dieser Spanne passt, hängt vom Setup ab: `0.5` hält Pakete klein und ist eine vernünftige Vorgabe für großflächige Abdeckung, `6.0` passt dort, wo eine Handvoll Heimatflughäfen wichtiger ist als die Gesamtpaketgröße.

Die übrigen Abweichungen folgen derselben Logik: Ein höheres `mask_zl` mit einem schmaleren `masks_width` erzeugt feinere, aber engere Küstenlinien, und `masking_mode=rocks` macht den Uferübergang abrupter als die Vorgabe `sand`. `road_level=3` weitet die Mesh-Einebnung vom Hauptstraßennetz auf Residential- und Unclassified-Straßen aus — Secondary-Straßen sind schon in der Vorgabe `1` enthalten — was mehr Vektordaten pro Kachel kostet.

Es handelt sich um Konfigurationswerte aus der Praxis, nicht um Messergebnisse. Für diesen Vergleich wurden weder Paketgrößen noch Bildraten gemessen, die beschriebenen Wirkungen geben also eine Richtung an, keine Größenordnung.

`cover_zl=17` auf einer Basis von `default_zl=16` hält die hochauflösende Zone eine Stufe über der Basis statt zwei, sodass die Szenerie weniger und sanftere Skalenwechsel enthält. Das ist ein Argument über Paketgröße und Einheitlichkeit. Ein Mittel gegen Bildfehler ist es nicht: Woher die im Einzelfall kommen, ist damit nicht gesagt, und weder die Ortho4XP- noch die X-Plane-Dokumentation stützt Zoomstufen-Mischung als allgemeine Ursache. Diese Werte zu ändern verschiebt, wo Skalenwechsel liegen; das als Fehlerbehebung zu verkaufen wäre geraten.

### Wohin das Paket gehört

Wie die fertigen Kacheln neben einem Streaming-Mount abgelegt werden und in welcher Reihenfolge sie in `scenery_packs.ini` erscheinen müssen, ist gesondert beschrieben:

- [Statisch + Streaming](../ortho_streaming/static_plus_streaming.md) — Mesh-only-Kacheln in einem Verzeichnis zusammenführen und die Ladereihenfolge setzen
- [XEarthLayer](../ortho_streaming/xearthlayer.md) — die regionalen DSF/TER-Pakete, die dieser Bauvorgang erzeugt, und ihre Installation
- [Wie Ortho-Streaming funktioniert](../ortho_streaming/how_streaming_works.md) — was der Streaming-Layer zur Laufzeit beisteuert

## Integration von LiDAR-Daten

Ortho4XP unterstützt die Integration von hochauflösenden LiDAR-Daten für eine verbesserte Geländedarstellung. Diese Daten sind besonders für Gebiete mit komplexer Topographie wie die Alpen oder andere Bergregionen nützlich.

### Verfügbare LiDAR-Daten

Die LiDAR-basierten Geländemodelle von [sonny.4lima.de](https://sonny.4lima.de) decken Europa mit höherer Auflösung und Genauigkeit ab als die Standard-Höhendaten. Diese Daten können in Ortho4XP auf zwei Arten integriert werden:

**Methode 1: Einzelne Kacheln**

- Die LiDAR-Daten als `custom_dem` in Ortho4XP verwenden
- Diese Methode eignet sich für einzelne Kacheln oder kleine Bereiche
- Die LiDAR-Daten werden nur für spezifische Kacheln verwendet

**Methode 2: Größere Bereiche**

- Die DEM-Dateien im Ortho4XP-Verzeichnis ersetzen
- Diese Methode eignet sich für größere Regionen
- Ortho4XP verwendet die LiDAR-Daten automatisch für alle Kacheln in der Region

### Schritte zur Integration

1. Die gewünschten LiDAR-Daten von [sonny.4lima.de](https://sonny.4lima.de) herunterladen
2. Für Methode 2 gibt es zwei Möglichkeiten:

    - Die Dateien in das Ortho4XP-Verzeichnis entpacken und die Kacheln entsprechend in die Verzeichnisse unter `Elevation_data` sortieren
    - Oder mit Links unter `Elevation_data` arbeiten:
        - Zuerst das alte `Elevation_data` sichern
        - Neues `Elevation_data` anlegen und darin die Verzeichnisse `+00-060` usw. als Links auf ein extra Verzeichnis (z.B. `GlobalElevationData`) anlegen. Folgendes Skript erstellt im neuen leeren `Elevation_data` alle nötigen Verzeichnisse als Links auf das Verzeichnis `../GlobalElevationData`:

        ```bash
        #!/bin/bash

        # Zielpfad für symbolische Links
        TARGET_PATH="../GlobalElevationData"

        # Zielverzeichnis erstellen, falls nicht vorhanden
        mkdir -p "$TARGET_PATH"

        # Funktion zum Erstellen eines Linknamens
        create_link_name() {
            local lat=$1
            local lon=$2
            # Breitengrad formatieren (+XX oder -XX)
            if [ $lat -ge 0 ]; then
                lat_str=$(printf "+%02d" $lat)
            else
                lat_str=$(printf "%03d" $lat)
            fi
            # Längengrad formatieren (+YYY oder -YYY)
            if [ $lon -ge 0 ]; then
                lon_str=$(printf "+%03d" $lon)
            else
                lon_str=$(printf "%04d" $lon)
            fi
            echo "${lat_str}${lon_str}"
        }

        # Alle möglichen Links generieren
        for lat in $(seq -90 10 80); do    # Breitengrade: -90° bis +80° in 10°-Schritten
            for lon in $(seq -180 10 170); do # Längengrade: -180° bis +170° in 10°-Schritten
                link_name=$(create_link_name $lat $lon)
                ln -s "$TARGET_PATH" "./$link_name"
            done
        done
        ```

        - Dann in das `GlobalElevationData`-Verzeichnis alle HGT-Dateien kopieren

3. Die gewünschte Integrationsmethode wählen (Methode 1 oder 2)
4. Die Kacheln wie gewohnt generieren

Die verbesserte Geländedarstellung wird automatisch in den generierten Kacheln übernommen.

### Vorgefertigte OSM- und DEM-Daten

Das OrthoForge-Projekt betreibt zwei begleitende Dienste, die unabhängig davon nützlich sind, welches Bauwerkzeug zum Einsatz kommt. Beide sind kostenfrei und erfordern kein Konto.

**Vorgefertigte OpenStreetMap-Kacheln**

- Fertige OSM-Vektorlayer (Flughäfen, Straßen, Küstenlinie, Gewässer) im Cache-Format von Ortho4XP, mit maximalem Straßendetail, sodass sie sich lokal weiter herunterfiltern lassen
- Die Abdeckung ist unvollständig und wächst mit der Zeit, Europa zuerst; Kacheln außerhalb des vorgefertigten Bereichs fallen auf eine gewöhnliche Overpass-Abfrage zurück
- Ausgeliefert als bzip2-komprimiertes OSM-XML unter `OSM_data/<block>/<tile>/`. Für Ortho4XP werden die Dateien unverändert nach `OSM_data` gelegt — nicht umbenannt, nicht entpackt — und das Bauwerkzeug greift darauf zu, statt Overpass aufzurufen
- Die Daten bleiben © OpenStreetMap-Mitwirkende, ODbL
- [Vorgefertigte OSM-Kacheln](https://xpconnect.me/orthoforge-data.html)

**Sonny-DTM-Spiegel**

Dieselbe Seite betreibt einen Spiegel der Höhendaten von Sonny, angeboten als übliche `.hgt`-Kacheln im SRTM-Stil in 3″ und 1″, dazu 0,5″-Kacheln — Sonnys eigene für die Alpen, wo er diese Auflösung für Österreich und die Schweiz veröffentlicht, und eigene Aufbereitungen von OrthoForge für Teile der Vereinigten Staaten. Ortho4XP verwendet sie genau wie die Originale: nach `Elevation_data` entpacken, wie oben beschrieben. OrthoForge kann über `custom_dem_search_dirs` darauf verweisen.

Die 0,5″-US-Kacheln stammen nicht von Sonny — sie sind aus USGS 3DEP neu erzeugt und tragen entsprechend diese Zuschreibung.

Für Sonnys eigene Daten ist [sonny.4lima.de](https://sonny.4lima.de) die maßgebliche Quelle mit der vollständigen europäischen Abdeckung und den aktuellen Aktualisierungen; der [Spiegel](https://xpconnect.me/sonny.html) führt davon eine Teilmenge als Bequemlichkeitskopie. Ausnahme sind die 0,5″-US-Kacheln — die gibt es nur auf dem Spiegel. Sonnys Daten stehen an beiden Orten unter CC BY 4.0 und werden Sonny zugeschrieben.

## Ortho Patches für Szenerien

Seit X-Plane 10.50 folgen Pisten immer der Geländekontur, und das Einebnen wird stattdessen je Flugplatz angefordert: Die `apt.dat`-Metadatenzeile `1302 flatten 1` kennzeichnet einen Flugplatz als einzuebnen. Laminar beschreibt die Wirkung als hartes Einebnen, das den Flugplatz und einen Rand des umliegenden Geländes erfasst und dessen Topografie zerstört. Viele Szenerien — sowohl Standard- als auch Drittanbieter-Szenerien — tragen das Flag, weil sie für eine ebene Fläche gebaut wurden. Das steht im Widerspruch zu dem Ziel, mit Ortho4XP ein möglichst genaues und realistisches Bodenmesh zu erzeugen.

Für einige Szenerien existieren spezielle Ortho Patches, die entweder vom Hersteller selbst oder von aktiven X-Plane-Nutzern bereitgestellt werden. Mithilfe dieser Patches kann das Mesh-Modell mit Ortho4XP gezielt an die jeweilige Szenerie angepasst werden. Zudem erlauben Modifikationen an der Szenerie, auf das Setzen von `1302 flatten 1` zu verzichten und dennoch eine korrekte Darstellung zu erreichen.

Der umgekehrte Fall ist ebenfalls wissenswert. Seit X-Plane 11 gibt es die frühere Rendering-Option, Pisten der Geländekontur folgen zu lassen, nicht mehr — sie folgen ihr immer. Auf einem sehr detaillierten Ortho4XP-Mesh kann ein Flugplatz dadurch eine sichtbar unebene Oberfläche bekommen. Dann ist das *Setzen* von `1302 flatten 1` die Lösung, nicht das Entfernen: genau dafür wurde das Flag je Flugplatz eingeführt.

## Wichtige Hinweise und Fehlerbehebung

### Allgemeine Hinweise

- Ortho4XP benötigt viel Speicherplatz für die generierten Texturen
- Die Qualität der Orthofotos hängt von der gewählten Bildquelle ab
- Die Verarbeitung kann je nach Gebietsgröße und Zoomstufe mehrere Stunden dauern
- Der shred86-Fork ergänzt Funktionen gegenüber dem Original — die Liste steht in dessen Wiki
- Die Verwendung der Binaries vereinfacht die Installation erheblich

### Performance-Optimierung

- Die Verarbeitungszeit hängt stark von der gewählten Zoomstufe und der Gebietsgröße ab
- Zu hohe Zoomstufen können das System überlasten
- `skip_downloads` und `skip_converts` sind nützlich für die Wiederverarbeitung einzelner Schritte und die Grundlage von Mesh-only-Builds
- Die Kachelerzeugung ist I/O-lastig: Sie schreibt sehr viele Texturdateien und liest durchgehend Höhen- und Vektordaten

### Optimierung der Dateigröße

Da Ortho4XP große Mengen an Texturen generiert, kann der Speicherplatzbedarf schnell ansteigen. ImageMagick verkleinert die fertigen DDS-Texturen an Ort und Stelle:

```bash
mogrify -resize 2048x2048 *.dds
```

Eine Halbierung der Kantenlänge viertelt die Dateigröße, und 2048x2048 ist ein vernünftiger Kompromiss zwischen Bildqualität und Speicherplatzbedarf. Kompressionsformat und Alphakanal überstehen den Vorgang — eine DXT1-Textur bleibt DXT1, eine maskierte DXT5-Textur behält ihr Alpha — und ImageMagick erzeugt die vollständige Mipmap-Kette für die neue Größe neu.

Wichtiger als die Mipmaps ist allerdings ein anderer Haken. Ortho4XP schreibt die Texturgröße in jede `.ter`-Datei als festen Wert `4096`:

```
LOAD_CENTER 0.15381 32.71729 4891 4096
```

Das Verkleinern der DDS-Dateien rührt die `.ter`-Dateien nicht an, danach behauptet also jede Terrain-Definition eine Auflösung, die die Textur nicht mehr hat. X-Plane nutzt diese Zahl für die entfernungsabhängige Auflösungsverwaltung — das Verkleinern ist deshalb nur unbedenklich, wenn die `.ter`-Dateien mitgezogen werden oder die Abweichung bewusst in Kauf genommen wird.

Wer die Mipmap-Kette einer Datei prüfen will: `magick identify -verbose` gibt sie gar nicht aus, die Anzahl steht im DDS-Header ab Byte-Offset 28.

Für noch nicht gebaute Kacheln ist der sauberere Weg, `default_zl` um eine Stufe zu senken, statt hinterher zu skalieren. Das ergibt kleinere Texturen mit passenden Terrain-Definitionen.

### Fehlerbehebung

Bei Problemen:

1. Die Log-Dateien im Ortho4XP-Verzeichnis überprüfen
2. Sicherstellen, dass alle Python-Abhängigkeiten installiert sind
3. Die [Dokumentation des shred86-Forks](https://github.com/shred86/Ortho4XP/wiki) konsultieren
4. Das [X-Plane Forum](https://forums.x-plane.org/forums/forum/322-ortho4xp/) besuchen

---

## Weiterführende Kapitel

| Thema | Seite | Schwerpunkt |
|---|---|---|
| AutoOrtho | [AutoOrtho](../ortho_streaming/autoortho.md) | Streaming-Alternative zur statischen Generierung |
| XEarthLayer | [XEarthLayer](../ortho_streaming/xearthlayer.md) | Rust-basierte Streaming-Alternative |
| XPME | [XPME](../ortho_streaming/xpme.md) | Closed-Source-Freemium-Streaming, Konflikt mit Ortho4XP-Kacheln |
| Funktionsweise Streaming | [Wie Ortho-Streaming funktioniert](../ortho_streaming/how_streaming_works.md) | Was der Streaming-Layer zur Laufzeit beisteuert |
| Statisch + Streaming | [Statisch + Streaming](../ortho_streaming/static_plus_streaming.md) | Kombination von Ortho4XP mit Streaming-Lösungen |
| Szenerie-Komponenten | [Wie X-Plane die Welt aufbaut](../aufbau_quellen/scenery_components.md) | scenery_packs.ini-Ladereihenfolge |
| Orthofotografie | [Konzepte & Methoden](orthophotography_intro.md) | Überblick statische und Streaming-Ansätze |
| Dateisystem | [Dateisystem](../../linux/optimizations/filesystem.md) | SSD-Performance für Kachelerzeugung und -speicherung |

---

## Quellen

- [Ortho4XP](https://github.com/oscarpilote/Ortho4XP) — Oscar Pilote, Originalprojekt
- [Ortho4XP-Fork und Wiki](https://github.com/shred86/Ortho4XP/wiki) — shred86, Installations- und Anwendungsdokumentation
- [OrthoForge](https://xpconnect.me/orthoforge.html) — xbard, eigenständig entwickelter Nachfolger
- [Vorgefertigte OSM-Kacheln](https://xpconnect.me/orthoforge-data.html) — OrthoForge-Projekt, OpenStreetMap-Vektordaten
- [Sonnys LiDAR-Geländemodelle](https://sonny.4lima.de) — Sonny, Höhendatensätze für Europa
- [Ortho4XP-Forum](https://forums.x-plane.org/forums/forum/322-ortho4xp/) — X-Plane.org, Community-Unterstützung
