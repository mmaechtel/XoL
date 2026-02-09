# Wayland — Display-Server für X-Plane

**Recherche-Datum:** 2026-02-09
**Quellen-Agenten:** 3 parallele Recherchen (Architektur, X-Plane-Kompatibilität, Performance/Latenz)

---

## Zusammenfassung

Wayland ist seit Debian 12 (GNOME) bzw. Debian 13 (KDE) der Standard-Display-Server. X-Plane 12 hat **keine native Wayland-Unterstützung** und läuft über XWayland. SDL2 (von X-Plane verwendet) bevorzugt standardmäßig X11 als Backend.

**Kernaussagen:**

- X-Plane 12 nutzt XWayland, nicht natives Wayland (bestätigt in Release Notes 12.1.3)
- XWayland-Overhead: ~7ms zusätzliche Latenz vs. natives Wayland, nahezu identisch mit X11
- Joysticks/HOTAS umgehen den Display-Server komplett (Kernel-Zugriff via `/dev/input`)
- AMD/Intel: Wayland ausgereift, keine Nachteile
- NVIDIA: Treiber 555+, Kernel 6.8+ für funktionierendes Explicit Sync erforderlich
- Multi-Monitor: Wayland besser (unabhängige Refresh-Rates), aber XWayland-Fullscreen problematisch

---

## Technischer Hintergrund

### Wayland vs. X11 — Architektur

**X11 (1984):** Client → X Server → Compositor → Hardware. Zentraler Server vermittelt alle Grafik-Operationen.

**Wayland:** Client → Compositor (= Display-Server) → Hardware. Direktes Client-Compositor-Modell, kein Intermediär.

Wesentliche Unterschiede:

- **Rendering:** Wayland-Clients rendern direkt in geteilte GPU-Puffer (DMA-buf), X11 sendet Zeichenbefehle an den Server
- **Sicherheit:** DMA-buf per File-Descriptor-Sharing (Kernel-enforced), X11 nutzt global erratbare GEM-Namen
- **State-Modell:** Wayland push-basiert (Events bei Änderung), X11 query-basiert (Polling)
- **Compositor-Rolle:** Bei Wayland ist der Compositor gleichzeitig Display-Server und Fenstermanager

**Quellen:**
- https://wayland.freedesktop.org/architecture.html
- https://wayland.freedesktop.org/docs/html/ch04.html

### XWayland — Kompatibilitätsschicht

XWayland ist ein vollständiger X11-Server, der als Wayland-Client läuft. X11-Anwendungen verbinden sich mit XWayland wie mit jedem X-Server.

**Performance:** „XWayland has nearly identical performance to that of X11, in most cases" (Arch Wiki). NVIDIA-Doku: „performance should be roughly on-par with native X11, though there is an extra copy required for presentation of windowed applications."

**Einschränkungen:**
- XInput2 nur teilweise implementiert
- Fensterpositionierung nicht möglich (Wayland-Design)
- Kein globaler Zugriff auf Fenster-Liste oder Input anderer Apps

**Quellen:**
- https://wiki.archlinux.org/title/Wayland
- https://download.nvidia.com/XFree86/Linux-x86_64/510.39.01/README/xwayland.html

### Compositor-Gaming-Features

**Direct Scanout:** Compositor übergibt Fullscreen-Buffer direkt an KMS/DRM, ohne GPU-Komposition. Verfügbar in KWin, Mutter, Sway.

**VRR (Variable Refresh Rate):**
- KDE Plasma 5.22+: produktionsreif
- GNOME 46+ experimentell, 50+ stabil
- Wayland hat breitere VRR-Kompatibilität als X11 (Multi-Monitor: X11 bricht G-SYNC bei mehreren Monitoren)

**Tearing Control (wp_tearing_control_v1):**
- Erlaubt Apps, Tearing zu akzeptieren für minimale Latenz
- Unterstützt von: KWin 6.4+, Mutter 49.2+, Sway 1.11+, XWayland 23.2+

**Quellen:**
- https://wayland.app/protocols/tearing-control-v1
- https://wiki.archlinux.org/title/Variable_refresh_rate
- https://zamundaaa.github.io/wayland/2021/12/14/about-gaming-on-wayland.html

---

## Aktueller Stand

### Debian-Spezifika

| Debian-Version | GNOME Standard | KDE Standard |
|----------------|---------------|--------------|
| 10 Buster (2019) | Wayland | X11 |
| 11 Bullseye (2021) | Wayland | X11 |
| 12 Bookworm (2023) | Wayland | Wayland |
| 13 Trixie (2026) | Wayland | Wayland |

GDM3 fällt bei proprietären NVIDIA-Treibern auf X11 zurück (Debian Wiki).

**Session prüfen:** `echo $XDG_SESSION_TYPE` → `wayland` oder `x11`

**Quellen:**
- https://wiki.debian.org/Wayland

### X-Plane 12 auf Wayland

**Bestätigt durch Release Notes:**

- **12.1.3 (Dez 2024):** „Force X11 backend in GDK to enable X-Plane Identity support for Wayland (via XWayland)"
- **12.1.4 (März 2025):** „Fixed an error when resizing the windows using a Wayland session on Linux"

X-Plane nutzt SDL2 (SDL3 erst Jan 2025, zu neu für Adoption). SDL2 bevorzugt X11 als Standard-Backend (nach Revert des Wayland-Defaults in 2022).

**Bekannte Probleme:**
- Fullscreen-Multi-Monitor über XWayland: falsche Position/Aspect-Ratio
- Identity-Login-Browser: DMABUF deaktiviert, GDK auf X11 erzwungen
- Window-Resizing-Crash (behoben in 12.1.4)
- Fensterpositionierung nicht möglich (Wayland-Design)

**Quellen:**
- https://www.x-plane.com/kb/x-plane-12-1-3-release-notes/
- https://www.x-plane.com/kb/x-plane-12-1-4-release-notes/

### SDL2/SDL3 Wayland-Status

**SDL2:** Wayland-Backend vorhanden, aber X11 ist Standard seit Revert (NVIDIA-Probleme, Steam-Overlay-Inkompatibilität). `SDL_VIDEODRIVER=wayland` für explizite Aktivierung.

**SDL3 (Jan 2025):** Natives Wayland als Standard, aber nur wenn `fifo-v1` Protokoll vom Compositor unterstützt wird.

**Quellen:**
- https://www.phoronix.com/news/SDL2-Reverts-Wayland-Default
- https://github.com/libsdl-org/SDL/pull/9383

---

## Performance und Latenz

### Hardware-Messung (David Justo, 2025)

Setup: AMD Ryzen 9 9950X3D + RTX 4090, 360Hz OLED, NVIDIA 580.119.02, KDE/KWin 6.5.4

| Display-Server | Median Latenz |
|----------------|---------------|
| Natives Wayland | 7.14 ms |
| XWayland | 14.45 ms |
| X11 | 6.88 ms |
| Windows 11 | 6.91 ms |

**Erkenntnis:** XWayland verdoppelt die Input-Latenz. Natives Wayland ≈ X11.

**Quelle:** https://davidjusto.com/articles/m2p-latency/

### Xaver Hugl (KDE-Entwickler) — 120Hz-Messungen

| Konfiguration | FIFO (VSync) | Mailbox | Immediate (Tearing) |
|---------------|-------------|---------|---------------------|
| X11 composited | 59 ms | 37 ms | — |
| X11 uncomposited | 41 ms | 38 ms | 19 ms |
| Wayland | 49 ms | 36 ms | 20 ms |

**Erkenntnis:** Wayland mit Compositor ≈ X11 ohne Compositor bei Mailbox/Immediate. X11 mit Compositor ist deutlich schlechter (1 Frame Verzögerung durch Architektur).

**Quelle:** https://zamundaaa.github.io/wayland/2021/12/14/about-gaming-on-wayland.html

### Phoronix-Benchmarks (Ubuntu 25.04, April 2025)

AMD Ryzen 9 9900X3D + Radeon RX 7900 XTX:
- GNOME Wayland und KDE Wayland **übertrafen** KDE X11 bei Gaming-Workloads

**Quelle:** https://www.phoronix.com/review/ubuntu-2504-x11-gaming

---

## GPU-Spezifika

### NVIDIA auf Wayland

**Mindestanforderungen:**
- Treiber 555+ (Explicit Sync via linux-drm-syncobj-v1)
- Kernel 6.8+ (Bug-Fixes)
- XWayland 24.1+
- `nvidia_drm.modeset=1` (Pflicht)

**GBM vs. EGLStreams:** EGLStreams deprecated, XWayland hat EGLStream-Backend März 2024 entfernt. GBM ist Standard.

**Bekannte Einschränkungen:**
- GLX Front-Buffer-Rendering funktioniert nicht mit XWayland
- Hardware-Overlays nicht für GLX/XWayland nutzbar
- SLI Mosaic, Frame Lock, Stereo Rendering nicht unterstützt
- Laptop dGPU-Mux-Switching: kein Wayland-Compositor unterstützt dies

**Quelle:** https://download.nvidia.com/XFree86/Linux-x86_64/580.126.09/README/wayland-issues.html

### AMD (RADV/Mesa) auf Wayland

- Keine RADV-spezifischen Wayland-Probleme dokumentiert
- Performance auf dem Niveau von oder besser als X11
- VRR funktioniert zuverlässig mit KDE/GNOME
- **Warnung:** Mesa 24.3.1 verursachte Freezes auf Vega-GPUs unter Wayland (gefixt)
- AMDVLK eingestellt (Mai 2025), RADV ist der einzige Fokus

**Quellen:**
- https://docs.mesa3d.org/drivers/radv.html

### Intel Arc auf Wayland

- Intel empfiehlt **offiziell** Wayland über Xorg für Arc-GPUs
- Xorg hat bekannte Rendering-Glitches mit Arc
- Kernel 6.2+ erforderlich (6.8+ empfohlen)

**Quelle:** https://www.intel.com/content/www/us/en/support/articles/000092987/graphics/intel-arc-dedicated-graphics-family.html

---

## Eingabegeräte

**Joysticks/HOTAS:** Umgehen den Display-Server komplett. Zugriff über `/dev/input/jsX` (Joystick API) und `/dev/input/eventX` (evdev). Kein Unterschied zwischen Wayland und X11.

**Maus/Tastatur:** libinput (Wayland) vs. xinput (X11). Konfiguration unterscheidet sich:
- X11: `xinput --set-prop "Device" "libinput Accel Speed" 0.0`
- Wayland: Compositor-Settings (GNOME/KDE Systemeinstellungen)

**libinput zu Joysticks:** „libinput does not provide support for joysticks, as any abstraction libinput would provide for joysticks would be so generic that libinput would merely introduce complexity."

**Quellen:**
- https://wayland.freedesktop.org/libinput/doc/latest/what-is-libinput.html
- https://wiki.archlinux.org/title/Gamepad

---

## Konfiguration und Fallback

### X11-Session am Login-Screen wählen

**GDM (GNOME):** „GNOME on Xorg" wählen
**SDDM (KDE):** „Plasma (X11)" wählen

**Dauerhaft X11 erzwingen (GDM):**
```ini
# /etc/gdm3/daemon.conf
[daemon]
WaylandEnable=false
```

### X11 pro Anwendung erzwingen

```bash
# SDL2-Anwendungen (X-Plane)
SDL_VIDEODRIVER=x11 ./X-Plane-x86_64

# GTK-Anwendungen
GDK_BACKEND=x11 ./application

# Qt-Anwendungen
QT_QPA_PLATFORM=xcb ./application
```

### Desktop-Datei für X-Plane

```ini
[Desktop Entry]
Name=X-Plane 12 (X11)
Exec=env SDL_VIDEODRIVER=x11 GDK_BACKEND=x11 /path/to/X-Plane-x86_64
Type=Application
Categories=Game;Simulation;
```

---

## Diagnose und Troubleshooting

### Session-Typ prüfen

```bash
echo $XDG_SESSION_TYPE          # wayland oder x11
echo $WAYLAND_DISPLAY           # wayland-0 wenn Wayland aktiv
loginctl show-session auto -p Type --value
```

### XWayland-Apps erkennen

```bash
xlsclients -l                   # Listet alle X11/XWayland-Apps
xprop                           # Klick auf Fenster: X11-Properties = XWayland
```

### Debug-Umgebungsvariablen

```bash
WAYLAND_DEBUG=1                 # Wayland-Protokoll-Logging
SDL_VIDEODRIVER=wayland          # SDL auf natives Wayland erzwingen
MESA_VK_WSI_PRESENT_MODE=mailbox  # Vulkan Presentation-Mode
```

### Häufige Probleme

| Symptom | Ursache | Lösung |
|---------|---------|--------|
| Screen Tearing | Compositor ohne Tearing-Control | VSync aktivieren oder KWin 6.4+ |
| Maus entweicht | Pointer Constraints nicht implementiert | `SDL_VIDEODRIVER=x11` oder Gamescope |
| Schwarzer Bildschirm (Fullscreen) | VRR-Bug oder NVIDIA Explicit Sync | VRR deaktivieren, Treiber 555+ prüfen |
| Schlechte Performance | XWayland statt natives Wayland | `xlsclients` prüfen, `SDL_VIDEODRIVER=wayland` testen |
| App pausiert bei Workspace-Wechsel | Wayland suspendiert nicht-sichtbare Apps | Fenstermodus verwenden |

---

## Wayland-Spezifika für Dokumentation

### Suspension bei Workspace-Wechsel

Wayland-Compositors suspendieren nicht-sichtbare Fenster. X-Plane stoppt das Rendering bei Workspace-Wechsel. X11 rendert im Hintergrund weiter.

### Vulkan auf Wayland

- VK_KHR_wayland_surface für natives Wayland
- Mailbox-Present-Mode ist Pflicht auf Wayland
- Surface-Extent wird von der Anwendung bestimmt (nicht vom Compositor)

### Wine/Proton auf Wayland

- Wine 10.0 (Jan 2025): experimenteller nativer Wayland-Treiber
- Vulkan-Support fehlt noch im nativen Treiber
- XWayland-Fallback funktioniert für Wine-basierte Plugins

---

## Quellen (Auswahl — vollständige Listen in den Einzel-Research-Papers)

### Primärquellen
- [Wayland Architecture](https://wayland.freedesktop.org/architecture.html)
- [Wayland Protocol](https://wayland.freedesktop.org/docs/html/ch04.html)
- [Arch Wiki — Wayland](https://wiki.archlinux.org/title/Wayland)
- [Debian Wiki — Wayland](https://wiki.debian.org/Wayland)
- [NVIDIA Wayland Known Issues](https://download.nvidia.com/XFree86/Linux-x86_64/580.126.09/README/wayland-issues.html)
- [X-Plane 12.1.3 Release Notes](https://www.x-plane.com/kb/x-plane-12-1-3-release-notes/)
- [X-Plane 12.1.4 Release Notes](https://www.x-plane.com/kb/x-plane-12-1-4-release-notes/)

### Technische Analysen
- [David Justo — Input-to-Photon Latency](https://davidjusto.com/articles/m2p-latency/)
- [Xaver Hugl — Gaming on Wayland](https://zamundaaa.github.io/wayland/2021/12/14/about-gaming-on-wayland.html)
- [Phoronix — Ubuntu 25.04 Gaming](https://www.phoronix.com/review/ubuntu-2504-x11-gaming)

### Protokoll-Spezifikationen
- [Tearing Control v1](https://wayland.app/protocols/tearing-control-v1)
- [VK_KHR_wayland_surface](https://registry.khronos.org/vulkan/specs/latest/man/html/VK_KHR_wayland_surface.html)
- [libinput Docs](https://wayland.freedesktop.org/libinput/doc/latest/what-is-libinput.html)
- [Arch Wiki — Variable Refresh Rate](https://wiki.archlinux.org/title/Variable_refresh_rate)
