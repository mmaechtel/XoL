# Clearance

When obtaining an IFR clearance (Instrument Flight Rules), the pilot must prepare for several important pieces of information. Here is a minimal summary:

## Preparation
* **Jeppesen or Navigraph Charts** – for SIDs, waypoints and frequencies.
* **FMS and navigation databases** – for flight route validation and entries.
* **Flight plan** (created with e.g. Simbrief) is then available as PDF
* **ATIS frequency or digital request (e.g. via Hoppie network)** for current weather information and active runway
* **FMGS/MCDU** program according to flight plan

## Phraseology

*Pilot*:
"Frankfurt Delivery, Lufthansa 123, IFR to Munich, stand A16, information Alpha, request clearance."

*ATC*:
"Lufthansa 123, cleared to Munich via MARUN 3F departure, initial climb 5000 feet, squawk 4712, contact departure on 119.9."

## Where to find the necessary information
1. **Clearance-Delivery Frequency** - to request clearance, found on airport chart (10-9)
2. **Flight number and aircraft identification** - flight plan or programmed FMGS/MCDU
3. **Departure and destination airport** - flight plan or programmed FMGS/MCDU
4. **Planned flight path, Departure** – flight plan or programmed FMGS/MCDU, possibly adapted according to changed runway (see ATIS)
5. **Target altitude (initial climb altitude)** – often given on the departure (SID) chart
6. **Radio frequency for departure** - often given on the departure (SID) chart.
7. **Squawk** - is individual, listen carefully!

## Digital clearance retrieval
* **AOC Menu in MCDU** (if available) allows e.g. obtaining a Predeparture Clearance (PDC) digitally.

### **ToLiss Airbus – Request Departure Clearance via CPDLC**

1. **Access MCDU Menu**:

    * Press `<MCDU MENU>`, then `<ATSU>`, followed by `<AOC MENU>`, and finally `<DEPARTURE CLEARANCE>`.

2. **Fields that need to be filled**:

    * **Flight Number**: Automatically taken from the INIT page, but can be manually changed.
    * **Departure Airport**: Also automatically filled, can be adjusted if needed.
    * **Arrival Airport**: Taken from the FMGS.
    * **Gate Number**: Enter manually (e.g., `A14`).
    * **ATIS ID**: Enter the current ATIS ID (e.g., `D`).
    * **Station ID** (bottom right): Enter the **Hoppie ID** of the ATC controller, for VATSIM e.g., `EDDH`. You can also check the airport ATIS for information about it or [Hoppie](https://www.hoppie.nl/acars/system/online.html).

3. **Send request**:

    * Once all fields are correctly filled **and** a valid Hoppie login is entered in the ISCS, an `*` appears next to **<REQUEST SEND>**.
    * Press `<REQUEST SEND>` to send the clearance request via telex.

4. **Receive and confirm message**:

    * The Pre-Departure Clearance appears on the **Received Messages** page.
    * There you can read it and confirm/accept it with LSK.


**Note**: Without a valid Hoppie code or if required fields are missing, sending the request is not possible.

## What's next?

Once the clearance has been correctly read back, continue with:

* [Pushback & Taxi](pushback_taxi.md) – request pushback and taxi to the runway

---

## Further Reading

| Topic | Page | Focus |
|---|---|---|
| Weather Briefing | [Weather Briefing](../weather/briefing.md) | ATIS and weather preparation before requesting clearance |
| VATSIM | [VATSIM](../vatsim/vatsim.md) | Online ATC clearance on the VATSIM network |
| Approach | [Approach](approach.md) | Approach clearance and STAR procedures |
| Landing & Taxi In | [Landing & Taxi In](landing.md) | Complete gate-to-gate ATC overview |