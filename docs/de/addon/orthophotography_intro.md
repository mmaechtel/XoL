# Einführung in die Orthofotographie in der Flugsimulation

Die Orthofotographie stellt einen zentralen Bestandteil moderner Flugsimulationsumgebungen dar, da sie hochauflösende und realistische Bodentexturen ermöglicht. Dieser Abschnitt erläutert die methodischen Ansätze zur Integration qualitativ hochwertiger Orthofotos in die Flugsimulationssoftware X-Plane.

## Bedeutung der Orthofotographie

In der Flugsimulation ist eine präzise Darstellung des Geländes essenziell, um realitätsnahe Lande- und Flugbedingungen zu gewährleisten. X-Plane enthält standardmäßig ein globales Höhenmodell („Mesh"), dessen Auflösung jedoch aufgrund von Speicherbeschränkungen oft begrenzt ist. Dieses Höhenmodell, das im Menü „Komponenten" der Szenerien detailliert beschrieben wird, bildet die Grundlage für die Geländedarstellung. Durch den Einsatz spezifischer Erweiterungen (Add-ons) können sowohl die Präzision des Meshes als auch die Qualität der projizierten Bodentexturen signifikant verbessert werden. Das primäre Ziel besteht in der Erhöhung der topografischen Genauigkeit, wobei die visuelle Optimierung der Szenerie als sekundärer Vorteil resultiert.

## Methoden zur Integration von Orthofotos

Zur Einbindung von Orthofotos in X-Plane haben sich zwei grundlegend verschiedene Ansätze etabliert:

### Statische Generierung

Bei diesem Ansatz werden Orthofoto-Kacheln vor dem Flug vollständig heruntergeladen, in DDS-Texturen konvertiert und dauerhaft auf der lokalen Festplatte gespeichert. X-Plane liest diese Kacheln wie reguläre Szeneriedaten ein — eine Internetverbindung wird zur Laufzeit nicht benötigt. Der Datenbestand muss manuell verwaltet werden und wächst mit jeder generierten Region.

- **[Ortho4XP](ortho4xp.md)**: Das etablierte Werkzeug zur statischen Generierung von Orthofoto-Szenerien. Ortho4XP erstellt sowohl Texturen als auch ein Höhenmodell (Mesh) für definierte geografische Ausschnitte („Kacheln") auf Basis öffentlich zugänglicher Fernerkundungsdaten (z. B. SRTM-Höhendaten oder hochauflösende LIDAR-Daten). Unterstützt Zoomstufen bis ZL19 für maximale Detailgenauigkeit.

### Ortho-Streaming

Bei diesem Ansatz werden Orthofoto-Texturen erst zur Laufzeit bei Bedarf von Kartenservern heruntergeladen und über ein virtuelles Dateisystem (FUSE) an X-Plane ausgeliefert. Einmal geladene Kacheln werden in einem lokalen Cache gespeichert; wird das konfigurierte Limit erreicht, werden ältere Kacheln automatisch entfernt. Dieser Ansatz erfordert eine stabile Internetverbindung, ermöglicht aber spontanes Fliegen ohne Vorabgenerierung.

- **[AutoOrtho](autoortho.md)**: Die erste und am weitesten verbreitete Streaming-Lösung für X-Plane. Der aktive [ProgrammingDinosaur Fork](https://github.com/ProgrammingDinosaur/autoortho4xplane) (Version 2.0) bietet eine C-Pipeline für schnelleres Laden, eine moderne GUI und unterstützt Windows, Linux und macOS.

- **[XEarthLayer](xearthlayer.md)**: Eine in Rust geschriebene Alternative mit adaptivem Prefetching, das zwischen bodennahem Ring-Prefetch und Reiseflug-Vorhersage umschaltet. Derzeit nur für Linux und X-Plane 12 verfügbar.

- **[X-Plane Map Enhancement](https://github.com/derekhe/xplane-map-enhancement-release)** (XPME): Eine Streaming-Lösung mit eigener Benutzeroberfläche, die Satellitenbilder direkt auf das Terrain projiziert. Verfügbar für Windows, macOS und Linux (.deb und AppImage).

### Kombination

Für ausgewählte Regionen können die hochauflösenden Ortho4XP-Kacheln mit der globalen Streaming-Abdeckung von AutoOrtho kombiniert werden. Dieses Verfahren wird im Kapitel [AutoOrtho + Ortho4XP](static_plus_streaming.md) detailliert beschrieben.

## Welches System passt zu welchem Spielerprofil?

Die Wahl des geeigneten Systems hängt maßgeblich vom individuellen Flugverhalten ab:

- **Stammflieger** (wiederkehrende Stammflughäfen und -routen): **Statische Generierung** bietet hier den größten Vorteil. Nach einmaliger Generierung der Stammregionen liegen alle Texturen lokal vor — maximale Qualität ohne Internetabhängigkeit und ohne Latenzschwankungen.

- **Explorativer Spieler** (ständig wechselnde Destinationen): **Streaming-Lösungen** sind die bessere Wahl. Sie eliminieren die zeitintensive Vorab-Generierung und ermöglichen spontanes Anfliegen beliebiger Regionen weltweit. Der Speicherverbrauch bleibt durch automatische Cache-Bereinigung stabil.

- **Hybrider Spieler** (Stammflughäfen + gelegentliche Exploration): Die **[Kombination aus statischer Generierung und Streaming](static_plus_streaming.md)** bietet das Beste aus beiden Welten — lokale Kacheln für die Stammregionen in höchster Qualität, Streaming für die flexible globale Abdeckung.
