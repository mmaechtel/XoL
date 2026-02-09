# Systemtuning für X-Plane

!!! danger "Work in Progress"
    Die Parameter für das Kernel-Tuning sind aktuell noch in der Überprüfung und funktionieren möglicherweise nicht alle wie beschrieben. Änderungen vorbehalten.

## Distributionen und ihre Zielausrichtung

Linux-Distributionen unterscheiden sich nicht nur in Paketmanager und Desktop-Umgebung, sondern vor allem in der **Abstimmung zwischen Kernel und Systemsoftware**. Jede Distribution trifft Konfigurationsentscheidungen für einen bestimmten Einsatzzweck:

- **Allzweck-Distributionen** (Debian, Ubuntu, Fedora) — optimieren auf Stabilität und breite Hardwarekompatibilität. Der Kernel ist konservativ konfiguriert, Energiesparen hat hohe Priorität.
- **Gaming-/Multimedia-Distributionen** (Nobara, Pop!_OS) — liefern bereits angepasste Kernel-Parameter, Scheduler-Einstellungen und Treiber-Konfigurationen für niedrige Latenz.
- **Audioproduktion** (Ubuntu Studio, AV Linux) — setzen auf Realtime-Kernel und priorisieren Audio-Pipelines.
- **Server-Distributionen** (Debian Server, Rocky Linux) — maximieren Durchsatz und Stabilität unter Dauerlast.

Das Zusammenspiel aus Kernel-Version, Scheduler-Konfiguration, Energieverwaltung, Treibern und sysctl-Parametern ergibt das Systemverhalten. Distributionen, die bereits auf niedrige Latenz oder Gaming optimiert sind, bringen viele der hier beschriebenen Einstellungen bereits mit.

!!! info "Debian als Basis"
    Die folgenden Anleitungen beziehen sich auf **Debian** (Trixie/13) als Ausgangspunkt — eine Allzweck-Distribution, die für allgemeine Nutzung keine Anpassung erfordert, aber für latenzsensitive Anwendungen wie X-Plane gezielt optimiert werden kann. Der Standardkernel wird dabei durch den optimierten [Liquorix Kernel](liquorix.md) ersetzt.

    Wer eine bereits getunte Distribution wie Nobara oder Ubuntu Studio verwendet, sollte die Empfehlungen **nicht pauschal übernehmen**. Dort kann ein Kerneltausch bestehende Optimierungen zerstören, und doppeltes Tuning führt oft zu schlechteren Ergebnissen. In diesem Fall ist es sinnvoller, einzelne Parameter gezielt zu prüfen, anstatt das gesamte Profil anzuwenden.

## Performance und Latenz — ein wichtiger Unterschied

Wer von „Performance" spricht, meint oft hohe FPS. Das ist bei Shootern oder Rennspielen richtig — dort zählt Durchsatz: möglichst viele Bilder pro Sekunde. Bei einem Flugsimulator wie X-Plane liegt der Fall anders.

X-Plane berechnet eine komplexe Welt mit Physik, Wetter, Szenerie und Eingabegeräten. Einzelne Frames sind aufwändig, und die Ziel-Framerate liegt typisch bei 30–40 FPS. Entscheidend ist nicht der Durchschnitt, sondern die **Gleichmäßigkeit** — also die Frame-Time-Konsistenz. Ein System, das stabil 35 FPS liefert, fühlt sich besser an als eines, das zwischen 25 und 50 schwankt.

Die Ursache für Ungleichmäßigkeit ist in den meisten Fällen nicht fehlende Rechenleistung, sondern **Latenz** — kurze Verzögerungen durch Systemereignisse, die den Hauptthread unterbrechen.

Typische Symptome schlechter Latenz:

- Mikroruckler trotz stabiler CPU/GPU-Auslastung
- Verzögerte Eingabereaktion (Joystick, Ruderpedale)
- Inkonsistente Reaktionszeit bei gleicher Szene

**Kernaussage:** Bei X-Plane ist Latenzoptimierung wichtiger als Durchsatzmaximierung. Zeitliche Vorhersagbarkeit schlägt maximale Rechenleistung.

## Latenzquellen verstehen

Systemlatenz entsteht nicht an einer Stelle, sondern aus vier unabhängigen Kategorien:

| Kategorie | Einfluss | Typisches Symptom |
|---|---|---|
| **Scheduling** | Verzögerter Threadstart | Ruckler nach Lastspitzen |
| **Energieverwaltung** | Aufwachlatenz aus Schlafzuständen | Periodische kurze Unterbrechungen |
| **Interrupts** | Konkurrenz um CPU-Zeit | Ruckler bei I/O oder Eingabe |
| **Speicher/IO** | Blockierende Hintergrundoperationen | Stotterer beim Laden neuer Szenerien |

### Scheduling

Der Linux-Scheduler entscheidet, wann ein Thread Rechenzeit bekommt. Ein konservativer Scheduler wartet länger, bevor er reagiert — das spart Energie, erhöht aber die Latenz. Moderne Scheduler (EEVDF) berücksichtigen Cache-Lokalität und Wake-Frequenz und platzieren latenzsensitive Threads automatisch besser.

### Energieverwaltung

Nicht die CPU-Last verursacht Ruckler, sondern Übergänge zwischen Energiestufen. Wenn ein Kern aus einem tiefen Schlafzustand aufwacht, entstehen Verzögerungen von bis zu mehreren hundert Mikrosekunden. Auch NVMe-SSDs im Energiesparmodus erzeugen spürbare Aufwachlatenzen (Details unter [NVMe Energiesparen deaktivieren](#4-nvme-energiesparen-deaktivieren)).

### Interrupts

Hardware-Interrupts (USB-Geräte, Netzwerk, Storage) unterbrechen den laufenden Thread. Ein einzelner Interrupt zur falschen Zeit kann eine Frame-Deadline verletzen:

```
periodischer Hauptthread + zufälliger Interrupt = verpasste Deadline
```

### Speicher/IO

Der Kernel optimiert Durchsatz durch gebündelte Hintergrundarbeit (Writeback, Cache-Bereinigung, Paging). Das erzeugt seltene, aber spürbare Blockierungen — besonders beim Laden großer Ortho-Texturen.

## Zwei Optimierungsmodelle

Die richtige Tuning-Strategie hängt vom Kernel ab. Standardkernel und Liquorix verfolgen grundlegend verschiedene Ansätze:

**Standardkernel** = offener Regelkreis → Reaktion muss erzwungen werden

Der generische Debian-Kernel priorisiert Fairness und Durchsatz. Er reagiert konservativ auf Lastveränderungen. Tuning bedeutet hier: der Anwendung explizit Vorrang einräumen.

**Liquorix** = geschlossener Regelkreis → Störungen müssen entfernt werden

Liquorix nutzt den EEVDF-Scheduler mit kürzeren Preemption-Fenstern und höherer Timer-Frequenz. Er reagiert selbstständig auf Laständerungen. Tuning bedeutet hier: externe Störquellen minimieren.

!!! warning "Gleiche Einstellung, gegenteiliges Ergebnis"
    Identische Parameter können je nach Kernel gegensätzliche Effekte haben. Ein `performance`-Governor hilft beim Standardkernel, schadet aber unter Liquorix (thermischer Spielraum geht verloren). CPU-Isolation hilft beim Standardkernel, verhindert aber unter Liquorix die adaptive Optimierung.

| Parameterbereich | Standardkernel | Liquorix |
|---|---|---|
| CPU-Takt | Konstant hoch | Adaptiv |
| Scheduler-Einfluss | Verstärken | Nicht einschränken |
| CPU-Bindung | Möglich | Vermeiden |
| Interrupt-Routing | Optional | Wesentlich |
| Energiesparen | Begrenzen | Fein abstimmen |
| Writeback | Neutral | Glätten |

### Welchen Kernel nutze ich?

```bash
uname -r
```

- Enthält `liquorix` → Profil B (Liquorix)
- Sonst → Profil A (Standardkernel)

Für die Installation von Liquorix siehe [Liquorix Kernel](liquorix.md).

## Profil A: Debian Standardkernel

**Ziel:** Scheduler reagiert konservativ → Anwendung aktiv bevorzugen.

### 1. CPU Governor

Den Governor auf festen Hochleistungstakt setzen, um Reaktionszeit zu verkürzen und fehlende Lastvorhersage zu kompensieren.

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

### 2. CPU Schlafzustände begrenzen

In `/etc/default/grub` den Parameter `GRUB_CMDLINE_LINUX_DEFAULT` erweitern:

```
processor.max_cstate=2
```

!!! note "AMD vs. Intel"
    **AMD Zen:** Exportiert per ACPI nur C1 und C2 an das OS. Tiefere Hardware-C-States (C6) werden firmware-autonom verwaltet. Der Wert `2` stellt sicher, dass alle verfügbaren OS-sichtbaren C-States genutzt werden. Zusätzlich kann `amd_pstate=active` gesetzt werden (seit Kernel 6.5 Standard für Zen 2+).

    **Intel:** Tiefere ACPI-C-States (C3, C6, C8, C10) sind sichtbar und steuerbar. Hier kann `processor.max_cstate=3` sinnvoll sein, um C6+ mit 170–680 µs Aufwachlatenz zu vermeiden.

Anwenden:

```bash
sudo update-grub
```

Neustart erforderlich.

### 3. Anwendung bevorzugen (Affinität + Priorität)

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
    `SCHED_FIFO` Priorität 45 liegt unterhalb kritischer Kernel-Migrations-Threads (Priorität 50), aber deutlich über normalen Prozessen. Werte über 50 können Kernel-Housekeeping preemptieren und zu Instabilität führen.

### 4. Optional: CPU-Isolation

Nur sinnvoll bei hoher Hintergrundlast. In `/etc/default/grub` ergänzen:

```
isolcpus=4-11
```

!!! note "Hinweis zur Abkündigung"
    `isolcpus` gilt seit Kernel 5.4 als semi-deprecated. Die modernere Alternative sind **cgroup v2 cpusets**, die zur Laufzeit ohne Neustart konfiguriert werden können. Für einen einfachen Desktop-Anwendungsfall bleibt `isolcpus` jedoch die unkompliziertere Variante.

### 5. Speicherverhalten

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

### 1. Adaptiver CPU-Governor

Sofort umschalten:

```bash
echo ondemand | sudo tee /sys/devices/system/cpu/cpu*/cpufreq/scaling_governor
```

Überprüfung:

```bash
cat /sys/devices/system/cpu/cpu0/cpufreq/scaling_governor
```

!!! note "Warum `ondemand` statt `schedutil`?"
    `schedutil` bezieht Auslastungssignale direkt vom CFS-Scheduler. Liquorix nutzt jedoch den BORE-Scheduler, der diese Signale nicht bereitstellt — `schedutil` wird daher gar nicht erst einkompiliert. `ondemand` passt den CPU-Takt ebenfalls lastabhängig an, arbeitet aber unabhängig vom Scheduler.

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
    Die Terminal-Befehle gelten bis zum nächsten Neustart. Die GRUB-Variante macht die Einstellung dauerhaft. Für permanente EPP-Einstellung eine systemd-Unit oder udev-Regel erstellen.

### 2. C-States und Energiesteuerung

!!! note "AMD vs. Intel"
    **AMD Zen:** Nur C1/C2 sind OS-sichtbar — keine C-State-Begrenzung nötig. Tiefere Hardware-C-States helfen dem thermischen Budget.

    **Intel:** `processor.max_cstate=5` erlaubt moderate Schlafzustände und vermeidet tiefste Zustände (C8/C10 mit 280–680 µs Latenz).

In `/etc/default/grub` — für Intel:

```
processor.max_cstate=5
```

### 3. Interrupt-Shielding

Die wichtigste Maßnahme unter Liquorix. Hardware-Interrupts auf die ersten Kerne konzentrieren, damit der Scheduler die restlichen Kerne ungestört für die Anwendung nutzen kann.

!!! warning "IRQ-Affinität unter Liquorix"
    Liquorix verwaltet die IRQ-Verteilung kernelintern. Auf AMD-Systemen sind `/proc/irq/*/smp_affinity_list` und `/proc/irq/*/smp_affinity` selbst als Root schreibgeschützt — manuelle Affinitätsänderungen zur Laufzeit sind nicht möglich.

    Die Lösung ist der Kernel-Parameter `noirqbalance`, der die kernelinterne IRQ-Verteilung deaktiviert und die Kontrolle an den Userspace übergibt.

In `/etc/default/grub` den Parameter `GRUB_CMDLINE_LINUX_DEFAULT` erweitern:

```
noirqbalance
```

```bash
sudo update-grub
```

Neustart erforderlich. Danach `irqbalance` mit gezielter Konfiguration nutzen. In `/etc/default/irqbalance` eintragen:

```
IRQBALANCE_BANNED_CPULIST="4-15"
```

Das schließt die angegebenen Kerne von der Interrupt-Verteilung aus. CPU 0–3 = System/Interrupts, Rest = Anwendung.

```bash
sudo systemctl enable --now irqbalance
```

!!! tip "Warum irqbalance statt manueller Affinität?"
    `irqbalance` mit `BANNED_CPULIST` ist wartungsfreundlicher als manuelle Affinität: Es passt sich automatisch an neue Hardware-IRQs an und verteilt die Last intelligent auf die erlaubten Kerne.

### 4. NVMe Energiesparen deaktivieren

NVMe-SSDs können im Energiesparmodus Aufwachlatenzen von 5–22 ms haben — länger als ein kompletter Frame bei 60 Hz (z.B. Samsung 950 Pro State 4: 22 ms Exit-Latenz).

Sofort deaktivieren:

```bash
echo 0 | sudo tee /sys/module/nvme_core/parameters/default_ps_max_latency_us
```

Für dauerhafte Einstellung über Neustarts hinweg in `/etc/default/grub` den Parameter `GRUB_CMDLINE_LINUX_DEFAULT` erweitern:

```
nvme_core.default_ps_max_latency_us=0
```

```bash
sudo update-grub
```

### 5. Speicher-Writeback glätten

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

### 6. Leichte Priorisierung

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

### Installierte Kernel anzeigen

```bash
dpkg --list | grep linux-image
```

### GRUB-Menüeinträge ermitteln

GRUB nummeriert die Einträge ab 0. Kernel im Untermenü „Advanced options" werden mit `>` adressiert:

```bash
grep -E "menuentry |submenu " /boot/grub/grub.cfg | head -20
```

Das Format für Untermenü-Einträge ist `"Übermenü>Eintrag"`, z.B.:

```
"Advanced options for Debian GNU/Linux>Debian GNU/Linux, with Linux 6.12.6-1-liquorix-amd64"
```

### Einmaliger Wechsel

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

### Aktuellen Kernel prüfen

```bash
uname -r
```

### Was lässt sich zur Laufzeit umschalten?

Nicht alle Einstellungen erfordern einen Neustart. Die folgende Tabelle zeigt, welche Parameter im laufenden Betrieb geändert werden können:

| Parameter | Zur Laufzeit änderbar? | Methode |
|---|---|---|
| Governor | Ja | `echo ... \| sudo tee /sys/devices/system/cpu/cpu*/cpufreq/scaling_governor` |
| NVMe APST | Ja | `echo 0 \| sudo tee /sys/module/nvme_core/parameters/default_ps_max_latency_us` |
| sysctl (vm.*) | Ja | `sudo sysctl --system` |
| irqbalance-Dienst | Ja | `sudo systemctl stop/start irqbalance` |
| nice / chrt / taskset | Ja | Wird beim Anwendungsstart gesetzt |
| IRQ-Affinität | **Nein** (Liquorix/AMD) | Kernel sperrt `/proc/irq/*/smp_affinity` — `noirqbalance` per GRUB nötig |
| processor.max_cstate | **Nein** | Nur per GRUB, Neustart nötig |
| isolcpus | **Nein** | Nur per GRUB (Alternative: cgroup v2 cpusets) |

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
