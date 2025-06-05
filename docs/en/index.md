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

### 2025-06-05
- [Additional information about aliasing and graphics settings](https://emvisio.com/en/xplane/config.html#graphics-settings)

### 2025-05-15
- [Ortho4XP](addon/ortho4xp.md) SonnyLiDAR chapter expanded
- [Clearance](flight_operations/clearance.md#**ToLiss Airbus – Request Departure Clearance via CPDLC**) CPDLC ToLiss information added
- [Weather radar functionality in real aircraft](flight_operations/weather.md#Weather Radar) summarized

### 2025-05-09
- ['Device Lost Crash'](xplane/geraeteverluste.md) explained
- New ['Flight Operations'](flight_operations/overview.md) menu with [weather tools](flight_operations/weather.md)

### 2025-05-08
- [Ortho4XP](addon/ortho4xp.md) + [AutoOrtho](addon/autoortho.md) significantly expanded
- Highlighted combinations of [Ortho4XP](addon/ortho4xp.md) and [AutoOrtho](addon/autoortho.md), and added practical examples in the [combination guide](addon/autoortho_plus_zortho.md)

??? note "Older Changes"

    **2025-05-05:**

    - New [filesystem documentation](filesystem.md)
    - Discord community channel added
        - Link available in the footer of both German and English versions
        - Join our community for discussions and support

    **2025-05-04:**

    - Scenery Documentation revised
        - List formatting corrected
        - English version aligned
        - Resources/Maps Chapter revised
    - Ortho4XP Guide extended
        - New chapter on file size optimization

    **2025-05-03:**

    - Scenery Documentation expanded
        - New chapter with scenery tips
        - Best practices for organization
    - RSS Feed created
        - Automatic generation
        - Available at assets/rss/blog.xml
