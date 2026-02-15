# Follow the Greens

Follow the Greens (FtG) is a taxiway guidance system based on the real-world A-SMGCS (Advanced Surface Movement Guidance and Control System). The [plugin](../glossary.md#plugin) activates green taxiway centerline lights ahead of the aircraft and signals hold positions with red lights — just like the system already in use at airports such as London Heathrow, Dubai, Munich, and Seoul.

## Background

- **Developer:** Pierre Mareschal (devleaks)
- **Repository:** [github.com/devleaks/followthegreens](https://github.com/devleaks/followthegreens) (open source, MIT license)
- **Platforms:** Windows, macOS, Linux (cross-platform via Python)
- **Compatibility:** [X-Plane](../glossary.md#x-plane) 12 (Release 2), X-Plane 11 + 12 (Release 1, critical fixes only)

The plugin is actively developed. Release 2 ("Follow the Greens 4D") adds speed management — an A-SMGCS Level 4 feature.

## Features

- **Green taxiway lights:** Illuminate progressively ahead of the aircraft showing the taxi route
- **Red stop bars:** Signal holds at intersections and holding points
- **4D speed management:** The "rabbit" light (pulsating light sequence) automatically adjusts speed and run length — fast and far means accelerate, slow and short means slow down
- **Routing algorithm:** Considers taxiway widths, one-way restrictions, and network constraints
- **Taxiway display:** ShowTaxiways mode to highlight the entire taxiway network
- **Runway lighting:** Runway light intensity adjustable
- **Command bindings:** Actions (OK, Cancel, Clearance, Speed, Bookmark, NewGreens) can be bound to keys or buttons
- **[SkunkCrafts Updater](skunkcrafts_updater.md):** Automatic updates are supported

## Value in Flight Simulation

The yellow ground arrows in X-Plane show the general taxi direction but offer no dynamic guidance. Follow the Greens adds progressive lighting and speed recommendations — particularly helpful at unfamiliar airports with complex taxiway layouts.

## Installation

**Prerequisite:** [XPPython3](xppython3.md) (version 4.5 or above). XPPython3 includes its own Python interpreter — a separate Python installation is not required.

**Download:** [GitHub Releases](https://github.com/devleaks/followthegreens/releases)

Copy the files `PI_FollowTheGreens.py`, `PI_SetRunwayLightIntensity.py`, and the `followthegreens/` folder to `Resources/plugins/PythonPlugins/`. After reloading Python scripts, a "Follow the greens..." entry appears in the Plugin menu.

Since FtG is a pure Python plugin, no native binaries are needed. There are no known Linux-specific issues.

!!! info "Requirement: Taxiway network"

    FtG requires a defined taxiway network at the airport. Default airports in X-Plane meet this requirement. The plugin will not work with custom sceneries that lack a taxiway network.

## Sources

- [Follow the Greens — GitHub](https://github.com/devleaks/followthegreens)
- [Follow the Greens — Documentation](https://devleaks.github.io/followthegreens/)
- [Follow the Greens — forums.x-plane.org](https://forums.x-plane.org/files/file/71124-follow-the-greens/)
