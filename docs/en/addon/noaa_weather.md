# NOAA Weather

NOAA Weather is a Python-based [plugin](../glossary.md#plugin) that adds real-world snow coverage and METAR monitoring to X-Plane 12. It downloads weather data from NOAA (National Oceanic and Atmospheric Administration) and cross-references it with X-Plane's built-in Real Weather engine.

## Background

- **Developer:** Antonio Golfari (biuti), originally by Joan Perez i Cauhe
- **Repository:** [github.com/biuti/XplaneNoaaWeather](https://github.com/biuti/XplaneNoaaWeather) (open source, GPLv2)
- **Platforms:** Windows, macOS, Linux
- **Compatibility:** X-Plane 12.1.2+
- **Prerequisite:** [XPPython3](xppython3.md) 4.6.0+
- **Price:** Free

Since X-Plane 12 already uses NOAA GFS data for its own weather engine, this plugin does not act as a full weather replacement but as a supplement — primarily for snow depiction and weather monitoring. The plugin is actively maintained with regular releases.

## Features

- **Snow coverage:** Downloads NOAA GFS snow depth and precipitation data to generate location-specific snow that X-Plane 12 cannot depict correctly on its own
- **Predictive algorithm:** Calculates snow coverage up to 70 nm ahead along the flight path when GFS data is unavailable for individual grid cells
- **METAR comparison:** Displays X-Plane 12 Real Weather METAR alongside external sources (NOAA, IVAO, VATSIM) in a dedicated window
- **Runway friction:** Simulates tarmac treatment in cold weather for more realistic braking behavior (X-Plane 12.4+)
- **Real Weather monitoring:** Monitors and visualizes in real time what X-Plane's internal weather engine is actually producing

## Value in Flight Simulation

While X-Plane 12 already sources its weather data from NOAA, it cannot depict snow coverage with location-specific accuracy. NOAA Weather fills this gap using actual GFS snow depth data and additionally provides a METAR comparison tool that is particularly useful for online flying on IVAO or VATSIM. Since commercial weather alternatives like Active Sky and xEnviro do not support Linux, NOAA Weather is one of the few options available to Linux users.

## Installation

**Download:** [GitHub Releases](https://github.com/biuti/XplaneNoaaWeather/releases)

[XPPython3](xppython3.md) must already be installed. Before installing, completely remove any previous version (do not overwrite). Extract the ZIP file to `Resources/plugins/PythonPlugins/`:

```
Resources/plugins/PythonPlugins/
├── PI_noaaWeather.py
└── noaaweather/
```

### Linux Notes

The plugin ships a pre-compiled `linux-wgrib2` binary (built on Ubuntu 20.04 LTS) for decoding GFS GRIB2 files. It is compatible with most current distributions. If the bundled binary does not work on your system, wgrib2 can be compiled from source.

No other Linux-specific issues are known.

## Sources

- [NOAA Weather — GitHub](https://github.com/biuti/XplaneNoaaWeather)
- [NOAA Weather — X-Plane.org Forum](https://forums.x-plane.org/forums/topic/72313-noaa-weather-plugin/)
- [XPPython3 — Documentation](https://xppython3.readthedocs.io/en/latest/index.html)
