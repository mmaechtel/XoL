---
description: "AOC Datalink Center für X-Plane 12 — kostenloses natives Plugin für ToLiss: Hoppie-ACARS, CPDLC, PDC, SimBrief-OFP, OOOI und Wetter-Monitore per WebUI."
---
# AOC Datalink Center

AOC Datalink Center holt die Arbeit eines Airline-Operations-Centers in [X-Plane](../../glossary.md#x-plane) 12: Wetterpakete als ACARS-Uplinks, Freitext-Telex, CPDLC und PDC über das Hoppie-Netzwerk, automatische OOOI-Meldungen und Hintergrund-Monitore entlang der Route. Es ist für den ToLiss Airbus ausgelegt und läuft als natives [Plugin](../../glossary.md#plugin) mit einer Browser-WebUI — auch vom Tablet im Homecockpit aus bedienbar.

## Hintergrund

- **Entwickler:** Vito Jackson (Isar Simworks, München)
- **Website:** [isarsimworks.de](https://isarsimworks.de/)
- **Lizenz:** Kostenlos, nur private Nutzung, keine Weitergabe
- **Plattformen:** Windows x64, Linux x64 (natives Plugin)
- **Kompatibilität:** X-Plane 12, ToLiss Airbus
- **Abhängigkeiten:** Keine (kein XPPython3); unter Linux die System-libcurl und glibc 2.17 oder neuer
- **Konten:** Hoppie-Logon-Code (kostenlos auf hoppie.nl), SimBrief-Benutzername

Der Entwickler bietet unter gleichem Namen zusätzlich ein eigenständiges Windows-Desktopprogramm an. Es ist ein separates Paket — diese Seite beschreibt das Plugin.

## Funktionsumfang

- **Wetterpakete:** METAR, TAF, SIGMET/AIRMET und D-ATIS als ACARS-Uplinks ins Flugzeug
- **SimBrief-Integration:** LOAD OFP füllt Callsign, Stationen, Flow-Routen, ATIS-Station und geplantes Gate aus; Loadsheet, OFP-Zusammenfassung und PDC werden als Uplinks gesendet
- **Telex und CPDLC:** Freitext-Nachrichten mit Vorlagen und automatischer Segmentierung, CPDLC und PDC über Hoppie
- **OOOI-Meldungen:** Automatische OUT/OFF/ON/IN-Meldungen mit Gate-Erkennung, Flugplanzeiten und Verspätung
- **Monitore:** Wetteränderungen an Ziel und Ausweichflughafen, SIGMET entlang des Korridors, neue ATIS-Buchstaben, ECFMP-Flow-Maßnahmen
- **Route-ATC-Monitor:** Ermittelt die von der SimBrief-Route gekreuzten FIRs und meldet VATSIM- oder IVAO-Lotsen, die online oder offline gehen — sektorbezogen anhand der Flugzeugposition
- **Oberflächen:** WebUI in zwei Layouts (Classic und Cockpit Rail), EFB-Ansicht für Tablets und ein In-Sim-Panel in X-Plane
- **Selbsttest:** Prüft jede Datenquelle und nennt die Ursache von Timeouts oder DNS-Sperren

## Mehrwert in der Flugsimulation

Datalink im Cockpit wird erst mit einer Gegenstelle am Boden lebendig. AOC Datalink Center übernimmt dieses Dispatch-Büro: Wetter, Freigaben und Loadsheets kommen ins Cockpit wie von einem echten Airline-OPS-Center, während die Monitore im Reiseflug mitlaufen. Auf VATSIM zeigt der Route-ATC-Monitor, welche Sektoren voraus besetzt sind.

## Installation

**Download:** [isarsimworks.de](https://isarsimworks.de/)

Den Ordner `plugins` aus dem Paket nach `Resources/` kopieren. Es entsteht `Resources/plugins/AOCDatalinkCenter/` mit den Plattformordnern `win_x64/` und `lin_x64/` sowie der Datei `AOCDatalinkCenter.dat`, die die WebUI enthält und neben den Plattformordnern liegen muss. X-Plane lädt den passenden Build automatisch.

Unter Linux nutzt das Plugin die System-libcurl für HTTPS. Fehlt sie, lässt sie sich über den Paketmanager nachinstallieren, etwa unter Debian/Ubuntu:

```bash
sudo apt install libcurl4
```

Anschließend die WebUI über **Plugins → AOC Datalink Center → Open WebUI** oder unter `http://localhost:8785/` öffnen (vom Tablet aus die IP-Adresse des Sim-PCs verwenden). Im Reiter SETUP den Hoppie-Logon-Code eintragen und mit Enter speichern. Im Reiter SIMBRIEF den SimBrief-Benutzernamen oder die Pilot-ID eintragen, dann auf LOAD OFP klicken. Einstellungen und gelernte Gates liegen in `Output/preferences/AOCDatalinkCenter/`.

!!! note "Port 8785 und ältere Versionen"

    Das Plugin, die ältere XPPython3-Version, das Desktopprogramm und das frühere FlyWithLua-Skript nutzen alle Port 8785 — nur eines davon betreiben oder in SETUP einen anderen Port setzen. Vor dem Umstieg die alte XPPython3-Kopie (`PythonPlugins/PI_AOC_Datalink_Center.py` und den Ordner `PythonPlugins/AOCDatalinkCenter`) sowie das frühere FlyWithLua-Skript entfernen. Beim ersten Start kopiert das Plugin Einstellungen und gelernte Gates nach `Output/preferences/AOCDatalinkCenter/`; die Originale bleiben erhalten. Die WebUI hat kein Passwort, den Port daher nicht ins Internet weiterleiten.

### Linux-Hinweise

Dieses Setup wurde erfolgreich unter Linux getestet: Das X-Plane-Log meldet das libcurl-Netzwerk-Backend, die native Initialisierung und die WebUI auf Port 8785.

## Quellen

- [Isar Simworks — Offizielle Website](https://isarsimworks.de/)
- [AOC Datalink Center — Handbuch (PDF, EN)](https://isarsimworks.de/dl.php?f=AOC_Datalink_Center_Manual_EN.pdf)
- [Hoppie ACARS](https://www.hoppie.nl/acars/)
