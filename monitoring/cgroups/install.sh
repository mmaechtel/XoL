#!/bin/bash
# Install cgroup CPU limit slices + cgwatcher.
# No sudo needed — runs entirely in user scope.
#
# Classes:
#   simulator  CPUWeight=1000  no limit   (X-Plane)
#   streamer   CPUWeight=300   max 60%    (xearthlayer, autoortho)
#   tools      CPUWeight=100   max 20%    (qemu-system)

set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

echo "=== cgroup CPU limit setup ==="
echo ""

# ── 1. Install user slices ──
USER_SLICE_DIR="$HOME/.config/systemd/user"
mkdir -p "$USER_SLICE_DIR"

for slice in simulator streamer tools; do
    cp "$SCRIPT_DIR/${slice}.slice" "$USER_SLICE_DIR/"
    echo "[OK] Installed ${slice}.slice"
done

systemctl --user daemon-reload
echo ""

# ── 2. Verify slices ──
echo "=== Slice verification ==="
for slice in simulator streamer tools; do
    weight=$(systemctl --user show "${slice}.slice" --property=CPUWeight --value 2>/dev/null)
    quota=$(systemctl --user show "${slice}.slice" --property=CPUQuotaPerSecUSec --value 2>/dev/null)
    echo "  ${slice}: CPUWeight=${weight:-?}  CPUQuota=${quota:-unlimited}"
done
echo ""

# ── 3. cgwatcher info ──
echo "=== cgwatcher ==="
echo "The watcher auto-classifies running processes by name."
echo ""
echo "  Start (foreground):  python3 $SCRIPT_DIR/cgwatcher.py"
echo "  Start (daemon):      python3 $SCRIPT_DIR/cgwatcher.py --daemon"
echo "  Single scan:         python3 $SCRIPT_DIR/cgwatcher.py --once"
echo "  Stop daemon:         kill \$(cat /tmp/cgwatcher.pid)"
echo ""

# ── 4. KVM note ──
echo "=== KVM (optional) ==="
echo "For KVM CPU limits via libvirt, edit the VM config:"
echo ""
echo "  sudo virsh edit win11"
echo ""
echo "Replace <cputune> with:"
echo "  <cputune>"
echo "    <shares>200</shares>"
echo "    <period>100000</period>"
echo "    <quota>320000</quota>"
echo "  </cputune>"
echo ""
echo "The cgwatcher also moves qemu-system into tools.slice"
echo "for user-level enforcement (works without virsh edit)."
echo ""

# ── Summary ──
echo "=== Summary ==="
echo "  simulator:  X-Plane           → 100% (all cores, highest prio)"
echo "  streamer:   xearthlayer et al → max 60% (9.6 cores)"
echo "  tools:      qemu-system et al → max 20% (3.2 cores)"
