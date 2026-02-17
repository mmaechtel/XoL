---
description: "SimReaperXP für X-Plane 12 — FlyWithLua-Skript zur FPS-Steigerung durch selektives Abschalten von Schatten, Licht und Wasserrendering."
---
# SimReaperXP

SimReaperXP ist ein [FlyWithLua](../scripting/flywithlua.md)-Skript, das FPS in X-Plane 12 zurückgewinnt, indem es ressourcenintensive Rendering-Features selektiv deaktiviert. Es bietet umschaltbare Schalter für sechs aufwändige Rendering-Systeme und gewinnt bis zu ~10 FPS (je nach System und Einstellungen) zurück, ohne die Objektdichte zu reduzieren.

## Hintergrund

- **Entwickler:** alstr
- **Repository:** [github.com/alstr/simreaperxp](https://github.com/alstr/simreaperxp) (MIT-Lizenz)
- **Plattformen:** Windows, macOS, Linux (reines Lua)
- **Kompatibilität:** X-Plane 12
- **Abhängigkeit:** [FlyWithLua NG+](../scripting/flywithlua.md)

!!! warning "Offizieller Download nur über GitHub"

    Die Version auf X-Plane.org wird nicht unterstützt und ist veraltet. Der Entwickler hat deren Entfernung beantragt. Nur den [GitHub-Release](https://github.com/alstr/simreaperxp) verwenden.

## Funktionsumfang

- **Shadow Prep:** Entfernt Cockpit-Schattenrendering (enthält Belichtungsanpassung, falls das Cockpit zu hell wird)
- **Cloud Shadow Render:** Stoppt die Berechnung von Wolkenschatten auf dem Boden
- **GBuff Lights:** Deaktiviert Lichtprojektion auf Oberflächen (kann sich nachts automatisch reaktivieren, um dunkle Flughäfen zu verhindern)
- **Planes:** Macht externe Flugzeugmodelle unsichtbar, das Cockpit bleibt funktional (kann sich in Außenansicht automatisch reaktivieren)
- **Water:** Deaktiviert Wasser-Rendering
- **Bump Maps:** Entfernt Oberflächenstrukturtexturen von Objekten

Alle Features sind umschaltbar über `Plugins > FlyWithLua > FlyWithLua Macros > SimReaperXP` oder per Tastenbelegung. Alle Einstellungen sind vollständig reversibel — keine permanenten Dateiänderungen.

## Mehrwert in der Flugsimulation

Leistungshungrige Payware-Flugzeuge (Hot Start CL650, ToLiss A340) an detaillierten Payware-Flughäfen können die Bildraten unter ein komfortables Niveau drücken. SimReaperXP tauscht gezielt visuelle Details gegen signifikante FPS-Gewinne. Da die deaktivierten Features einzeln wählbar sind, lässt sich die eigene Balance zwischen visueller Qualität und Performance finden. Besonders nützlich für IFR-Flüge, bei denen die Außenoptik gegenüber den Cockpitinstrumenten zweitrangig ist.

## Installation

**Download:** [GitHub Releases](https://github.com/alstr/simreaperxp)

`simreaperxp.lua` in `Resources/plugins/FlyWithLua/Scripts/` ablegen.

## Quellen

- [SimReaperXP — GitHub](https://github.com/alstr/simreaperxp)
