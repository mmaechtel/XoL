# Research: Wayland vs X11 for X-Plane on Linux

**Research Date:** 2026-02-09
**Topic:** Performance comparison, latency analysis, and troubleshooting for Wayland vs X11 display servers in gaming contexts
**Scope:** Focus on Linux gaming with emphasis on Vulkan applications like X-Plane 12

---

## Executive Summary

Wayland has matured significantly for gaming workloads as of 2025-2026, with recent benchmarks showing Wayland sessions outperforming X11 in most gaming scenarios on modern hardware. However, the landscape remains nuanced:

- **Native Wayland** applications achieve latency parity with X11
- **XWayland** (compatibility layer) introduces measurable overhead (~7ms additional latency)
- **NVIDIA** users require driver 555+ and kernel 6.8+ for optimal Wayland experience
- **AMD/Intel** users generally have mature Wayland support with minimal issues
- **Tearing control** and **VRR** support vary by compositor (KDE/GNOME implementations differ)

---

## 1. Performance: Wayland vs X11 for Gaming

### 1.1 Recent Benchmark Results (2025-2026)

**Phoronix Ubuntu 25.04 Benchmark (April 2025)**

Test configuration:
- Hardware: AMD Ryzen 9 9900X3D + Radeon RX 7900 XTX
- Software: Ubuntu 25.04, Linux 6.14, Mesa 25.0.1
- Desktop environments tested:
    - GNOME 48 Wayland
    - KDE Plasma 6.3.3 Wayland
    - KDE Plasma 6.3.3 X11
    - Xfce 4.20 X11
    - LXQt 2.1 X11

**Key finding:** "Both GNOME under Wayland and KDE under Wayland were outperforming KDE on X11" for gaming workloads. GNOME's X11 session encountered technical issues preventing testing.

**Source:** [Phoronix - Ubuntu 25.04 Gaming Benchmarks](https://www.phoronix.com/review/ubuntu-2504-x11-gaming)

**Earlier KDE Plasma 6.0 Testing (2024)**

KDE Neon testing with Fedora 40 showed performance parity between Wayland and X11 sessions on AMD Radeon hardware, indicating that by 2024 the performance gap had closed.

**Source:** [Phoronix Forums - AMD Radeon Performance Parity](https://www.phoronix.com/forums/forum/software/desktop-linux/1456174-amd-radeon-linux-gaming-performance-at-parity-between-kde-plasma-6-0-x11-vs-wayland)

### 1.2 Compositor Overhead Analysis

#### Direct Scanout

Wayland compositors implement **direct scanout** (also called "unredirection" in X11 terminology), where fullscreen application buffers can bypass composition and be sent directly to the display hardware. This works in both fullscreen and windowed mode when compositor and hardware support it.

**Technical mechanism:** The compositor configures the CRTC to read directly from the application's front buffer, eliminating unnecessary buffer copies. This provides:
- Reduced GPU load and power consumption
- Lower latency (no additional compositing step)
- Transparency to applications (no API changes needed)

**Source:** [Xaver Hugl - Gaming on Wayland](https://zamundaaa.github.io/wayland/2021/12/14/about-gaming-on-wayland.html)

**GNOME Mutter improvements:** GNOME landed improved direct scanout handling for subsurfaces, expanding coverage beyond simple fullscreen scenarios.

**Source:** [Phoronix - GNOME Direct Scanout](https://www.phoronix.com/news/GNOME-Subsurface-Scanout)

#### X11 Compositing Limitations

X11 with compositing suffers from a fundamental architectural flaw: "the image from it goes to the compositor exactly at the time when it's too late to present it for the current frame - it gets delayed by one additional refresh cycle." This guaranteed one-frame latency penalty does not exist in Wayland's design.

Uncomposited X11 avoids this but loses modern desktop features (transparent windows, effects, multi-monitor synchronization).

**Source:** [Xaver Hugl - Gaming on Wayland](https://zamundaaa.github.io/wayland/2021/12/14/about-gaming-on-wayland.html)

### 1.3 Frame Scheduling and Rendering Efficiency

Wayland enables better design decisions that remove architectural restrictions:
- **Multi-monitor rendering:** Simultaneous rendering of multiple monitors at different refresh rates
- **Per-monitor VSync:** Each output can maintain its own refresh cycle
- **Variable refresh rate:** Native support without X11's limitations

X11 compositors must present "one big image for all outputs at once," limiting refresh rates to the slowest monitor and making adaptive sync with multi-monitor setups impossible.

**Source:** [Xaver Hugl - Gaming on Wayland](https://zamundaaa.github.io/wayland/2021/12/14/about-gaming-on-wayland.html)

---

## 2. Latency Analysis

### 2.1 Input-to-Photon Measurements

**David Justo's Hardware Measurement Study**

Test methodology:
- Arduino Pro Micro + TEMT6000 phototransistor sensor
- Hardware: AMD Ryzen 9 9950X3D + NVIDIA RTX 4090
- Display: Dell AW2725DF OLED, 360Hz
- Driver: NVIDIA 580.119.02 proprietary
- Desktop: KDE/KWin 6.5.4
- Frame rate: 400fps (engine-capped)

**Results (100 measurements per configuration):**

| Display Server | Median Latency |
|----------------|----------------|
| Native Wayland | 7.14ms         |
| XWayland       | 14.45ms        |
| X11            | 6.88ms         |
| Windows 11     | 6.91ms         |

**Critical finding:** "The extra lag came from running the game under XWayland rather than native Wayland." When forcing native Wayland backend with `SDL_VIDEO_DRIVER=wayland`, latency matched X11 performance. XWayland's translation layer approximately **doubles** input lag.

**Source:** [David Justo - Input-to-Photon Latency Measurement](https://davidjusto.com/articles/m2p-latency/)

### 2.2 Comparative Latency by Presentation Mode

**Xaver Hugl's measurements (120Hz display, median values):**

| Configuration      | FIFO (VSync) | Mailbox | Immediate (Tearing) |
|--------------------|--------------|---------|---------------------|
| X composited       | 59ms         | 37ms    | —                   |
| X uncomposited     | 41ms         | 38ms    | 19ms                |
| Wayland            | 49ms         | 36ms    | 20ms                |

**Key observations:**
- Wayland achieves latency comparable to uncomposited X11 in mailbox/immediate modes
- X11 with compositing adds significant overhead in FIFO mode
- Wayland maintains compositing benefits while matching uncomposited X11 performance

**Source:** [Xaver Hugl - Gaming on Wayland](https://zamundaaa.github.io/wayland/2021/12/14/about-gaming-on-wayland.html)

### 2.3 VSync Behavior

#### Presentation Modes Explained

- **FIFO (VSync):** Frame rate capped to display refresh rate, tear-free, higher latency
- **Mailbox:** Uncapped frame rate with synchronization (triple buffering), tear-free, lower latency
- **Immediate:** No synchronization, lowest latency, causes tearing

**Wayland default:** Most compositors enforce FIFO mode by default. This caused early complaints about "forced VSync" but can be overridden.

**Workarounds for Vulkan applications:**
```bash
MESA_VK_WSI_PRESENT_MODE=<fifo|relaxed|mailbox|immediate>
```

**Source:** [NVIDIA Forums - Forced VSync Discussion](https://forums.developer.nvidia.com/t/nvidia-bug-kde-wayland-games-are-force-vsynced/237880)

### 2.4 The "Wayland is Smoother" Claim

Wayland's perceived smoothness advantage comes from:

1. **Consistent frame pacing:** Wayland's architecture prevents the one-frame compositor delay present in X11
2. **Better multi-monitor synchronization:** Each output maintains proper timing
3. **Native VRR support:** Adaptive sync works more reliably
4. **Triple buffering in mailbox mode:** Reduces stutter while maintaining tear-free presentation

These benefits are most noticeable in:
- Multi-monitor setups
- VRR-enabled displays
- High-refresh-rate gaming (120Hz+)

**Sources:**
- [Xaver Hugl - Gaming on Wayland](https://zamundaaa.github.io/wayland/2021/12/14/about-gaming-on-wayland.html)
- [Phoronix - Ubuntu 25.04 Gaming](https://www.phoronix.com/review/ubuntu-2504-x11-gaming)

---

## 3. Tearing Control Protocol

### 3.1 Protocol Overview

**Protocol:** wp_tearing_control_v1 (Wayland Tearing Control Protocol)
**Status:** Version 1, Staging (as of 2026)
**Purpose:** Allow applications to request asynchronous page flips for reduced latency in exchange for accepting screen tearing

**How it works:**
- Applications request "async" presentation mode (vs default "vsync")
- Hint is double-buffered and applied on surface commit
- Compositors retain discretion to respect or ignore hints
- Designed for latency-sensitive applications (games, drawing tablets)

**Source:** [Wayland Explorer - Tearing Control Protocol](https://wayland.app/protocols/tearing-control-v1)

### 3.2 Compositor Support Status

**18 compositors support wp_tearing_control_v1**, including:

- **KDE KWin:** Version 6.4+ (tearing support for fullscreen clients)
- **GNOME Mutter:** Version 49.2+
- **Hyprland:** Version 0.52.1+
- **Sway:** Version 1.11+

**XWayland support:** Version 23.2+ implements tearing control for X11 applications running on Wayland compositors.

**Sources:**
- [Wayland Explorer - Tearing Control Protocol](https://wayland.app/protocols/tearing-control-v1)
- [Phoronix - XWayland 23.2](https://www.phoronix.com/news/XWayland-23.2-Released)

### 3.3 KDE KWin Implementation

**Plasma 6.4.0 changelog:**
- "kcm: reload kwin config when tearing option is changed"
- Tearing support for fullscreen clients implemented via merge request !927

**User interface:** System Settings includes "allow screen tearing in fullscreen" option for per-application control via window rules.

**Status:** Tearing support is functional but primarily targets fullscreen scenarios. Desktop-wide tearing options remain under discussion.

**Sources:**
- [KDE GitLab - KWin Tearing MR](https://invent.kde.org/plasma/kwin/-/merge_requests/927)
- [KDE Community - Plasma 6.4.0 Changelog](https://kde.org/announcements/changelogs/plasma/6/6.3.5-6.4.0/)

### 3.4 GNOME Mutter Implementation

**VRR focus over tearing:** Mutter prioritized Variable Refresh Rate implementation over traditional tearing control.

**GNOME 46+ (experimental):** VRR support introduced for X.Org and Wayland sessions
**GNOME 50 (stable):** VRR works seamlessly across both display servers

**Technical approach:**
- VRR synchronizes monitor refresh rate with content
- Eliminates tearing while reducing stuttering
- No upstream Wayland VRR protocol yet (compositor-specific implementations)

**Source:** [Tech Edu Byte - GNOME 50 VRR Support](https://www.techedubyte.com/gnome-50-vrr-support-latency-wayland-performance/)

---

## 4. NVIDIA on Wayland

### 4.1 Driver Requirements and Timeline

**Minimum requirements for functional Wayland:**
- **Driver version:** 555+ (explicit sync support)
- **Kernel version:** 6.8+ (explicit sync bug fixes)
- **XWayland version:** 24.1+ (linux-drm-syncobj-v1 support)
- **wayland-protocols:** 1.34+ (protocol definitions)

**Driver timeline:**
- **555.42.02 beta (May 2024):** First explicit sync support via linux-drm-syncobj-v1
- **555.58 stable (June 2024):** Stable release with explicit sync
- **560+:** Explicit sync for Vulkan Wayland WSI (not backported to 555)
- **580+ (current):** Mature Wayland support

**Sources:**
- [Phoronix - NVIDIA 555.42.02 Beta](https://www.phoronix.com/news/NVIDIA-555.42.02-Linux-Beta)
- [9to5Linux - NVIDIA 555.58](https://9to5linux.com/nvidia-555-58-linux-graphics-driver-released-with-explicit-sync-on-wayland)
- [GitHub - Hyprland Explicit Sync Issue](https://github.com/hyprwm/Hyprland/issues/4857)

### 4.2 Explicit Sync (linux-drm-syncobj-v1)

**What it is:** A Wayland protocol for explicit synchronization using DRM synchronization objects. Applications signal when rendering is complete to drivers, kernel, and compositors, preventing race conditions.

**Why NVIDIA needs it:** Prior to explicit sync, NVIDIA drivers experienced:
- Flickering
- Out-of-order frames
- Black screens
- General visual corruption

This affected both native Wayland and XWayland applications.

**Technical requirements:**
- Protocol merged into wayland-protocols 1.34 (2 years in development)
- Merged into Mesa, GNOME Mutter, KWin, and NVIDIA's EGL-Wayland library
- Kernel 6.8+ contains necessary bug fixes

**Sources:**
- [GNOME Mutter DRM Sync Obj Support](https://www.phoronix.com/news/GNOME-Linux-DRM-Sync-Obj-v1)
- [KDE KWin Explicit Sync MR](https://invent.kde.org/plasma/kwin/-/merge_requests/4693)
- [Arch Wiki - NVIDIA](https://wiki.archlinux.org/title/NVIDIA)

### 4.3 GBM vs EGLStreams History

**EGLStreams (legacy):** NVIDIA's proprietary buffer management API, rejected by most Wayland compositors in favor of industry-standard GBM.

**GBM support:** NVIDIA driver 495+ (2021) added GBM support alongside EGLStreams.

**Current status (2025-2026):**
- GBM is the standard across all compositors
- XWayland removed EGLStream backend in March 2024
- NVIDIA drivers now prioritize GBM
- EGLStreams deprecated and being phased out

**Source:** [Phoronix - XWayland Drops EGLStream](https://www.phoronix.com/news/XWayland-Drops-EGLStream)

### 4.4 NVIDIA-Specific Gaming Issues

**Known limitations from NVIDIA README (driver 580.126.09):**

**Framebuffer conflicts:**
- nvidia-drm and simpledrm both driving same display causes black screens, corruption, or flickering
- Workaround: Set `nvidia-drm.fbdev=1` kernel parameter

**Rendering limitations:**
- GLX front-buffer rendering does not work with XWayland
- Hardware overlays cannot be used by GLX applications with XWayland
- Indirect GLX not supported by XWayland

**Unsupported features:**
- SLI Mosaic
- Frame Lock and Genlock (partial VK_KHR_display support only)
- Swap Groups
- Stereo rendering
- Advanced display features (warp, blend, pixel shift, YUV420 emulation)

**Laptop dGPU switching:**
- Display mux switching works on X11
- No Wayland compositor currently supports this functionality
- Prevents automatic GPU switching for fullscreen games on laptops

**Kernel requirements:**
- `nvidia_drm.modeset=1` mandatory for all Wayland functionality
- Check status: `cat /sys/module/nvidia_drm/parameters/modeset` (should return "Y")

**Source:** [NVIDIA Wayland Known Issues](https://download.nvidia.com/XFree86/Linux-x86_64/580.126.09/README/wayland-issues.html)

### 4.5 NVIDIA VRR and Multi-Monitor

**VRR support:**
- Requires driver 545+
- Requires Volta GPU architecture or newer
- Works with KDE Plasma 5.22+ and GNOME 46+

**Multi-monitor challenges:**
- VRR may not activate on multi-monitor setups
- Single-monitor VRR generally works reliably
- Some users report VRR doesn't sync properly to games even in single-monitor configurations

**Source:** [NVIDIA Forums - VRR Multi-Monitor Issues](https://forums.developer.nvidia.com/t/vrr-not-working-on-wayland-with-2-screens-545-23-06/270259)

---

## 5. AMD/Intel on Wayland

### 5.1 AMD RADV Mesa Driver

**Hardware support:**
- All GCN and RDNA GPUs supported by Linux kernel
- GCN 1-2 (GFX6-7): Vulkan 1.3
- GFX8 and newer: Vulkan 1.4

**Configuration for older GPUs (GCN 1-2):**
```bash
# Kernel parameters required
radeon.si_support=0 radeon.cik_support=0 amdgpu.si_support=1 amdgpu.cik_support=1
```

**Recent issues (2025):**
- Mesa 24.3.1 caused system freezing on Vega graphics with Wayland (all compositors)
- Affected older GPUs without format modifier support
- Fixed in Mesa developers' subsequent releases
- Workaround: Downgrade to Mesa 24.2.7

**Current development focus:**
- AMD discontinued AMDVLK proprietary driver (May 2025)
- RADV is now the sole focus, fully mature
- Valve and AMD are top Mesa contributors
- Ray tracing performance improvements in progress

**Sources:**
- [Mesa RADV Documentation](https://docs.mesa3d.org/drivers/radv.html)
- [Arch Forums - Mesa 24.3.x Issues](https://bbs.archlinux.org/viewtopic.php?id=301798)
- [WebProNews - Mesa 2025 Drivers](https://www.webpronews.com/2025-mesa-drivers-surge-valve-amd-boost-linux-gaming/)

**Wayland-specific considerations:**
- No RADV-specific Wayland issues documented
- Standard Wayland gaming practices apply
- Performance on par with or better than X11
- VRR support works reliably with KDE/GNOME

### 5.2 Intel Arc

**Official support status:**
- **Ubuntu 22.04 with Wayland:** Officially supported configuration
- **Recommendation:** Intel officially recommends Wayland over Xorg for Arc GPUs

**Linux kernel support:**
- Linux 6.2+: Arc graphics no longer treated as experimental
- Out-of-box support in Ubuntu 25.04 and Fedora 42

**Recent hardware (2025):**
- Arc B580 Battlemage (December 2024 launch): Stable on Wayland
- Arc B570 (January 2025): Mature driver support in current kernels
- Community reports successful gaming on KDE Wayland with recent Arc GPUs

**General Intel GPU guidance:**
- Any Intel GPU from last decade: Wayland recommended
- Smoother desktop experience, tear-free rendering
- Better mixed-DPI display handling

**Sources:**
- [Intel Community - Arc A750 Linux Gaming](https://community.intel.com/t5/Graphics/Arc-A750-and-Linux-Gaming/td-p/1658899)
- [Intel Community - Arc Battlemage KDE Wayland Solution](https://community.intel.com/t5/Graphics/Intel-Arc-Bartelmagen-compleate-Solution-for-BigLinux-KDE/m-p/1720837)
- [Phoronix - Intel Battlemage Linux Performance](https://www.phoronix.com/review/intel-battlemage-linux-may2025)

**Known issues:**
- Xorg experiences glitches with Arc GPUs (Intel official notice)
- Wayland avoids these X11-specific rendering problems

**Source:** [Intel Support - Xorg Glitches with Arc](https://www.intel.com/content/www/us/en/support/articles/000092987/graphics/intel-arc-dedicated-graphics-family.html)

---

## 6. Diagnostic Tools and Troubleshooting

### 6.1 Checking Active Display Server

**Method 1: Check session type**
```bash
echo $XDG_SESSION_TYPE
```
Output: `wayland` or `x11`

**Method 2: Using loginctl (systemd systems)**
```bash
loginctl show-session $(loginctl | grep $(whoami) | awk '{print $1}') -p Type
```
Output: `Type=wayland` or `Type=x11` (or `Type=tty` for SSH sessions)

**Method 3: Check for Wayland socket**
```bash
echo $WAYLAND_DISPLAY
```
Output: `wayland-0`, `wayland-1`, etc. if Wayland is active

**Sources:**
- [nixCraft - Check Wayland or X11](https://www.cyberciti.biz/faq/howto-check-for-wayland-or-x11-with-my-linux-desktop/)
- [Arch Wiki - Wayland](https://wiki.archlinux.org/title/Wayland)

### 6.2 Detecting XWayland vs Native Wayland Applications

**Method 1: xprop (interactive)**
```bash
xprop
```
Then click on a window:
- **XWayland apps:** Display X11 properties (_NET_WM_PID, WM_CLASS, etc.)
- **Native Wayland apps:** No output or cursor doesn't change to crosshair

**Method 2: xlsclients (list all XWayland apps)**
```bash
xlsclients -l
```
Lists all X11 applications running via XWayland. Native Wayland apps won't appear.

**Method 3: xorg-xeyes (visual method)**
Install `xorg-xeyes` and run it. The eyes follow cursor movement only over XWayland windows, not native Wayland windows.

**Sources:**
- [Ask Ubuntu - Detecting XWayland](https://askubuntu-com.translate.goog/questions/1393618/how-can-i-tell-if-an-application-is-using-xwayland)
- [Arch Wiki - Wayland](https://wiki.archlinux.org/title/Wayland)

### 6.3 Environment Variables for Debugging

**Wayland protocol debugging:**
```bash
WAYLAND_DEBUG=1        # Enable Wayland protocol logging
WAYLAND_DEBUG=client   # Client-side debugging only
WAYLAND_DEBUG=server   # Server-side debugging only
```

**Force specific backend for applications:**

**GTK apps:**
```bash
GDK_BACKEND=wayland    # Force Wayland
GDK_BACKEND=x11        # Force X11/XWayland
```

**Qt apps:**
```bash
QT_QPA_PLATFORM=wayland              # Force Wayland
QT_QPA_PLATFORM=xcb                  # Force X11
QT_QPA_PLATFORM="wayland;xcb"        # Try Wayland, fallback to X11
```

**SDL2 apps:**
```bash
SDL_VIDEODRIVER=wayland              # Force Wayland
SDL_VIDEODRIVER="wayland,x11"        # Wayland with X11 fallback
```

**Vulkan presentation mode (Mesa):**
```bash
MESA_VK_WSI_PRESENT_MODE=<fifo|relaxed|mailbox|immediate>
```

**NVIDIA-specific:**
```bash
GBM_BACKEND=nvidia-drm
__GLX_VENDOR_LIBRARY_NAME=nvidia
```

**Sources:**
- [GitHub - Wayland Debug Tool](https://github.com/wmww/wayland-debug)
- [Ubuntu Discourse - Wayland Environment Variables](https://discourse.ubuntu.com/t/environment-variables-for-wayland-hackers/12750)
- [Arch Wiki - Wayland](https://wiki.archlinux.org/title/Wayland)

### 6.4 Common Symptoms and Fixes

#### Screen Tearing

**Symptoms:**
- Horizontal line artifacts during fast motion
- Image appears "split" at specific horizontal positions

**Causes:**
- Compositor doesn't support tearing control protocol
- Application using immediate/mailbox presentation without tearing support
- VSync disabled without tearing compensation

**Fixes:**
1. **Enable VSync in application:** Forces FIFO mode, eliminates tearing
2. **Use compositor with tearing support:** KWin 6.4+, Mutter 49.2+, Sway 1.11+
3. **Enable VRR/Adaptive Sync:** Eliminates tearing while maintaining low latency
4. **Fallback to X11:** For compositors without tearing support

**Source:** [KDE Bug #450914 - Forced VSync](https://bugs.kde.org/show_bug.cgi?id=450914)

#### Mouse Not Captured (Escaping Fullscreen Game)

**Symptoms:**
- Cursor leaves game window in fullscreen
- Mouse moves to other monitors during gameplay
- Camera view stops responding at screen edges

**Causes:**
- Wayland pointer constraints not implemented by compositor
- Game doesn't properly request pointer lock
- Multi-monitor configuration issues

**Fixes:**
1. **Check compositor support:** Ensure pointer constraints protocol is implemented
2. **Use Gamescope:** Run game through Gamescope without `--expose-wayland` flag
   ```bash
   gamescope -- <game-command>
   ```
3. **Force X11 for specific game:** Use environment variables
   ```bash
   SDL_VIDEODRIVER=x11 <game-command>
   GDK_BACKEND=x11 <game-command>
   ```
4. **Switch to X11 session:** Global fallback for persistent issues

**Sources:**
- [Arch Forums - Proton Mouse Capture](https://bbs.archlinux.org/viewtopic.php?id=293560)
- [KDE Bug #441464 - Screen Edges in Fullscreen](https://bugs.kde.org/show_bug.cgi?id=441464)

#### Black Screen on Fullscreen

**Symptoms:**
- Game launches but shows only black screen
- Monitor appears to lose signal repeatedly
- Screen goes dark then reconnects in cycles

**Causes:**
- VRR enabled with compositor bugs
- Direct scanout failures
- NVIDIA explicit sync issues (pre-555 drivers)
- DMA-BUF modifier incompatibilities

**Fixes:**

**For VRR-related issues:**
1. Disable VRR/Adaptive Sync in compositor settings
2. Force compositor to stay active (disable unredirection):
   ```bash
   # GNOME extension to disable unredirection
   # KDE: disable in compositor settings
   ```

**For NVIDIA users:**
1. Ensure driver 555+ installed
2. Verify explicit sync requirements:
   ```bash
   # Check kernel version (need 6.8+)
   uname -r

   # Check modeset enabled
   cat /sys/module/nvidia_drm/parameters/modeset
   # Should output "Y"
   ```
3. Add kernel parameter if needed:
   ```
   nvidia_drm.modeset=1
   ```

**For general fullscreen issues:**
1. Try windowed mode first to isolate issue
2. Check compositor logs:
   ```bash
   journalctl -b 0 --grep "renderer"
   ```
3. Test with different application backend:
   ```bash
   SDL_VIDEODRIVER=x11 <game>
   ```

**Sources:**
- [Arch Forums - NVIDIA Prime Wayland Black Screen](https://bbs.archlinux.org/viewtopic.php?id=305915)
- [NVIDIA Forums - VRR Black Screen](https://forums.developer.nvidia.com/t/black-screen-with-fullscreen-applications-after-suspend-with-vrr-enabled-on-wayland/357570)
- [KDE Discuss - Fullscreen Black Screen](https://discuss.kde.org/t/black-screen-on-fullscreen-with-wayland/29368)

#### Poor Performance / Stuttering

**Symptoms:**
- Lower FPS than expected
- Periodic stuttering or frame drops
- Input feels sluggish

**Diagnostic steps:**

1. **Check if running via XWayland:**
   ```bash
   xlsclients -l | grep <game-name>
   ```
   If game appears, it's using XWayland (adds ~7ms latency)

2. **Force native Wayland backend:**
   ```bash
   SDL_VIDEODRIVER=wayland <game>
   ```

3. **Check presentation mode:**
   - FIFO (VSync) caps framerate to refresh rate
   - Try mailbox or immediate modes:
   ```bash
   MESA_VK_WSI_PRESENT_MODE=mailbox <game>
   ```

4. **AMD-specific (kernel 6.11.2+ performance regression):**
   ```bash
   # Add to kernel parameters
   amdgpu.dcdebugmask=0x400
   ```

5. **Verify compositor version:**
   - KDE Plasma: 6.1+ for gaming optimizations
   - GNOME: 46+ for VRR, 50+ for stable VRR

6. **Check system resources:**
   ```bash
   # Monitor GPU usage
   radeontop    # AMD
   nvidia-smi   # NVIDIA
   intel_gpu_top # Intel
   ```

**Sources:**
- [David Justo - Latency Measurements](https://davidjusto.com/articles/m2p-latency/)
- [Arch Wiki - Wayland](https://wiki.archlinux.org/title/Wayland)

#### Multi-Monitor Issues

**Different refresh rates:**
- **X11 limitation:** All monitors locked to slowest refresh rate
- **Wayland advantage:** Each monitor maintains independent refresh rate
- **Requirement:** Wayland session with modern compositor (KDE 6+, GNOME 46+)

**VRR on multiple monitors:**
- Single monitor: Generally works
- Multiple monitors: May not activate (compositor-dependent)
- **Workaround:** Test single-monitor gaming setup

**Mixed DPI displays:**
- Wayland handles per-monitor scaling natively
- X11 struggles with fractional scaling
- **Recommendation:** Use Wayland for mixed-DPI setups

**Source:** [Xaver Hugl - Gaming on Wayland](https://zamundaaa.github.io/wayland/2021/12/14/about-gaming-on-wayland.html)

---

## 7. X-Plane 12 Specific Considerations

### 7.1 X-Plane 12 Technical Profile

**Graphics API:** Vulkan (primary on Linux and Windows)
**Availability:** Native Linux version available
**SDK compatibility:** Primarily uses Vulkan API, designed for cross-platform compatibility

**Driver requirements:**
- NVIDIA: Proprietary driver 510+ for Vulkan support
- AMD: Mesa 22.0+ for Vulkan support
- Intel: Modern Mesa with Arc support (kernel 6.2+ for Battlemage/Arc)

**Sources:**
- [Phoronix - X-Plane 12 Beta](https://www.phoronix.com/news/X-Plane-12-Beta)
- [X-Plane Forums - Wayland Discussion](https://forums.x-plane.org/forums/topic/338406-linux-wayland/)

### 7.2 X-Plane 12 Wayland Behavior

**Current status (as of 2026):**
- X-Plane 12 runs on Linux distributions that have transitioned to Wayland
- Community discussions indicate need for better Wayland support
- Bug affecting X-Plane 11 with offloaded graphics does not occur in X-Plane 12 Demo

**XWayland acceleration:**
- NVIDIA driver facilitates accelerated 3D rendering for XWayland applications
- Suboptimal fallback path results in degraded performance if requirements not met
- Proper driver configuration essential (modeset, explicit sync)

**SDL considerations:**
- If X-Plane uses SDL2 for window management, backend selection matters:
  - Default SDL2 behavior may prefer X11 over Wayland
  - Can be overridden with `SDL_VIDEODRIVER=wayland`
- Native Wayland backend reduces latency by ~7ms vs XWayland

**Sources:**
- [NVIDIA README - XWayland OpenGL/Vulkan](https://download.nvidia.com/XFree86/Linux-x86_64/510.39.01/README/xwayland.html)
- [X-Plane Forums - Optimus and Wayland](https://forums.x-plane.org/forums/topic/295526-xp12-linux-optimus-nvidiaamd-and-wayland/)

### 7.3 Recommendations for X-Plane 12

**NVIDIA users:**
1. Ensure driver 555+ installed with kernel 6.8+
2. Verify `nvidia_drm.modeset=1` active
3. Use compositor with explicit sync support (KWin 6.4+, Mutter 49.2+)
4. Consider X11 for older GPUs (pre-Volta) or driver versions <555

**AMD users:**
1. Wayland recommended (mature RADV support)
2. Ensure Mesa 24.2.7+ (avoid 24.3.1 if using Vega)
3. Enable VRR in compositor for adaptive sync benefits
4. Multi-monitor setups: Wayland significantly better than X11

**Intel Arc users:**
1. Wayland strongly recommended (Intel's official stance)
2. Kernel 6.2+ required (6.8+ preferred)
3. Avoid X11 (known glitching issues)

**General optimization:**
1. **Force native Wayland if performance issues occur:**
   ```bash
   SDL_VIDEODRIVER=wayland ./X-Plane
   ```

2. **For VRR displays:**
   - Enable adaptive sync in compositor settings
   - Disable in-game VSync (let compositor handle it)

3. **Multi-monitor flight sim setups:**
   - Wayland handles different refresh rates better
   - X11 may be more stable for complex (3+ monitor) configurations with older GPUs

4. **Troubleshooting black screens:**
   - Try disabling VRR temporarily
   - Verify fullscreen mode settings
   - Check compositor logs for DMA-BUF errors

---

## 8. Recommendation Framework

### 8.1 When to Use Wayland (Daily Desktop + Gaming)

**Ideal candidates:**
- AMD Radeon GPU users (GCN 3+ or RDNA)
- Intel integrated/Arc GPU users
- NVIDIA users with driver 555+ and Volta+ GPUs
- Multi-monitor setups (especially different refresh rates)
- VRR/FreeSync/G-Sync display owners
- Modern desktop environments (KDE Plasma 6+, GNOME 46+)

**Benefits in these scenarios:**
- Better multi-monitor handling (independent refresh rates)
- Native VRR support across multiple displays
- Lower latency than composited X11
- Modern security model (application isolation)
- Better fractional/mixed-DPI scaling
- Active development and long-term support

**Requirements:**
- Recent compositor (KDE 6.1+, GNOME 46+, Sway 1.11+)
- Modern kernel (6.8+ for NVIDIA, 6.2+ for general stability)
- Updated Mesa (24.2.7+ for AMD)
- Applications with native Wayland or good XWayland support

### 8.2 When to Stick with X11

**Scenarios where X11 is currently better:**

**NVIDIA users with:**
- GPUs older than Volta architecture
- Driver versions below 555
- Kernels older than 6.8
- Need for unsupported features (SLI, stereo rendering, frame lock)

**Multi-monitor edge cases:**
- 3+ monitor setups on older hardware
- Professional color-critical work (some apps lack Wayland ICC support)
- Applications requiring precise color management

**Application compatibility:**
- Legacy software without XWayland compatibility
- Professional software with X11-specific features
- Screen recording/streaming tools not yet Wayland-native

**Gaming-specific scenarios:**
- Games with known pointer constraint issues on Wayland
- Older games that don't work well via XWayland
- Competitive gaming where every millisecond matters (uncomposited X11 still lowest latency)

**Laptop dGPU configurations:**
- NVIDIA laptops needing mux switching
- Optimus configurations on older drivers
- Power management concerns with Wayland overhead

### 8.3 Per-Application XWayland Fallback

**Strategy:** Run Wayland session but force problematic applications to use X11 via XWayland.

**Use cases:**
- Specific game has mouse capture issues on Wayland
- Application has fullscreen black screen bug
- Performance regression in specific title

**Implementation:**

**For SDL2 games:**
```bash
SDL_VIDEODRIVER=x11 <game>
```

**For GTK applications:**
```bash
GDK_BACKEND=x11 <application>
```

**For Qt applications:**
```bash
QT_QPA_PLATFORM=xcb <application>
```

**For Steam games (persistent setting):**
1. Right-click game in library
2. Properties → Launch Options
3. Add: `SDL_VIDEODRIVER=x11 %command%`

**Benefits:**
- Keep Wayland's advantages for desktop and most games
- Isolate compatibility issues to specific applications
- Easy A/B testing to identify XWayland overhead

**Drawbacks:**
- XWayland adds ~7ms latency vs native Wayland
- Still benefits from Wayland's multi-monitor improvements
- Not as optimized as native X11 session

### 8.4 Migration Path Recommendation

**Phase 1: Assessment (1-2 weeks)**
1. Check current setup compatibility:
   ```bash
   # GPU driver versions
   nvidia-smi | grep "Driver Version"  # NVIDIA
   glxinfo | grep "OpenGL version"      # AMD/Intel

   # Kernel version
   uname -r

   # Current session type
   echo $XDG_SESSION_TYPE
   ```

2. Verify compositor versions:
   - KDE: `plasmashell --version` (need 6.1+)
   - GNOME: `gnome-shell --version` (need 46+)

3. Test Wayland session:
   - Log out, select Wayland session at login
   - Use desktop normally for a week
   - Note any application issues

**Phase 2: Gaming Testing (2-4 weeks)**
1. Test primary games on Wayland
2. Document issues:
   - Performance regressions
   - Mouse capture problems
   - Fullscreen issues
   - VRR behavior

3. For each issue, test workarounds:
   - Native Wayland backend forcing
   - XWayland fallback
   - Presentation mode changes
   - Compositor settings adjustments

**Phase 3: Decision**

**Stay on Wayland if:**
- Most/all games work acceptably
- Desktop experience is better
- Multi-monitor setup improved
- VRR works reliably

**Revert to X11 if:**
- Critical application incompatibility
- Significant performance regression
- GPU/driver not yet mature enough
- Unresolved stability issues

**Hybrid approach:**
- Wayland for daily use
- X11 session available for specific games/applications
- Use display manager session switcher as needed

**Phase 4: Optimization (ongoing)**
1. Keep compositor/drivers updated
2. Report bugs to compositor developers
3. Re-test problematic games after updates
4. Participate in beta testing for improvements

---

## 9. Summary: Key Takeaways for X-Plane Documentation

### 9.1 Performance

- **Wayland ≈ X11** for native Wayland applications (within margin of error)
- **XWayland adds ~7ms latency** vs native (measureable but acceptable for most)
- **Wayland > X11** for multi-monitor gaming (independent refresh rates)
- **VRR support** is better on Wayland (multi-monitor, stability)

### 9.2 Hardware Recommendations

| GPU Vendor | Wayland Status | Minimum Requirements | Notes |
|------------|----------------|----------------------|-------|
| AMD (RADV) | Excellent | Mesa 24.2.7+, any modern kernel | Avoid Mesa 24.3.1 on Vega GPUs |
| NVIDIA | Good (with caveats) | Driver 555+, Kernel 6.8+, Volta+ GPU | Explicit sync essential |
| Intel | Excellent | Kernel 6.2+, modern Mesa | Intel officially recommends Wayland |

### 9.3 Compositor Requirements

| Compositor | Minimum Version | Tearing Support | VRR Support | Notes |
|------------|-----------------|-----------------|-------------|-------|
| KDE Plasma | 6.1 (6.4+ recommended) | 6.4+ | 5.22+ | Best gaming support |
| GNOME | 46 (50+ recommended) | 49.2+ | 46+ (exp), 50+ (stable) | VRR focus over tearing |
| Sway | 1.11+ | 1.11+ | No NVIDIA VRR | Lightweight, tiling WM |

### 9.4 Troubleshooting Priority

1. **Black screen** → Check VRR settings, verify NVIDIA explicit sync (555+, kernel 6.8+)
2. **Screen tearing** → Enable VSync or use tearing-capable compositor (KWin 6.4+)
3. **Mouse escaping** → Use Gamescope wrapper or force X11 backend for specific game
4. **Poor performance** → Verify native Wayland vs XWayland, check presentation mode
5. **Multi-monitor issues** → Use Wayland (X11 fundamentally limited here)

### 9.5 X-Plane 12 Specific Guidance

**Recommended configuration:**
- **AMD/Intel users:** Wayland preferred
- **NVIDIA users (555+ driver, Volta+ GPU):** Wayland recommended, X11 acceptable
- **NVIDIA users (older):** X11 recommended
- **Multi-monitor cockpit setups:** Wayland for different refresh rates, test stability

**Performance optimization:**
```bash
# Force native Wayland if using SDL2
SDL_VIDEODRIVER=wayland ./X-Plane

# NVIDIA environment variables (if needed)
GBM_BACKEND=nvidia-drm __GLX_VENDOR_LIBRARY_NAME=nvidia ./X-Plane
```

**Troubleshooting checklist:**
1. Verify driver versions match minimum requirements
2. Check `nvidia_drm.modeset=1` for NVIDIA
3. Test VRR disabled if black screen occurs
4. Try X11 session if persistent fullscreen issues
5. Use `xlsclients -l` to verify if running via XWayland

---

## 10. Source Quality Assessment

### 10.1 Primary Sources Used

**Tier 1 (Authoritative):**
- Official documentation (NVIDIA, Mesa, Wayland protocols)
- Kernel documentation
- Distribution wikis (Arch, Debian)
- Official project repositories (GitHub: KWin, Mutter, wayland-protocols)

**Tier 2 (Technical/Reliable):**
- Phoronix benchmarks (controlled, reproducible)
- Individual developer blogs (Xaver Hugl/KDE, David Justo with hardware measurements)
- Distribution forums with technical depth (Arch, EndeavourOS)

**Tier 3 (Anecdotal but Useful):**
- User bug reports (KDE, GNOME bug trackers)
- NVIDIA developer forums
- Community discussions (limited to pattern identification)

### 10.2 Limitations and Gaps

**Missing quantitative data:**
- Specific X-Plane 12 benchmarks comparing Wayland vs X11
- FPS differences across various GPU configurations
- Detailed frame-time analysis

**Version-specific information:**
- KWin tearing implementation details across 6.2-6.4 minor versions
- Precise NVIDIA driver changelog for 560, 565, 570, 580
- Mesa version-specific Wayland optimizations

**Incomplete coverage:**
- Wayland gaming on non-mainstream compositors (wlroots-based beyond Sway)
- Proton/Wine-specific Wayland integration status
- Steam Deck/Gamescope architecture details

### 10.3 Recommendations for Documentation

**What can be stated confidently:**
- General Wayland vs X11 performance trends (backed by Phoronix)
- NVIDIA explicit sync requirements (well-documented)
- Latency measurements (hardware-verified by David Justo)
- Compositor version requirements (from official changelogs)

**What requires hedging:**
- Specific FPS improvements (varies by game, config)
- Individual user experience (hardware-dependent)
- Future compatibility (ongoing development)

**What should be tested before documenting:**
- X-Plane 12 specific behavior on Wayland
- Performance with various GPU vendors
- Multi-monitor X-Plane setups on Wayland vs X11

---

## Sources

### Performance and Benchmarking
- [Phoronix - Ubuntu 25.04 Desktop Gaming Benchmarks](https://www.phoronix.com/review/ubuntu-2504-x11-gaming)
- [Phoronix Forums - AMD Radeon KDE Plasma 6.0 Parity](https://www.phoronix.com/forums/forum/software/desktop-linux/1456174-amd-radeon-linux-gaming-performance-at-parity-between-kde-plasma-6-0-x11-vs-wayland)
- [OpenBenchmarking - GNOME vs KDE Wayland vs X.Org](https://openbenchmarking.org/result/2112278-PTS-TESTRUN718)

### Latency and Technical Analysis
- [David Justo - Input-to-Photon Latency Measurement](https://davidjusto.com/articles/m2p-latency/)
- [Xaver Hugl (KDE) - Gaming on Wayland](https://zamundaaa.github.io/wayland/2021/12/14/about-gaming-on-wayland.html)
- [Mort's Coffee - Wayland vs X11 Input Latency](https://mort.coffee/home/wayland-input-latency/)

### Direct Scanout and Compositor Technology
- [Phoronix - GNOME Direct Scanout Support](https://www.phoronix.com/news/GNOME-Subsurface-Scanout)
- [Phoronix Forums - GNOME Direct Scanout Discussion](https://www.phoronix.com/forums/forum/software/desktop-linux/1301099-gnome-on-wayland-lands-improved-handling-for-direct-scanout-support)

### Tearing Control Protocol
- [Wayland Explorer - Tearing Control v1](https://wayland.app/protocols/tearing-control-v1)
- [Phoronix - XWayland 23.2 Released](https://www.phoronix.com/news/XWayland-23.2-Released)
- [KDE GitLab - KWin Tearing Support MR](https://invent.kde.org/plasma/kwin/-/merge_requests/927)

### NVIDIA Wayland Support
- [NVIDIA README - Wayland Known Issues (580.126.09)](https://download.nvidia.com/XFree86/Linux-x86_64/580.126.09/README/wayland-issues.html)
- [Phoronix - NVIDIA 555.42.02 Beta Explicit Sync](https://www.phoronix.com/news/NVIDIA-555.42.02-Linux-Beta)
- [9to5Linux - NVIDIA 555.58 Stable Release](https://9to5linux.com/nvidia-555-58-linux-graphics-driver-released-with-explicit-sync-on-wayland)
- [Phoronix - GNOME Mutter DRM Sync Obj Support](https://www.phoronix.com/news/GNOME-Linux-DRM-Sync-Obj-v1)
- [GitHub - NVIDIA EGL-Wayland Explicit Sync PR](https://github.com/NVIDIA/egl-wayland/pull/104)
- [KDE GitLab - KWin Explicit Sync MR](https://invent.kde.org/plasma/kwin/-/merge_requests/4693)
- [Phoronix - XWayland Drops EGLStream](https://www.phoronix.com/news/XWayland-Drops-EGLStream)

### AMD/Mesa Support
- [Mesa Documentation - RADV Driver](https://docs.mesa3d.org/drivers/radv.html)
- [Arch Forums - Mesa 24.3.x Vega Issues](https://bbs.archlinux.org/viewtopic.php?id=301798)
- [WebProNews - Mesa 2025 Drivers Surge](https://www.webpronews.com/2025-mesa-drivers-surge-valve-amd-boost-linux-gaming/)
- [GamingOnLinux - Mesa RADV Ray Tracing Performance](https://www.gamingonlinux.com/2026/01/mesa-radv-driver-on-linux-looks-set-for-a-big-ray-tracing-performance-boost/)

### Intel Arc Support
- [Intel Community - Arc A750 Linux Gaming](https://community.intel.com/t5/Graphics/Arc-A750-and-Linux-Gaming/td-p/1658899)
- [Intel Community - Arc Battlemage KDE Wayland](https://community.intel.com/t5/Graphics/Intel-Arc-Bartelmagen-compleate-Solution-for-BigLinux-KDE/m-p/1720837)
- [Phoronix - Intel Battlemage Linux Gaming](https://www.phoronix.com/review/intel-battlemage-linux-may2025)
- [Intel Support - Xorg Glitches with Arc](https://www.intel.com/content/www/us/en/support/articles/000092987/graphics/intel-arc-dedicated-graphics-family.html)

### VRR and Multi-Monitor
- [Arch Wiki - Variable Refresh Rate](https://wiki.archlinux.org/title/Variable_refresh_rate)
- [Tech Edu Byte - GNOME 50 VRR Support](https://www.techedubyte.com/gnome-50-vrr-support-latency-wayland-performance/)
- [Tech Edu Byte - Mutter 50 VRR Enhancements](https://www.techedubyte.com/mutter-50-vrr-enhancements-wayland-performance/)
- [NVIDIA Forums - VRR Multi-Monitor Issues](https://forums.developer.nvidia.com/t/vrr-not-working-on-wayland-with-2-screens-545-23-06/270259)

### VSync and Presentation Modes
- [NVIDIA Forums - Forced VSync Discussion](https://forums.developer.nvidia.com/t/nvidia-bug-kde-wayland-games-are-force-vsynced/237880)
- [KDE Bug #450914 - Forced VSync](https://bugs.kde.org/show_bug.cgi?id=450914)

### KDE Plasma Development
- [KDE - Plasma 6.4.0 Changelog](https://kde.org/announcements/changelogs/plasma/6/6.3.5-6.4.0/)
- [KDE - Plasma 6.3.6 Changelog](https://kde.org/announcements/changelogs/plasma/6/6.3.5-6.3.6/)
- [9to5Linux - KDE Plasma 6.5.3 VRR Improvements](https://9to5linux.com/kde-plasma-6-5-3-improves-visual-smoothness-on-multi-monitor-vrr-setups)
- [Linux Journal - KDE Plasma 6 Wayland Improvements](https://www.linuxjournal.com/content/kde-plasma-6-wayland-payoff-years-plumbing)

### Diagnostic Tools and Environment Variables
- [Arch Wiki - Wayland](https://wiki.archlinux.org/title/Wayland)
- [GitHub - Wayland Debug Tool](https://github.com/wmww/wayland-debug)
- [Ubuntu Discourse - Environment Variables for Wayland](https://discourse.ubuntu.com/t/environment-variables-for-wayland-hackers/12750)
- [nixCraft - Check Wayland or X11](https://www.cyberciti.biz/faq/howto-check-for-wayland-or-x11-with-my-linux-desktop/)
- [Adams Desk - Check Display Server](https://www.adamsdesk.com/posts/find-display-server-wayland-xorg/)

### Troubleshooting
- [Arch Forums - Proton Mouse Capture Issues](https://bbs.archlinux.org/viewtopic.php?id=293560)
- [KDE Bug #441464 - Screen Edges in Fullscreen](https://bugs.kde.org/show_bug.cgi?id=441464)
- [Arch Forums - NVIDIA Prime Wayland Black Screen](https://bbs.archlinux.org/viewtopic.php?id=305915)
- [NVIDIA Forums - VRR Black Screen After Suspend](https://forums.developer.nvidia.com/t/black-screen-with-fullscreen-applications-after-suspend-with-vrr-enabled-on-wayland/357570)
- [KDE Discuss - Fullscreen Black Screen](https://discuss.kde.org/t/black-screen-on-fullscreen-with-wayland/29368)

### X-Plane Specific
- [Phoronix - X-Plane 12 Vulkan Beta](https://www.phoronix.com/news/X-Plane-12-Beta)
- [X-Plane Forums - Linux Wayland Discussion](https://forums.x-plane.org/forums/topic/338406-linux-wayland/)
- [X-Plane Forums - Optimus and Wayland](https://forums.x-plane.org/forums/topic/295526-xp12-linux-optimus-nvidiaamd-and-wayland/)
- [NVIDIA README - XWayland OpenGL/Vulkan](https://download.nvidia.com/XFree86/Linux-x86_64/510.39.01/README/xwayland.html)

### SDL and Application Backend
- [GitHub - SDL Issue #4988 - Wayland Default](https://github.com/libsdl-org/SDL/issues/4988)
- [GamingOnLinux - SDL 3 Wayland Preference](https://www.gamingonlinux.com/2024/03/sdl-3-will-prefer-wayland-over-x11-if-certain-protocols-are-available/)
- [NVIDIA Forums - SDL Wayland Performance](https://forums.developer.nvidia.com/t/performance-loss-wine-walyand-sdl-wayland/353495)

### Compositor Support Documentation
- [KDE Community Wiki - Plasma Wayland NVIDIA](https://community.kde.org/Plasma/Wayland/Nvidia)
- [Arch Wiki - NVIDIA](https://wiki.archlinux.org/title/NVIDIA)
- [Wayland Explorer - DRM Syncobj Protocol](https://wayland.app/protocols/linux-drm-syncobj-v1)

---

**Research completed:** 2026-02-09
**Total primary sources:** 60+
**Confidence level:** High for general Wayland gaming guidance, Medium for X-Plane 12 specifics (requires hands-on testing)
