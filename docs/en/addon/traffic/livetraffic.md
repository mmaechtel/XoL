---
description: "LiveTraffic renders real-world ADS-B air traffic in X-Plane with TCAS integration, 3D sound, and multiple free and paid data sources."
---
# LiveTraffic

LiveTraffic displays real-world air traffic in [X-Plane](../../glossary.md#x-plane) 11 and 12 by rendering ADS-B data from public and commercial sources in real time.

## Background

- **Developer:** TwinFan
- **Repository:** [github.com/TwinFan/LiveTraffic](https://github.com/TwinFan/LiveTraffic) (open source, MIT license)
- **Platforms:** Windows, macOS, Linux (native binaries)
- **Compatibility:** X-Plane 11 and X-Plane 12

LiveTraffic is actively maintained and uses the [XPMP2](https://github.com/TwinFan/XPMP2) library for GPU instancing and [Vulkan](../../glossary.md#vulkan-api) compatibility.

## Features

- **Real-time air traffic:** Real aircraft instead of AI traffic, based on ADS-B data
- **TCAS integration:** Traffic appears on TCAS displays in the cockpit
- **3D sound:** Engines, landing gear, flaps, and taxiing via [FMOD](../../glossary.md#fmod) Core API
- **Landing/takeoff prediction:** Calculates rotate, liftoff, and touchdown points
- **Contrails:** Configurable altitude range for condensation trails
- **Map layer:** Integration into the X-Plane internal map
- **Aircraft labels:** Configurable flight information above aircraft
- **CSL model matching:** Uses Bluebell OBJ8 and X-CSL packages for realistic aircraft models

### Data Sources

Several channels work immediately without registration:

| Channel | Cost | Notes |
|---------|------|-------|
| Airplanes.live | Free | Anonymous, enabled by default |
| adsb.fi | Free | Works out of the box, anonymous, enabled by default |
| OpenSky Network | Free | Anonymous or registered, request limits apply |
| Open Glider Network | Free | Anonymous, unlimited |
| SayIntentions | Free | Anonymous, virtual traffic |
| AutoATC | Free | Anonymous, virtual traffic |

Additional channels (registration or subscription required):

| Channel | Cost | Notes |
|---------|------|-------|
| RealTraffic | Paid | Most comprehensive source with parked aircraft and weather data |
| ADSBHub | Free for active data feeders | Requires an active ADSBHub feed |
| ADS-B Exchange | Paid | API key required |
| Navigraph/FR24 | Paid | Requires Navigraph Unlimited subscription; 20 second / 80 nm update limits |
| FSCharter | Free (account required) | Virtual traffic network, requires a registered FSCharter account |

## Value in Flight Simulation

LiveTraffic replaces generic AI traffic with real flight movements — the current traffic volume at the airport, real callsigns, and actual routes. TCAS integration enables realistic separation and traffic awareness. With RealTraffic as the data source, parked aircraft and weather data are also injected.

## Installation

**Download:** [forums.x-plane.org](https://forums.x-plane.org/files/file/49749-livetraffic/)

Extract the ZIP file to `Resources/plugins/`. CSL models (Bluebell recommended) are placed in the subdirectory `Resources/plugins/LiveTraffic/Resources/CSL/`.

**Dependencies on Debian/Ubuntu:**

```bash
sudo apt install libcurl4 xdg-utils
```

### CURL_OPENSSL_4 Issue with Steam

!!! warning "Plugin fails to load with Steam installation"

    With X-Plane installations through Steam, the following error may occur:

    ```
    libcurl.so.4: version 'CURL_OPENSSL_4' not found (required by .../LiveTraffic.xpl)
    ```

    The Steam Runtime ships an older `libcurl.so.4` that lacks the `CURL_OPENSSL_4` symbol. LiveTraffic is built against the system version of libcurl which provides this symbol.

    **Workaround:** Rename the Steam Runtime's `libcurl.so.4` to `libcurl.so.4.bak` and create a symlink to the system version. The Steam Runtime directory is usually `/opt/steamapps/common/SteamRuntime` or similar. This workaround must be reapplied after Steam updates. Refer to the [LiveTraffic documentation](https://twinfan.gitbook.io/livetraffic) for detailed instructions. The issue does not affect non-Steam X-Plane installations.

### RealTraffic Ports (Firewall)

When using RealTraffic, the following ports must be open for inbound traffic:

| Port | Protocol | Purpose |
|------|----------|---------|
| 10747 | TCP | Direct connection |
| 49004 | UDP | Weather data |
| 49005 | UDP | Primary traffic data (RTTFC) |

## Sources

- [LiveTraffic — GitHub](https://github.com/TwinFan/LiveTraffic)
- [LiveTraffic — Documentation](https://twinfan.gitbook.io/livetraffic)
- [XPMP2 — GitHub](https://github.com/TwinFan/XPMP2)
- [LiveTraffic — forums.x-plane.org](https://forums.x-plane.org/files/file/49749-livetraffic/)
