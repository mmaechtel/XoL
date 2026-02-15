# My FS Flights

My FS Flights is a cloud-based flight tracking and analysis platform that automatically records flights, generates detailed reports, and provides AI-enhanced landing feedback. The companion app is **Windows-only** — Linux users need a Windows VM (KVM/QEMU) to run it alongside [X-Plane](../glossary.md#x-plane) on the host.

## Background

- **Developer:** Agile Software Management Limited (York, UK)
- **Website:** [myfs.flights](https://myfs.flights/)
- **Platforms:** Windows 10+ only (Microsoft Store or direct download)
- **Compatibility:** X-Plane 11/12, MSFS 2020/2024, Prepar3D v4–v6

## Features

- **Automatic flight recording:** Starts when engines run, stops at shutdown — no pre-flight setup required
- **Detailed flight reports:** Approximately 10 pages per flight with stage-by-stage breakdown
- **AI landing analysis:** Approach evaluation, glide slope tracking, threshold height, touchdown speed, rollout assessment
- **Takeoff analysis:** Runway alignment, takeoff distance, liftoff speed, climb profile
- **3D flight profile:** Interactive three-dimensional visualization of the flight path
- **Flight logbook:** Auto-generated descriptions, personal notes, tags, screenshots
- **Statistics dashboard:** Flying time, distance, leaderboards
- **Route discovery:** Flight route suggestions with SimBrief integration
- **Live flight sharing:** Real-time tracking shareable via link

Flight reports and dashboards are accessible from any browser. Only the data collection component requires the Windows app.

## KVM Setup

Since My FS Flights has no Linux build, it must run inside a Windows VM. The app detects simulators automatically — for this to work across the VM boundary, the VM needs network access to the X-Plane host.

**Requirements**

- Windows 10+ guest in KVM/QEMU (see [Docker & Virtualization](../docker.md) for KVM basics)
- Bridged or NAT networking with host access
- X-Plane running on the Linux host

**Connection**

The exact mechanism My FS Flights uses to connect to X-Plane is not publicly documented. X-Plane broadcasts its presence via UDP multicast (beacon on 239.255.1.1:49707). With bridged networking, the Windows VM resides on the same network segment as the host, which allows discovery of the X-Plane instance.

!!! warning "Untested on Linux"

    This KVM approach is documented based on the tool's architecture. Whether My FS Flights reliably discovers and connects to an X-Plane instance on the Linux host has not been independently verified. Feedback is welcome.

## Sources

- [My FS Flights — Official Website](https://myfs.flights/)
- [My FS Flights — Microsoft Store](https://apps.microsoft.com/detail/9pgb7ngn6l24)
- [What is My FS Flights? — Blog](https://blog.myfs.flights/posts/about-my-fs-flights/)
