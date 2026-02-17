# Setup & Diagnostics

The configuration page covers what is different on Linux: Vulkan as the sole rendering API, Zink as the OpenGL translation layer for plugins, shader caches, Mesa and NVIDIA environment variables, audio under PipeWire, controller detection via evdev and udev rules, and CLI diagnostics from safe mode to GDB backtrace. The performance page adds the analysis perspective — X-Plane's internal Microprofiler identifies whether CPU or GPU limits the frame, MangoHUD provides the frame time graph as a Vulkan overlay, and targeted diagnostic workflows connect symptoms with the appropriate Linux tools.

- **[Configuration](config.md)** — Graphics settings, rendering options, and Linux-specific adjustments
- **[Performance](performance.md)** — FPS analysis, bottleneck diagnosis, and optimization strategies
