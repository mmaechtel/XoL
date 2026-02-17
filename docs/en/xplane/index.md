---
description: "X-Plane 12 on Linux: Vulkan rendering, Zink for plugins, shader caches, PipeWire audio, controller setup, and systematic GPU troubleshooting."
---
# X-Plane on Linux

X-Plane 12 uses Vulkan as its sole rendering API — most graphics settings work identically across platforms, but Linux adds specifics: Zink as the OpenGL bridge for plugins, Mesa shader caches, PipeWire audio, and controller detection via evdev. Setup & Diagnostics covers configuration and performance analysis — from the Microprofiler through MangoHUD to reproducible CLI benchmarks. The troubleshooting section addresses GPU device losses, safe mode options, and subsystem isolation for systematic debugging.

- **[Setup & Diagnostics](setup_diagnose/index.md)** — Configuration, performance analysis, and CLI diagnostics
- **[System Errors](systemfehler/index.md)** — GPU crashes, device losses, and systematic troubleshooting
