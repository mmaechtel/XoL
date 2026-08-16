---
description: "Carda Realistic Engine Mods: hochdetaillierte 3D-Triebwerksmodelle für ToLiss A319, A320 und A321 in X-Plane 12 — nativer Linux-Installer für den .acf-Patch."
---
# Carda Realistic Engine Mods

Hochdetaillierte 3D-Triebwerksmodelle von Carda Jowol mit 4K-Texturen, animierter Schubumkehr, Engine-Flex-Animationen und eigenen Partikeleffekten. Verfügbar für A319, A320 CEO/NEO und A321 CEO/NEO. Die Triebwerksmodelle sind kostenlos und plattformunabhängig (OBJ-Dateien im `objects/`-Ordner des Flugzeugs).

Verfügbare Triebwerke: CFM56-5A, CFM56-5B, IAE V2500 (CEO-Varianten), CFM LEAP-1A, PW1100G (NEO-Varianten).

Die Installation erfordert zwei Schritte: Die Engine-OBJ-Dateien von den Threshold-Foren herunterladen und anschließend die `.acf`-Datei patchen, damit sie auf die neuen Modelle verweist. Der **Carda Engine Mod Installer** von iy4vet automatisiert das `.acf`-Patching; ein älterer, separater Installer von Todaloo deckt dasselbe ab. Der separate **Carda Engines Mod Fix** von Travis wird empfohlen, um Animationsfehler zu beheben.

- **Triebwerksmod-Entwickler:** Carda Jowol
- **Installer-Entwickler:** iy4vet
- **Engine-Downloads:** [Threshold Forums](https://forum.thresholdx.net/files/category/36-mods/) (kostenlos)
- **Installer-Download:** [forums.x-plane.org](https://forums.x-plane.org/files/file/99205-carda-engine-mod-installer-for-toliss-a319-a320-a321/)

!!! note "Linux: Native Installer-Binary"

    Der Installer enthält die native Linux-Binary (`install-carda-linux-x64`, auch ARM64). Mit `chmod +x` ausführbar machen und aus dem Flugzeug-Ordner heraus starten. Alternativ lässt sich `install_carda.py` direkt mit Python 3.10+ ausführen, ohne externe Abhängigkeiten. Die Triebwerksmodelle selbst (OBJ/DDS) sind plattformunabhängig. Nach jedem ToLiss-Update muss der Installer erneut ausgeführt werden.

## Quellen

- [Carda Engine Mod Installer](https://forums.x-plane.org/files/file/99205-carda-engine-mod-installer-for-toliss-a319-a320-a321/) — Installer für die Carda-Triebwerksmods
- [Threshold Forums — Mods](https://forum.thresholdx.net/files/category/36-mods/) — Download der Triebwerksmodelle
