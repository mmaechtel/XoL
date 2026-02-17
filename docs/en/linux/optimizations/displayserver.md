# Display Server

X-Plane 12 has no native Wayland support. How it connects to your screen depends on which display server session you choose at login. This page explains the three protocols involved and helps you decide which session to use.

<div class="video-container" markdown>
<video controls width="100%" preload="metadata" aria-label="Video: X-Plane — Display Server Choice" poster="../../../assets/video/en/X-Plane__Display_Server_Choice/X-Plane__Display_Server_Choice.jpg">
  <source src="../../../assets/video/en/X-Plane__Display_Server_Choice/X-Plane__Display_Server_Choice.mp4" type="video/mp4">
</video>
</div>

## Three Protocols

### X11 (Xorg)

The classic display server protocol, developed since 1984 (X11 version from 1987). A central X server manages all graphics and input. Applications send drawing commands to the server, which renders everything and forwards it to the GPU.

X-Plane speaks X11 natively. When you run an X11 session, X-Plane communicates directly with the X server — no translation, no overhead.

### Wayland

The modern successor to X11. Instead of a central server, the **compositor** (e.g., Mutter for GNOME, KWin for KDE) acts as both display server and window manager. Applications render directly into GPU buffers and hand them to the compositor.

Wayland offers per-monitor refresh rates and native Variable Refresh Rate (VRR) support. It has been the default GNOME session since Debian 10. For KDE, Wayland becomes the default in Debian 13 (Plasma 6).

X-Plane **cannot** speak Wayland natively.

### XWayland

A compatibility layer — a complete X11 server that runs **inside** a Wayland session. When an X11 application (like X-Plane) starts on a Wayland desktop, XWayland automatically handles the translation between X11 and the Wayland compositor.

The application doesn't notice the difference — it talks X11 as usual. But the extra translation step adds latency and an additional frame copy for windowed applications.

---

## What Happens with X-Plane?

| | X11 Session | Wayland Session |
|---|---|---|
| **Desktop apps** | X11 → X server → GPU | Wayland → Compositor → GPU |
| **X-Plane** | X11 → X server → GPU | X11 → XWayland → Compositor → GPU |
| **Extra overhead** | None | ~7 ms latency, extra frame copy |
| **Fullscreen** | Compositor bypass possible | XWayland fullscreen limited |
| **Multi-monitor** | All monitors share one refresh rate | Per-monitor refresh rate, but XWayland fullscreen issues |
| **Joysticks/HOTAS** | `/dev/input` (kernel direct) | `/dev/input` (kernel direct) |

Joysticks, throttles, and rudder pedals bypass the display server entirely. They communicate directly with the kernel via `/dev/input`. Your choice of display server has **no effect** on flight peripherals.

!!! tip "Recommendation"
    Use an **X11 session** for X-Plane. It eliminates the XWayland overhead and provides the most reliable fullscreen and multi-monitor behavior. Details: [X11 Session for X-Plane](displayserver_x11.md)

    If you want to keep Wayland for your desktop, X-Plane will work via XWayland — with some limitations. Details: [Wayland Session with X-Plane](displayserver_wayland.md)

---

## Latency Comparison

### Hardware Measurements (David Justo)

Test setup: AMD Ryzen 9 9950X3D, NVIDIA RTX 4090, Dell AW2725DF 360 Hz OLED

| Display Server | Input-to-Photon Latency |
|----------------|-------------------------------|
| X11 | 6.88 ms |
| Native Wayland | 7.14 ms |
| XWayland | 14.45 ms |
| Windows 11 | 6.91 ms |

Native Wayland matches X11. XWayland approximately **doubles** the input latency due to the translation layer.

### Compositor Latency (Xaver Hugl, KDE developer)

Measurements at 120 Hz with different Vulkan presentation modes

| Configuration | FIFO (VSync) | Mailbox | Immediate (Tearing) |
|---------------|-------------|---------|---------------------|
| X11 with compositor | 59 ms | 37 ms | — |
| X11 without compositor | 41 ms | 38 ms | 19 ms |
| Wayland | 49 ms | 36 ms | 20 ms |
| XWayland | 49 ms | 38 ms | 20 ms |

Wayland with an active compositor matches X11 **without** a compositor in Mailbox and Immediate modes. In VSync (FIFO) mode, X11 with a compositor adds a full frame of latency compared to Wayland. In Mailbox mode, the difference disappears.

??? abstract "About these measurements"

    The David Justo measurements used a hardware sensor (Arduino Pro Micro + TEMT6000 phototransistor) to measure actual input-to-photon latency. Test application: Counter-Strike 2 (400 fps engine cap, VSync off, VRR off, Allow Tearing on). Test conditions: KWin 6.5.4, NVIDIA driver 580.119.02, Fedora 43, 100 measurements per configuration.

    The Xaver Hugl measurements come from the KDE compositor developer and compare presentation modes on a 120 Hz display.

    Both measurements were conducted with modern hardware and current drivers. Results may differ on older systems.

---

## GPU Recommendations

| GPU | Wayland Desktop | X-Plane Session | Notes |
|-----|----------------|-----------------|-------|
| **AMD (RADV)** | Excellent | X11 recommended | Wayland desktop works perfectly, but X-Plane still goes through XWayland |
| **NVIDIA** | Good (555+ driver) | X11 recommended | Older drivers (<555): X11 session mandatory. Current drivers: Wayland desktop possible |
| **Intel Arc** | Excellent | X11 recommended | Intel officially recommends Wayland for the desktop. X11 has known rendering glitches on Arc |

The GPU recommendation is about the **desktop session**, not about X-Plane itself. X-Plane always speaks X11 — either directly (X11 session) or via XWayland (Wayland session).

!!! note "Intel Arc: Special case"
    Intel Arc GPUs have known rendering glitches under X11/Xorg. If you use an Arc GPU, a Wayland session may actually be the better choice for the overall desktop experience, accepting the XWayland overhead for X-Plane.

---

## Input Devices

### Joysticks, Throttles, Rudder Pedals

Flight peripherals are **not affected** by the display server choice. They communicate directly with the Linux kernel:

- Accessed via `/dev/input/eventX` (evdev interface)
- Accessed via `/dev/input/jsX` (legacy joystick API)
- Managed by the kernel, not by Wayland or X11
- libinput explicitly does not handle joysticks

Your Thrustmaster, VKB, Virpil, or Logitech hardware works identically on X11 and Wayland.

### Mouse and Keyboard

Mouse and keyboard input **does** differ between display servers:

- **X11:** Managed by Xorg with xinput configuration
- **Wayland:** Managed by the compositor via libinput

For X-Plane cockpit clicking, consider disabling mouse acceleration:

- **X11:** `xinput --set-prop "device" "libinput Accel Profile Enabled" 0 1` (enables flat profile)
- **Wayland:** Compositor settings (GNOME Settings → Mouse, KDE System Settings → Input Devices)

---

## Which Session Should I Use?

```bash
# Check your current session type
echo $XDG_SESSION_TYPE
```

Output: `x11` or `wayland`

| Your Situation | Recommendation | Page |
|----------------|---------------|------|
| Want the simplest, most reliable X-Plane setup | X11 session | [X11 Session](displayserver_x11.md) |
| Already on Wayland, X-Plane works fine | Stay on Wayland | [Wayland Session](displayserver_wayland.md) |
| Fullscreen or multi-monitor problems | Switch to X11 | [X11 Session](displayserver_x11.md) |
| Intel Arc GPU with X11 desktop glitches | Wayland session | [Wayland Session](displayserver_wayland.md) |
| NVIDIA with driver older than 555 | X11 session (mandatory) | [X11 Session](displayserver_x11.md) |

---

## Sources

- [Wayland Architecture](https://wayland.freedesktop.org/architecture.html) — Official Wayland project
- [Arch Wiki — Wayland](https://wiki.archlinux.org/title/Wayland) — Comprehensive reference
- [David Justo — Input-to-Photon Latency](https://davidjusto.com/articles/m2p-latency/) — Hardware latency measurements
- [Xaver Hugl — Gaming on Wayland](https://zamundaaa.github.io/wayland/2021/12/14/about-gaming-on-wayland.html) — KDE developer analysis
- [libinput — What is libinput](https://wayland.freedesktop.org/libinput/doc/latest/what-is-libinput.html) — Input device handling
