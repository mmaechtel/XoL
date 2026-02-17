# Wie X-Plane die Welt aufbaut

<div class="video-container" markdown>
<video controls width="100%" preload="metadata" aria-label="Video: X-Planes Welt — Richtig gebaut" poster="../assets/video/de/X-Planes_Welt__Richtig_gebaut/X-Planes_Welt__Richtig_gebaut.jpg">
  <source src="../assets/video/de/X-Planes_Welt__Richtig_gebaut/X-Planes_Welt__Richtig_gebaut.mp4" type="video/mp4">
</video>
</div>

X-Plane liefert eine Szenerie, die aus der Höhe plausibel wirkt, aber weit entfernt von fotorealistisch ist. Mit den richtigen Add-ons lässt sich die visuelle Qualität jedoch deutlich steigern. Um dort hinzukommen, hilft es, die drei Schichten zu verstehen, aus denen X-Planes Szeneriesystem aufgebaut ist: das **Mesh** definiert die Geländehöhen, **Orthos** liefern Satellitenbilder als Bodentexturen, und **Autogen** bevölkert die Landschaft mit 3D-Objekten.

## Meshes

Das [Mesh](../glossary.md#mesh) ist das Höhenmodell des Geländes — ein Netzwerk aus Dreiecken (ein Triangulated Irregular Network, kurz TIN), das Höhen und Neigungen definiert. Jeder Dreieckspunkt trägt eine Koordinate mit Längengrad, Breitengrad und Höhe. Zusammen formen diese Dreiecke Berge, Täler und Ebenen.

Mesh-Daten sind in X-Planes [DSF](../glossary.md#dsf-distribution-scenery-format)-Dateien (Distribution Scenery Format) gespeichert. Das Standard-Mesh wird mit dem Simulator ausgeliefert; höher aufgelöste Alternativen (z. B. HD Mesh Scenery) lassen sich als Scenery Packs installieren.

Das Mesh liefert nur die Struktur — keine Texturen oder Objekte.

## Orthos

Orthos ([Orthofotos](../glossary.md#orthofotos)) sind Luft- oder Satellitenbilder, die als Bodentexturen auf das Mesh projiziert werden. Sie ersetzen X-Planes prozedurale Landklassen durch fotorealistische Darstellungen — Straßen, Felder, Wälder und Gebäude werden aus der Höhe sichtbar.

X-Plane verwendet intern [DDS](../glossary.md#dds-directdraw-surface)-Texturen (DirectDraw Surface). Quellbilder von Kartendiensten (JPEG, PNG) werden vor der Nutzung in GPU-komprimiertes DDS-Format (DXT1/BC1 oder DXT5/BC3) konvertiert.

Tools wie **[Ortho4XP](orthophotography/ortho4xp.md)** generieren diese DDS-Kacheln offline, während Streaming-Lösungen sie bei Bedarf liefern (siehe unten).

## Autogen

[Autogen](../glossary.md#autogen) (automatisch generierte Szenerie) fügt der Landschaft 3D-Objekte hinzu — Gebäude, Bäume, Fahrzeuge, Stromleitungen. X-Plane liest Platzierungsinformationen aus seinen DSF-Szeneriedateien und verteilt Objekte entsprechend: Bäume in Waldgebieten, Gebäude in Wohnzonen, Fabriken in Industriegebieten.

Die Platzierungsdaten in X-Planes Standardszenerie stammen aus OpenStreetMap und anderen geografischen Datensätzen, die während Laminar Researchs Szenerie-Build-Pipeline verarbeitet werden. Diese Daten sind in die DSF-Dateien eingebacken — X-Plane fragt OSM nicht zur Laufzeit ab. Drittanbieter-Add-ons wie SimHeaven X-World nutzen OSM-Daten separat, um detailliertere Autogen-Abdeckung zu erzeugen.

## Zusammenspiel der Schichten

Die drei Schichten bauen in fester Reihenfolge aufeinander auf:

1. **Mesh** — definiert Höhen und Geländeform
2. **Ortho** — projiziert Satellitenbilder auf die Mesh-Oberfläche
3. **Autogen** — platziert 3D-Objekte basierend auf Landnutzungsdaten

Jede Schicht hängt von der darunterliegenden ab. Orthos benötigen das Mesh für korrekte Projektion, und Autogen benötigt sowohl Mesh- als auch Ortho-Daten, um Objekte an den richtigen Positionen und Höhen zu platzieren.

## Add-ons

Mehrere Add-ons erweitern die Standard-Szenerieschichten:

- **[Ortho4XP](orthophotography/ortho4xp.md)** — generiert hochauflösende Ortho-Kacheln offline aus Satellitenbildern
- **[Ortho-Streaming](orthophotography/orthophotography_intro.md#ortho-streaming)** — AutoOrtho, XEarthLayer und XPME streamen Satellitenbilder bei Bedarf, ohne Vorabgenerierung
- **[Custom Sceneries](../glossary.md#custom-scenery)** — höher aufgelöste Meshes oder regionale Autogen-Objekte (z. B. SimHeaven X-World)
- **Autogen-Bibliotheken** — zusätzliche Objektsets für vielfältigere Gebäude- und Vegetationsplatzierung

---

## Die scenery_packs.ini-Ladereihenfolge

Die Landschaften in X-Plane entstehen durch das Zusammenspiel verschiedener Komponenten: Meshes, Orthos, Autogen und spezielle Szenerien wie Flughäfen. X-Plane verarbeitet die `scenery_packs.ini` von oben nach unten — Einträge weiter oben haben höhere Priorität und überschreiben Einträge darunter. Eine falsche Reihenfolge kann zu schwebenden Flughäfen, unsichtbaren Szenerien oder Autogen-Objekten auf Landebahnen führen.

**Schicht-Priorität (unten → oben in der Datei)**

| Priorität | Schicht | Funktion | Beispiel |
|-----------|---------|----------|----------|
| 6 (oben) | Custom Sceneries & Landmarks | Detaillierte Flughäfen, Landmarken | `Aerosoft_EDDF_Frankfurt_3_Scenery` |
| 5 | [Global Airports](../glossary.md#global-airports) | Standard-Flughäfen (X-Plane Gateway) | `*GLOBAL_AIRPORTS*` |
| 4 | Spezielle Objekte | Funkmasten, Windräder | `world_wind_turbines` |
| 3 | Autogen & Bibliotheken | 3D-Objekte (Gebäude, Bäume, Fahrzeuge) | `simHeaven_X-World_Europe-6-scenery` |
| 2 | Ortho-Szenerien | Satellitenbilder auf dem Mesh | `z_ortho_California` |
| 1 (unten) | Mesh-Dateien | 3D-Geländestruktur (Höhen, Täler) | `HD_Mesh_Scenery` |

!!! warning "Global Airports — Position beachten"
    Die Zeile `SCENERY_PACK *GLOBAL_AIRPORTS*` muss **unter** Custom Sceneries, aber **über** Autogen, Orthos und Meshes stehen. Steht sie zu tief, überdecken Autogen-Objekte Landebahnen und Rollwege; steht sie zu hoch, verlieren Custom Airports ihren Vorrang. Eine falsche Position verursacht häufig „schwebende" Flughäfen oder fehlende Details.

### Beispiel einer korrekten Reihenfolge

Hier ein Auszug aus einer typischen `scenery_packs.ini` (von oben nach unten, also in der Reihenfolge, wie X-Plane sie verarbeitet):

```ini
# Custom Airports und Landmarks (höchste Priorität)
SCENERY_PACK Custom Scenery/Aerosoft-EGLL Airport London-Heathrow_1_DefaultStreets/
SCENERY_PACK Custom Scenery/Aerosoft-EGLL Airport London-Heathrow_2/
SCENERY_PACK Custom Scenery/Aerosoft_EDDF_Frankfurt_1_Parked_Cars/
SCENERY_PACK Custom Scenery/Aerosoft_EDDF_Frankfurt_2_Roads/
SCENERY_PACK Custom Scenery/Aerosoft_EDDF_Frankfurt_3_Scenery/
SCENERY_PACK Custom Scenery/X-Plane Landmarks - Berlin and Frankfurt/
SCENERY_PACK Custom Scenery/X-Plane Landmarks - London/
SCENERY_PACK Custom Scenery/X-Plane Landmarks - Paris/

# Global Airports (Standard-Flughäfen)
SCENERY_PACK *GLOBAL_AIRPORTS*

# Spezielle Objekte und Masten
SCENERY_PACK Custom Scenery/Usa_Radio_Masts_01/
SCENERY_PACK Custom Scenery/Usa_TV_Masts_0/
SCENERY_PACK Custom Scenery/world_wind_turbines/

# SimHeaven X-World (Autogen)
SCENERY_PACK Custom Scenery/simHeaven_X-World_Europe-1-vfr/
SCENERY_PACK Custom Scenery/simHeaven_X-World_Europe-2-regions/
SCENERY_PACK Custom Scenery/simHeaven_X-World_Europe-3-details/
SCENERY_PACK Custom Scenery/simHeaven_X-World_Europe-4-extras/
SCENERY_PACK Custom Scenery/simHeaven_X-World_Europe-5-footprints/
SCENERY_PACK Custom Scenery/simHeaven_X-World_Europe-6-scenery/
SCENERY_PACK Custom Scenery/simHeaven_X-World_Europe-7-forests/
SCENERY_PACK Custom Scenery/simHeaven_X-World_Europe-8-network/

# Ortho-Szenerien
SCENERY_PACK Custom Scenery/z_ortho_California/
SCENERY_PACK Custom Scenery/z_ortho_Colorado/
SCENERY_PACK Custom Scenery/z_ortho_Florida/
SCENERY_PACK Custom Scenery/zz_Ortho_Alps_West/
SCENERY_PACK Custom Scenery/zz_Ortho_SpainUHDv2_1/

# Mesh-Dateien (niedrigste Priorität)
SCENERY_PACK Custom Scenery/FlyTampa_Athens_3_mesh/
SCENERY_PACK Custom Scenery/FlyTampa_Amsterdam_4_mesh/
SCENERY_PACK Custom Scenery/KDEN-Denver International Airport_Mesh/
SCENERY_PACK Custom Scenery/SFD_EDDM_Munich_2_Mesh/
```

!!! tip "Pflege der scenery_packs.ini"
    - **Tools nutzen** — Programme wie **[XOrganizer](../addon/tools/xorganizer.md)** können die Reihenfolge automatisch optimieren und Konflikte erkennen.
    - **Backup erstellen** vor Änderungen an der `scenery_packs.ini`, um Fehler rückgängig machen zu können.
    - **Nach Änderungen testen** — eine Szenerie in X-Plane laden und Flughäfen, Orthos und Autogen prüfen. Besonders auf „schwebende" Objekte oder fehlende Details achten.
    - **Updates im Blick behalten** — neue Szenerien oder Add-ons können die Reihenfolge durcheinanderbringen. Die Datei regelmäßig prüfen, besonders nach Installationen.

---

## Quellen

- [X-Plane Scenery Developer Documentation](https://developer.x-plane.com/article/dsf-usage-in-x-plane/) — DSF-Dateiformat und Szeneriestruktur
- [X-Plane Manual — Custom Scenery](https://www.x-plane.com/manuals/) — scenery_packs.ini-Ladereihenfolge
