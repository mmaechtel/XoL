# Wie X-Plane die Welt aufbaut: Meshes, Orthos und Autogen einfach erklärt

<div class="video-container" markdown>
<video controls width="100%" preload="metadata" poster="../assets/video/xplane_und_scenery_packs.ini/X-Planes_Welt__Richtig_gebaut.jpg">
  <source src="../assets/video/xplane_und_scenery_packs.ini/X-Planes_Welt__Richtig_gebaut.mp4" type="video/mp4">
</video>
</div>

X-Plane ist bekannt für seine realistischen Landschaften, die den Nutzer beim Fliegen in eine lebendige Welt eintauchen lassen. Drei zentrale Bausteine machen die Szenerie aus: **Meshes**, **Orthos** und **Autogen**. In diesem Beitrag wird erklärt, was diese Begriffe bedeuten und wie sie zusammenwirken, um die beeindruckenden Landschaften in X-Plane zu schaffen.

## Meshes: Das 3D-Gerüst der Welt

Die X-Plane-Welt lässt sich wie ein riesiges 3D-Puzzle vorstellen. Den Anfang macht das **Mesh**. Ein Mesh ist die Grundform der Landschaft – das digitale Gerüst, das Höhen und Formen des Geländes definiert. Es bestimmt, wie Berge, Täler, Hügel oder Ebenen aussehen.

- **Was ist ein Mesh?** Es besteht aus vielen kleinen Dreiecken (Polygone), die zusammen ein Netz bilden – daher der Name „Mesh" (englisch für Netz). Diese Dreiecke definieren für X-Plane, wie hoch oder tief ein Punkt ist und wie steil ein Hang sein soll.
- **Beispiel**: Ein Berg in X-Plane ist durch ein Mesh definiert, das seine Höhe, Form und Neigung beschreibt. Ohne Mesh wäre die Welt nur eine flache Ebene.

Das Mesh ist also der erste Schritt: Es gibt der Landschaft ihre Struktur, aber noch keine Farben oder Details.

## Orthos: Die Satellitenbilder für Realismus

Der zweite Baustein sind die **Orthos**. Während das Mesh die Form vorgibt, sorgen Orthos für die visuelle Oberfläche – quasi wie ein riesiges Foto, das auf das Mesh geklebt wird.

- **Was sind Orthos?** Orthos sind Luft- oder Satellitenbilder, die die Erde von oben zeigen. Sie enthalten Details wie Häuser, Straßen, Wälder, Felder oder Flüsse. In X-Plane werden sie als Bilddateien (z. B. .jpg oder .png) auf das Mesh gelegt.
- **Warum sind sie wichtig?** Ohne Orthos würde das Mesh nur wie graue, leblose Hügel aussehen. Orthos bringen die Farben und Muster der echten Welt ins Spiel.
- **Beispiel**: Beim Flug über eine Stadt sind dank Orthos Dächer, Straßen und Grünflächen zu sehen, die realistisch wirken.

Tools wie **Ortho4XP** helfen dabei, hochauflösende Ortho-Bilder herunterzuladen und in X-Plane einzubinden. So wird die Szenerie noch detailreicher.

## Autogen: Die Welt wird lebendig

Mesh und Ortho schaffen schon eine beeindruckende Basis, aber etwas fehlt noch: die Tiefe. Hier kommt **Autogen** ins Spiel. Autogen (kurz für „automatisch generiert") fügt der Landschaft 3D-Objekte hinzu, die sie lebendig machen – wie Häuser, Bäume, Autos oder Strommasten.

- **Was ist Autogen?** X-Plane analysiert die Landschaft (Mesh und Ortho) und platziert automatisch passende Objekte. Es nutzt dafür oft Datenquellen wie OpenStreetMap, um zu wissen, wo Städte, Wälder oder Straßen sind.
- **Wie funktioniert es?** Autogen "liest" die Szenerie und verteilt Objekte: Bäume in Waldgebieten, Häuser in Wohnvierteln, Fabriken in Industriezonen. Diese Objekte kommen aus Bibliotheken, die X-Plane oder Add-ons bereitstellen.
- **Beispiel**: In einem Dorf sind dank Autogen Häuser mit Gärten, Bäume am Straßenrand und vielleicht ein paar parkende Autos zu sehen. Ohne Autogen wäre die Landschaft flach – nur ein Satellitenbild ohne Tiefe.

## Zusammenspiel: Wie alles zusammenkommt

Die drei Bausteine arbeiten Hand in Hand:

1. **Mesh**: Gibt die 3D-Form der Landschaft, z. B. die Höhe eines Berges oder die Tiefe eines Tals.
2. **Ortho**: Liefert das realistische Bild, das auf das Mesh gelegt wird, z. B. Wälder oder Straßen auf dem Berg.
3. **Autogen**: Fügt die 3D-Objekte hinzu, z. B. Bäume und Häuser, die perfekt zur Szenerie passen.

Das Ergebnis ist eine Welt, die nicht nur echt aussieht, sondern sich auch echt anfühlt. Beim Flug über ein Tal formt das Mesh die Hügel, das Ortho zeigt grüne Wiesen und Wege, und Autogen streut Kühe, Bäume und kleine Hütten dazu – fertig ist die lebendige Szenerie!

## Add-ons und die nächste Stufe

Viele X-Plane-Fans nutzen Add-ons, um Meshes, Orthos und Autogen zu verbessern:

- **Ortho4XP**: Lädt hochauflösende Satellitenbilder und passt sie an Meshes an.
- **Custom Sceneries**: Bringen bessere Meshes oder regionale Autogen-Objekte, z. B. typische Fachwerkhäuser für Deutschland.
- **Autogen-Bibliotheken**: Erweitern die Auswahl an Objekten, um die Szenerie noch realistischer zu machen.

Mit solchen Tools lässt sich die X-Plane-Welt noch detaillierter gestalten – perfekt für alle, die tief in die Szeneriegestaltung eintauchen wollen.

# Die richtige Reihenfolge in der scenery_packs.ini: Mesh, Orthos, Autogen und mehr

Die Landschaften in X-Plane entstehen durch das Zusammenspiel verschiedener Komponenten: Meshes, Orthos, Autogen und spezielle Szenerien wie Flughäfen. Damit alles korrekt dargestellt wird, ist die Reihenfolge in der `scenery_packs.ini`-Datei entscheidend. In diesem Beitrag wird erklärt, wie die Reihenfolge aufgebaut sein sollte, warum sie wichtig ist und wie Fehler vermieden werden können.

## Die richtige Reihenfolge der Komponenten

X-Plane lädt Szenerien von unten nach oben in der `scenery_packs.ini`. Das bedeutet: Einträge weiter unten haben eine höhere Priorität und können Einträge weiter oben überschreiben. Basierend auf den Hauptkomponenten ergibt sich folgende Reihenfolge (von unten nach oben):

1. **Mesh-Dateien (z. B. HD Mesh, UHD Mesh)**  
    - **Funktion**: Meshes bilden die 3D-Grundstruktur der Landschaft, also Höhen, Täler und Hügel.  
    - **Warum zuerst?** Sie sind die Basis für alles andere. Ohne ein Mesh können Orthos und Objekte nicht korrekt platziert werden.  
    - **Beispiel**: `FlyTampa_Athens_3_mesh` oder `SFD_EDDM_Munich_2_Mesh`.

2. **Ortho-Szenerien**  
    - **Funktion**: Orthos sind Satelliten- oder Luftbilder, die auf das Mesh gelegt werden, um realistische Texturen wie Straßen oder Wälder darzustellen.  
    - **Warum danach?** Orthos brauchen das Mesh, um korrekt "aufgespannt" zu werden, müssen aber vor Autogen geladen werden, damit Objekte darauf platziert werden können.  
    - **Beispiel**: `z_ortho_California` oder `zz_Ortho_SpainUHDv2_1`.

3. **Autogen-Objekte und Bibliotheken**  
    - **Funktion**: Autogen fügt 3D-Objekte wie Gebäude, Bäume oder Fahrzeuge hinzu, die die Landschaft lebendig machen.  
    - **Warum danach?** Autogen basiert auf Mesh und Ortho, um Objekte korrekt zu platzieren (z. B. Häuser auf ebenem Grund, keine Bäume auf Straßen).  
    - **Beispiel**: `simHeaven_X-World_Europe-6-scenery` oder `simHeaven_X-World_Europe-7-forests`.

4. **Spezielle Objekte und Masten**  
    - **Funktion**: Spezielle Objekte wie Funkmasten, Windräder oder andere markante Strukturen.  
    - **Warum danach?** Diese Objekte sollten über dem Autogen liegen, um sicherzustellen, dass sie sichtbar sind.  
    - **Beispiel**: `Usa_Radio_Masts_01` oder `world_wind_turbines`.

5. **Global Airports**  
    - **Funktion**: Enthält die Standard-Flughäfen von X-Plane.  
    - **Warum danach?** Muss über Autogen und Orthos liegen, aber unter Custom Sceneries.  
    - **Beispiel**: `*GLOBAL_AIRPORTS*`.

6. **Custom Sceneries und Landmarks**  
    - **Funktion**: Spezielle Szenerien wie Flughäfen oder Landmarken (z. B. der Eiffelturm) enthalten detaillierte Objekte und Texturen.  
    - **Warum ganz oben?** Sie haben die höchste Priorität, damit sie nicht von anderen Komponenten überdeckt werden.  
    - **Beispiel**: `Aerosoft_EDDF_Frankfurt_3_Scenery` oder `X-Plane Landmarks - Paris`.

### Beispiel einer korrekten Reihenfolge

Hier ein Auszug aus einer typischen `scenery_packs.ini` (von oben nach unten, also in der Reihenfolge, wie X-Plane sie lädt):

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

## Die besondere Rolle der Global Airports

Die Zeile `SCENERY_PACK *GLOBAL_AIRPORTS*` verdient besondere Aufmerksamkeit:

- **Position**: Sie sollte **nach** den Custom Sceneries und Landmarks, aber **vor** den SimHeaven-Komponenten und Orthos stehen.  
- **Funktion**: Global Airports enthält die Standard-Flughäfen von X-Plane, die oft von der Community über das X-Plane Gateway erstellt wurden.  
- **Warum diese Position?**  
    - Custom Sceneries (z. B. ein detailliertes EDDF oder EGLL) können die Standard-Flughäfen überschreiben, wenn sie höher in der Liste stehen.  
    - Global Airports muss über den SimHeaven-Komponenten stehen, um sicherzustellen, dass die Flughäfen nicht von Autogen-Objekten überdeckt werden.  
    - Gleichzeitig müssen Global Airports über Orthos und Meshes liegen, damit Flughäfen korrekt auf der Landschaft platziert werden.  
- **Wichtiger Hinweis**: Eine falsche Position kann zu Problemen führen, wie "schwebenden" Flughäfen, fehlenden Rollwegen oder überdeckten Details.

## Warum die Reihenfolge so wichtig ist

Die korrekte Reihenfolge in der `scenery_packs.ini` ist entscheidend aus mehreren Gründen:

- **Überlagerung**: Einträge weiter oben (mit höherer Priorität) überschreiben Einträge weiter unten. Ein falsch platzierter Eintrag kann z. B. einen Flughafen unsichtbar machen oder Orthos verdecken.  
- **Korrektheit**: Nur die richtige Reihenfolge stellt sicher, dass Objekte korrekt platziert werden – Häuser stehen auf dem Boden, nicht in der Luft, und Flughäfen passen zum Mesh.  
- **Performance**: Eine logische Reihenfolge hilft X-Plane, Szenerien effizienter zu laden, was die Ladezeiten und Performance verbessern kann.  

## Tipps für die Pflege der scenery_packs.ini

Damit die Szenerien immer korrekt angezeigt werden, hier einige praktische Tipps:

- **Tools nutzen**: Programme wie **[XOrganizer](addon/xorganizer.md)** können die Reihenfolge automatisch optimieren und Konflikte erkennen.  
- **Backup erstellen**: Vor Änderungen an der `scenery_packs.ini` sollte eine Sicherungskopie erstellt werden, um Fehler rückgängig machen zu können.  
- **Testen**: Nach Änderungen sollte eine Szenerie in X-Plane geladen und geprüft werden, ob Flughäfen, Orthos und Autogen korrekt angezeigt werden. Besonders auf "schwebende" Objekte oder fehlende Details sollte geachtet werden.  
- **Updates im Blick behalten**: Neue Szenerien oder Add-ons können die Reihenfolge durcheinanderbringen. Die Datei sollte regelmäßig, besonders nach Installationen, überprüft werden. 