# Introduction

??? abstract "What makes X-Plane different"

    [X-Plane](glossary.md#x-plane) stands out from other flight simulators through its simulation-oriented approach. The flight physics are based on [Blade Element Theory](glossary.md#blade-element-theory) — instead of pre-made lookup tables, airflow and forces are calculated in real-time for each aircraft segment. This extends to engine and systems simulation as well as weather with atmospheric effects.

    The rendering engine uses [PBR](glossary.md#pbr) for physically correct material representation, combined with dynamic lighting, atmospheric effects, real-time reflections, and [HDR](glossary.md#hdr) rendering. The focus is on realistic rather than artistic interpretation.

    X-Plane's open [plugin](glossary.md#plugin) architecture allows deep customization — from custom aircraft models to FlyWithLua scripts and third-party tools. The simulation engine is actively developed, with X-Plane 12 distributing substantial rendering work across multiple CPU cores while the physics main thread remains single-core bound.

## Why X-Plane under Linux?

The short answer: because the entire stack is open. The Linux kernel, the GPU drivers ([Mesa](glossary.md#mesa)/[RADV](glossary.md#radv) for AMD, [ANV](glossary.md#anv) for Intel), the display server, the filesystem — all open source. This is not an ideological point, it is a practical one: open source is the reason you can tune a Linux system for X-Plane in ways that are simply not possible on a closed platform.

Every optimization described in this documentation — from CPU scheduling to interrupt routing to shader cache configuration — exists because the source code is available, the interfaces are documented, and the community continuously improves the stack. [Zink](glossary.md#zink), the OpenGL-to-Vulkan translation layer that is critical for X-Plane plugin compatibility, is an open-source Mesa project. The Vulkan drivers that power X-Plane's rendering are developed in the open. Performance improvements flow directly from community contributions.

This transparency has concrete consequences for flight simulation:

- **Kernel tuning:** Precise control over CPU governor, interrupt affinity, and scheduling — covered in [System Tuning](systemtuning.md) and [Liquorix Kernel](liquorix.md)
- **No background interference:** No automatic updates or telemetry competing for CPU cycles during flight. System performance is predictable.
- **Display server choice:** [Wayland or X11](displayserver.md) can be selected based on GPU and compositor behavior
- **Driver control:** GPU driver version, persistence mode, and power management are fully configurable — see [Nvidia Drivers](nvidia.md)
- **Filesystem optimization:** Mount options, I/O scheduler, and TRIM can be tuned for fast scenery loading — see [Filesystem](filesystem.md)
- **Debuggability:** When micro-stutters occur, the cause can be traced down to the kernel level — scheduler decisions, interrupt timing, driver behavior. Nothing is a black box.
- **Stability:** Debian Stable provides a predictable base with no surprise OS upgrades, no forced reboots, no breaking changes mid-session.

The trade-off: initial setup and tuning require more effort than on Windows. But this is not a platform where following a checklist is enough — the same kernel parameter can improve or degrade performance depending on which kernel you run. This documentation provides the background to make informed decisions: how scheduling and latency work, why two kernels need opposite tuning strategies, and where each optimization makes a measurable difference. [Getting Started](begin.md) covers system requirements and installation.

Sources:

- [X-Plane Official Website](https://www.x-plane.com/)
