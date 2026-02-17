# System

Latency rather than throughput is the optimization target for X-Plane on Linux: a stable frame-time budget matters more than raw computing power. This section presents two kernel profiles — one for the stock kernel, one for Liquorix — and the monitoring tools to verify every tuning measure.

- **[Why Latency Matters](overview.md)** — Video introduction and tuning philosophy
- **[Tuning](systemtuning.md)** — Kernel parameters, CPU governor, interrupt affinity, NVMe tuning
- **[Monitoring](systemtools.md)** — btop, turbostat, perf, mpstat and other analysis tools
