# Faktencheck: AutoOrtho + XEarthLayer (EN + DE)

**Datum:** 2026-02-18
**Geprüfte Seiten:** `docs/en/scenery/ortho_streaming/autoortho.md`, `docs/de/scenery/ortho_streaming/autoortho.md`, `docs/en/scenery/ortho_streaming/xearthlayer.md`, `docs/de/scenery/ortho_streaming/xearthlayer.md`
**Primärquellen verifiziert:** github.com/kubilus1/autoortho, github.com/ProgrammingDinosaur/autoortho4xplane, programmingdinosaur.github.io, github.com/samsoir/xearthlayer, xearthlayer.app, verticalsims.com

---

## AutoOrtho — Fehler (1) — Korrekturbedarf

### 1. USGS als AutoOrtho-Provider empfohlen
**Datei:** `autoortho.md:115`
**Behauptung:** "Solution: Use VPN or switch to USGS sources" (bei HTTP 429)
**Befund:** USGS ist kein Map-Provider im ProgrammingDinosaur-Fork. Die Provider-Liste umfasst: Bing, Google, Here, Yandex, Apple Maps (Research-Paper `autoortho4xplane_fork.md`, Zeilen 254–261). USGS war im Original-kubilus1-AutoOrtho vorhanden, aber mit HTTP-404-Fehlern gemeldet und im Fork nicht weitergeführt. USGS ist ein XEarthLayer-Provider (v0.2.6). Da die Seite den Fork als Standard empfiehlt, ist die Empfehlung irreführend.
**Korrektur:** "Use VPN or switch to another map provider (e.g., Google or Here)" / DE: "VPN verwenden oder zu einem anderen Kartenanbieter wechseln (z. B. Google oder Here)"

---

## AutoOrtho — Nuancen (3) — verbesserbar, aber akzeptabel

### N1. RAM "up to 64 GB"
**Datei:** `autoortho.md:20`
**Befund:** Die Zahl 64 GB stammt aus den XEarthLayer-Systemanforderungen ("Ultimate"-Tier), nicht aus AutoOrtho-Quellen. Der AutoOrtho-Fork dokumentiert RAM-Nutzung nur qualitativ (abhängig von Buffer Pool, Zoom Level, Pre-Fetch). 64 GB ist als pauschale Aussage irreführend.
**Empfehlung:** Ersetzen durch "The streaming process impacts CPU, RAM, and disk performance" ohne konkrete Zahl.

### N2. Python 3.12+ empfohlen für Fork
**Datei:** `autoortho.md:171`
**Befund:** v2.0.0 des Forks nutzt Python 3.14 (Research-Paper Zeile 60). Die Angabe "Python 3.12+" könnte für Source-Installationen zu niedrig sein. Für Binary-Installationen irrelevant (alle Dependencies gebundelt). Lektorat-Dokument empfiehlt, Python-Versionsdetails als Implementierungsdetail wegzulassen.
**Empfehlung:** Hinweis ergänzen, dass die Binary-Installation empfohlen wird und keine Python-Version erfordert.

### N3. ≥100 Mbps Internet erforderlich
**Datei:** `autoortho.md:14, 40`
**Befund:** Kein AutoOrtho-Primärquelle dokumentiert "100 Mbps" als Minimum. Der Fork hat ein Fallback-System (Cache, Mipmap-Skalierung), das bei schlechteren Verbindungen funktioniert. Die 100-Mbps-Zahl stammt möglicherweise aus den XEarthLayer-Minimum-Anforderungen.
**Empfehlung:** Abschwächen zu "a fast, stable internet connection" / "eine schnelle, stabile Internetverbindung".

---

## AutoOrtho — Korrekt (14) — keine Änderung nötig

| # | Behauptung | Quelle |
|---|------------|--------|
| 1 | kubilus1 letzte Version 0.7.2 (21. Jan 2024) | GitHub Releases kubilus1/autoortho |
| 2 | Fork-URL github.com/ProgrammingDinosaur/autoortho4xplane | GitHub (aktiv, 97 Stars, 2.0.4 aktuell) |
| 3 | C-Pipeline "bis zu 3× Verbesserung" | v2.0.0 Release Notes (netzwerkabhängig) |
| 4 | Vier Pipeline-Modi: Auto, Native, Hybrid, Python | v2.0.0 Release Notes |
| 5 | Provider: Bing, Google, Here, Yandex, Apple Maps | Research-Paper Zeilen 254–261 |
| 6 | flatten 1 in apt.dat | Etablierter X-Plane-Mechanismus, auch in ortho4xp.md dokumentiert |
| 7 | vStates als Ortho-Alternative | Verticalsim Studios, reales Freeware-Produkt für US |
| 8 | Ortho4XP max ZL19 | ortho4xp.md und Research-Paper |
| 9 | .aob2 Bundle-Format | v2.0.0 Release Notes |
| 10 | macOS nur Apple Silicon | Research-Paper, seit v1.2.0 |
| 11 | Auto scenery_packs.ini für SimHeaven | Research-Paper, seit v1.0.1 |
| 12 | X-Plane 11.50+ oder X-Plane 12 | Research-Paper Zeilen 153, 487 |
| 13 | SimHeaven X-World nutzt OpenStreetMap | Allgemein bekannt, SimHeaven-Doku |
| 14 | yOrtho-Overlays redundant mit SimHeaven | Research-Paper Zeile 306 |

## AutoOrtho — Nicht verifizierbar (2)

| # | Behauptung | Anmerkung |
|---|------------|-----------|
| 1 | Log-Pfad ~/.autoortho-data/autoortho.log | Plausibel (kubilus1-Konvention), nicht explizit bestätigt für Fork |
| 2 | 16 GB RAM Minimum | Nicht in AutoOrtho-Quellen dokumentiert, aber plausible allgemeine Empfehlung |

---

## XEarthLayer — Fehler (0)

Keine.

---

## XEarthLayer — Nuancen (3) — verbesserbar, aber akzeptabel

### N4. ≥800 Mbps Internet empfohlen
**Datei:** `xearthlayer.md:50`
**Befund:** Die README sagt "800 Mbps recommended", die Website-Tier-Tabelle (xearthlayer.app) differenziert: Minimum 100 Mbps, Recommended 500 Mbps, Ultimate 1 Gbps. Die 800-Mbps-Zahl scheint eine ältere Angabe, die in der differenzierteren Tabelle aufgegangen ist. Research-Paper bestätigt die Diskrepanz.
**Empfehlung:** Auf 500 Mbps (Recommended-Tier der Website) aktualisieren oder die Tier-Tabelle übernehmen.

### N5. Version 0.3.0 im dpkg-Befehl
**Datei:** `xearthlayer.md:65`
**Befund:** `sudo dpkg -i xearthlayer_0.3.0-1_amd64.deb` enthält eine hartcodierte Versionsnummer. Bei 8 Releases in 7 Wochen wird diese schnell veraltet.
**Empfehlung:** Versionsnummer entfernen oder auf Releases-Seite verweisen.

### N6. cpu_concurrent Default vereinfacht
**Datei:** `xearthlayer.md:133`
**Befund:** Doku sagt "CPUs × 1.25", tatsächliche Formel ist `max(num_cpus × 1.25, num_cpus + 2)`. Unterschied nur bei wenigen CPUs relevant (4 CPUs: Formel gibt 6 statt 5).
**Empfehlung:** Akzeptabel als Vereinfachung, ggf. Fußnote für Präzision.

---

## XEarthLayer — Korrekt (17) — keine Änderung nötig

| # | Behauptung | Quelle |
|---|------------|--------|
| 1 | Rust-basiert | Cargo.toml, GitHub Language Field |
| 2 | DDS BC1/BC3-Kompression | xearthlayer.app/docs/how-it-works/ |
| 3 | Zwei-Tier-Cache (Memory + Disk) | xearthlayer.app/docs/how-it-works/ |
| 4 | Adaptives Prefetching (Ground/Cruise) | v0.3.0 Release Notes |
| 5 | Circuit-Breaker-Mechanismus | v0.2.12, v0.3.0 Release Notes |
| 6 | 6 Map-Provider (Bing, Google, Apple, ArcGIS, MapBox, USGS) | v0.2.6 Release Notes, xearthlayer.app/docs/configuration/ |
| 7 | Nur Linux | xearthlayer.app/docs/faq/ |
| 8 | Nur X-Plane 12 | README, Website |
| 9 | Pakete: .deb, .rpm, .tar.gz, AUR | v0.3.0 Release Assets |
| 10 | Build: make release, make install → ~/.local/bin | Makefile |
| 11 | ForeFlight UDP Port 49002 | v0.2.8, xearthlayer.app/docs/getting-started/ |
| 12 | DSF/TER-Pakete aus xearthlayer-regional-scenery | GitHub Repository bestätigt |
| 13 | Basiert auf Shred86 Ortho4XP-Fork | Regional Scenery Repository |
| 14 | threads Default = num_cpus | Source Code / Research-Paper |
| 15 | max_concurrent_jobs Default = num_cpus × 2 | Source Code / Research-Paper |
| 16 | Config-Pfad ~/.xearthlayer/config.ini | Mehrere Quellen |
| 17 | disk_io_profile: hdd/ssd/nvme/auto mit dokumentierten Werten | v0.2.7 Release Notes |
