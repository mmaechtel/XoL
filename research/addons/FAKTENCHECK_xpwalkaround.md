# Faktencheck: XP Walkaround (EN + DE)

**Datum:** 2026-02-20
**Geprüfte Seiten:** `docs/en/addon/cockpit/xpwalkaround.md`, `docs/de/addon/cockpit/xpwalkaround.md`
**Primärquelle:** Gumroad-Produktseite (Text vom User bereitgestellt, da WebFetch 403 liefert)
**Sekundärquellen:** x-plane.to, streamlineaddons.com (für SimpleWalkaround)

---

## Ergebnis

Die ursprüngliche Dokumentation beschrieb fast durchgehend Features des **VFRScenery "WalkAround"**-Plugins (X-Plane Store, $19.99), nicht des **clemacamelc "XP Walkaround"**-Plugins (Gumroad). 10 von 16 Behauptungen waren falsch — die Seite wurde komplett neu geschrieben.

### Korrigierte Fehler (10)

| # | Behauptung (alt) | Korrektur | Quelle |
|---|-------------------|-----------|--------|
| 1 | Kompatibilität X-Plane 11, 12 | Nur X-Plane 12 | Gumroad: "X-Plane 12" |
| 2 | "chocks, doors, remove-before-flight tags" | Entfernt — nicht Teil von XP Walkaround | Gumroad: keine Erwähnung |
| 3 | "Door entry/exit" | Entfernt — Walk Mode per Klick/Menü/ESC | Gumroad: "Enter or exit Walk Mode with a single click" |
| 4 | "Interactive elements: Chocks, RBF-tags" | Entfernt — VFRScenery-Feature | Gumroad: keine Erwähnung |
| 5 | "E-key to stand up" | E ist Lean, ESC beendet Walk Mode | Gumroad: "Lean: Q / E", "Exit Walk Mode: ESC" |
| 6 | "spacebar + click interaction" | Entfernt | Gumroad: keine Erwähnung |
| 7 | "AZERTY keyboard support" | Entfernt — nur WASD dokumentiert | Gumroad: "Move: WASD" |
| 8 | "Synchronized footsteps" | Entfernt | Gumroad: keine Erwähnung |
| 9 | "Spawn in front of aircraft" | Ersetzt durch Campsite System | Gumroad: "Spawn a campsite" |
| 10 | "Wide aircraft support: ToLiss, FF..." | Entfernt — VFRScenery-Liste | Gumroad: keine flugzeugspezifische Unterstützung |

### Ergänzte Features (7)

| # | Feature | Quelle |
|---|---------|--------|
| 1 | Flashlight (F-Taste) | Gumroad: "Toggle the flashlight with the F key" |
| 2 | Campsite System (X-Plane 12.04+) | Gumroad: "Campsite System (X-Plane 12.4+)" |
| 3 | Mouse Look (M-Taste) | Gumroad: "Toggle mouse look with the M key" |
| 4 | Lean Q/E, Crouch C, Jump Backspace | Gumroad: Keyboard Shortcuts |
| 5 | ImGui floating window | Gumroad: "Floating, resizable ImGui window" |
| 6 | Gumroad-Lizenzaktivierung | Gumroad: "Built-in Gumroad license activation" |
| 7 | Persistent Settings | Gumroad: "remembers your preferences between sessions" |

### Korrekt (unverändert)

| # | Behauptung | Quelle |
|---|------------|--------|
| 1 | Entwickler: clemacamelc | Gumroad-Seite |
| 2 | Store: Gumroad | Gumroad-Seite + Lizenzaktivierung |
| 3 | Plattformen: Windows, macOS, Linux | Gumroad: "Cross-Plattform compatible: MacOS, Windows & Linux" |
| 4 | First/third-person view (seit v1.5) | Gumroad: "Switch between First-Person or third Person View" |

### SimpleWalkaround (separat verifiziert)

| # | Behauptung | Quelle |
|---|------------|--------|
| 1 | URL forums.x-plane.org/files/file/96508 | x-plane.to, streamlineaddons.com |
| 2 | WASD, Sprint (C), Crouch (X) | x-plane.to, streamlineaddons.com |
| 3 | SASL3-Abhängigkeit entfernt | x-plane.to: v1.5 "fully rewritten without using SASL3" |
