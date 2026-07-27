---
description: "XGS zeigt Landequalitätsdaten in X-Plane — Sinkrate, G-Kräfte, Mittellinienabweichung und Aufsetzentfernung mit konfigurierbaren Bewertungsskalen."
---
# XGS

XGS (Landing Speed Plugin Reloaded) ist ein eigenständiges [Plugin](../../glossary.md#plugin) von hotbso, das detaillierte Daten zur Landequalität anzeigt — von Sinkrate und G-Kräften über Touchdown-Distanz bis hin zur Centerline-Abweichung.

## Hintergrund

- **Entwickler:** hotbso (Holger Teutsch)
- **Repository:** [github.com/hotbso/xgs](https://github.com/hotbso/xgs) (Open Source, GPL-2.0)
- **Plattformen:** Windows, macOS, Linux (native Binaries)
- **Kompatibilität:** [X-Plane](../../glossary.md#x-plane) 12

XGS ist eine Weiterentwicklung des ursprünglichen Landing Speed Plugins. Die Entwicklung stagniert (letztes Release Juni 2023, letzter Commit Oktober 2024), aber das Plugin funktioniert weiter.

## Funktionsumfang

- **Sinkrate & G-Kräfte:** Maximale Sinkrate (fpm) und maximale G-Kraft bei der Landung
- **Qualitätsbewertung:** Textuelle Bewertung der Landequalität aus konfigurierbarer Datei (z.B. "Smooth landing", "Hard landing, requires inspection")
- **Geschwindigkeit & Pitch:** Angezeigte Fluggeschwindigkeit und Pitch-Winkel beim Aufsetzen; bei ToLiss-Airbus-Modellen wird zusätzlich die VLS neben der IAS angezeigt
- **Schwellenüberflug:** Höhe über der Schwelle und Entfernung von der Schwelle bis zum Aufsetzen
- **Centerline-Abweichung:** Laterale und Winkel-Abweichung von der Bahnmitte
- **ToLiss-Erkennung:** Bei ToLiss-Modellen erkennt XGS den Bodenkontakt über die Kompression der Hauptfahrwerksstreben und meldet zusätzlich die Touchdown-Distanz für das Bugrad

**Konfigurierbare Bewertungsskalen**

XGS liefert eine Standard-Bewertungsskala und eine flugzeugspezifische Skala für Airbus-Typen (basierend auf realen Inspektionsschwellen). Eigene Skalen lassen sich als Textdateien im Flugzeugverzeichnis hinterlegen.

## Mehrwert in der Flugsimulation

Die integrierten X-Plane-Instrumente zeigen nach der Landung keine Detaildaten zur Landequalität. XGS schließt diese Lücke und gibt sofortiges Feedback — nützlich für das Training konsistenter Landungen. Die ToLiss-spezifische Fahrwerkserkennung liefert präzisere Daten als die generische Methode.

## Installation

**Download:** [GitHub Releases](https://github.com/hotbso/xgs/releases)

Die ZIP-Datei nach `Resources/plugins/` entpacken. Es entsteht der Ordner `xgs/` mit der Linux-Binary unter `64/lin.xpl`.

Es werden keine zusätzlichen Systempakete benötigt. Es sind keine Linux-spezifischen Probleme bekannt.

## Quellen

- [XGS — GitHub](https://github.com/hotbso/xgs)
- [XGS — forums.x-plane.org](https://forums.x-plane.org/files/file/45734-landing-speed-plugin-xgs-reloaded/)
