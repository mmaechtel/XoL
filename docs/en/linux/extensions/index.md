---
title: "KVM, Wine, Docker: Linux Utilities"
description: "Linux utilities for X-Plane: KVM for Windows VMs, Wine for installers, Docker containers, pyenv for Python plugins, and zsh shell setup."
---
# Utilities

Not every X-Plane tool runs natively on Linux, and not every Linux default suits a simulator workstation. This section collects the utilities that close those gaps — from full Windows virtualization down to shell configuration.

[KVM](kvm.md) provides a complete Windows VM on Debian with USB passthrough — the route for addons such as StreamDeck or MobiFlight that have no Linux build at all; the [Via KVM](../../addon/kvm/index.md) addon section builds on it. [Wine](wine.md) is the lighter option for simpler Windows installers and helper tools, including 32-bit support and Winetricks. [Docker](docker.md) isolates development and test environments from the host's package setup. [pyenv](pyenv.md) manages parallel Python versions for scripting and plugin development without touching the system Python. [zsh](zsh.md) rounds it off with a more capable shell for daily system work: autocompletion, syntax highlighting, and plugins.

Read KVM first if a Windows-only addon is the reason for visiting; the remaining chapters are independent and can be picked as needed.

- **[KVM](kvm.md)** — Windows virtualization for add-ons without native Linux support
- **[Docker](docker.md)** — Isolated development and testing environments
- **[Wine](wine.md)** — Windows-based tools and installers
- **[pyenv](pyenv.md)** — Python environments for scripting and plugins
- **[zsh](zsh.md)** — Powerful shell configuration
