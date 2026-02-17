---
description: "X11-Session für X-Plane unter Linux einrichten: Session-Wechsel, Compositor-Bypass, Desktop-Entry-Konfiguration und Vorteile gegenüber Wayland."
---
# X11-Session für X-Plane

Das empfohlene Setup für X-Plane unter Linux. In einer X11-Session kommuniziert X-Plane direkt mit dem X-Server — keine Übersetzungsschicht, kein Overhead.

## Was passiert

```
X-Plane → X11 → X-Server → GPU → Monitor
Desktop  → X11 → X-Server → GPU → Monitor
```

Alles spricht das gleiche Protokoll. X-Planes X11-Aufrufe gehen direkt an den X-Server, der sie an die GPU weitergibt. Keine Compositor-Übersetzung, keine Extra-Bildkopien.

---

## Aktuelle Session prüfen

```bash
echo $XDG_SESSION_TYPE
```

Wenn die Ausgabe `x11` ist, läuft bereits eine X11-Session. Keine Änderungen nötig.

Wenn die Ausgabe `wayland` ist, folge den Schritten unten.

---

## Zu X11 wechseln

### Am Login-Screen

Der Session-Typ wird **vor** dem Einloggen gewählt. Achte auf ein Zahnrad-Symbol oder Session-Menü, meist in der unteren Ecke.

**GDM (GNOME)**

- Benutzernamen anklicken
- Vor der Passworteingabe das Zahnrad-Symbol (unten rechts) anklicken
- **„GNOME on Xorg"** auswählen

**SDDM (KDE)**

- Am Login-Screen den Session-Selektor suchen (unten links)
- **„Plasma (X11)"** auswählen

Die Auswahl bleibt gespeichert bis zur nächsten Änderung. Sie muss nicht bei jedem Login neu getroffen werden.

### X11 dauerhaft erzwingen (optional)

Wer Wayland-Sessions komplett verhindern will, kann Wayland auf Display-Manager-Ebene deaktivieren.

**GDM (GNOME)**

```ini
# /etc/gdm3/daemon.conf
[daemon]
WaylandEnable=false
```

Nach dem Speichern GDM neu starten oder rebooten. Der Login-Screen bietet dann nur noch X11-Sessions an.

**SDDM (KDE)**

SDDM nutzt auf Debian kein Wayland für den Login-Screen. Die Auswahl von „Plasma (X11)" im Session-Menü ist ausreichend.

---

## Compositor-Bypass

In einer X11-Session können Fullscreen-Anwendungen den Compositor komplett umgehen. Das eliminiert einen Frame Latenz, den der Compositor sonst hinzufügen würde.

**KDE Plasma**

KDE deaktiviert das Compositing, wenn eine Fullscreen-Anwendung dies anfordert. Die Standardeinstellung „Anwendungen dürfen Compositing blockieren" regelt dies. Keine manuelle Konfiguration nötig.

Zur Verifikation X-Plane im Fullscreen starten und prüfen:

```bash
qdbus org.kde.KWin /Compositor org.kde.kwin.Compositing.active
```

Ausgabe `false` bedeutet: der Compositor ist umgangen — X-Plane rendert direkt auf den Bildschirm.

**GNOME**

Mutter (GNOMEs Compositor) unterstützt keinen vollständigen Compositor-Bypass, führt aber eine Optimierung namens **Direct Scanout** für Fullscreen-Anwendungen durch. Dabei wird der GPU-Kompositionsschritt vermieden, während der Compositor aktiv bleibt.

---

## Desktop-Eintrag

Eine optionale `.desktop`-Datei stellt sicher, dass X-Plane immer mit dem X11-Backend startet, auch wenn sich der Session-Typ später ändert.

```ini
# ~/.local/share/applications/x-plane-12.desktop
[Desktop Entry]
Name=X-Plane 12
Exec=env SDL_VIDEODRIVER=x11 GDK_BACKEND=x11 /path/to/X-Plane-x86_64
Type=Application
Categories=Game;Simulation;
Comment=X-Plane 12 Flight Simulator (X11)
```

`/path/to/` durch den tatsächlichen Pfad zur X-Plane-Installation ersetzen.

`SDL_VIDEODRIVER=x11` weist SDL2 an, das X11-Backend zu verwenden. `GDK_BACKEND=x11` stellt sicher, dass der Identity-Login-Browser ebenfalls X11 nutzt. X-Plane setzt dies seit Version 12.1.3 intern, aber die Angabe im Desktop-Eintrag garantiert es für alle Startmethoden.

---

## Vorteile

- **Kein Latenz-Overhead** — direkter X11-Pfad, keine XWayland-Übersetzung
- **Zuverlässiger Fullscreen** — Compositor-Bypass funktioniert, keine Sonderfälle
- **Multi-Monitor** — X-Plane-Fullscreen über mehrere Monitore funktioniert ohne Probleme
- **Identity-Login** — keine Workarounds nötig
- **Bewährter Pfad** — X-Plane nutzt X11 unter Linux seit der ersten Version

## Einschränkungen

- **Einheitliche Refresh-Rate** — alle Monitore teilen sich die gleiche Refresh-Rate unter X11. Bei einem 144-Hz- und einem 60-Hz-Monitor laufen beide mit 60 Hz
- **VRR pro Monitor eingeschränkt** — Variable Refresh Rate wird unterstützt, aber Per-Monitor-VRR ist unter X11 problematisch
- **Desktop-Sicherheit** — X11 erlaubt Anwendungen, die Eingaben anderer Fenster mitzulesen (keine Isolation)

Diese Einschränkungen betreffen die **Desktop-Erfahrung**, nicht X-Plane selbst. Bei einem dedizierten Flugsim-Setup sind sie selten relevant.

---

## Zurück zu Wayland

Wer später zu einer Wayland-Session wechseln möchte, wählt „GNOME" oder „Plasma (Wayland)" am Login-Screen. Falls Wayland dauerhaft deaktiviert wurde, zuerst wieder aktivieren:

```ini
# /etc/gdm3/daemon.conf
[daemon]
WaylandEnable=true
```

---

## Weiterführende Kapitel

| Thema | Seite | Schwerpunkt |
|---|---|---|
| Display-Server-Übersicht | [Display-Server](displayserver.md) | Protokollvergleich und Latenzmessungen |
| Wayland-Session | [Wayland-Session](displayserver_wayland.md) | Alternative: Wayland-Desktop mit XWayland |
| Nvidia-Treiber | [Nvidia-Treiber](nvidia.md) | Composition Pipeline und X11-spezifische Einstellungen |
| Kernel-Tuning | [Kernel-Tuning](../system/systemtuning.md) | Latenzoptimierung auf Systemebene |
| Konfiguration | [Konfiguration](../../xplane/setup_diagnose/config.md) | X-Plane Display- und Rendering-Einstellungen |
