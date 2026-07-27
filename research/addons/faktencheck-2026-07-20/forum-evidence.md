# Forum-Belege (via Chrome, 2026-07-20)

Volltext der x-plane.org-Seiten, die per WebFetch mit 403 blockiert sind.
Quelle: echter Browser-Zugriff. Diese Datei ist die Belegbasis fuer die Forum-only-Plugin-Seiten.

---

## cockpit/kabinxp.md — KabinXP
URL: https://forums.x-plane.org/files/file/98298-kabinxp/
Stand: "What's New in Version 06/18/2026", released June 18 2026. Edited June 15 by EffectiveAir1434.

PA-Engine fuer X-Plane. Cabin announcements, vollstaendig anpassbar. Kommt bewusst mit LEERER
Announcement-Library — eigene Audiodateien (.wav, .mp3, .flac) hinzufuegen. Pro Livery eigener
Announcement-Pack: Ordner in den Livery-Ordner legen, wird automatisch geladen, kein Neustart.
Funktioniert mit jedem Aircraft mit Livery-Ordner.
NEU: "True 3D Spatial Audio: Sounds are physically attached into the aircraft cabin. so no more flat 2d audio."
Changelog 06/18/2026: major bug fixes, updated UI, announced KabinXP Enhanced.
Support: Discord https://discord.gg/aBGfwVMUJS

---

## cockpit/anyairline.md — AnyAirline
URL: https://forums.x-plane.org/files/file/100112-anyairline-ai-cabin-crew-passenger-ife-airline-immersion/
Stand: "What's New in Version 07/13/2026", released July 13 2026. Version 1.5.0.
Autor: Filip / Chudoba Design.

Passenger-Cabin-Immersion-App fuer X-Plane 12. Status: OPEN BETA.
Features: cabin/gate announcements; captain-, gate-, cabin-crew-Stimmrollen; SimBrief-OFP-Import oder
manuelles Setup; mehrere Kabinensprachen; lokales/offline englisches TTS im FREE TIER; Cloud-AI-Stimmen
ueber BEZAHLTE AI-Credits; Workshop-Assets; Live-Passenger-IFE-Map mit Route/Position/ETA;
Desktop-Connector-Workflow.
WICHTIG: "A free AnyAirline account is required because the app uses an online workspace for account
sync, workshop access, credits and cloud features." Free tier = lokales englisches TTS + Workshop.
Paid credits = Cloud-AI-Stimmen, mehrsprachig, custom announcements.
Changelog 1.5.0: new audio distribution; reworked webdeck (Dispatch von Mobile/Tablet);
save preferred airport/airline fuer random flights; new pilgrimage features.
Discord: https://discord.gg/hX7uvXVr5Z

---

## cockpit/terrainradar.md — Terrain Radar + Vertical Situation Display
URL: https://forums.x-plane.org/files/file/37864-terrain-radar-vertical-situation-display/
Stand: "Edited April 26, 2023 by DrGluck", Version 1.31. SEIT 2023 UNVERAENDERT — Stagnationssignal.

EGPWS-Terrain-Display mit Peaks-Mode. Zwei Modi: Integration ins Navigation Display (Liste
unterstuetzter Aircraft) und Overlay-Fenster (alle anderen).
X-Plane: 10 32/64-bit, 11 64-bit, 12 64-bit.
OS: "Windows, Linux and MacOS (included Apple Silicon)" — Linux explizit unterstuetzt.
Installation: Ordner "TerrainRadar" nach "X-Plane/resources/plugins".
Overlay: "Show radar window" im "Terrain radar" Plugin-Menue.
Commands: terrain_radar/radar_show, terrain_radar/radar_range_increase,
terrain_radar/radar_range_decrease, terrain_radar/enable_egpws.
Integration u.a.: Zibo 737-800 (XP11+XP12), 737 LevelUp, default 737-800 (XP11+XP12, XP12 mit
unabhaengigen Terrain-Displays links/rechts), default 747-400, FlightFactor 777, X-Crafts E175/E195
und ERJ, Magknight 787, Rotate MD-80, iniSimulations A300/A310, X-Bureau A318, AKD GLF550 u.v.m.

---

## cockpit/xpwalkaround.md — SimpleWalkaround
URL: https://forums.x-plane.org/files/file/96508-simplewalkaround/
Stand: "What's New in Version 08/30/2025", released August 30 2025, v1.5. Edited by scarythrash.

"A simple plugin that enables a pre-flight walkaround of your aircraft — similar to the walk mode in
MSFS2024. No extra settings, no customization." Works in xp11 and xp12.
Controls: Movement WASD, Sprint C, Crouch X, Exit Esc.
Installation: Plugin nach X-Plane 12/Resources/plugins.
Usage: Hotkey fuer "Walkaround / Turn on Walkaround" in den X-Plane Keyboard-Settings zuweisen.
LIMITATION (woertlich): "Tested in X-Plane 12 on Windows; functionality in other versions is not
guaranteed."  <-- LINUX-RELEVANT: Linux-Funktion ist vom Autor NICHT zugesichert.
Changelog v1.5: komplett neu geschrieben OHNE SASL3; Interaktion mit externen Elementen (Tueren, Pins);
Aircraft mit custom external rendering werden im Walkaround korrekt dargestellt.
Vor Update alte Version vollstaendig entfernen.

---

## flylua_scripts/3drainspeedstop.md — 3d rain stop
URL: https://forums.x-plane.org/files/file/88602-3d-rain-stop-lua-script-xp12/
Stand: v1.0.0, released November 3 2023. Edited November 3, 2023 by domvc10. SEIT 2023 UNVERAENDERT.

ZWEI Skripte:
1. 3drainspeedstop.lua — stoppt 3D-Rain ab 100 kt, startet wieder bei 99 und darunter.
2. 3drainheightstop.lua — stoppt Rain ab 7000 ft, startet wieder darunter.
"These do not stop the rain on the aircraft windows only the falling 3d rain."
Voraussetzung: FlyWithLua.
Installation: 3drainspeedstop.lua ODER 3drainheightstop.lua nach
X-Plane 12/Resources/plugins/FlyWithLua/Scripts — NUR EINS, nicht beide.
Werte im Skript per Texteditor anpassbar.

---

## flylua_scripts/rain_rate.md — Dynamic Rain Rate
URL: https://forums.x-plane.org/files/file/97500-dynamic-rain-rate/
Beschreibung komplett (sehr kurz): "Lua script that runs ever half second and checks the current true
airspeed and ajust the rain rate to a more 'realistic' rate to make rainy days... challenging."
Kein Changelog-Block, kein Versionshinweis auf der Seite.

---

## flylua_scripts/sges.md — Simple Ground Equipment & Services (SGES)
URL: https://forums.x-plane.org/files/file/62296-simple-ground-equipment-services-low-tech-services/
Stand: "What's New in Version 06/29/2026", released June 29 2026. Edited July 1 by XPJavelin.
AKTIV GEPFLEGT.

Versionslage (wichtig): v79.6 = stable; v80.1 = NUR ueber SkunkCrafts Updater BETA-Channel.
Features: Ramp-Equipment (Passagierbus, Cargo-Loader); aktive Chocks die das Flugzeug auf schraeger
Apron halten; Shortcuts fuer Better Pushback und X-Plane 12/openSAM Jetways; alternativer
Pushback-Truck (funktioniert auf dem XP12 Aircraft Carrier); Aircraft Arresting Systems (Cables,
Net Barriers); aktives Deicing das den Airframe wirklich vor X-Plane-Ice schuetzt; Adaptive Kit mit
regionalen/lokalen Fahrzeugvarianten; Carrier/Fregatten/U-Boote/Unfallstellen platzierbar;
Wildfires platzierbar (von Water-Bombern loeschbar); SAM-Site die schiessen kann.
Fuer XP11 UND XP12 — dasselbe Skript in beiden.
Installation: Dateien in den FlyWithLua-Scripts-Ordner, Taste fuer das Menue zuweisen.
Extended Coding fuer: ToLiSS, FF/STS, Colimata, X-Trident, JustFlight/Thranda.
Update ueber SkunkCrafts Updater ab v78.0.
Neuere Changelog-Punkte: Pushback-Modul fuer X-Plane 12.4 aktualisiert; Hook-and-Release-Command fuer
Helikopter-Slingload; XP-12.4.1-3D-Assets (Fuel Truck, Catering Truck ersetzt); Hoppie-Network
ATIS (IVAO/VATSIM/PilotEdge, Hoppie-Logon-Code noetig); direkter METAR-Abruf; Front-Line-Modul
neu codiert, resistent gegen Long-Range-Fluege und DSF-Loading.

---

## flylua_scripts/simloadmanager.md — SimLoad Manager
URL: https://forums.x-plane.org/files/file/93858-simload-manager-realistic-pax-cargo-fuel-ground-operations/
Stand: "What's New in Version 07/12/2026", released July 12 2026, V4.1. Edited July 12 by RackhamRPL.
AKTIV GEPFLEGT.

Fuer XP11 und XP12. SimBrief-Integration fuer Pax/Fuel/Cargo.
"SIMBRIEF IS NOW MANDATORY" — SimBrief-Account ist Pflicht.
Voraussetzungen: FlyWithLua; SGES fuer automatisch verknuepfte Ground Services; SimBrief-Account.
Installation: alte Dateien VOR dem Update loeschen. SimLoadManager.lua nach FlyWithLua/Scripts/,
kompletten SLM-Data/-Ordner ins selbe Verzeichnis (nicht umbenennen).
Features: realistisches Laden/Entladen Pax, Cargo, Fuel; automatische Einheitenerkennung (kg/lbs);
Fortschrittsbalken + Zeitschaetzungen; Modi Realistic/Fast/Very Fast/Custom; Fuel-Top-Up;
Tankering-System; Passenger Variability (No-shows, Standbys); Low-Cost-Mode; Random-Events-System
mit eigenem Audio; Ambient Sounds und AI-generierte Voice-Alerts; Boarding-Musik ueber
Boarding_music.wav im SLM-Data-Ordner; Departure- und Arrival-Modus; Turnaround und RON;
Crew Briefing, Catering, Cleaning; Beacon-aware Safety Stop; volle SGES-Integration;
Loadsheet-System (SLMLS); ACARS-Loadsheet-Uplink via Hoppie; SayIntentions.ai-API-Support;
Flight-Sim-Deck-Integration (Android).
Aircraft: Laminar 737-800/A330-300/MD-82/C750; Zibo & LevelUp 737-Familie; ToLiss ALLE;
X-Crafts E-Jets/ERJ; FlightFactor 757/767-Familie + A320; FPS 747-800.
AUSGESCHLOSSEN: Q4XP — SLM deaktiviert dort automatisch die Weight/Fuel-Integration.
Changelog V4.1: Korrektur der Werte bei CDPLC/TELEX-Loadsheet-Uebermittlung, wenn die Einheit Pfund war.

---

## flylua_scripts/xproturb.md — X-ProTurb
URL: https://forums.x-plane.org/files/file/100195-x-proturb-professional-turbulence-engine/
Stand: "What's New in Version 06/30/2026", released June 30 2026. Changelog v2.0.1 -> v2.3.1.
Edited June 20 by sfkcyl. AKTIV GEPFLEGT, sehr hohe Update-Frequenz.

Turbulenz-Engine fuer X-Plane 12, laeuft unter FlyWithLua NG+. Ersetzt XP12s generisches Schuetteln.
Modelliert Atmosphaere und Flugzeug als zwei gekoppelte Systeme.
Grundlagen: MIL-F-8785C, FAA AC/FAR 25.341 (Pratt), ICAO 9625 (Level-D), von-Karman-Spektrum (-5/3),
Dryden- und von-Karman-Gusts, Richardson-Number-CAT, Kelvin-Helmholtz-Billows.
Features: Full 6-DOF-Response (inkl. echtem vertikalem Heave, Sway, Surge); per-Aircraft-Lastvielfaches
(Delta-n in g) via FAR 25.341; Mountain-Wave-Suite (Queney-Lee-Waves, Rotor-Zonen, Wave Breaking,
Hydraulic Jump, Scorer-Parameter); Storm-Modelling (CB-Cores, Hagel, Starkregen, FAA-Severity-Baender
LIGHT bis EXTREME); liest XP-eigenes 3D-Weather-Grid via FFI und kompensiert Doppelzaehlung, oder
"Owns mode"; Turbulence-ahead-Warnung; Live-Diagnostic-UI mit fuenf Tabs
(Status/Weather/Phenomena/Aircraft/Settings); Fly-by-Wire-Erkennung (Airbus behaelt eigenes Law).
Kompatibel: X-Plane 12, FlyWithLua NG+, jedes Aircraft (default/freeware/study-level).
Enthaelt englisches PDF-Handbuch. "Free for personal use. Not for real-world aviation."

---

## toliss/dk_toliss_callout.md — ToLiss Airbus FMA Callout
URL: https://forums.x-plane.org/files/file/91367-toliss-airbus-fma-callout-flywithlua-script/
Stand: v1.0.1, released June 18 2024. Edited June 18, 2024 by DINKIssTyle. SEIT 2024 UNVERAENDERT.

FlyWithLua-Skript, das die FMA fuer den ToLiss Airbus per TTS ansagt.
Ablesemethode pro Airline anpassbar, Skript ist kommentiert.
"It should work with any Toliss Airbus, but I have only verified it on the A319 and A320neo."
EINSCHRAENKUNG (woertlich): "Extracting FMA values from the Toliss Airbus is not easy, so it doesn't
always work 100% of the time, and there are instances where the callouts fail depending on changes in
the variables. The script tries to read up to the blue values in the upper box as much as possible.
I haven't implemented the magenta yet."
Changelog v1.0.1: stellt sicher, dass nichts laeuft, wenn es kein ToLiss Airbus ist.

---

## toliss/toicabrdy.md — ToLiss Airbus Cabin Ready
URL: https://forums.x-plane.org/files/file/91876-toliss-airbus-cabin-ready-automatic-flywithlua-script/
Kein Changelog-Block auf der Seite, keine Versionsangabe.

Sendet automatisch den "Cabin Ready"-Call fuer alle ToLiss-Airbus-Muster.
Beim Departure: Cabin ready nach ca. 4-8 Minuten, abhaengig von der Passagierzahl.
Beim Approach: Cabin ready wenige Sekunden nachdem Flaps UND Gear draussen sind.
"Only tested under XP12, if might works in XP11 version."
"Only tested with normal routing flight condition, including go-around and through flight. In worst
case, you might need to press the FWD call manually, or you get unnecessary ding, it won't cancel ready."
Voraussetzung: FlyWithLua.

---

## toliss/toliss_mods.md — zwei verlinkte Mods

### Easy Freighter (A321) — OK
URL: https://forums.x-plane.org/files/file/92976-easy-freighter-conversion-kit-for-the-toliss-321/
Stand: Version 3.3, released December 18 2024 ("3.3 has upgraded interior objects").
Edited August 31, 2025 by XPJavelin.
Conversion-Kit, das einen A321-Frachter nachbildet. Neues Objekt in den A321-Objektordner legen,
kompatible Livery installieren. Die Cargo-Livery braucht in livery.tlscfg zwei Zeilen:
  external_Extras = YES
  custom_Cabin = F
Wird mit Demo-Livery ausgeliefert. Es gibt ein separates A320-Kit.

### CARDA Engine Installer (A320 family) — TOTER LINK (bestaetigt)
URL: https://forums.x-plane.org/files/file/94704-carda-engine-installer-for-toliss-a320-family/
Antwort im echten Browser: "Sorry, you do not have permission for that! ... We could not locate the
item you are trying to view. Error code: 2D161/2"
Das ist KEIN Cloudflare-403, sondern eine echte Nicht-Existenz. Der Eintrag wurde entfernt.
=> Findung fuer toliss_mods.md: Link tot, Mod offenbar zurueckgezogen.

---

## sounds/mango_studios.md — Mango Studios (nur Teilbeleg)
URL: https://forums.x-plane.org/forums/forum/653-mango-studios-sound-packs/
Das ist ein Support-Unterforum unter "Commercial Vendors Support", keine Produktseite.
10 Seiten Threads. Juengste Aktivitaet Juli 2026 (MD80 installation issue, Rotate MD80 pack,
Engine volume setting) — Vendor ist also aktiv.
Genannte Produkte in den Threads: ATR-72-500 (Aircraft Development, Dezember 2025), PW4000 Engine Mod
Paint Kit, PT6 Soundpack v1.01 fuer Aerobask Epic 1000, Rotate MD-80 Pack, Rotate MD-11 Sound Bank
v1.15, Magknight 787 Sound Pack, Felis 747-200(F), ToLiss A330 Sound Pack, A330neo, X-Crafts ERJ v2
Sound Pack, JustFlight BAe 146 Sound Pack, FlightFactor 767/757, FPS B747-8.
Thread "X-Plane 12 Product Compatability" existiert (September 2022, 52 Antworten).
NICHT BELEGT: Produktdetails/Preise — die liegen auf store.x-plane.org (Extension-Domain gesperrt).

---

## NICHT BELEGBAR — offen

- `flylua_scripts/simbrief_simple_ofp.md` — Seite liefert nur eine User-Review von 2021, die
  Beschreibung ist offenbar leer. Aus der Autorenantwort geht hervor: Skript liegt in
  FlyWithLua/Scripts, schreibt simbrief_ofp.xml, Pfad im Skript per SCRIPT_DIRECTORY aenderbar.
  Version 0.2 war fuer Oktober 2021 angekuendigt.
- `sounds/kosp_project.md` — store.x-plane.org von der Chrome-Extension gesperrt.
- `scenery_addons/aep.md`, `kvm/myfs_flights.md`, `flylua_scripts/simscreenoverlay.md` — enthalten
  gar keine x-plane.org-URL, Quelle muss anderswo liegen.
