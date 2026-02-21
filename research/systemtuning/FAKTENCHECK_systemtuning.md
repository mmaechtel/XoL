# Faktencheck: System Tuning for X-Plane (EN + DE)

**Datum:** 2026-02-21
**Geprüfte Seiten:** `docs/en/linux/system/systemtuning.md`, `docs/de/linux/system/systemtuning.md`
**Primärquellen verifiziert:** docs.kernel.org, liquorix.net, github.com/damentz/liquorix-package, gitlab.com/alfredchen/linux-prjc, manpages.debian.org, wiki.archlinux.org, lwn.net, man7.org, gnu.org

---

## Fehler (2) — Korrekturbedarf

### 1. Intel C-States "visible and controllable" — zu stark formuliert
**Datei:** `systemtuning.md:103-105 (EN), :103-105 (DE)`
**Behauptung:** "Intel: Deeper ACPI C-states (C3, C6, C8, C10) are visible and controllable."
**Befund:** Intel-Datasheets bestätigen, dass C2/C3 nicht explizit per Software angefordert werden können ("PKG C2 and C3 can not be requested explicitly by the software"). Der `intel_idle`-Treiber ignoriert BIOS-C-State-Einstellungen und nutzt eigene Tabellen. Die Zustände sind sichtbar in sysfs, aber nicht direkt "controllable" — sie lassen sich nur über `max_cstate` begrenzen.
**Korrektur:** "visible and controllable" → "visible and can be limited via `max_cstate` parameters"
**Quellen:** [Intel 12th Gen Datasheet](https://edc.intel.com/content/www/us/en/design/ipla/software-development-platforms/client/platforms/alder-lake-desktop/12th-generation-intel-core-processors-datasheet-volume-1-of-2/010/package-c-states/), [intel_idle Kernel Docs](https://docs.kernel.org/admin-guide/pm/intel_idle.html)

### 2. vfs_cache_pressure Inkonsistenz zwischen systemtuning.md und swap.md
**Datei:** `systemtuning.md:154,279 (EN), :154,279 (DE)` und `swap.md:315 (EN), :315 (DE)`
**Behauptung:** systemtuning.md verwendet `vm.vfs_cache_pressure=100` in beiden Profilen. swap.md empfiehlt `50` in der Kernel-Parameter-Tabelle.
**Befund:** 100 ist der Kernel-Default. swap.md empfiehlt 50 mit Begründung "Favor keeping inode/dentry caches for scenery file lookups". Für X-Plane mit häufigen Szenerie-Datei-Zugriffen ist 50 die bessere Wahl. Kernel-Docs: "Decreasing vfs_cache_pressure causes the kernel to prefer to retain dentry and inode caches."
**Korrektur:** In systemtuning.md beide Profile auf `vm.vfs_cache_pressure=50` ändern, konsistent mit swap.md.
**Quellen:** [/proc/sys/vm/ — Kernel Docs](https://docs.kernel.org/admin-guide/sysctl/vm.html)

---

## Nuancen (5) — verbesserbar, aber akzeptabel

### 1. Profile A Memory-Werte sind größtenteils Kernel-Defaults
**Datei:** `systemtuning.md:150-155 (EN)`
**Befund:** 3 von 4 Werten (`dirty_ratio=20`, `dirty_background_ratio=10`, `vfs_cache_pressure=100`) sind identisch mit Kernel-Defaults. Nur `swappiness=20` weicht ab. Der Leser wird nicht darauf hingewiesen. Option: "These values match kernel defaults except for swappiness" ergänzen, oder die Werte tatsächlich anpassen.

### 2. NVMe APST Runtime-Tabelle widerspricht Seiteninhalt
**Datei:** `systemtuning.md:371 (EN)`
**Befund:** Die Runtime-Tabelle sagt "No" für NVMe APST, aber Zeile 267-271 dokumentiert eine funktionierende Runtime-Methode über PM QOS (`pm_qos_latency_tolerance_us`). Tabelle sollte "Partially" sagen mit Verweis auf PM QOS.

### 3. dirty_ratio / dirty_background_ratio ohne Erklärung
**Datei:** `systemtuning.md:150-155, 275-282 (EN)`
**Befund:** Beide Profile listen die Parameter ohne Erklärung. Profile B heißt "Smooth Memory Writeback", was den Zweck andeutet, aber `dirty_background_ratio=3` vs. `dirty_background_ratio=10` wird nicht erklärt. Kurze Inline-Erklärung ("background flusher starts at 3% dirty pages for more frequent, smaller writes") wäre hilfreich.

### 4. PM QOS sysfs-Pfad hardware-abhängig
**Datei:** `systemtuning.md:268-270 (EN)`
**Befund:** Der Pfad `/sys/class/nvme/nvme*/device/power/pm_qos_latency_tolerance_us` ist korrekt für NVMe-Geräte mit PCI PM QOS-Support, aber die Verfügbarkeit hängt von Hardware und Kernel-Version ab. Ein "if available" wäre präziser.

### 5. schedutil in Liquorix nicht nur dysfunktional, sondern komplett entfernt
**Datei:** `systemtuning.md:192 (EN)`
**Befund:** Die Seite erklärt, warum schedutil mit PDS nicht korrekt funktioniert. Tatsächlich hat Liquorix 6.18 schedutil komplett aus dem Kernel entfernt (`# CONFIG_CPU_FREQ_GOV_SCHEDUTIL is not set`). Ein Hinweis darauf würde die Empfehlung noch stärker untermauern.
**Quelle:** [Liquorix 6.18 Kernel Config](https://github.com/damentz/liquorix-package/blob/6.18/master/linux-liquorix/debian/config/kernelarch-x86/config-arch-64)

---

## Korrekt (30) — keine Änderung nötig

| # | Behauptung | Quelle |
|---|------------|--------|
| 1 | PDS scheduler in Liquorix | [Liquorix kernel config](https://github.com/damentz/liquorix-package): `CONFIG_SCHED_PDS=y` |
| 2 | 1000 Hz Timer-Frequenz | Kernel config: `CONFIG_HZ=1000`, liquorix.net |
| 3 | schedutil/PELT-Inkompatibilität mit PDS | [Project C Issue #12](https://gitlab.com/alfredchen/linux-prjc/-/issues/12) |
| 4 | ondemand-Empfehlung für Liquorix | Project C Issue #12, Liquorix Release Notes |
| 5 | Full Kernel Preemption (CONFIG_PREEMPT=y) | Liquorix kernel config |
| 6 | Liquorix aktiv gewartet (6.18-14, Feb 2026) | liquorix.net, GitHub releases |
| 7 | AMD Zen: Nur C1/C2 OS-sichtbar, C6 firmware-verwaltet | [arXiv:2108.00808](https://arxiv.org/pdf/2108.00808), CoreFreq, Gentoo Wiki |
| 8 | amd_pstate=active für CPPC-fähige Zen-Prozessoren | [Kernel Docs amd-pstate](https://docs.kernel.org/admin-guide/pm/amd-pstate.html) |
| 9 | SCHED_FIFO 45 unter Kernel-IRQ-Priority 50 | [LWN: sched_set_fifo()](https://lwn.net/Articles/818388/), kernel/irq/manage.c |
| 10 | isolcpus als deprecated gekennzeichnet | [Kernel Parameters Docs](https://docs.kernel.org/admin-guide/kernel-parameters.html) |
| 11 | Managed Interrupts: smp_affinity writes rejected (-EPERM) | kernel/irq/proc.c, [Red Hat KB](https://access.redhat.com/solutions/4819541) |
| 12 | IRQBALANCE_BANNED_CPULIST Syntax korrekt | [irqbalance(1) Manpage](https://manpages.debian.org/testing/irqbalance/irqbalance.1.en.html) |
| 13 | NVMe Aufwachlatenzen im Millisekundenbereich | [Arch Wiki NVMe](https://wiki.archlinux.org/title/Solid_state_drive/NVMe), MS NVMe Docs |
| 14 | nvme_core.default_ps_max_latency_us=0 funktioniert | Arch Wiki, Kernel Source |
| 15 | processor.max_cstate + intel_idle.max_cstate nötig | [intel_idle Kernel Docs](https://docs.kernel.org/admin-guide/pm/intel_idle.html) |
| 16 | GRUB_DEFAULT=saved für grub-reboot | [Debian Wiki GrubReboot](https://wiki.debian.org/GrubReboot), GNU GRUB Manual |
| 17 | vm.swappiness=20 Profile A / 10 Profile B | Konsistent mit swap.md (10-20 für Disk-Swap) |
| 18 | dirty_background_ratio=3 für smootheres Writeback | [SUSE Tuning Guide](https://documentation.suse.com/sles/15-SP7/html/SLES-all/cha-tuning-memory.html) |
| 19 | Governor zur Laufzeit änderbar | [Kernel Docs cpufreq](https://docs.kernel.org/admin-guide/pm/cpufreq.html) |
| 20 | sysctl (vm.*) zur Laufzeit änderbar | Kernel Docs |
| 21 | irqbalance zur Laufzeit steuerbar | Systemd-Service |
| 22 | nice/chrt/taskset zur Laufzeit anwendbar | Userspace-Tools |
| 23 | IRQ-Affinität nicht änderbar für managed IRQs | Kernel Source, Red Hat KB |
| 24 | processor.max_cstate nicht zur Laufzeit änderbar | intel_idle Kernel Docs |
| 25 | isolcpus nicht zur Laufzeit änderbar | Kernel Docs, Red Hat KB |
| 26 | NVMe sysfs-Parameter nur für neue Geräte wirksam | Kernel Source: MODULE_PARM_DESC |
| 27 | Alle 8 Quellen-URLs erreichbar und aktuell | Geprüft am 2026-02-21 |
| 28 | Open-loop (Standardkernel) vs. closed-loop (Liquorix) Modell | Research-Paper, funktional korrekt |
| 29 | performance Governor für Standardkernel empfohlen | Konsistent mit Research-Paper und Praxisempfehlungen |
| 30 | nice -n -10 für Liquorix statt SCHED_FIFO | Vermeidet Scheduler-Einschränkung, korrekte Strategie |
