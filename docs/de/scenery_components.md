# Wie X-Plane die Welt aufbaut

<div class="video-container" markdown>
<video controls width="100%" preload="metadata" aria-label="Video: X-Planes Welt — Richtig gebaut" poster="../assets/video/de/X-Planes_Welt__Richtig_gebaut/X-Planes_Welt__Richtig_gebaut.jpg">
  <source src="../assets/video/de/X-Planes_Welt__Richtig_gebaut/X-Planes_Welt__Richtig_gebaut.mp4" type="video/mp4">
</video>
</div>

X-Plane liefert eine Szenerie, die aus der Höhe plausibel wirkt, aber weit entfernt von fotorealistisch ist. Mit den richtigen Add-ons lässt sich die visuelle Qualität jedoch deutlich steigern. Um dort hinzukommen, hilft es, die drei Schichten zu verstehen, aus denen X-Planes Szeneriesystem aufgebaut ist: das **Mesh** definiert die Geländehöhen, **Orthos** liefern Satellitenbilder als Bodentexturen, und **Autogen** bevölkert die Landschaft mit 3D-Objekten.

## Meshes

Das Mesh ist das Höhenmodell des Geländes — ein Netzwerk aus Dreiecken (ein Triangulated Irregular Network, kurz TIN), das Höhen und Neigungen definiert. Jeder Dreieckspunkt trägt eine Koordinate mit Längengrad, Breitengrad und Höhe. Zusammen formen diese Dreiecke Berge, Täler und Ebenen.

Mesh-Daten sind in X-Planes DSF-Dateien (Distribution Scenery Format) gespeichert. Das Standard-Mesh wird mit dem Simulator ausgeliefert; höher aufgelöste Alternativen (z. B. HD Mesh Scenery) lassen sich als Scenery Packs installieren.

Das Mesh liefert nur die Struktur — keine Texturen oder Objekte.

## Orthos

Orthos (Orthophotos) sind Luft- oder Satellitenbilder, die als Bodentexturen auf das Mesh projiziert werden. Sie ersetzen X-Planes prozedurale Landklassen durch fotorealistische Darstellungen — Straßen, Felder, Wälder und Gebäude werden aus der Höhe sichtbar.

X-Plane verwendet intern DDS-Texturen (DirectDraw Surface). Quellbilder von Kartendiensten (JPEG, PNG) werden vor der Nutzung in GPU-komprimiertes DDS-Format (DXT1/BC1 oder DXT5/BC3) konvertiert.

Tools wie **[Ortho4XP](addon/ortho4xp.md)** generieren diese DDS-Kacheln offline, während Streaming-Lösungen sie bei Bedarf liefern (siehe unten).

## Autogen

Autogen (automatisch generierte Szenerie) fügt der Landschaft 3D-Objekte hinzu — Gebäude, Bäume, Fahrzeuge, Stromleitungen. X-Plane liest Platzierungsinformationen aus seinen DSF-Szeneriedateien und verteilt Objekte entsprechend: Bäume in Waldgebieten, Gebäude in Wohnzonen, Fabriken in Industriegebieten.

Die Platzierungsdaten in X-Planes Standardszenerie stammen aus OpenStreetMap und anderen geografischen Datensätzen, die während Laminar Researchs Szenerie-Build-Pipeline verarbeitet werden. Diese Daten sind in die DSF-Dateien eingebacken — X-Plane fragt OSM nicht zur Laufzeit ab. Drittanbieter-Add-ons wie SimHeaven X-World nutzen OSM-Daten separat, um detailliertere Autogen-Abdeckung zu erzeugen.

## Zusammenspiel der Schichten

Die drei Schichten bauen in fester Reihenfolge aufeinander auf:

1. **Mesh** — definiert Höhen und Geländeform
2. **Ortho** — projiziert Satellitenbilder auf die Mesh-Oberfläche
3. **Autogen** — platziert 3D-Objekte basierend auf Landnutzungsdaten

Jede Schicht hängt von der darunterliegenden ab. Orthos benötigen das Mesh für korrekte Projektion, und Autogen benötigt sowohl Mesh- als auch Ortho-Daten, um Objekte an den richtigen Positionen und Höhen zu platzieren.

## Add-ons

Mehrere Add-ons erweitern die Standard-Szenerieschichten:

- **[Ortho4XP](addon/ortho4xp.md)** — generiert hochauflösende Ortho-Kacheln offline aus Satellitenbildern
- **[Ortho-Streaming](addon/orthophotography_intro.md#ortho-streaming)** — AutoOrtho, XEarthLayer und XPME streamen Satellitenbilder bei Bedarf, ohne Vorabgenerierung
- **Custom Sceneries** — höher aufgelöste Meshes oder regionale Autogen-Objekte (z. B. SimHeaven X-World)
- **Autogen-Bibliotheken** — zusätzliche Objektsets für vielfältigere Gebäude- und Vegetationsplatzierung

---

## Die scenery_packs.ini-Ladereihenfolge

Die Landschaften in X-Plane entstehen durch das Zusammenspiel verschiedener Komponenten: Meshes, Orthos, Autogen und spezielle Szenerien wie Flughäfen. Damit alles korrekt dargestellt wird, ist die Reihenfolge in der `scenery_packs.ini`-Datei entscheidend.

## Die richtige Reihenfolge der Komponenten

X-Plane verarbeitet die `scenery_packs.ini` von oben nach unten. Einträge weiter oben in der Datei haben höhere Priorität und überschreiben Einträge darunter. Die folgende Liste beschreibt die Schichten von der niedrigsten Priorität (unten in der Datei) zur höchsten (oben):

1. **Mesh-Dateien (z. B. HD Mesh, UHD Mesh)**
    - **Funktion**: Meshes bilden die 3D-Grundstruktur der Landschaft — Höhen, Täler und Hügel.
    - **Warum unten?** Sie sind die Basis für alles andere. Ohne ein Mesh lassen sich Orthos und Objekte nicht korrekt platzieren.
    - **Beispiel**: `FlyTampa_Athens_3_mesh` oder `SFD_EDDM_Munich_2_Mesh`.

2. **Ortho-Szenerien**
    - **Funktion**: Orthos sind Satelliten- oder Luftbilder, die auf das Mesh gelegt werden, um realistische Texturen wie Straßen oder Wälder darzustellen.
    - **Warum darüber?** Orthos brauchen das Mesh für korrekte Projektion, müssen aber über den Meshes und unter Autogen liegen.
    - **Beispiel**: `z_ortho_California` oder `zz_Ortho_SpainUHDv2_1`.

3. **Autogen-Objekte und Bibliotheken**
    - **Funktion**: Autogen fügt 3D-Objekte wie Gebäude, Bäume oder Fahrzeuge hinzu, die die Landschaft beleben.
    - **Warum darüber?** Autogen basiert auf Mesh und Ortho, um Objekte korrekt zu platzieren (z. B. Häuser auf ebenem Grund, keine Bäume auf Straßen).
    - **Beispiel**: `simHeaven_X-World_Europe-6-scenery` oder `simHeaven_X-World_Europe-7-forests`.

4. **Spezielle Objekte und Masten**
    - **Funktion**: Spezielle Objekte wie Funkmasten, Windräder oder andere markante Strukturen.
    - **Warum darüber?** Diese Objekte sollten über dem Autogen liegen, um sichtbar zu bleiben.
    - **Beispiel**: `Usa_Radio_Masts_01` oder `world_wind_turbines`.

5. **Global Airports**
    - **Funktion**: Enthält die Standard-Flughäfen von X-Plane.
    - **Warum darüber?** Muss über Autogen und Orthos liegen, aber unter Custom Sceneries.
    - **Beispiel**: `*GLOBAL_AIRPORTS*`.

6. **Custom Sceneries und Landmarks**
    - **Funktion**: Spezielle Szenerien wie Flughäfen oder Landmarken (z. B. der Eiffelturm) enthalten detaillierte Objekte und Texturen.
    - **Warum ganz oben?** Sie haben die höchste Priorität, damit sie nicht von anderen Komponenten überdeckt werden.
    - **Beispiel**: `Aerosoft_EDDF_Frankfurt_3_Scenery` oder `X-Plane Landmarks - Paris`.

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

### Die besondere Rolle der Global Airports

Die Zeile `SCENERY_PACK *GLOBAL_AIRPORTS*` verdient besondere Aufmerksamkeit:

- **Position**: Sie sollte **unter** den Custom Sceneries und Landmarks stehen, aber **über** den SimHeaven-Komponenten, Orthos und Meshes.
- **Funktion**: Global Airports enthält die Standard-Flughäfen von X-Plane, die oft von der Community über das X-Plane Gateway erstellt wurden.
- **Warum diese Position?**
    - Custom Sceneries (z. B. ein detailliertes EDDF oder EGLL) überschreiben die Standard-Flughäfen, weil sie weiter oben gelistet sind.
    - Global Airports muss über den SimHeaven-Komponenten stehen, damit Flughäfen nicht von Autogen-Objekten überdeckt werden.
    - Gleichzeitig muss Global Airports über Orthos und Meshes liegen, damit Flughäfen korrekt auf der Landschaft platziert werden.
- **Wichtiger Hinweis**: Eine falsche Position kann zu „schwebenden" Flughäfen, fehlenden Rollwegen oder überdeckten Details führen.

---

## Warum die Reihenfolge wichtig ist

Die Reihenfolge in der `scenery_packs.ini` beeinflusst direkt die visuelle Korrektheit:

- **Überlagerung**: Einträge weiter oben in der Datei überschreiben Einträge darunter. Ein falsch platzierter Eintrag kann einen Flughafen unsichtbar machen oder Orthos mit Autogen-Objekten verdecken.
- **Korrektheit**: Nur die richtige Reihenfolge stellt sicher, dass Objekte korrekt platziert werden — Häuser stehen auf dem Boden, nicht in der Luft, und Flughäfen passen zum Mesh.

---

## Tipps für die Pflege der scenery_packs.ini

- **Tools nutzen**: Programme wie **[XOrganizer](addon/xorganizer.md)** können die Reihenfolge automatisch optimieren und Konflikte erkennen.
- **Backup erstellen**: Vor Änderungen an der `scenery_packs.ini` eine Sicherungskopie erstellen, um Fehler rückgängig machen zu können.
- **Testen**: Nach Änderungen eine Szenerie in X-Plane laden und prüfen, ob Flughäfen, Orthos und Autogen korrekt angezeigt werden. Besonders auf „schwebende" Objekte oder fehlende Details achten.
- **Updates im Blick behalten**: Neue Szenerien oder Add-ons können die Reihenfolge durcheinanderbringen. Die Datei regelmäßig prüfen, besonders nach Installationen.

---

## Quellen

- [X-Plane Scenery Developer Documentation](https://developer.x-plane.com/article/dsf-usage-in-x-plane/) — DSF-Dateiformat und Szeneriestruktur
- [X-Plane Manual — Custom Scenery](https://www.x-plane.com/manuals/) — scenery_packs.ini-Ladereihenfolge
- [Arch Wiki — X-Plane](https://wiki.archlinux.org/title/X-Plane) — Linux-spezifische Konfiguration
