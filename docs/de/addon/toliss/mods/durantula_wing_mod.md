---
description: "Der Durantula Wing Enhancement MOD überarbeitet Klappen, Klappenschienen-Verkleidungen und Wingflex der ToLiss A319, A320 und A321 — mit Linux-Installer."
---
# Durantula Wing Enhancement MOD

Der Durantula Wing Enhancement MOD überarbeitet Teile des ToLiss-Flügels bei A319, A320 und A321: neue Geometrie für Klappen und Klappenschienen-Verkleidungen sowie einen Wingflex, der auf der eigenen Flügeldurchbiegung von [X-Plane](../../../glossary.md#x-plane) aufsetzt statt auf der Animation, die ToLiss mitbringt. Beide Teile sind unabhängig und lassen sich einzeln oder gemeinsam installieren.

## Hintergrund

- **Mod-Entwickler:** Durantula2405 (3D-Modellierung und Animation: Giorgi_Z4)
- **Installer-Entwickler:** iy4vet
- **Mod-Download:** [forums.x-plane.org](https://forums.x-plane.org/files/file/88518-toliss-a319-a320-and-a321-wing-enhancement-mod/)
- **Installer:** [github.com/iy4vet](https://github.com/iy4vet/xplane-toliss-durantula-installer)
- **Plattformen:** Der Mod selbst besteht aus OBJ- und Texturdaten und ist plattformunabhängig; der Installer bringt native Binaries für Linux, macOS und Windows mit
- **Kompatibilität:** X-Plane 12, ToLiss A319, A320 und A321
- **Lizenz:** Mod als kostenloser Forum-Download, Installer unter GPL-3.0

Der Mod ist rein visuell — er ändert Geometrie, Texturen und Animationen, nicht die Systeme des Flugzeugs.

## Funktionsumfang

- **Klappen:** Ersetzt die Original-Klappen und Klappenschienen-Verkleidungen in den Flügel-OBJs durch neue Meshes mit eigenen Texturen. Bei CEO-Mustern wird zusätzlich die überflüssige Triebwerks-„Kit"-Geometrie entfernt, die sich mit den neuen Verkleidungen überschneidet: aus den Carda-Triebwerks-OBJs, falls installiert, sonst aus der Original-`engines.obj`
- **Wingflex:** Ersetzt die ToLiss-eigenen Winglet-Flex-Animationen in den Flügel-, Glas-, Decal-, Beleuchtungs- und Partikel-OBJs durch die X-Plane-native `wing_tip_deflection_deg`-Animation und setzt die Flügel-Dämpfungswerte in der `.acf`
- **Paintkit:** Ein optionales Set „New Wing Textures" liegt bei; die fertige Livery kommt von Hand in den `liveries/`-Ordner des Flugzeugs

Die beiden Teile hängen enger zusammen, als die getrennte Installation vermuten lässt: Das neue Klappen-Mesh ist flach modelliert und legt sich erst über die Wingflex-Animation an den Flügel an. Der Installer wählt deshalb das flexende Mesh, wenn der Wingflex mitinstalliert wird, und sonst das statische.

## Mehrwert in der Flugsimulation

Klappen und Klappenschienen-Verkleidungen liegen im Anflug und nach der Landung genau dort, wohin der Blick geht, und die Originalgeometrie ist der gröbste Teil des ToLiss-Außenmodells. Die größere Änderung ist der Wingflex: Die native Durchbiegung von X-Plane reagiert auf Last und Turbulenz, statt eine feste Animation abzuspielen — der Flügel bewegt sich im ruppigen Anflug also anders als im ruhigen. Am Flugverhalten ändert keiner der beiden Teile etwas.

## Installation

**Download:** [forums.x-plane.org](https://forums.x-plane.org/files/file/88518-toliss-a319-a320-and-a321-wing-enhancement-mod/) · **Installer:** [GitHub Releases](https://github.com/iy4vet/xplane-toliss-durantula-installer/releases)

Den Mod von Hand zu installieren bedeutet, OBJ-Dateien im Texteditor und die `.acf` im Plane Maker zu bearbeiten. Der Installer automatisiert all diese Eingriffe:

1. Den Mod-Download entpacken — es entstehen Ordner mit den Namen `Durantula_ToLiss_New_Flaps_*`, `Durantula_ToLiss_Wingflex_*` sowie ein Handbuch.
2. Diese Ordner **und** den Installer in den Flugzeugordner legen, neben die `.acf`-Datei. Von Hand wird nichts kopiert; der Installer holt sich OBJs und Texturen selbst aus den Mod-Ordnern. Mit `--mod-dir` lässt er sich auf einen anderen Ort verweisen.
3. Den Installer aus diesem Ordner heraus starten. Er fragt Flugzeug und zu installierende Teile ab — und bei einem A319 oder A320 mit beiden Triebwerksfamilien zusätzlich das gewünschte Klappen-Mesh.

Die Triebwerksfamilie liest der Installer selbst aus der `.acf`. Er sucht nach Geometrie- und Animations-Inhalten statt nach Zeilennummern und funktioniert deshalb auch dann, wenn andere Mods — die Carda-Triebwerke oder ein Lighting-Mod — die Zeilennummerierung verschoben haben; mehrfaches Ausführen ist unbedenklich. Vor jeder Dateiänderung werden Backups als `*.durantula.bak` angelegt. Lässt sich die Original-Klappengeometrie nicht entfernen, bricht der Installer ab, statt die neuen Klappen darüberzulegen.

!!! note "Linux: Native Installer-Binary"

    Es gibt native Linux-Binaries (`install-durantula-linux-x64`, auch ARM64). Mit `chmod +x` ausführbar machen und aus dem Flugzeugordner heraus starten, alternativ `install_durantula.py` direkt mit Python 3.10+ ausführen — ohne externe Abhängigkeiten. Beide akzeptieren `--aircraft`, `--parts`, `--flaps-engine`, `--textures`, `--mod-dir` und `--aircraft-dir` für eine vollständig nicht-interaktive Installation, was sich lohnt: Der Mod muss regelmäßig neu installiert werden.

!!! warning "Ein ToLiss-Update entfernt den Mod"

    Ein Update über den SkunkCraftsUpdater stellt die Originaldateien wieder her, der Installer muss danach jedes Mal erneut laufen. Wiederholte Läufe sind harmlos — der Installer erkennt bereits erledigte Arbeit und legt weder Objekte doppelt an noch löscht er zu viel Geometrie. Die Backups `*.durantula.bak` erlauben jederzeit eine Rückkehr zum Ausgangszustand; das Suffix ist mod-spezifisch und kollidiert deshalb nie mit den `.bak`-Dateien anderer Mods oder des SkunkCraftsUpdaters. Eine Deinstallationsfunktion gibt es nicht — der Weg zurück führt über diese Backups.

!!! warning "RealWings und der Durantula-Mod überschneiden sich"

    Beide Mods greifen auf dieselben Dateien zu, und [RealWings](realwings.md) entfernt die Original-Flügel-OBJs ganz aus der `.acf` — womit die Änderungen dieses Mods still wirkungslos werden. Darüber hinaus bearbeiten beide auch `Decals.obj`, die Beleuchtungs-OBJ und die Carda-Triebwerks-OBJs, und keiner der beiden Installer kennt den jeweils anderen — erkannt wird nur der Carda-Mod. Die beiden sind als Alternativen zu behandeln, nicht als Stapel.

    Wer von RealWings kommt, spielt **zuerst** dessen `*.bak`-Backups zurück — insbesondere das der `.acf`. RealWings verschiebt die Carda-Triebwerkskoordinaten passend zum eigenen Flügel, und dieser Installer setzt sie nicht zurück.

!!! note "Der Lighting-Mod kommt zuletzt"

    [ToLiss Photon](toliss_photon.md) spielt eine Lichtvariante ein, die zu dem tatsächlich gezeichneten Flügel passt; sein Installer muss deshalb nach diesem laufen — und nach jedem weiteren Lauf noch einmal.

## Quellen

- [Toliss A319, A320 and A321 — Wing Enhancement MOD](https://forums.x-plane.org/files/file/88518-toliss-a319-a320-and-a321-wing-enhancement-mod/) — Mod von Durantula2405
- [xplane-toliss-durantula-installer](https://github.com/iy4vet/xplane-toliss-durantula-installer) — Installer-Quellcode, Binaries und Dokumentation
