#!/bin/bash
# Quick overview: which processes are in which cgroup slice.
# Usage: ./cgstatus.sh

SEP="----------------------------------------------------------------------"
echo ""
echo "$SEP"
printf "%-12s %-10s %-8s  %s\n" "CLASS" "WEIGHT" "QUOTA" "PROCESSES"
echo "$SEP"

for slice in simulator streamer tools; do
    weight=$(systemctl --user show "${slice}.slice" --property=CPUWeight --value 2>/dev/null)
    quota=$(systemctl --user show "${slice}.slice" --property=CPUQuotaPerSecUSec --value 2>/dev/null)

    [ -z "$weight" ] && weight="?"
    [ "$weight" = "[not set]" ] && weight="(default)"
    # Convert quota from seconds to percentage (9.6s = 960% = 60% of 16 CPUs)
    if [ "$quota" = "infinity" ]; then
        quota="--"
    elif [ -n "$quota" ]; then
        # Strip trailing 's', multiply by 100, divide by num CPUs
        secs=$(echo "$quota" | sed 's/s$//')
        pct=$(awk "BEGIN {printf \"%.0f%%\", $secs * 100 / $(nproc)}")
        quota="$pct"
    fi

    # Find PIDs in this slice's cgroup
    cg_dir=$(find /sys/fs/cgroup/user.slice/user-$(id -u).slice -maxdepth 1 -name "${slice}.slice" -type d 2>/dev/null)
    procs=""
    if [ -n "$cg_dir" ] && [ -f "$cg_dir/cgroup.procs" ]; then
        while IFS= read -r pid; do
            name=$(cat "/proc/$pid/comm" 2>/dev/null)
            [ -n "$name" ] && procs="$procs $name($pid)"
        done < "$cg_dir/cgroup.procs"
    fi

    [ -z "$procs" ] && procs="(empty)"
    printf "%-12s %-10s %-8s %s\n" "$slice" "$weight" "$quota" "$procs"
done

echo "$SEP"
echo ""
