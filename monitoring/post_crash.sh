#!/bin/bash
# post_crash.sh — Post-crash diagnostic collection.
#
# Run immediately after an X-Plane freeze or GPU crash to capture
# volatile system state before it is overwritten by subsequent events.
#
# Collects:
#   1) NVIDIA bug report (comprehensive GPU state dump)
#   2) Full kernel ring buffer (dmesg) with timestamps
#   3) Filtered journal: GPU-related kernel messages from the last 30 min
#
# Usage:
#   sudo bash post_crash.sh [-o DIR] [-h]
#
# Options:
#   -o, --outdir DIR   output directory (default: /tmp)
#   -h, --help         show this help
#
# Output files are timestamped so multiple crash captures don't overwrite.
# If nvidia-smi is hanging after a device loss, try:
#   sudo nvidia-bug-report.sh --safe-mode

set -euo pipefail

# ─── Argument parsing ────────────────────────────────────────────────

OUTDIR="/tmp"

while [[ $# -gt 0 ]]; do
    case "$1" in
        -o|--outdir) OUTDIR="$2"; shift 2 ;;
        -h|--help)
            sed -n '2,/^$/{ s/^# //; s/^#//; p }' "$0"
            exit 0
            ;;
        *) echo "Unknown option: $1 (use --help)"; exit 1 ;;
    esac
done

mkdir -p "$OUTDIR"

TS=$(date +%s)
echo "=== Post-Crash Diagnostics: $(date) ==="
echo "Output: $OUTDIR"
echo ""

# 1) NVIDIA bug report (comprehensive GPU state dump)
echo "[1/3] Collecting NVIDIA bug report..."
if command -v nvidia-bug-report.sh &>/dev/null; then
    sudo nvidia-bug-report.sh --output-file "${OUTDIR}/nvidia-crash-${TS}" \
        && echo "  -> ${OUTDIR}/nvidia-crash-${TS}.log.gz" \
        || echo "  [WARN] nvidia-bug-report.sh failed.  If nvidia-smi hangs, try:" \
        && echo "         sudo nvidia-bug-report.sh --safe-mode"
else
    echo "  [SKIP] nvidia-bug-report.sh not found (not an NVIDIA system?)"
fi

# 2) Full dmesg with timestamps
echo "[2/3] Saving kernel ring buffer..."
dmesg -T > "${OUTDIR}/dmesg_crash_${TS}.log" \
    && echo "  -> ${OUTDIR}/dmesg_crash_${TS}.log" \
    || echo "  [WARN] dmesg capture failed (need root or dmesg permissions)"

# 3) Filtered journal (GPU-related kernel messages, last 30 min)
echo "[3/3] Saving GPU journal entries (last 30 min)..."
journalctl -k --since "30 min ago" --grep="NVRM|Xid|drm|nvidia|amdgpu" \
    > "${OUTDIR}/journal_crash_${TS}.log" 2>/dev/null \
    && echo "  -> ${OUTDIR}/journal_crash_${TS}.log" \
    || echo "  [WARN] journalctl capture failed (may need journal access)"

echo ""
echo "=== Collection complete ==="
echo "Files:"
ls -lh "${OUTDIR}"/*crash*${TS}* 2>/dev/null || echo "  (no files found)"
echo ""
echo "Next steps:"
echo "  - Check dmesg for Xid errors (NVIDIA) or amdgpu timeouts"
echo "  - If crash happened during monitoring: check sysmon CSV for spikes"
echo "  - Share nvidia-crash-*.log.gz and dmesg when reporting bugs"
