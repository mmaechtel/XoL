# IO-Monitoring-Tools für Linux — Research Paper

Recherche-Datum: 2026-02-09
Zielseite: `systemtools.md` (TODO-Eintrag 1c)
Fokus: Tools zur Disk-I/O-Analyse, Latenz-Messung und NVMe-Power-State-Diagnose während X-Plane läuft.

---

## Übersicht

| Tool | Paket (Debian Bookworm) | Typ | Per-Prozess | Latenz | NVMe APST |
|------|------------------------|-----|-------------|--------|-----------|
| iotop | `iotop-c` | Per-Prozess IO-Bandwidth | Ja | Nein | Nein |
| iostat | `sysstat` (12.6.1) | Device-Level Statistiken | Nein | Gemittelt | Indirekt |
| fatrace | `fatrace` | Datei-Zugriffs-Events | Ja | Nein | Nein |
| blktrace | `blktrace` | Block-Layer Tracing | Via PID | Ja (ns) | Ja (D2C) |
| ioping | `ioping` | Synthetische Latenz-Messung | Nein | Ja | Ja (direkt) |
| nvme-cli | `nvme-cli` | NVMe-Management | Nein | Nein | Konfiguration |

---

## 1. iotop — Per-Prozess IO-Bandwidth

### Quelle

- GitHub: [Tomas-M/iotop](https://github.com/Tomas-M/iotop) (iotop-c, C-Rewrite)
- Paket: [packages.debian.org/bookworm/iotop-c](https://packages.debian.org/bookworm/iotop-c)

### Installation

```bash
sudo apt install iotop-c
```

### Was es zeigt

- **Disk Read/Write Rate pro Prozess** in Echtzeit
- **IO Wait Prozent** pro Prozess
- **Swap-In Prozent** pro Prozess
- Nutzt das Kernel-taskstats-Interface (CONFIG_TASK_DELAY_ACCT, CONFIG_TASK_IO_ACCOUNTING)

### Relevante Flags für X-Plane-Analyse

| Flag | Zweck |
|------|-------|
| `-o` | Nur Prozesse mit aktiver IO anzeigen (Rauschen ausblenden) |
| `-P` | Nur Prozesse, keine einzelnen Threads |
| `-a` | Akkumulierte IO seit Start (Gesamt-IO-Verursacher finden) |
| `-d 0.5` | Update alle 0.5 Sekunden |
| `-b` | Batch-Modus für Logging in Datei |
| `-t` | Zeitstempel hinzufügen (für Korrelation mit Stutter-Events) |
| `-p PID` | Nur X-Plane's PID überwachen |

### Verwendungsbeispiele

```bash
# Live-Monitoring — nur aktive IO-Prozesse, halbe Sekunde Refresh
sudo iotop -oPd 0.5

# X-Plane IO in Datei loggen
sudo iotop -botPd 0.5 -p $(pgrep -f "X-Plane") > /tmp/xplane_io.log

# Akkumulierte Ansicht — wer hat insgesamt am meisten gelesen
sudo iotop -oPa
```

### Limitierungen

- Requires root (oder CAP_NET_ADMIN)
- Zeigt Bandwidth, nicht Latenz — kann nicht sagen ob ein Read 50µs oder 500ms dauerte
- Kernel muss taskstats kompiliert haben (Standard auf Debian-Kernels)

### Stärke

Einziges Tool das zeigt **welcher Prozess** die IO verursacht. Essentiell um zu identifizieren ob Stutter von X-Plane selbst, einem Compositor, journald oder anderem Hintergrundprozess kommt.

---

## 2. iostat — Device-Level IO-Statistiken

### Quelle

- GitHub: [sysstat/sysstat](https://github.com/sysstat/sysstat)
- Manpage: [iostat(1)](https://manpages.debian.org/bookworm/sysstat/iostat.1.en.html)
- Paket: [packages.debian.org/bookworm/sysstat](https://packages.debian.org/bookworm/sysstat)

### Installation

```bash
sudo apt install sysstat
```

### Was es zeigt (mit `-x`)

| Feld | Bedeutung |
|------|-----------|
| `r/s` | Read-Requests pro Sekunde |
| `w/s` | Write-Requests pro Sekunde |
| `rareq-sz` | Durchschnittliche Read-Request-Größe (KiB) |
| `wareq-sz` | Durchschnittliche Write-Request-Größe (KiB) |
| `r_await` | Durchschnittliche Read-Request-Zeit (ms), inkl. Queue |
| `w_await` | Durchschnittliche Write-Request-Zeit (ms), inkl. Queue |
| `aqu-sz` | Durchschnittliche Queue-Länge |
| `%util` | Device-Auslastung in Prozent |

### Relevante Flags für X-Plane-Analyse

| Flag | Zweck |
|------|-------|
| `-x` | Extended Statistics (notwendig für await, %util, aqu-sz) |
| `-d` | Nur Device-Report (CPU überspringen) |
| `-t` | Zeitstempel ausgeben |
| `-p nvme0n1` | Spezifisches NVMe-Device überwachen |
| `-h` | Human-readable Ausgabe |
| `-o JSON` | JSON-Ausgabe für Scripting |
| `-y` | Ersten (seit-Boot) Report überspringen |
| `-z` | Devices ohne Aktivität ausblenden |

### Verwendungsbeispiele

```bash
# Extended Stats für NVMe, 1-Sekunden-Intervall, mit Zeitstempeln
iostat -xdth -p nvme0n1 1

# In Datei loggen (JSON, alle 2 Sekunden, 1800 Iterationen = 1 Stunde)
iostat -xdt -o JSON -p nvme0n1 2 1800 > /tmp/iostat_flight.json

# Quick Check: ist das Device gesättigt?
iostat -xdh -p nvme0n1 1 5
```

### NVMe Power State Erkennung

Indirekt. Ein plötzlicher Sprung in `r_await` von sub-Millisekunde auf 50-500ms nach einer Idle-Phase deutet stark auf NVMe APST Wake-Up-Latenz hin. iostat zeigt Power States nicht direkt, aber die Latenz-Signatur ist sichtbar.

### Limitierungen

- Device-Level — kann IO nicht einem bestimmten Prozess zuordnen (dafür iotop)
- Mittelt über das Sampling-Intervall — ein einzelner 200ms-Stall wird mit hunderten schneller Requests gemittelt
- Zeigt keine individuellen Request-Latenzen, nur Durchschnitte

### Stärke

Wichtigstes Tool für **Device-Level-Latenz** (`r_await`). Wenn `r_await` während des Flugs sprunghaft ansteigt, ist das Device der Flaschenhals. Zeigt auch `%util` für Sättigungs-Erkennung.

---

## 3. fatrace — Datei-Zugriffs-Events

### Quelle

- GitHub: [martinpitt/fatrace](https://github.com/martinpitt/fatrace)
- Paket: [packages.debian.org/bookworm/fatrace](https://packages.debian.org/bookworm/fatrace)

### Installation

```bash
sudo apt install fatrace
```

### Was es zeigt

Echtzeit-Datei-Zugriffs-Events (Open, Read, Write, Close) von allen Prozessen, mit vollem Dateipfad. Nutzt das Kernel-fanotify-Interface.

### Event-Typen

O (Open), R (Read), W (Write), C (Close), + (Directory create), D (Directory delete), < (moved from), > (moved to). Kombinationen möglich, z.B. CW = close-after-write.

### Relevante Flags

| Flag | Zweck |
|------|-------|
| `-f R` | Filter: nur Read-Events |
| `-f W` | Filter: nur Write-Events |
| `-C X-Plane` | Nur X-Plane-Prozess nach Kommando-Name |
| `-t` | Zeitstempel hinzufügen (`-tt` für Epoch) |
| `-s 60` | Nach 60 Sekunden stoppen |
| `-o /tmp/fatrace.log` | In Datei schreiben (vermeidet Disk-Wake durch Terminal-Ausgabe) |
| `-j` | JSONL-Ausgabe für Scripting |

### Verwendungsbeispiele

```bash
# Welche Dateien liest X-Plane gerade?
sudo fatrace -tf R -C X-Plane -o /tmp/xplane_reads.log

# Alle Dateizugriffe auf dem Scenery-Laufwerk für 60 Sekunden
sudo fatrace -tcs 60 -o /tmp/scenery_io.log

# Hintergrundprozesse finden die während des Flugs auf Disk schreiben
sudo fatrace -tf W -s 120 -o /tmp/writes_during_flight.log
```

### Limitierungen

- Zeigt Dateinamen und Zugriffstyp, aber nicht IO-Größe oder Latenz
- Immer in Datei umleiten mit `-o` (Terminal-Ausgabe erzeugt zusätzliche Disk-IO)
- Requires root

### Stärke

Beantwortet: "Welche Dateien liest X-Plane beim Szenerie-Wechsel?" und "Welche Hintergrundprozesse machen Disk-IO während des Flugs?"

---

## 4. blktrace / blkparse — Block-Layer IO-Tracing

### Quelle

- Kernel-Source: [torvalds/linux — kernel/trace/blktrace.c](https://github.com/torvalds/linux/blob/master/kernel/trace/blktrace.c)
- Manpage: [blkparse(1)](https://manpages.debian.org/testing/blktrace/blkparse.1.en.html)
- Paket: [packages.debian.org/bookworm/blktrace](https://packages.debian.org/bookworm/blktrace)

### Installation

```bash
sudo apt install blktrace
```

### Was es zeigt

Tiefstes Level der IO-Analyse — jeder Request auf Block-Layer-Ebene, von Queue-Insertion über Scheduler-Merge und Driver-Dispatch bis Hardware-Completion. Per-Request-Timing mit Nanosekunden-Präzision.

### Action Letters

| Buchstabe | Bedeutung |
|-----------|-----------|
| Q | Request in Queue eingefügt |
| G | Get Request (allokiert) |
| I | In Elevator/Scheduler eingefügt |
| D | An Device-Driver dispatched |
| C | Completed |
| M | Mit bestehendem Request gemerged (front) |
| F | Mit bestehendem Request gemerged (back) |
| P | Plug (Batching beginnt) |
| U | Unplug (Batch dispatched) |

### Relevante Flags

blktrace:

| Flag | Zweck |
|------|-------|
| `-d /dev/nvme0n1` | Device zum Tracen |
| `-w 30` | 30 Sekunden tracen |
| `-a read` | Filter: nur Read-Requests |
| `-o -` | Live-Ausgabe (Pipe zu blkparse) |

### Verwendungsbeispiele

```bash
# Live-Trace der NVMe-Reads für 30 Sekunden
sudo blktrace -d /dev/nvme0n1 -a read -w 30 -o - | blkparse -i -

# In Dateien aufzeichnen für Post-Analyse
sudo blktrace -d /dev/nvme0n1 -w 60
blkparse -i nvme0n1 -s > /tmp/blktrace_analysis.txt

# btt für Latenz-Analyse (im blktrace-Paket enthalten)
blkparse -i nvme0n1 -d nvme0n1.bin
btt -i nvme0n1.bin

# Quick Live-Trace (btrace = Kurzform für blktrace | blkparse)
sudo btrace /dev/nvme0n1
```

### NVMe Power State Erkennung

Ja, indirekt aber effektiv. D2C (Dispatch-to-Completion) Zeiten zeigen einzelne Requests die 10-500ms brauchten, während der Hintergrund bei <0.1ms liegt. Das ist das stärkste Signal für APST Wake-Up-Latenz aus dem Userspace.

### btt (Block Trace Timing)

Das blktrace-Paket enthält `btt`, das Latenz-Aufschlüsselungen produziert:

| Metrik | Bedeutung |
|--------|-----------|
| Q2Q | Queue-to-Queue (Zeit zwischen aufeinanderfolgenden Requests) |
| Q2C | Queue-to-Completion (gesamte Request-Zeit) |
| D2C | Dispatch-to-Completion (Device-Service-Zeit) |
| Q2D | Queue-to-Dispatch (Wartezeit in Scheduler) |

D2C ist die relevanteste Metrik für NVMe APST Wake-Up-Erkennung.

### Limitierungen

- Komplexe Ausgabe — erfordert Verständnis des Block-Layers
- Generiert große Datenmengen (hunderte MB bei längeren Traces)
- Moderater Overhead während des Tracings
- Requires root

---

## 5. ioping — Disk-IO-Latenz-Messung

### Quelle

- GitHub: [koct9i/ioping](https://github.com/koct9i/ioping)
- Paket: [packages.debian.org/bookworm/ioping](https://packages.debian.org/bookworm/ioping)

### Installation

```bash
sudo apt install ioping
```

### Was es zeigt

Individuelle IO-Request-Latenzen in Echtzeit, ähnlich wie `ping` für Netzwerk-Latenz. Sendet synthetische IO-Requests und misst die Antwortzeit. Zeigt min/avg/max/mdev-Statistiken.

### Relevante Flags

| Flag | Zweck |
|------|-------|
| `-c COUNT` | Nach COUNT Requests stoppen |
| `-s SIZE` | Request-Größe (Standard 4k; `-s 256k` für Scenery-ähnliche Reads) |
| `-i INTERVAL` | Zeit zwischen Requests (Standard 1s) |
| `-D` | Direct IO (Page Cache umgehen — zeigt wahre Device-Latenz) |
| `-C` | Cached IO (Page-Cache-Performance messen) |
| `-L` | Sequential (lineares) Zugriffsmuster |
| `-R` | Rapid-Modus — Seek-Rate-Test, keine Pause zwischen Requests |
| `-W` | Write-Modus statt Read |
| `-w TIME` | Nach TIME stoppen |
| `-B` | Batch-Modus (nur Summary ausgeben) |
| `-J` | JSON-Ausgabe |

### Verwendungsbeispiele

```bash
# Basis-Latenz-Check auf Scenery-Verzeichnis
ioping -c 20 /path/to/X-Plane/Custom\ Scenery/

# Direct IO-Latenz (Cache umgangen, zeigt wahre NVMe-Latenz)
ioping -c 20 -D /dev/nvme0n1

# Ortho-Texture-Reads simulieren: 256K sequentiell, Direct IO
ioping -c 50 -s 256k -D -L /dev/nvme0n1

# NVMe Wake-Up erkennen: 5 Sekunden idle, dann messen
sleep 5 && ioping -c 5 -D /dev/nvme0n1

# Rapid Random-Read-Test (IOPS-Messung)
ioping -R -D -w 10 /dev/nvme0n1
```

### NVMe APST Wake-Up-Latenz-Test

```bash
# Automatisierter Test: 5x idle + Messung
for i in $(seq 1 5); do
    sleep 5
    ioping -c 1 -D /dev/nvme0n1
done
```

Muster: Erster Request nach Idle zeigt 10-500ms, nachfolgende Requests <0.1ms = APST Wake-Up.

### Limitierungen

- Synthetischer Workload — zeigt was das Device *kann*, nicht was tatsächlich passiert
- Kann keine reale Application-IO überwachen (dafür iostat/blktrace)
- Write-Modus (`-W`) schreibt tatsächlich Daten — Vorsicht bei Raw-Devices

### Stärke

Einfachstes und direktestes Tool für NVMe APST Wake-Up-Erkennung. Kein Root für Dateisystem-Tests nötig.

---

## 6. nvme-cli — NVMe Power State Konfiguration

### Quelle

- GitHub: [linux-nvme/nvme-cli](https://github.com/linux-nvme/nvme-cli)
- Arch Wiki: [Solid state drive/NVMe](https://wiki.archlinux.org/title/Solid_state_drive/NVMe)
- Paket: [packages.debian.org/bookworm/nvme-cli](https://packages.debian.org/bookworm/nvme-cli)

### Installation

```bash
sudo apt install nvme-cli
```

### Relevante Befehle

```bash
# Alle Power States und ihre Entry/Exit-Latenz anzeigen
sudo nvme id-ctrl /dev/nvme0 | grep -A 5 "ps "

# APST-Konfiguration prüfen (Feature 0x0c)
sudo nvme get-feature /dev/nvme0 -f 0x0c -H

# Aktuellen Power State prüfen (Feature 0x02)
sudo nvme get-feature /dev/nvme0 -f 0x02 -H
```

### Stärke

Einziges Tool das die NVMe Power States direkt abfragen kann. Zeigt Entry/Exit-Latenzen der einzelnen States. Ergänzt ioping (Latenz messen) um die Ursache (welcher Power State).

---

## Vergleichsmatrix

| Fähigkeit | iotop | iostat | fatrace | blktrace | ioping |
|-----------|-------|--------|---------|----------|--------|
| Per-Prozess IO | Ja | Nein | Ja | Via PID | Nein |
| Device-Throughput | Nein | Ja | Nein | Ja | Synthetisch |
| Per-Request-Latenz | Nein | Gemittelt | Nein | Ja (ns) | Ja (synthetisch) |
| Datei-Level-Tracing | Nein | Nein | Ja | Nein | Nein |
| NVMe APST Erkennung | Nein | Indirekt | Nein | Ja (D2C) | Ja (direkt) |
| Overhead | Niedrig | Minimal | Niedrig | Moderat | Keiner (synthetisch) |
| Komplexität | Niedrig | Niedrig | Niedrig | Hoch | Niedrig |
| Root nötig | Ja | Nein | Ja | Ja | Nein (Dateien) / Ja (Devices) |

---

## Empfohlener Workflow für X-Plane IO-Stutter-Analyse

1. **Baseline:** `ioping -c 20 -D /dev/nvme0n1` — normale Device-Latenz ermitteln
2. **APST-Check:** `sleep 5 && ioping -c 3 -D /dev/nvme0n1` — Wake-Up-Penalty prüfen
3. **Während Flug:** `iostat -xdth -p nvme0n1 1` — `r_await` und `%util` auf Spikes beobachten
4. **Verursacher identifizieren:** `sudo iotop -oPd 0.5` — wer macht IO während Stutter
5. **Dateien identifizieren:** `sudo fatrace -tf R -C X-Plane -o /tmp/reads.log` — was liest X-Plane
6. **Deep Dive (falls nötig):** `sudo blktrace -d /dev/nvme0n1 -w 60` dann `btt`-Analyse

---

## Alle Pakete auf einen Blick

```bash
sudo apt install iotop-c sysstat fatrace blktrace ioping nvme-cli
```

---

## Quellen

- [Tomas-M/iotop (GitHub)](https://github.com/Tomas-M/iotop)
- [sysstat/sysstat (GitHub)](https://github.com/sysstat/sysstat)
- [martinpitt/fatrace (GitHub)](https://github.com/martinpitt/fatrace)
- [linux-nvme/nvme-cli (GitHub)](https://github.com/linux-nvme/nvme-cli)
- [koct9i/ioping (GitHub)](https://github.com/koct9i/ioping)
- [Arch Wiki: NVMe](https://wiki.archlinux.org/title/Solid_state_drive/NVMe)
- [blktrace Kernel Source](https://github.com/torvalds/linux/blob/master/kernel/trace/blktrace.c)
