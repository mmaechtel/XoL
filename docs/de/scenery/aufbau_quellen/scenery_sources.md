---
description: "Verfügbare X-Plane-Szenerie: Standard-Szenerie mit Gateway-Airports, SimHeaven X-World und X-World Pro Autogen, Freeware, Payware und interaktive WorldMaps."
---
# Szenerien

Hier finden sich Informationen zu verschiedenen Szenerieoptionen für X-Plane.

## Übersicht

X-Plane bietet verschiedene Möglichkeiten, realistische Szenerien und Landschaften zu nutzen. In diesem Abschnitt werden die wichtigsten Optionen vorgestellt.

## Standard-Szenerien

X-Plane wird mit einer umfangreichen Sammlung von Standard-Szenerien ausgeliefert:

- **Global Scenery**: Grundlegende Landschaftsdaten für die gesamte Welt
- **Default Airports**: Basis-Flughäfen mit grundlegenden Gebäuden und Landebahnen ([X-Plane Gateway](https://gateway.x-plane.com/))
- **Autogen**: Automatisch generierte Gebäude und Vegetation
- **Mesh**: Grundlegende Geländedaten

Die Standard-Szenerien bieten eine gute Basis für den Flugsimulator, können aber durch zusätzliche Szenerien erheblich verbessert werden.

### X-Plane Gateway Server

Der [X-Plane Gateway Server](https://gateway.x-plane.com/) stellt eine zentrale Plattform für die Community-gestützte Entwicklung von Flughafenszenerien dar. Auf dieser Plattform haben Benutzer die Möglichkeit, Flughäfen zu erstellen und zu verbessern, ihre Arbeiten mit der Community zu teilen, von anderen Benutzern erstellte Flughäfen herunterzuladen und an der Qualitätssicherung teilzunehmen. Die auf dem Gateway veröffentlichten Flughäfen durchlaufen eine Überprüfung durch Laminar Research und werden in zukünftige X-Plane-Updates integriert. Dieses System gewährleistet eine stetige Verbesserung der Standard-Flughäfen, ermöglicht eine weltweite Community von Entwicklern, bietet Qualitätskontrolle durch Laminar Research und garantiert regelmäßige Updates der Flughäfen. Eine Übersicht aller verfügbaren Gateway-Flughäfen findet sich in der [Gateway Scenery Map](https://x-plane.cleverest.eu/). Auch ist dort vermerkt, ab welcher Version der Flughafen mit X-Plane ausgeliefert wird. Vor einem Download ist somit zu prüfen, ob der Flughafen nicht schon in der aktuellen X-Plane Version mit dabei ist.

## SimHeaven X-World

SimHeaven X-World stellt eine Szenerie-Erweiterung dar, die die Standard-Szenerien von X-Plane erheblich verbessert. Die Erweiterung bietet detaillierte Gebäude und Stadtlandschaften, realistische Vegetation und Bäume sowie verbesserte Straßennetze und Autobahnen. Besonders hervorzuheben sind die korrekten Gebäudehöhen und -formen sowie die regionalen Architekturstile, die eine authentische Darstellung verschiedener Regionen ermöglichen.

Die Erweiterung deckt verschiedene Regionen ab: X-World Europe bietet detaillierte europäische Städte und Landschaften, X-World America umfasst nord- und südamerikanische Regionen, X-World Asia präsentiert asiatische Städte und Landschaften, X-World Africa zeigt afrikanische Regionen, und X-World Oceania stellt Australien und Ozeanien dar.

Die Installation erfolgt manuell im Custom Scenery Verzeichnis. Die Erweiterung ist kompatibel mit Ortho4XP und AutoOrtho, optimiert für X-Plane 12 und wird durch regelmäßige Updates und Verbesserungen kontinuierlich weiterentwickelt.

Die klassischen X-World-Pakete für X-Plane 11 und X-Plane 12 bleiben kostenlose Downloads auf [simheaven.com](https://simheaven.com/xp12-sceneries/) und werden weiterhin gepflegt. Daneben bietet SimHeaven inzwischen eine kommerzielle Linie an: [X-World Pro](https://simheaven.com/x-world-pro/).

### X-World Pro

X-World Pro ist eine VFR-orientierte Szenerie-Linie für X-Plane 12 und wird über den X-Plane.org Store verkauft — entweder einzelne Kontinente oder ein vergünstigtes World-Bundle. Die kostenlosen Pakete werden dadurch nicht abgelöst, sie bleiben verfügbar; Pro verzichtet lediglich auf die inhaltlichen Kürzungen der freien Versionen.

**Was Pro gegenüber den freien Paketen bietet**

- Vollständige VFR-Daten statt des reduzierten Umfangs der freien X-World-Pakete
- Komplette Netz-Layer (Straße, Schiff, Luft) inklusive Verkehrsdichte, die in den freien Paketen fehlen oder stark gekürzt sind
- Deutlich größere Objektvielfalt sowie mehr Detail bei Vegetation, Feldern und Feldfrüchten
- Animierte Effekte wie Schornsteinrauch, Dampf und Geysire sowie Straßenverkehr mit regionstypischen Geschwindigkeiten
- Weltweit platzierte Landmarks als visuelle Navigationsreferenz

Die Objektplatzierung basiert auf OpenStreetMap und Microsoft Building Footprints — derselben Datengrundlage wie bei den freien Paketen. Der Unterschied liegt in Dichte und Vollständigkeit, nicht in einer anderen Datenquelle.

Auf der SimHeaven-Seite steht eine kostenlose Testszenerie über rund 15 Kacheln im Ruhrgebiet, in Luxemburg sowie in Teilen der Niederlande, Belgiens und Frankreichs bereit. Sie dient dazu, Framerate und Ladeverhalten vor dem Kauf zu prüfen.

**Installation**

Pro besteht aus den Szenerie-Layern und einem separaten Library-Paket (`simHeaven_X-WORLD-Pro_Library`), das Vegetation und die referenzierten X-Plane-12-Assets liefert. Beides wird nach `Custom Scenery/` entpackt und in der [scenery_packs.ini](../../glossary.md#scenery_packsini) in der üblichen Reihenfolge eingetragen: zuerst Flughäfen und regionale Szenerien, dann die X-World-Layer, anschließend Libraries, Overlays, Ortho und Mesh.

!!! warning "Vegetations-Library braucht unter Linux einen Symlink"

    Die Vegetations-Libraries von SimHeaven liefern die Wald-Definitionen von X-Plane nicht mit, sondern verlinken sie. Unter Windows erledigt das ein mitgeliefertes `.bat`-Skript, das unter Linux wirkungslos ist. Liegt im Library-Verzeichnis eine solche Batch-Datei, ist der Link manuell anzulegen:

    ```bash
    cd "X-Plane 12/Custom Scenery/simHeaven_X-World_Vegetation_Library"   # oder das Pro-Library-Verzeichnis
    ln -sf "../../Resources/default scenery/1200 forests" "1200 forests"
    ```

    Fehlt der Link, bricht X-Plane das Laden mit `Failed to find resource 'simheaven/forests/….for'` ab. Den Ordner `1200 forests` stattdessen zu kopieren funktioniert zwar, kostet aber Plattenplatz und geht bei X-Plane-Updates verloren.

Ob X-World Pro und ein freies X-World-Paket für denselben Kontinent parallel betrieben werden können, dokumentiert SimHeaven nicht. Da beide Autogen aus derselben Datengrundlage platzieren, führt ein Stapeln zu doppelten Objekten — pro Region sollte nur eine Linie aktiv sein.

## Freeware und Shareware

Auf [x-plane.org](https://forums.x-plane.org/) findet sich eine umfangreiche Auswahl an kostenlosen und günstigen Szenerien. Die Community bietet eine Vielzahl von Flughäfen an, darunter verbesserte Versionen von Standard-Flughäfen und historische Flughäfen. Im Bereich der Landschaften stehen verbesserte Geländedaten, detailliertere Vegetation und spezielle Regionen zur Verfügung.

Für die Erstellung und Verwaltung von Szenerien stehen verschiedene Tools zur Verfügung. [Ortho4XP](../orthophotography/ortho4xp.md) ermöglicht die Erstellung eigener Orthofoto-Szenerien, während [AutoOrtho](../ortho_streaming/autoortho.md) automatische Orthofoto-Szenerien bereitstellt. [XRoad](../../addon/scenery_addons/xroad.md) bietet verbesserte Straßennetze für eine realistischere Darstellung der Infrastruktur.

## Payware-Szenerien

Für die höchste Qualität und Detailtreue stehen zahlreiche kommerzielle Szenerien zur Verfügung. Eine fast vollständige Übersicht findet sich unten verlinkt.

## Ressourcen

Zur besseren Übersicht und Planung der Flugsimulation stehen zwei selbst erstellte WorldMaps zur Verfügung:

- **[WorldMap der Szenerien](/Maps/airportmap.html)** – Eine interaktive Karte mit über 1800 Szenerien für X-Plane 12. Die Karte bietet detaillierte Informationen zu jedem Flughafen, um die Suche nach der passenden Szenerie zu erleichtern. Die Suche erfolgt über einen 4-stelligen gültigen ICAO-Code, wodurch kleinere Landeplätze wie Graspisten und Hubschrauberlandeplätze nicht dargestellt werden - dies würde die Karte an einigen Stellen bereits jetzt zu unübersichtlich machen. Auf direkte Download-Links wurde bewusst verzichtet, da:
    - Keine Kaufempfehlungen für bestimmte Shops gegeben werden sollen
    - Die Aktualisierung zahlreicher Links sehr aufwändig wäre
    - Die Karte sich auf X-Plane 12 Szenerien konzentriert (XP11 Szenerien wurden nur dann aufgenommen, wenn es spezielle Anpassungen gibt, wodurch die Szenerie Features von XP12 unterstützt)

    Es gibt einen Hilfe-Link in der Agenda, der die Einträge des Popups erklärt.

- **[WorldMap der Ortho Tiles](/Maps/scenerymap.html)** – Eine Übersichtskarte der selbst erstellten und installierten Ortho Tiles. Die dargestellten Orthos wurden speziell für Addon-Szenerien erstellt und bieten hochauflösende Texturen, oft ergänzt durch Mesh Patches für zusätzliche Details wie Runway Slopes. Neben den selbst erstellten Orthos werden auch offizielle Ortho Patches der Szenerienhersteller sowie Community-erstellte Patches aus dem X-Plane.org Forum benutzt.

---

## Weiterführende Kapitel

| Thema | Seite | Schwerpunkt |
|---|---|---|
| Szenerie-Komponenten | [Wie X-Plane die Welt aufbaut](scenery_components.md) | Mesh, Ortho, Autogen und scenery_packs.ini-Ladereihenfolge |
| Orthofotografie | [Konzepte & Methoden](../orthophotography/orthophotography_intro.md) | Statische vs. Streaming-Ansätze für Bodentexturen |
| AutoOrtho | [AutoOrtho](../ortho_streaming/autoortho.md) | Echtzeit-Ortho-Streaming mit globaler Abdeckung |
| XEarthLayer | [XEarthLayer](../ortho_streaming/xearthlayer.md) | Rust-basiertes Streaming mit adaptivem Prefetch |
| XOrganizer | [XOrganizer](../../addon/tools/xorganizer.md) | Szenerie-Verwaltung und scenery_packs.ini-Editor |
| GPU & VRAM | [GPU & VRAM](../../fundamentals/performance/gpu_vram.md) | VRAM-Auswirkungen der Szeneriequalität |