---
description: "ToLiss-Flugzeug-Mods für X-Plane 12: Easy Freighter A321 P2F Frachttür-Umbau und Carda-3D-Triebwerksersatz mit 4K-Texturen in hohem Detailgrad."
---
# ToLiss Mods

Flugzeug-Modifikationen für die ToLiss-Flotte (A319, A320 CEO/NEO, A321 CEO/NEO) — 3D-Modell-Ersetzungen und Umbauten, die über Scripting hinausgehen.

## Easy Freighter — A321 P2F Cargo Door Mod

Simuliert einen A321-Frachter-Umbau (A321P2F/A321PCF). Das Kit ist ein Drag-and-Drop-Objekt für den `objects/`-Ordner des Flugzeugs; die Fracht-Livery muss separat hinzugefügt werden. Eine separate Version existiert auch für den A320. Nicht offiziell von ToLiss genehmigt.

- **Entwickler:** XPJavelin
- **Download:** [forums.x-plane.org](https://forums.x-plane.org/files/file/92976-easy-freighter-conversion-kit-for-the-toliss-321/)

## Carda Realistic Engine Mods

Hochdetaillierte 3D-Triebwerksmodelle von Carda Jowol mit 4K-Texturen, animierter Schubumkehr, Engine-Flex-Animationen und eigenen Partikeleffekten. Verfügbar für A319, A320 CEO/NEO und A321 CEO/NEO. Die Triebwerksmodelle sind kostenlos und plattformunabhängig (OBJ-Dateien im `objects/`-Ordner des Flugzeugs).

Verfügbare Triebwerke: CFM56-5A, CFM56-5B, IAE V2500 (CEO-Varianten), CFM LEAP-1A, PW1100G (NEO-Varianten).

Die Installation erfordert zwei Schritte: Die Engine-OBJ-Dateien von den Threshold-Foren herunterladen und anschließend die `.acf`-Datei patchen, damit sie auf die neuen Modelle verweist. Der **Carda Engine Installer** von Todaloo automatisiert das `.acf`-Patching. Der separate **Carda Engines Mod Fix** von Travis wird empfohlen, um Animationsfehler zu beheben.

- **Triebwerksmod-Entwickler:** Carda Jowol
- **Installer-Entwickler:** iy4vet
- **Engine-Downloads:** [Threshold Forums](https://forum.thresholdx.net/files/category/36-mods/) (kostenlos)
- **Installer-Download:** [forums.x-plane.org](https://forums.x-plane.org/files/file/99205-carda-engine-mod-installer-for-toliss-a319-a320-a321/)

!!! note "Linux: Native Installer-Binary"

    Der Installer enthält eine native Linux-Binary (`install-carda-linux-x64`, auch ARM64). Mit `chmod +x` ausführbar machen und direkt starten. Die Triebwerksmodelle selbst (OBJ/DDS) sind plattformunabhängig. Nach jedem ToLiss-Update muss der Installer erneut ausgeführt werden.
