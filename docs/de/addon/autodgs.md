# AutoDGS

AutoDGS stellt an über 5.000 Gateway-Flughäfen automatisch ein Docking Guidance System (VDGS oder Marshaller) bereit — ohne dass die Szenerie dafür angepasst sein muss.

## Hintergrund

- **Entwickler:** hotbso (auch Entwickler von openSAM und Better Pushback Mod-Fork)
- **Repository:** [github.com/hotbso/AutoDGS](https://github.com/hotbso/AutoDGS) (Open Source, LGPL-2.1)
- **Plattformen:** Windows, macOS, Linux (native Binaries)
- **Kompatibilität:** [X-Plane](../glossary.md#x-plane) 12
- **Preis:** Kostenlos

AutoDGS wird aktiv gepflegt und erhält regelmäßige Updates. Das [Plugin](../glossary.md#plugin) ist eigenständig und benötigt keine weiteren Plugins.

## Funktionsumfang

- **Automatisches DGS:** Aktiviert sich nach der Landung (Beacon an, Flugzeit erforderlich) und sucht passende Stands in Rollrichtung
- **Zwei DGS-Typen:** Animierter Marshaller (Bodenpersonal) oder elektronisches VDGS (Safedock-Stil mit Azimut- und Distanzanzeige)
- **Vorauswahl-Modus:** Manuelle Stand-Auswahl am Boden
- **SimBrief-Integration:** Zeigt Flugnummer, Ziel und Zeitdaten auf dem VDGS an (erfordert das optionale Plugin [simbrief_hub](https://github.com/hotbso/simbrief_hub))
- **Jetway-Andocken:** Automatische X-Plane-12-Jetway-Animation bei Ankunft
- **Pro-Flughafen-Konfiguration:** GUI-Einstellungen werden lokal gespeichert

## Mehrwert in der Flugsimulation

Standard-Flughäfen ohne Custom-Szenerie haben kein Docking Guidance System. AutoDGS füllt diese Lücke, indem es an jedem Gateway-Flughafen mit Tower und Stands ein VDGS oder einen Marshaller bereitstellt. Das Plugin ergänzt openSAM: AutoDGS übernimmt Default-Flughäfen, openSAM kümmert sich um SAM-fähige Custom-Szenerien. Beide Plugins können parallel betrieben werden — AutoDGS überspringt automatisch Flughäfen mit `sam.xml`.

## Installation

**Download:** [GitHub Releases](https://github.com/hotbso/AutoDGS/releases)

Die ZIP-Datei nach `Resources/plugins/` entpacken. Es entsteht der Ordner `AutoDGS/` mit der Linux-Binary unter `lin_x64/AutoDGS.xpl`.

Es werden keine zusätzlichen Systempakete benötigt. Es sind keine Linux-spezifischen Probleme bekannt. Automatische Updates über den Skunkcrafts Updater werden unterstützt.

## Quellen

- [AutoDGS — GitHub](https://github.com/hotbso/AutoDGS)
- [AutoDGS — forums.x-plane.org](https://forums.x-plane.org/forums/topic/290222-autodgs-dgs-marshaller-or-vdgs-for-every-gateway-airport/)
