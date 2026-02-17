---
description: "Running X-Plane in a Wayland session via XWayland: latency overhead, known issues, environment variables, and GPU-specific troubleshooting."
---
# Wayland Session with X-Plane

If you use a Wayland session for your desktop, X-Plane will still work — via the XWayland compatibility layer. This page explains what happens, what to expect, and how to troubleshoot.

## What Happens

```
Desktop  → Wayland → Compositor → GPU → Monitor   (native)
X-Plane  → X11 → XWayland → Compositor → GPU → Monitor   (translated)
```

Your desktop applications speak native Wayland and communicate directly with the compositor. X-Plane cannot speak Wayland — it speaks X11. XWayland automatically steps in as a translator: a complete X11 server running inside the Wayland session.

X-Plane does not notice the difference. It talks X11 as usual. But the extra translation step adds latency and an additional frame copy.

---

## XWayland Overhead

XWayland approximately doubles the input latency compared to native X11 or native Wayland (~7 ms vs. ~14 ms in hardware measurements). The exact overhead depends on GPU, display, and configuration. For detailed measurements and compositor comparisons, see the [Display Server Overview](displayserver.md#latency-comparison).

---

## Verify X-Plane Uses XWayland

In a Wayland session, X-Plane should appear as an XWayland client. To verify:

```bash
# List all X11/XWayland clients
xlsclients -l
```

If X-Plane appears in the list, it is running through XWayland. If nothing appears, the tool `xprop` provides another check — click on the X-Plane window. If it shows X11 properties, the application runs via XWayland.

---

## Known Issues

| Symptom | Cause | Solution |
|---------|-------|----------|
| Fullscreen wrong size or position on multi-monitor | Wayland does not allow applications to position windows — XWayland inherits this limitation | Run X-Plane windowed, or switch to an [X11 session](displayserver_x11.md) |
| Identity login fails or shows blank page | Browser component needs X11 backend | Set `GDK_BACKEND=x11` (automatic since X-Plane 12.1.3) |
| X-Plane pauses when switching workspace | Wayland compositors suspend non-visible applications | Stay on X-Plane's workspace, or use windowed mode |
| Screen tearing | Compositor does not support tearing control | Enable VSync in X-Plane, or use a recent KDE Plasma version |
| Mouse escapes X-Plane window | Pointer constraints not fully implemented | Set `SDL_VIDEODRIVER=x11`, or use fullscreen |
| Black screen after Alt-Tab | VRR interaction with XWayland fullscreen | Disable VRR, or use windowed mode |

---

## Environment Variables

These variables can help with XWayland-related issues. Set them before starting X-Plane:

```bash
# Force X11 backend in SDL2 (usually automatic)
export SDL_VIDEODRIVER=x11

# Force X11 backend for GTK (identity login browser)
export GDK_BACKEND=x11

# Set Vulkan presentation mode (Mesa drivers only — AMD, Intel)
export MESA_VK_WSI_PRESENT_MODE=mailbox
```

To make these permanent, add them to a [desktop entry](displayserver_x11.md#desktop-entry) or your shell profile.

---

## Desktop Entry

The base setup is the same as for an [X11 session](displayserver_x11.md#desktop-entry). For Wayland with AMD or Intel GPUs, add the presentation mode variable:

```ini
Exec=env SDL_VIDEODRIVER=x11 GDK_BACKEND=x11 MESA_VK_WSI_PRESENT_MODE=mailbox /path/to/X-Plane-x86_64
```

`MESA_VK_WSI_PRESENT_MODE=mailbox` applies only to Mesa drivers (AMD, Intel) and can reduce latency under XWayland. NVIDIA users should omit this variable.

---

## GPU-Specific Notes

### AMD (RADV)

Wayland works well on AMD with excellent driver support and no special configuration required. If X-Plane runs without issues in your Wayland session, there is no strong reason to switch to X11.

### NVIDIA

Wayland on NVIDIA requires current drivers with Explicit Sync support. Older drivers will cause visual glitches, input lag, or crashes under Wayland.

**Minimum requirements for Wayland**

- NVIDIA driver 555 or newer
- Kernel 6.8 or newer
- `nvidia_drm.modeset=1` active (default since driver 560; verify with `cat /sys/module/nvidia_drm/parameters/modeset`)

If your driver is older than 555, use an [X11 session](displayserver_x11.md) — Wayland will not work reliably.

### Intel Arc

Intel officially recommends Wayland for Arc GPUs. X11/Xorg has known rendering glitches on Arc hardware. If you use an Arc GPU, staying on Wayland (with X-Plane via XWayland) may be the better overall experience.

---

## What About Native Wayland?

Setting `SDL_VIDEODRIVER=wayland` forces SDL2 to attempt a native Wayland connection. X-Plane 12 does not have a native Wayland backend, and this configuration is not tested or supported by Laminar Research — results vary from crashes and rendering glitches to a silent fallback to XWayland.

!!! warning "Do not force native Wayland"
    `SDL_VIDEODRIVER=wayland` is **not recommended** for X-Plane. X-Plane 12 has no native Wayland backend, and this configuration produces unpredictable results. If you encounter issues, the first troubleshooting step is to remove this variable.

---

## When to Switch to X11

Consider switching to an [X11 session](displayserver_x11.md) if:

- Fullscreen or multi-monitor problems persist
- You notice input latency compared to Windows or X11
- You use an NVIDIA GPU with drivers older than 555
- You want the simplest, most reliable X-Plane setup

For most users who already have a working Wayland desktop and no X-Plane issues, staying on Wayland is fine.

---

## Further Reading

| Topic | Page | Focus |
|---|---|---|
| Display Server Overview | [Display Server](displayserver.md) | Protocol comparison and latency measurements |
| X11 Session | [X11 Session](displayserver_x11.md) | Alternative: direct X11 without XWayland overhead |
| Nvidia Drivers | [Nvidia Drivers](nvidia.md) | Wayland driver requirements (Explicit Sync) |
| Latency and Predictability | [Latency and Predictability](../../fundamentals/performance/latency.md) | Understanding XWayland latency overhead |
| Configuration | [Configuration](../../xplane/setup_diagnose/config.md) | X-Plane display and rendering settings |
