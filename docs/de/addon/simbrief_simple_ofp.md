# SimBrief Simple OFP

SimBrief Simple OFP ist ein [FlyWithLua](flywithlua.md)-Skript, das den aktuellen Flugplan von SimBrief herunterlädt und als lesbaren Operational Flight Plan (OFP) direkt in X-Plane anzeigt.

## Hintergrund

- **Entwickler:** HurricanetwistR
- **Download:** [X-Plane.org](https://forums.x-plane.org/files/file/75422-simbrief-simple-operational-flight-plan-ofp-xp1112/)
- **Plattformen:** Windows, macOS, Linux (reines Lua)
- **Kompatibilität:** X-Plane 11/12
- **Abhängigkeiten:** [FlyWithLua NG+](flywithlua.md), SimBrief-Konto (kostenlos), xml2lua-Bibliothek (im Download enthalten)

Das Skript verbindet sich über den SimBrief-Benutzernamen mit der SimBrief-API, lädt den Flugplan im XML-Format herunter und stellt ihn als formatierten OFP dar. Zwei Layout-Optionen stehen zur Verfügung. Aufruf über `Plugins > FlyWithLua > FlyWithLua Macros`.

## Funktionsumfang

- **SimBrief-API-Integration:** Automatischer Download des zuletzt generierten Flugplans
- **Zwei OFP-Layouts:** Verschiedene Darstellungsformate zur Auswahl
- **METAR-Abkürzungen:** Dekodierte Wetterinformationen im OFP
- **SELCAL-Codes:** SELCAL-Code des Flugzeugs in Layout 1
- **Lokalzeiten:** Lokale Zeitumrechnung für Abflug und Ankunft
- **Mehrere Ausweichflughäfen:** Unterstützung für Flugpläne mit mehreren Alternates

## Mehrwert in der Flugsimulation

Die Anzeige des OFP erfordert normalerweise den Wechsel zum Browser oder zweiten Monitor. SimBrief Simple OFP bringt die wesentlichen Flugplandaten als Overlay in X-Plane — nützlich für den schnellen Blick auf Treibstoffwerte, Routeninformationen und Wetterdaten, ohne den Simulator zu verlassen.

## Installation

**Download:** [X-Plane.org](https://forums.x-plane.org/files/file/75422-simbrief-simple-operational-flight-plan-ofp-xp1112/)

Der Download enthält:

- `SIMBRIEF_SIMPLE_OFP.lua` und `SIMBRIEF_SIMPLE_OFP_Lib.lua` — beide in `Resources/plugins/FlyWithLua/Scripts/` ablegen
- `xml2lua`-Modul — in `Resources/plugins/FlyWithLua/Modules/` ablegen

Vor der ersten Nutzung den SimBrief-Benutzernamen in der Skript-Konfiguration eintragen.

## Quellen

- [SimBrief Simple OFP — X-Plane.org](https://forums.x-plane.org/files/file/75422-simbrief-simple-operational-flight-plan-ofp-xp1112/)
