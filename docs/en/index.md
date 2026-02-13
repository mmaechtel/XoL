# **XoL**: Running **X**-Plane **o**n **L**inux

This documentation is aimed at experienced Linux users who want to run X-Plane on Linux. A working Linux installation is assumed.

The examples shown here are based on Debian Linux but can be easily adapted to other distributions. The basic concepts and approaches remain the same - only the specific package manager commands or repository configurations need to be adjusted accordingly.

## Featured Video

<div class="video-container" markdown>
<video controls width="100%" preload="metadata" poster="../assets/video/X11_vs_Wayland/X11_vs_Wayland.jpg">
  <source src="../assets/video/X11_vs_Wayland/X11_vs_Wayland.mp4" type="video/mp4">
</video>
</div>

[All Videos →](videos.md)

## Documentation Content

The documentation covers the most important areas of X-Plane configuration under Linux. The focus is on optimal settings for X-Plane, performance optimization through kernel, drivers, and system settings, as well as the installation and configuration of important extensions like AutoOrtho. Additionally, common problems and their solutions are thoroughly addressed. A special emphasis is placed on performance analysis using integrated and external tools, filesystem optimization for fast loading times, and hardware-specific adjustments for maximum performance.

## Guide Structure

The technical guides are modular in design and enable flexible implementation. You can implement individual components as needed or adapt the entire system according to your requirements. Each guide describes the goal and benefit of the change, shows the necessary steps, explains important configuration options, and provides troubleshooting tips. The guides are organized into logical sections: Basic system optimization, performance monitoring and analysis, hardware-specific adjustments, and advanced configurations for special use cases.

## Contributing

This documentation is an open project. Improvements or additions can be contributed via GitHub:

- Create issues for bugs or suggestions
- Submit pull requests for changes
- Share experiences in the discussions in the footer of this website (e.g., via the Discord link)

## Recent Changes

### 2026-02-13
- New [Videos](videos.md) page — video collection with embedded overview videos
- [XEarthLayer](addon/xearthlayer.md) expanded: CPU tuning section with thread configuration, scenario table, and disk I/O profiles for parallel operation with X-Plane
- [Display Server](displayserver.md) and home page: videos moved to beginning of chapters
- [Wayland Session](displayserver_wayland.md) streamlined: redundant latency table and desktop entry replaced with references to main pages
- [Introduction](intro.md) expanded: overview video embedded
- [Introduction to Orthophotography](addon/orthophotography_intro.md) expanded: New section on ortho streamer placement in scenery_packs.ini with example configurations for AutoOrtho, XEarthLayer, and XPME

### 2026-02-11
- [Display Server](displayserver.md) pages fact-checked: Debian defaults corrected, XWayland row added to Hugl table, latency measurements clarified, NVIDIA modeset default updated, MESA variable scoped to Mesa drivers

### 2026-02-09
- New [Display Server](displayserver.md) pages — overview, [X11 Session](displayserver_x11.md) and [Wayland Session](displayserver_wayland.md): protocol comparison (X11/Wayland/XWayland), hardware latency measurements, GPU recommendations, session switching, troubleshooting
- [Glossary](glossary.md) expanded: Compositor, Display Server, Wayland, X11, XWayland
- [X-Plane Configuration](xplane/config.md) display server section shortened with references to new pages
- New [System Tools](systemtools.md) page — monitoring tools (htop, turbostat, mpstat, iotop, ioping, glances etc.) for verifying tuning settings. All claims fact-checked against primary sources
- New [System Tuning](systemtuning.md) page — latency optimization for X-Plane: two kernel profiles (standard kernel vs. Liquorix), governor, C-states, interrupt shielding, NVMe power saving, kernel switching via GRUB
- [X-Plane Configuration](xplane/config.md) revised: focus on Linux specifics — Vulkan/Zink, shader cache, environment variables, display server, audio, controllers, CLI troubleshooting. Sources section with primary references added
- [Liquorix](liquorix.md) updated: EEVDF scheduler and optimization model explained
- [System Errors](xplane/systemfehler.md) reduced to navigation page, [Glossary](glossary.md) expanded with Zink, FMOD, evdev, RADV
- New [XEarthLayer](addon/xearthlayer.md) documentation — Rust-based streaming alternative with adaptive prefetch
- [Orthophotography](addon/orthophotography_intro.md) restructured, [AutoOrtho](addon/autoortho.md) updated (Fork 2.0), [Static + Streaming](addon/static_plus_streaming.md) fully revised
