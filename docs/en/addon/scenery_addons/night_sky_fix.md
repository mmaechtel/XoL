---
description: "Night Sky Fix for X-Plane 12 — star catalogs with up to 900,000 stars for a visible Milky Way, plus a FlyWithLua script for realistic star brightness."
---
# Night Sky Fix

Night Sky Fix replaces the star catalog of [X-Plane](../../glossary.md#x-plane) 12 with a much denser one and adds an optional FlyWithLua script that corrects how the stars are drawn. The default `earth_astro.dat` contains about 8,500 stars down to magnitude 6.5 — the limit of the naked eye. Fainter stars are not resolved individually, but their combined light is visible as haze; without them the sky shows empty patches. The mod's catalogs go down to magnitude 11, and with the largest option the Milky Way becomes visible.

## Background

- **Developer:** lucas1999
- **Download:** [forums.x-plane.org](https://forums.x-plane.org/files/file/100904-night-sky-fix/)
- **Platforms:** No platform restriction — the package contains a data file and a Lua script, no binary
- **Compatibility:** X-Plane 12
- **Optional:** [FlyWithLua NG+](../scripting/flywithlua.md) for the script
- **License:** Freeware, redistribution not permitted

## Features

- **Star catalog options:** Six `earth_astro.dat` variants, from 9,000 stars (magnitude 6.5) to 900,000 (magnitude 11):

| Stars | Limiting magnitude |
|---|---|
| 9,000 | 6.5 |
| 16,000 | 7.0 |
| 45,000 | 8.0 |
| 120,000 | 9.0 |
| 300,000 | 10.0 |
| 900,000 | 11.0 |

- **Dark band and horizon:** The script removes the dark band that hides stars (notably Polaris) and corrects atmospheric extinction — star brightness now decreases toward the horizon, where stars previously stayed visible even in twilight
- **Constellations:** The script adjusts the photometric gain so bright stars stand out and constellations become recognizable
- **Altitude-dependent gain:** With the script, only the main constellations are visible on the ground; the higher the aircraft climbs, the more faint stars appear
- **Moon:** The script raises moon surface brightness to a more realistic 2,500 nits

## Value in Flight Simulation

At night, default X-Plane draws a sky in which all stars look roughly alike and parts of the sky stay empty. The denser catalogs fill the empty patches; the 900,000-star file is the one that makes the Milky Way visible. The optional script makes constellations recognizable, keeps the ramp view toned down, and lets fainter stars appear as the aircraft climbs. The effort is limited to replacing one data file and optionally adding a short script.

## Installation

**Download:** [forums.x-plane.org](https://forums.x-plane.org/files/file/100904-night-sky-fix/)

1. Back up the original star catalog, then copy the chosen variant over it — the folder name `default data` contains a space and must be quoted (adjust the path to the X-Plane installation):

    ```bash
    cd "/path/to/X-Plane 12/Resources/default data" &&
    cp earth_astro.dat earth_astro.dat.orig &&
    cp /path/to/chosen/earth_astro.dat .
    ```

2. Optional but recommended: copy the Lua script into `Resources/plugins/FlyWithLua/Scripts/`.

Without a backup, the X-Plane installer restores the default file: running an update offers to overwrite the modified file.

!!! warning "Script side effect"

    The script sets the private dataref `sim/private/controls/dome/per_view` to `1`. This removes the dark band, but the ground lighting can take a while to update when time is moved forward or back. Commenting out that line in the script (`--`) avoids the delay and brings the band back. The second value it changes, `sim/private/controls/stars/gain_photometric` (default 20), varies between 1 and 30 with altitude and can be adjusted in the script to taste and to the monitor setting.

## Sources

- [Night Sky Fix — forums.x-plane.org](https://forums.x-plane.org/files/file/100904-night-sky-fix/)
