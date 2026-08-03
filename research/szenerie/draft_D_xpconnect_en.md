# Klärungsergebnis — "xpme" ist NICHT xpconnect.me

**Kurzfassung:** Auf xpconnect.me gibt es kein Ortho-Streaming und keine Gebühr für einen
hochauflösenden Modus. Beides trifft dagegen exakt auf ein anderes Produkt zu:
**XPME = X-Plane Map Enhancement** (Entwickler `derekhe`, Herausgeber AIFlyGo, aiflygo.com).
Das ist mit hoher Wahrscheinlichkeit das vom Nutzer gemeinte Tool.

---

## 1. Gibt es bei xpconnect.me ein Streaming-Angebot? — Nein

Alle Navigationspunkte der Site wurden über `sitemap.xml` erfasst und durchgesehen
(53 URLs, plus der komplette Plattform-Guide unter `/guide/`). Ergebnis:

| Angebot | Was es ist | Streaming? |
|---|---|---|
| OrthoForge | Photoscenery-Builder, englischer Fork von Ortho4XP V3.2, GPL v3 | Nein — Build-Pipeline, schreibt `zOrtho4XP_<lat><lon>` nach `Custom Scenery/` |
| Pre-baked OSM Tiles | Fertige OSM-Vektorlayer als statische Dateien gegen Overpass-Rate-Limits | Nein — Build-Zeit-Daten |
| Sonny LiDAR DTM Mirror | Spiegel von Sonnys `.hgt`-Höhentiles + eigene USGS-3DEP-Bakes | Nein — Build-Zeit-Daten |
| Ireland Scenery, Traffic-Fixes, Treelines | Statische Custom-Scenery-Pakete | Nein |

Es existiert kein Produkt mit Laufzeit-Texturlieferung, kein FUSE-Layer, kein Tile-Proxy.
Die Rolle, die AutoOrtho und XEarthLayer spielen, spielt bei xpconnect.me nichts.

**Tote Links (belegt):** `https://xpconnect.me/ortho.html` und
`https://xpconnect.me/ortho-library.html` stehen in der `sitemap.xml`, liefern aber beide
HTTP 404. Das waren die einzigen Kandidaten, die noch ein weiteres Ortho-Angebot hätten
sein können.

## 2. Gebührenaussage bei xpconnect.me — widerlegt

Zitat aus dem offiziellen Plattform-Guide, Abschnitt "What it costs"
(<https://xpconnect.me/guide/>):

> "Nothing. There is no subscription, no membership tier and no paid unlock anywhere on the
> platform."

Ergänzend, <https://xpconnect.me/guide/marketplace.html>:

> "XPConnect never takes your money for an add-on: every paid product checks out on the
> seller's own store."

Was dort überhaupt Geld kostet, ist eng begrenzt und hat nichts mit Auflösung zu tun:

- **AI-Funktionen (BYOK):** eigener API-Key bei Anthropic/OpenAI/Mistral/DeepSeek/Qwen/GLM/Kimi,
  Zahlung direkt an den LLM-Anbieter. Eine AI-Tower-Position in Casement wird vom Server bezahlt.
- **Marketplace:** Payware Dritter, Checkout beim jeweiligen Verkäufer, 5 % Referral-Provision.
- **Geplante Eigenprodukte:** drei Platzhalter-Einträge (POH Copilot Premium 5 €, Career Premium 4 €,
  Sticker Pack 6 €) — laut Guide "None of them are real yet and all three checkout links are
  literal placeholders."
- **Ko-fi-Spendenbutton**, ausdrücklich freiwillig.

Der einzige entfernt passende Treffer in Sachen "hochauflösend kostet": In OrthoForge braucht der
Imagery-Provider `Mapbox` "an API token in the URL", und `Maxar` liefert "High-res, up to ZL 22"
(<https://xpconnect.me/orthoforge/providers.html>). Das ist ein Fremdanbieter-Konto, keine
XPConnect-Gebühr, und es ist keine Grundlage für die Nutzeraussage.

## 3. Der wahrscheinlich gemeinte Kandidat: XPME

**X-Plane Map Enhancement (XPME)** — Entwickler `derekhe`, Website AIFlyGo.
Passt auf alle drei Merkmale der Nutzeraussage:

- **Laufzeit-Streaming wie AutoOrtho/XEarthLayer:** "Stream seamless satellite images directly
  onto the terrain" (Produktseite auf x-plane.to). Ersetzt Bodentexturen live, arbeitet mit
  "base packages" (Basispakete, entsprechen den DSF/TER-Paketen bei XEarthLayer) und liefert
  DDS-Texturen an X-Plane.
- **Offizieller Linux-Build:** Release-Assets auf GitHub enthalten
  `xplane-map-enhancement-<ver>.AppImage` und `xplane-map-enhancement_<ver>_amd64.deb`.
  Linux-Abhängigkeiten laut Doku: `libfuse3-dev`, `aria2`, `dotnet-runtime-10.0`,
  `aspnetcore-runtime-10.0`. FUSE3 ⇒ dasselbe VFS-Prinzip wie AutoOrtho/XEarthLayer.
- **Hochauflösender Modus kostenpflichtig — belegt.** FAQ (aiflygo.com): frei sind ArcGIS, Bing
  und Google Maps bei "medium image quality"; die Pro-Version bringt "additional map sources with
  superior image quality and more frequent updates", "map color adjustment", "preloading feature"
  und "high-resolution ground textures".
  **Preise** (aus dem Bestellformular k.aiflygo.com/purchase, Produkt "X-Plane 12"):
  `XP30: $5` (30 Tage), `XP365: $40` (365 Tage). Also ein **Zeit-Abo**, kein Einmalkauf.
  Lizenz ist pro PC ("One license can only be used by one pc"), nicht-kommerziell.

---

# Gliederungsskizze: `docs/en/scenery/ortho_streaming/xpme.md`

Vorbilder: `autoortho.md` und `xearthlayer.md`. Gleiche Tiefe, gleicher Ton, Tabellen statt
Listenwüsten, `---` zwischen Hauptsektionen, Glossar-Links (`../../glossary.md#...`) für
orthophotos, FUSE, DDS, DSF, ZL, mesh, scenery_packs.ini.

**Frontmatter**

- `description:` eine Zeile, Muster xearthlayer.md: "XPME (X-Plane Map Enhancement) streams
  satellite imagery into X-Plane 12 via FUSE. Linux setup, free vs. paid Pro tier, and comparison
  with AutoOrtho and XEarthLayer."

**# XPME (X-Plane Map Enhancement)** — Einleitung, 3–4 Sätze

- Dritte Streaming-Lösung neben AutoOrtho und XEarthLayer
- Entwickler derekhe / AIFlyGo, closed source, Release-Repo auf GitHub
- Zwei Sim-Familien (MSFS und X-Plane 12) — hier nur die X-Plane-Seite
- **Direkt hier, nicht versteckt:** Freemium. Frei ist ArcGIS/Bing/Google bei mittlerer Qualität;
  hohe Auflösung nur im kostenpflichtigen Pro-Abo. `!!! warning`-Box mit den Preisen.

**## How It Works**

- FUSE3-basiertes VFS, Querverweis auf `how_streaming_works.md` statt Wiederholung
- Base Packages (Basispakete) — Rolle wie DSF/TER-Pakete bei XEarthLayer; Downloader in der App,
  `aria2c` als Download-Backend, sequenzielle Installation
- Kartenquellen: ArcGIS, Bing, Google (frei) + Pro-Quellen
- Offene Frage im Text nicht kaschieren: Cache-Architektur und Zoomlevel sind offiziell nicht
  dokumentiert (siehe OFFENE PUNKTE)

**## Free vs. Pro** — eigener Abschnitt, Tabelle

| | Free | Pro |
|---|---|---|
| Kartenquellen | ArcGIS, Bing, Google Maps | zusätzliche Quellen, häufigere Updates |
| Bildqualität | "medium image quality" | high-resolution ground textures |
| Farbanpassung | nein | ja |
| Preloading | nein | ja |
| Neue Features | später | zuerst |
| Preis | 0 | $5 / 30 Tage, $40 / 365 Tage, 1 Lizenz = 1 PC |

- Klarstellen: Abo, keine Dauerlizenz; nicht-kommerziell; Zahlung PayPal/BuyMeACoffee
- Nüchterner Satz zur Einordnung: AutoOrtho und XEarthLayer sind kostenlos und quelloffen —
  bei XPME zahlt man für Aufbereitung und Komfort, nicht für die Bilddaten selbst
  (Disclaimer des Herstellers dazu zitierfähig)

**## System Requirements** — Tabelle wie xearthlayer.md

- Linux x86_64, FUSE3
- Pakete (Debian/Ubuntu): `libfuse3-dev`, `aria2`, `dotnet-runtime-10.0`, `aspnetcore-runtime-10.0`
- SSD für Basispakete (Doku warnt ausdrücklich vor HDD/externen Laufwerken)
- X-Plane 12

**## Installation on Linux** — Kern der Seite

- `.deb` bzw. `.AppImage` von den GitHub-Releases
- ```bash-Block mit `sudo apt install …` und `dpkg -i`
- Basispaket-Pfad in den Einstellungen setzen, Downloader starten
- `!!! warning`: Linux-Assets fehlen in einzelnen Releases (4.7.4 nur .exe/.dmg) — im Zweifel
  auf das letzte Release mit AppImage/.deb zurückgehen
- .NET 10 ist auf Debian stable ggf. nicht in den Repos → Microsoft-Repo/Backports (PRÜFEN)

**## Comparison with AutoOrtho and XEarthLayer** — Pflichtabschnitt, Muster
`autoortho.md#comparison-with-ortho4xp` bzw. `xearthlayer.md#comparison-with-autoortho`

| Dimension | XPME | AutoOrtho | XEarthLayer |
|---|---|---|---|
| Lizenz/Kosten | closed source, Freemium, Pro-Abo | GPL, kostenlos | quelloffen, kostenlos |
| Plattform | Windows, macOS, Linux | Windows, Linux, macOS (Apple Silicon) | nur Linux |
| Sprache/Stack | .NET, Electron-Frontend (PRÜFEN) | Python + C | Rust |
| Streaming | FUSE3 | FUSE | FUSE |
| Regionaldaten | Base Packages via In-App-Downloader | Overlay-Downloads | `xearthlayer packages install` |
| Max. Auflösung | volle Auflösung nur mit Pro | bis ZL18 | providerabhängig |
| Konfiguration | GUI | GUI | CLI + `config.ini` |

- Abschließender Absatz "Which system is a better fit?" analog autoortho.md

**## Known Limitations on Linux**

- Nur belegbares: unregelmäßige Linux-Assets pro Release, .NET-10-Abhängigkeit,
  Doku und FAQ sind windowszentriert
- Nichts erfinden — was ungeprüft ist, gehört in OFFENE PUNKTE, nicht auf die Seite

**## Further Reading** — Tabelle

| Topic | Page | Focus |
|---|---|---|
| AutoOrtho | `autoortho.md` | Streaming mit breiter Plattformunterstützung |
| XEarthLayer | `xearthlayer.md` | Rust-Streaming, Linux-only, GPU-Encoding |
| How Ortho Streaming Works | `how_streaming_works.md` | DSF → .ter → DDS, FUSE, Cache |
| Ortho4XP | `../orthophotography/ortho4xp.md` | Statische Tiles offline erzeugen |
| Static + Streaming | `static_plus_streaming.md` | Kombination beider Ansätze |
| Filesystem | `../../linux/optimizations/filesystem.md` | I/O für Cache und Basispakete |

**## Sources** — 5–8 Einträge, Format `- [Titel](URL) — Herausgeber`

- GitHub Release-Repo, aiflygo.com Download-Doku, FAQ, License, Purchase-Seite, x-plane.to-Produktseite

---

<!-- ZURUECKGESTELLT: Multiplayer/ATC/Voice (xpconnect.me) -->

Recherchestand zu xpconnect.me, falls daraus später doch eine Tool-Seite unter
`docs/en/addon/tools/xpconnect.md` werden soll. Alles unten ist belegt, Quelle jeweils genannt.

**Was XPConnect ist**

Freie Multiplayer-Plattform für X-Plane 12 (bis 60 Piloten), mit Live-ATC, In-Browser-Voice,
Instructor Operating Station, Karriere-/Wirtschaftsmodus, Forum, Leaderboard, Galerie.
Kein Bezug zu VATSIM/IVAO/PilotEdge; eigener Server, aktuell genau einer. Registrierung ist
gratis, wird aber manuell freigeschaltet, Mindestalter 18.

**Dreiteilige Architektur** (Quelle: <https://xpconnect.me/guide/>)

- C++-Plugin unter `X-Plane 12/Resources/plugins/XPConnect/` — liest Position, Funk, Steuerflächen,
  zeichnet fremde Flugzeuge, Menü unter `Plugins → XPConnect`
- Desktop-GUI-App daneben — stellt die Serververbindung her, trägt Karte, Chat, ATC-Comms, Voice,
  Glascockpit-Panels, Karriere, AI-Copilot. Qt/QtWebEngine-basiert
- Website mit ca. 70 Seiten

**Linux-Installation** (Quelle: <https://xpconnect.me/downloads.html>)

- "XPConnect Full Bundle" als `.tar.gz`, Zielplattform "Linux x86_64, glibc 2.31+"
- Bemerkenswert: macOS ist nur Source ("Source-only plugin — compile steps in
  BUILD-PLUGIN-MAC.md"), Linux bekommt ein fertiges Paket
- Download erfordert Login
- Ablauf laut Site: `plugin/XPConnect/` nach `X-Plane 12/Resources/plugins/` kopieren, einmalig
  `setup`-Skript (ca. 2 min, legt lokale Python-Umgebung an), danach `start`-Skript
- Voraussetzung: "Python 3.12+ from python.org"
- CSL-Modelle nötig, sonst unsichtbarer Verkehr; Pfad
  `X-Plane 12/Resources/plugins/XPConnect/Resources/CSL/`, empfohlen Bluebell OBJ8 CSL
- `config.ini` mit `callsign`, `aircraft_type`, `airline`, `gui_port = 49000`
- Netz: "HTTPS 443 only (WebSocket — no port forwarding needed)"
- Systemanforderungen laut Tabelle: X-Plane 12.0 min. / 12.1+ empfohlen; 50 MB Plugin,
  500 MB+ mit CSL

**Linux-Spezifika, die eine Seite rechtfertigen würden**

- **Hardware-PTT über evdev:** "Bind any USB footswitch, HOTAS button, macropad key, or keyboard key
  via Linux evdev — the PTT fires even when X-Plane has focus, not just the GUI"
  (<https://xpconnect.me/features.html>). Das ist ein explizit für Linux gebautes Feature.
- **QtWebEngine-Sandbox:** Changelog auf downloads.html: "QtWebEngine sandbox auto-disabled on Linux
  to fix silent blank-view issues on Fedora". Sicherheitsrelevant, gehört benannt.
- Landing-Log unter `~/.xpconnect/landings.log`, Streambot-Config unter `~/.xpconnect/streambot/`

**Voice**

- "Live voice comms for pilots and controllers — join in-browser, no app needed"
  (<https://xpconnect.me/voice.html>), Login nötig. Kanäle: Lounge, ATC-Frequenzen,
  Group Flights, Emergency/UNICOM. Voice läuft auch in der Desktop-App, die eine
  eingebettete Browser-View nutzt.
- **Nicht belegt:** WebRTC-Nachweis, PipeWire/PulseAudio-Verhalten, Mikrofonrechte,
  Browser-Permission-Fallstricke. Dazu steht auf der Site nichts.

**ATC**

- Browser-Radarschirm unter `atc.xpconnect.me`, keine Zusatzsoftware. Controller können
  optional einen Observer-Slot in X-Plane belegen.
- AI-Controller ist BYOK; eine Position (Casement/EIME, 123.500) wird vom Server bezahlt.

---

<!-- OFFENE PUNKTE -->

**Zu XPME (vor dem Schreiben der Seite zu klären)**

1. **Interner Aufbau nicht dokumentiert.** Ob XPME wirklich einen FUSE-Mount fährt (statt FUSE3 nur
   für etwas anderes zu brauchen), wie der Cache aufgebaut ist, welche Zoomlevel maximal geliefert
   werden — steht nirgends offiziell. `libfuse3-dev` in den Linux-Abhängigkeiten ist ein starkes
   Indiz, mehr nicht. Ohne besseren Beleg darf die Seite keine Cache- oder ZL-Zahlen nennen.
2. **Technologie-Stack der App** (Electron? Avalonia?) ist geraten. `dotnet-runtime` + `aspnetcore-runtime`
   belegen .NET, das Frontend nicht. In der Vergleichstabelle sonst weglassen.
3. **Was genau "high-resolution ground textures" in Pro heißt** — keine Zahl, keine Zoomstufe,
   nur Marketingformulierung im FAQ. Auf der Seite entsprechend vorsichtig formulieren.
4. **Linux-Assets sind release-abhängig.** 4.7.3 hat `.AppImage` + `.deb`, 4.7.4 nur `.exe`/`.dmg`.
   Ob das Absicht, Versehen oder ein Nachreichen ist, ist unklar. Vor Veröffentlichung erneut prüfen.
5. **.NET 10 Runtime auf Debian/Ubuntu:** Der Doku-Befehl `sudo apt install dotnet-runtime-10.0`
   setzt Repos voraus, die auf Debian stable nicht selbstverständlich sind. Ungeprüft.
6. **Keine unabhängige Linux-Erfahrungsquelle geprüft.** Der einschlägige Thread
   "XPlane Map Enhancement can run on Linux now" liegt auf forums.x-plane.org, das WebFetch
   mit 403 blockt (bekanntes Problem). Aussagen wie "getestet unter Ubuntu 24.04" stammen bisher
   nur aus Suchmaschinen-Snippets, nicht aus der gelesenen Primärquelle.
7. **Quellenaktualität** ist unkritisch: Releases und Doku sind von 2026.

**Zu xpconnect.me**

8. `ortho.html` und `ortho-library.html` sind in der Sitemap, liefern aber 404.
9. Voice-Audio unter Linux ist nirgends dokumentiert — für eine ehrliche Tool-Seite müsste das
   entweder selbst getestet oder als "nicht dokumentiert" benannt werden.
10. Download und damit jede Verifikation der Installationsschritte erfordert ein manuell
    freigeschaltetes Konto. Alle Installationsangaben oben sind Website-Text, nicht nachvollzogen.

**Generell**

11. **Die Zuordnung "xpme = X-Plane Map Enhancement" ist eine Schlussfolgerung, keine Bestätigung
    des Nutzers.** Sie passt auf alle drei Merkmale (Streaming wie AutoOrtho/XEarthLayer, Linux,
    hochauflösend kostenpflichtig), sollte aber vor dem Schreiben kurz rückbestätigt werden.
