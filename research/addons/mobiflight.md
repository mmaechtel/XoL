# MobiFlight — Research Paper

**Datum:** 2026-02-15
**Kategorie:** Addons / Cockpit-Hardware
**Relevanz für XoL:** Hoch (Hardware-Cockpit-Anbindung unter Linux)
**Status:** Recherche abgeschlossen

---

## 1. Was ist MobiFlight?

MobiFlight ist ein Open-Source-Projekt (MIT-Lizenz), das es ermöglicht, einen eigenen Home-Cockpit für Flugsimulatoren zu bauen. Das Kernprodukt ist der **MobiFlight Connector** — eine Windows-Desktop-Anwendung (C#, .NET Framework 4.8, Windows Forms), die als Middleware zwischen Flugsimulator und physischer Hardware fungiert.

**Kernfunktion:** MobiFlight liest Simulator-Variablen (DataRefs, SimVars, FSUIPC-Offsets) und schreibt sie auf physische Hardware (LEDs, 7-Segment-Anzeigen, Stepper-Motoren, Servos, LCDs). Umgekehrt werden physische Eingaben (Schalter, Encoder, Potentiometer) als Simulator-Befehle zurückgespielt.

**Unterstützte Simulatoren:**

- Microsoft Flight Simulator 2020 (via WASM-Modul + SimConnect)
- Microsoft Flight Simulator 2024 (seit Version 10.5.0, Januar 2025)
- Prepar3D (via FSUIPC)
- X-Plane 11/12 (nativ via UDP seit ~2022, zuvor nur via XPUIPC)

**Offizielle Website:** https://www.mobiflight.com
**GitHub:** https://github.com/MobiFlight/MobiFlight-Connector (322 Stars, 136 Forks, Stand 2026-02)
**Lizenz:** MIT
**Hauptentwickler:** Sebastian Möbius (@DocMoebiuz), Neil Enns (@neilenns), weitere Community-Beitragende
**Dokumentation:** https://docs.mobiflight.com

---

## 2. Architektur und Funktionsweise

### 2.1 Gesamtarchitektur

```
┌──────────────────┐     ┌──────────────────────┐     ┌─────────────────┐
│  Flugsimulator   │◄───►│  MobiFlight Connector │◄───►│  Arduino/Pico   │
│  (X-Plane, MSFS) │     │  (Windows, C#/.NET)   │     │  (USB-Serial)   │
└──────────────────┘     └──────────────────────┘     └─────────────────┘
        ▲                         ▲                          ▲
   UDP/SimConnect           Windows Forms UI           MobiFlight Firmware
   FSUIPC/XPUIPC           Konfigurationslogik        auf Mikrocontrollern
```

### 2.2 Simulator-Anbindung: X-Plane 12

Die X-Plane-Anbindung nutzt die **XPlaneConnector**-Bibliothek (NuGet-Paket von MaxFerretti), die über **UDP Port 49000** kommuniziert — das ist X-Planes eingebaute Netzwerkschnittstelle für DataRef-Zugriff.

**Kein Plugin erforderlich:** Anders als bei MSFS (wo ein WASM-Modul installiert werden muss) ist für X-Plane kein zusätzliches Plugin in X-Plane nötig. Die Kommunikation läuft über X-Planes integrierte UDP-Schnittstelle.

**Funktionsumfang:**

- **Lesen:** Beliebige X-Plane DataRefs abonnieren (Polling-basiert, konfigurierbare Frequenz)
- **Schreiben:** Beschreibbare DataRefs mit Werten setzen
- **Commands:** X-Plane Commands auslösen (z.B. `sim/autopilot/heading_up`)
- **Aircraft-Erkennung:** Automatische Erkennung des geladenen Flugzeugs via `sim/aircraft/view/acf_ui_name`
- **HubHop-Presets:** Zugriff auf über 7.000 Community-Presets für verschiedene Aircraft

**Historisch:** Vor der nativen X-Plane-Integration (PR #826, gemerged Juni 2022 von @DocMoebiuz) war X-Plane nur über **XPUIPC** nutzbar — ein Plugin, das FSUIPCs Offset-basierte Variablen-Zugriffe auf X-Plane-DataRefs abbildet.

### 2.3 WASM-Modul (nur MSFS)

Das **MobiFlight-WASM-Module** (separates GitHub-Repository: https://github.com/MobiFlight/MobiFlight-WASM-Module) ist **ausschließlich** für Microsoft Flight Simulator 2020/2024 relevant. Es ermöglicht den Zugriff auf L-Variablen und andere Variablentypen, die über SimConnect allein nicht erreichbar sind.

**Für X-Plane gibt es kein WASM-Modul und keines ist nötig** — X-Planes UDP-Interface bietet direkten DataRef-Zugriff ohne Zusatzkomponenten.

### 2.4 Hardware-Kommunikation

MobiFlight kommuniziert mit den Mikrocontrollern über **USB-Serial** (COM-Ports unter Windows). Die eigene **MobiFlight-Firmware** wird auf die Boards geflasht und kommuniziert über ein proprietäres serielles Protokoll mit dem Connector.

**Zusätzlich unterstützt:**

- HID-Geräte (Joysticks, Gamepads) als Input-Quellen
- MIDI-Controller (z.B. Korg nanoKONTROL2)
- Kommerzielle Panels: Winwing FCU/EFIS, VKB-Geräte, Octavi IFR-1, Kav Simulations, CoreFlightTech
- Custom Devices (seit 10.0)

---

## 3. Unterstützte Hardware

### 3.1 Empfohlene Boards

| Board | Mikrocontroller | Bemerkung |
|-------|----------------|-----------|
| Mega 2560 Pro Mini | ATmega2560 | Empfohlen: viele I/O-Pins |
| Arduino Nano | ATmega328P | Kompakt |
| Pro Micro (16 MHz) | ATmega32U4 | HID-fähig |
| Raspberry Pi Pico 1 | RP2040 | 3.3V-Signale (nicht alle Devices kompatibel) |

### 3.2 Unterstützte (nicht empfohlene) Boards

- Arduino Mega 2560 Rev3
- Arduino Uno R3

### 3.3 Nicht unterstützte Boards

- Raspberry Pi Pico 2 (RP2350) — nicht kompatibel
- ESP32-Varianten — nicht unterstützt
- Arduino Nano 33 BLE/IoT/ESP32 — nicht unterstützt
- Arduino Uno R4 — nicht unterstützt

### 3.4 Output-Devices

- LEDs (einzeln und über Shift-Register 74HC595)
- 7-Segment-Anzeigen (MAX7219, TM1637)
- Stepper-Motoren
- Servos
- LCD-Displays
- Custom Devices (herstellerspezifische Displays)

### 3.5 Input-Devices

- Taster/Schalter (mit Debouncing)
- Rotary Encoder
- Potentiometer (Analog-Eingänge)
- Input Shift Register (74HC165, seit Version 9.3)
- Multiplexer

---

## 4. Versionen und Release-Historie

### 4.1 Aktuelle stabile Version

**10.5.3** (Hotfix, 6. April 2025)
- Fix: Crash mit MSFS2024 SU2
- MIDI-Geräte korrekt im Dropdown
- Verschiedene Bugfixes

### 4.2 Aktuelle Beta

**10.5.3.21** (5. Februar 2026)
- Neue Controller-Bindings-Dialog
- Scroll-Buttons für Tabs
- Winwing AGP Chrono Display Support
- Diverse Bugfixes

### 4.3 Wichtige Meilensteine

| Version | Datum | Wichtige Änderung |
|---------|-------|-------------------|
| 10.5.0 | Jan 2025 | MSFS 2024 Support |
| 10.4.0 | Okt 2024 | VKB HID Controller, Winwing EFIS |
| 10.3.0 | Jun 2024 | Winwing FCU Support |
| 10.2.0 | Mär 2024 | String SimVars, WASM 1.0.1 |
| 10.1.0 | Jan 2024 | Neues Firmware 2.5.1, Device-Limits erhöht |
| 10.0.0 | Dez 2023 | MIDI-Support, Custom Devices, Joystick-Definitionen, Generic Custom Device |
| PR #826 | Jun 2022 | **Native X-Plane Support** (DataRefs + Commands direkt, ohne XPUIPC) |

---

## 5. Linux-Kompatibilität

### 5.1 MobiFlight Connector: Kein nativer Linux-Support

MobiFlight Connector ist eine **reine Windows-Anwendung**:

- **Zielplattform:** .NET Framework 4.8 (nicht .NET Core/.NET 5+)
- **UI-Framework:** Windows Forms (WinForms)
- **Hardware-Zugriff:** Windows COM-Port API für Serial, SharpDX.DirectInput für Joysticks, WMI für Device-Monitoring
- **Dependencies:** Windows-spezifische Bibliotheken (Device.Net, Hid.Net, Microsoft.Web.WebView2)

Es gibt keine offiziellen Pläne für einen Linux-Port. Eine Discussion (#508) zur Migration auf .NET 5+ existiert seit 2021, ist aber nicht aktiv verfolgt worden. Selbst eine .NET 5+-Migration würde `net5.0-windows` targetieren (Windows-spezifisch).

### 5.2 Wine/Proton: Ungetestet / Problematisch

**CodeWeavers CrossOver** hat einen Kompatibilitätseintrag für MobiFlight Release 9.6 (veraltet). Es gibt keine bestätigten Berichte über erfolgreichen Betrieb unter Wine/Proton.

**Erwartete Probleme unter Wine/Proton:**

1. **USB-Serial (COM-Ports):** Wine kann COM-Ports auf `/dev/ttyUSBx` oder `/dev/ttyACMx` mappen, aber das erfordert manuelle Konfiguration und ist fehleranfällig
2. **WMI-Abfragen:** MobiFlight nutzt Windows Management Instrumentation für Device-Monitoring — nicht durch Wine unterstützt
3. **DirectInput (SharpDX):** Joystick-Erkennung über DirectInput ist unter Wine eingeschränkt
4. **Firmware-Upload:** avrdude-basierter Firmware-Upload über simulierte COM-Ports ist unzuverlässig
5. **HID-Zugriff:** Device.Net/Hid.Net setzen Windows-HID-Stack voraus
6. **WebView2:** Teile der neuen UI nutzen Microsoft Edge WebView2 — unter Wine nicht verfügbar

**Fazit:** Ein Betrieb von MobiFlight Connector unter Wine/Proton ist **höchst unwahrscheinlich funktional**, insbesondere wegen der tiefen Hardware-Integration über Windows-APIs.

### 5.3 Architektur-Besonderheit: X-Plane UDP ist plattformunabhängig

Die X-Plane-Kommunikation selbst (UDP Port 49000) ist **netzwerkbasiert und plattformunabhängig**. Das eröffnet theoretische Alternativen:

- **Netzwerk-Setup:** MobiFlight auf einem Windows-PC, X-Plane auf Linux — Kommunikation über LAN (die XPlaneConnector-Bibliothek erlaubt konfigurierbare IP-Adresse und Port)
- **Alternative Middleware:** Andere Tools wie SimVimX/RealSimControl oder eigene Lösungen könnten dieselbe UDP-Schnittstelle nutzen
- **Eigene Implementierung:** Die XPlaneConnector-Bibliothek (.NET Standard 2.0) ließe sich theoretisch in einem .NET-Core-Projekt unter Linux nutzen — ohne MobiFlight Connector

### 5.4 Alternatives Setup: MobiFlight auf Windows, X-Plane auf Linux

Da MobiFlight mit X-Plane über UDP kommuniziert, ist ein **Netzwerk-Split** möglich:

- **Linux-PC:** X-Plane 12 (nativ, bester Performance)
- **Windows-PC (oder VM):** MobiFlight Connector + Arduino-Hardware

Konfiguration: In MobiFlight die IP-Adresse des Linux-PCs eintragen (statt 127.0.0.1). X-Plane muss UDP-Verbindungen akzeptieren (Standard: Port 49000).

**Einschränkung:** Erfordert einen zweiten Rechner oder eine Windows-VM mit USB-Passthrough.

---

## 6. HubHop — Community-Preset-Datenbank

**Website:** https://hubhop.mobiflight.com

HubHop ist eine Community-getriebene Datenbank für Variablen und Events. Für X-Plane bietet sie über 7.000 Presets für verschiedene Aircraft (Zibo 737, Toliss A320, etc.).

**Funktion:**

- Presets werden direkt in MobiFlight Connector geladen
- Benutzer können eigene Presets hochladen und teilen
- Automatische Updates über den Connector (Extras > HubHop > Download Latest Presets)

---

## 7. Verwandte Projekte und GitHub-Repositories

| Repository | Beschreibung |
|-----------|-------------|
| [MobiFlight-Connector](https://github.com/MobiFlight/MobiFlight-Connector) | Haupt-Anwendung (C#, MIT) |
| [MobiFlight-WASM-Module](https://github.com/MobiFlight/MobiFlight-WASM-Module) | MSFS-Interface (nur MSFS) |
| [MobiFlight-FirmwareSource](https://github.com/MobiFlight/MobiFlight-FirmwareSource) | Arduino/Pico Firmware |
| [mobiflight-panels](https://github.com/MobiFlight/mobiflight-panels) | Open-Source Panel-Designs |
| [mobiflight-templates](https://github.com/MobiFlight/mobiflight-templates) | Panel-Design-Templates |
| [mobiflight-pcbs](https://github.com/MobiFlight/mobiflight-pcbs) | Breakout-Boards und PCB-Designs |
| [kicad-sim-panel-components](https://github.com/MobiFlight/kicad-sim-panel-components) | KiCad-Bibliothek für Sim-Panels |
| [CommunityTemplate](https://github.com/MobiFlight/CommunityTemplate) | Template für Custom-Firmware |
| [CommunityDevices](https://github.com/MobiFlight/CommunityDevices) | Community-Device-Definitionen |
| [HubHop-Website](https://github.com/MobiFlight/HubHop-Website) | HubHop-Frontend |

---

## 8. Alternativen für Linux-Nutzer

Da MobiFlight nativ nicht unter Linux läuft, sind folgende Alternativen relevant:

### 8.1 SimVimX / RealSimControl

- **Website:** https://simvim.com
- Speziell für X-Plane entwickelt
- Arduino-basiert, eigene Firmware und Konfiguration
- Existiert seit 2015, kostenlos
- **Linux-Kompatibilität:** Nutzt X-Plane-Plugin (läuft nativ im Sim) — kein separates Windows-Tool nötig

### 8.2 X-Plane UDP direkt

- X-Plane bietet eine dokumentierte UDP-Schnittstelle (Port 49000)
- Eigene Scripte in Python, C/C++ oder anderen Sprachen können DataRefs lesen/schreiben
- NASA XPlaneConnect (Python/C): https://github.com/nasa/XPlaneConnect
- XPlaneConnector (C# .NET Standard): https://github.com/MaxFerretti/XPlaneConnector

### 8.3 X-Plane SDK Plugins

- Direkte Plugin-Entwicklung mit dem X-Plane SDK (C/C++)
- Plugin läuft innerhalb von X-Plane, plattformunabhängig (Linux, macOS, Windows)
- Voller Zugriff auf alle DataRefs und Commands
- Beispiel: FlyWithLua für Lua-basierte Steuerung

---

## 9. Bekannte Probleme und Limitierungen (X-Plane)

Basierend auf GitHub Issues:

1. **DataRef-Typen:** Nicht-Integer-DataRefs können Probleme bereiten (#1751, geschlossen März 2024)
2. **Float-Präzision:** Output-getriebener analoger Input kann keine Floats handhaben (#1571, offen)
3. **Config-Wechsel:** Automatisches Laden der Konfiguration beim Wechsel von MSFS zu X-Plane fehlerhaft (#1884, offen)
4. **DataRef-Population:** DataRefs in Konfigurationselementen erfordern Start/Stop zum Auffüllen (#1931, offen)
5. **VPN-Konflikt:** MobiFlight crashed wenn X-Plane verbindet während NordVPN aktiv ist (#2052, offen)
6. **UDP-Port-Konflikt:** Port 49000 wird auch von anderen X-Plane-Tools genutzt — Konflikte möglich

---

## 10. Bewertung für XoL-Dokumentation

### Relevanz

MobiFlight ist das **populärste Open-Source-Tool für Flight-Sim-Cockpit-Bau** und wird von vielen X-Plane-Nutzern eingesetzt. Für die XoL-Zielgruppe (X-Plane auf Linux) ist es relevant als:

1. **Thema mit Linux-Einschränkung:** MobiFlight Connector läuft nicht nativ unter Linux
2. **Netzwerk-Workaround:** Split-Setup (X-Plane auf Linux, MobiFlight auf Windows) ist praktikabel
3. **Alternativen-Übersicht:** SimVimX und direkte UDP-Anbindung als Linux-native Optionen

### Empfehlung für Dokumentation

Ein Abschnitt in der Addon-Dokumentation könnte sinnvoll sein:
- Kurze Erklärung was MobiFlight ist
- Klare Aussage: Connector läuft nicht unter Linux
- Netzwerk-Split als Workaround
- Verweis auf Linux-native Alternativen (SimVimX, direkte UDP-Programmierung)

### Haltbarkeit

- Die Windows-Abhängigkeit wird sich mittelfristig nicht ändern (.NET Framework 4.8, WinForms)
- Die X-Plane-UDP-Architektur ist stabil (seit X-Plane 9)
- HubHop-Presets werden aktiv gepflegt

---

## Quellen

1. MobiFlight GitHub Repository — https://github.com/MobiFlight/MobiFlight-Connector (abgerufen 2026-02-15)
2. MobiFlight Offizielle Website — https://www.mobiflight.com (abgerufen 2026-02-15)
3. MobiFlight Documentation — https://docs.mobiflight.com (abgerufen 2026-02-15)
4. MobiFlight X-Plane Quick Start Guide — https://www.mobiflight.com/en/tutorials/x-plane-quick-start-guide.html (abgerufen 2026-02-15)
5. XPlaneConnector (MaxFerretti) — https://github.com/MaxFerretti/XPlaneConnector (abgerufen 2026-02-15)
6. HubHop Preset Database — https://hubhop.mobiflight.com (abgerufen 2026-02-15)
7. MobiFlight WASM Module — https://github.com/MobiFlight/MobiFlight-WASM-Module (abgerufen 2026-02-15)
8. Native X-Plane Support PR #826 — https://github.com/MobiFlight/MobiFlight-Connector/pull/826 (gemerged 2022-06-03)
9. .NET 5 Migration Discussion #508 — https://github.com/MobiFlight/MobiFlight-Connector/discussions/508 (seit 2021, inaktiv)
10. CodeWeavers CrossOver MobiFlight Entry — https://www.codeweavers.com/compatibility/crossover/mobiflight-release-96 (nur v9.6 getestet)
