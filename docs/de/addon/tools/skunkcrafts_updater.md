---
description: "SkunkCrafts Updater hält X-Plane-Addons unter Linux aktuell: automatische Erkennung, differentielle Downloads und glibc-Kompatibilität für Debian."
---
# SkunkCrafts Updater

Der SkunkCrafts Updater ist das De-facto-Standard-Update-Tool für [X-Plane](../../glossary.md#x-plane)-Addons. Er durchsucht eine X-Plane-Installation nach Addons, die SkunkCrafts-Konfigurationsdateien mitliefern, vergleicht Versionen mit Remote-Repositories und lädt Updates automatisch herunter.

## Hintergrund

- **Entwickler:** Lionel Zamouth (SkunkCrafts / Aerobask)
- **Forum:** [forums.x-plane.org](https://forums.x-plane.org/forums/forum/406-skunkcrafts-updater/)
- **Lizenz:** Freeware, Closed Source (das Update-Protokoll ist offen und dokumentiert)
- **Plattformen:** Windows, macOS, Linux (native Binaries)
- **Kompatibilität:** X-Plane 11 und 12

Die aktuelle Standalone-Version ist eine komplette Neuentwicklung in Go mit Fyne-UI. Sie ersetzt das ältere In-Game-[Plugin](../../glossary.md#plugin) und läuft unabhängig von X-Plane — kein laufender Simulator für Updates nötig.

## Funktionsumfang

- **Automatische Erkennung:** Durchsucht alle X-Plane-Unterverzeichnisse nach `skunkcrafts_updater.cfg`-Dateien
- **Differenzielle Updates:** Nur Dateien, deren CRC32-Prüfsumme oder Größe von der Remote-Version abweicht, werden heruntergeladen
- **Parallele Downloads:** Bis zu 32 gleichzeitige Downloads (konfigurierbar)
- **Beta-Kanal:** Optionale `skunkcrafts_updater_beta.cfg` für Beta-Releases
- **Offenes Protokoll:** Jeder Addon-Entwickler kann sich integrieren, indem er eine cfg-Datei mitliefert, die auf sein eigenes Repository verweist — keine Abstimmung mit dem Updater-Entwickler nötig

## Mehrwert in der Flugsimulation

Da Dutzende kommerzieller und Freeware-Entwickler das SkunkCrafts-Protokoll nutzen — darunter Aerobask, X-Crafts, SimCoders, VSKYLABS, Just Flight, FlyJSim und Stick and Rudder Studios — genügt ein einziges Tool, um die meisten Addons aktuell zu halten. Jedes Addon liefert eine `skunkcrafts_updater.cfg` mit, die auf das Repository des Entwicklers verweist; der Updater findet diese Dateien automatisch und erledigt den Rest.

!!! info "Fehlerbehebung"

    Die cfg-Dateien sind Klartext mit Pipe-Trennzeichen (`key|value`) — kein INI, kein JSON. Wenn ein Addon im Updater nicht erscheint: prüfen, ob die `skunkcrafts_updater.cfg` im Stammverzeichnis des Addons existiert, ob `disabled` auf `false` steht und ob die `module`-URL erreichbar ist.

## Installation

**Download:** Der Standalone-Client wird über den [forums.x-plane.org Release-Thread](https://forums.x-plane.org/forums/topic/292710-20250206-skunkcrafts-updater-standalone-client-v32d-available/) verteilt. Ein kostenloser X-Plane.org-Account ist erforderlich.

Das Linux-Binary ist eine einzelne Datei mit dem Namen `SkunkcraftsUpdater_lin`. Sie wird im X-Plane-Stammverzeichnis abgelegt (der Ordner, der `X-Plane-x86_64` enthält) und ausführbar gemacht:

```bash
chmod +x SkunkcraftsUpdater_lin
./SkunkcraftsUpdater_lin
```

Der Updater muss aus dem X-Plane-Stammverzeichnis gestartet werden — er entdeckt Addons durch Scannen der Unterverzeichnisse ausgehend von seinem eigenen Verzeichnis. Eine ältere In-Game-Plugin-Version existiert, wird aber nicht mehr aktiv weiterentwickelt.

### glibc-Anforderung

Das Linux-Binary benötigt glibc 2.32 oder höher. Dies ist eine Folge der Go + Fyne Build-Toolchain (CGo linkt gegen die glibc des Build-Systems).

| Distribution | glibc | Status |
|---|---|---|
| Debian 12 Bookworm | 2.36 | Funktioniert |
| Debian 11 Bullseye | 2.31 | Kann fehlschlagen |
| Ubuntu 22.04+ | 2.35 | Funktioniert |
| Ubuntu 20.04 | 2.31 | Fehlschlag |

### Fyne-UI und Wayland

Das Fyne-Toolkit unterstützt Wayland, kann aber je nach Compositor auf XWayland zurückfallen. Es sind keine SkunkCrafts-spezifischen Wayland-Probleme dokumentiert.

## Quellen

- [SkunkCrafts Updater — forums.x-plane.org](https://forums.x-plane.org/forums/forum/406-skunkcrafts-updater/)
- [Standalone Client Release Thread — forums.x-plane.org](https://forums.x-plane.org/forums/topic/292710-20250206-skunkcrafts-updater-standalone-client-v32d-available/)
- [glibc-Anforderung Diskussion — forums.x-plane.org](https://forums.x-plane.org/forums/topic/302313-linux-standalone-skunkcrafts-updater-requires-glibc-232-or-higher/)
- [openSAM SkunkCrafts-Integration — GitHub](https://github.com/hotbso/openSAM)
