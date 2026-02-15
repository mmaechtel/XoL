# ToLiss SimBrief Connector

The ToLiss SimBrief Connector is a standalone [plugin](../glossary.md#plugin) by hotbso that bridges SimBrief and the entire ToLiss fleet. It enables direct retrieval of the Operational Flight Plan (OFP) and transfer of flight data into the cockpit — without manual entry.

## Background

- **Developer:** hotbso (Holger Teutsch)
- **Repository:** [github.com/hotbso/toliss_simbrief](https://github.com/hotbso/toliss_simbrief) (open source, MIT license)
- **Platforms:** Windows, macOS, Linux (native binaries)
- **Compatibility:** [X-Plane](../glossary.md#x-plane) 12, ToLiss fleet (A319, A320 CEO/NEO, A321 CEO/NEO, A330neo, A340-600)
- **Price:** Free
- **Type:** Standalone X-Plane plugin (not a FlyWithLua script)

hotbso is also the developer of [openSAM](opensam.md) and [AutoDGS](autodgs.md).

!!! warning "Repository archived"

    The GitHub repository was archived in August 2025. The plugin still works with current X-Plane 12 and ToLiss versions but no longer receives updates.

## Features

- **OFP retrieval:** Fetch the Operational Flight Plan directly from simbrief.com
- **Data display:** Show key flight data (route, fuel, payload, wind, alternates) in the plugin window
- **Load & fuel transfer:** Transfer fuel and payload from the OFP directly into the aircraft
- **FMS file:** Load the flight plan as an FMS file
- **AviTab PDF:** Download the OFP as PDF to [AviTab](avitab.md)
- **Command bindings:** Exported commands (`tlsb/toggle`, `tlsb/fetch`, `tlsb/fetch_xfer`) can be bound to hardware buttons
- **VR support:** Window works in VR environments

## Value in Flight Simulation

Without the SimBrief Connector, the OFP must be retrieved manually and data entered individually into the cockpit. The plugin reduces this to a single click. Together with AviTab, the OFP is available as a PDF directly on the cockpit tablet.

## Installation

**Download:** [GitHub Releases](https://github.com/hotbso/toliss_simbrief/releases)

Extract the ZIP file to `Resources/plugins/`. This creates the `toliss_simbrief/` folder with the Linux binary at `lin_x64/toliss_simbrief.xpl`.

No additional system packages are required. There are no known Linux-specific issues.

!!! info "Not to be confused with simbrief_hub"

    The ToLiss SimBrief Connector is a standalone plugin that communicates directly with the SimBrief API. The separate plugin [simbrief_hub](https://github.com/hotbso/simbrief_hub) provides SimBrief data as datarefs for other plugins (e.g., for [AutoDGS](autodgs.md) and [openSAM](opensam.md)).

## Sources

- [ToLiss SimBrief Connector — GitHub](https://github.com/hotbso/toliss_simbrief)
- [hotbso — GitHub profile](https://github.com/hotbso)
