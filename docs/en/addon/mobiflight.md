# MobiFlight

MobiFlight is an open-source middleware for building home cockpits. The software connects microcontrollers (Arduino, Raspberry Pi Pico) to [X-Plane](../glossary.md#x-plane) and translates simulator variables into physical outputs (LEDs, 7-segment displays, stepper motors) and vice versa, converting physical inputs (switches, encoders, potentiometers) into simulator commands. The MobiFlight Connector is **Windows-only** — Linux users need a network split (Connector on a Windows machine or KVM/QEMU VM) to use it alongside X-Plane on the host.

## Background

- **Developer:** Sebastian Möbius (community project, MIT license)
- **Website:** [mobiflight.com](https://www.mobiflight.com)
- **GitHub:** [MobiFlight/MobiFlight-Connector](https://github.com/MobiFlight/MobiFlight-Connector)
- **Platforms:** Windows 10+ only (.NET Framework 4.8, Windows Forms)
- **Compatibility:** X-Plane 11/12, MSFS 2020/2024, Prepar3D

## Features

- **DataRef access:** Read and write any X-Plane DataRef via UDP (port 49000)
- **Commands:** Trigger X-Plane commands (e.g. `sim/autopilot/heading_up`)
- **Aircraft detection:** Automatically switches configuration based on the loaded aircraft
- **HubHop presets:** Over 7,000 community presets for various aircraft (Zibo 737, ToLiss A320, etc.)
- **Hardware support:** Arduino Mega/Nano/Pro Micro, Raspberry Pi Pico, MIDI controllers, HID devices, commercial panels (Winwing, VKB, Octavi)
- **No X-Plane plugin required:** Communication uses X-Plane's built-in UDP interface — no additional plugin needed

## KVM Setup

Since the MobiFlight Connector does not run on Linux (Wine/Proton is impractical due to deep Windows API dependencies), there are two approaches:

### Network Split (recommended)

MobiFlight communicates with X-Plane over UDP — the protocol is network-based and platform-independent. This enables a split setup:

- **Linux PC:** X-Plane 12 (native)
- **Windows PC or VM:** MobiFlight Connector + connected hardware

In MobiFlight, enter the IP address of the Linux PC (instead of `127.0.0.1`). X-Plane accepts UDP connections on port 49000 by default.

### Windows VM with USB Passthrough

If no second machine is available, a Windows VM (KVM/QEMU) on the Linux host can run the Connector. The Arduino hardware is passed through to the VM via USB passthrough (see [Docker & Virtualization](../docker.md) for KVM basics).

**Requirements**

- Windows 10+ guest in KVM/QEMU
- USB passthrough configured for Arduino/Pico boards
- Bridged or NAT networking with host access (for UDP port 49000)

For UDP forwarding between the VM and native X-Plane on the host, [SayIntentionsForMac](https://github.com/paulfisher53/SayIntentionsForMac) works well — the project provides `sudppipe.exe` and a dummy `X-Plane.exe` that forward the UDP connection directly to the host. This eliminates the need to install any additional plugin in X-Plane. This setup has been successfully tested.

## Sources

- [MobiFlight — Official Website](https://www.mobiflight.com)
- [MobiFlight — GitHub Repository](https://github.com/MobiFlight/MobiFlight-Connector)
- [MobiFlight — Documentation](https://docs.mobiflight.com)
- [MobiFlight — X-Plane Quick Start Guide](https://www.mobiflight.com/en/tutorials/x-plane-quick-start-guide.html)
- [HubHop — Community Preset Database](https://hubhop.mobiflight.com)
