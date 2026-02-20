---
description: "XP Walkaround für X-Plane 12 — First-Person-Walkaround mit Taschenlampe, Campsite-System und Mouse Look. Natives Linux-Plugin mit SimpleWalkaround als kostenlose Alternative."
---
# XP Walkaround

XP Walkaround ist ein kommerzielles [Plugin](../../glossary.md#plugin) für [X-Plane](../../glossary.md#x-plane) 12, das First-Person-Bewegung außerhalb des Cockpits ermöglicht — um das Flugzeug herumgehen, die Flughafenumgebung erkunden und das Vorfeld nachts mit integrierter Taschenlampe inspizieren. Das Plugin läuft nativ unter Linux.

## Hintergrund

- **Entwickler:** clemacamelc
- **Store:** [Gumroad](https://clemacamelc.gumroad.com/l/xpwalkaround) (kommerziell)
- **Plattformen:** Windows, macOS, Linux
- **Kompatibilität:** X-Plane 12

Das Plugin liefert native Binaries für alle drei Plattformen — unter Linux sind keine zusätzlichen Systempakete oder Abhängigkeiten erforderlich.

## Funktionsumfang

- **Walk Mode:** Das Cockpit verlassen und sich frei um das Flugzeug und den Flughafen bewegen. Aktivierung über das Plugin-Fenster, das Plugins-Menü oder ESC-Taste.
- **Erst-/Drittperson-Ansicht:** Wechsel zwischen Erst- und Drittperson-Perspektive
- **Mouse Look:** Mit M-Taste umschalten für natürliches Umsehen beim Gehen. Optionale invertierte Y-Achse. Bei deaktiviertem Mouse Look bleibt X-Planes Standard-Rechtsklick-Kamera erhalten.
- **Taschenlampe:** Mit F-Taste umschalten für dunkle Cockpits, Kabinen und nächtliche Vorfeld-Inspektionen. Lautstärke über Plugin-Einstellungen regelbar.
- **Campsite-System:** Lagerplatz mit Lagerfeuer vor der aktuellen Blickrichtung aufstellen (erfordert X-Plane 12.04+). Aufbau, Abbruch oder Abbau über die Benutzeroberfläche. Konzipiert für Bush Flying und abgelegene Landeplätze.
- **Steuerung:** WASD-Bewegung, Q/E Neigen, C Ducken, Backspace Springen, ESC Walk Mode beenden
- **Plugin-Fenster:** Schwebendes, größenveränderbares ImGui-Fenster über das Plugins-Menü erreichbar. Optionale automatische Anzeige beim Start.
- **Persistente Einstellungen:** Augenhöhe, Lautstärke, Maus-Invertierung und Fenster-Einstellungen werden zwischen Sitzungen gespeichert

## Mehrwert in der Flugsimulation

Statt an die Cockpit-Kamera gebunden zu sein, lässt sich das Flugzeug umrunden und die Flughafenumgebung erkunden. Die Taschenlampe ermöglicht nächtliche Inspektionen von Cockpits und Frachträumen. Das Campsite-System schafft Atmosphäre für Bush Flying an abgelegenen Pisten. Anders als viele kommerzielle X-Plane-Addons enthält das Plugin ein natives Linux-Binary und funktioniert ohne Kompatibilitätsschichten oder Workarounds.

## Installation

**Download:** [Gumroad](https://clemacamelc.gumroad.com/l/xpwalkaround)

Als Standalone-Plugin nach `Resources/plugins/` installieren. Nach dem ersten Start den Gumroad-Lizenzschlüssel im Plugin-Fenster aktivieren. Unter Linux sind keine zusätzlichen Systempakete oder Konfigurationen erforderlich.

!!! tip "Linux-Kompatibilität"

    XP Walkaround funktioniert ohne Einschränkungen unter Linux. Keine zusätzliche Konfiguration oder Workarounds erforderlich.

## Kostenlose Alternative: SimpleWalkaround

[SimpleWalkaround](https://forums.x-plane.org/files/file/96508-simplewalkaround/) ist ein kostenloses Plugin mit ähnlicher Walkaround-Funktionalität. Es nutzt WASD-Bewegungssteuerung, Sprint (C) und Ducken (X). Die frühere SASL3-Abhängigkeit wurde inzwischen entfernt.

## Quellen

- [XP Walkaround — Gumroad](https://clemacamelc.gumroad.com/l/xpwalkaround)
- [SimpleWalkaround — forums.x-plane.org](https://forums.x-plane.org/files/file/96508-simplewalkaround/)
