---
description: "FlyWithLua NG+ Lua-Scripting-Engine für X-Plane 12 unter Linux: Installation, libglut-Symlink-Fix auf Debian, FMOD-Fehler-Workaround und Skript-Setup."
---
# FlyWithLua

FlyWithLua NG+ ist eine Lua-Scripting-Engine für [X-Plane](../../glossary.md#x-plane) 12, die als Basis für zahlreiche Community-Plugins und eigene Automatisierungen dient.

## Hintergrund

- **Entwickler:** X-Friese (Carsten Lynker), Maintainer sparker256 / smoothchat
- **Repository:** [github.com/X-Friese/FlyWithLua](https://github.com/X-Friese/FlyWithLua) (Open Source, MIT-Lizenz)
- **Plattformen:** Windows, macOS, Linux (native Binaries)
- **Kompatibilität:** X-Plane 12 (NG+ Edition), X-Plane 11 (ältere NG-Edition)

Das [Plugin](../../glossary.md#plugin) wird seit X-Plane 9 entwickelt und ist eines der meistverbreiteten X-Plane-Plugins. Viele Plugins und Skripte wie 3jFPS oder SGES benötigen FlyWithLua.

## Funktionsumfang

- **Lua-Scripting via LuaJIT:** Datarefs lesen und schreiben, eigene Commands erstellen, Menüs anlegen
- **ImGui-Integration:** Native Dear-ImGui-Fenster für eigene Benutzeroberflächen
- **[FMOD](../../glossary.md#fmod)-Audio:** Zugriff auf das X-Plane-FMOD-Soundsystem (COM1, Interior, UI, Master-Busse)
- **HID-Gerätezugriff:** Direkte USB-HID-Kommunikation für Custom-Controller
- **Script-Quarantine:** Fehlerhafte Skripte werden automatisch in den Ordner `Scripts (Quarantine)/` verschoben und können nach Korrektur über das Plugins-Menü neu geladen werden
- **Scripts (disabled):** Skripte in diesem Ordner werden beim Start übersprungen, ohne sie löschen zu müssen

## Mehrwert in der Flugsimulation

FlyWithLua ermöglicht die Automatisierung wiederkehrender Abläufe im Cockpit — von einfachen Checklisten-Helfern bis hin zu komplexen Custom-UIs mit ImGui. Über HID-Zugriff lassen sich auch ungewöhnliche Controller direkt ansprechen, die X-Plane nicht nativ unterstützt. Da viele Community-Plugins FlyWithLua als Voraussetzung haben, gehört es zur Grundausstattung einer X-Plane-Installation.

## Installation

**Download:** [forums.x-plane.org](https://forums.x-plane.org/files/file/82888-flywithlua-ng-next-generation-plus-edition-for-x-plane-12-win-lin-mac/) (kostenloser X-Plane.Org-Account erforderlich)

Die ZIP-Datei nach `Resources/plugins/` entpacken. Es entsteht folgende Verzeichnisstruktur:

```
Resources/plugins/FlyWithLua/
    lin_x64/FlyWithLua.xpl
    Scripts/
    Scripts (disabled)/
    Scripts (Quarantine)/
    Internals/
    Modules/
```

**Abhängigkeiten auf Debian/Ubuntu:**

```bash
sudo apt install libglut3.12 libopenal1
```

### Fehlender libglut-Symlink auf Debian Bookworm

Auf Debian Bookworm (oldstable) enthält das Paket `libglut3.12` keinen `libglut.so.3`-Symlink. FlyWithLua linkt gegen `libglut.so.3` und lädt ohne diesen Symlink nicht — ohne Fehlermeldung im `Log.txt`.

**Workaround:**

```bash
sudo ln -s /usr/lib/x86_64-linux-gnu/libglut.so.3.12 /usr/lib/x86_64-linux-gnu/libglut.so.3
```

Auf Debian Trixie (Stable) und Ubuntu 24.04+ ist der Symlink bereits im Paket enthalten.

### FMOD-Fehler bei bestimmten Flugzeugen

Beim Laden von Flugzeugen mit FMOD-Soundpaket (z.B. ToLiss A321) kann im `Log.txt` folgender Fehler erscheinen:

```
FlyWithLua Error: Error in ../Fmod/FmodIntegration.cpp, line 732: An invalid parameter was passed to this function.
```

Das Plugin lädt und funktioniert trotz der Meldung weiterhin. [Issue #126](https://github.com/X-Friese/FlyWithLua/issues/126) ist offen und bislang unbeantwortet.

## Skript-Installation

FlyWithLua-Skripte (`.lua`-Dateien) werden nach `Resources/plugins/FlyWithLua/Scripts/` kopiert. Lua-Bibliotheken, die von mehreren Skripten gemeinsam genutzt werden, gehören in `Modules/` — nicht in `Scripts/`.

Viele Skripte liefern Sound-Ordner oder Konfigurationsdateien mit. Diese müssen im selben Verzeichnis wie das Skript liegen, damit sie gefunden werden.

```
Resources/plugins/FlyWithLua/
    Modules/
        SharedLibrary.lua
    Scripts/
        MyScript.lua
        MyScript_Sounds/
```

Reine Lua-Skripte sind plattformunabhängig und laufen unter Linux identisch wie unter Windows und macOS. Linux-spezifische Probleme treten nur auf, wenn ein Skript externe Binaries oder Betriebssystem-Funktionen aufruft.

Der Abschnitt [FlyWithLua-Skripte](../flylua_scripts/index.md) dokumentiert einzelne Skripte für den täglichen Einsatz.

## Quellen

- [FlyWithLua — GitHub](https://github.com/X-Friese/FlyWithLua)
- [FlyWithLua NG+ für X-Plane 12 — forums.x-plane.org](https://forums.x-plane.org/files/file/82888-flywithlua-ng-next-generation-plus-edition-for-x-plane-12-win-lin-mac/)
- [Issue #111 — libglut.so.3-Symlink fehlt auf Debian](https://github.com/X-Friese/FlyWithLua/issues/111)
- [Issue #126 — FMOD-Fehler auf Linux](https://github.com/X-Friese/FlyWithLua/issues/126)
