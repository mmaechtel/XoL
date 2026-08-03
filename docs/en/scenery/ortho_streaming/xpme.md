---
description: "XPME (X-Plane Map Enhancement) streams satellite imagery into X-Plane 12 through a mounted virtual filesystem. Linux setup, free tier versus paid Pro subscription, and comparison with AutoOrtho and XEarthLayer."
---
# XPME (X-Plane Map Enhancement)

**X-Plane Map Enhancement (XPME)** is a third streaming solution alongside [AutoOrtho](autoortho.md) and [XEarthLayer](xearthlayer.md). It loads satellite imagery at runtime and substitutes it for X-Plane's ground textures, so it fills the same role as the two established tools: global [orthophoto](../../glossary.md#orthophotos) coverage without generating tiles offline beforehand. The developer is `derekhe`, published under the AIFlyGo brand; the application is closed source, and GitHub is used only to host release binaries.

XPME is one product family covering two simulators — Microsoft Flight Simulator and X-Plane. Only the X-Plane side is relevant here, and it has its own documentation, its own base packages, and its own license.

The decisive difference from the alternatives is the licensing model. XPME is freemium: the free tier is usable but capped, and the features most people associate with ortho streaming — high-resolution ground textures and preloading — sit behind a paid subscription. AutoOrtho and XEarthLayer are free and open source. That is not a verdict on quality, but it is the first thing to weigh before investing setup time.

!!! warning "Pro Is a Subscription, Not a Purchase"
    The order form at `k.aiflygo.com/purchase` prices the X-Plane 12 license at **$5 for 30 days** and **$40 for 365 days** — the form builds its price display dynamically, so confirm the current figures there before paying. There is no perpetual license. One license is valid for exactly one PC, is bound to the hardware (changing the CPU or disk, or reinstalling the system, can invalidate it), and commercial use — flight schools, training centres, any for-profit operation — is explicitly prohibited. Payment runs through PayPal or Buy Me a Coffee; the vendor states a 7-day refund window.

## How It Works

XPME mounts a **virtual filesystem** into the X-Plane scenery tree and answers texture reads from the network instead of from disk — the same principle described under [How Ortho Streaming Works](how_streaming_works.md). The platform-specific mount layer is what the dependency list reveals: WinFSP on Windows, FUSE-T on macOS, and [FUSE](../../glossary.md#fuse-filesystem-in-userspace) 3 on Linux. Imagery is fetched, compressed to [DDS](../../glossary.md#dds-directdraw-surface), and handed to the simulator; the documentation names the DDS conversion as a main source of CPU load.

Unlike AutoOrtho and XEarthLayer, XPME does not read the terrain [mesh](../../glossary.md#mesh) from X-Plane's own scenery. It ships **base packages** — regional [DSF](../../glossary.md#dsf-distribution-scenery-format)/terrain data generated with a modified [Ortho4XP](../../glossary.md#ortho4xp) fork at ZL16 — which take the same role that the DSF/TER packages take in XEarthLayer. Base packages cannot be installed by hand: they are hosted on Cloudflare and pulled by the in-app downloader, which uses `aria2c` as its transfer backend and installs the selected packages sequentially. Users behind restrictive networks are told to configure an HTTP proxy or a VPN.

Map sources selectable in the interface are Bing, ArcGIS, Google, and Apple. Switching sources mid-flight is possible but does not take effect immediately — X-Plane has to reload the affected textures.

**What is not documented**

- **Cache architecture.** Settings expose a clearable image cache and the docs warn against slow storage, but there is no published description of cache tiers, sizing, or eviction.
- **Imagery zoom levels.** ZL16 refers to the mesh in the base packages. No zoom level is published for the streamed imagery in either tier.
- **What "high-resolution ground textures" means.** The Pro feature is described in marketing terms only; no resolution, no zoom level, no figures.

Nothing here should be inferred from the behaviour of AutoOrtho or XEarthLayer — the implementations are unrelated and XPME's is not open to inspection.

---

## Free Tier and Pro Subscription

The vendor FAQ is precise about the split:

| Aspect | Free | Pro |
|---|---|---|
| Map sources | ArcGIS, Bing, Google Maps | Additional sources, higher image quality, more frequent updates |
| Image quality setting | Medium only | High-quality settings available |
| Map colour adjustment | No | Yes |
| Preloading | No | Yes |
| High-resolution ground textures | No | Yes |
| New features | Later | First |
| Price | Free | $5 / 30 days, $40 / 365 days, one PC per license |

Two of these matter more than the rest. **Preloading** is the vendor's own recommended remedy for the two most common complaints — blurry imagery and stuttering when tiles arrive late — and it is a Pro-only feature. **High-resolution ground textures** is the feature that makes XPME comparable to what AutoOrtho and XEarthLayer deliver for free. The free tier is therefore best understood as a functional trial of the pipeline rather than a permanent configuration.

Note that the money buys packaging and convenience, not the imagery: copyright to the map data belongs to the map providers, and the vendor states the tool is for entertainment use only.

## System Requirements

| Requirement | Detail |
|---|---|
| Operating system | Linux x86_64 with FUSE 3 |
| Simulator | X-Plane 12 (X-Plane 11 works for some users but is not officially supported) |
| Runtime | .NET 10 runtime and ASP.NET Core 10 runtime |
| Download helper | `aria2` |
| Storage | SSD for base packages and cache — the docs explicitly advise against HDDs and external drives |
| Internet connection | Fast and low-latency; the client opens roughly 200 parallel connections by default |
| Memory | Generous headroom; the docs describe the tool as memory-intensive and offer a "Memory Optimization" option in the advanced settings |

The .NET 10 dependency is the one worth checking before anything else. Distributions package .NET on very different schedules, and on Debian stable the `dotnet-runtime-10.0` package may not be available from the standard repositories — in that case the Microsoft package feed or a distribution backport is required.

## Installation on Linux

Install the dependencies first. On Debian-based systems the vendor documents this command:

```bash
sudo apt install libfuse3-dev aria2 dotnet-runtime-10.0 aspnetcore-runtime-10.0
```

Then fetch the application from the [release repository](https://github.com/derekhe/xplane-map-enhancement-release/releases). Linux is served as an `.AppImage` and as a `_amd64.deb`:

```bash
# Debian package
sudo dpkg -i xplane-map-enhancement_<version>_amd64.deb

# or AppImage — no installation, just make it executable
chmod +x xplane-map-enhancement-<version>.AppImage
./xplane-map-enhancement-<version>.AppImage
```

!!! warning "Linux Builds Are Release-Dependent"
    Not every release ships Linux assets. Several releases contain only the Windows `.exe` and the macOS `.dmg`, including recent ones — the `.AppImage` and `.deb` appear in most releases but not reliably in the newest. Check the asset list of the release before downloading, and fall back to the most recent release that does include a Linux build.

After the first start, open the settings and set the **base package path** on a fast SSD, then use the "Downloader" view to select and install the regions to be flown. Downloads run sequentially and can be large. The application must be running and started before X-Plane so that the virtual filesystem is mounted; on exit the order is reversed — close X-Plane first, then press "Stop" in XPME, otherwise the mount is not cleaned up properly.

## Known Limitations on Linux

Only what the vendor documents or what the release history shows:

- **Irregular Linux builds.** See the warning above. There is no commitment to a Linux asset per release, so an update may mean staying on an older version for a while.
- **Windows-centric documentation.** Setup guides, FAQ, and troubleshooting are written for Windows. WinFSP notes, NTFS requirements, antivirus exclusions, and page-file advice do not apply to Linux and have no documented Linux equivalents. The underlying point of the page-file advice does carry over: the tool needs memory headroom.
- **Scenery conflicts.** Ortho4XP and X-Plane HD Mesh Scenery override XPME's base packages and are named as known conflicts — they have to be removed or disabled, so mixing XPME with existing [static tiles](static_plus_streaming.md) is not supported the way it is with AutoOrtho or XEarthLayer.
- **CPU load during loading is expected.** The vendor states that X-Plane 12 is not optimized for this kind of texture substitution and that image processing plus DDS conversion is inherently expensive. Preloading with high-resolution textures enabled is explicitly called out as capable of degrading simulator performance.
- **Base packages cannot be installed manually.** If the in-app downloader cannot reach the Cloudflare-hosted packages, the documented remedy is a proxy or VPN — there is no offline path.
- **No independent Linux experience reports were verifiable** for this page. The relevant community thread lives on a forum that blocks automated retrieval, so nothing here rests on it.

---

## Comparison with AutoOrtho and XEarthLayer

| Dimension | XPME | AutoOrtho | XEarthLayer |
|---|---|---|---|
| Source code | Closed | Open (GPL) | Open |
| Cost | Free tier capped, Pro subscription | Free | Free |
| Platform | Windows, macOS, Linux | Windows, Linux, macOS (Apple Silicon) | Linux only |
| Mount layer | WinFSP / FUSE-T / FUSE 3 | FUSE | FUSE |
| Terrain data | Own base packages (Ortho4XP-derived, ZL16), in-app downloader | Uses X-Plane scenery plus overlay downloads | DSF/TER packages via `xearthlayer packages install` |
| Map sources | Bing, ArcGIS, Google, Apple (three of them in the free tier) | Bing, Google, Here, Yandex, Apple | Bing, Google, Apple, ArcGIS, MapBox, USGS |
| Imagery zoom level | Not documented | Up to ZL18 | Provider-dependent |
| Cache | Not documented (clearable from the UI) | Configurable size, automatic eviction | Three-tier, configurable |
| Configuration | [GUI](../../glossary.md#gui-graphical-user-interface) | GUI | CLI plus `config.ini` |
| Combinable with Ortho4XP tiles | No — documented conflict | Yes | Yes |

**Which system is a better fit?**

- **Linux users who want maximum control**: XEarthLayer and AutoOrtho are open, free, tunable down to thread counts and cache tiers, and their behaviour can be inspected when something goes wrong. XPME offers none of that — its internals are undocumented and its Linux builds are not guaranteed per release.

- **Users who already keep Ortho4XP tiles**: XPME is the wrong tool. Ortho4XP is a documented conflict and must be removed, whereas [combining static tiles with streaming](static_plus_streaming.md) is a supported workflow for the other two.

- **Users flying several simulators**: XPME is the only one of the three that covers both X-Plane and Microsoft Flight Simulator with one product family and one interface, which is its clearest structural advantage.

---

## Further Reading

| Topic | Page | Focus |
|---|---|---|
| AutoOrtho | [AutoOrtho](autoortho.md) | Free streaming with wide platform support |
| XEarthLayer | [XEarthLayer](xearthlayer.md) | Rust-based Linux streaming with GPU encoding |
| How Ortho Streaming Works | [How Ortho Streaming Works](how_streaming_works.md) | DSF → .ter → DDS chain, FUSE interception, caching |
| Ortho4XP | [Ortho4XP](../orthophotography/ortho4xp.md) | Generating static ortho tiles offline |
| Static + Streaming | [Static + Streaming](static_plus_streaming.md) | Combining local tiles with streaming |
| Filesystem | [Filesystem](../../linux/optimizations/filesystem.md) | I/O tuning for base packages and cache |

---

## Sources

- [X-Plane Map Enhancement Releases](https://github.com/derekhe/xplane-map-enhancement-release/releases)
- [Download and Installation](https://www.aiflygo.com/docs/xplane-map-enhancement/download/) — AIFlyGo
- [Software Usage and Configuration](https://www.aiflygo.com/docs/xplane-map-enhancement/usage/) — AIFlyGo
- [FAQ Guide](https://www.aiflygo.com/docs/xplane-map-enhancement/faq/) — AIFlyGo
- [License Terms](https://www.aiflygo.com/docs/license/) — AIFlyGo
- [Order Form](https://k.aiflygo.com/purchase) — AIFlyGo
