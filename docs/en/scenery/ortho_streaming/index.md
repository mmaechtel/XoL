---
description: "Ortho streaming for X-Plane on Linux: AutoOrtho and XEarthLayer deliver satellite imagery on demand via FUSE, combinable with local Ortho4XP tiles."
---
# Ortho Streaming

AutoOrtho and XEarthLayer stream satellite imagery on demand via a virtual FUSE filesystem directly into X-Plane — global coverage without local pre-generation. AutoOrtho in its active fork version 2.0 features a native C pipeline for faster loading, while XEarthLayer uses Rust with adaptive prefetching that switches between ring preloading on the ground and track prediction during cruise. Both systems can be combined with local Ortho4XP tiles: static tiles take priority in the `scenery_packs.ini`, streaming fills the rest.

- **[AutoOrtho](autoortho.md)** — Ortho streaming for global coverage
- **[XEarthLayer](xearthlayer.md)** — Rust-based streaming with adaptive prefetch
- **[Static + Streaming](static_plus_streaming.md)** — Combine both systems
