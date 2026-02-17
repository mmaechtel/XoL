# SimScreen Overlay

SimScreen Overlay ist ein [FlyWithLua](../scripting/flywithlua.md)-Skript, das X-Plane-12-Screenshots mit einem sauberen Fluginformations-Overlay versieht. Das Overlay erscheint nur während der Screenshot-Aufnahme — keine visuelle Störung beim Fliegen.

## Hintergrund

- **Entwickler:** RackhamRPL
- **Download:** [x-plane.to](https://x-plane.to/file/1910/simscreen-overlay)
- **Plattformen:** Windows, macOS, Linux (reines Lua)
- **Kompatibilität:** X-Plane 12
- **Abhängigkeiten:** [FlyWithLua NG+](../scripting/flywithlua.md), SimBrief-Konto (optional, für automatischen Flugdaten-Import)

## Funktionsumfang

- **Screenshot-Overlay:** Fluginformationen (Flugzeugtyp, Abflug, Ankunft) unten links im Screenshot
- **SimBrief-Integration:** Automatischer Import von Flugplandaten über die Pilot-ID
- **Editierbare Felder:** Flugzeugtyp, Abflug-ICAO und Ankunft-ICAO lassen sich manuell eingeben (für VFR oder Flüge ohne SimBrief)
- **Nur bei Aufnahme sichtbar:** Overlay wird nur im Moment des Screenshots aktiviert
- **Einstellungs-UI:** Konfigurierbar über `FlyWithLua Macros > SimScreen Overlay: Settings`

## Mehrwert in der Flugsimulation

Screenshots ohne Kontext verlieren ihre Geschichte — Flugzeugtyp, Route und Bedingungen sind nicht sichtbar. SimScreen Overlay stempelt diese Informationen automatisch auf Screenshots, ohne Nachbearbeitung zu erfordern. Da das Overlay nur bei der Aufnahme erscheint, beeinflusst es das normale Fliegen nicht.

## Installation

**Download:** [x-plane.to](https://x-plane.to/file/1910/simscreen-overlay)

`SimScreenOverlay.lua` in `Resources/plugins/FlyWithLua/Scripts/` ablegen.

Nach der Installation eine Taste für den Befehl `FlyWithLua / SimScreen_Overlay / Screenshot` in den X-Plane-Tastatureinstellungen zuweisen.

## Quellen

- [SimScreen Overlay — x-plane.to](https://x-plane.to/file/1910/simscreen-overlay)
