---
description: "Dynamic Rain Rate für X-Plane 12 — FlyWithLua-Skript zur geschwindigkeitsabhängigen Anpassung der Regenintensität für realistischere Effekte."
---
# Dynamic Rain Rate

Dynamic Rain Rate ist ein [FlyWithLua](../scripting/flywithlua.md)-Skript, das die Regenintensität in X-Plane 12 dynamisch an die wahre Fluggeschwindigkeit (TAS) des Flugzeugs anpasst. Anstelle einer statischen Regenrate skaliert das Skript den Effekt kontinuierlich, um bei verschiedenen Fluggeschwindigkeiten realistischeren Niederschlag zu erzeugen.

## Hintergrund

- **Entwickler:** GusRodrigues
- **Download:** [X-Plane.org](https://forums.x-plane.org/files/file/97500-dynamic-rain-rate/)
- **Plattformen:** Windows, macOS, Linux (reines Lua)
- **Kompatibilität:** X-Plane 12
- **Abhängigkeit:** [FlyWithLua NG+](../scripting/flywithlua.md)

## Funktionsumfang

- **Geschwindigkeitsproportionaler Regen:** Regenintensität skaliert kontinuierlich mit der wahren Fluggeschwindigkeit (Aktualisierung alle 0,5 Sekunden)
- **Keine manuelle Interaktion:** Vollständig automatisch — läuft ohne Benutzereingabe im Hintergrund
- **Ressourcenschonend:** Minimale Performance-Auswirkung durch niedrige Aktualisierungsfrequenz

## Mehrwert in der Flugsimulation

X-Plane 12 verwendet eine feste Regenrate unabhängig von der Flugzeuggeschwindigkeit, was unrealistisch wirkt — langsames Rollen sieht genauso aus wie schneller Reiseflug. Dynamic Rain Rate koppelt die Regenintensität an die wahre Fluggeschwindigkeit — nach der ausdrücklichen Absicht des Autors wird das Fliegen bei Regen dadurch spürbar anspruchsvoller, nicht bloß ansehnlicher.

## Installation

**Download:** [X-Plane.org](https://forums.x-plane.org/files/file/97500-dynamic-rain-rate/)

Die `.lua`-Datei in `Resources/plugins/FlyWithLua/Scripts/` ablegen.

## Quellen

- [Dynamic Rain Rate — X-Plane.org](https://forums.x-plane.org/files/file/97500-dynamic-rain-rate/)
