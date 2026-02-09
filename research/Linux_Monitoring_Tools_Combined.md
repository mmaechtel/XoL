# Linux Monitoring Tools: Combined/Comprehensive System Monitors

Research paper for `systemtools.md` — Focus on all-in-one dashboards and multi-metric tools relevant to latency/performance analysis for X-Plane on Debian Linux.

---

## 1. glances (nicolargo/glances)

### Overview

Glances is a cross-platform curses-based system monitoring tool written in Python, using the psutil library. It provides a comprehensive single-screen dashboard showing CPU, memory, disk I/O, network, processes, sensors, GPU, containers, and more. It serves as a top/htop alternative with significantly broader metric coverage.

### Debian Package

- **Package:** `glances`
- **Bookworm version:** 3.3.1.1+dfsg-1
- **Install:** `sudo apt install glances`
- **Note:** The Debian packaged version lags behind upstream (currently 4.x). For the latest features (web UI improvements, GPU plugin), install via pip: `pip install glances[all]`

### Key Features

**Metrics in a single view:**

- CPU utilization (per-core and aggregate)
- Load average
- Memory and swap usage
- Disk I/O throughput, IOPS, and mean latency (`--diskio-latency` or `L` hotkey)
- Network I/O per interface
- Filesystem usage
- Sensor readings (temperatures, voltages, fan speeds)
- GPU utilization (NVIDIA/AMD via optional plugin)
- Process list with sorting (CPU, memory, I/O)
- Container monitoring (Docker, LXC)

**Web UI mode:**

```bash
glances -w
```

Starts a web server on port 61208 with a browser-accessible dashboard. Also exposes a RESTful JSON API at `http://localhost:61208/api/4`. Useful for monitoring from another device while X-Plane is running fullscreen.

**Export/logging capabilities:**

- CSV: `glances --export csv --export-csv-file /tmp/glances.csv`
- JSON export
- Database backends: InfluxDB, Elasticsearch, PostgreSQL/TimescaleDB, Prometheus, Graphite, Cassandra, OpenTSDB
- Message brokers: RabbitMQ, Kafka, NATS, ZeroMQ, StatsD

**Relevant hotkeys (terminal mode):**

| Key | Function |
|-----|----------|
| `1` | Toggle per-CPU stats |
| `b` | Toggle bytes/bits for network |
| `B` | Toggle disk I/O to IOPS view |
| `L` | Toggle disk I/O to latency view |
| `d` | Toggle disk I/O display |
| `n` | Toggle network display |
| `s` | Toggle sensors display |
| `G` | Toggle GPU display |
| `T` | Toggle network I/O sum |

### Relevance for Latency/Performance Analysis

- **Disk I/O latency display** shows mean latency per device — directly relevant for detecting NVMe power-saving wake-up delays documented in systemtuning.md
- **Sensor monitoring** shows CPU temperature and fan speed — useful for detecting thermal throttling
- **Per-CPU view** helps identify interrupt imbalance (relevant to irqbalance tuning)
- **Web UI** allows monitoring from a second device while X-Plane runs fullscreen
- **Process I/O** tracking identifies background processes competing for disk bandwidth

### Best Use Case

All-in-one dashboard for ongoing system monitoring. Best when you need a broad overview of system health across all subsystems simultaneously. The web UI makes it uniquely useful for monitoring during X-Plane sessions.

### Limitations

- Debian Bookworm ships an older version (3.x); the latest features require pip installation
- GPU monitoring requires additional Python packages (`py3nvml` for NVIDIA)
- Higher resource overhead than simpler tools due to breadth of monitoring
- No built-in stress testing capability

### Key Usage Examples

```bash
# Basic terminal dashboard
glances

# Web UI mode (access at http://localhost:61208)
glances -w

# Show disk latency and per-CPU stats
glances --diskio-latency --percpu

# Export to CSV for later analysis
glances --export csv --export-csv-file /tmp/session.csv

# Quiet mode: only show alerts
glances -q
```

---

## 2. nmon (Nigel's Monitor)

### Overview

nmon (Nigel's Monitor) is a performance monitoring tool originally developed internally at IBM for AIX, later released as open source under GPL for Linux. It has two distinct operating modes: interactive real-time display and batch recording to CSV files for post-analysis. The toggle-panel design allows building a custom dashboard for the specific problem being investigated.

### Debian Package

- **Package:** `nmon`
- **Bookworm version:** 16n+debian-1
- **Install:** `sudo apt install nmon`
- Available in all current Debian releases

### Key Features

**Interactive mode — toggle-based panels:**

Each metric is toggled on/off with a single keypress, allowing users to build a custom view:

| Key | Panel |
|-----|-------|
| `c` | CPU utilization (per-core bar graphs) |
| `m` | Memory statistics |
| `d` | Disk I/O statistics |
| `n` | Network I/O |
| `t` | Top processes |
| `k` | Kernel information |
| `r` | System resource info (architecture, OS, kernel version) |
| `j` | Filesystem statistics |
| `N` | NFS data |
| `V` | Virtual memory and paging |
| `l` | Long-term CPU averages |
| `.` | Show only busy disks |
| `q` | Quit |

**Recording mode (batch/CSV):**

```bash
nmon -f -s 5 -c 720
```

- `-f` — write to file (auto-named: `hostname_YYYYMMDD_HHMM.nmon`)
- `-s 5` — snapshot every 5 seconds
- `-c 720` — collect 720 snapshots (= 1 hour at 5s intervals)
- Output is CSV format, importable into spreadsheets or analysis tools

**Post-analysis tools:**

- `nmonchart` — shell script converting nmon CSV to interactive HTML using Google Charts
- `nmonvisualizer` — Java-based graphical analyzer (GitHub: nmonvisualizer/nmonvisualizer)
- `pyNmonAnalyzer` — Python tool for reformatting and plotting nmon output

### What nmon Shows That Others Don't

- **Per-CPU bar graph visualization** in terminal — more visual than numeric tables
- **Disk I/O per device** with busy percentage
- **NFS statistics** — unique among the tools listed here
- **Recording mode** designed for unattended data collection over long periods — ideal for capturing a full X-Plane flight session and analyzing afterward
- **Minimal resource footprint** — single C binary, no Python dependencies

### Relevance for Latency/Performance Analysis

- **Recording mode** is ideal for capturing system behavior during an entire X-Plane session, then analyzing bottlenecks afterward
- **Per-disk busy percentage** identifies storage contention during ortho scenery loading
- **Toggle-panel design** lets users focus on exactly the subsystems relevant to their latency investigation
- **Low overhead** means it won't influence the measurements

### Best Use Case

Batch recording during X-Plane sessions for post-flight analysis. Also strong for quick interactive checks when you want a lightweight, dependency-free monitor. The recording-then-analyze workflow is nmon's distinguishing strength.

### Limitations

- No web UI — terminal only
- No sensor/temperature monitoring (no CPU temps, fan speeds)
- No GPU monitoring
- Interactive UI is functional but visually dated
- No real-time alerting or thresholds

### Key Usage Examples

```bash
# Interactive mode with CPU, memory, disk, and network panels
nmon
# Then press: c m d n

# Record a 1-hour session (snapshots every 5 seconds)
nmon -f -s 5 -c 720

# Record a 2-hour session (snapshots every 10 seconds)
nmon -f -s 10 -c 720

# Convert recording to HTML charts
nmonchart hostname_20250101_1200.nmon output.html
```

---

## 3. dool (scottchiefbaker/dool) — Successor to dstat

### Overview

Dool is a Python 3 compatible fork and successor of the discontinued dstat tool. It provides real-time, columnar resource statistics in the terminal — essentially a versatile replacement for vmstat, iostat, and ifstat combined. Each column shows a different resource category, updated at configurable intervals. An extensible plugin system allows adding custom metric collectors.

### Debian Package

- **Package:** NOT available in Debian Bookworm or Trixie
- The original `dstat` has been removed from Debian unstable (as of October 2025)
- An ITP (Intent to Package) for dool was filed (Debian bug #1032875) but the package has not materialized
- **Installation from source:**

```bash
git clone https://github.com/scottchiefbaker/dool.git
sudo cp dool/dool /usr/local/bin/
mkdir -p ~/.dool/ && cp dool/plugins/* ~/.dool/
```

### Key Features

**Default output columns:**

```bash
dool
```

Shows CPU, disk, network, paging, and system stats in a continuously scrolling table. Each row is one time sample.

**Available preset modes:**

- `dool --defaults` — standard set (CPU, disk, net, paging, system)
- `dool --more` — extended set
- `dool --all` — all available metrics

**Plugin system:**

Over 40 built-in plugins: `aio`, `cpu`, `cpu24`, `cpu-adv`, `cpu-use`, `disk`, `disk24`, `epoch`, `fs`, `int`, `int24`, `io`, `ipc`, `load`, `lock`, `mem`, `mem-adv`, `net`, `page`, `page24`, `proc`, `raw`, `socket`, `swap`, `sys`, `tcp`, `time`, `udp`, `unix`, `vm`, `vm-adv`, `zones`, and more.

**CSV export:**

```bash
dool --time --cpu --mem --load --output report.csv 1 5
```

**Notable difference from dstat:** Network and disk bandwidth displayed in bits instead of bytes by default.

### Relevance for Latency/Performance Analysis

- **Columnar scrolling output** makes it easy to correlate events across subsystems (e.g., seeing a CPU spike and disk I/O spike at the same timestamp)
- **Interrupt statistics** (`--int`) can identify IRQ storms
- **System stats** (`--sys`) show context switches and interrupts per second — direct indicators of scheduling pressure
- **Lightweight** — good for quick "is something happening right now" checks

### Best Use Case

Quick, correlating real-time statistics across multiple subsystems. Best for one-off investigations where you want to see if events in one subsystem (disk, network) correlate with symptoms in another (CPU spikes, context switches). The columnar format is ideal for piping to files or post-processing.

### Limitations

- **Not in Debian repos** — requires manual installation
- No dashboard/UI — pure scrolling text output
- No sensor or temperature data
- No GPU monitoring
- No web interface
- Maintenance activity has been questioned by Debian packagers

### Key Usage Examples

```bash
# Default view: CPU, disk, net, paging, system
dool

# CPU, disk I/O, and interrupt stats with timestamps
dool --time --cpu --disk --int 1

# All stats, output to CSV, 2-second interval
dool --all --output session.csv 2

# Monitor specific disk device
dool --disk -D sda,nvme0n1 1

# Show context switches and interrupts (scheduling pressure)
dool --time --sys --cpu 1
```

---

## 4. s-tui (amanusk/s-tui) — Stress Terminal UI

### Overview

s-tui is a terminal-based CPU monitoring and stress testing tool that displays real-time graphs of CPU frequency, temperature, power consumption, and utilization. It is specifically designed to verify CPU governor behavior and detect thermal throttling — making it directly relevant to the governor tuning documented in systemtuning.md.

### Debian Package

- **Package:** `s-tui`
- **Bookworm version:** 1.1.4-1
- **Install:** `sudo apt install s-tui`
- **Stress tools (optional):** `sudo apt install stress stress-ng`

### Key Features

**Four real-time graphs:**

1. **CPU Frequency** — shows clock speed per core, updated every 2 seconds
2. **CPU Utilization** — load percentage per core
3. **CPU Temperature** — thermal sensor readings
4. **CPU Power** — power consumption (Intel Sandy Bridge+, AMD Family 17h+; reads Intel RAPL)

**Stress testing integration:**

- Built-in toggling between monitoring and stress modes via sidebar radio buttons
- Supports three stress backends:
    - `stress` — basic CPU load generation
    - `stress-ng` — enhanced stress testing with more options
    - `FIRESTARTER` — extreme stress testing (optional submodule)
- Stress parameters configurable through the UI

**Governor verification workflow:**

Running s-tui while switching governors reveals the immediate effect on frequency behavior:

- **`performance` governor:** Frequency stays pinned at maximum
- **`ondemand` governor:** Frequency ramps up under stress, drops when idle
- **`powersave` governor:** Frequency stays at minimum even under load

Detecting thermal throttling is straightforward: a drop in the frequency graph while temperature is high indicates the CPU is throttling.

**Root vs. non-root:**

- As root: shows maximum Turbo Boost frequency available across all cores
- Without root: shows single-core Turbo Boost

**CSV logging:**

```bash
s-tui --csv
```

Creates a CSV file with timestamped frequency, utilization, temperature, and power data.

### Relevance for Latency/Performance Analysis

- **Governor verification:** Directly confirms whether the CPU governor recommended in systemtuning.md (performance or ondemand) is actually working as expected
- **Thermal throttling detection:** Frequency drops during sustained load indicate the CPU is self-limiting — a hidden latency source
- **Power monitoring:** Confirms whether power management is aggressive (causing wake-up latency) or disabled as intended
- **Stress testing:** Can simulate sustained CPU load to verify that the system maintains stable frequencies without throttling — simulates X-Plane workload characteristics

### Best Use Case

Verifying CPU governor configuration and detecting thermal throttling. The tool directly answers: "Is my governor setting actually doing what I configured?" This makes it the companion tool for the governor tuning in systemtuning.md. Also useful for burn-in testing after changing thermal paste or cooler.

### Limitations

- **CPU-only** — no disk, network, or memory monitoring
- No GPU monitoring
- Power reading requires Intel RAPL or AMD equivalent (not available on all hardware)
- No web UI
- No remote monitoring capability
- Requires `stress` or `stress-ng` packages for stress testing mode

### Key Usage Examples

```bash
# Basic monitoring (shows frequency, utilization, temperature, power)
s-tui

# Run as root for full Turbo Boost info
sudo s-tui

# Log to CSV for later analysis
s-tui --csv

# Non-interactive mode: just collect data, no UI
s-tui -j  # JSON output
```

---

## 5. powertop (Intel)

### Overview

PowerTOP is a diagnostic tool developed by Intel for analyzing power consumption and power management behavior on Linux systems. It identifies which components, processes, and kernel subsystems cause the most wakeups and power consumption. Beyond diagnostics, it provides an interactive mode to experiment with power management settings and a Tunables tab with optimization suggestions.

### Debian Package

- **Package:** `powertop`
- **Bookworm version:** 2.14-1+b2
- **Install:** `sudo apt install powertop`
- Requires root to run

### Key Features

**Five tabs (navigate with Tab/Shift+Tab):**

1. **Overview** — processes and devices ranked by wakeups per second and power consumption. Shows which components blame for power use. Fewer wakeups = less power consumed = fewer latency-inducing transitions.

2. **Idle Stats (C-States)** — shows C-state residency for all processors and cores. Higher C-states (C4 > C3 > C2 > C1) mean deeper sleep. Ideally, idle residency should be 90%+ in the highest C-state when the system is idle. For latency-sensitive workloads, *shallow* C-states are preferred (less wake-up delay).

3. **Frequency Stats (P-States)** — shows P-state usage and Turbo mode residency for all cores. Reveals whether the CPU is spending time at expected frequencies.

4. **Device Stats** — similar to Overview but focused on hardware devices. Identifies which devices are causing wakeups.

5. **Tunables** — lists all tunable power parameters with Good/Bad ratings. Toggle suggestions on/off with Enter key. Changes do not persist across reboots.

**Report generation:**

```bash
sudo powertop --html=report.html
```

Generates a detailed HTML report with all tab data, tunable states, and device statistics. Useful for documenting system state before/after tuning.

**Calibration:**

```bash
sudo powertop --calibrate
```

Runs calibration cycles to improve power estimation accuracy. Warning: toggles display brightness, WiFi, and other hardware during calibration — may disrupt display and connectivity.

**Auto-tune:**

```bash
sudo powertop --auto-tune
```

Sets all tunables to their "Good" (power-saving) setting. **Warning for X-Plane use:** This enables aggressive power saving which increases latency. Not recommended for gaming workloads — the opposite of what systemtuning.md recommends.

### Relevance for Latency/Performance Analysis

- **C-State analysis** is critical: Deep C-states (C6, C7) cause wake-up latencies in the hundreds-of-microseconds range. PowerTOP shows whether the system is entering deep C-states that could cause micro-stutters. This directly relates to the `intel_idle.max_cstate` and `processor.max_cstate` kernel parameters in systemtuning.md.
- **Wakeup analysis** identifies which processes and devices are causing the most interrupts — complements irqbalance tuning.
- **P-State/Frequency stats** confirm whether the governor and frequency scaling are working as intended.
- **Device power states** reveal whether USB devices, NVMe, and other peripherals are entering power-saving modes that cause latency spikes.
- **Tunables tab** lists everything that can be toggled — but for latency-sensitive use, many "Good" (power-saving) settings are actually harmful.

### Best Use Case

Diagnosing power-management-related latency sources. PowerTOP answers: "Which devices and kernel subsystems are entering power-saving states that cause wake-up latency?" It is the primary tool for verifying that the C-state and P-state restrictions from systemtuning.md are actually in effect. Use it *after* applying tuning parameters to confirm they took hold.

### Limitations

- **Requires root** for all functionality
- **Power estimation requires calibration** — without it, power numbers are approximate. Full calibration takes 90 minutes (270 measurements x 20 seconds each).
- **Auto-tune is counterproductive** for latency-sensitive workloads — it enables aggressive power saving
- No continuous logging mode (use `--html` for snapshots)
- No GPU monitoring
- No process-level CPU or memory tracking (not a general-purpose monitor)
- Intel-focused: power estimation is most accurate on Intel hardware; works on AMD but with reduced feature set

### Key Usage Examples

```bash
# Interactive mode (requires root)
sudo powertop

# Generate HTML report
sudo powertop --html=powertop_report.html

# Generate CSV report
sudo powertop --csv=powertop_report.csv

# Run calibration (warning: disrupts display/WiFi)
sudo powertop --calibrate

# Check C-state residency after applying kernel parameters
# Navigate to "Idle Stats" tab
sudo powertop
```

---

## Tool Comparison Matrix

| Feature | glances | nmon | dool | s-tui | powertop |
|---------|---------|------|------|-------|----------|
| **Debian package** | glances | nmon | not available | s-tui | powertop |
| **CPU monitoring** | per-core | per-core bar graph | aggregate | per-core graph | P-states |
| **Memory** | yes | yes | yes | no | no |
| **Disk I/O** | throughput + latency | per-device + busy% | throughput | no | device power states |
| **Network** | per-interface | per-interface | per-interface | no | no |
| **CPU temperature** | yes (sensors) | no | no | yes (graphed) | no |
| **CPU frequency** | no | no | no | yes (graphed) | P-state residency |
| **Power consumption** | no | no | no | yes (RAPL) | yes (estimated) |
| **C-State analysis** | no | no | no | no | yes |
| **GPU** | optional plugin | no | no | no | no |
| **Process list** | yes | top processes | no | no | wakeup sources |
| **Web UI** | yes (port 61208) | no | no | no | no |
| **CSV/recording** | CSV + databases | CSV (batch mode) | CSV | CSV | HTML/CSV reports |
| **Stress testing** | no | no | no | yes | no |
| **Root required** | no (some features) | no | no | no (full info: yes) | yes |
| **Dependencies** | Python + psutil | none (C binary) | Python 3 | Python + urwid | C binary |

---

## Recommended Usage by Scenario

### Scenario 1: "Something feels off during a flight"

**Use:** `glances` in web mode from a second device

```bash
glances -w --percpu --diskio-latency
```

Gives a real-time overview of all subsystems. The web UI means you don't need to alt-tab out of X-Plane. Look for: disk latency spikes, CPU core imbalance, memory pressure, high I/O from background processes.

### Scenario 2: "I want to record an entire session and analyze later"

**Use:** `nmon` in recording mode

```bash
nmon -f -s 5 -c 1440   # 2 hours at 5-second intervals
```

Start before launching X-Plane, stop after the session. Convert to HTML with `nmonchart` or import CSV into a spreadsheet. Compare timestamps of stutters with system metric spikes.

### Scenario 3: "I changed the CPU governor and want to verify it works"

**Use:** `s-tui`

```bash
sudo s-tui
```

Watch the frequency graph. With `performance` governor, all cores should be at max frequency. With `ondemand`, frequency should ramp up under load and drop when idle. If frequency drops while temperature is high, you have thermal throttling.

### Scenario 4: "I applied C-state restrictions and want to confirm"

**Use:** `powertop`

```bash
sudo powertop
```

Navigate to Idle Stats tab. After applying `intel_idle.max_cstate=1` or `processor.max_cstate=1`, the system should show near-zero residency in C-states above C1. If deep C-states still show activity, the kernel parameter is not in effect.

### Scenario 5: "I want to check what's causing periodic stutters"

**Use:** `dool` for quick correlation

```bash
dool --time --cpu --disk --sys --int 1
```

Watch for correlations: interrupt spikes coinciding with context switch spikes and CPU usage bumps. The scrolling columnar format makes temporal correlations visible. If disk I/O spikes correlate with stutters, the NVMe power-saving or writeback configuration may need attention.

---

## Sources

- GitHub: nicolargo/glances — https://github.com/nicolargo/glances
- Glances documentation — https://glances.readthedocs.io/en/latest/
- Glances Disk I/O documentation — https://glances.readthedocs.io/en/latest/aoa/diskio.html
- Debian package: glances (Bookworm) — https://packages.debian.org/bookworm/glances
- nmon SourceForge project — https://nmon.sourceforge.io/
- IBM nmon documentation — https://www.ibm.com/docs/ssw_aix_72/n_commands/nmon.html
- IBM nmon for Linux page — https://www.ibm.com/support/pages/original-nmon-web-page
- Debian package: nmon (Bookworm) — https://packages.debian.org/bookworm/source/nmon
- GitHub: scottchiefbaker/dool — https://github.com/scottchiefbaker/dool
- Debian ITP for dool — https://bugs.debian.org/cgi-bin/bugreport.cgi?bug=1032875
- GitHub: amanusk/s-tui — https://github.com/amanusk/s-tui
- Debian package: s-tui (Bookworm) — https://packages.debian.org/stable/utils/s-tui
- GitHub: fenrus75/powertop (Intel) — https://github.com/fenrus75/powertop
- Arch Wiki: Powertop — https://wiki.archlinux.org/title/Powertop
- Debian package: powertop (Bookworm) — https://packages.debian.org/bookworm/powertop
- Red Hat: Managing power consumption with PowerTOP — https://docs.redhat.com/en/documentation/red_hat_enterprise_linux/9/html/monitoring_and_managing_system_status_and_performance/managing-power-consumption-with-powertop_monitoring-and-managing-system-status-and-performance
