# ToLiss Mods

Flugzeug-Modifikationen für die ToLiss-Flotte (A319, A320 CEO/NEO, A321 CEO/NEO) — 3D-Modell-Ersetzungen und Umbauten, die über Scripting hinausgehen.

## Easy Freighter — A321 P2F Cargo Door Mod

Simuliert eine Cargo-Haupttür für den A321P2F/A321PCF mit rigider Cargo-Barriere und Fenster-Plugs als FlyWithLua-Objekt. Enthält Liveries für Frachtfluggesellschaften. Eine separate Version existiert auch für den A320. Nicht offiziell von ToLiss genehmigt.

- **Entwickler:** XPJavelin
- **Download:** [forums.x-plane.org](https://forums.x-plane.org/files/file/92976-easy-freighter-conversion-kit-for-the-toliss-321/)

## Carda Realistic Engine Mods

Hochdetaillierte 3D-Triebwerksmodelle von Carda Jowol mit 4K-Texturen, animierter Schubumkehr, Engine-Flex-Animationen und eigenen Partikeleffekten. Verfügbar für A319, A320 CEO/NEO und A321 CEO/NEO. Die Triebwerksmodelle sind kostenlos und plattformunabhängig (OBJ-Dateien im `objects/`-Ordner des Flugzeugs).

Verfügbare Triebwerke: CFM56-5A, CFM56-5B, IAE V2500 (CEO-Varianten), CFM LEAP-1A, PW1100G (NEO-Varianten).

Die Installation erfordert zwei Schritte: Die Engine-OBJ-Dateien von den Threshold-Foren herunterladen und anschließend die `.acf`-Datei patchen, damit sie auf die neuen Modelle verweist. Der **Carda Engine Installer** von Todaloo automatisiert das `.acf`-Patching. Der separate **Carda Engines Mod Fix** von Travis wird empfohlen, um Animationsfehler zu beheben.

- **Triebwerksmod-Entwickler:** Carda Jowol
- **Installer-Entwickler:** Todaloo
- **Engine-Downloads:** [Threshold Forums](https://forum.thresholdx.net/files/category/36-mods/) (kostenlos)
- **Installer-Download:** [forums.x-plane.org](https://forums.x-plane.org/files/file/94704-carda-engine-installer-for-toliss-a320-family/)
- **Mod-Fix-Download:** [Threshold Forums](https://forum.thresholdx.net/files/file/3685-carda-engines-mod-fix-for-toliss-airbus/)

!!! warning "Linux: Installer ist Windows-only"

    Der Carda Engine Installer ist eine Windows-`.exe`. Unter Linux lässt er sich in einer [KVM](../../linux/extensions/kvm.md)-Windows-VM ausführen. Die Triebwerksmodelle selbst (OBJ/DDS) sind plattformunabhängig und funktionieren unter Linux ohne Anpassung. Nach jedem ToLiss-Update muss der Patch erneut angewendet werden.
