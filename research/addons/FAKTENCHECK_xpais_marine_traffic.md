# Faktencheck: XPAIS Marine Traffic (EN + DE)

**Datum:** 2026-08-03
**Geprüfte Seiten:** `docs/en/addon/traffic/xpais_marine_traffic.md`, `docs/de/addon/traffic/xpais_marine_traffic.md` (neu angelegt)
**Primärquellen:** codeberg.org/xbard/XPAIS-Marine-Traffic (README + Repo-Status), forums.x-plane.org Topic 348448 (per Chrome), forums.x-plane.org Datei 100400 (per Chrome)

---

## Ausgangslage: zwei verschiedene Projekte mit fast gleichem Namen

Beim Einstieg über die Forum-Datei 100400 sah die Sache nach einem Windows-Only-Tool aus. Es sind
aber **zwei unabhängige Projekte**:

| | XP AIS Traffic | XPAIS Marine Traffic |
|---|---|---|
| Autor | nestasko | CheckCanopy / xbard |
| Quelle | forums.x-plane.org Datei 100400 | codeberg.org/xbard, Forum-Topic 348448 |
| Plattform | **Windows 64-bit** (wörtlich unter „Requirements → Supported Platform") | **Linux**, Bau aus dem Quellcode |
| Lizenz | nicht genannt, quellgeschlossen | GPL-3.0 |
| Stand | Beta 2.1, aktualisiert 2026-06-22 | letzter Commit 2026-06-16, Repo **archiviert 2026-07-07** |
| Bewegungsmodell | Dead Reckoning (Vorausrechnung) | Interpolation, 60 s hinter Echtzeit |

Ein Fork-/Abstammungsverhältnis ist **nicht belegt** und wird auf der Seite auch nicht behauptet —
nur die Verwechslungsgefahr ist benannt.

Zum Windows-Projekt: Auf die Nutzerfrage vom 2026-06-14 („is it currently Windows-only?")
antwortet nestasko, Linux- und Mac-Unterstützung stünden „definitely on the roadmap", der Kern sei
„already largely platform independent"; zunächst werde aber Windows stabilisiert. Stand 2026-08-03
kein Linux-Build. Deshalb bekommt es keine eigene Seite, sondern nur den Abgrenzungshinweis.

---

## Belegte Behauptungen

| # | Behauptung | Quelle |
|---|------------|--------|
| 1 | Repo archiviert am 2026-07-07, letzter Commit 2026-06-16, 19 Commits | Codeberg-Banner, wörtlich: „This repository has been archived on 2026-07-07. You can view files and clone it, but you cannot make any changes to its state" |
| 2 | GPL-3.0 | Repo-Metadaten + README |
| 3 | Live-AIS über AISStream via TLS-WebSocket | README |
| 4 | Thread-Trennung: `ais_client` hält die WebSocket, fasst die X-Plane-API nie an; Sim-Aufrufe im Flight-Loop-Thread | README, wörtlich: „ais_client — owns the WebSocket on a background thread…Never touches the X-Plane API" |
| 5 | Darstellung 60 s hinter Echtzeit, Interpolation zwischen bekannten Fixes statt Vorausrechnung | README |
| 6 | Rümpfe aus X-Planes Standard-Schiffsobjekten, Klassifikation über AIS-Typcode und Schiffsmaße | README |
| 7 | OpenSceneryX optional; ohne sie fallen Passagierschiffe auf Yacht-Rümpfe zurück (XP12 hat keine Passagierschiff-Modelle) | README |
| 8 | Bau mit `cmake`, C++17, OpenSSL-Dev; SDK liegt bei; `./build.sh`, `./build.sh install` | README |
| 9 | Installationspfad `Resources/plugins/XPAISTraffic/` | README |
| 10 | `config.ini` mit `[AIS] ApiKey=` und `[Display] ShowTraffic/Labels/OpenSceneryX` | README |
| 11 | Menüpunkte Show traffic / Show labels / Use OpenSceneryX ships / Contacts: N | README |
| 12 | Menüpunkt „Hide vessels w/o heading (HDG 000)", standardmäßig aus; Ursache und Grenze | Forum 348448, Beitrag des Entwicklers vom 2026-06-15 |
| 13 | Wakes standardmäßig aus, referenzieren `wake.png` statt sie zu kopieren | Forum 348448, ebd. |
| 14 | XPs Schiffs-Engine ist positionsgeschlossen (`shipping-lanes-for-boats.png` als Dichteraster, kein Dataref/SDK-Aufruf zur Positionierung), daher kein Einspeisen und kein geerbtes Kielwasser | Forum 348448, ebd., ausführliche Begründung des Entwicklers |
| 15 | Log unter `logs/xpaistraffic.log` | Forum 348448, ebd. |
| 16 | Grenzen: keine Kollisionsvermeidung, kein Hafen-Skripting, Visuals unfertig | README, wörtlich „No collision avoidance.", „No berth/port scripting.", „Visuals untuned in-sim" |
| 17 | ~3.000 Kontakte im Bereich EHAM, keine Daten in der Straße von Hormus | Forum 348448, Testbericht flightwusel 2026-06-15 |

---

## Widerspruch (dokumentiert, nicht aufgelöst)

**„Show ships and balloons" — an oder aus?**

- **README:** „Keep 'show ships and balloons' enabled" — Begründung dort: die Schiffe seien
  instanziierte Standard-Schiffsobjekte.
- **Forum 348448, Entwickler am 2026-06-15:** „confirmed, you can leave it off. Our vessels are
  plugin-instanced so they render regardless, and that also means we won't fight XP's own boats."
  Zusätzlich: „Leaving XP's traffic on actively hurts. Those synthetic boats have nothing to do with
  real traffic, so they'd ghost and duplicate right next to our real AIS vessels."

Die Forum-Aussage ist die jüngere und stammt vom Entwickler selbst, im direkten Kontext einer
Nutzerkorrektur. Die Seite folgt ihr, benennt den Widerspruch zur README aber ausdrücklich, damit
Leser nicht an der README hängenbleiben. Da das Repo archiviert ist, wird die README nicht mehr
nachgezogen — der Widerspruch bleibt dauerhaft bestehen.

---

## Nicht übernommen

- **Schiffsbibliothek und AIS-Typcode-Tabelle** des Windows-Projekts (Rumpfnamen wie
  „BulkCarrier 155A", Typcodes 30–89) — gehört zum anderen Projekt, nicht zum Linux-Build.
- **Versionsnummern** und Dateigröße des Windows-Projekts — irrelevant für die Seite.
- **Diagnose-Framework** des Windows-Projekts (OpenSSL-Version-Reporting, WebSocket-State-Tracking
  usw.) — ebenfalls anderes Projekt.

## Offen

- **Grund der Archivierung** ist nirgends genannt: kein Abschluss-Commit, keine Notiz im Repo, im
  Forum-Thread bis zum letzten gelesenen Beitrag kein Hinweis. Ein Nachfolgeprojekt ist nicht
  auffindbar. Falls sich das ändert, Seite aktualisieren.
- **Ob das Plugin gegen aktuelle X-Plane-12-Versionen noch baut und läuft**, ist mangels Pflege
  ungetestet. Nicht behauptet, aber der Archiv-Hinweis warnt entsprechend.
