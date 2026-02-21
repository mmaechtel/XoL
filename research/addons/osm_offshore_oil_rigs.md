# OSM Offshore Oil Rigs — Research Paper

**Datum:** 2026-02-21
**Status:** recherchiert
**Quellen-Zeitraum:** 2025–2026

---

## 1. Was ist OSM Offshore Oil Rigs?

OSM Offshore Oil Rigs ist ein Freeware-Szenerie-Addon für X-Plane 12, das Offshore-Ölplattformen als Heliports in Ozeanen und Meeren platziert. Die Positionsdaten stammen aus OpenStreetMap (OSM). Das Addon wurde von **Saar Snagar** (snagar.dev) entwickelt — demselben Entwickler, der auch das Mission-X-Plugin erstellt hat.

### Kerndaten

| Eigenschaft | Wert |
|---|---|
| **Entwickler** | Saar Snagar (snagar.dev) |
| **Erstveröffentlichung** | 31. August 2025 |
| **Aktuelle Version** | v1.0.1 (31. Januar 2026) |
| **Dateigröße** | 297,68 KB |
| **Downloads** | ~269 (x-plane.to, Stand Feb. 2026) + ~90 (forums.x-plane.org) |
| **Kategorie** | Scenery Enhancements / Helipads |
| **Lizenz** | Freeware |
| **Kompatibilität** | X-Plane 12 |
| **Plattformen** | Windows, macOS, Linux (plattformunabhängiges Szenerie-Format) |
| **Bewertung** | Noch keine Bewertungen (x-plane.to) |

### Distribution

Das Addon ist auf zwei Plattformen verfügbar:

- **x-plane.to:** https://x-plane.to/file/1896/osm-offshore-oil-rigs
- **forums.x-plane.org:** https://forums.x-plane.org/files/file/96552-osm-offshore-oil-rigs/

---

## 2. Technischer Aufbau

### Funktionsprinzip

Ölplattformen werden in X-Plane als **Heliports** dargestellt — sie nutzen das `apt.dat`-Dateiformat mit Row Code 17 (Heliport-Header) und Row Code 102 (Helipad-Definitionen). Jeder Heliport erhält:

- Lat/Long-Koordinaten (8 Dezimalstellen)
- Orientierung (True Heading)
- Helipad-Dimensionen (Länge/Breite in Metern)
- Oberflächentyp
- Das `apt.dat`-Format unterstützt explizit `is_oilrig` als Metadaten-Schlüssel (Row Code 1302)

Das Addon enthält **keine eigenen 3D-Modelle** — es nutzt die in X-Plane 12 eingebauten Standard-Ölplattform-Assets. Bei nur 298 KB Dateigröße besteht das Paket im Wesentlichen aus `apt.dat`-Dateien mit Heliport-Definitionen und den zugehörigen DSF-Referenzen (Digital Scenery Files), organisiert im Standard-Custom-Scenery-Ordnerformat mit `Earth nav data/`-Unterverzeichnissen.

### Datenquelle: OpenStreetMap

Die Positionsdaten der Ölplattformen werden aus OpenStreetMap extrahiert, konkret aus Einträgen mit dem Tag `man_made=offshore_platform`. Der Entwickler gibt explizit an: *"The data comes from the OSM site, which means it is not official but should be reasonably accurate."*

### Generierungs-Pipeline

Das Addon wurde per **Python-Skript** generiert — nicht manuell erstellt. Der Entwickler hat dafür ein öffentliches Repository:

- **Repository:** https://github.com/snagar/osm_to_xplane_dist
- **Sprache:** Python (98,7%)
- **Lizenz:** MIT
- **Version:** v0.09 (August 2025)

Das `osm_to_xplane_dist`-Tool ist ein allgemeinerer OSM-zu-X-Plane-Konverter, der auch für Gebäude genutzt werden kann. Die Pipeline umfasst:

1. **Daten-Extraktion** aus OpenStreetMap (Overpass API oder OSM-Exporte)
2. **Koordinaten-Konvertierung** in X-Plane-Format
3. **Filterung** gegen bestehende X-Plane-Ölplattformen (um Überlappungen zu minimieren)
4. **Generierung** von `apt.dat`-Einträgen und DSF-Dateien
5. **Alignment-Tests** für 3D-Assets und Helipads

### Scenery-Packs-Reihenfolge

Laut Installationsanleitung soll das Addon in `scenery_packs.ini` **nach** GLOBAL_AIRPORTS und anderer Custom Scenery platziert werden (= niedrigere Priorität). Das ist ungewöhnlich — normalerweise werden Custom-Airports *über* GLOBAL_AIRPORTS platziert, damit sie diese überschreiben. Bei diesem Addon ist die niedrige Priorität vermutlich beabsichtigt, damit höherwertige Flughafen-Scenery nicht von den generischen Heliport-Einträgen gestört wird.

Die Reihenfolge in `scenery_packs.ini` funktioniert generell so:

- **Oben = höchste Priorität** — wird zuerst geladen und überschreibt niedrigere Einträge
- Empfohlene Hierarchie: Custom Airports → GLOBAL_AIRPORTS → Base Mesh
- Neu installierte Scenery wird automatisch an die Spitze der Datei gesetzt
- Scenery kann durch Ändern von `SCENERY_PACK` zu `SCENERY_PACK_DISABLED` deaktiviert werden

Quelle: https://www.x-plane.com/kb/prioritization-scenery-packs/

### Bekannte Einschränkungen

1. **Überlappungen:** Der Entwickler hat versucht, bestehende X-Plane-Ölplattformen herauszufiltern, aber Überlappungen können auftreten. User werden gebeten, diese zu melden.
2. **Positionsgenauigkeit:** Trotz Alignment-Tests kann es zu leicht verschobenen Platzierungen kommen.
3. **OSM-Datenqualität:** Die Daten sind nicht offiziell und die Abdeckung variiert regional (siehe Abschnitt 3).

---

## 3. OpenStreetMap-Datenquelle im Detail

### Tagging-Standard

Offshore-Plattformen werden in OSM mit folgendem Schema getaggt:

| Tag | Bedeutung |
|---|---|
| `man_made=offshore_platform` | Haupttag — Plattform für Produktion, Bohrung, Beobachtung etc. |
| `name=*` | Plattformname |
| `operator=*` | Betreiber |
| `ref=*` | Referenz-ID |
| `aeroway=helipad` | Helikopter-Landefläche vorhanden |
| `seamark:type=platform` | Nautische Kartendarstellung |
| `seamark:platform:category=*` | Plattform-Kategorie (11 Typen, s.u.) |

### Plattform-Kategorien (seamark)

Die OSM-Seamark-Spezifikation definiert 11 Kategorien:

1. **oil** — temporäre mobile Struktur für Exploration
2. **production** — permanente Förderplattform
3. **observation** — wissenschaftliche Beobachtung
4. **alp** — Articulated Loading Platform
5. **salm** — Single Anchor Leg Mooring
6. **mooring** — Anlegeplattform
7. **artificial_island** — künstliche Insel
8. **fpso** — Floating Production, Storage and Offloading
9. **accommodation** — Wohn-/Versorgungsplattform
10. **nccb** — Navigation/Communication/Control Buoy
11. *(Basis-Kategorie)* — allgemeine Offshore-Plattform

### Verfügbare Datenfelder

Zusätzlich zu den Basis-Tags gibt es Seamark-Attribute:

- Farbe (`colour`), Farbmuster (`colour_pattern`)
- Baumaterial (`construction`), Zustand (`condition`)
- Höhe über Meeresspiegel (`height`)
- Förderprodukt (`product`)
- Radar-Sichtbarkeit (`reflectivity`), visuelle Auffälligkeit (`visibility`)

### Datenqualität und Abdeckung

Die OSM-Abdeckung für Offshore-Plattformen ist **lückenhaft**. Das OSM-Wiki selbst notiert: *"There is little tagged within the OSM database, and what there is is difficult to find."*

- **Gut abgedeckt:** Nordsee (UK, Norwegen), Golf von Mexiko — Regionen mit aktiver OSM-Community und öffentlich verfügbaren Behördendaten (z.B. BSEE für den Golf von Mexiko)
- **Schwach abgedeckt:** Persischer Golf, Südostasien, Westafrika — trotz hoher realer Plattformdichte
- **Mapping-Methode:** Nodes am Zentrum der Plattform, teilweise auch als Flächen (Areas)

Für das OSM Offshore Oil Rigs Addon bedeutet dies: Die Abdeckung hängt stark von der Region ab. In gut kartierten Gebieten (Nordsee, Golf von Mexiko) ist die Platzierung relativ vollständig, in anderen Regionen fehlen viele Plattformen.

### Quellen

- https://wiki.openstreetmap.org/wiki/Tag:man_made=offshore_platform
- https://wiki.openstreetmap.org/wiki/Seamarks/Offshore_Platforms
- https://wiki.openstreetmap.org/wiki/Oil_and_Gas_Infrastructure

---

## 4. Mission-X Integration

### Was ist Mission-X?

Mission-X ist ein X-Plane-Plugin desselben Entwicklers (Saar Snagar), das ein Framework für Flugmissionen bereitstellt. Es ist als "Schweizer Taschenmesser" für Missionsdesigner und Zufallsmissionen-Enthusiasten gedacht.

| Eigenschaft | Wert |
|---|---|
| **Entwickler** | Saar Snagar (snagar.dev) |
| **Aktuelle Version** | v26.01.5 (31. Januar 2026) |
| **Dateigröße** | 99,52 MB |
| **Lizenz** | Freeware |
| **Kompatibilität** | X-Plane 11 und 12 |
| **Sprachen** | XML-basiert + MY-BASIC-Interpreter für Scripting |
| **Quellcode** | https://github.com/snagar/mx-source-build (C 63,7%, C++ 34,2%, Apache-2.0) |
| **Distribution** | x-plane.to, forums.x-plane.org, MediaFire |
| **Website** | http://snagardev.weebly.com/plugins.html |

### Kern-Features

- **Zufallsmissionen:** Generierung von Cargo-, Medevac- und Helikopter-Missionen auf Basis von Community-Templates
- **Overpass-basierte Templates:** Nutzung von OpenStreetMap-Daten (Overpass API) für Missionsstandorte
- **ILS-Training:** Automatische Suche nach ILS-Airports in der Umgebung
- **Flugplan-Import:** LittleNavMap, SimBrief, flightplandatabase.com
- **Szenerie-Bibliotheken:** Integration mit MX Library, RescueX, 3D People, R2, OpenSceneryX, MisterX, CDB Library, RuScenery, Handy Objects
- **Scripting:** XML-basierte Missionsstruktur + eingebetteter MY-BASIC-Interpreter
- **Ölplattform-Missionen:** Ab v3.304.14 beta1 explizite Unterstützung für Oil-Rig-Missionen (X-Plane 12.05+)

### Integration mit OSM Offshore Oil Rigs

Die Verbindung zwischen beiden Addons funktioniert folgendermaßen:

1. **OSM Offshore Oil Rigs** platziert Heliports (Ölplattformen) in der X-Plane-Welt
2. **Mission-X** liest die `apt.dat`-Daten und erkennt diese Heliports als mögliche Missionsziele
3. Der User muss nach Installation des Szenerie-Addons im Mission-X Setup-Bildschirm die **"APT Data Optimization"** ausführen — damit werden die neuen Heliport-Daten indexiert und für die Missionsgenerierung verfügbar gemacht
4. Danach kann Mission-X zufällige Helikopter-Missionen zu den Ölplattformen generieren

Die APT Data Optimization ist nötig, weil Mission-X einen eigenen Index der verfügbaren Airports/Heliports pflegt und neue Custom-Scenery-Einträge nicht automatisch erkennt.

### Quellen

- https://x-plane.to/file/135/mission-x
- http://snagardev.weebly.com/plugins.html
- https://forums.x-plane.org/files/file/41874-mission-x/

---

## 5. Entwickler-Ökosystem: snagar

Saar Snagar ist ein aktiver X-Plane-Entwickler mit mehreren Projekten. Sein GitHub-Profil (https://github.com/snagar) zeigt 14 Repositories:

### Relevante Projekte

| Projekt | Beschreibung | Sprache | Letztes Update |
|---|---|---|---|
| **mx-source-build** | Mission-X Quellcode | C/C++ | Jan. 2026 |
| **mx-release** | Mission-X Release-Builds | Python | Jan. 2026 |
| **mx-random-scenery** | Random Scenery Pack für Mission-X | — | Jan. 2026 |
| **osm_to_xplane_dist** | OSM-zu-X-Plane-Konverter (für Oil Rigs) | Python | Aug. 2025 |
| **button_shifter** | Modifier-Button-Plugin für X-Plane | C | Nov. 2025 |
| **HSL-K80** | Helicopter Sling Line Plugin | C++ | Jan. 2022 |
| **imgui4xp** | ImGui-Template für X-Plane 11, inkl. Linux-Support | — | Jul. 2020 |

### Weitere Plugins (von Weebly-Seite)

- **Button Shifter:** Software-basierte Shift-State-Emulation für Joystick-Buttons
- **Coordinate Converter:** Lat/Long-Konvertierung ins X-Plane-Format + FMS-Paste-Funktion

### Kontakt

- E-Mail: snagar.dev@protonmail.com
- Website: http://snagardev.weebly.com/plugins.html
- X-Plane.to-Profil: Mitglied seit Januar 2022

---

## 6. Versionsverlauf

### v1.0.0 — 31. August 2025

- Erstveröffentlichung
- Offshore-Ölplattformen basierend auf OSM-Daten
- Heliport-Platzierungen in Ozeanen/Meeren
- Script-generierte Szenerie mit Alignment-Tests
- Filterung gegen bestehende X-Plane-Ölplattformen

### v1.0.1 — 31. Januar 2026

- Hinweis auf OSM-Daten-Cutoff integriert (laut x-plane.to: "OSM 2006 data cutoff information" — vermutlich bezogen auf den Zeitpunkt des Datenexports oder einen Metadaten-Hinweis; Details unklar)
- Erweiterte Script-Funktionalität für benutzerdefinierte Oil-Rig-Datei-Ergänzungen

---

## 7. Linux-Kompatibilität

### Plattformunabhängiges Format

Das Addon besteht ausschließlich aus plattformunabhängigen Dateien (Text-basierte `apt.dat`, DSF-Binärdateien im X-Plane-Standardformat). Es gibt **keine plattformspezifischen Binaries, Skripte oder Abhängigkeiten**. Die Installation ist auf allen drei Plattformen identisch:

1. Entpacken in den `Custom Scenery/`-Ordner
2. `scenery_packs.ini`-Reihenfolge anpassen

### Generierungs-Tool

Das `osm_to_xplane_dist`-Python-Skript, mit dem das Addon generiert wurde, unterstützt explizit Linux:

- Separate Config-Dateien: `config_lin.json` und `config_win.json`
- Build-Skripte: `proj_build.sh` (Linux) und `proj_build.bat` (Windows)
- Getestet mit Python 3.9–3.12
- Benötigt Blender 3.6x oder 4.2.x

### Mission-X auf Linux

Der Quellcode von Mission-X (mx-source-build) wird mit CMake gebaut und ist in C/C++ geschrieben. Das imgui4xp-Template zeigt explizit Linux-Support. Die Release-Builds auf x-plane.to umfassen Linux-Binaries (.so-Dateien).

---

## 8. Vergleich: Offshore-Ölplattform-Addons für X-Plane

### Übersicht

| Addon | Typ | Abdeckung | Preis | XP12 | Datenquelle |
|---|---|---|---|---|---|
| **OSM Offshore Oil Rigs** (snagar) | Heliports | Weltweit (OSM-Abdeckung) | Frei | Ja | OpenStreetMap |
| **X-OilRigs Vol 1/2** (Skytitude) | 3D-Modell-Ersatz | Weltweit (ersetzt Default) | $16,90 | XP11 (XP12 unklar) | Default-Positionen |
| **Gulf of Mexico Oil Rigs** (JoshM) | Heliports | Golf von Mexiko | Frei | Unklar | BSEE-Datenbank |
| **WW Oil Rigs - Gulf of Mexico** (Bristow-Stagg) | Heliports | Golf von Mexiko | Frei | Unklar (XP10/11) | BSEE-Daten |
| **UK Oil Fields** | Heliports | Nordsee (UK) | Frei | Unklar | ? |
| **X-Plane Default** | Dynamische Objekte | Verstreut | Inkl. | Ja (eingeschränkt) | Laminar Research |

### Detailvergleich

**OSM Offshore Oil Rigs vs. regionale Addons (JoshM, WW Oil Rigs, UK Oil Fields):**

- OSM Offshore Oil Rigs ist das einzige Addon mit **weltweiter Abdeckung** — alle anderen decken nur einzelne Regionen ab
- Die regionalen Addons nutzen oft präzisere Datenquellen (z.B. BSEE für den Golf von Mexiko mit Rig-Betreiber, Typ, Manned/Unmanned-Status)
- JoshMs Paket enthält PDFs mit Koordinaten, Betreibern und Sektordaten — deutlich mehr Metadaten als das OSM-Addon
- Die regionalen Addons sind älter (2019–2023) und möglicherweise nicht XP12-kompatibel

**OSM Offshore Oil Rigs vs. Skytitude X-OilRigs:**

- Grundlegend verschiedene Ansätze: Skytitude **ersetzt die visuellen Modelle** der Default-Rigs mit hochauflösenden PBR-Varianten; OSM Offshore Oil Rigs **fügt neue Positionen hinzu**
- Theoretisch komplementär nutzbar: Skytitude für bessere Optik, OSM für mehr Positionen
- Skytitude ist Payware ($16,90), OSM ist Freeware

**X-Plane Default Oil Rigs:**

- X-Plane 12 enthält Standard-Ölplattformen als Teil der Szenerie
- Die dynamisch platzierten Ölplattformen aus X-Plane 11 wurden in XP12 möglicherweise entfernt oder reduziert
- Die eingebauten Modelle sind funktional, aber visuell einfach
- Das OSM-Addon nutzt genau diese Default-Modelle, platziert sie aber an OSM-basierten Koordinaten

### Alleinstellungsmerkmal

OSM Offshore Oil Rigs ist das einzige X-Plane-Addon, das:

1. **OSM-Daten** als Positionsquelle nutzt
2. **Weltweite Abdeckung** bietet (statt nur einzelne Regionen)
3. **Mission-X-Integration** mitbringt (selber Entwickler)
4. Durch ein **öffentliches Python-Tool** generiert wurde, das andere nachnutzen könnten

---

## 9. Konflikte und Interaktion mit Default-Szenerie

### Überlappungsproblem

Der Entwickler hat versucht, Positionen herauszufiltern, die mit bestehenden X-Plane-Ölplattformen überlappen. Die Filterung ist jedoch nicht perfekt — Überlappungen können auftreten. Der Entwickler bittet User, solche Fälle zu melden.

### scenery_packs.ini-Strategie

Die empfohlene Platzierung **nach** GLOBAL_AIRPORTS (niedrigere Priorität) bedeutet:

- Falls ein Heliport-Code bereits in einem höherwertigen Scenery-Pack existiert, wird die höherwertige Version geladen
- Die OSM-Heliports überschreiben keine bestehenden Airport-/Heliport-Definitionen
- Sie ergänzen nur dort, wo X-Plane noch keine Einträge hat

### Kompatibilität mit anderen Addons

- **Mission-X:** Explizit kompatibel (APT Data Optimization erforderlich)
- **Skytitude X-OilRigs:** Theoretisch kompatibel (unterschiedliche Funktionen: Skytitude ersetzt Modelle, OSM ergänzt Positionen)
- **Regionale Oil-Rig-Packs:** Potenzielle Überlappungen, wenn beide dieselben Plattformen abdecken

---

## 10. Bewertung und Einordnung

### Stärken

- Einziges weltweites Ölplattform-Addon für X-Plane 12
- Freeware, winzige Dateigröße (298 KB)
- Script-generiert — kann bei OSM-Daten-Updates neu generiert werden
- Natürliche Integration mit Mission-X für Helikopter-Missionen
- Quelloffenes Generierungs-Tool (MIT-Lizenz)
- Plattformunabhängig (Linux, macOS, Windows)
- Aktiver Entwickler mit regelmäßigen Updates

### Schwächen

- Keine eigenen 3D-Modelle — nutzt nur die einfachen Default-Assets
- OSM-Datenqualität regional stark unterschiedlich
- Überlappungen mit Default-Plattformen möglich
- Noch keine Community-Bewertungen
- Das "OSM 2006 data cutoff" aus den v1.0.1-Releasenotes ist unklar — es könnte bedeuten, dass nur OSM-Daten bis zu einem bestimmten Datum verwendet wurden

### Relevanz für XoL

- **Helicopter-Fokus:** Primär für Helikopter-Enthusiasten relevant, die zu realistisch platzierten Offshore-Plattformen fliegen wollen
- **Linux-kompatibel:** Keine Einschränkungen, plattformunabhängiges Format
- **Mission-X-Synergie:** Der Mehrwert steigt deutlich in Kombination mit Mission-X für zufallsgenerierte Helikopter-Missionen
- **Nischen-Addon:** Kleines, spezialisiertes Addon — könnte in einer Szenerie-Übersicht oder Helikopter-Sektion erwähnt werden, ist aber vermutlich kein Kandidat für eine eigene Docs-Seite

---

## Quellen

1. **x-plane.to Produktseite:** https://x-plane.to/file/1896/osm-offshore-oil-rigs
2. **forums.x-plane.org:** https://forums.x-plane.org/files/file/96552-osm-offshore-oil-rigs/
3. **OSM-zu-X-Plane-Tool (GitHub):** https://github.com/snagar/osm_to_xplane_dist
4. **snagar GitHub-Profil:** https://github.com/snagar
5. **Mission-X (x-plane.to):** https://x-plane.to/file/135/mission-x
6. **snagar Entwickler-Website:** http://snagardev.weebly.com/plugins.html
7. **Mission-X Source (GitHub):** https://github.com/snagar/mx-source-build
8. **OSM Offshore-Platform-Tag:** https://wiki.openstreetmap.org/wiki/Tag:man_made=offshore_platform
9. **OSM Seamarks/Offshore Platforms:** https://wiki.openstreetmap.org/wiki/Seamarks/Offshore_Platforms
10. **OSM Oil and Gas Infrastructure:** https://wiki.openstreetmap.org/wiki/Oil_and_Gas_Infrastructure
11. **X-Plane Scenery Priority:** https://www.x-plane.com/kb/prioritization-scenery-packs/
12. **X-Plane apt.dat 12.00 Spec:** https://developer.x-plane.com/article/airport-data-apt-dat-12-00-file-format-specification/
13. **Skytitude X-OilRigs Review:** https://www.helisimmer.com/reviews/skytitude-x-oilrigs-x-plane
14. **WW Oil Rigs Gulf of Mexico:** https://www.helisimmer.com/news/freeware-ww-oil-rigs-gulf-mexico-x-plane
15. **JoshM Gulf of Mexico Oil Rigs:** https://forums.x-plane.org/files/file/84005-gulf-of-mexico-oil-rigs-by-joshm/
