# **XoL**: Running **X**-Plane **o**n **L**inux

This documentation is aimed at experienced Linux users who want to run X-Plane on Linux. A working Linux installation is assumed.

The examples shown here are based on Debian Linux but can be easily adapted to other distributions. The basic concepts and approaches remain the same - only the specific package manager commands or repository configurations need to be adjusted accordingly.

## Featured Video

<div class="video-container" markdown>
<video controls width="100%" preload="metadata" poster="../assets/video/en/Mastering_scenery_packs.jpg">
  <source src="../assets/video/en/Mastering_scenery_packs.mp4" type="video/mp4">
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

### 2026-02-14
- [System Tuning](systemtuning.md) fact-checked: Corrected scheduler references, removed non-functional kernel parameter, clarified NVMe notes, added sources section
- [Getting Started](begin.md) revised: Merged troubleshooting sections, clarified 32-bit note, added display server link
- Language revision (DE): [Getting Started](begin.md) and [Docker](docker.md) converted to impersonal style

### 2026-02-13
- [Getting Started](begin.md) corrected: Updated installer instructions, refined system recommendations, fixed outdated package names and single-core claims, added cross-references
- [Getting Started](begin.md) glossary links added: GRUB, NVMe, VRAM, Orthophotos, FPS, Wayland
- Video content separated by language: German videos on DE pages only, first English video [Mastering scenery packs](videos.md) embedded
- New [Videos](videos.md) page — video collection with embedded overview videos
- [XEarthLayer](addon/xearthlayer.md) expanded: CPU tuning section for parallel operation with X-Plane
- [Introduction to Orthophotography](addon/orthophotography_intro.md) expanded: ortho streamer placement in scenery_packs.ini
- [Scenery Components](scenery_components.md) expanded: videos and links to Ortho Streaming and Ortho4XP
- [Wayland Session](displayserver_wayland.md) streamlined, [Display Server](displayserver.md) and [Introduction](intro.md): videos embedded
- [About](about.md) revised: license, privacy policy, legal notices, target audience
- [Glossary](glossary.md) expanded: 40 new terms covering kernel, graphics, filesystem, audio, and scenery

### 2026-02-11
- [Display Server](displayserver.md) pages fact-checked: Debian defaults corrected, XWayland row added to Hugl table, latency measurements clarified, NVIDIA modeset default updated, MESA variable scoped to Mesa drivers

### 2026-02-09
- New [Display Server](displayserver.md), [X11 Session](displayserver_x11.md) and [Wayland Session](displayserver_wayland.md) pages: protocol comparison, latency measurements, GPU recommendations
- New [System Tools](systemtools.md) page — monitoring tools for verifying tuning settings
- New [System Tuning](systemtuning.md) page — latency optimization: kernel profiles, governor, C-states, interrupt shielding
- [X-Plane Configuration](xplane/config.md) revised: focus on Linux specifics (Vulkan/Zink, shader cache, audio, controllers)
- New [XEarthLayer](addon/xearthlayer.md) documentation, [Orthophotography](addon/orthophotography_intro.md) restructured, [AutoOrtho](addon/autoortho.md) updated
- [Liquorix](liquorix.md) updated, [Glossary](glossary.md) expanded
