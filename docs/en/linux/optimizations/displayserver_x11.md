---
description: "Setting up an X11 session for X-Plane on Linux: session switching, compositor bypass, desktop entry configuration, and advantages over Wayland."
---
# X11 Session for X-Plane

The recommended setup for X-Plane on Linux. In an X11 session, X-Plane communicates directly with the X server — no translation layer, no overhead.

## What Happens

```
X-Plane → X11 → X server → GPU → Monitor
Desktop  → X11 → X server → GPU → Monitor
```

Everything speaks the same protocol. X-Plane's X11 calls go straight to the X server, which passes them to the GPU. No compositor translation, no extra frame copies.

---

## Check Your Current Session

```bash
echo $XDG_SESSION_TYPE
```

If the output is `x11`, you are already in an X11 session. No changes needed.

If the output is `wayland`, follow the steps below to switch.

---

## Switch to X11

### At the Login Screen

The session type is selected **before** logging in. Look for a gear icon or session menu, usually in the bottom corner.

**GDM (GNOME)**

- Click your username
- Before entering your password, click the gear icon (bottom right)
- Select **"GNOME on Xorg"**

**SDDM (KDE)**

- At the login screen, look for the session selector (bottom left)
- Select **"Plasma (X11)"**

This selection persists until you change it again. You do not need to re-select it on every login.

### Make X11 Permanent (Optional)

If you want to prevent Wayland sessions entirely, you can disable Wayland at the display manager level.

**GDM (GNOME)**

```ini
# /etc/gdm3/daemon.conf
[daemon]
WaylandEnable=false
```

After saving, restart GDM or reboot. The login screen will only offer X11 sessions.

**SDDM (KDE)**

SDDM does not use Wayland for the login screen on Debian. Selecting "Plasma (X11)" at the session menu is sufficient.

---

## Compositor Bypass

In an X11 session, fullscreen applications can bypass the compositor entirely. This eliminates one frame of latency that the compositor would otherwise add.

**KDE Plasma**

KDE suspends compositing when a fullscreen application requests it. The default setting "Allow applications to block compositing" handles this. No manual configuration needed.

To verify, run X-Plane in fullscreen and check:

```bash
qdbus org.kde.KWin /Compositor org.kde.kwin.Compositing.active
```

Output `false` means the compositor is bypassed — X-Plane renders directly to the screen.

**GNOME**

Mutter (GNOME's compositor) does not support full compositor bypass, but performs an optimization called **direct scanout** for fullscreen applications. This avoids the GPU composition step while the compositor remains active.

---

## Desktop Entry

An optional `.desktop` file ensures X-Plane always starts with the X11 backend, even if your session type changes later.

```ini
# ~/.local/share/applications/x-plane-12.desktop
[Desktop Entry]
Name=X-Plane 12
Exec=env SDL_VIDEODRIVER=x11 GDK_BACKEND=x11 /path/to/X-Plane-x86_64
Type=Application
Categories=Game;Simulation;
Comment=X-Plane 12 Flight Simulator (X11)
```

Replace `/path/to/` with the actual path to your X-Plane installation.

`SDL_VIDEODRIVER=x11` tells SDL2 to use the X11 backend. `GDK_BACKEND=x11` ensures the identity login browser also uses X11. X-Plane sets this internally since version 12.1.3, but specifying it in the desktop entry guarantees it for all launch methods.

---

## Advantages

- **No latency overhead** — direct X11 path, no XWayland translation
- **Reliable fullscreen** — compositor bypass works, no edge cases
- **Multi-monitor** — X-Plane fullscreen across monitors works without issues
- **Identity login** — no workarounds needed
- **Proven path** — X-Plane has used X11 on Linux since its first release

## Limitations

- **Single refresh rate** — all monitors share the same refresh rate under X11. If you have a 144 Hz and a 60 Hz monitor, both run at 60 Hz
- **Limited VRR per monitor** — Variable Refresh Rate support exists but per-monitor VRR is problematic under X11
- **Desktop security** — X11 allows applications to read each other's input (no isolation between windows)

These limitations affect the **desktop experience**, not X-Plane itself. For a dedicated flight sim setup, they are rarely relevant.

---

## Returning to Wayland

If you want to switch back to a Wayland session later, select "GNOME" or "Plasma (Wayland)" at the login screen. If you disabled Wayland permanently via `daemon.conf`, re-enable it first:

```ini
# /etc/gdm3/daemon.conf
[daemon]
WaylandEnable=true
```

---

## Further Reading

| Topic | Page | Focus |
|---|---|---|
| Display Server Overview | [Display Server](displayserver.md) | Protocol comparison and latency measurements |
| Wayland Session | [Wayland Session](displayserver_wayland.md) | Alternative: Wayland desktop with XWayland |
| Nvidia Drivers | [Nvidia Drivers](nvidia.md) | Composition pipeline and X11-specific settings |
| Kernel Tuning | [Kernel Tuning](../system/systemtuning.md) | System-level optimization for latency |
| Configuration | [Configuration](../../xplane/setup_diagnose/config.md) | X-Plane display and rendering settings |
