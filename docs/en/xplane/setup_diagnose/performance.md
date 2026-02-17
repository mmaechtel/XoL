---
description: "X-Plane 12 performance analysis on Linux: Microprofiler for CPU/GPU bottlenecks, MangoHUD frame time overlay, GPU monitoring, and optimization tips."
---
# X-Plane Performance on Linux

X-Plane 12 is a cross-platform application — the general graphics settings (textures, shadows, clouds, anti-aliasing) work the same on all operating systems and are documented in the [official documentation](https://www.x-plane.com/kb/configuring-the-rendering-options/). This page covers performance **analysis** on Linux: internal diagnostic tools, Linux-specific monitoring utilities, and targeted optimization recommendations. The Linux-specific graphics settings are documented under [Configuration](config.md), system tuning under [System Tuning](../../linux/system/systemtuning.md).

## Internal Diagnostic Tools

### FPS Display

The FPS display (Frames per Second) is the simplest tool for assessing performance. It shows how many frames are calculated per second — but the average value alone reveals little. What matters is the frame time: the time in milliseconds that a single frame requires. A stable 30 FPS (≈ 33 ms per frame) delivers a smoother experience than a fluctuating average of 40 FPS with regular spikes to 60 ms.

**Reference Values**

| FPS | Frame Time | Rating |
|-----|------------|--------|
| 50+ | < 20 ms | Very smooth |
| 30–49 | 20–33 ms | Smooth |
| 20–29 | 33–50 ms | Acceptable |
| < 20 | > 50 ms | Noticeable stuttering |

**Activation:** In the menu under *Settings → Data Output*, enable the *frame rate* option. The display appears in the upper left corner of the screen. Alternatively, the FPS display can be toggled with the keyboard shortcut `Shift+Ctrl+F` — provided the binding has not been changed.

### Microprofiler

While the FPS display only shows the overall result, the Microprofiler breaks down frame generation into individual tasks. This reveals whether physics calculations, scenery rendering, plugins, or the GPU are causing the bottleneck.

**Activation:** In the menu, select *Developer → Toggle Microprofiler*. A real-time graphical display appears showing the time distribution per frame.

**Task Categories**

| Category | What is measured | Typical values (30 FPS) |
|----------|-----------------|-------------------------|
| Flight Model | Physics and aerodynamics | 5–15 ms |
| Scenery | Landscapes, buildings, roads | 5–10 ms |
| Clouds/Weather | Clouds, rain, fog | 3–8 ms |
| Plugins | Installed plugins and addons | 2–10 ms |
| Swapchain Acquire | CPU/GPU synchronization | 1–5 ms |

**Identifying CPU-bound vs. GPU-bound**

The total time splits into CPU time (physics, plugins, scenery logic) and GPU time (textures, shadows, clouds). If CPU time is significantly higher than GPU time, the processor is the bottleneck — lowering graphics settings will have little effect. Conversely, GPU bottlenecks respond well to reducing texture quality, shadows, or anti-aliasing. The table in the [Optimization Tips](#optimization-tips) section maps each bottleneck to specific measures.

**Calculation Example**

| Component | Time |
|-----------|------|
| **Total frame time** | **33.3 ms (30 FPS)** |
| Physics calculation | 10 ms |
| Scenery rendering | 8 ms |
| Clouds/weather | 7 ms |
| Plugins | 5 ms |
| Swapchain Acquire | 3 ms |
| **Total CPU time** | **20 ms** |
| **Total GPU time** | **13 ms** |

In this example, the CPU at 20 ms is the limiting factor. Physics calculations and plugin load are the largest individual items — this is where optimizations should focus.

## External Tools

X-Plane shows **what** is slow — Linux tools show **why**. The internal diagnostic tools (Microprofiler, FPS display) identify bottlenecks within the simulation. External tools provide the system perspective: GPU utilization, CPU frequency, I/O wait times, and thermal throttling.

### MangoHUD — In-Game Performance Overlay

MangoHUD is a Vulkan layer overlay that displays performance metrics directly in-game.

**Installation and Launch**

```bash
sudo apt install mangohud
mangohud ./X-Plane-x86_64
```

**Displayed Metrics**

- FPS and frame time graph
- GPU load, temperature, clock speed, and [VRAM](../../glossary.md#vram-video-ram) usage
- CPU load, temperature, and frequency per core
- RAM usage

**Frame time graph** — the most important tool: spikes reveal stutters that the average FPS hides. A stable graph at 33 ms (30 FPS) is better than a fluctuating one averaging 25 ms.

**Configuration**

MangoHUD can be customized via a configuration file. A compact layout works well for X-Plane:

`~/.config/MangoHud/X-Plane-x86_64.conf`

```ini
fps
frame_timing
gpu_stats
gpu_temp
gpu_core_clock
gpu_mem_clock
vram
cpu_stats
cpu_temp
cpu_mhz
ram
position=top-left
font_size=20
```

**Keyboard Shortcuts**

| Shortcut | Function |
|----------|----------|
| `Shift_R+F12` | Toggle overlay |
| `Shift_L+F2` | Start/stop CSV logging |

CSV logging records metrics for post-flight analysis — log files are saved under `/tmp/MangoHud/`.

### GPU Monitoring

| GPU | Tool | Installation | Command |
|-----|------|-------------|---------|
| NVIDIA | nvidia-smi | (included with driver) | `nvidia-smi dmon` |
| AMD | radeontop | `sudo apt install radeontop` | `sudo radeontop` |
| Intel | intel_gpu_top | `sudo apt install intel-gpu-tools` | `sudo intel_gpu_top` |

For NVIDIA cards, a compact CSV monitor can be started:

```bash
nvidia-smi --query-gpu=utilization.gpu,utilization.memory,temperature.gpu,clocks.gr,power.draw --format=csv -l 2
```

**Identifying GPU Bottlenecks**

- GPU 95–100% + low FPS → GPU-bound (reduce graphics settings)
- GPU < 70% + low FPS → CPU-bound (check Microprofiler for blocking thread)

## Diagnostic Workflows

The following table connects typical symptoms with the appropriate toolchain. Details on the Linux tools can be found under [System Monitoring](../../linux/system/systemtools.md).

| Symptom | Toolchain | What to check |
|---------|-----------|---------------|
| Micro-stutters during flight | MangoHUD frame time + `iostat` | NVMe wake-up latency (APST) |
| Low FPS with low GPU load | Microprofiler + `htop` | CPU-bound — which thread is blocking? |
| Stutter during scenery transitions | `iotop` + `fatrace` | Which files are being read? |
| FPS drop after driver update | MangoHUD comparison before/after | Clear shader cache, driver regression? |
| Periodic stutters every ~30 s | `mpstat -I CPU 1` | IRQ storm on application cores? |

## Optimization Tips

The Microprofiler shows where frame time is being lost. The following table maps each bottleneck to the most effective measure.

| Bottleneck | Measure | Setting |
|------------|---------|---------|
| CPU (Physics) | Reduce flight models | Flight Models per Frame: 2–4 |
| CPU (Plugins) | Disable resource-heavy addons | — |
| CPU (Scenery) | Reduce objects and AI aircraft | Lower Object Density |
| GPU (Textures) | Lower texture quality | Texture Quality: Medium or High |
| GPU (Shadows) | Reduce shadows and anti-aliasing | Lower Shadow Quality and MSAA level |
| GPU (Clouds) | Adjust cloud quality | Lower Cloud Quality |

For Linux-specific optimizations (CPU governor, interrupt routing, memory parameters) see [System Tuning](../../linux/system/systemtuning.md). Benchmarking methods and rendering options are documented under [Configuration](config.md).

---

## Further Reading

| Topic | Page | Focus |
|---|---|---|
| Load Dimensions | [Load Dimensions](../../fundamentals/performance/performance_overview.md) | Conceptual framework: CPU, GPU, VRAM, I/O bottleneck categories |
| Latency and Predictability | [Latency Theory](../../fundamentals/performance/latency.md) | Frame time analysis, jitter, scheduling theory |
| CPU & RAM | [CPU & RAM](../../fundamentals/performance/cpu_ram.md) | CPU architecture, thread scheduling, memory bandwidth |
| GPU & VRAM | [GPU & VRAM](../../fundamentals/performance/gpu_vram.md) | GPU pipeline, VRAM budget, texture compression |
| Nvidia Drivers | [Nvidia Drivers](../../linux/optimizations/nvidia.md) | Driver installation, nvidia-smi, GPU configuration |
| Device Losses | [Device Losses](../systemfehler/geraeteverluste.md) | GPU crashes: causes, Aftermath debugging, resolution |

---

## Sources

- [MangoHUD — GitHub](https://github.com/flightlessmango/MangoHud)
- [X-Plane 12 — Rendering Options](https://www.x-plane.com/kb/configuring-the-rendering-options/)
- [nvidia-smi Documentation](https://developer.nvidia.com/nvidia-system-management-interface)
