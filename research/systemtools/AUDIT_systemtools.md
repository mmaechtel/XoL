# Audit: systemtools.md

| Feld | Wert |
|------|------|
| **Datei** | `docs/en/systemtools.md` |
| **Titel** | Linux System Tools |
| **Zeilen** | 422 |
| **Aufwand** | L |
| **Audit-Datum** | 2026-02-14 |
| **Gesamtbewertung** | B |

---

## Detail-Tabelle

| # | Zeile | Abschnitt | Behauptung | Typ | Bewertung | Quelle / Beleg | Empfehlung | Entscheidung |
|---|-------|-----------|------------|-----|-----------|----------------|------------|:------------:|
| 1 | 12 | Installation | `sysstat` enthält mpstat+iostat, `linux-cpupower` enthält cpupower+turbostat, `util-linux-extra` enthält lsirq | FAK | OK | Debian-Paketseiten bookworm/trixie bestätigen alle drei Zuordnungen | — | |
| 2 | 33 | htop | `H` = toggle user threads | FAK | OK | Man page: "Hide user threads: on systems that represent them differently than ordinary processes" | — | |
| 3 | 34 | htop | `t` = tree view | FAK | OK | Man page: "Tree view: organize processes by parenthood" (auch `F5`) | — | |
| 4 | 35 | htop | `P` = sort by CPU | FAK | OK | Man page: "Sort by processor usage (top compatibility key)" | — | |
| 5 | 36 | htop | `F4` = filter | FAK | OK | Man page: "Incremental process filtering" | — | |
| 6 | 38 | htop | PROCESSOR column shows last CPU core | FAK | OK | Man page: "PROCESSOR (CPU): The ID of the CPU the process last executed on." | — | |
| 7 | 50 | btop | `f` = filter, `t` = tree view, `p` = presets | FAK | **FAIL** | btop source (`btop_input.cpp`): Tree view ist `e`, nicht `t`. `key == "e"` triggert `Config::flip("proc_tree")`. Filter `f` und Presets `p` sind korrekt. | `t` → `e` ändern | |
| 8 | 60 | cpupower | `-p` zeigt Governor | FAK | WARN | Man page: `-p`/`--policy` zeigt "currently used cpufreq policy" — enthält Governor **und** Frequenzbereich. "Shows governor" ist vereinfacht. | Präzisieren: "shows active policy (governor and frequency range)" | |
| 9 | 74 | s-tui | Vier Graphen: frequency, utilization, temperature, power | FAK | OK | GitHub README: "monitors CPU temperature, frequency, power and utilization" | — | |
| 10 | 82 | s-tui | `stress-ng` für Stresstest | FAK | OK | Paket in Debian bookworm bestätigt (0.15.06-2) | — | |
| 11 | 95 | turbostat | `--show Core,CPU,Avg_MHz,Bzy_MHz,Busy%,IRQ,CoreTmp` | FAK | OK | Alle Spaltennamen in Man page dokumentiert | — | |
| 12 | 105 | turbostat | `Bzy_MHz` = Takt bei aktiven Phasen | FAK | OK | Man page: "average clock rate while CPU was not idle (ie. in 'c0' state)" | — | |
| 13 | 106 | turbostat | `Busy%` = Anteil in C0 | FAK | OK | Man page: "percent of measurement interval that CPU executes instructions" | — | |
| 14 | 107 | turbostat | `CPU%c1`–`CPU%c7` = C-State Residency | FAK | WARN | Man page listet `CPU%c1, CPU%c3, CPU%c6, CPU%c7` — kein durchgehender Bereich c1–c7. Verfügbare States sind hardware-abhängig. | Notation ändern: z.B. `CPU%c1, CPU%c3, …` oder Hinweis "verfügbare C-States hardware-abhängig" | |
| 15 | 108 | turbostat | `IRQ` = Interrupts pro Intervall und Core | FAK | OK | Man page: "number of interrupts serviced by that CPU during measurement interval" | — | |
| 16 | 111 | turbostat | AMD Zen: "limited functionality" | FAK | WARN | Man page sagt turbostat arbeitet auf "X86 processors" und erwähnt "some information not available on older processors". Formulierung "limited functionality" nicht aus offizieller Quelle. | Umformulieren: "works on AMD Zen; available columns depend on processor MSR support" | |
| 17 | 121 | mpstat | `-P ALL 1` = alle Cores, 1s-Intervall | FAK | OK | Man page bestätigt | — | |
| 18 | 123–124 | mpstat | `-I CPU 1` = "hardware interrupts per core per second" | FAK | WARN | Man page: "the number of each individual interrupt received per second by the CPU or CPUs" (Quelle: `/proc/interrupts`). Man page sagt nicht explizit "hardware". | "Hardware interrupts" → "interrupts" | |
| 19 | 127 | mpstat | `-A 1` = CPU + Interrupts + NUMA | FAK | OK | Man page: äquivalent zu `-n -u -I ALL -N ALL -P ALL` | — | |
| 20 | 130 | mpstat | `%irq` und `%soft` Spalten | FAK | OK | Man page definiert beide Spalten | — | |
| 21 | 144 | iotop | `-oPd 0.5` Flags | FAK | OK | Standard iotop-c Flags | — | |
| 22 | 156 | iostat | `-xdth -p nvme0n1 1` Flags | FAK | OK | Alle Flags dokumentiert: -x extended, -d device, -t timestamp, -h human-readable | — | |
| 23 | 163 | iostat | `r_await` = Ø Leselatenz (ms) | FAK | OK | Man page: "average time in ms for read requests to be served" | — | |
| 24 | 164 | iostat | `%util` = Geräteauslastung | FAK | OK | Man page bestätigt | — | |
| 25 | 165 | iostat | `aqu-sz` = Queue-Länge | FAK | OK | Man page: "average queue length of requests issued to device" | — | |
| 26 | 167 | iostat | NVMe APST-Signatur: 50–500 ms | FAK | OK | AnandTech gemessen: 44–371 ms; Microsoft APST-Schwellwerte: 50/500 ms. Bereich plausibel. | — | |
| 27 | 175 | ioping | `-c 20 -D /dev/nvme0n1` | FAK | OK | Man page bestätigt alle Flags | — | |
| 28 | 178 | ioping | `-c 50 -s 256k -D -L` | FAK | OK | `-L` setzt sequential + Default 256k; explizites `-s 256k` redundant aber nicht falsch | — | |
| 29 | 201 | nvme-cli | `nvme id-ctrl \| grep -A 5 "ps "` | FAK | OK | Output-Zeilen beginnen mit `ps  0 :`, Pattern matcht korrekt | — | |
| 30 | 204 | nvme-cli | Feature 0x0c = APST | FAK | OK | NVMe-Spec bestätigt (Autonomous Power State Transition) | — | |
| 31 | 207 | nvme-cli | Feature 0x02 = Power State | FAK | OK | NVMe-Spec bestätigt (Power Management) | — | |
| 32 | 243 | lsirq | `-s TOTAL` sortiert nach Gesamtzahl | FAK | OK | Lokal verifiziert: `lsirq --help` listet `TOTAL  total count` als verfügbare Spalte | — | |
| 33 | 246 | lsirq | `-C 0-3` zeigt bestimmte CPUs | FAK | OK | Man page: "-C, --cpu-list list" bestätigt | — | |
| 34 | 249 | lsirq | `-S` zeigt Softirqs | FAK | OK | Man page: "-S, --softirq" bestätigt | — | |
| 35 | 296 | glances | Web UI auf Port 61208 | FAK | OK | Glances-Docs bestätigen Default-Port 61208 | — | |
| 36 | 297 | glances | `-w` aktiviert Web-Modus | FAK | OK | Docs: "-w, --webserver" | — | |
| 37 | 300 | glances | `L` aktiviert Disk-IO-Latenz | FAK | WARN | Uppercase `L` = Disk-IO-Latenz (korrekt). Lowercase `l` = Log-Meldungen (andere Funktion). Groß-/Kleinschreibung entscheidend, im Text aber nicht explizit. | Großschreibung hervorheben: z.B. `` `Shift+L` `` oder `` `L` (uppercase) `` | |
| 38 | 314 | powertop | Idle Stats zeigt C-State-Residency | FAK | OK | Red Hat Docs bestätigen | — | |
| 39 | 315 | powertop | Frequency Stats Tab | FAK | OK | Bestätigt | — | |
| 40 | 316 | powertop | Device Stats Tab | FAK | OK | Bestätigt | — | |
| 41 | 320 | powertop | `--html=filename` | FAK | OK | Bestätigt | — | |
| 42 | 324 | powertop | `--auto-tune` Warnung | FAK | OK | Bestätigt; Warnung angemessen | — | |
| 43 | 347 | nmon | `-f -s 5 -c 720` | FAK | OK | Alle Flags bestätigt | — | |
| 44 | 365 | nmon | Dateiname `hostname_YYYYMMDD_HHMM.nmon` | FAK | OK | Lokal verifiziert: `nmon -h` zeigt `<hostname>_YYYYMMDD_HHMM.nmon` | — | |
| 45 | 365 | nmon | `nmonchart` für Visualisierung | FAK | OK | Bestätigt: konvertiert .nmon zu interaktiven HTML-Charts | — | |
| 46 | 375 | fatrace | `-tf R -C X-Plane` | FAK | WARN | Einzelflags korrekt (`-t` Timestamp, `-f R` Read-Filter, `-C X-Plane` Kommando). Kombinierte Form `-tf R` ist untypisch; sicherer: `-t -f R`. | Schreibweise ändern zu `-t -f R` für Klarheit | |
| 47 | 395 | perf | `perf sched record -- sleep 10` + `perf sched latency` | FAK | OK | Man page bestätigt Zwei-Schritt-Workflow | — | |
| 48 | 404 | trace-cmd | `trace-cmd record -p irqsoff sleep 10` | FAK | OK | `-p` akzeptiert Tracer-Plugin, `irqsoff` ist valider ftrace-Tracer | — | |

---

## Zusammenfassung Findings

| Bewertung | Anzahl |
|-----------|--------|
| OK | 42 |
| WARN | 5 |
| FAIL | 1 |
| N/V | 0 |

---

## FAIL-Findings

1. **#7 — btop Tree-View-Taste** (Zeile 50): Dokument sagt `t` für Tree View, tatsächlich ist es `e`. Belegt durch btop-Quellcode (`btop_input.cpp`): `key == "e"` triggert `Config::flip("proc_tree")`.

## WARN-Findings

1. **#8 — cpupower -p Beschreibung** (Zeile 60): Sagt "shows governor", aber `-p` zeigt die gesamte Policy (Governor + Frequenzbereich).
2. **#14 — turbostat C-State-Notation** (Zeile 107): `CPU%c1–CPU%c7` suggeriert durchgehenden Bereich; tatsächlich hardware-abhängig (Man page listet c1, c3, c6, c7).
3. **#16 — turbostat AMD "limited functionality"** (Zeile 111): Man page beschreibt turbostat für "X86 processors", nicht spezifisch "limited" für AMD.
4. **#18 — mpstat "hardware interrupts"** (Zeile 123–124): Man page sagt "each individual interrupt", nicht "hardware interrupts".
5. **#37 — glances `L` Groß-/Kleinschreibung** (Zeile 300): Großes `L` = Latenz, kleines `l` = Log. Unterscheidung fehlt im Text.
6. **#46 — fatrace `-tf R` Schreibweise** (Zeile 375): Kombinierte Kurzform untypisch; `-t -f R` ist klarer.

---

## Struktur-Review (Schritt 2)

| Aspekt | Bewertung | Anmerkung |
|--------|-----------|-----------|
| Fehlende Themen | OK | Alle relevanten Monitoring-Tools für System-Tuning-Verifikation abgedeckt. Keine kritischen Lücken. |
| Überflüssiges | OK | Gesamter Inhalt ist Linux-spezifische Tool-Nutzung. Nichts off-topic. |
| Zielgruppe | OK | Angemessener Detailgrad — Befehle mit Erklärung, nicht überladen. |
| Struktur | Gut | Klare H2-Abschnitte (CPU, IO, Interrupt, Dashboards), dann Szenario-Tabelle, dann Advanced. Logischer Aufbau. |
| Querverweise | OK | Verweise auf systemtuning.md-Abschnitte vorhanden und relevant. |
| Markdown/Format | 5 Fixes | Tabellen-Beschriftungen waren plain text statt **fett** (5× EN, 5× DE). Korrigiert. |

**Markdown-Check (MARKDOWN_RULES.txt)**

| Regel | Ergebnis |
|-------|----------|
| Leerzeile nach jeder Überschrift | OK — alle H1–H3 und **fett**-Labels korrekt |
| Kein Doppelpunkt vor Listen | OK — keine Verstöße |
| Listen-Einrückung 4 Spaces | OK — Advanced-Blöcke und Sources korrekt |
| Leerzeichen nach Doppelpunkten | OK — alle `**Label**: Text` korrekt |
| Code-Block-Tags (`bash`) | OK — alle Shell-Blöcke mit `bash` getaggt |
| Konsistenz DE/EN | OK — identische Struktur |
| **Tabellen-Beschriftungen** | **5 Fixes** — plain text → **fett**: "Key hotkeys", "Key columns" (2×), "Key fields", "Relevant tabs" (EN+DE je 5) |

**Strukturelle Stärken:**

- Die Szenario-Tabelle (Zeile 332–347) ist ein Highlight — schneller Lookup für den Leser
- Advanced-Tools in klappbaren Blöcken (nmon, fatrace, perf) ist gute Praxis
- Quellenabschnitt am Ende vorhanden
- Cross-References zu systemtuning.md konsequent durchgehalten

---

## Quellen

- [htop(1) Man page](https://www.man7.org/linux/man-pages/man1/htop.1.html)
- [btop Quellcode btop_input.cpp](https://github.com/aristocratos/btop/blob/main/src/btop_input.cpp)
- [cpupower-frequency-info(1) Debian Man page](https://manpages.debian.org/experimental/linux-cpupower/cpupower-frequency-info.1.en.html)
- [s-tui GitHub](https://github.com/amanusk/s-tui)
- [turbostat(8) Debian Man page](https://manpages.debian.org/testing/linux-cpupower/turbostat.8.en.html)
- [mpstat(1) Man page](https://man7.org/linux/man-pages/man1/mpstat.1.html)
- [iostat(1) Man page](https://www.man7.org/linux/man-pages/man1/iostat.1.html)
- [ioping GitHub + Man page](https://github.com/koct9i/ioping)
- [Arch Wiki NVMe](https://wiki.archlinux.org/title/Solid_state_drive/NVMe)
- [AnandTech 2021 SSD Benchmark — Power Management](https://www.anandtech.com/show/16458/2021-ssd-benchmark-suite/6)
- [Glances Docs](https://glances.readthedocs.io/en/latest/)
- [Red Hat PowerTOP Docs](https://docs.redhat.com/en/documentation/red_hat_enterprise_linux/9/html/monitoring_and_managing_system_status_and_performance/managing-power-consumption-with-powertop_monitoring-and-managing-system-status-and-performance)
- [lsirq(1) Man page](https://www.man7.org/linux/man-pages/man1/lsirq.1.html)
- [fatrace Debian Man page](https://manpages.debian.org/testing/fatrace/fatrace.8.en.html)
- [perf-sched(1) Man page](https://www.man7.org/linux/man-pages/man1/perf-sched.1.html)
- [trace-cmd-record(1) Man page](https://man7.org/linux/man-pages/man1/trace-cmd-record.1.html)
- Lokale Verifikation: `lsirq --help`, `nmon -h` auf Debian Liquorix 6.18
