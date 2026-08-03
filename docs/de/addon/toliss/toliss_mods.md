---
description: "ToLiss-Flugzeug-Mods für X-Plane 12: Easy Freighter A321 P2F Frachttür-Umbau, Carda-3D-Triebwerksersatz, der Durantula-Flügelmod mit neuen Klappen und nativem Wingflex sowie der Flügelersatz RealWings."
---
# ToLiss Mods

Flugzeug-Modifikationen für die ToLiss-Flotte (A319, A320 CEO/NEO, A321 CEO/NEO) — 3D-Modell-Ersetzungen und Umbauten, die über Scripting hinausgehen.

## Easy Freighter — A321 P2F Cargo Door Mod

Simuliert einen A321-Frachter-Umbau (A321P2F/A321PCF). Das Kit ist ein Drag-and-Drop-Objekt für den `objects/`-Ordner des Flugzeugs; die Fracht-Livery muss in ihrer `livery.tlscfg` die Zeilen `external_Extras = YES` und `custom_Cabin = F` enthalten. Eine Demo-Livery liegt bei. Eine separate Version existiert auch für den A320. Nicht offiziell von ToLiss genehmigt.

- **Entwickler:** XPJavelin
- **Download:** [forums.x-plane.org](https://forums.x-plane.org/files/file/92976-easy-freighter-conversion-kit-for-the-toliss-321/)

## Carda Realistic Engine Mods

Hochdetaillierte 3D-Triebwerksmodelle von Carda Jowol mit 4K-Texturen, animierter Schubumkehr, Engine-Flex-Animationen und eigenen Partikeleffekten. Verfügbar für A319, A320 CEO/NEO und A321 CEO/NEO. Die Triebwerksmodelle sind kostenlos und plattformunabhängig (OBJ-Dateien im `objects/`-Ordner des Flugzeugs).

Verfügbare Triebwerke: CFM56-5A, CFM56-5B, IAE V2500 (CEO-Varianten), CFM LEAP-1A, PW1100G (NEO-Varianten).

Die Installation erfordert zwei Schritte: Die Engine-OBJ-Dateien von den Threshold-Foren herunterladen und anschließend die `.acf`-Datei patchen, damit sie auf die neuen Modelle verweist. Der **Carda Engine Mod Installer** von iy4vet automatisiert das `.acf`-Patching; ein älterer, separater Installer von Todaloo deckt dasselbe ab. Der separate **Carda Engines Mod Fix** von Travis wird empfohlen, um Animationsfehler zu beheben.

- **Triebwerksmod-Entwickler:** Carda Jowol
- **Installer-Entwickler:** iy4vet
- **Engine-Downloads:** [Threshold Forums](https://forum.thresholdx.net/files/category/36-mods/) (kostenlos)
- **Installer-Download:** [forums.x-plane.org](https://forums.x-plane.org/files/file/99205-carda-engine-mod-installer-for-toliss-a319-a320-a321/)

!!! note "Linux: Native Installer-Binary"

    Der Installer enthält die native Linux-Binary (`install-carda-linux-x64`, auch ARM64). Mit `chmod +x` ausführbar machen und aus dem Flugzeug-Ordner heraus starten. Alternativ lässt sich `install_carda.py` direkt mit Python 3.10+ ausführen, ohne externe Abhängigkeiten. Die Triebwerksmodelle selbst (OBJ/DDS) sind plattformunabhängig. Nach jedem ToLiss-Update muss der Installer erneut ausgeführt werden.

## Durantula Wing Enhancement MOD

Neue Klappen- und Klappenträger-Geometrie sowie eine native Wingflex-Animation für A319, A320 und A321. Der Mod besteht aus zwei unabhängigen Teilen, die sich einzeln oder gemeinsam installieren lassen:

- **Klappen** — ersetzt die Original-Landeklappen und Klappenschienen-Verkleidungen in den Flügel-OBJs durch neue Meshes mit eigenen Texturen. Bei CEO-Mustern wird zusätzlich die überflüssige Triebwerks-„Kit"-Geometrie entfernt, die sich mit den neuen Verkleidungen überschneidet: aus den Carda-Triebwerks-OBJs, falls installiert, sonst aus der Original-`engines.obj`
- **Wingflex** — ersetzt die ToLiss-eigenen Winglet-Flex-Animationen in den Flügel-, Glas-, Decal-, Licht- und Partikel-OBJs durch die X-Plane-native `wing_tip_deflection_deg`-Animation und setzt die Flügel-Dämpfungswerte in der `.acf`

Ein optionales Paintkit „New Wing Textures" liegt bei; die fertige Livery kommt von Hand in den `liveries/`-Ordner des Flugzeugs.

Von Hand installiert bedeutet der Mod, OBJ-Dateien im Texteditor und die `.acf` im Plane Maker zu bearbeiten. Der **Durantula Wing Mod Installer** von iy4vet automatisiert all diese Eingriffe. Er sucht nach Geometrie- und Animations-Inhalten statt nach Zeilennummern und funktioniert deshalb auch dann, wenn andere Mods — die Carda-Triebwerke oder ein Lighting-Mod — die Zeilennummerierung verschoben haben; mehrfaches Ausführen ist unbedenklich. Vor jeder Dateiänderung werden Backups als `*.durantula.bak` angelegt, die Triebwerksfamilie liest der Installer selbst aus der `.acf`.

- **Mod-Entwickler:** Durantula2405 (3D-Modellierung und Animation: Giorgi_Z4)
- **Installer-Entwickler:** iy4vet
- **Mod-Download:** [forums.x-plane.org](https://forums.x-plane.org/files/file/88518-toliss-a319-a320-and-a321-wing-enhancement-mod/)
- **Installer:** [github.com/iy4vet](https://github.com/iy4vet/xplane-toliss-durantula-installer) (GPL-3.0, mit vorkompilierten Binaries)

!!! note "Linux: Native Installer-Binary"

    Es gibt eine native Linux-Binary (`install-durantula-linux-x64`, auch ARM64). Mit `chmod +x` ausführbar machen und aus dem Flugzeug-Ordner heraus starten, alternativ `install_durantula.py` direkt mit Python 3.10+ ausführen — ohne externe Abhängigkeiten. Beide akzeptieren `--aircraft`, `--parts`, `--flaps-engine` und `--textures` für eine vollständig nicht-interaktive Installation. Ein ToLiss-Update über den SkunkCraftsUpdater stellt die Originaldateien wieder her, der Installer muss danach erneut laufen.

## RealWings

Während der Durantula-Mod Teile des Originalflügels überarbeitet, ersetzt RealWings ihn komplett: neu modellierte Flügelgeometrie mit neuen 4K-Texturen, ein Substance-3D-Painter-Paintkit für Repainter und als Dreingabe neue Fensterrahmen. Der Mod ist rein visuell — er enthält keine Originaldateien von ToLiss und greift nicht in den Systemcode des Flugzeugs ein. Er ist darauf ausgelegt, neben den Carda-Triebwerken (CFM/IAE) zu bestehen.

Pro Schmalrumpf-Muster gibt es einen eigenen Download, der jeweils die passenden Flügelspitzen-Varianten abdeckt (ein RealWings340 für die ToLiss A340-600 existiert ebenfalls, liegt aber außerhalb dieser Seite):

| Download | Flugzeug | Varianten |
|----------|----------|-----------|
| RealWings319 | A319 | CEO |
| RealWings320 | A320 | NEO, CEO mit Sharklets, CEO mit Wingtips |
| RealWings321 | A321 | NEO, CEO mit Sharklets, CEO mit Wingtips |

Der Installer — wieder von iy4vet — tauscht die Original-Flügel-OBJs an den richtigen Stellen gegen die RealWings-Versionen, entfernt die dadurch überflüssigen Geometrieblöcke und korrigiert die Triebwerkskoordinaten, falls er den Carda-Mod vorfindet. Es ist immer nur eine Flügelspitzen-Variante aktiv; ein erneuter Lauf wechselt zwischen ihnen. Bei A320 und A321 enthält der Download verschachtelte `CEO/`- und `NEO/`-Ordner, die der Installer selbstständig zusammenführt. Ein Schritt bleibt manuell: Bringt eine Livery eigene RealWings-Texturen mit, ist deren Ordner `objects/RealWings3XX/` in den passenden Livery-Ordner zu kopieren.

- **Mod-Entwickler:** GeoBuilds, gemeinsam mit Durantula2405
- **Installer-Entwickler:** iy4vet
- **Downloads:** [RealWings319](https://forums.x-plane.org/files/file/99042-realwings319-wing-replacement-mod-for-toliss-a319/) · [RealWings320](https://forums.x-plane.org/files/file/99352-realwings320-wing-replacement-mod-for-toliss-a320neo/) · [RealWings321](https://forums.x-plane.org/files/file/99442-realwings321-wing-replacement-mod-for-toliss-a321neoceo/)
- **Installer:** [github.com/iy4vet](https://github.com/iy4vet/xplane-toliss-realwings-installer) (GPL-3.0, mit vorkompilierten Binaries)

!!! note "Linux: Native Installer-Binary"

    Wie bei den beiden anderen Installern gibt es native Linux-Binaries (`install-realwings-linux-x64` und `-arm64`); `chmod +x`, dann aus dem Flugzeug-Ordner heraus starten. `install_realwings.py` läuft direkt mit Python 3.10+ ohne externe Abhängigkeiten. Nicht-interaktiv über `--aircraft`, `--variant`, `--frames` und `--aircraft-dir`.

!!! warning "RealWings und Durantula-Mod überschneiden sich"

    Beide Mods greifen auf dieselben Dateien zu. RealWings überschreibt die Original-Flügel-OBJs nicht, sondern entfernt sie ganz aus der `.acf` — womit die Änderungen des Durantula-Mods still wirkungslos werden; darüber hinaus bearbeiten beide auch `Decals.obj`, die Beleuchtungs-OBJ und die Carda-Triebwerks-OBJs. Keiner der beiden Installer kennt den jeweils anderen — erkannt wird nur der Carda-Mod — und RealWings löscht die überflüssige Carda-„kit"-Geometrie über Zeilennummern, die ein vorheriger Durantula-Lauf bereits verschoben hat. Die beiden sind als Alternativen zu behandeln, nicht als Stapel.

## Quellen

- [Toliss A319, A320 and A321 — Wing Enhancement MOD](https://forums.x-plane.org/files/file/88518-toliss-a319-a320-and-a321-wing-enhancement-mod/) — Mod von Durantula2405
- [RealWings320](https://forums.x-plane.org/files/file/99352-realwings320-wing-replacement-mod-for-toliss-a320neo/) — Flügelersatz-Mod von GeoBuilds (A319- und A321-Version oben verlinkt)
- [xplane-toliss-realwings-installer](https://github.com/iy4vet/xplane-toliss-realwings-installer) — Installer-Quellcode, Binaries und Dokumentation
- [xplane-toliss-durantula-installer](https://github.com/iy4vet/xplane-toliss-durantula-installer) — Installer-Quellcode, Binaries und Dokumentation
- [Carda Engine Mod Installer](https://forums.x-plane.org/files/file/99205-carda-engine-mod-installer-for-toliss-a319-a320-a321/) — Installer für die Carda-Triebwerksmods
- [Easy Freighter Conversion Kit](https://forums.x-plane.org/files/file/92976-easy-freighter-conversion-kit-for-the-toliss-321/) — A321-P2F-Frachttür-Mod
