# 3D Rain Stop

3D Rain Stop ist ein [FlyWithLua](flywithlua.md)-Skriptpaket, das den 3D-Regenpartikeleffekt bei höheren Geschwindigkeiten oder Flughöhen automatisch deaktiviert. Die fallenden Regenpartikel von X-Plane 12 erzeugen bei hoher Geschwindigkeit einen störenden „Star-Wars-Warp-Speed"-Effekt — die Skripte entfernen diesen, während der Regeneffekt auf der Windschutzscheibe erhalten bleibt.

## Hintergrund

- **Entwickler:** domvc10
- **Download:** [X-Plane.org](https://forums.x-plane.org/files/file/88602-3d-rain-stop-lua-script-xp12/)
- **Plattformen:** Windows, macOS, Linux (reines Lua)
- **Kompatibilität:** X-Plane 12
- **Preis:** Kostenlos
- **Abhängigkeit:** [FlyWithLua NG+](flywithlua.md)

Der Download enthält zwei Skripte — nur eines sollte gleichzeitig aktiv sein:

- **3drainspeedstop.lua** — Deaktiviert 3D-Regen über 100 Knoten, reaktiviert unter 99 Knoten
- **3drainheightstop.lua** — Deaktiviert 3D-Regen über 7.000 ft AGL, reaktiviert unterhalb dieser Höhe

Beide Schwellenwerte lassen sich durch Bearbeiten der Werte in der `.lua`-Datei anpassen.

## Funktionsumfang

- **Geschwindigkeitsbasierte Regensteuerung:** Automatisches Ein/Aus basierend auf der angezeigten Fluggeschwindigkeit
- **Höhenbasierte Regensteuerung:** Alternative Variante mit AGL-Höhe als Auslöser
- **Windschutzscheibe unbeeinflusst:** Deaktiviert nur die fallenden 3D-Regenpartikel — der Regeneffekt auf der Windschutzscheibe bleibt aktiv
- **Editierbare Schwellenwerte:** Geschwindigkeits- und Höhenwerte sind im Skript-Quelltext konfigurierbar

## Mehrwert in der Flugsimulation

Bei Reisegeschwindigkeit rasen die 3D-Regenpartikel von X-Plane 12 unrealistisch über den Bildschirm. Der Effekt ist in großer Höhe rein kosmetisch und lenkt von den Instrumenten ab. 3D Rain Stop entfernt dieses visuelle Artefakt während schneller Flugphasen, während der atmosphärische Regeneffekt bei langsameren Phasen wie Anflug und Rollen erhalten bleibt.

## Installation

**Download:** [X-Plane.org](https://forums.x-plane.org/files/file/88602-3d-rain-stop-lua-script-xp12/)

**Eine** der beiden `.lua`-Dateien in `Resources/plugins/FlyWithLua/Scripts/` ablegen. Nicht beide Skripte gleichzeitig verwenden.

### Linux-Hinweise

Keine Linux-spezifischen Probleme bekannt. Das Skript ist eine reine Lua-Textdatei und läuft auf allen von FlyWithLua unterstützten Plattformen identisch.

## Quellen

- [3D Rain Stop — X-Plane.org](https://forums.x-plane.org/files/file/88602-3d-rain-stop-lua-script-xp12/)
