---
description: "openSAM ist ein freier Open-Source-Ersatz für das SAM-Plugin — steuert animierte Fluggastbrücken, VDGS und Marshaller in X-Plane-Szenerien."
---
# openSAM

openSAM ist ein Open-Source-Ersatz für das kommerzielle SAM-[Plugin](../../glossary.md#plugin) (Scenery Animation Manager) von Stairport. Es steuert animierte Jetways, VDGS, Marshallers und Custom-Animationen in SAM-fähigen Custom-Szenerien.

## Hintergrund

- **Entwickler:** hotbso (auch Entwickler von [AutoDGS](autodgs.md))
- **Repository:** [github.com/hotbso/openSAM](https://github.com/hotbso/openSAM) (Open Source; Code LGPL-2.1, Assets/VDGS CC-BY und CC BY-NC-SA)
- **Plattformen:** Windows, macOS, Linux (native Binaries)
- **Kompatibilität:** nur [X-Plane](../../glossary.md#x-plane) 12 — das aktuelle openSAM (v5.x) läuft ausschließlich unter XP12. XP11-Nutzer müssen bei einer Legacy-4.x-Version bleiben, die nicht mehr aktiv weiterentwickelt wird

openSAM wird aktiv gepflegt und ist der empfohlene Nachfolger des kommerziellen SAM-Plugins, das ab X-Plane 12.4 nicht mehr geladen wird. openSAM liest die originalen `sam.xml`-Konfigurationsdateien der Szenerien und ist somit ein Drop-in-Ersatz.

## Funktionsumfang

- **Animierte Jetways:** Scannt SAM-fähige Szenerien beim Start und steuert deren Jetways; Fallback auf X-Plane-12-native Jetways
- **VDGS:** Aktiviert sich nach der Landung (Beacon an), zeigt Azimut- und Distanzführung zum Stand
- **Marshallers:** Animierte Bodenpersonal-Führung
- **Custom-Animationen:** Unterstützung für SAM Custom Animations
- **SAM-Seasons-Emulator:** Integriert (separates SAM-Seasons-Plugin sollte entfernt werden)
- **SimBrief-Integration:** Über das Companion-Plugin [simbrief_hub](../toliss/toliss_ecosystem.md#simbrief_hub)
- **Multiplayer-Support:** Kompatibel mit xPilot, Traffic Global XP und [LiveTraffic](livetraffic.md)
- **Zero-Configuration-Modus:** Szenerie-Entwickler können openSAM-Library-Assets in WED platzieren, ohne eigene Konfigurationsdateien zu schreiben

## Mehrwert in der Flugsimulation

Viele hochwertige Custom-Szenerien wurden für das kommerzielle SAM-Plugin entwickelt. Da SAM ab X-Plane 12.4 nicht mehr funktioniert, übernimmt openSAM diese Rolle als kostenloser Open-Source-Ersatz. Ab v5.x ist [AutoDGS](autodgs.md) in openSAM integriert, sodass es Default-/Gateway-Flughäfen ebenso wie SAM-fähige Custom-Szenerien aus einem einzigen Plugin abdeckt — eine separate AutoDGS-Installation ist unter X-Plane 12 nicht mehr erforderlich.

## Installation

**Download:** [GitHub Releases](https://github.com/hotbso/openSAM/releases)

Die ZIP-Datei enthält zwei Komponenten:

- `openSAM` → nach `Resources/plugins/` entpacken
- `openSAM_Library` → nach `Custom Scenery/` entpacken

In der `scenery_packs.ini` muss `openSAM_Library` über `SAM_Library` stehen. Falls das kommerzielle SAM-Plugin noch installiert ist, sollte es entfernt werden (die `SAM_Library` kann bei Bedarf bleiben).

Es werden keine zusätzlichen Systempakete benötigt. Es sind keine Linux-spezifischen Probleme bekannt. Automatische Updates über den [SkunkCrafts Updater](../tools/skunkcrafts_updater.md) werden unterstützt.

## Quellen

- [openSAM — GitHub](https://github.com/hotbso/openSAM)
- [openSAM — forums.x-plane.org](https://forums.x-plane.org/index.php?/files/file/90865-opensam-an-open-source-replacement-for-sam-on-xp12/)
