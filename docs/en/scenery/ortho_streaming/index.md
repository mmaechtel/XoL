---
description: "Ortho streaming for X-Plane on Linux: AutoOrtho, XEarthLayer and XPME deliver satellite imagery on demand via FUSE, combinable with local Ortho4XP tiles."
---
# Ortho Streaming

AutoOrtho and XEarthLayer stream satellite imagery on demand via a virtual FUSE filesystem directly into X-Plane — global coverage without local pre-generation. AutoOrtho in its active fork version 2.0 features a native C pipeline for faster loading, while XEarthLayer uses Rust with adaptive prefetching that switches between ring preloading on the ground and track prediction during cruise. Both can be combined with local Ortho4XP tiles: static tiles take priority in the `scenery_packs.ini`, streaming fills the rest. XPME is a third option, closed source and freemium — its high-resolution textures require a paid subscription, and it conflicts with existing Ortho4XP tiles.

- **[How Ortho Streaming Works](how_streaming_works.md)** — X-Plane's texture loading chain, FUSE virtual filesystem, and the streaming pipeline
- **[AutoOrtho](autoortho.md)** — Ortho streaming for global coverage
- **[XEarthLayer](xearthlayer.md)** — Rust-based streaming with adaptive prefetch
- **[XPME](xpme.md)** — Closed-source freemium alternative with its own base packages
- **[Static + Streaming](static_plus_streaming.md)** — Combine both systems
