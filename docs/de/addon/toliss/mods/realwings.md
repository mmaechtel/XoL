---
description: "RealWings ersetzt den Flügel der ToLiss A319, A320 und A321 komplett — neue Geometrie, 4K-Texturen und Fensterrahmen, mit Linux-Installer."
---
# RealWings

Während der [Durantula-Mod](durantula_wing_mod.md) Teile des Originalflügels überarbeitet, ersetzt RealWings ihn komplett: vollständig neu modellierte Flügelgeometrie einschließlich der Landeklappen, neue 4K-Texturen, ein Substance-3D-Painter-Paintkit für Repainter und optional neue Kabinenfensterrahmen. Der Mod ist rein visuell — er enthält keine Originaldateien von ToLiss und greift nicht in den Systemcode des Flugzeugs ein. Er ist darauf ausgelegt, neben den Carda-Triebwerken (CFM/IAE) zu funktionieren.

## Hintergrund

- **Mod-Entwickler:** GeoBuilds, gemeinsam mit Durantula2405
- **Installer-Entwickler:** iy4vet (aufbauend auf früheren Auto-Installern von alexvor20)
- **Downloads:** [RealWings319](https://forums.x-plane.org/files/file/99042-realwings319-wing-replacement-mod-for-toliss-a319/) · [RealWings320](https://forums.x-plane.org/files/file/99352-realwings320-wing-replacement-mod-for-toliss-a320neo/) · [RealWings321](https://forums.x-plane.org/files/file/99442-realwings321-wing-replacement-mod-for-toliss-a321neoceo/)
- **Installer:** [github.com/iy4vet](https://github.com/iy4vet/xplane-toliss-realwings-installer)
- **Plattformen:** Der Mod selbst besteht aus OBJ- und Texturdaten und ist plattformunabhängig; der Installer bringt native Binaries für Linux, macOS und Windows mit
- **Kompatibilität:** X-Plane 12, ToLiss A319, A320 und A321
- **Lizenz:** Mods als kostenlose Forum-Downloads, Installer unter GPL-3.0

## Abdeckung

Pro Schmalrumpf-Muster gibt es einen eigenen Download, der jeweils die passenden Flügelspitzen-Varianten abdeckt. Es ist immer nur eine Variante aktiv; ein erneuter Lauf des Installers wechselt zwischen ihnen. Ein RealWings340 für die ToLiss A340-600 existiert ebenfalls, ist aber nicht Gegenstand dieser Seite.

| Download | Flugzeug | Varianten |
|----------|----------|-----------|
| RealWings319 | A319 | CEO |
| RealWings320 | A320 | NEO, CEO mit Sharklets, CEO mit Wingtips |
| RealWings321 | A321 | NEO, CEO mit Sharklets, CEO mit Wingtips |

## Mehrwert in der Flugsimulation

Der Flügel ist die größte zusammenhängende Fläche in jeder Außenansicht und in den meisten Kabinenansichten, und die Originalgeometrie von ToLiss fällt gegenüber dem übrigen Modell ab. Weil der Ersatz vollständig statt teilweise erfolgt, bleibt das Ergebnis über alle Flügelspitzen-Varianten hinweg einheitlich, statt neue und alte Detailtiefe auf einer Fläche zu mischen. Der Preis dafür ist die engere Kopplung an alles andere, was die Flügel-OBJs anfasst — Triebwerks-Mods, Lighting-Mods und jeder weitere Flügel-Mod.

## Installation

**Downloads:** siehe oben · **Installer:** [GitHub Releases](https://github.com/iy4vet/xplane-toliss-realwings-installer/releases)

1. Den RealWings-Download in den Flugzeugordner entpacken. Der Installer findet die Quellordner `RealWings3XX/` dort und kopiert sie selbst nach `objects/RealWings3XX/`. Bei A320 und A321 liegen die Daten im Download in den Unterordnern `CEO/` und `NEO/`, die der Installer selbstständig zusammenführt.
2. Den Installer in denselben Ordner legen und starten. Er fragt Flugzeug, Flügelspitzen-Variante und die optionalen Kabinenfensterrahmen ab.

Der Installer tauscht die Original-Flügel-OBJs an den richtigen Stellen gegen die RealWings-Versionen — samt Schattenmodus und Beleuchtungsflags —, entfernt die dadurch überflüssigen Geometrieblöcke (`LIGHT_PARAM`-Blöcke in der Beleuchtungs-OBJ, verwaiste `TRIS` in `Decals.obj` und, bei einem A319 ohne Carda-Mod, in `engines.obj`) und korrigiert die Triebwerkskoordinaten, falls er den Carda-Mod vorfindet. Vor jeder Änderung werden Backups als `*.bak` angelegt; `.acf`-Dateien, die nicht zu X-Plane 12 gehören, werden übersprungen. Eine Deinstallationsfunktion gibt es nicht — der Rückbau erfolgt von Hand über diese Backups, und da der Installer ein vorhandenes `.bak` nie überschreibt, ist ein von einem anderen Flügel-Mod hinterlassenes Backup nicht zwangsläufig der Originalzustand.

Ein Schritt bleibt manuell: Bringt eine Livery eigene RealWings-Texturen mit, ist deren Ordner `objects/RealWings3XX/` in den passenden Livery-Ordner zu kopieren.

!!! note "Linux: Native Installer-Binary"

    Es gibt native Linux-Binaries (`install-realwings-linux-x64` und `-arm64`); `chmod +x`, dann aus dem Flugzeugordner heraus starten. `install_realwings.py` läuft direkt mit Python 3.10+ ohne externe Abhängigkeiten. Nicht-interaktiv über `--aircraft`, `--variant`, `--frames` und `--aircraft-dir`; die Variantenschlüssel lauten `ceo` (nur A319), `ceo-wingtips`, `ceo-sharklets` und `neo`.

!!! warning "Ein ToLiss-Update entfernt den Mod"

    Wie bei jedem Mod, der die Dateien des Flugzeugs bearbeitet, stellt ein Update über den SkunkCraftsUpdater den Originalzustand wieder her — der Installer muss danach erneut laufen.

!!! warning "RealWings und der Durantula-Mod überschneiden sich"

    RealWings überschreibt die Original-Flügel-OBJs nicht, sondern entfernt sie ganz aus der `.acf` — womit die Änderungen des [Durantula-Mods](durantula_wing_mod.md) still wirkungslos werden. Darüber hinaus bearbeiten beide auch `Decals.obj`, die Beleuchtungs-OBJ und die Carda-Triebwerks-OBJs. Keiner der beiden Installer kennt den jeweils anderen — erkannt wird nur der Carda-Mod — und RealWings löscht die überflüssige Carda-„Kit"-Geometrie über Zeilennummern, die ein vorheriger Durantula-Lauf bereits verschoben hat. Die beiden sind als Alternativen zu behandeln, nicht als Stapel.

    Ein Wechsel von Durantula zu RealWings bedeutet deshalb, **zuerst** die Backups `*.durantula.bak` zurückzuspielen — vor allem die der Carda-Triebwerks-OBJs. Durantula hat dort bereits eine `TRIS`-Zeile gelöscht, während RealWings die überflüssige Carda-Geometrie an festen Zeilennummern sucht und damit still den falschen Block aus einer Datei entfernen würde, die eine Zeile kürzer ist als erwartet.

!!! note "Der Lighting-Mod kommt zuletzt"

    [ToLiss Photon](toliss_photon.md) patcht die Lichtobjekte von RealWings, damit die Lichtpositionen zur neuen Geometrie passen. Sein Installer muss deshalb nach diesem laufen — und nach jedem weiteren Lauf noch einmal.

## Quellen

- [RealWings320](https://forums.x-plane.org/files/file/99352-realwings320-wing-replacement-mod-for-toliss-a320neo/) — Flügelersatz-Mod von GeoBuilds (A319- und A321-Version oben verlinkt)
- [xplane-toliss-realwings-installer](https://github.com/iy4vet/xplane-toliss-realwings-installer) — Installer-Quellcode, Binaries und Dokumentation
