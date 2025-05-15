# Einführung in die Orthofotographie in der Flugsimulation

Die Orthofotographie stellt einen zentralen Bestandteil moderner Flugsimulationsumgebungen dar, da sie hochauflösende und realistische Bodentexturen ermöglicht. Dieser Abschnitt erläutert die methodischen Ansätze zur Integration qualitativ hochwertiger Orthofotos in die Flugsimulationssoftware X-Plane.

## Bedeutung der Orthofotographie

In der Flugsimulation ist eine präzise Darstellung des Geländes essenziell, um realitätsnahe Lande- und Flugbedingungen zu gewährleisten. X-Plane enthält standardmäßig ein globales Höhenmodell („Mesh“), dessen Auflösung jedoch aufgrund von Speicherbeschränkungen oft begrenzt ist. Dieses Höhenmodell, das im Menü „Komponenten“ der Szenerien detailliert beschrieben wird, bildet die Grundlage für die Geländedarstellung. Durch den Einsatz spezifischer Erweiterungen (Add-ons) können sowohl die Präzision des Meshes als auch die Qualität der projizierten Bodentexturen signifikant verbessert werden. Das primäre Ziel besteht in der Erhöhung der topografischen Genauigkeit, wobei die visuelle Optimierung der Szenerie als sekundärer Vorteil resultiert.

## Methoden zur Integration von Orthofotos

Zur Implementierung von Orthofotos in X-Plane stehen mehrere Ansätze zur Verfügung:

1. **[Ortho4XP](ortho4xp.md)**: Ein leistungsfähiges Werkzeug zur Generierung von Orthofoto-Szenerien. Ortho4XP erstellt ein Höhenmodell (Mesh) für definierte geografische Ausschnitte („Kacheln“) auf Basis öffentlich zugänglicher Satellitendaten, wie beispielsweise LIDAR-Daten. Die Genauigkeit des Meshes ist anpassbar und kann durch die Verwendung hochauflösender LIDAR-Daten gesteigert werden. Im entsprechenden Kapitel wird neben der Funktionsweise und Bedienung von Ortho4XP auch erläutert, wie solche hochauflösenden Datenquellen genutzt werden können.

2. **[AutoOrtho](autoortho.md)**: Eine innovative Lösung für das dynamische Streaming von Orthofotos. Während Ortho4XP große Datenmengen an Satellitenbildern speichert, verfolgt AutoOrtho einen datensparenden Ansatz, indem die Bilddaten für die Projektion auf das Mesh bedarfsorientiert („on demand“) geladen werden. Dies reduziert den Speicherbedarf erheblich.

3. **[Kombination](autoortho_plus_zortho.md)**: Um die Auflösung von AutoOrtho weiter zu optimieren, können die präziseren Meshes von Ortho4XP mit der Streaming-Technologie von AutoOrtho kombiniert werden. Dieses Verfahren wird in einem spezifischen Kapitel detailliert beschrieben.

Durch die vorgestellten Methoden wird eine flexible und effiziente Integration von Orthofotos in X-Plane ermöglicht, die sowohl die topografische Präzision als auch die visuelle Qualität der Flugsimulation erheblich steigert.