# CPU-Monitoring-Tools fur Linux — Research Paper

Recherche-Datum: 2026-02-09
Zielseite: `systemtools.md` (TODO-Eintrag 1c)
Fokus: Tools zur CPU-Lastanalyse, Per-Core-Auslastung, Frequenzskalierung und Scheduling-Verhalten wahrend X-Plane lauft.

---

## Ubersicht

| Tool | Paket (Debian Bookworm) | Typ | Per-Core | Frequenz | Root notig |
|------|------------------------|-----|----------|----------|------------|
| htop | `htop` (3.2.2) | Interaktiver Prozess-Viewer | Ja (Balken) | Nein | Nein |
| btop | `btop` (1.2.13) | Moderner System-Monitor | Ja (Graphen) | Nur gesamt | Nein |
| mpstat | `sysstat` (12.6.1) | Per-CPU-Statistiken (CLI) | Ja (Zahlen) | Nein | Nein |
| turbostat | `linux-cpupower` (6.1.x) | CPU-Frequenz/C-States/Power | Ja | Ja (pro Core) | Ja |
| cpupower | `linux-cpupower` (6.1.x) | Governor-Info/Frequenz | Ja (mit -c) | Ja | Teilweise |

---

## 1. htop — Interaktiver Prozess-Viewer

### Quelle

- GitHub: [htop-dev/htop](https://github.com/htop-dev/htop)
- Manpage: [htop(1) Debian Bookworm](https://manpages.debian.org/bookworm/htop/htop.1.en.html)
- Paket: [packages.debian.org/bookworm/htop](https://packages.debian.org/bookworm/htop)

### Installation

```bash
sudo apt install htop
```

### Was es zeigt

- **CPU-Auslastung pro Core** als farbige Balken im Header (user/system/nice/irq/softirq/steal/guest/iowait)
- **Prozessliste** mit PID, User, CPU%, MEM%, Kommandozeile
- **Load Average**, Uptime, Speicher/Swap
- **CPU-Temperatur** (wenn libsensors verfugbar und in Setup aktiviert)
- **Prozess-Baum** (Eltern-Kind-Beziehungen)

### Per-Core-Daten

Ja. Der Header zeigt standardmasig einen Balken pro logischem CPU-Kern. Die Farben unterscheiden User (grun), System (rot), Nice (blau/cyan), IRQ (gelb/Baumharz). Im Setup (F2) kann die Darstellung angepasst werden (Balken, Text, Graph).

### Relevante Flags fur X-Plane-Analyse

| Flag | Zweck |
|------|-------|
| `-d 5` | Update-Intervall auf 0.5s (Einheit: Zehntelsekunden) |
| `-t` | Baumansicht — zeigt X-Plane-Kindprozesse/Threads |
| `-p PID` | Nur bestimmte PIDs anzeigen |
| `-u USER` | Nur Prozesse eines Users |
| `-s COLUMN` | Sortierung (z.B. `-s PERCENT_CPU`) |
| `-H` | Versteckte User-Threads anzeigen |

### Interaktive Bedienung (wahrend X-Plane lauft)

- `F2` — Setup: CPU-Meter-Darstellung konfigurieren
- `F5` / `t` — Baumansicht ein/aus
- `F4` / `\` — Filter (z.B. "X-Plane")
- `F6` / `<` / `>` — Sortierung andern
- `P` — Nach CPU-Verbrauch sortieren
- `H` — User-Threads ein/ausblenden (wichtig: X-Plane nutzt viele Threads)

### Spalte PROCESSOR (CPU)

Zeigt, auf welchem CPU-Kern ein Prozess zuletzt ausgefuhrt wurde. Nutzlich um zu prufen, ob Interrupt-Shielding (IRQ-Affinitat) funktioniert.

### Limitierungen

- **Keine CPU-Frequenz-Anzeige** — zeigt weder aktuelle Taktrate noch Governor
- **Keine C-State-Informationen**
- **Keine Power-Daten**
- Zeigt Auslastung, aber nicht *warum* ein Core busy ist (keine IRQ-Aufschlusselung pro Core)

### Starke

Beste Wahl fur schnellen visuellen Uberblick: welcher Core ist unter Last, auf welchem Core lauft X-Plane, welche Threads verbrauchen CPU. Minimaler Overhead.

---

## 2. btop — Moderner System-Monitor

### Quelle

- GitHub: [aristocratos/btop](https://github.com/aristocratos/btop)
- Paket: [packages.debian.org/bookworm/btop](https://packages.debian.org/bookworm/btop)
- Feature-Request Per-Core-Frequenz: [Issue #190](https://github.com/aristocratos/btop/issues/190) (offen, Stand 2026)

### Installation

```bash
sudo apt install btop
```

### Was es zeigt

- **CPU-Auslastung pro Core** als Graphen (Zeitverlauf)
- **Gesamte CPU-Frequenz** (einzelner Wert, nicht pro Core)
- **Speicher, Swap, Disk-I/O, Netzwerk** in einem Dashboard
- **Prozessliste** mit Filterung und Baumansicht
- **GPU-Monitoring** (NVIDIA, AMD, Intel) — separates Feature
- **Detailansicht** fur ausgewahlte Prozesse

### Per-Core-Daten

Ja, fur Auslastung. Jeder logische Core bekommt einen eigenen Graphen mit Zeitverlauf. **CPU-Frequenz wird nur als Gesamtwert angezeigt** — per-Core-Frequenz ist ein offener Feature-Request (Issue #190, seit 2021 offen). In Version 1.4.6 wurden "CPU frequency display modes" eingefuhrt (PR #1277), aber dies betrifft die Darstellungsart, nicht per-Core-Granularitat.

### Relevante Flags

| Flag | Zweck |
|------|-------|
| `-t` / `--tty_on` | TTY-Modus fur einfache Terminals |
| `--utf-force` | UTF-8 erzwingen |
| `--update 500` | Update-Intervall in ms |

### Interaktive Bedienung

- Volle Maus-Unterstutzung
- Pfeiltasten zur Prozessauswahl
- `f` — Filter Prozesse
- `t` — Baumansicht
- `Esc` — Menu
- Presets: `p` wechselt zwischen vordefinierten Layouts

### Limitierungen

- **Keine Per-Core-Frequenz** (nur Gesamtwert)
- **Keine C-State-Informationen**
- **Keine IRQ-Statistiken**
- **Hohere Ressourcennutzung** als htop (Graphen-Rendering)
- Debian Bookworm-Version (1.2.13) ist deutlich alter als upstream; einige neuere Features fehlen

### Starke

Bester visueller Gesamtuberblick mit Zeitverlaufs-Graphen. Zeigt CPU, RAM, Disk, Netzwerk gleichzeitig. Gut um Korrelationen zu erkennen (z.B. CPU-Last + Disk-I/O wahrend Szenerie-Laden). Maus-Unterstutzung macht Prozess-Inspektion einfacher als in htop.

---

## 3. mpstat — Per-CPU-Statistiken

### Quelle

- GitHub: [sysstat/sysstat](https://github.com/sysstat/sysstat)
- Manpage: [mpstat(1) Debian Bookworm](https://manpages.debian.org/bookworm/sysstat/mpstat.1.en.html)
- Paket: [packages.debian.org/bookworm/sysstat](https://packages.debian.org/bookworm/sysstat)

### Installation

```bash
sudo apt install sysstat
```

### Was es zeigt

Tabellarische Per-CPU-Statistiken, aufgeschlusselt in:

| Spalte | Bedeutung |
|--------|-----------|
| `%usr` | User-Space CPU-Zeit |
| `%nice` | Nice-Prozesse |
| `%sys` | Kernel-Zeit |
| `%iowait` | Warten auf I/O |
| `%irq` | Hardware-Interrupts |
| `%soft` | Software-Interrupts (Softirqs) |
| `%steal` | Gestohlene Zeit (VM) |
| `%guest` | Gast-VM-Zeit |
| `%idle` | Leerlauf |

### Per-Core-Daten

Ja — das ist der Hauptzweck. `-P ALL` zeigt jeden einzelnen logischen CPU-Kern separat. Unterstutzt auch NUMA-Node-Gruppierung (`-n`, `-N`).

### Relevante Flags fur X-Plane-Analyse

| Befehl | Zweck |
|--------|-------|
| `mpstat -P ALL 1` | Alle Cores, 1-Sekunden-Intervall, fortlaufend |
| `mpstat -P ALL 2 5` | Alle Cores, 2s-Intervall, 5 Messungen |
| `mpstat -P 0,2,4-7 1` | Nur bestimmte Cores (z.B. nicht-isolierte) |
| `mpstat -I ALL 1` | Interrupt-Statistiken pro CPU |
| `mpstat -T -P ALL 1` | Mit Topologie-Info (Core, Socket, NUMA Node) |
| `mpstat -A 1` | Alles: CPU + Interrupts + NUMA |
| `mpstat -o JSON -P ALL 1` | JSON-Ausgabe (fur Scripting) |

### Interrupt-Monitoring (`-I`)

Besonders relevant fur Interrupt-Shielding-Verifikation:

- `mpstat -I CPU 1` — Interrupts pro CPU pro Sekunde (Hardware)
- `mpstat -I SCPU 1` — Software-Interrupts pro CPU
- `mpstat -I SUM 1` — Summe aller Interrupts pro CPU

Damit lasst sich prufen, ob `irqbalance` die Gaming-Cores tatsachlich in Ruhe lasst.

### Limitierungen

- **Keine interaktive Oberflache** — rein textbasiert, keine Graphen
- **Keine CPU-Frequenz-Daten**
- **Keine Prozess-Information** — zeigt nur Core-Statistiken, nicht welcher Prozess die Last erzeugt
- **Keine C-State oder Power-Daten**

### Starke

Praziseste Per-Core-Aufschlusselung aller genannten Tools. Einziges Tool das **Hardware-IRQs und Softirqs pro Core** zeigt — unverzichtbar fur Interrupt-Shielding-Verifikation. Minimaler Overhead, gut fur gleichzeitiges Monitoring neben X-Plane. JSON-Output ermoglicht automatisierte Auswertung.

---

## 4. turbostat — CPU-Frequenz, C-States und Power

### Quelle

- Manpage: [turbostat(8) Debian Bookworm](https://manpages.debian.org/bookworm/linux-cpupower/turbostat.8.en.html)
- Kernel-Source: [torvalds/linux — tools/power/x86/turbostat](https://github.com/torvalds/linux/blob/master/tools/power/x86/turbostat/turbostat.c)
- Arch Wiki: [CPU frequency scaling](https://wiki.archlinux.org/title/CPU_frequency_scaling)

### Installation

```bash
sudo apt install linux-cpupower
```

Binary liegt in `/usr/sbin/turbostat`.

### Was es zeigt

| Spalte | Bedeutung |
|--------|-----------|
| `Core` | Physischer Core |
| `CPU` | Logischer CPU (Thread) |
| `Avg_MHz` | Durchschnittliche Taktrate inkl. Idle-Zeit |
| `Busy%` | Anteil der Zeit im C0-Zustand (aktiv) |
| `Bzy_MHz` | Taktrate wahrend aktiver Phasen (C0) |
| `TSC_MHz` | Time Stamp Counter Frequenz |
| `CPU%c1` - `CPU%c7` | Hardware-C-State-Residency pro Core |
| `CoreTmp` | Core-Temperatur |
| `PkgTmp` | Package-Temperatur |
| `PkgWatt` | Package-Leistungsaufnahme |
| `CorWatt` | Core-Leistungsaufnahme |
| `GFXWatt` | GPU-Leistungsaufnahme (integriert) |
| `IRQ` | Interrupts pro Intervall |

### Per-Core-Daten

Ja — turbostat zeigt standardmasig pro logischem CPU, pro physischem Core und pro Package. Mit `--cpu` kann die Ausgabe gefiltert werden:

- `--cpu core` — ein Eintrag pro physischem Core
- `--cpu package` — ein Eintrag pro Socket
- `--cpu 0-7` — nur bestimmte CPUs

### Relevante Befehle fur X-Plane-Analyse

```bash
# Standard: alle Cores, 5-Sekunden-Intervall
sudo turbostat

# Kurzerer Intervall, nur Frequenz und C-States
sudo turbostat --interval 2

# Nur bestimmte Spalten anzeigen
sudo turbostat --show Core,CPU,Avg_MHz,Busy%,Bzy_MHz,IRQ,CoreTmp

# Wahrend X-Plane lauft — Frequenz pro Core uberwachen
sudo turbostat --interval 1 --show Core,CPU,Avg_MHz,Bzy_MHz,Busy%

# Energieverbrauch in Joule statt Watt
sudo turbostat --Joules

# Ausgabe in Datei (fur spatere Analyse)
sudo turbostat --interval 2 --out turbostat_xplane.log

# Nur bestimmte Cores (z.B. die X-Plane-Cores)
sudo turbostat --cpu 0-7 --interval 1

# Einmalige Messung wahrend eines Befehls
sudo turbostat -- sleep 10
```

### AMD-Unterstutzung

turbostat unterstutzt AMD-Prozessoren mit Einschrankungen:

- **AMD Zen/Zen2/Zen3+**: Grundlegende Frequenz- und C-State-Daten funktionieren seit Kernel 5.13+ (Fix fur MSR_PKG_ENERGY_STAT auf AMD Family 17h)
- **RAPL-Power-Daten**: Funktionieren auf neueren AMD-Chips (Zen 2+)
- **Einschrankung**: Einige Intel-spezifische Spalten (z.B. bestimmte Package-C-States) sind auf AMD nicht verfugbar
- turbostat wurde primar fur Intel entwickelt; AMD-Support wird kontinuierlich verbessert

### Root-Zugriff

**Ja, zwingend erforderlich.** turbostat benotigt `cap_sys_admin`, `cap_sys_rawio` und `cap_sys_nice`, oder root-Rechte. Liest hardware-nahe MSR-Register und `/dev/cpu/*/msr`.

### Limitierungen

- **Root erforderlich**
- **x86-only** — kein ARM-Support
- **Keine Prozess-Information** — zeigt CPU-Metriken, nicht welcher Prozess aktiv ist
- **AMD-Support eingeschrankt** — nicht alle Spalten verfugbar
- **Nicht interaktiv** — reine Textausgabe, keine Filterung

### Starke

Einziges Tool das **echte Hardware-Frequenzen pro Core** zeigt (Bzy_MHz), nicht nur was der Governor meldet. Zeigt ob Turbo Boost/Precision Boost tatsachlich greift. C-State-Residency zeigt ob Cores tief schlafen oder ob Interrupts sie wach halten — direkte Relevanz fur Interrupt-Shielding und Latenz-Tuning.

---

## 5. cpupower — Governor und Frequenz-Info

### Quelle

- Manpage: [cpupower(1)](https://manpages.debian.org/bookworm/linux-cpupower/cpupower.1.en.html), [cpupower-frequency-info(1)](https://manpages.debian.org/bookworm/linux-cpupower/cpupower-frequency-info.1.en.html), [cpupower-monitor(1)](https://manpages.debian.org/bookworm/linux-cpupower/cpupower-monitor.1.en.html)
- Arch Wiki: [CPU frequency scaling](https://wiki.archlinux.org/title/CPU_frequency_scaling)
- Paket: [packages.debian.org/bookworm/linux-cpupower](https://packages.debian.org/bookworm/linux-cpupower)

### Installation

```bash
sudo apt install linux-cpupower
```

Binary liegt in `/usr/bin/cpupower`.

### Subkommandos

| Subkommando | Zweck |
|-------------|-------|
| `frequency-info` | Aktueller Governor, Frequenz, Treiber, Limits |
| `frequency-set` | Governor oder Frequenz andern |
| `monitor` | Echtzeit-Monitoring (Frequenz, C-States) |
| `info` | Allgemeine CPU-Power-Infos |
| `idle-info` | C-State-Informationen |
| `idle-set` | C-States aktivieren/deaktivieren |
| `set` | Energy Performance Bias setzen |

### Relevante Befehle fur X-Plane-Analyse

```bash
# Aktuellen Governor und Frequenz aller Cores anzeigen
cpupower frequency-info

# Governor und Treiber pro Core
cpupower -c all frequency-info -p

# Nur aktuelle Frequenz
cpupower frequency-info -f

# Hardware-Frequenz (root erforderlich)
sudo cpupower frequency-info -w

# Frequenzgrenzen (min/max)
cpupower frequency-info -l

# Verfugbare Governors
cpupower frequency-info -g

# Aktiver cpufreq-Treiber
cpupower frequency-info -d

# Frequenz eines bestimmten Cores
cpupower -c 4 frequency-info -f

# Echtzeit-Monitoring mit cpupower monitor
sudo cpupower monitor

# Verfugbare Monitor-Module auflisten
cpupower monitor -l

# Governor setzen (z.B. performance fur Gaming)
sudo cpupower frequency-set -g performance

# Governor nur fur bestimmte Cores
sudo cpupower -c 0-7 frequency-set -g performance
```

### cpupower monitor — Echtzeit-Uberwachung

`cpupower monitor` liefert ahnliche Daten wie turbostat, aber uber das cpufreq-Subsystem:

- **Mperf-Monitor**: Durchschnittsfrequenz, C0/Cx-Residency (auf modernen x86)
- **Idle_Stats**: Kernel-cpuidle-Daten (Software-C-States)
- **Architektur-spezifisch**: Nehalem/SandyBridge/Haswell (Intel), Fam_12h/Fam_14h (AMD)

Hierarchie-Level der Counter: Thread [T], Core [C], Package [P], Machine [M].

### Per-Core-Daten

Ja, mit `-c` Flag:

- `cpupower -c all frequency-info` — alle Cores
- `cpupower -c 0,1 frequency-info` — Core 0 und 1
- `cpupower -c 0-3 frequency-info` — Core 0 bis 3
- `cpupower -c 0-7:2 frequency-info` — Cores 0, 2, 4, 6 (Stride)

### Root-Zugriff

- **frequency-info**: Meist ohne root, auder `-w` (Hardware-Frequenz)
- **frequency-set**: Root erforderlich
- **monitor**: Root erforderlich (MSR-Zugriff)
- **idle-set/idle-info**: Root erforderlich

### Limitierungen

- **Kein kontinuierliches Live-Monitoring** bei frequency-info — Snapshot-basiert
- **cpupower monitor** braucht Root
- **Keine Prozess-Zuordnung** — zeigt nur CPU-Metriken
- **Keine interaktive Oberflache**

### Starke

Einziges Tool das **Governor-Konfiguration anzeigen UND andern** kann. Essentiell um zu prufen ob der richtige Governor aktiv ist (z.B. `performance` fur Gaming-Profil). `cpupower monitor` ist eine leichtgewichtige Alternative zu turbostat fur Frequenz-Monitoring.

---

## Vergleichsmatrix: Welches Tool wofur?

| Anwendungsfall | Bestes Tool | Alternative |
|----------------|-------------|-------------|
| "Welcher Core ist unter Last?" | htop (visuell) | btop (Graphen) |
| "Auf welchem Core lauft X-Plane?" | htop (PROCESSOR-Spalte) | — |
| "Funktioniert Interrupt-Shielding?" | mpstat -I ALL | turbostat (IRQ-Spalte) |
| "Lauft der Turbo Boost?" | turbostat (Bzy_MHz) | cpupower frequency-info -w |
| "Welcher Governor ist aktiv?" | cpupower frequency-info | — |
| "Wie viel Power verbraucht die CPU?" | turbostat (PkgWatt) | — |
| "Schlafen die Idle-Cores tief genug?" | turbostat (C-States) | cpupower monitor |
| "CPU + RAM + Disk gleichzeitig?" | btop | — |
| "IRQs pro Core aufschlusseln" | mpstat -I CPU | — |
| "Skriptbare Ausgabe" | mpstat -o JSON | turbostat --out |

---

## Empfohlene Kombination fur X-Plane Performance-Analyse

### Quick Check (kein root)

```bash
# Terminal 1: CPU-Auslastung pro Core + Prozesse
htop -t -d 5

# Terminal 2: Per-Core-Statistiken mit IRQ-Aufschlusselung
mpstat -P ALL 1
```

### Deep Analysis (root)

```bash
# Terminal 1: Hardware-Frequenzen, C-States, Power
sudo turbostat --interval 2 --show Core,CPU,Avg_MHz,Bzy_MHz,Busy%,IRQ,CoreTmp,PkgWatt

# Terminal 2: Interrupt-Verteilung (Shielding-Check)
mpstat -I ALL -P ALL 2

# Terminal 3: Governor-Status verifizieren
cpupower -c all frequency-info -p
```

### Vor dem Start (Konfiguration prufen)

```bash
# Governor korrekt?
cpupower -c all frequency-info -p -g

# C-States aktiv?
cpupower idle-info

# Verfugbare Monitore
cpupower monitor -l
```

---

## Alle Pakete auf einen Blick

```bash
sudo apt install htop btop sysstat linux-cpupower
```

Dies installiert alle funf Tools (turbostat und cpupower sind beide im Paket `linux-cpupower` enthalten).
