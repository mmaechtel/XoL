# XoL Monitoring Suite

## The Problem

X-Plane 12 with ortho scenery streaming consumes enormous amounts of RAM,
disk IO, and GPU resources simultaneously.  When the system runs out of
free memory, the Linux kernel reclaims pages synchronously — on the very
thread that needs the memory.  If that thread is X-Plane's rendering loop,
the result is a micro-stutter.

These stutters are invisible to simple tools like `htop` because they happen
in bursts of milliseconds.  A 5-minute test flight looks fine; a 90-minute
flight across ortho scenery exposes memory pressure, swap storms, and IO
contention that only appear after 30-60 minutes.

## The Solution: Three Layers of Visibility

This suite provides three scripts that work together to capture what happens
during a flight — from high-level system metrics down to individual kernel
events.

```
  Layer 1: sysmon.py           Always run.  No root needed.
  ─────────────────────────────────────────────────────────
  Polls /proc and GPU every 200 ms (CPU, memory, disk IO)
  and every 1 s (GPU, interrupts, vmstat, per-process).
  Writes 9 CSV files + correlates with X-Plane Log.txt.
  With --xplane: also records FPS, CPU/GPU frame time
  via UDP RREF (xplane_telemetry.py, 5 Hz default).

  Layer 2: sysmon_trace.sh     Run when hunting a specific cause.  Needs sudo.
  ─────────────────────────────────────────────────────────
  Attaches bpftrace to kernel tracepoints.  Captures events
  that polling cannot see: which process triggers Direct
  Reclaim, which NVMe requests exceed 5 ms, whether the CPU
  stalls waiting for the GPU.

  Layer 3: post_crash.sh       Run after a crash.  Needs sudo.
  ─────────────────────────────────────────────────────────
  Captures volatile GPU/kernel state (dmesg, NVIDIA bug report,
  journal) before it gets overwritten.
```

**Typical workflow:** Start `sysmon.py` before every flight.  If the summary
shows allocation stalls or swap spikes, re-run with `sysmon_trace.sh` in a
second terminal to identify root causes.  Use `post_crash.sh` only after
GPU crashes.

## How sysmon.py Collects Data

The sampling loop runs at two rates to balance detail against overhead:

**Fast probes (every 200 ms)** read `/proc/stat`, `/proc/meminfo`, and
`/proc/diskstats`.  These are plain text files that the kernel updates
continuously — reading them costs ~0.1 ms and has no measurable impact on
system performance.  The 200 ms rate captures burst events (IO spikes,
memory pressure surges) that 1-second sampling would miss.

**Slow probes (every 1 s)** collect GPU metrics via NVML, parse
`/proc/interrupts` and `/proc/vmstat`, read per-process stats from
`/proc/<pid>/stat`, and poll PSI.  These are heavier operations (GPU query
alone takes ~1 ms) so they run at a lower rate.

After the recording completes, sysmon.py parses X-Plane's `Log.txt` and
matches system spikes (IO > 50 MB/s, allocation stalls > 0) against
application events (DSF scenery loads, airport transitions, weather changes)
within a +-3 second window.

All data is written to CSV files for post-flight analysis in any
spreadsheet or plotting tool.

## Quick Start

```bash
# Record a 20-minute session (default)
python3 sysmon.py

# Record 90 minutes to a specific directory
python3 sysmon.py -d 5400 -o ~/flightlogs/run_01

# Add kernel tracepoints (separate terminal)
sudo bash sysmon_trace.sh -o ~/flightlogs/run_01

# After a crash
sudo bash post_crash.sh
```

Run `python3 sysmon.py --help` for all options.

### Dependencies

- Python 3.9+, Linux kernel 4.20+
- Optional: `nvidia-ml-py` (pip) for GPU metrics, `bpftrace` (apt) for kernel traces

## What to Look For

The terminal summary after each run highlights the critical numbers.
Here is what matters most:

| Metric | Where | Healthy | Problem |
|--------|-------|---------|---------|
| Alloc stalls | vmstat summary | 0/s | >0 means a thread was blocked waiting for free memory |
| Direct reclaim scan | vmstat summary | 0/s | >0 means the kernel reclaims on the requesting thread |
| Swap swing | memory summary | <100 MB | >1 GB means swap thrashing |
| Dirty pages | memory summary | <10 MB | >100 MB means writeback backlog |
| Write latency | disk IO summary | <5 ms | >10 ms suggests NVMe power-state or swap contention |
| GPU utilization drop | GPU summary | stable | Sudden drop with rising frame times = CPU starvation |

### The Three-Phase Pattern

Long flights with ortho streaming follow a predictable pattern:

1. **Warm-up (0-10 min)** — Memory fills, caches warm up, everything is smooth.
2. **Ramp-up (10-60 min)** — Memory approaches the limit, swap begins, reclaim
   events appear.  Most stutters happen here.
3. **Steady state (60+ min)** — Working set stabilizes.  A well-tuned system
   shows zero reclaim in this phase.

Short test runs (5-10 min) miss the ramp-up entirely.  Record at least
20 minutes, ideally 60+ minutes for a realistic profile.

---

## Analyzing a Run

After a recording session, analyze the results by feeding the run directory
and application logs to an AI or reviewing them manually.  The suite
collects four types of data:

1. **System metrics** (CSV files in the run directory)
2. **Kernel traces** (trace log files, if Layer 2 was used)
3. **X-Plane application events** (`~/X-Plane-12/Log.txt` or archived
   logs in `~/X-Plane-12/Output/Log Archive/`)
4. **XEarthLayer streaming events** (`~/.xearthlayer/xearthlayer.log`)

The XEarthLayer log is particularly valuable: it reveals *why* the system
is under pressure (tile loading bursts, circuit breaker activations,
flight phase changes, heading turns) while the CSV data shows *what*
happens at the system level (memory pressure, IO storms, CPU stalls).

Cross-correlating these sources is the key to identifying root causes.
See [ANALYSIS_RULES.txt](ANALYSIS_RULES.txt) for a complete, structured
analysis framework with thresholds, causal chains, and known signatures.

**Note:** X-Plane overwrites `Log.txt` on each launch.  If analyzing a
past session, use the archived log from `~/X-Plane-12/Output/Log Archive/`
and pass it via `--xplane-log` or `SYSMON_XPLANE_LOG`.

---

## Further Reading

- [FEATURES.md](FEATURES.md) — CLI options, CSV column reference, tracepoint
  details, cgwatcher configuration
- [ANALYSIS_RULES.txt](ANALYSIS_RULES.txt) — structured analysis framework
  for AI-assisted or manual post-flight analysis
- `python3 sysmon.py --help` — all command-line options
- `python3 cgroups/cgwatcher.py --help` — CPU priority manager

## Directory Layout

```
monitoring/
  sysmon.py              Layer 1 — system metrics collector
  xplane_telemetry.py    X-Plane FPS/CPU/GPU recorder (UDP RREF, auto-started via --xplane)
  sysmon_trace.sh        Layer 2 — kernel tracepoint sidecar
  post_crash.sh          Layer 3 — post-crash diagnostics
  README.md              This file
  FEATURES.md            Detailed reference (CSV formats, CLI, tracepoints)
  ANALYSIS_RULES.txt     AI analysis framework (thresholds, correlations)
  cgroups/
    cgwatcher.py         CPU priority manager
    cgwatcher.conf       Process-to-priority mapping
    install.sh           Install systemd user slices
    cgstatus.sh          Show current classification
    *.slice              systemd slice definitions
```
