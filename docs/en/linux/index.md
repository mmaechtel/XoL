---
description: "Linux tuning for X-Plane: kernel profiles, GPU drivers, display server choice, filesystem optimization, and tools for Windows-only addons."
---
# Linux Optimizations for X-Plane

Linux offers tuning points at every layer of the system that directly affect X-Plane's runtime behavior — from kernel scheduler to GPU driver to display server. The system section focuses on latency tuning: two profiles for different kernel types plus matching monitoring tools for verification. The optimizations section covers the concrete components — NVIDIA driver, Liquorix kernel, X11 vs. Wayland, and filesystem configuration. For Windows-only addons and development tools, KVM, Wine, Docker, and Python environments are available.

- **[System](system/index.md)** — Tuning, monitoring
- **[Optimizations](optimizations/index.md)** — Drivers, kernel, display server, filesystem
- **[Extensions](extensions/index.md)** — KVM, Docker, Wine, pyenv, zsh