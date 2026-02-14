# X-Plane Configuration on Linux

X-Plane 12 is a cross-platform application — the general graphics settings (textures, shadows, clouds, anti-aliasing) work the same on all operating systems and are documented in the [official documentation](https://www.x-plane.com/kb/configuring-the-rendering-options/). This page covers exclusively what is **different** on Linux.

## Vulkan and Zink

X-Plane 12 uses Vulkan exclusively as its rendering API. There is no OpenGL fallback.

**Driver Requirements (Vulkan 1.3)**

| GPU | Driver | Minimum Version |
|-----|--------|----------------|
| NVIDIA | Proprietary driver | 510+ |
| AMD | Mesa RADV | 22.0+ |
| Intel Arc | Mesa ANV | Supported in recent versions |

For NVIDIA driver installation and optimization see [Nvidia Drivers](../nvidia.md).

### Zink — Plugin Compatibility

Many X-Plane plugins use OpenGL for their rendering (e.g. cockpit displays, overlays). Since X-Plane 12 uses Vulkan exclusively, the plugins' OpenGL rendering needs to be translated. X-Plane ships the [Zink](../glossary.md#zink) driver for this purpose — a translation layer that converts OpenGL commands into Vulkan commands.

**Why this is particularly relevant on Linux**

- Without Zink, the driver attempts to coordinate OpenGL and Vulkan simultaneously (Native Interop). This cost up to 10 ms per frame, in extreme cases 30 ms
- With Zink: measurably 50 FPS → 80 FPS in Laminar Research tests
- AMD GPUs ([RADV](../glossary.md#radv)) benefit the most — native OpenGL/Vulkan interop was particularly problematic on Mesa
- NVIDIA: Zink support has a turbulent history — status changes between releases and may change with updates

**Known limitation:** Shared OpenGL Contexts for background processing in plugins are not fully stable with Zink. For general OpenGL error diagnostics with plugins, `--debug_gl` can be useful.

## Shader Cache

X-Plane 12 uses two independent shader cache systems on Linux. If graphics glitches occur after a driver update or performance is unexplainably poor, clearing one or both caches can help.

### X-Plane's Own Cache

Contains pre-compiled Vulkan pipeline objects.

- **Path:** `<X-Plane 12>/Output/shadercache/vulkan/`
- To clear: delete the directory contents. Will be automatically rebuilt on next start (may take several minutes)

### Mesa Shader Cache (AMD/Intel only)

The Mesa driver stack additionally caches shaders compiled by the ACO compiler.

- **Default path:** `~/.cache/mesa_shader_cache/` (from Mesa 24.2: `~/.cache/mesa_shader_cache_db/`)
- **Default maximum:** 1 GB

Redirect cache to faster SSD or increase size:

```bash
export MESA_SHADER_CACHE_DIR=/path/to/fast/ssd/mesa_cache
export MESA_SHADER_CACHE_MAX_SIZE=2G
```

NVIDIA uses its own internal shader cache that is not configured through Mesa.

## Environment Variables

Some Mesa/RADV variables can be useful for X-Plane on Linux. Set them via launch script or directly before the command:

```bash
MESA_VK_WSI_PRESENT_MODE=mailbox ./X-Plane-x86_64
```

**Useful Variables (AMD/Intel with Mesa)**

| Variable | Recommended Value | Effect |
|----------|------------------|--------|
| `MESA_VK_WSI_PRESENT_MODE` | `mailbox` | Tear-free with low latency. Alternative: `immediate` (lowest latency, but tearing) |
| `MESA_SHADER_CACHE_MAX_SIZE` | `2G` | Increase shader cache (default: 1 GB) |
| `MESA_SHADER_CACHE_DIR` | Path | Redirect shader cache to faster storage |

!!! warning "NVIDIA: `__GL_*` variables — do not set blindly"
    `__GL_THREADED_OPTIMIZATIONS` and `__GL_YIELD` affect OpenGL only and have **no effect** under X-Plane 12 (Vulkan).

    `__GL_SYNC_TO_VBLANK`, however, does affect Vulkan — but only when VSync is active (FIFO present mode). Setting `__GL_SYNC_TO_VBLANK=0` overrides VSync at the driver level even though X-Plane has it enabled. **Recommendation:** Control VSync through X-Plane settings, not environment variables.

    Other `__GL_*` variables with Vulkan effect: `__GL_SHARPEN_ENABLE` (image sharpening) and `__GL_SHOW_GRAPHICS_OSD` (performance overlay).

!!! note "Experimental: NVIDIA Smooth Motion (RTX 40/50)"
    `NVPRESENT_ENABLE_SMOOTH_MOTION=1` enables AI-based frame interpolation at the driver level. The NVIDIA driver uses Tensor Cores to generate an interpolated intermediate frame between each rendered frame, effectively doubling the perceived frame rate — without any engine integration.

    X-Plane 12 has no native DLSS Frame Generation, making Smooth Motion currently the only option for driver-based frame generation. Requires at least driver 580.82 (RTX 40) or 575.51 (RTX 50). Low Latency Mode is automatically enabled to compensate for the additional input latency.

    Launch via script: `NVPRESENT_ENABLE_SMOOTH_MOTION=1 ./X-Plane-x86_64`

    **Known limitations:** Reports of flickering, Vulkan errors and artifacts during rapid view changes exist in the X-Plane community. Quality is below native DLSS Frame Generation since no motion vectors from the engine are used. That said, the author of this documentation has achieved very good results with Smooth Motion under X-Plane — it is worth trying out.

!!! note "Experimental: Variable Rate Shading"
    `RADV_FORCE_VRS=2x2` can provide 10-30% FPS gain on RDNA2+ GPUs (RX 6000 and newer), but reduces image quality. **Not tested with X-Plane** — artifacts possible.

## Display Server

X-Plane 12 has no native Wayland support. For details on session selection, latency measurements, and GPU-specific recommendations, see the [Display Server](../displayserver.md) guide.

!!! tip "Recommendation: Use X11 session"
    Under X11, X-Plane communicates directly with the X server — no translation, no overhead. Details: [X11 Session for X-Plane](../displayserver_x11.md)

For fullscreen issues under Wayland, `--window=1920x1080` can serve as a workaround (see [Troubleshooting](#diagnostic-launch-with-cli-parameters)).

## Audio

X-Plane 12 uses [FMOD](../glossary.md#fmod) Studio 2.02 as its audio engine. Under Debian 12 (PulseAudio), audio typically works without configuration.

!!! tip "PipeWire: No sound?"
    Under PipeWire (Debian 13 default, in Debian 12 default for GNOME, optional for other DEs), FMOD sometimes fails to detect the audio system. FMOD checks `/usr/bin/pulseaudio --check` — on pure PipeWire systems this binary does not exist.

    Solution:

    ```bash
    sudo apt install pipewire-pulse pipewire-alsa
    # If that alone is not sufficient:
    sudo ln -s /bin/true /usr/bin/pulseaudio
    ```

    Official troubleshooting article: [PipeWire Audio Issues](https://www.x-plane.com/kb/troubleshooting-audio-issues-with-pipewire-on-linux/)

    For diagnostics: `--no_sound` starts X-Plane without audio initialization and isolates audio problems.

## Controllers

X-Plane detects controllers on Linux via SDL2 with the [evdev](../glossary.md#evdev) backend (`/dev/input/event*`). For this to work, the user needs read permissions on the input devices — **X-Plane must never be run as root**.

### udev Rules

If a controller is not detected, permissions are usually missing. The official guide covers the basics: [Using Joysticks on Linux](https://www.x-plane.com/kb/using-joysticks-x-plane-11-linux-systems/)

Beyond that, custom udev rules can set permissions, create stable symlinks and lock down device assignment — particularly useful for multi-controller setups.

**Step 1: Identify device IDs**

List connected USB controllers:

```bash
lsusb | grep -i -E "thrustmaster|logitech|saitek|vkb|virpil|winwing"
```

The udev rule needs the vendor and product IDs. Display the details of a specific event device:

```bash
# Find the event number (filter for joystick devices):
cat /proc/bus/input/devices | grep -A 4 "Thrustmaster"

# Full attribute hierarchy for the udev rule:
udevadm info --attribute-walk --name=/dev/input/event<N>
```

Relevant fields: `idVendor`, `idProduct`, optionally `serial` (most flight sim controllers do not expose a serial number).

**Step 2: Create rule file**

```bash
sudo nano /etc/udev/rules.d/70-flight-controllers.rules
```

```ini
# Thrustmaster T.16000M FCS — permissions + symlink
KERNEL=="event*", SUBSYSTEM=="input", ATTRS{idVendor}=="044f", ATTRS{idProduct}=="b10a", \
  MODE="0660", GROUP="input", SYMLINK+="input/flight-stick"

# Logitech/Saitek Pro Flight Rudder Pedals
KERNEL=="event*", SUBSYSTEM=="input", ATTRS{idVendor}=="06a3", ATTRS{idProduct}=="0764", \
  MODE="0660", GROUP="input", SYMLINK+="input/flight-rudder"
```

Replace the vendor and product IDs (`044f:b10a` etc.) with the values from step 1.

**Step 3: Activate rules**

```bash
sudo udevadm control --reload-rules
sudo udevadm trigger --subsystem-match=input
```

Alternatively: unplug and re-plug the device. Verify symlinks:

```bash
ls -la /dev/input/flight-*
```

!!! tip "Distinguishing identical devices"
    Two identical controllers (e.g. two TCA quadrants) share the same VID:PID and usually have no serial number. The only stable way to tell them apart is the **physical USB port path**.

    Find the port path:

    ```bash
    udevadm info --query=path --name=/dev/input/event<N>
    ```

    Then add a `KERNELS` match to the rule (e.g. `KERNELS=="3-2.1"` for the port). **Important:** The devices must always be plugged into the same USB port.

    X-Plane identifies controllers internally by VID:PID via SDL2 and does not use symlinks. With identical devices, the assignment may swap between reboots despite udev rules. As a workaround, the order can be forced via the SDL2 environment variable:

    ```bash
    SDL_JOYSTICK_DEVICE=/dev/input/by-path/<path-1>:/dev/input/by-path/<path-2> ./X-Plane-x86_64
    ```

    The stable paths under `/dev/input/by-path/` are tied to the physical USB port and do not change.

### Configuration Files

| File | Path (relative to X-Plane 12) | Contents |
|------|-------------------------------|----------|
| `.joy` | `Resources/joystick configs/` | Device definitions |
| `.prf` | `Output/preferences/` | User-specific assignments |

Backup: Save the entire `Output/preferences/` directory. Reset: Delete `X-Plane Joystick Settings.prf` — it will be recreated on next start.

### Common Problems

- **Device not detected:** SDL2 uses `/dev/input/event*`, not `/dev/input/js*`. If the device works in `jstest-gtk` but not in X-Plane → check udev rules for evdev nodes
- **Device disappears after suspend:** Disable USB autosuspend — see [System Tuning](../systemtuning.md)
- **Phantom axes / multiple detection:** Some devices register as multiple input devices. In the `.joy` file, phantom controls can be marked as "hidden"
- **Axes inverted:** "Reverse" checkbox in X-Plane axis settings

For diagnostics: `--no_joysticks` starts X-Plane without controller initialization (see [Troubleshooting](#diagnostic-launch-with-cli-parameters)).

## Troubleshooting

### Log Files

X-Plane writes a new `Log.txt` in the installation directory on each start.

**Log rotation (in recent versions)**

- Up to 4 copies: `Log.txt` (current), `Log.1.txt`, `Log.2.txt`, `Log.3.txt`
- Older logs are archived in `Output/Log Archive/` with timestamps
- Separate `Log_ATC.txt` with its own rotation cycle

**What to look for?**

- **GPU initialization:** `Vulkan Device :` shows detected GPU and VRAM
- **Plugin issues:** `Loaded:` followed by plugin path confirms successful loading. Missing line → plugin was not loaded
- **Device Loss:** `Encountered Vulkan device loss error!` — GPU crash during runtime

### Diagnostic Launch with CLI Parameters

The command line is the most powerful troubleshooting tool on Linux. Instead of launching X-Plane through the launcher:

```bash
cd ~/X-Plane\ 12/
./X-Plane-x86_64 --<option>
```

**Scenario: X-Plane won't start or crashes**

```bash
# Graphics issue? Graphics-only safe mode:
./X-Plane-x86_64 --safe_mode=GFX

# Plugin issue? Disable only plugins:
./X-Plane-x86_64 --safe_mode=PLG

# Multiple subsystems at once:
./X-Plane-x86_64 --safe_mode=PLG,SCN

# Full safe mode:
./X-Plane-x86_64 --safe_mode
```

The `--safe_mode` options in detail:

| Option | Disables |
|--------|----------|
| `GFX` | Graphics settings reset |
| `PLG` | All plugins |
| `SCN` | Custom Scenery |
| `ART` | Art Controls |
| `UI` | UI settings reset |

**Scenario: Audio or controllers not working**

```bash
# Start without sound (isolates PipeWire/PulseAudio):
./X-Plane-x86_64 --no_sound

# Start without controllers (isolates evdev/udev):
./X-Plane-x86_64 --no_joysticks

# Without networking (isolates IPv6/network issues):
./X-Plane-x86_64 --disable_networking
```

**Scenario: Fullscreen issues under Wayland**

```bash
# Force windowed mode:
./X-Plane-x86_64 --window=1920x1080

# Or fullscreen with explicit resolution:
./X-Plane-x86_64 --full=2560x1440
```

**Scenario: Performance testing / comparison**

```bash
# Reproducible benchmark (cockpit, clear weather, high quality):
./X-Plane-x86_64 --fps_test=003 --verbose --weather_seed=42

# Pass/fail test for scripting (minimum 30 FPS):
./X-Plane-x86_64 --fps_test=003 --require_fps=30
```

The `--fps_test` code has three digits: hundreds = camera position (0=cockpit, 1=top view), tens = weather (0-7), ones = quality (1=Low to 5=Extreme). The test runs for 90 seconds and writes results to `Log.txt`.

**Launch Scripts with Profiles**

With `--pref` and `--dref`, settings can be overridden via command line — useful for different launch profiles:

```bash
# Set DataRef at startup:
./X-Plane-x86_64 --dref:sim/private/controls/rain/kill_it=1

# Override preference:
./X-Plane-x86_64 --pref:_is_full_res=1
```

!!! note "Complete parameter list"
    `./X-Plane-x86_64 --help` shows all available options. Many of the listed `--no_vbos`, `--no_fbos` etc. are OpenGL legacy flags and irrelevant under X-Plane 12 (Vulkan).

### GPU Debugging

**Aftermath (GPU Crash Analysis)**

X-Plane can collect detailed diagnostic data during GPU crashes (Device Loss) — for all GPU vendors (NVIDIA, AMD, Intel):

```bash
./X-Plane-x86_64 --aftermath
```

Aftermath injects checkpoints into the GPU command stream. During a Device Loss, these markers help reconstruct the GPU state at the time of the error. Performance overhead is present, but the diagnostic data is invaluable for recurring GPU crashes. For a deeper understanding of Device Losses and their causes, see [Device Losses](geraeteverluste.md).

**Vulkan Validation Layers**

For deep Vulkan diagnostics:

```bash
sudo apt install vulkan-validationlayers
VK_INSTANCE_LAYERS=VK_LAYER_KHRONOS_validation ./X-Plane-x86_64
```

!!! warning "Debugging only"
    Validation Layers cause massive performance degradation. Only enable when specifically investigating Vulkan errors.

### Crash Analysis with GDB

For recurring crashes, GDB can provide a backtrace:

```bash
cd ~/X-Plane\ 12/
gdb ./X-Plane-x86_64
(gdb) run
# After the crash:
(gdb) backtrace full
(gdb) thread apply all backtrace
```

**Enable core dumps** (if no core dump is generated):

```bash
ulimit -c unlimited
./X-Plane-x86_64
```

Check core dump path: `cat /proc/sys/kernel/core_pattern`

Under systemd, core dumps are stored in `/var/lib/systemd/coredump/` (compressed).

## Sources

The most important sources on the topics covered on this page:

- [Addressing Plugin Flickering](https://developer.x-plane.com/2023/02/addressing-plugin-flickering/) — Laminar Research blog post on Zink integration and OpenGL/Vulkan interop
- [Mesa Environment Variables](https://docs.mesa3d.org/envvars.html) — Official Mesa documentation for shader cache, present mode and driver variables
- [PipeWire Audio Troubleshooting](https://www.x-plane.com/kb/troubleshooting-audio-issues-with-pipewire-on-linux/) — Official X-Plane KB article on FMOD and PipeWire compatibility
- [Using Joysticks on Linux](https://www.x-plane.com/kb/using-joysticks-x-plane-11-linux-systems/) — Official X-Plane guide for udev rules and controller permissions
- [Vulkan Specification](https://registry.khronos.org/vulkan/) — Khronos Group Vulkan API specification and reference
- [NVIDIA Driver README: Environment Variables](https://download.nvidia.com/XFree86/Linux-x86_64/570.86.16/README/openglenvvariables.html) — Official documentation of `__GL_*` variables including Vulkan applicability
- [NVIDIA Driver README: Smooth Motion](https://download.nvidia.com/XFree86/Linux-x86_64/580.95.05/README/nvpresent.html) — Official documentation for AI-based frame interpolation
- [Arch Wiki: Vulkan](https://wiki.archlinux.org/title/Vulkan) — Practical guide to Vulkan setup, ICD selection and troubleshooting on Linux

## Background: Anti-Aliasing and Rendering

??? abstract "Technical Background: Anti-Aliasing in X-Plane"

    #### Aliasing and Sampling

    Aliasing is a phenomenon that occurs due to the discrete sampling of a continuous signal, as described by the **Nyquist-Shannon Theorem**. This theorem states that the sampling frequency must be at least twice as high as the highest signal frequency to avoid aliasing artifacts. In computer graphics, insufficient sampling frequency leads to stair-stepping effects, especially at edges that are not aligned with the pixel grid.

    #### AA Techniques in X-Plane 12

    **FXAA (Fast Approximate Anti-Aliasing)** is a post-processing technique for edge smoothing. It is computationally efficient and requires no additional memory, but can lead to blurry instruments, especially at 1080p. At 4K resolutions, FXAA shows better results. From version 12.1.0, FXAA is available as a separate toggle; from 12.4.0, cockpit displays are excluded from FXAA (better readability).

    **MSAA (Multi-Sample Anti-Aliasing)** is a hardware-implemented technique with a coverage mask per pixel. It is particularly effective at geometric edges but has difficulties with transparent geometries. In X-Plane 12.1, these issues were improved through Alpha-to-Coverage and Alpha-to-One.

    X-Plane uses deferred rendering, where metadata is stored in a G-buffer. This reduces overdraw but increases complexity with MSAA, as lighting steps must be executed per sample.

    #### Driver-Based MSAA

    MSAA can also be forced through the graphics driver. This leads to faster execution but also to less accurate shading, as the complex X-Plane render pipeline is not taken into account.

    #### Recommendation

    For optimal image quality: disable FSR (slider at maximum), then gradually increase MSAA and check performance. FXAA can be optionally enabled, taking into account its impact on image sharpness. If this is insufficient, a monitor with higher resolution provides the most effective improvement.

??? abstract "Technical Background: PBR and Interior Lighting"

    #### Physically Based Rendering

    Lighting in X-Plane is based on **Physically Based Rendering (PBR)**, which leads to realistic but also complex lighting effects. Materials are influenced by their environment — a cockpit in a pink hangar would take on a corresponding tint. Weather conditions like an orange sunset affect cockpit lighting.

    #### Known Limitations

    The current render pipeline of X-Plane has some technical limitations. Each pixel is calculated independently and in parallel, without context about the surrounding geometry. Particularly with narrow geometries like cockpit edges or wing curves, unwanted light from the environment can be captured.

    Screen-Space Reflections (SSR) can lead to visible artifacts — shimmering reflections on wet asphalt or uneven reflections due to lack of ray coherence. A complete solution would require significant computational power.

    #### Development

    From version 12.2.0, tone mapping was switched to AgX and Exposure Fusion was introduced for interior views, which improves the balance between bright and dark areas. SSAO was recalibrated for trees, buildings, and aircraft. According to Laminar Research, optimization of interior lighting continues to be a high priority.
