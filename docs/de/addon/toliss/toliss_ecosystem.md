---
description: "Community-FlyWithLua-Skripte und Plugins für die ToLiss-Airbus-Flotte in X-Plane 12: Callouts, Cockpit-Automatisierung, Boarding und Bodendienste."
---
# ToLiss FlyWithLua-Ökosystem

<div class="video-container" markdown>
<video controls width="100%" preload="metadata" aria-label="Video: Vom Briefing zum Gate" poster="../../../assets/video/de/Vom_Briefing_zum_Gate/Vom_Briefing_zum_Gate.jpg">
  <source src="../../../assets/video/de/Vom_Briefing_zum_Gate/Vom_Briefing_zum_Gate.mp4" type="video/mp4">
</video>
</div>

Rund um die ToLiss-Flotte (A319, A320 CEO/NEO, A321 CEO/NEO, A330neo, A340-600) hat die Community ein umfangreiches Ökosystem aus [FlyWithLua](../scripting/flywithlua.md)-Skripten aufgebaut. Diese Skripte erweitern die Flugzeuge um Callouts, Cockpit-Automatisierung, Boarding-Simulation und weitere Funktionen. Zusätzlich gibt es eigenständige Plugins, die mit der ToLiss-Flotte zusammenarbeiten.

Die meisten Skripte setzen die X-Airbus Library als Grundlage voraus. Zuerst diese Library installieren, dann die Skripte auswählen, die zum eigenen Workflow passen — von Callouts und Cockpit-Initialisierung bis hin zur vollständigen First-Officer-Assistenz.

## X-Airbus Library

Die X-Airbus Library ist eine Lua-Bibliothek, die als Fundament für viele ToLiss-Skripte dient. Sie stellt gemeinsame Funktionen und Dataref-Zugriffe bereit, die von abhängigen Skripten genutzt werden.

- **Entwickler:** FrankLFRS
- **Typ:** FlyWithLua-Modul
- **Download:** [forums.x-plane.org](https://forums.x-plane.org/files/file/92739-x-airbus-library/)
- **Kompatibel mit:** A319, A320 CEO/NEO, A321 CEO/NEO, A330neo, A340-600

!!! warning "Installation"

    Die X-Airbus Library gehört in den Ordner `Modules/` von FlyWithLua — nicht in `Scripts/`. Skripte, die X-Airbus voraussetzen, funktionieren ohne die Library nicht.

## simbrief_hub

Ein zentraler Datenprovider, der den aktuellen SimBrief OFP (Operational Flight Plan) abruft und anderen Plugins über Datarefs bereitstellt. Fungiert als Grundlage — Plugins wie [AutoDGS](../traffic/autodgs.md) und [openSAM](../traffic/opensam.md) lesen Flugplandaten aus simbrief_hub, statt SimBrief einzeln abzufragen.

- **Entwickler:** hotbso
- **Repository:** [github.com/hotbso/simbrief_hub](https://github.com/hotbso/simbrief_hub) (Open Source, LGPL-2.1)
- **Plattformen:** Windows, macOS, Linux (native Binaries)
- **Download:** [GitHub Releases](https://github.com/hotbso/simbrief_hub/releases)

**Funktionsumfang:**

- OFP-Auto-Fetch beim Start, gespeichert als Byte-Arrays in Datarefs
- Status-Datarefs: `sbh/seqno` (Sequenznummer für OFP-Updates) und `sbh/stale` (Indikator für fehlgeschlagenen Download)
- VATSIM-CDM-Unterstützung: ruft Collaborative Departure Management-Daten (TOBT, TSAT, CTOT) für kompatible VDGS-Plugins ab
- Fake-CDM-Modus für Offline-Flüge — wird bei VATSIM-Verbindung automatisch durch echte Daten ersetzt

**Installation:** Nach `Resources/plugins/` entpacken. Die Linux-Binary liegt unter `lin_x64/simbrief_hub.xpl`. Das Plugin enthält `cdm_cfg.default.json` für regionale CDM-Server — zum Anpassen als `cdm_cfg.json` kopieren.

## Callouts & Sound

### ToLiss V-Speeds

V-Speed-Callouts für Start und Landung: Spoilers, Reverse Green, Brake Low/Medium, Decel, 70 Knots sowie Gear Down, Flaps, Speed Checked und Go-Around Flaps. PF/PM-Stimmen und Lautstärken sind pro Flugzeugtyp konfigurierbar.

- **Benötigt:** X-Airbus Library
- **Download:** [forums.x-plane.org](https://forums.x-plane.org/files/file/92767-toliss-v-speeds/)

### PMCO — Pilot Monitoring Callouts

FlyWithLua-Skript von hotbso, das Standard-Callouts des Pilot Monitoring spricht und auf Piloteneingaben reagiert (z.B. "Gear up"). Unterstützt normale Verfahren und Touch-and-Go-Training. Mehrere Soundsets verfügbar (männlich/weiblich, Airbus-konform).

- **Benötigt:** FlyWithLua, nur ToLiss-Flotte
- **Download:** [forums.x-plane.org](https://forums.x-plane.org/files/file/90074-pmco-pilot-monitoring-callouts-for-the-toliss-fleet/)

### ToLiss Announcements

Spielt Flugbegleiter- und Kapitänsdurchsagen ab und verwaltet das ECAM Cabin Ready. Nur [X-Plane](../../glossary.md#x-plane) 12.

- **Benötigt:** X-Airbus Library
- **Download:** [forums.x-plane.org](https://forums.x-plane.org/files/file/95101-toliss-announcements/)

!!! info "Linux: Airline-spezifische Sound-Packs"

    ToLiss Announcements enthält einen .exe-Switcher für airline-spezifische Sound-Packs. Unter Linux funktioniert dieses Tool nicht — die gewünschten Sound-Dateien manuell in den Sound-Ordner des Skripts kopieren.

### DK Toliss Callout — FMA-Ansagen

FlyWithLua-Skript, das Autopilot-Modusänderungen (CLB, OP CLB, SPEED, NAV, G/S) per Text-to-Speech ansagt. Liest die blauen FMA-Werte aus dem oberen PFD-Feld. Unter Linux ist [XLinSpeak](../tools/xlinspeak.md) für hörbare Ausgabe erforderlich. [→ Detailseite](dk_toliss_callout.md)

- **Entwickler:** DINKIssTyle
- **Benötigt:** FlyWithLua
- **Download:** [forums.x-plane.org](https://forums.x-plane.org/files/file/91367-toliss-airbus-fma-callout-flywithlua-script/)

### Cockpit Rain Noise

Fügt Regengeräusche zum Cockpit hinzu. Die Lautstärke skaliert mit der Niederschlagsmenge und nimmt bei zunehmender Geschwindigkeit ab. Lautstärke in dB konfigurierbar, einzelne Flugzeugtypen lassen sich ausschließen.

- **Benötigt:** X-Airbus Library
- **Download:** [forums.x-plane.org](https://forums.x-plane.org/files/file/94901-toliss-cockpit-rain-noise/)

## Cockpit-Automatisierung

### TOI Cabin Ready

Sendet automatisch den Cabin-Ready-Call: Bei Abflug nach 4–8 Minuten (basierend auf Passagierzahl), im Anflug wenige Sekunden nach Klappen- und Fahrwerksausfahren. Verarbeitet Sonderfälle wie Durchstarten sicher. [→ Detailseite](toicabrdy.md)

- **Entwickler:** cxn0026
- **Benötigt:** FlyWithLua
- **Download:** [forums.x-plane.org](https://forums.x-plane.org/files/file/91876-toliss-airbus-cabin-ready-automatic-flywithlua-script/)

### ToLiss Init

Initialisiert das Cockpit nach individuellen Vorlieben: ND-Mode, ND-Range, MKR Beeps, External-Power-Status, CSTR-Licht und weitere Einstellungen. Das Skript wartet, bis BAT 1 + BAT 2 eingeschaltet sind, und wendet die Konfiguration nach etwa 15 Sekunden an.

- **Benötigt:** X-Airbus Library
- **Download:** [forums.x-plane.org](https://forums.x-plane.org/files/file/95194-toliss-init/)

### Speedy Copilot

Umfangreicher FO/PM-Assistent, der die Aufgaben des First Officers und Pilot Monitoring von der Cockpit Preparation über Engine Start bis zur Landung übernimmt. Enthält ein PDF-Handbuch und verschiedene Sprachpakete (US, British, French, Australian, Egyptian). Funktioniert mit X-Plane 11 und 12.

- **Kompatibel mit:** A319, A320 CEO/NEO, A321 CEO/NEO, A330neo, A340-600
- **Download:** [forums.x-plane.org](https://forums.x-plane.org/files/file/54069-speedy-copilot-for-toliss/)

### Windshield & Window Icing Mod

Lua-basiertes Mod, das Vereisung der Cockpit- und Kabinenfenster simuliert. Berücksichtigt Relative Humidity, OAT und Spread. Eis verschwindet nur bei aktivierter Window Heat / Pitot Heat und schmilzt realistisch animiert. Visuelle Effekte nur für A320, der Lua-Code funktioniert auch mit A346 und A339.

- **Benötigt:** FlyWithLua
- **Download:** [forums.x-plane.org](https://forums.x-plane.org/files/file/98503-toliss-a320-windows-icing-cabin-rain/)

## Boarding & Ground

### TOBUS — Boarding/Deboarding

Simuliert einen realistischen Boarding- und Deboarding-Prozess mit Live-Anpassung der Payload. Passagierzahl manuell wählbar oder per SimBrief importierbar. Drei Geschwindigkeitsmodi: Real, Fast, Instant. Vorder- und Hintertür oder nur Vordertür. Eine verbesserte Version von hotbso ([GitHub](https://github.com/hotbso/TOBUS/releases)) bietet zusätzliche Tür-Optionen und A346-Unterstützung.

- **Benötigt:** FlyWithLua, X-Airbus Library (im Modules-Ordner)
- **Download:** [forums.x-plane.org](https://forums.x-plane.org/files/file/87996-tobus-your-toliss-boarding-lua-script/)

### ToLiss Ground Services

Automatisches Setzen und Entfernen von Chocks und External Power. Beim Abflug: APU verfügbar + PAX/Cargo-Türen geschlossen — Chocks entfernt, External Power getrennt. Bei Ankunft: Parkbremse + N1 < 10% — Chocks gesetzt, External Power angeschlossen.

- **Benötigt:** X-Airbus Library
- **Download:** [forums.x-plane.org](https://forums.x-plane.org/files/file/94691-toliss-ground-services/)

## Verwandte Plugins

Die folgenden eigenständigen Plugins arbeiten mit der ToLiss-Flotte zusammen, sind aber als separate Seiten dokumentiert:

- **[XGS](../tools/xgs.md)** — Landing-Speed-Analyse mit ToLiss-spezifischer Fahrwerksstreben-Erkennung
- **[Follow the Greens](../traffic/followthegreens.md)** — A-SMGCS Taxiway-Leitsystem
- **[openSAM](../traffic/opensam.md)** — Jetways, VDGS, Marshaller für Custom-Szenerien
- **[AutoDGS](../traffic/autodgs.md)** — Docking Guidance für Default-Flughäfen
- **[AviTab](../cockpit/avitab.md)** — Cockpit-Tablet mit PDF-Viewer und Moving Map
- **[KOSP Project](../sounds/kosp_project.md)** — FMOD-Soundscape für A319, A320, A321 (alle Triebwerksvarianten)
- **[Mango Studios](../sounds/mango_studios.md)** — FMOD-Sound-Packs für die gesamte ToLiss-Flotte

