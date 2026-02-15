# SayIntentions.AI

SayIntentions.AI is an AI-based Air Traffic Control (ATC) system for flight simulators. The pilot communicates with AI-powered air traffic control via microphone — the system uses speech recognition and large language models (LLM) for natural, dynamic responses. The SayIntentions Client is **Windows-only** — Linux users need a Windows VM (KVM/QEMU) with UDP port forwarding to run the client alongside [X-Plane](../glossary.md#x-plane) on the host.

## Background

- **Developer:** SayAgain Solutions, LLC
- **Website:** [sayintentions.ai](https://www.sayintentions.ai/)
- **Platforms:** Windows 10/11 only
- **Compatibility:** X-Plane 11/12, MSFS 2020/2024, Prepar3D v5/v6
- **Price:** Premium $18.95/month (or ~$16.25/month billed annually); Entourage (no ATC) $49.95 one-time; 24h free trial

## Features

- **AI ATC:** 24/7 worldwide coverage at ~88,000 airports, full IFR/VFR support
- **Natural voice communication:** Pilot speaks freely via microphone, AI responds dynamically (no menu selection)
- **650+ AI voices:** Regionally distinct accents in 15 languages
- **ACARS/CPDLC:** Text-based communication between pilot and ATC
- **AI Co-Pilot:** Handles radio communications and checklists
- **Traffic injection:** Commercial and GA traffic from real-world schedules
- **Taxi arrows:** Visual taxi guidance in the simulator

Communication with X-Plane uses DataRefs and UDP (port 49000).

## KVM Setup

Since the SayIntentions Client does not run on Linux and Wine/Proton is impractical (microphone access, Windows-specific APIs), the client must run inside a Windows VM.

A community project for macOS ([SayIntentionsForMac](https://github.com/paulfisher53/SayIntentionsForMac)) demonstrates the approach using a Windows VM with UDP port forwarding. This principle can be adapted for KVM/QEMU.

**Requirements**

- Windows 10+ guest in KVM/QEMU (see [Docker & Virtualization](../docker.md) for KVM basics)
- Bridged or NAT networking with host access
- Microphone passthrough to the VM (for speech recognition)
- X-Plane running on the Linux host

**Connection**

The SayIntentions Client communicates with X-Plane over UDP port 49000. With bridged networking, the Windows VM resides on the same network segment as the host. The UDP communication must be forwarded between the VM and native X-Plane — the [SayIntentionsForMac](https://github.com/paulfisher53/SayIntentionsForMac) project provides `sudppipe.exe` and a dummy `X-Plane.exe` to redirect the client to the host IP. This setup has been successfully tested with a KVM VM and native X-Plane on the Linux host.

## Sources

- [SayIntentions.AI — Official Website](https://www.sayintentions.ai/)
- [SayIntentions.AI — Pricing](https://www.sayintentions.ai/pricing)
- [SayIntentions.AI — Features Overview](https://sayintentionsai.freshdesk.com/support/solutions/articles/154000219433)
- [SayIntentionsForMac — GitHub (Community Workaround)](https://github.com/paulfisher53/SayIntentionsForMac)
