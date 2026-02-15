# SayIntentions.AI -- Research Paper

**Datum:** 2026-02-15
**Kategorie:** Addons
**Relevanz fuer XoL:** Hoch (ATC-Addon fuer X-Plane 12, aber Linux-Unterstuetzung fehlt)

---

## 1. Was ist SayIntentions.AI?

SayIntentions.AI ist ein KI-basiertes Air Traffic Control (ATC) System fuer Flugsimulatoren. Entwickelt von **SayAgain Solutions, LLC**, gegruendet von Brian (CEO), einem AI/ML-Ingenieur mit ueber 25 Jahren IT- und Flugsimulationserfahrung.

**Korrekte Schreibweise:** "SayIntentions.AI" (mit Punkt und Grossbuchstaben). Nicht "SayIntensions" (haeufiger Tippfehler).

**Kernkonzept:** Vollstaendig KI-basierte ATC-Simulation -- keine vorgefertigten Skripte, sondern dynamische, ungeskripted AI-Kommunikation. Der Pilot spricht per Mikrofon mit dem ATC, das System nutzt Spracherkennung und grosse Sprachmodelle (LLMs/GPT-Technologie) fuer natuerliche Antworten.

**Offizielle Website:** https://www.sayintentions.ai/
**Support-Portal:** https://sayintentionsai.freshdesk.com/
**Pilot Portal:** https://portal.sayintentions.ai/

### Unterstuetzte Simulatoren

- Microsoft Flight Simulator 2020
- Microsoft Flight Simulator 2024
- X-Plane 11
- X-Plane 12
- Prepar3D v5/v6
- Weitere Simulatoren ueber SimAPI moeglich (z.B. DCS via Community-Adapter)

---

## 2. Funktionsweise und Architektur

### Client-Server-Architektur

SayIntentions.AI arbeitet als Cloud-basierter Dienst:

1. **SayIntentions Client** (Windows-Anwendung): Laeuft lokal, kommuniziert mit dem Simulator und dem Cloud-Backend
2. **Simulator-Integration:** Liest Telemetriedaten (Hoehe, Kurs, Geschwindigkeit, Transponder, Funkfrequenzen) ueber DataRefs (X-Plane) bzw. SimVars/LVars (MSFS)
3. **Cloud-AI-Backend:** Verarbeitet Spracheingaben, generiert ATC-Anweisungen, spricht ueber synthetische Stimmen

### X-Plane-spezifische Integration

- **DataRef-basiert:** Nutzt X-Plane DataRefs fuer Telemetrie und Radio-Stack (z.B. `siai/radio_ptt`)
- **UDP-Port 49000:** Kommunikation zwischen Client und X-Plane (gleicher Port wie ZHSI, MobiFlight, Sismo OrbitXP -- kann Konflikte verursachen)
- **X-Plane-Support seit Mai 2024:** Offiziell angekuendigt am 16. Mai 2024
- **Taxi-Arrows-Plugin:** Wird vom SI-Client automatisch in X-Plane installiert (nach erstmaligem Start)
- **Startreihenfolge:** SI-Client erst starten, NACHDEM man im Cockpit sitzt

### SimAPI (offene Integrationsschnittstelle)

- RESTful API fuer programmatischen Zugriff
- JSON-dateibasierte Kommunikation:
    - Input: `%localappdata%\SayIntentionsAI\simAPI_input.json` (Telemetrie vom Sim)
    - Output: `%localappdata%\SayIntentionsAI\simAPI_output.jsonl` (Variablenaenderungen an den Sim)
- Adapter in beliebiger Sprache schreibbar (C++, C#, Python)
- Ermoeglicht Integration mit beliebigen Simulatoren
- Flight.JSON und SimAPI-Zugang dauerhaft kostenlos

---

## 3. Feature-Uebersicht

### Premium (Abo-Modell, alle Features)

- **AI ATC:** 24/7 weltweite Abdeckung, ~88.000 Flughaefen, vollstaendige IFR/VFR-Unterstuetzung
- **Spracherkennung:** Pilot spricht natuerlich per Mikrofon
- **650+ KI-Stimmen:** Regional unterschiedliche Akzente (in Zusammenarbeit mit ElevenLabs), 15 Sprachen
- **ACARS/CPDLC:** Einziges nicht-menschliches ATC-Netzwerk weltweit mit voller CPDLC-Unterstuetzung
- **AI Co-Pilot:** Uebernimmt Funkkommunikation, Checklisten, kann Steuerung automatisieren; verschiedene Persoenlichkeiten waehlbar
- **Traffic Injection:** Kommerzieller und GA-Verkehr aus realen Flugplaenen, KI-gesteuerte Sequenzierung
- **SkyOps Missions:** Dynamische, KI-generierte Szenarien (Wetter, Standort, Flugzeug-abhaengig)
- **Dynamic SID/STAR Shortcuts:** KI beruecksichtigt Laermschutz, Terrain, Verkehrsaufkommen
- **Taxi-Arrows:** Visuelle Rollhilfe im Simulator
- **SkyNet Multiplayer:** Multiplayer-Netzwerk fuer gemeinsames ATC

### Entourage (Einmalkauf, KEIN ATC)

- AI Cabin Crews (6 Crews, verschiedene Persoenlichkeiten)
- AI Tour Guides (3 Guides, dynamischer Kommentar zu Sehenswuerdigkeiten)
- Flight Mentor (1 Trainer)
- Virtual-Airline Dispatchers (4 Dispatcher)
- Ground Crews und Managed Pushback
- Progressive Taxi Guidance
- **Hinweis:** Entourage ist nur US-Englisch, nur Windows

---

## 4. Preismodell (Stand: Februar 2026)

### Preishistorie

| Zeitraum | Monatlich | Jaehrlich (pro Monat) |
|----------|-----------|----------------------|
| Bis Oktober 2025 | $19.95/Monat | ~$16.25/Monat |
| November 2025 (Erhoehung) | $23.95/Monat | $239.95/Jahr |
| Ab November 2025 (Senkung) | **$18.95/Monat** | ~$16.25/Monat |

Die Preiserhoehung im November 2025 wurde nach wenigen Tagen zurueckgenommen, nachdem SayIntentions guenstigere Konditionen bei Infrastruktur- und AI-Providern aushandeln konnte. Kunden, die den hoeheren Preis zahlten, erhielten automatische Gutschriften.

### Aktuelle Preise

- **Premium monatlich:** $18.95/Monat
- **Premium jaehrlich:** ~$16.25/Monat ($195/Jahr)
- **Entourage (Einmalkauf, ohne ATC):** $49.95
- **Kostenlose Testphase:** 24 Stunden voller Zugang, keine Kreditkarte erforderlich

### Vertriebskanaele

- Direkt ueber sayintentions.ai
- Aerosoft Shop
- simMarket (nur Entourage)
- Contrail Shop

---

## 5. Linux-Unterstuetzung

### Offizieller Status: NICHT UNTERSTUETZT

SayIntentions.AI ist **ausschliesslich Windows-kompatibel** (Windows 10/11). Mac und Linux werden offiziell nicht unterstuetzt. Dies betrifft:

- Den SayIntentions Client (Windows-Desktop-Anwendung)
- Alle AI-Voice-Features (Windows-only)
- Entourage (Windows-only, US English only)

### Warum Linux problematisch ist

Das Grundproblem: SayIntentions besteht aus zwei Komponenten:

1. **X-Plane Plugin** (DataRef-Kommunikation) -- laeuft innerhalb von X-Plane, theoretisch plattformunabhaengig
2. **SayIntentions Client** (Windows-GUI-Anwendung) -- muss separat laufen, verbindet sich mit Cloud-Backend

Fuer Linux-Nutzer mit nativem X-Plane 12 muesste der Windows-Client parallel via Wine/Proton laufen. Die Kommunikation erfolgt ueber UDP (Port 49000) und lokale JSON-Dateien (%localappdata%), was unter Wine theoretisch funktionieren koennte, aber:

- Keine offiziellen Tests oder Dokumentation
- Spracherkennung (Mikrofon-Zugriff) unter Wine ist problematisch
- Netzwerk-Kommunikation zwischen Wine-Client und nativem X-Plane erfordert Konfiguration
- Kein Support bei Problemen

### Mac-Workaround (Analogie fuer Linux)

Es existiert ein Community-Projekt: [SayIntentionsForMac](https://github.com/paulfisher53/SayIntentionsForMac)

- **Ansatz:** Windows-11-VM (nicht Wine!) mit UDP-Port-Forwarding (sudppipe.exe) und Dummy-X-Plane.exe
- **Funktionsweise:** Die VM laeuft den SI-Client, die UDP-Kommunikation wird zur nativen X-Plane-Instanz auf dem Host weitergeleitet
- **Theoretisch auf Linux uebertragbar:** QEMU/KVM statt UTM, gleicher Port-Forwarding-Ansatz
- **Einschraenkungen:** Mikrofon-Passthrough in VM noetig, zusaetzlicher Ressourcenverbrauch

### Bewertung fuer XoL-Dokumentation

SayIntentions.AI ist fuer Linux-Nutzer derzeit **nicht praxistauglich** ohne erheblichen Workaround-Aufwand:

- Entweder Windows-VM mit Port-Forwarding (nach Mac-Vorbild)
- Oder Wine/Proton fuer den Client (ungetestet, nicht dokumentiert)
- Beides ohne offiziellen Support
- Kein Indiz, dass Linux-Support geplant ist

---

## 6. Versionen und Release-Status

### Versionsschema

SayIntentions.AI verwendet ein Rolling-Release-Modell mit haeufigen Updates. Konkrete Versionsnummern werden im Client angezeigt (z.B. 2.7.5.2), aber nicht prominent auf der Website kommuniziert. "SayIntentions 2.0" wird als Markenname fuer den aktuellen Hauptzweig verwendet.

### Wichtige Meilensteine

| Datum | Meilenstein |
|-------|------------|
| 2023 | Erstveroeffentlichung (nur MSFS) |
| Mai 2024 | X-Plane 11/12 Support |
| Oktober 2024 | Entourage Release (Einmalkauf-Option) |
| 2025 Q1 | SimAPI fuer beliebige Sim-Integration |
| 2025 Q2 | ACARS/CPDLC Release |
| 2025 Q3 | SkyOps Missions, 15 Sprachen |
| November 2025 | Preisanpassung, SkyNet Multiplayer |
| Laufend | AI Traffic System ("Living World"), EU-Voice-Packs |

### Roadmap (angekuendigt)

- AI Living World Traffic fuer X-Plane 11/12 (noch nicht vollstaendig implementiert)
- Weitere regionale Stimmenpakete (Schweiz, Niederlande)
- Checklists v2 (dynamisch, kontextbezogen)

---

## 7. GitHub-Praesenz

SayIntentions.AI selbst ist **nicht Open Source**. Es gibt keine offiziellen GitHub-Repositories.

### Community-Projekte auf GitHub

- **[paulfisher53/SayIntentionsForMac](https://github.com/paulfisher53/SayIntentionsForMac):** Mac-Workaround mit Windows-VM und UDP-Port-Forwarding
- **[papiplanes/sayintentions-dcs-adapter](https://github.com/papiplanes/sayintentions-dcs-adapter):** Community-Adapter fuer DCS World via SimAPI

### Offene APIs

- **SimAPI:** JSON-basierte Integrationsschnittstelle (kostenlos, dokumentiert)
- **SAPI (SayIntentions API):** RESTful API fuer programmatischen Zugriff auf Sprach-Kommunikation, Wetterdaten, Flugoperationen
- **Flight.JSON:** Kostenloser, dauerhafter Zugang

---

## 8. Bekannte Probleme und Einschraenkungen (X-Plane)

### Allgemeine Probleme

- **Fenster-Fokus:** Mausinteraktion im Cockpit kann den SI-Client aus dem Fokus werfen; manuelle Wiederherstellung noetig
- **Authentifizierung:** "Invalid username or password" Fehler im SI-Fenster gemeldet
- **Mikrofon:** Nach erstmaliger Nutzung funktioniert das Mikrofon manchmal nicht mehr (Neustart erforderlich)
- **Port-Konflikte:** UDP-Port 49000 wird auch von ZHSI, MobiFlight und Sismo OrbitXP genutzt -- Empfehlung: SI-Client erst nach X-Plane und anderen Tools starten
- **ATC-Logik:** Gelegentliche Quirks, Abstuerze und Audio-Glitches (werden laufend gepatcht)

### X-Plane-spezifische Einschraenkungen

- **Traffic Injection:** AI Living World Traffic fuer X-Plane noch nicht vollstaendig implementiert (MSFS-Prioritaet)
- **Startreihenfolge:** Client muss nach dem Einsteigen ins Cockpit gestartet werden
- **Taxi-Arrows-Plugin:** Muss einmalig durch SI-Client-Start (vor X-Plane-Oeffnung) installiert werden
- **Feature-Paritaet:** Einige Features (Ground Services, Jetways) sind primaer fuer MSFS entwickelt

---

## 9. Vergleich mit Alternativen

### X-Plane ATC-Optionen

| Kriterium | X-Plane Built-in ATC | SayIntentions.AI | Pilot2ATC | 124th ATC | BeyondATC |
|-----------|---------------------|------------------|-----------|-----------|-----------|
| **Typ** | Integriert | Cloud-AI | Standalone | X-Plane Plugin | Standalone |
| **Kommunikation** | Menue-basiert | Sprache (natuerlich) | Sprache | Menue/Sprache | Sprache |
| **AI-Technologie** | Skriptbasiert | GPT/LLM | Spracherkennung | Regelbasiert | KI-basiert |
| **IFR** | Ja (einfach) | Ja | Ja (Fokus) | Ja | Ja (Fokus) |
| **VFR** | Begrenzt | Ja (Fokus) | Begrenzt | Ja | Nein |
| **X-Plane 12** | Ja | Ja | Ja (via XPUIPC) | Ja | **Nein** |
| **Linux** | Ja (nativ) | **Nein** | Via Wine (?) | Ja (nativ) | **Nein** |
| **Preismodell** | Kostenlos | Abo ($18.95/m) | Einmalkauf ($39.95) | Kostenlos | Einmalkauf (~$40) |
| **Verkehr** | Einfach | Traffic Injection | Kein AI-Traffic | Kein AI-Traffic | Traffic |
| **CPDLC** | Nein | Ja | Nein | Nein | Nein |

### Bewertung

- **SayIntentions.AI** bietet die fortschrittlichste AI-ATC-Erfahrung, aber das Abo-Modell und die fehlende Linux-Unterstuetzung sind erhebliche Nachteile fuer die XoL-Zielgruppe
- **Pilot2ATC** ist die traditionelle Alternative (Einmalkauf), benoetigt aber XPUIPC und hat keine AI-basierte Konversation
- **124th ATC** ist kostenlos und Linux-nativ, aber veraltet und mit bekannten Routing-Problemen
- **BeyondATC** unterstuetzt kein X-Plane und kein Linux
- **Built-in ATC** bleibt die einzige garantiert funktionierende Option fuer Linux-X-Plane-Nutzer

---

## 10. Fazit und Empfehlung fuer XoL

### Relevanz

SayIntentions.AI ist das fortschrittlichste ATC-Addon fuer X-Plane 12. Die AI-basierte Sprachkommunikation, CPDLC-Integration und Traffic Injection setzen Massstaebe im Bereich der Flugsimulation.

### Linux-Blocker

Fuer die XoL-Dokumentation (Linux-Fokus) ist SayIntentions derzeit **nicht empfehlenswert**:

- Kein Linux-Support, kein Indiz fuer geplanten Support
- Workarounds (Windows-VM, Wine) sind aufwaendig und fragil
- Abo-Kosten kommen zum Workaround-Aufwand hinzu
- Kein offizieller Support bei Linux-Problemen

### Dokumentations-Empfehlung

- **Erwaehnung in der Addon-Uebersicht:** Ja, als wichtiges ATC-Addon mit Hinweis auf fehlenden Linux-Support
- **Eigene Seite:** Nein, nicht sinnvoll ohne funktionierende Linux-Loesung
- **Alternative dokumentieren:** Built-in ATC und evtl. 124th ATC als Linux-kompatible Optionen
- **Beobachten:** SimAPI koennte theoretisch einen Linux-nativen Adapter ermoeglichen (Community-Projekt), aber derzeit existiert keiner

---

## Quellen

1. SayIntentions.AI -- Offizielle Website: https://www.sayintentions.ai/ (abgerufen 2026-02-15)
2. SayIntentions.AI -- Pricing: https://www.sayintentions.ai/pricing (abgerufen 2026-02-15)
3. SayIntentions.AI -- Premium: https://www.sayintentions.ai/premium (abgerufen 2026-02-15)
4. SayIntentions.AI -- FAQ: https://www.sayintentions.ai/faq (abgerufen 2026-02-15)
5. SayIntentions.AI -- SimAPI Developer HowTo: https://sayintentionsai.freshdesk.com/support/solutions/articles/154000221017 (abgerufen 2026-02-15)
6. SayIntentions.AI -- Features Overview: https://sayintentionsai.freshdesk.com/support/solutions/articles/154000219433 (abgerufen 2026-02-15)
7. SayIntentions.AI -- Client User Guide: https://sayintentionsai.freshdesk.com/support/solutions/articles/154000218811 (abgerufen 2026-02-15)
8. FSNews -- X-Plane 12.1.0 / SayIntentions Integration: https://fsnews.eu/x-plane-12-update-12-1-0/ (abgerufen 2026-02-15)
9. FSElite -- SayIntentions.AI Reducing Pricing: https://fselite.net/content/sayintentions-ai-reducing-pricing-following-price-increase/ (abgerufen 2026-02-15)
10. GitHub -- SayIntentionsForMac: https://github.com/paulfisher53/SayIntentionsForMac (abgerufen 2026-02-15)
11. GitHub -- DCS Adapter: https://github.com/papiplanes/sayintentions-dcs-adapter (abgerufen 2026-02-15)
12. forums.x-plane.org -- SayIntentions Diskussionen: https://forums.x-plane.org/forums/topic/317846-xplane12-sayintentions-atc/ (abgerufen 2026-02-15)
13. SimBlitz -- Beyond ATC vs SayIntentions.ai: https://simblitz.com/beyond-atc-vs-sayintentions-ai/ (abgerufen 2026-02-15)
