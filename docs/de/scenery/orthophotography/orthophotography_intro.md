---
description: "Statische Generierung vs. Ortho-Streaming für X-Plane-Bodentexturen. Ortho4XP, AutoOrtho, XEarthLayer, scenery_packs.ini und Spielerprofile."
---
# Einführung in die Orthofotographie in der Flugsimulation

Die Orthofotographie stellt einen zentralen Bestandteil moderner Flugsimulationsumgebungen dar, da sie hochauflösende und realistische Bodentexturen ermöglicht. Dieser Abschnitt erläutert die methodischen Ansätze zur Integration qualitativ hochwertiger Orthofotos in die Flugsimulationssoftware X-Plane.

<div class="video-container" markdown>
<video controls width="100%" preload="metadata" aria-label="Video: Ortho-Streaming für X-Plane" poster="../../../assets/video/de/Ortho-Streaming_für_X-Plane/Ortho-Streaming_für_X-Plane.jpg">
  <source src="../../../assets/video/de/Ortho-Streaming_für_X-Plane/Ortho-Streaming_für_X-Plane.mp4" type="video/mp4">
</video>
</div>

## Bedeutung der Orthofotographie

In der Flugsimulation ist eine präzise Darstellung des Geländes essenziell, um realitätsnahe Lande- und Flugbedingungen zu gewährleisten. X-Plane enthält standardmäßig ein globales Höhenmodell („Mesh"), dessen Auflösung jedoch aufgrund von Speicherbeschränkungen oft begrenzt ist. Dieses Höhenmodell, das im Menü „Komponenten" der Szenerien detailliert beschrieben wird, bildet die Grundlage für die Geländedarstellung. Durch den Einsatz spezifischer Erweiterungen (Add-ons) können sowohl die Präzision des Meshes als auch die Qualität der projizierten Bodentexturen signifikant verbessert werden. Das primäre Ziel besteht in der Erhöhung der topografischen Genauigkeit, wobei die visuelle Optimierung der Szenerie als sekundärer Vorteil resultiert.

## Methoden zur Integration von Orthofotos

Zur Einbindung von Orthofotos in X-Plane haben sich zwei grundlegend verschiedene Ansätze etabliert:

### Statische Generierung

Bei diesem Ansatz werden Orthofoto-Kacheln vor dem Flug vollständig heruntergeladen, in DDS-Texturen konvertiert und dauerhaft auf der lokalen Festplatte gespeichert. X-Plane liest diese Kacheln wie reguläre Szeneriedaten ein — eine Internetverbindung wird zur Laufzeit nicht benötigt. Der Datenbestand muss manuell verwaltet werden und wächst mit jeder generierten Region.

- **[Ortho4XP](ortho4xp.md)**: Das etablierte Werkzeug zur statischen Generierung von Orthofoto-Szenerien. Ortho4XP erstellt sowohl Texturen als auch ein Höhenmodell (Mesh) für definierte geografische Ausschnitte („Kacheln") auf Basis öffentlich zugänglicher Fernerkundungsdaten (z. B. SRTM-Höhendaten oder hochauflösende LIDAR-Daten). Unterstützt Zoomstufen bis ZL19 für maximale Detailgenauigkeit.

### Ortho-Streaming

Bei diesem Ansatz werden Orthofoto-Texturen erst zur Laufzeit bei Bedarf von Kartenservern heruntergeladen und über ein virtuelles Dateisystem ([FUSE](../ortho_streaming/how_streaming_works.md)) an X-Plane ausgeliefert. Einmal geladene Kacheln werden in einem lokalen Cache gespeichert; wird das konfigurierte Limit erreicht, werden ältere Kacheln automatisch entfernt. Dieser Ansatz erfordert eine stabile Internetverbindung, ermöglicht aber spontanes Fliegen ohne Vorabgenerierung.

- **[AutoOrtho](../ortho_streaming/autoortho.md)**: Die erste und am weitesten verbreitete Streaming-Lösung für X-Plane. Der aktive [ProgrammingDinosaur Fork](https://github.com/ProgrammingDinosaur/autoortho4xplane) (Version 2.0) bietet eine C-Pipeline für schnelleres Laden, eine moderne GUI und unterstützt Windows, Linux und macOS.

- **[XEarthLayer](../ortho_streaming/xearthlayer.md)**: Eine in Rust geschriebene Alternative mit adaptivem Prefetching, das zwischen bodennahem Ring-Prefetch und Reiseflug-Vorhersage umschaltet. Derzeit nur für Linux und X-Plane 12 verfügbar.

- **[X-Plane Map Enhancement](https://github.com/derekhe/xplane-map-enhancement-release)** (XPME): Eine Streaming-Lösung mit eigener Benutzeroberfläche, die Satellitenbilder direkt auf das Terrain projiziert. Verfügbar für Windows, macOS und Linux (.deb und AppImage).

### Einordnung in der scenery_packs.ini

Alle drei Streaming-Lösungen haben eine Gemeinsamkeit: Ihre Einträge gehören in der `scenery_packs.ini` **ganz nach unten**.

Der Grund liegt in der Prioritätenlogik von X-Plane. Einträge weiter oben in der Datei haben höhere Priorität und werden bevorzugt geladen. Lokale Szenerien — seien es Custom Airports, SimHeaven-Autogen oder lokale Ortho4XP-Kacheln — stehen weiter oben und werden daher immer zuerst verwendet. Nur wenn für einen bestimmten Bereich keine lokale Szenerie existiert, fällt X-Plane auf die weiter unten stehenden Streaming-Einträge zurück und lädt die Satellitenbilder aus dem Internet.

Dieses Fallback-Prinzip hat einen entscheidenden Vorteil: Lokale Kacheln, die man aufwendig in hoher Auflösung generiert hat, werden nie von gestreamten Bildern überschrieben. Gleichzeitig erhält man eine weltweite Abdeckung für alle Gebiete, für die keine lokalen Daten vorhanden sind.

Das folgende Beispiel zeigt eine typische `scenery_packs.ini` am Beispiel von AutoOrtho für Europa:

```ini
# Custom Airports und Landmarks
SCENERY_PACK Custom Scenery/Aerosoft_EDDF_Frankfurt_3_Scenery/
SCENERY_PACK Custom Scenery/X-Plane Landmarks - Paris/

# Standard-Flughäfen
SCENERY_PACK *GLOBAL_AIRPORTS*

# Autogen (SimHeaven X-World)
SCENERY_PACK Custom Scenery/simHeaven_X-World_Europe-6-scenery/
SCENERY_PACK Custom Scenery/simHeaven_X-World_Europe-7-forests/

# Lokale Ortho4XP-Kacheln (optional)
SCENERY_PACK Custom Scenery/zOrtho4XP_+48+011/
SCENERY_PACK Custom Scenery/zOrtho4XP_+47+011/

# Mesh-Dateien
SCENERY_PACK Custom Scenery/SFD_EDDM_Munich_2_Mesh/

# Ortho-Streaming (ganz unten — Fallback für fehlende lokale Daten)
SCENERY_PACK Custom Scenery/yAutoOrtho_Overlays/
SCENERY_PACK Custom Scenery/z_ao_eur/
SCENERY_PACK Custom Scenery/z_autoortho/
```

Bei **XEarthLayer** werden die regionalen Pakete über die CLI installiert (`xearthlayer packages install eu`). Die Einträge verwenden das Präfix `zzXEL_` und stehen ebenfalls am Ende der Datei:

```ini
# XEarthLayer Ortho-Streaming (ganz unten)
SCENERY_PACK Custom Scenery/zzXEL_eu_ortho/
```

**XPME** platziert seine Einträge bei der Installation automatisch in der `scenery_packs.ini`. Das Prinzip ist identisch: Die Streaming-Einträge müssen am Ende stehen, damit lokale Szenerien Vorrang haben.

### Kombination

Für ausgewählte Regionen können die hochauflösenden Ortho4XP-Kacheln mit der globalen Streaming-Abdeckung von AutoOrtho kombiniert werden. Dieses Verfahren wird im Kapitel [AutoOrtho + Ortho4XP](../ortho_streaming/static_plus_streaming.md) detailliert beschrieben.

## Welches System passt zu welchem Spielerprofil?

Die Wahl des geeigneten Systems hängt maßgeblich vom individuellen Flugverhalten ab:

- **Stammflieger** (wiederkehrende Stammflughäfen und -routen): **Statische Generierung** bietet hier den größten Vorteil. Nach einmaliger Generierung der Stammregionen liegen alle Texturen lokal vor. Maximale Qualität ohne Internetabhängigkeit und ohne Latenzschwankungen.

- **Explorativer Spieler** (ständig wechselnde Destinationen): **Streaming-Lösungen** sind die bessere Wahl. Sie eliminieren die zeitintensive Vorab-Generierung und ermöglichen spontanes Anfliegen beliebiger Regionen weltweit. Der Speicherverbrauch bleibt durch automatische Cache-Bereinigung stabil.

- **Hybrider Spieler** (Stammflughäfen + gelegentliche Exploration): Die **[Kombination aus statischer Generierung und Streaming](../ortho_streaming/static_plus_streaming.md)** bietet das Beste aus beiden Welten. Lokale Kacheln für die Stammregionen in höchster Qualität, Streaming für die flexible globale Abdeckung.

---

## Weiterführende Kapitel

| Thema | Seite | Schwerpunkt |
|---|---|---|
| Szenerie-Komponenten | [Wie X-Plane die Welt aufbaut](../aufbau_quellen/scenery_components.md) | Mesh, Ortho, Autogen und ihr Zusammenspiel |
| Szenerie-Quellen | [Szenerien](../aufbau_quellen/scenery_sources.md) | SimHeaven, Freeware und Payware |
| GPU & VRAM | [GPU & VRAM](../../fundamentals/performance/gpu_vram.md) | VRAM-Auswirkungen von Ortho-Texturen |
| Dateisystem | [Dateisystem](../../linux/optimizations/filesystem.md) | Speicher und I/O für Ortho-Daten |
| XOrganizer | [XOrganizer](../../addon/tools/xorganizer.md) | Szenerie-Verwaltung und scenery_packs.ini-Editor |
| XRoad | [XRoad](../../addon/scenery_addons/xroad.md) | Straßennetz-Erweiterung für Szenerien |
