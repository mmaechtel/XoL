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

### 2025-05-05
- New [filesystem documentation](filesystem.md)
- Discord community channel added
    - Link available in the footer of both German and English versions
    - Join our community for discussions and support

### 2025-05-04
- [Scenery Documentation](scenery.md) revised
    - List formatting corrected (indentation, spaces)
    - English version aligned with German version
    - [Resources/Maps Chapter](scenery.md#resources) revised
        - Self-created WorldMaps and their purpose highlighted
        - Limitations of ICAO code search for X-Plane 12 scenery documented
- [Ortho4XP Guide](addon/ortho4xp.md) extended
    - New chapter [File Size Optimization](addon/ortho4xp.md#file-size-optimization) added

### 2025-05-03
- [Scenery Documentation](scenery.md) expanded
    - New chapter [Scenery Tips](blog/kcle-cleveland.html) added
        - Collection of useful tips and tricks for scenery management
        - Best practices for organizing and optimizing sceneries
    - RSS Feed created
        - Automatic generation from English blog entries
        - Available at `assets/rss/blog.xml`
