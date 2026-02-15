# SimReaperXP

SimReaperXP is a [FlyWithLua](flywithlua.md) script that recovers FPS in X-Plane 12 by selectively disabling resource-heavy rendering features. It provides toggleable switches for six expensive rendering systems, recovering approximately 10 FPS without reducing object density.

## Background

- **Developer:** alstr
- **Repository:** [github.com/alstr/simreaperxp](https://github.com/alstr/simreaperxp) (MIT license)
- **Platforms:** Windows, macOS, Linux (pure Lua)
- **Compatibility:** X-Plane 12
- **Price:** Free (open source)
- **Dependency:** [FlyWithLua NG+](flywithlua.md)

!!! warning "Official download is GitHub only"

    The version on X-Plane.org is unsupported and outdated. The developer has requested its removal. Only use the [GitHub release](https://github.com/alstr/simreaperxp).

## Features

- **Shadow Prep:** Removes cockpit shadow rendering (includes exposure adjustment if cockpit becomes too bright)
- **Cloud Shadow Render:** Stops clouds from calculating ground shadows
- **GBuff Lights:** Disables light casting on surfaces (can auto-reenable at night to prevent dark airports)
- **Planes:** Makes exterior aircraft models invisible while keeping the cockpit functional (can auto-reenable in exterior view)
- **Water:** Disables water rendering
- **Bump Maps:** Removes object surface bump textures

All features are toggleable via `Plugins > FlyWithLua > FlyWithLua Macros > SimReaperXP` or via keyboard assignments. All settings are fully reversible — no permanent file modifications.

## Value in Flight Simulation

Performance-heavy payware aircraft (Hot Start CL650, ToLiss A340) at detailed payware airports can push frame rates below comfortable levels. SimReaperXP trades specific visual details for significant FPS gains. Since the disabled features are selectable individually, users can find their own balance between visual quality and performance. Particularly useful for IFR flying where exterior visuals are secondary to cockpit instruments.

## Installation

**Download:** [GitHub Releases](https://github.com/alstr/simreaperxp)

Place `simreaperxp.lua` into `Resources/plugins/FlyWithLua/Scripts/`.

### Linux Notes

No Linux-specific issues are known. The script is a plain Lua text file and runs identically on all platforms supported by FlyWithLua.

## Sources

- [SimReaperXP — GitHub](https://github.com/alstr/simreaperxp)
