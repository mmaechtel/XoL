#!/usr/bin/env python3
"""
cgroup watcher — classifies running processes by CPU priority.

Scans for processes matching patterns from cgwatcher.conf and applies
CPU prioritization.  The enforcement method depends on the scheduler:

  CFS (Debian stock kernel)  → systemd user slices (CPUWeight + CPUQuota)
  PDS (Liquorix kernel)      → nice values (cgroup cpu.weight is a no-op)

Detection is automatic at startup.

Usage:
  python3 cgwatcher.py              # foreground, Ctrl+C to stop
  python3 cgwatcher.py --daemon     # background, log to /tmp/cgwatcher.log
  python3 cgwatcher.py --once       # single scan, then exit

Environment:
  CGWATCH_INTERVAL   scan interval in seconds (default 5)

Log: /tmp/cgwatcher.log (daemon mode) or stdout (foreground)
"""

import os, sys, time, subprocess, logging
from pathlib import Path

INTERVAL = int(os.environ.get("CGWATCH_INTERVAL", 5))
UID = os.getuid()
CONF_PATH = Path(__file__).parent / "cgwatcher.conf"
LOG_PATH = Path("/tmp/cgwatcher.log")
PID_PATH = Path("/tmp/cgwatcher.pid")

# ─── class definitions ────────────────────────────────────────────────
# Each class: (CPUWeight, CPUQuota or None, nice value)

CLASSES = {
    "simulator": {"weight": 1000, "quota": None,   "nice": 0},
    "streamer":  {"weight": 300,  "quota": "960%", "nice": 5},
    "tools":     {"weight": 100,  "quota": "320%", "nice": 10},
}

# ─── logging ─────────────────────────────────────────────────────────

log = logging.getLogger("cgwatcher")
log.setLevel(logging.INFO)

def setup_logging(to_file=False):
    fmt = logging.Formatter("%(asctime)s  %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
    if to_file:
        h = logging.FileHandler(LOG_PATH)
    else:
        h = logging.StreamHandler(sys.stdout)
    h.setFormatter(fmt)
    log.addHandler(h)

# ─── scheduler detection ─────────────────────────────────────────────

def detect_scheduler():
    """Detect CPU scheduler: 'pds' (Liquorix) or 'cfs' (stock kernel)."""
    config_path = Path(f"/boot/config-{os.uname().release}")
    try:
        text = config_path.read_text()
        if "CONFIG_SCHED_PDS=y" in text:
            return "pds"
        if "CONFIG_SCHED_BMQ=y" in text:
            return "bmq"
    except FileNotFoundError:
        # Try /proc/config.gz
        try:
            import gzip
            text = gzip.open("/proc/config.gz", "rt").read()
            if "CONFIG_SCHED_PDS=y" in text:
                return "pds"
            if "CONFIG_SCHED_BMQ=y" in text:
                return "bmq"
        except (FileNotFoundError, ImportError):
            pass
    return "cfs"

# ─── config loading ──────────────────────────────────────────────────

def load_rules(conf_path):
    """Load process→class mapping from cgwatcher.conf.
    Format: pattern = class  (one per line, # comments)"""
    rules = {}
    try:
        for line in conf_path.read_text().splitlines():
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if "=" not in line:
                continue
            pattern, cls = line.split("=", 1)
            cls = cls.strip()
            if cls not in CLASSES:
                log.warning(f"Unknown class '{cls}' for pattern '{pattern.strip()}' — skipped")
                continue
            rules[pattern.strip()] = cls
    except FileNotFoundError:
        log.error(f"Config not found: {conf_path}")
        sys.exit(1)
    return rules

# ─── cgroup helpers (CFS mode) ───────────────────────────────────────

def get_user_cgroup_base():
    """Find the cgroup v2 base path for current user's service manager."""
    try:
        with open(f"/proc/{os.getpid()}/cgroup") as f:
            line = f.read().strip()
            cg_path = line.split("::")[-1]
            parts = cg_path.strip("/").split("/")
            for i, p in enumerate(parts):
                if p == f"user@{UID}.service":
                    return Path("/sys/fs/cgroup") / "/".join(parts[:i+1])
    except Exception:
        pass
    return Path(f"/sys/fs/cgroup/user.slice/user-{UID}.slice/user@{UID}.service")


def get_pid_cgroup(pid):
    """Return the cgroup path for a PID."""
    try:
        with open(f"/proc/{pid}/cgroup") as f:
            return f.read().strip().split("::")[-1]
    except (FileNotFoundError, PermissionError):
        return ""


def ensure_slice_active(slice_name):
    """Ensure the slice unit is started so its cgroup directory exists."""
    unit = f"{slice_name}.slice"
    result = subprocess.run(
        ["systemctl", "--user", "start", unit],
        capture_output=True, text=True)
    if result.returncode != 0:
        log.warning(f"Cannot start {unit}: {result.stderr.strip()}")
    return result.returncode == 0


def move_pid_to_slice(pid, slice_name, comm):
    """Move a PID into a slice by writing to cgroup.procs."""
    cg_base = get_user_cgroup_base()
    procs_file = cg_base / f"{slice_name}.slice" / "cgroup.procs"

    if not procs_file.parent.exists():
        ensure_slice_active(slice_name)

    try:
        procs_file.write_text(str(pid))
        return True
    except FileNotFoundError:
        if ensure_slice_active(slice_name):
            try:
                procs_file.write_text(str(pid))
                return True
            except OSError as e:
                log.warning(f"Cannot move PID {pid} ({comm}) → {slice_name}: {e}")
        else:
            log.warning(f"Cannot move PID {pid} ({comm}) → {slice_name}: "
                        f"slice cgroup not found")
    except OSError as e:
        log.warning(f"Cannot move PID {pid} ({comm}) → {slice_name}: {e}")
    return False

# ─── nice helpers (PDS/BMQ mode) ─────────────────────────────────────

def get_pid_nice(pid):
    """Return the current nice value of a PID."""
    try:
        return os.getpriority(os.PRIO_PROCESS, pid)
    except OSError:
        return None


def set_pid_nice(pid, nice_val, comm):
    """Set the nice value of a PID."""
    try:
        os.setpriority(os.PRIO_PROCESS, pid, nice_val)
        return True
    except PermissionError:
        # Negative nice requires CAP_SYS_NICE or root
        result = subprocess.run(
            ["renice", "-n", str(nice_val), "-p", str(pid)],
            capture_output=True, text=True)
        if result.returncode == 0:
            return True
        log.warning(f"Cannot renice PID {pid} ({comm}) → {nice_val}: "
                    f"permission denied (try: sudo setcap cap_sys_nice+ep "
                    f"$(which python3))")
    except OSError as e:
        log.warning(f"Cannot renice PID {pid} ({comm}) → {nice_val}: {e}")
    return False

# ─── process scanner ─────────────────────────────────────────────────

def match_process(pid, rules):
    """Match a PID against rules. Returns (comm, class_name, pattern) or None."""
    try:
        comm = Path(f"/proc/{pid}/comm").read_text().strip()
    except (FileNotFoundError, PermissionError):
        return None

    for pattern, cls in rules.items():
        if pattern.lower() in comm.lower():
            return comm, cls, pattern

    # Fallback: check cmdline
    try:
        cmdline = Path(f"/proc/{pid}/cmdline").read_text()\
            .replace("\0", " ").strip()
    except (FileNotFoundError, PermissionError):
        return None

    for pattern, cls in rules.items():
        if pattern.lower() in cmdline.lower():
            return comm, cls, pattern

    return None


def scan_and_classify(rules, scheduler):
    """Scan /proc for matching processes, apply priority."""
    applied = []

    try:
        entries = os.listdir("/proc")
    except OSError:
        return applied

    for entry in entries:
        if not entry.isdigit():
            continue
        pid = int(entry)

        try:
            if os.stat(f"/proc/{pid}").st_uid != UID:
                continue
        except (FileNotFoundError, PermissionError):
            continue

        match = match_process(pid, rules)
        if match is None:
            continue

        comm, cls, pattern = match
        props = CLASSES[cls]

        if scheduler == "cfs":
            # Already in correct cgroup?
            current_cg = get_pid_cgroup(pid)
            if f"{cls}.slice" in current_cg:
                continue
            if move_pid_to_slice(pid, cls, comm):
                applied.append((pid, comm, cls, pattern, f"→ {cls}.slice"))

        else:  # pds / bmq — use nice
            target_nice = props["nice"]
            current_nice = get_pid_nice(pid)
            if current_nice == target_nice:
                continue
            if set_pid_nice(pid, target_nice, comm):
                applied.append((pid, comm, cls, pattern, f"nice {target_nice}"))

    return applied


# ─── main ─────────────────────────────────────────────────────────────

def run_once(rules, scheduler):
    applied = scan_and_classify(rules, scheduler)
    for pid, comm, cls, pattern, action in applied:
        log.info(f"SET    PID {pid:>7}  {comm:<20} → {cls:<12} "
                 f"{action}  (matched: {pattern})")
    return applied


def run_loop(rules, scheduler):
    mode = "cgroup slices" if scheduler == "cfs" else f"nice values ({scheduler})"
    log.info(f"Started — scanning every {INTERVAL}s")
    log.info(f"Scheduler: {scheduler} — enforcement: {mode}")
    log.info(f"Config: {CONF_PATH}")
    log.info(f"Rules: {len(rules)} patterns")
    for pattern, cls in rules.items():
        props = CLASSES[cls]
        if scheduler == "cfs":
            detail = f"weight={props['weight']}"
            if props["quota"]:
                detail += f" quota={props['quota']}"
        else:
            detail = f"nice={props['nice']}"
        log.info(f"  {pattern:<20} → {cls:<12} ({detail})")

    try:
        while True:
            run_once(rules, scheduler)
            time.sleep(INTERVAL)
    except KeyboardInterrupt:
        log.info("Stopped (keyboard interrupt)")


def main():
    daemon = "--daemon" in sys.argv
    once = "--once" in sys.argv

    setup_logging(to_file=daemon)

    scheduler = detect_scheduler()
    rules = load_rules(CONF_PATH)

    if not rules:
        log.error("No rules in config — nothing to watch")
        sys.exit(1)

    if once:
        applied = run_once(rules, scheduler)
        if not applied:
            log.info(f"No matching processes found (scheduler: {scheduler})")
        return

    if daemon:
        pid = os.fork()
        if pid > 0:
            PID_PATH.write_text(str(pid))
            print(f"cgwatcher daemon started (PID {pid})")
            print(f"  Log: {LOG_PATH}")
            print(f"  Stop: kill $(cat {PID_PATH})")
            return
        os.setsid()

    run_loop(rules, scheduler)


if __name__ == "__main__":
    main()
