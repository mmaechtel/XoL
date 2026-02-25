# Feature Reference

Detailed reference for CLI options, CSV output formats, kernel tracepoints,
and the CPU priority manager.  For an introduction, see [README.md](README.md).

---

## sysmon.py — CLI Options

```
sysmon [-h] [-V] [-d SEC] [-i SEC] [-o DIR] [-p PAT] [-l PATH]
       [--no-gpu] [--no-dmesg] [--xplane] [--xplane-rate HZ]

  -d, --duration SEC    Recording duration in seconds (default: 1200 = 20 min)
  -i, --interval SEC    Base sampling interval (default: 0.2)
  -o, --outdir DIR      Output directory (default: /tmp/sysmon_out)
  -p, --procs PAT       Comma-separated process patterns to track
  -l, --xplane-log PATH Path to X-Plane Log.txt (auto-detected if omitted)
  --no-gpu              Disable GPU monitoring
  --no-dmesg            Skip dmesg capture
  --xplane              Start X-Plane telemetry recorder (FPS, CPU/GPU time via UDP)
  --xplane-rate HZ      Telemetry poll rate in Hz (default: 5)
  -V, --version         Show version
```

Environment variables (`SYSMON_DURATION`, `SYSMON_INTERVAL`, `SYSMON_OUTDIR`,
`SYSMON_PROCS`, `SYSMON_XPLANE_LOG`) override defaults but are themselves
overridden by CLI arguments.

### GPU Backend Selection

GPU monitoring is initialized at startup in this order:

1. **NVML direct** — tries `nvidia-ml-py` Python bindings (fastest, ~0.3 ms per query)
2. **nvidia-smi** — falls back to subprocess call (~2 ms per query)
3. **AMD detection** — reports AMD GPU presence but does not sample (not yet implemented)
4. **None** — no GPU monitoring; vram.csv is written with headers only

Use `--no-gpu` to skip GPU initialization entirely (useful on headless systems
or when the NVIDIA driver is in a bad state after a crash).

### X-Plane Log Correlation

After recording completes, sysmon.py parses X-Plane's `Log.txt` and matches
system spikes against application events within a +-3 second window:

- **IO spikes >50 MB/s** correlated with DSF loads and airport transitions
- **Major faults >100/s** correlated with scenery streaming activity
- **Allocation stalls >0** correlated with all event types

Auto-detected log paths: `~/X-Plane-12/Log.txt`,
`~/X-Plane-12-Native/Log.txt`, `~/.local/share/X-Plane-12/Log.txt`.

### X-Plane In-Sim Telemetry (`--xplane`)

When `--xplane` is passed, sysmon.py spawns `xplane_telemetry.py` as a
subprocess.  This connects to X-Plane's UDP RREF interface (port 49000) and
records in-sim performance data at the configured rate (default: 5 Hz).

**Requires:** X-Plane 12.1.1+, Settings > Network > Accept incoming connections.

**How it works:** Dataref names are resolved to session-specific numeric IDs at
startup (IDs change with every X-Plane launch).  X-Plane then pushes all
subscribed values in a single UDP packet at the requested frequency.

**Note:** The X-Plane Web API (port 8086) was evaluated but found too slow for
bulk queries (~3 s per HTTP request due to synchronous main-thread processing).
UDP RREF delivers all values in <1 ms.

**Output:** `xplane_telemetry.csv` in the output directory (see CSV reference below).

---

## CSV Output Reference

Each run writes 9 CSV files (10 with `--xplane`) to the output directory.
All files use Unix timestamps (seconds since epoch, 3 decimal places) as the
first column.

### cpu.csv — Per-CPU Usage (200 ms)

| Column | Unit | Description |
|--------|------|-------------|
| cpu_id | — | CPU number or "all" for aggregate |
| user | % | User-space time (includes nice) |
| sys | % | Kernel time |
| iowait | % | Waiting for IO completion |
| irq | % | Hardware interrupt servicing |
| softirq | % | Software interrupt servicing |
| idle | % | Idle time |
| steal | % | Time stolen by hypervisor (KVM) |
| guest | % | Time running guest VMs |

### mem.csv — Memory (200 ms)

| Column | Unit | Description |
|--------|------|-------------|
| total_mb | MB | Total physical RAM |
| used_mb | MB | Used (total - free - buffers - cached) |
| free_mb | MB | Free pages |
| available_mb | MB | Available without swapping |
| buffers_mb | MB | Kernel buffer cache |
| cached_mb | MB | Page cache |
| swap_used_mb | MB | Swap in use |
| swap_free_mb | MB | Swap available |
| dirty_mb | MB | Dirty pages pending writeback |
| writeback_mb | MB | Pages actively being written back |

### io.csv — Per-Device Disk IO (200 ms)

| Column | Unit | Description |
|--------|------|-------------|
| device | — | Block device name (e.g., nvme0n1) |
| r_per_s | ops/s | Read operations per second |
| w_per_s | ops/s | Write operations per second |
| rMB_per_s | MB/s | Read throughput |
| wMB_per_s | MB/s | Write throughput |
| avg_r_lat_ms | ms | Average read latency |
| avg_w_lat_ms | ms | Average write latency |
| io_util_pct | % | Device utilization |
| ios_in_progress | — | Instantaneous queue depth |

### vram.csv — GPU / NVIDIA (1 s)

| Column | Unit | Description |
|--------|------|-------------|
| mem_used_mib | MiB | VRAM in use |
| mem_total_mib | MiB | Total VRAM |
| mem_free_mib | MiB | VRAM free |
| temp_c | C | GPU temperature |
| gpu_util_pct | % | GPU compute utilization |
| mem_util_pct | % | Memory controller utilization |
| gpu_clock_mhz | MHz | Current GPU clock |
| mem_clock_mhz | MHz | Current memory clock |
| power_w | W | Power draw |
| pcie_tx_kbs | KB/s | PCIe TX throughput |
| pcie_rx_kbs | KB/s | PCIe RX throughput |
| throttle_reasons | bitmask | Clock throttle reasons (0 = none) |
| perf_state | — | Performance state (P0 = max) |

### vmstat.csv — Kernel VM Counters (1 s)

All rate columns are per-second deltas.

| Column | Unit | Description |
|--------|------|-------------|
| ctxt_s | /s | Context switches |
| pgfault_s | /s | Minor page faults |
| pgmajfault_s | /s | Major page faults (disk-backed) |
| pgscan_kswapd_s | /s | Pages scanned by kswapd (background reclaim) |
| pgscan_direct_s | /s | Pages scanned by direct reclaim (stall-inducing) |
| pgsteal_kswapd_s | /s | Pages reclaimed by kswapd |
| pgsteal_direct_s | /s | Pages reclaimed by direct reclaim |
| allocstall_s | /s | Allocation stalls (thread blocked waiting for pages) |
| compact_stall_s | /s | Memory compaction stalls |
| tlb_shootdown_s | /s | TLB shootdowns (cross-CPU cache invalidations) |
| nr_dirty | pages | Current dirty page count |
| nr_writeback | pages | Pages being written back |
| pswpin_s | /s | Pages swapped in |
| pswpout_s | /s | Pages swapped out |
| wset_refault_anon_s | /s | Anonymous working set refaults (zram thrashing signal) |
| wset_refault_file_s | /s | File working set refaults |
| thp_fault_fallback_s | /s | THP (Transparent Hugepage) allocation failures |

### psi.csv — Pressure Stall Information (1 s)

| Column | Unit | Description |
|--------|------|-------------|
| cpu_some10 | % | CPU pressure (some tasks stalled, 10s window) |
| cpu_some60 | % | CPU pressure (60s window) |
| mem_some10 | % | Memory pressure, some (10s) |
| mem_some60 | % | Memory pressure, some (60s) |
| mem_full10 | % | Memory pressure, full (10s) |
| mem_full60 | % | Memory pressure, full (60s) |
| io_some10 | % | IO pressure, some (10s) |
| io_some60 | % | IO pressure, some (60s) |
| io_full10 | % | IO pressure, full (10s) |
| io_full60 | % | IO pressure, full (60s) |

### irq.csv — Interrupts (1 s)

| Column | Unit | Description |
|--------|------|-------------|
| irq | — | IRQ number or name |
| desc | — | Interrupt description |
| total_rate | /s | Total interrupt rate |
| cpu0..cpuN | /s | Per-CPU interrupt rate |

### proc.csv — Per-Process (1 s)

| Column | Unit | Description |
|--------|------|-------------|
| pid | — | Process ID |
| name | — | Process name or name[pattern] |
| cpu_pct | % | CPU usage (all threads combined) |
| rss_mb | MB | Resident Set Size |
| io_read_mbs | MB/s | Read IO throughput |
| io_write_mbs | MB/s | Write IO throughput |
| threads | — | Thread count |

### freq.csv — CPU Frequency (1 s)

| Column | Unit | Description |
|--------|------|-------------|
| cpu0_mhz..cpuN_mhz | MHz | Current clock frequency per CPU |

### xplane_events.csv — X-Plane Log Correlation (post-run)

Generated when X-Plane Log.txt is found.

| Column | Description |
|--------|-------------|
| timestamp | Unix timestamp |
| rel_offset_s | Seconds since monitoring start |
| category | DSF, AIRPORT, WEATHER, PRELOAD, or ERROR |
| message | Event description from Log.txt |

### xplane_telemetry.csv — In-Sim Telemetry (5 Hz, `--xplane` only)

Generated by xplane_telemetry.py subprocess via X-Plane UDP RREF (port 49000).

| Column | Unit | Description |
|--------|------|-------------|
| timestamp | epoch s | Unix timestamp |
| rel_s | s | Seconds since recording start |
| fps | 1/s | Frames per second (1 / frame_time) |
| frame_time_ms | ms | Total frame time |
| cpu_time_ms | ms | CPU frame time (frame_time - gpu_time) |
| gpu_time_ms | ms | GPU frame time (approx) |
| lat | deg | Aircraft latitude |
| lon | deg | Aircraft longitude |
| elev_m | m | Elevation MSL |
| agl_m | m | Altitude AGL |
| gs_kts | kts | Ground speed |
| ias_kts | kts | Indicated airspeed |
| sim_time_s | s | X-Plane simulation elapsed time |
| paused | 0/1 | Simulation paused flag |

**Datarefs used:** `sim/operation/misc/frame_rate_period`,
`sim/time/gpu_time_per_frame_sec_approx`, `sim/flightmodel/position/*`,
`sim/time/total_running_time_sec`, `sim/time/paused`.

**Note:** CPU time is derived (frame_time minus gpu_time).  Values use float32
precision (RREF protocol limitation) — lat/lon have ~6 significant digits.

---

## sysmon_trace.sh — Kernel Tracepoints

Three parallel bpftrace probes that capture events invisible to polling.
All require root.

### Probe 1: Direct Reclaim (`trace_reclaim.log`)

Tracepoints: `mm_vmscan_direct_reclaim_begin/end`,
`mm_vmscan_kswapd_wake/sleep`

Captures per-process reclaim duration in microseconds and the number of
pages reclaimed.  The key insight this provides: which process and thread
is being stalled by memory reclaim.  In measured sessions, 67% of all
Direct Reclaim events occurred on X-Plane's main rendering thread.

Output format:

```
HH:MM:SS pid=<pid> comm=<name> reclaim_us=<duration> nr_reclaimed=<pages>
HH:MM:SS KSWAPD_WAKE nid=<node> order=<order>
HH:MM:SS KSWAPD_SLEEP nid=<node>
```

### Probe 2: Slow IO (`trace_io_slow.log`)

Tracepoints: `block_rq_issue/complete` (filtered: latency > 5 ms)

NVMe drives in deep power-saving states (PS3/PS4) take 10-11 ms to wake
up.  This probe makes those transitions visible as distinct latency
clusters, separate from normal IO variability.

Output format:

```
HH:MM:SS dev=<major:minor> sector=<sector> lat_ms=<latency> nr_sector=<size>
```

### Probe 3: DMA Fence Waits (`trace_fence.log`)

Tracepoints: `dma_fence_wait_start/end` (filtered: wait > 5 ms)

Fires when a CPU thread blocks waiting for a GPU fence to signal.
Non-zero events indicate CPU-GPU synchronization bottlenecks.  In all
measured X-Plane sessions, this was consistently zero — confirming that
stutters originate from memory/IO, not GPU synchronization.

Output format:

```
HH:MM:SS pid=<pid> comm=<name> fence_wait_ms=<duration>
```

### Map Overflow Prevention

bpftrace's default map size (4096 keys) is too small for long sessions.
`sysmon_trace.sh` sets `BPFTRACE_MAP_KEYS_MAX=65536` automatically.

---

## cgwatcher.py — CPU Priority Manager

### Scheduler Detection

cgwatcher reads `/boot/config-$(uname -r)` or `/proc/config.gz` at
startup to detect the active scheduler:

| Scheduler | Kernel | Enforcement | Why |
|-----------|--------|-------------|-----|
| CFS | Debian stock | systemd user slices (CPUWeight + CPUQuota) | cgroup v2 weights work as expected |
| PDS | Liquorix | nice values | PDS ignores cgroup cpu.weight; nice is the only lever |
| BMQ | Project C | nice values | Same as PDS |

### Priority Classes

Configured in `cgroups/cgwatcher.conf` (one rule per line: `pattern = class`):

| Class | CPUWeight | CPUQuota | nice | Default processes |
|-------|-----------|----------|------|-------------------|
| simulator | 1000 | unlimited | 0 | X-Plane, gamescope |
| streamer | 300 | 960% | 5 | xearthlayer, autoortho |
| tools | 100 | 320% | 10 | LittleNavmap |

CPUQuota is expressed as percentage of one CPU core.  960% = 9.6 cores
on a 16-core system (60% total).  Only applies in CFS mode.

### Modes

```bash
python3 cgwatcher.py              # foreground, Ctrl+C to stop
python3 cgwatcher.py --daemon     # background, logs to /tmp/cgwatcher.log
python3 cgwatcher.py --once       # single scan, then exit
```

### Setup (CFS mode only)

```bash
cd cgroups/
bash install.sh     # copies *.slice to ~/.config/systemd/user/, reloads
bash cgstatus.sh    # shows which processes are in which slice
```

In PDS/BMQ mode, no setup is needed — nice values are applied directly.

---

## post_crash.sh — What It Collects

| Step | Tool | Output | Purpose |
|------|------|--------|---------|
| 1 | nvidia-bug-report.sh | nvidia-crash-*.log.gz | Complete GPU state dump (registers, allocations, error state) |
| 2 | dmesg -T | dmesg_crash_*.log | Full kernel ring buffer with timestamps |
| 3 | journalctl -k --grep | journal_crash_*.log | GPU-related kernel messages (NVRM, Xid, drm, amdgpu) from last 30 min |

All files are timestamped so multiple crash captures don't overwrite each other.

If `nvidia-smi` is hanging after a device loss (GPU locked up), use:

```bash
sudo nvidia-bug-report.sh --safe-mode
```
