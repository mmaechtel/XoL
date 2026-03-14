# Faktencheck: VATSim (EN + DE)

**Datum:** 2026-03-14
**Gepruefte Seiten:** `vatsim.md` (EN), `vatsim.md` (DE)
**Primaerquellen verifiziert:** vatsim.net, atc.emvisio.de, my.vatsim.net

---

## Fehler (3) — Korrekturbedarf

### 1. VATSIM Academy URL tot
**Datei:** `vatsim.md:44 (EN)`, `vatsim.md:39 (DE)`
**Behauptung:** "VATSIM Academy" verlinkt auf `academy.vatsim.net`
**Befund:** `academy.vatsim.net` liefert ECONNREFUSED — Subdomain existiert nicht mehr. VATSIM bietet stattdessen das "Pilot Learning Center" unter `https://my.vatsim.net/learn`.
**Korrektur:** Link und Text auf "Pilot Learning Center" / `https://my.vatsim.net/learn` aendern.

### 2. Client-Download-URL 404
**Datei:** `vatsim.md:46 (EN)`, `vatsim.md:41 (DE)`
**Behauptung:** Client Downloads verlinkt auf `vatsim.net/community/pilots/software`
**Befund:** URL liefert HTTP 404. Die korrekte Seite ist `https://vatsim.net/docs/policy/approved-software`.
**Korrektur:** URL auf `https://vatsim.net/docs/policy/approved-software` aendern.

### 3. "Register for free" nicht belegbar
**Datei:** `vatsim.md:36 (EN)`, `vatsim.md:34 (DE)`
**Behauptung:** "Register for free at vatsim.net" / "Registrieren Sie sich kostenlos"
**Befund:** Weder Website noch User Agreement bestaetigen explizit "kostenlos". VATSIM ist eine 501(c)(3)-Non-Profit und es existiert kein Bezahlvorgang, aber die Behauptung "for free" ist nicht direkt belegbar.
**Korrektur:** "for free" entfernen → "Register at vatsim.net"

## Nuancen (1) — verbesserbar, aber akzeptabel

### N1. A320-Default nicht verifizierbar
**Datei:** `vatsim.md:31 (EN)`, `vatsim.md:28 (DE)`
**Befund:** Die Webapp hat einen konfigurierbaren Aircraft-Selector mit Defaults pro Typ. Ob A320 tatsaechlich der Standard ist, laesst sich nicht aus der UI verifizieren. Da der Seitenbetreiber identisch ist, koennte das intern korrekt sein — aber die Formulierung "default to A320 cruise speed" ist oeffentlich nicht belegbar.

## Korrekt (9) — keine Aenderung noetig

| # | Behauptung | Quelle |
|---|------------|--------|
| 1 | VATSIM ist das groesste Online-Aviation-Netzwerk | vatsim.net: "the largest online aviation network" |
| 2 | App sammelt Controller-Buchungen, Events, Live-Traffic | atc.emvisio.de: booking/event/online Datentypen bestaetigt |
| 3 | Vorberechnete ATC-Coverage-Zeitfenster pro Flughafen | atc.emvisio.de: "Pre-calculated time slots", airport_slots Tabelle |
| 4 | Korrelation mit Aircraft-Performance-Daten | atc.emvisio.de: Flight-Phase-Konfiguration mit Speeds/Range |
| 5 | Geranktes Ergebnis nach Combined Coverage Score (0-9) | atc.emvisio.de: "Results are ranked by Combined Score (0-9)" |
| 6 | 7-Tage-Controller-Buchungsplan | atc.emvisio.de: "7-day overview" bestaetigt |
| 7 | SimBrief-Integration mit vorausgefuellten Feldern | atc.emvisio.de: Origin, Destination, Aircraft, Airline, Callsign |
| 8 | Livery-Filter nach Land | atc.emvisio.de: "Browse liveries filtered to the origin airport's country" |
| 9 | Live-Traffic-Anzeige mit Pilotenzahlen | atc.emvisio.de: Ground Traffic Filter (>=5, >=15) |
