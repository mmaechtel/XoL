# **XoL**: Running **X**-Plane **o**n **L**inux

This documentation is aimed at experienced Linux users who want to run X-Plane on Linux. A working Linux installation is assumed.

The examples shown here are based on Debian Linux but can be easily adapted to other distributions. The basic concepts and approaches remain the same - only the specific package manager commands or repository configurations need to be adjusted accordingly.

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

### 2026-02-09
- [X-Plane Configuration](xplane/config.md) revised: Focus on Linux specifics — Vulkan/Zink, shader cache, environment variables, display server, audio, controllers, scenario-based troubleshooting with CLI parameters. All claims verified against primary sources, version-specific information removed for long-term validity
- [Glossary](glossary.md) expanded: Zink, FMOD, evdev, RADV
- New [System Tuning](systemtuning.md) page — latency optimization for X-Plane: distributions, latency sources, two kernel profiles (standard kernel vs. Liquorix) with concrete configuration steps
- [Liquorix](liquorix.md) updated: new "Why Liquorix?" section explaining the EEVDF scheduler and optimization model
- [Linux Overview](linux.md), [Performance](xplane/performance.md), and navigation extended with system tuning references
- New [XEarthLayer](addon/xearthlayer.md) documentation — Rust-based streaming alternative with adaptive prefetch
- [Orthophotography Introduction](addon/orthophotography_intro.md) restructured: Static Generation vs. Ortho Streaming, player profiles
- [AutoOrtho](addon/autoortho.md) updated: Fork 2.0 (C-Pipeline, .aob2), comparison with Ortho4XP revised
- [Static + Streaming](addon/static_plus_streaming.md) renamed and fully revised
