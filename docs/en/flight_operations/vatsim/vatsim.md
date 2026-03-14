---
description: "Getting started with VATSIM for X-Plane — account setup, client installation, and flight planning with optimal ATC coverage via the ATC Flight Planner."
---
# VATSim

VATSIM (Virtual Air Traffic Simulation Network) is the world's largest online aviation network for virtual flight simulation with realistic air traffic and air traffic control.

## What is VATSIM?

VATSIM offers pilots and air traffic controllers the opportunity to fly and work in a realistic environment. The network simulates real air traffic operations with:

- Realistic flight plans
- Live air traffic controllers
- Weather data
- Air traffic rules

## Getting Started

To begin with VATSIM:

1. **VATSIM Account** — register at [vatsim.net](https://vatsim.net)
2. **VATSIM Client** — download a compatible client (e.g., xPilot for X-Plane, vPilot for MSFS)
3. **Flight Plan** — create a realistic flight plan
4. **Training** — visit the [Pilot Learning Center](https://my.vatsim.net/learn) for basics

## Useful Links

- [VATSIM Website](https://vatsim.net)
- [Pilot Learning Center](https://my.vatsim.net/learn)
- [VATSIM Rules](https://vatsim.net/docs/policy)
- [Approved Software](https://vatsim.net/docs/policy/approved-software)

---

## ATC Flight Planner

The **[ATC Flight Planner](https://atc.emvisio.de)** is a webapp that finds VATSIM flight routes with maximum ATC coverage. It continuously collects controller bookings, event schedules, and live traffic data from VATSIM, then calculates which departure/arrival combinations offer the best controller coverage for a given time window and aircraft type.

### How It Works

The app pre-calculates ATC coverage time slots for airports worldwide based on booked controller sessions. When planning a flight, it correlates these slots with aircraft performance data (cruise speed, range) to determine which routes are realistically flyable and fully covered by active controllers. The result is a ranked list of origin-destination pairs — sorted by combined ATC coverage score.

### Planning a Flight

1. **Set aircraft and time** — choose aircraft type and preferred departure window
2. **Browse routes** — the app ranks airports by ATC availability, optionally filtered by coverage score, live traffic density, or runway length
3. **Explore the map** — airports are color-coded by coverage quality for visual route discovery
4. **Check ATC timeline** — a 7-day controller booking schedule shows exactly when coverage is available at each airport
5. **Dispatch to SimBrief** — one click generates a SimBrief flight plan with pre-filled origin, destination, aircraft, airline, and callsign

### Additional Features

- **Event integration** — browse upcoming VATSIM events and find matching departure or arrival airports within the event time window
- **Livery selection** — filter airline liveries by country and push them directly into the flight plan
- **Live traffic view** — see which airports currently have the most active pilots for a realistic traffic environment

!!! tip "Aircraft and livery configuration"
    The pre-configured aircraft types and liveries focus on ToLiss and X-Plane. All aircraft performance data (cruise speed, range, flight phase durations) can be individually adjusted to match any aircraft type.

---

## Further Reading

| Topic | Page | Focus |
|---|---|---|
| Clearance | [Clearance](../atc/clearance.md) | IFR clearance procedures and CPDLC |
| Pushback & Taxi | [Pushback & Taxi](../atc/pushback_taxi.md) | Ground movement procedures |
| En Route | [En Route](../atc/enroute.md) | Center control and frequency changes |
| Approach | [Approach](../atc/approach.md) | Approach and radar vectors |
| Weather Briefing | [Weather Briefing](../weather/briefing.md) | Weather preparation for online flights |
