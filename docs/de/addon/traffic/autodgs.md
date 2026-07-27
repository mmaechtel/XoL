---
description: "AutoDGS bietet automatische Andockführung per VDGS oder Marshaller an über 5.000 X-Plane-Gateway-Flughäfen — ohne Szenerie-Anpassungen."
---
# AutoDGS

AutoDGS stellt an über 5.000 Gateway-Flughäfen automatisch ein Docking Guidance System (VDGS oder Marshaller) bereit — ohne dass die Szenerie dafür angepasst sein muss.

## Hintergrund

- **Entwickler:** hotbso (auch Entwickler von [openSAM](opensam.md) und [Better Pushback](betterpushback.md) Mod-Fork)
- **Repository:** [github.com/hotbso/AutoDGS](https://github.com/hotbso/AutoDGS) (Open Source; Code LGPL-2.1, 3D-Objekte/Texturen CC-BY, Safedock-T2-24-VDGS CC BY-NC-SA)
- **Plattformen:** Windows, macOS, Linux (native Binaries)
- **Kompatibilität:** [X-Plane](../../glossary.md#x-plane) 11 und 12 — unter X-Plane 12 ist jedoch [openSAM](opensam.md) v5.x der gepflegte Weg, in das AutoDGS eingegliedert wurde. Das eigenständige AutoDGS ist die Legacy-Linie (XP11 über die eingefrorene 4.x-Version)

!!! warning "Veraltet — in openSAM eingegliedert"

    Die AutoDGS-Funktionalität wurde in [openSAM](opensam.md) v5.x überführt. Das eigenständige Plugin gilt als veraltet und wird nicht mehr unterstützt (Support nur noch über Discord). Unter X-Plane 12 ersetzt openSAM v5.x das eigenständige AutoDGS.

Das [Plugin](../../glossary.md#plugin) ist eigenständig und benötigt keine weiteren Plugins.

## Funktionsumfang

- **Automatisches DGS:** Aktiviert sich nach der Landung (Beacon muss an sein) und sucht passende Stands in Rollrichtung
- **Zwei DGS-Typen:** Animierter Marshaller (Bodenpersonal) oder elektronisches VDGS (Safedock-Stil mit Azimut- und Distanzanzeige)
- **Vorauswahl-Modus:** Manuelle Stand-Auswahl am Boden
- **SimBrief-Integration:** Zeigt Flugnummer, Ziel und Zeitdaten auf dem VDGS an (erfordert das optionale Plugin [simbrief_hub](../toliss/toliss_ecosystem.md#simbrief_hub))
- **Jetway-Andocken:** Automatische X-Plane-12-Jetway-Animation bei Ankunft
- **Pro-Flughafen-Konfiguration:** GUI-Einstellungen werden lokal gespeichert

## Mehrwert in der Flugsimulation

Standard-Flughäfen ohne Custom-Szenerie haben kein Docking Guidance System. AutoDGS füllt diese Lücke, indem es an jedem Gateway-Flughafen mit Tower und Stands ein VDGS oder einen Marshaller bereitstellt. Unter X-Plane 12 ist diese Funktionalität inzwischen Teil von [openSAM](opensam.md) v5.x, das sowohl Default-/Gateway-Flughäfen als auch SAM-fähige Custom-Szenerien aus einem einzigen Plugin abdeckt. Das frühere Modell, eigenständiges AutoDGS parallel zu openSAM zu betreiben — wobei AutoDGS Flughäfen mit `sam.xml` überspringt — ist Legacy.

## Installation

**Download:** [GitHub Releases](https://github.com/hotbso/AutoDGS/releases)

Die ZIP-Datei nach `Resources/plugins/` entpacken. Es entsteht der Ordner `AutoDGS/` mit der Linux-Binary unter `lin_x64/AutoDGS.xpl`.

Es werden keine zusätzlichen Systempakete benötigt. Es sind keine Linux-spezifischen Probleme bekannt. Automatische Updates über den [SkunkCrafts Updater](../tools/skunkcrafts_updater.md) werden unterstützt.

## Quellen

- [AutoDGS — GitHub](https://github.com/hotbso/AutoDGS)
- [AutoDGS — forums.x-plane.org](https://forums.x-plane.org/forums/topic/290222-autodgs-dgs-marshaller-or-vdgs-for-every-gateway-airport/)
