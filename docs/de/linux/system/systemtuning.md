---
description: "Kernel-Tuning für X-Plane unter Linux: Zwei Profile für Standard- und Liquorix-Kernel — CPU-Governor, C-States, Interrupt-Shielding und NVMe-Powermanagement."
---
# Systemtuning für X-Plane

!!! warning "Work in Progress"
    Die Parameter für das Kernel-Tuning sind aktuell noch in der Überprüfung und funktionieren möglicherweise nicht alle wie beschrieben. Änderungen vorbehalten.

## Distributionen und ihre Zielausrichtung

Linux-Distributionen unterscheiden sich nicht nur in Paketmanager und Desktop-Umgebung, sondern vor allem in der **Abstimmung zwischen Kernel und Systemsoftware**. Jede Distribution trifft Konfigurationsentscheidungen für einen bestimmten Einsatzzweck:

- **Allzweck-Distributionen** (Debian, Ubuntu, Fedora) — optimieren auf Stabilität und breite Hardwarekompatibilität. Der Kernel ist konservativ konfiguriert, Energiesparen hat hohe Priorität.
- **Gaming-/Multimedia-Distributionen** (Nobara, Pop!_OS) — liefern bereits angepasste [Kernel-Parameter](../../glossary.md#kernel-parameter), Scheduler-Einstellungen und Treiber-Konfigurationen für niedrige [Latenz](../../glossary.md#latenz).
- **Audioproduktion** (Ubuntu Studio, AV Linux) — setzen auf Realtime-Kernel und priorisieren Audio-Pipelines.
- **Server-Distributionen** (Debian Server, Rocky Linux) — maximieren Durchsatz und Stabilität unter Dauerlast.

Das Zusammenspiel aus Kernel-Version, Scheduler-Konfiguration, Energieverwaltung, Treibern und [sysctl](../../glossary.md#sysctl)-Parametern ergibt das Systemverhalten. Distributionen, die bereits auf niedrige Latenz oder Gaming optimiert sind, bringen viele der hier beschriebenen Einstellungen bereits mit.

!!! info "Debian als Basis"
    Die folgenden Anleitungen beziehen sich auf **Debian** (Trixie/13) als Ausgangspunkt — eine Allzweck-Distribution, die für allgemeine Nutzung keine Anpassung erfordert, aber für latenzsensitive Anwendungen wie X-Plane gezielt optimiert werden kann. Der Standardkernel wird dabei durch den optimierten [Liquorix Kernel](../optimizations/liquorix.md) ersetzt.

    Wer eine bereits getunte Distribution wie Nobara oder Ubuntu Studio verwendet, sollte die Empfehlungen **nicht pauschal übernehmen**. Dort kann ein Kerneltausch bestehende Optimierungen zerstören, und doppeltes Tuning führt oft zu schlechteren Ergebnissen. In diesem Fall ist es sinnvoller, einzelne Parameter gezielt zu prüfen, anstatt das gesamte Profil anzuwenden.

Warum Latenz für X-Plane wichtiger ist als Durchsatz und welche Systemquellen Latenz erzeugen, beschreibt das Kapitel [Latenz und Vorhersagbarkeit](../../fundamentals/performance/latency.md).

## Zwei Optimierungsmodelle

Die richtige Tuning-Strategie hängt vom Kernel ab. Standardkernel und Liquorix verfolgen grundlegend verschiedene Ansätze:

**Standardkernel** = offener Regelkreis → Reaktion muss erzwungen werden

Der generische Debian-Kernel priorisiert Fairness und Durchsatz. Er reagiert konservativ auf Lastveränderungen. Tuning bedeutet hier: der Anwendung explizit Vorrang einräumen.

**Liquorix** = geschlossener Regelkreis → Störungen müssen entfernt werden

Liquorix nutzt den [PDS](../../glossary.md#pds-priority-and-deadline-based-skiplist)-Scheduler (Priority and Deadline based Skiplist) mit kürzeren [Preemption](../../glossary.md#preemption)-Fenstern und einer Timer-Frequenz von 1000 Hz. Er reagiert selbstständig auf Laständerungen. Tuning bedeutet hier: externe Störquellen minimieren.

!!! warning "Gleiche Einstellung, gegenteiliges Ergebnis"
    Identische Parameter können je nach Kernel gegensätzliche Effekte haben. Ein `performance`-Governor hilft beim Standardkernel, kann aber unter Liquorix kontraproduktiv sein (thermischer Spielraum geht verloren). CPU-Isolation hilft beim Standardkernel, verhindert aber unter Liquorix die adaptive Optimierung.

| Parameterbereich | Standardkernel | Liquorix |
|---|---|---|
| CPU-Takt | Konstant hoch | Adaptiv |
| Scheduler-Einfluss | Verstärken | Nicht einschränken |
| CPU-Bindung | Möglich | Vermeiden |
| Interrupt-Routing | Optional | Wesentlich |
| Energiesparen | Begrenzen | Fein abstimmen |
| Writeback | Neutral | Glätten |

**Welchen Kernel nutze ich?**

```bash
uname -r
```

- Enthält `liquorix` → Profil B (Liquorix)
- Sonst → Profil A (Standardkernel)

Für die Installation von Liquorix siehe [Liquorix Kernel](../optimizations/liquorix.md).

## Profil A: Debian Standardkernel

**Ziel:** Scheduler reagiert konservativ → Anwendung aktiv bevorzugen.

### CPU-Takt und Schlafzustände

**Governor**

Den [Governor](../../glossary.md#cpu-governor) auf festen Hochleistungstakt setzen, um Reaktionszeit zu verkürzen und fehlende Lastvorhersage zu kompensieren.

Sofort umschalten:

```bash
echo performance | sudo tee /sys/devices/system/cpu/cpu*/cpufreq/scaling_governor
```

Überprüfung:

```bash
cat /sys/devices/system/cpu/cpu0/cpufreq/scaling_governor
```

Für dauerhafte Einstellung über Neustarts hinweg in `/etc/default/grub` den Parameter `GRUB_CMDLINE_LINUX_DEFAULT` erweitern:

```
cpufreq.default_governor=performance
```

```bash
sudo update-grub
```

**Schlafzustände begrenzen**

In `/etc/default/grub` den Parameter `GRUB_CMDLINE_LINUX_DEFAULT` erweitern:

```
processor.max_cstate=2
```

!!! note "AMD vs. Intel"
    **AMD Zen:** Exportiert per ACPI nur C1 und C2 an das OS. Tiefere Hardware-[C-States](../../glossary.md#c-states-cpu-idle-states) (C6) werden firmware-autonom verwaltet. Der Wert `2` stellt sicher, dass alle verfügbaren OS-sichtbaren C-States genutzt werden. Zusätzlich kann `amd_pstate=active` für moderne Zen-Prozessoren mit CPPC-Unterstützung gesetzt werden.

    **Intel:** Tiefere ACPI-C-States (C3, C6, C8, C10) sind sichtbar und steuerbar. Hier kann `processor.max_cstate=3` sinnvoll sein, um tiefe Zustände zu begrenzen. Auf Systemen mit dem `intel_idle`-Treiber (Standard bei modernem Intel) wird ggf. zusätzlich `intel_idle.max_cstate` benötigt.

Anwenden:

```bash
sudo update-grub
```

Neustart erforderlich.

### Anwendung bevorzugen (Affinität + Priorität)

Ein Starter-Script, das X-Plane auf bestimmte Kerne bindet und mit erhöhter Scheduling-Priorität startet:

```bash title="~/run_xplane.sh"
#!/bin/bash
exec taskset -c 4-11 chrt -f 45 "$@"
```

```bash
chmod +x ~/run_xplane.sh
```

Starten:

```bash
~/run_xplane.sh /pfad/zu/X-Plane-x86_64
```

!!! note "Zur Priorität"
    `SCHED_FIFO` Priorität 45 liegt unterhalb der Standardpriorität von Kernel-Threaded-IRQ-Handlern (Priorität 50), aber deutlich über normalen Prozessen. Werte über 50 können Kernel-Housekeeping-Threads preemptieren und zu Instabilität führen.

**Optional: CPU-Isolation**

Nur sinnvoll bei hoher Hintergrundlast. In `/etc/default/grub` ergänzen:

```
isolcpus=4-11
```

!!! note "Hinweis zur Abkündigung"
    `isolcpus` ist in der Kernel-Dokumentation als deprecated gekennzeichnet. Die modernere Alternative sind **cpusets**, die zur Laufzeit ohne Neustart konfiguriert werden können. Für einen einfachen Desktop-Anwendungsfall bleibt `isolcpus` jedoch die unkompliziertere Variante.

**Speicherverhalten**

```ini title="/etc/sysctl.d/60-desktop.conf"
vm.swappiness=20
vm.dirty_ratio=20
vm.dirty_background_ratio=10
vm.vfs_cache_pressure=100
```

Anwenden:

```bash
sudo sysctl --system
```

### Ergebnis Profil A

Der Kernel reagiert schneller, da Rechenzeit für die Anwendung garantiert wird.

---

## Profil B: Liquorix Kernel

**Ziel:** Scheduler arbeitet bereits optimal → externe Störungen entfernen.

**Wichtig:** Kein `isolcpus`, kein `taskset` — diese würden die adaptive Optimierung des Schedulers verhindern.

### CPU-Takt und Energiesteuerung

**Governor**

Sofort umschalten:

```bash
echo ondemand | sudo tee /sys/devices/system/cpu/cpu*/cpufreq/scaling_governor
```

Überprüfung:

```bash
cat /sys/devices/system/cpu/cpu0/cpufreq/scaling_governor
```

!!! note "Warum `ondemand` statt `schedutil`?"
    `schedutil` bezieht Auslastungssignale (PELT — Per-Entity Load Tracking) vom Mainline-CFS/[EEVDF](../../glossary.md#eevdf-earliest-eligible-virtual-deadline-first)-Scheduler. Liquorix nutzt jedoch den alternativen PDS-Scheduler, der diese Signale nicht korrekt liefert — `schedutil` fixiert den CPU-Takt auf Maximalfrequenz und bietet damit keinen Vorteil gegenüber dem `performance`-Governor. `ondemand` passt den CPU-Takt ebenfalls lastabhängig an, arbeitet aber unabhängig vom Scheduler.

Optional Energy Performance Preference setzen:

```bash
echo balance_performance | sudo tee /sys/devices/system/cpu/cpu*/cpufreq/energy_performance_preference
```

Für dauerhafte Einstellung über Neustarts hinweg in `/etc/default/grub` den Parameter `GRUB_CMDLINE_LINUX_DEFAULT` erweitern:

```
cpufreq.default_governor=ondemand
```

```bash
sudo update-grub
```

!!! tip "Persistenz"
    Die Terminal-Befehle gelten bis zum nächsten Neustart. Die GRUB-Variante macht die Einstellung dauerhaft. Für permanente EPP-Einstellung eine [systemd](../../glossary.md#systemd)-Unit oder udev-Regel erstellen.

**C-States und Energiesteuerung**

!!! note "AMD vs. Intel"
    **AMD Zen:** Nur C1/C2 sind OS-sichtbar — keine C-State-Begrenzung nötig. Tiefere Hardware-C-States helfen dem thermischen Budget.

    **Intel:** `processor.max_cstate=5` erlaubt moderate Schlafzustände und vermeidet die tiefsten Zustände. Auf Systemen mit `intel_idle` (Standard) zusätzlich `intel_idle.max_cstate=5` setzen.

In `/etc/default/grub` — für Intel:

```
processor.max_cstate=5
```

### Interrupt-Shielding

Die wichtigste Maßnahme unter Liquorix. Hardware-Interrupts auf die ersten Kerne konzentrieren, damit der Scheduler die restlichen Kerne ungestört für die Anwendung nutzen kann.

!!! warning "IRQ-Affinität auf modernen Kerneln"
    Moderne Kernel verwenden Managed Interrupts für MSI-X-Geräte ([NVMe](../../glossary.md#nvme-non-volatile-memory-express), GPU, etc.). Der Kernel steuert die Affinitätszuordnung dieser IRQs, und Schreibzugriffe auf `/proc/irq/*/smp_affinity` werden vom Kernel abgelehnt — unabhängig von der Kernel-Variante. Das ist kein Liquorix-Spezifikum, sondern ein allgemeiner Kernel-Mechanismus.

    Der Userspace-Daemon [`irqbalance`](../../glossary.md#irqbalance) übernimmt die Verteilung nicht verwalteter IRQs und berücksichtigt diese Kernel-Einschränkungen automatisch.

Für nicht verwaltete IRQs bietet `irqbalance` eine effektive CPU-Ausgrenzung. In `/etc/default/irqbalance` eintragen:

```
IRQBALANCE_BANNED_CPULIST="4-15"
```

Das schließt die angegebenen Kerne von der Interrupt-Verteilung aus. CPU 0–3 = System/Interrupts, Rest = Anwendung.

```bash
sudo systemctl enable --now irqbalance
```

!!! tip "Warum irqbalance statt manueller Affinität?"
    `irqbalance` mit `BANNED_CPULIST` ist wartungsfreundlicher als manuelle Affinität: Es passt sich automatisch an neue Hardware-IRQs an und verteilt die Last intelligent auf die erlaubten Kerne.

### NVMe Energiesparen deaktivieren

NVMe-SSDs können im Energiesparmodus Aufwachlatenzen im Millisekundenbereich haben — länger als ein kompletter Frame bei 60 Hz. Die Exit-Latenzen variieren je nach Hersteller und Energiesparstufe.

Um NVMe-Energiesparen zu deaktivieren, in `/etc/default/grub` den Parameter `GRUB_CMDLINE_LINUX_DEFAULT` erweitern:

```
nvme_core.default_ps_max_latency_us=0
```

```bash
sudo update-grub
```

Neustart erforderlich.

!!! note "Laufzeitänderungen"
    Der sysfs-Parameter `/sys/module/nvme_core/parameters/default_ps_max_latency_us` wirkt nur auf **neu initialisierte** NVMe-Geräte. Für bereits aktive Geräte per-Device PM QOS verwenden:
    ```bash
    for dev in /sys/class/nvme/nvme*/device/power/pm_qos_latency_tolerance_us; do echo 0 | sudo tee "$dev"; done
    ```
    Die GRUB-Methode ist der zuverlässigste Weg.

**Speicher-Writeback glätten**

```ini title="/etc/sysctl.d/99-lowlatency.conf"
vm.swappiness=10
vm.dirty_background_ratio=3
vm.dirty_ratio=10
vm.vfs_cache_pressure=100
```

Anwenden:

```bash
sudo sysctl --system
```

**Leichte Priorisierung**

Unter Liquorix genügt eine moderate `nice`-Anpassung:

```bash title="~/run_xplane.sh"
#!/bin/bash
exec nice -n -10 "$@"
```

### Ergebnis Profil B

Keine maximale Leistung — sondern minimale Frame-Time-Spikes. Der Scheduler kann frei optimieren, weil äußere Störungen reduziert sind.

---

## Zwischen Kerneln wechseln

Wer beide Kernel parallel installiert hat (Standard-Debian + Liquorix), kann beim Booten wählen, welcher geladen wird. So lässt sich das passende Tuning-Profil je nach Einsatzzweck nutzen — ohne einen der Kernel deinstallieren zu müssen.

**Installierte Kernel anzeigen**

```bash
dpkg --list | grep linux-image
```

**GRUB-Menüeinträge ermitteln**

[GRUB](../../glossary.md#grub-grand-unified-bootloader) nummeriert die Einträge ab 0. Kernel im Untermenü „Advanced options" werden mit `>` adressiert:

```bash
grep -E "menuentry |submenu " /boot/grub/grub.cfg | head -20
```

Das Format für Untermenü-Einträge ist `"Übermenü>Eintrag"`, z.B.:

```
"Advanced options for Debian GNU/Linux>Debian GNU/Linux, with Linux 6.12.6-1-liquorix-amd64"
```

**Einmaliger Wechsel**

!!! note "Voraussetzung"
    `grub-reboot` erfordert `GRUB_DEFAULT=saved` in `/etc/default/grub` (siehe [Dauerhafter Wechsel](#dauerhafter-wechsel) weiter unten). Ohne diese Einstellung ignoriert GRUB den gespeicherten Eintrag.

Beim nächsten Neustart einen bestimmten Kernel starten, danach wieder den Standard:

```bash
sudo grub-reboot "Advanced options for Debian GNU/Linux>Debian GNU/Linux, with Linux 6.12.6-1-liquorix-amd64"
sudo reboot
```

### Dauerhafter Wechsel

Den Standard-Boot-Eintrag permanent ändern:

1. In `/etc/default/grub` setzen:

    ```
    GRUB_DEFAULT=saved
    ```

2. Gewünschten Kernel als Standard setzen:

    ```bash
    sudo grub-set-default "Advanced options for Debian GNU/Linux>Debian GNU/Linux, with Linux 6.12.6-1-liquorix-amd64"
    sudo update-grub
    ```

Nach dieser Einrichtung funktioniert auch `grub-reboot` für einmalige Abweichungen vom gespeicherten Standard.

**Aktuellen Kernel prüfen**

```bash
uname -r
```

### Was lässt sich zur Laufzeit umschalten?

Nicht alle Einstellungen erfordern einen Neustart. Die folgende Tabelle zeigt, welche Parameter im laufenden Betrieb geändert werden können:

| Parameter | Zur Laufzeit änderbar? | Methode |
|---|---|---|
| Governor | Ja | `echo ... \| sudo tee /sys/devices/system/cpu/cpu*/cpufreq/scaling_governor` |
| NVMe [APST](../../glossary.md#apst-autonomous-power-state-transitions) | **Nein** | Nur per GRUB — sysfs-Parameter wirkt nur auf neu initialisierte Geräte |
| sysctl (vm.*) | Ja | `sudo sysctl --system` |
| irqbalance-Dienst | Ja | `sudo systemctl stop/start irqbalance` |
| nice / chrt / taskset | Ja | Wird beim Anwendungsstart gesetzt |
| IRQ-Affinität | **Nein** (Managed IRQs) | Kernel verwaltet MSI-X-Affinität — `irqbalance` mit `BANNED_CPULIST` für nicht verwaltete IRQs nutzen |
| processor.max_cstate | **Nein** | Nur per GRUB, Neustart nötig |
| isolcpus | **Nein** | Nur per GRUB (Alternative: cpusets) |

!!! warning "Tuning-Profil anpassen"
    Nach einem Kernel-Wechsel das passende Profil verwenden: [Profil A](#profil-a-debian-standardkernel) für den Standardkernel, [Profil B](#profil-b-liquorix-kernel) für Liquorix. Die Governor- und sysctl-Einstellungen unterscheiden sich grundlegend — falsche Kombination verschlechtert die Performance.

---

## Gesamtvergleich

| Bereich | Standardkernel | Liquorix |
|---|---|---|
| Governor | `performance` | `ondemand` |
| CPU-Bindung | Ja (`taskset`) | Nein |
| Interrupt-Trennung | Optional | Wichtig |
| NVMe APST | Optional deaktivieren | Deaktiviert |
| Writeback | Normal | Geglättet |
| Priorisierung | `SCHED_FIFO` + Affinität | `nice -n -10` |
| **Ziel** | **Reaktionszeit erzwingen** | **Störungen verhindern** |

!!! info "Kernregel"
    **Standardkernel braucht Priorisierung — Liquorix braucht Ruhe.**

    Wenn beide Kernel gleich konfiguriert werden, verschlechtert sich das Ergebnis fast immer.

---

## Weiterführende Kapitel

| Thema | Seite | Schwerpunkt |
|---|---|---|
| Monitoring | [Monitoring](systemtools.md) | Tuning-Maßnahmen verifizieren mit turbostat, mpstat, ioping |
| Warum Latenz zählt | [Warum Latenz zählt](latency.md) | Motivation und Kontext für Kernel-Tuning |
| Latenz und Vorhersagbarkeit | [Latenz und Vorhersagbarkeit](../../fundamentals/performance/latency.md) | Theoretische Grundlagen — Latenzquellen und Messung |
| Liquorix Kernel | [Liquorix Kernel](../optimizations/liquorix.md) | Installation und Features des Low-Latency-Kernels |
| Nvidia-Treiber | [Nvidia-Treiber](../optimizations/nvidia.md) | Treiberinstallation, KMS und Kernel-Parameter |
| Performance-Analyse | [Performance-Analyse](../../xplane/setup_diagnose/performance.md) | X-Plane-spezifische Performance-Diagnostik |

---

## Quellen

Die wichtigsten Quellen zu den auf dieser Seite behandelten Themen:

- [CPU Performance Scaling — Linux Kernel Documentation](https://docs.kernel.org/admin-guide/pm/cpufreq.html) — CPU-Frequenz-Governor und Skalierungstreiber
- [CPU Idle Time Management — Linux Kernel Documentation](https://docs.kernel.org/admin-guide/pm/cpuidle.html) — C-States und Idle-Treiber (acpi_idle, intel_idle)
- [amd-pstate CPU Performance Scaling Driver — Linux Kernel Documentation](https://docs.kernel.org/admin-guide/pm/amd-pstate.html) — AMD P-State-Treiber und Modi
- [Liquorix Kernel](https://liquorix.net/) — PDS-Scheduler, Zen Interactive Tuning, Kernel-Features
- [irqbalance(1) — Debian Man Page](https://manpages.debian.org/testing/irqbalance/irqbalance.1.en.html) — IRQ-Verteilungs-Daemon-Konfiguration
- [Solid State Drive/NVMe — Arch Wiki](https://wiki.archlinux.org/title/Solid_state_drive/NVMe) — NVMe-Energieverwaltung (APST)
- [sysctl.d(5) — Linux Man Page](https://man7.org/linux/man-pages/man5/sysctl.d.5.html) — sysctl Drop-in-Konfiguration
- [GNU GRUB Manual](https://www.gnu.org/software/grub/manual/grub/html_node/Simple-configuration.html) — GRUB-Konfiguration und Kernel-Auswahl
