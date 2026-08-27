---
title: Windows X-Plane Addons via KVM
description: "Three Windows-only X-Plane addons usable on Linux via KVM virtualization: My FS Flights, MobiFlight, and SayIntentions.AI."
---
# Via KVM

Three Windows-only addons made usable on Linux through [KVM virtualization](../../linux/extensions/kvm.md): a Windows guest runs the addon, X-Plane keeps running natively on the Linux host, and the two talk over the network. [My FS Flights](myfs_flights.md) records flights and gives AI-based landing feedback; its connector detects the simulator automatically, so the VM only needs network access to the host. [MobiFlight](mobiflight.md) links Arduino- or Pico-based hardware cockpits — either from a second Windows PC or from a VM with USB passthrough for the boards, plus a UDP relay for port 49000. [SayIntentions.AI](sayintentions.md) provides voice-controlled ATC and needs UDP port forwarding and microphone passthrough into the guest.

Unless a second Windows PC is available, set up the VM first via the KVM chapter — the addon pages build on a working Windows guest and only add the addon-specific networking and passthrough.

- **[My FS Flights](myfs_flights.md)** — Logbook and statistics
- **[MobiFlight](mobiflight.md)** — Hardware cockpit integration
- **[SayIntentions.AI](sayintentions.md)** — AI-powered ATC communication
