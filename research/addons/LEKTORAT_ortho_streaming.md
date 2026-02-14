# Lektorat: Ortho-Streaming-Lösungen (AutoOrtho Fork, XEarthLayer, XPME)

**Datum:** 2026-02-14
**Bezug:** Research-Papers `autoortho4xplane_fork.md`, `xearthlayer_current_state.md`, `XPME_research.md`
**Betroffene Docs-Seiten:** `addon/autoortho.md`, `addon/xearthlayer.md`, `addon/orthophotography_intro.md`

---

## 1. Informationsbewertung

### 1.1 AutoOrtho (ProgrammingDinosaur Fork)

| Information | Relevanz | Mehrwert | Haltbarkeit | Empfehlung |
|---|---|---|---|---|
| C-Pipeline (Architektur, 4 Modi) | Hoch | Hoch — erklärt Performance-Unterschied | Mittel — Modi könnten sich ändern | **Aufnehmen** (ohne spezifische Speedup-Zahlen) |
| Performance-Tuning (Time Budget, Fallback, Pre-Fetch) | Hoch | Hoch — direkt anwendbar | Mittel — Parameter-Namen stabil, Defaults variabel | **Aufnehmen** (mit Hinweis "Defaults können sich ändern") |
| SimBrief-Integration | Hoch | Hoch — Alleinstellungsmerkmal, praktisch nutzbar | Gut — Feature ist stabil seit v1.6 | **Aufnehmen** |
| Seasons-Feature | Mittel | Mittel — interessant aber nicht Linux-spezifisch | Gut | **Aufnehmen** (kurz, nicht im Detail) |
| Dynamic Zoom Levels | Mittel | Mittel — automatisch, wenig Konfigurationsbedarf | Gut | **Aufnehmen** (kurz) |
| .aob2 Cache-Format | Mittel | Mittel — erklärt Cache-Verhalten | Gut | **Aufnehmen** (kurz, im Cache-Abschnitt) |
| Linux-Binaries (Jammy/Noble) | Hoch | Hoch — direkt relevant für Debian-Nutzer | Mittel — Builds ändern sich mit Ubuntu-Releases | **Aufnehmen** (ohne Versionsnummern der Binaries) |
| FUSE-Troubleshooting (user_allow_other, ulimit, stale mounts) | Hoch | Hoch — löst häufige Linux-Probleme | Gut — FUSE-Konfiguration ist stabil | **Aufnehmen** |
| Release-Timeline (83 Releases in 6 Monaten) | Niedrig | Niedrig — veraltet schnell | Schlecht | **Weglassen** |
| Offene Issues (RAM, Stuttering) | Niedrig | Niedrig — zu volatil | Schlecht | **Weglassen** (allgemeiner Hinweis reicht) |
| Detaillierte Pipeline-Performance-Zahlen (10x, 8x, 12x) | Niedrig | Niedrig — Marketing-Zahlen, nicht verifizierbar | Schlecht | **Weglassen** |
| Map-Provider-Liste (alle 5) | Mittel | Mittel — schon vorhanden, nur aktualisieren | Gut | **Aktualisieren** |
| Python-Version/PyInstaller-Details | Niedrig | Niedrig — Implementierungsdetail | Schlecht | **Weglassen** |
| GUI-Details (PyQt6, Tabs) | Niedrig | Niedrig — UI ändert sich | Schlecht | **Weglassen** |

### 1.2 XEarthLayer

| Information | Relevanz | Mehrwert | Haltbarkeit | Empfehlung |
|---|---|---|---|---|
| Adaptive Prefetch (Ground/Cruise, Self-Calibration) | Hoch | Hoch — erklärt Kernarchitektur | Gut — Design-Entscheidung, nicht versionsspezifisch | **Aktualisieren** (v0.3.0-Rewrite erwähnen) |
| Job Executor Framework | Niedrig | Niedrig — internes Implementierungsdetail | Mittel | **Weglassen** (nur indirekt über Priority-System) |
| Circuit Breaker | Mittel | Mittel — erklärt Verhalten bei Last | Gut | **Aufnehmen** (kurz, im Prefetch-Abschnitt) |
| ForeFlight-Telemetrie Setup | Hoch | Hoch — nötig für Kernfeature | Gut | **Beibehalten** (bereits vorhanden, ggf. ergänzen) |
| CLI-Befehle (erweitert) | Mittel | Mittel — Referenz für Nutzer | Mittel — Befehle können sich ändern | **Aufnehmen** (selektiv: die wichtigsten) |
| Tile Patches | Mittel | Mittel — nützlich für Airport-Addon-Nutzer | Gut | **Aufnehmen** (kurz) |
| Dashboard-Beschreibung | Niedrig | Niedrig — UI-Detail | Schlecht | **Weglassen** |
| Resource Pool Architektur (3 Ebenen) | Niedrig | Niedrig — zu technisch | Mittel | **Weglassen** (CPU-Tuning-Tabelle reicht) |
| 800 vs. 500 Mbps Inkonsistenz | Mittel | Mittel — aktuell irreführend | — | **Korrigieren** (Website-Tabelle als Referenz, 500 Mbps recommended) |
| Regionale Pakete (erweiterte Liste) | Mittel | Mittel — Abdeckungsinformation | Mittel | **Aktualisieren** |
| Disk I/O Auto-Detection | Mittel | Mittel — bereits dokumentiert | Gut | **Beibehalten** |

### 1.3 XPME

| Information | Relevanz | Mehrwert | Haltbarkeit | Empfehlung |
|---|---|---|---|---|
| Linux-Support existiert (seit Feb 2026) | Hoch | Hoch — Neuigkeit für XoL-Leser | Schlecht — Status ändert sich schnell | **Aufnehmen** (als Beta-Hinweis in Intro-Seite) |
| .NET 10.0 Abhängigkeit | Hoch | Hoch — Showstopper für viele Linux-Nutzer | Mittel — wird sich ändern wenn .NET LTS kommt | **Aufnehmen** (als Warnung) |
| Seasons + Nachttexturen | Mittel | Mittel — Alleinstellungsmerkmale | Gut | **Erwähnen** (in Intro-Vergleich) |
| Freemium-Modell (30 USD/Jahr) | Mittel | Mittel — Unterscheidungsmerkmal | Gut | **Erwähnen** |
| VHD-Architektur | Niedrig | Niedrig — Implementierungsdetail | Mittel | **Weglassen** |
| Detaillierte Installationsanleitung | Niedrig | Niedrig — zu früh, ändert sich schnell | Schlecht | **Weglassen** (auf offizielle Docs verweisen) |
| Ortho4XP-Konflikt | Mittel | Mittel — wichtig für bestehende Nutzer | Gut | **Erwähnen** (in Intro oder static_plus_streaming) |
| Eigene Docs-Seite für XPME | — | — | — | **Noch nicht** — Linux-Support zu jung |

---

## 2. Strukturvorschlag

### 2.1 autoortho.md — Überarbeitung (Gewichtung)

| Abschnitt | Gewichtung | Format | Anmerkung |
|---|---|---|---|
| How It Works | 15% | Fließtext | Kürzen, Fork-Abschnitt integrieren |
| Installation (Binary + Source) | 25% | Schritte + Code-Blöcke | Linux-Binary als Primärweg, Source als Alternative |
| FUSE-Konfiguration (Linux) | 15% | Code-Blöcke + Admonition | Neuer Abschnitt, löst häufige Probleme |
| Performance-Tuning | 20% | Tabellen + Code-Blöcke | Neuer Abschnitt mit den wichtigsten Parametern |
| Features (SimBrief, Seasons, Dynamic Zoom) | 10% | Kurz-Beschreibungen | Neuer Abschnitt |
| Vergleich mit Ortho4XP | 10% | Tabelle | Aktualisieren |
| Troubleshooting | 5% | Liste | Kürzen, auf offizielle Docs verweisen |

**Tonalität:** Technisch-sachlich. Die bestehende Seite ist stellenweise zu ausführlich bei Grundlagen und zu dünn bei Linux-Spezifika. Umkehren: weniger "wie Streaming funktioniert", mehr "wie man es unter Linux optimal betreibt".

**Kernänderungen:**
- "Enhanced Features of the Fork" Abschnitt auflösen — der Fork IST jetzt AutoOrtho
- Kubilus1-Referenzen in die Geschichte verschieben, nicht prominent halten
- Linux-Binary-Installation als primärer Installationsweg
- Source-Installation als klappbaren Block
- Performance-Tuning als eigenständigen Abschnitt
- FUSE-Konfiguration als eigenständigen Abschnitt

### 2.2 xearthlayer.md — Aktualisierung (Gewichtung)

| Abschnitt | Gewichtung | Format | Anmerkung |
|---|---|---|---|
| How It Works + Prefetch | 20% | Fließtext | Adaptive Prefetch aktualisieren |
| Installation + Setup | 20% | Code-Blöcke | Beibehalten, Versionsnummern entfernen |
| CLI-Referenz | 15% | Tabelle/Code | Erweitern (packages, config, diagnostics) |
| CPU Tuning | 20% | Tabellen + ini-Beispiel | Beibehalten |
| Tile Patches | 5% | Kurz | Neu |
| Vergleich mit AutoOrtho | 10% | Tabelle | Aktualisieren |
| Troubleshooting | 10% | Liste | Neu (Magenta Tiles, weiße Tiles) |

### 2.3 orthophotography_intro.md — Minimale Aktualisierung

- XPME-Erwähnung um Beta-Status und Einschränkungen ergänzen
- Vergleichstabelle aller drei Streaming-Lösungen erwägen (optional)

### 2.4 static_plus_streaming.md — Keine Änderung nötig

Die Seite ist generisch genug formuliert ("other streaming solutions").

---

## 3. Versionsspezifische Inhalte

| Information | Versionsbindung | Empfehlung |
|---|---|---|
| AutoOrtho "Version 2.0" | Stark — wird bald 2.x.y | Meta-Formulierung: "aktuelle Versionen bieten eine C-Pipeline" |
| XEarthLayer "v0.3.0" | Stark | Keine Versionsnummer in der Doku, stattdessen Feature-basiert beschreiben |
| AutoOrtho Jammy/Noble Builds | Mittel — Ubuntu-Versionen | "Binaries für gängige Ubuntu-Versionen" |
| XPME ".NET 10.0" | Stark — wird sich ändern | Erwähnen mit Hinweis "erfordert aktuell .NET 10.0 (Preview)" |
| CPU-Tuning-Defaults (num_cpus × 1.25) | Mittel | Defaults als "zum Zeitpunkt der Dokumentation" kennzeichnen |

---

## 4. Quellen-Qualität

| Quelle | Bewertung | Anmerkung |
|---|---|---|
| GitHub Releases (AutoOrtho) | Belastbar | Primärquelle, 83 Releases dokumentiert |
| AutoOrtho Docs-Site | Belastbar | Offizielle Dokumentation, aktuell gepflegt |
| XEarthLayer GitHub | Belastbar | Primärquelle, Release Notes detailliert |
| xearthlayer.app | Belastbar | Offizielle Website, gut strukturiert |
| XPME GitHub (Release-Repo) | Eingeschränkt | Nur Binaries, kein Source, Issues geben Einblick |
| XPME aiflygo.com | Eingeschränkt | Offizielle Seite, aber Installationsanleitung für Linux dünn |
| X-Plane.org Forum-Threads | Ergänzend | Nutzererfahrungen, nicht als Faktenquelle |
| Performance-Vergleiche (Forum) | Nicht belastbar | Subjektiv, Windows-basiert, keine Benchmarks |

### Markierung für Faktencheck

- [ ] AutoOrtho: "user_allow_other" in /etc/fuse.conf ist Pflicht — verifizieren
- [ ] AutoOrtho: ulimit 8192 Empfehlung — Quelle prüfen
- [ ] XEarthLayer: 500 Mbps vs. 800 Mbps — aktuellen Stand der Website prüfen
- [ ] XPME: .NET 10.0 auf Debian 12 über Microsoft-Repo — funktioniert das aktuell?
- [ ] XPME: AppImage benötigt --no-sandbox — verifizieren

---

## 5. Nicht übernommene Research-Ergebnisse

| Information | Grund |
|---|---|
| AutoOrtho komplette Release-Timeline | Zu volatil, kein Mehrwert für Leser |
| AutoOrtho offene Issues (RAM, Stuttering) | Versionsspezifisch, ändert sich wöchentlich |
| AutoOrtho GUI-Details (PyQt6, Tabs) | UI-Detail, ändert sich |
| AutoOrtho Python 3.14 / PyInstaller-Interna | Implementierungsdetail |
| XEarthLayer Job Executor Framework Interna | Zu technisch für Doku-Zielgruppe |
| XEarthLayer Resource Pool Architektur | Zu technisch, CPU-Tuning-Tabelle reicht |
| XEarthLayer Repository-Statistiken (Stars, Forks) | Veraltet schnell |
| XPME detaillierte Installationsanleitung | Zu früh, ändert sich schnell |
| XPME VHD-Architekturdetails | Implementierungsdetail |
| XPME Lizenzdetails (nicht übertragbar, Hardware-Bindung) | Für XoL nicht relevant |
| XPME MSFS-Unterstützung | Für XoL irrelevant |
| Formale Benchmark-Vergleiche | Existieren nicht — keine unbelegten Claims aufstellen |

---

## 6. Zusammenfassung

### Empfohlene Maßnahmen

1. **autoortho.md** — Substantielle Überarbeitung: Fork als Standard behandeln, Linux-Binary-Installation, FUSE-Config, Performance-Tuning, neue Features (SimBrief, Seasons, Dynamic Zoom)
2. **xearthlayer.md** — Moderate Aktualisierung: Prefetch-System aktualisieren, CLI erweitern, Tile Patches, Troubleshooting ergänzen
3. **orthophotography_intro.md** — Minimale Aktualisierung: XPME Beta-Status und Einschränkungen
4. **XPME eigene Seite** — Nicht jetzt. Erst wenn Linux-Support stabil (>= 3 Monate, Debian-Tests vorhanden)

### Aufwand

- autoortho.md: **L** (große Umstrukturierung)
- xearthlayer.md: **M** (gezielte Ergänzungen)
- orthophotography_intro.md: **S** (wenige Zeilen)
