# Empfohlene Systemkonfigurationen zur Latenzreduktion unter Linux

## Parametrische Ableitung geeigneter Einstellungen für generische und Low-Latency-Kernel

---

## Abstract

Dieses Paper fasst konkrete Systemparameter zusammen, die aus einer Analyse latenzsensitiver Desktop-Workloads abgeleitet wurden. Ziel ist nicht die Maximierung des Durchsatzes, sondern die Minimierung der zeitlichen Varianz periodischer Aufgaben.
Zwei Betriebsmodelle werden unterschieden:

1. **Generischer Distributionskernel** – konservatives Scheduling
2. **Low-Latency-Kernel** – reaktionsoptimiertes Scheduling

Die Arbeit zeigt, dass identische Konfigurationen in beiden Fällen gegensätzliche Resultate liefern können und formuliert daraus ein systematisches Parametermodell.

---

## 1. Methodik

Die Parameter wurden nicht nach Benchmark-Durchschnittswerten gewählt, sondern nach Reduktion von **Worst-Case-Latenzen**:

```
Zielgröße = min(max(Δt_frame))
```

Damit wird nicht die mittlere Bildrate optimiert, sondern die maximale Abweichung eines Rechenzyklus.

Messbare Symptome:

- periodische kurze Unterbrechungen
- verzögerte Eingabereaktion
- konstante Auslastung bei inkonsistenter Reaktionszeit

---

## 2. Parameterräume

Die Systemlatenz setzt sich aus vier unabhängigen Quellen zusammen:

| Kategorie         | Einfluss                 |
| ----------------- | ------------------------ |
| Scheduling        | Threadstart-Zeit         |
| Energieverwaltung | Aufwecklatenz            |
| Interrupts        | Konkurrenz um CPU        |
| Speicher/I/O      | Blockierende Operationen |

Optimierung bedeutet:
jede Kategorie einzeln stabilisieren statt eine global zu maximieren.

---

## 3. Konfiguration: Generischer Kernel

### 3.1 Ziel

Scheduler reagiert konservativ → Interaktivität muss explizit priorisiert werden.

---

### 3.2 CPU-Frequenzsteuerung

**Strategie:** Mindestleistung erhöhen

Empfehlung:

- Governor: fester Hochleistungstakt
- reduzierte tiefe Schlafzustände

Begründung:
Verkürzt Reaktionszeit, kompensiert fehlende Lastvorhersage.

---

### 3.3 CPU-Topologie

**Strategie:** garantierte Rechenzeit

Maßnahmen:

- bevorzugte Kernzuweisung
- optionale CPU-Isolation
- erhöhte Scheduling-Priorität

Erwarteter Effekt:
Reduzierte Konkurrenz mit Hintergrundprozessen.

---

### 3.4 Interrupts

**Strategie:** optional bündeln

Da der Kernel längere Timeslices verwendet, sind Störungen weniger kritisch.

---

### 3.5 Speicherverwaltung

**Strategie:** ausgewogene Cachestrategie

Moderate Writeback-Grenzen verhindern starke Durchsatzverluste, ohne große Blockierungen zu erzeugen.

---

## 4. Konfiguration: Low-Latency-Kernel

### 4.1 Ziel

Der Scheduler reagiert bereits optimal → externe Latenzquellen minimieren.

---

### 4.2 CPU-Frequenzsteuerung

**Strategie:** adaptiven Boost ermöglichen

Empfehlung:

- adaptiver Governor
- moderate Schlafzustände erlaubt

Begründung:
Thermischer Spielraum erhöht Burst-Leistung stärker als hoher Basistakt.

---

### 4.3 CPU-Topologie

**Strategie:** keine statische Bindung

Feste Zuordnung verhindert Cache-Optimierung und Lastprognose.

---

### 4.4 Interrupt-Routing

**Strategie:** räumliche Trennung

Hardwareereignisse auf dedizierte Kerne konzentrieren, statt Prioritäten zu erhöhen.

Wirkung:
Verhindert Deadline-Verletzungen periodischer Threads.

---

### 4.5 Speicher- und I/O-Subsystem

**Strategie:** Übergänge vermeiden

- Energiesparzustände von Massenspeichern reduzieren
- Writeback über Zeit verteilen
- Cache aggressiver halten

Ziel:
Verhindern einzelner Blockierereignisse statt Maximierung der Bandbreite.

---

## 5. Vergleich der optimalen Parameterstrategien

| Parameterbereich   | Generischer Kernel | Low-Latency-Kernel |
| ------------------ | ------------------ | ------------------ |
| CPU-Takt           | konstant hoch      | adaptiv            |
| Scheduler-Einfluss | verstärken         | nicht einschränken |
| CPU-Bindung        | möglich            | vermeiden          |
| Interrupt-Routing  | optional           | wesentlich         |
| Energiesparen      | begrenzen          | fein abstimmen     |
| Writeback          | neutral            | glätten            |

---

## 6. Systemtheoretische Interpretation

Der Unterschied entspricht zwei Regelkreisen:

**Generischer Kernel**

> Offener Regelkreis → externe Stabilisierung notwendig

**Low-Latency-Kernel**

> Geschlossener Regelkreis → Störungen minimieren

Damit ändern sich nicht nur Parameterwerte, sondern das gesamte Optimierungsmodell.

---

## 7. Schlussfolgerung

Effiziente Linux-Konfiguration hängt nicht von einzelnen „Performance-Tweaks“ ab, sondern vom Verhalten des zugrunde liegenden Kernels.

Zwei gegensätzliche Prinzipien entstehen:

- konservativer Kernel benötigt erzwungene Priorisierung
- reaktiver Kernel benötigt störungsarme Umgebung

Die optimale Einstellung ergibt sich somit nicht aus maximaler Leistung, sondern aus minimaler zeitlicher Varianz.

---

## Kernaussage

> Die richtige Konfiguration ist keine universelle Liste von Tweaks, sondern eine Anpassung an das Regelverhalten des Kernels.

---

# Practical Guide

## Konkrete Debian-13 Einstellungen für Standardkernel und Low-Latency-Kernel

Dieses Dokument ist absichtlich **nicht theoretisch**.
Hier stehen nur umsetzbare Schritte — getrennt nach Kerneltyp.

> Erst feststellen welchen Kernel du nutzt:

```
uname -r
```

- enthält „liquorix“ → Low-Latency-Profil
- sonst → Standard-Debian-Kernel

---

# Teil A — Debian Standardkernel (generisches Verhalten stabilisieren)

Ziel: Scheduler reagiert konservativ → Anwendung aktiv bevorzugen

---

## 1. CPU Governor (festen Basistakt erzwingen)

Auf Debian wird der Governor am zuverlässigsten über einen Kernel-Boot-Parameter gesetzt, da das `linux-cpupower`-Paket keinen systemd-Service enthält (Debian Bug #894906):

```
sudo nano /etc/default/grub
```

GRUB_CMDLINE_LINUX_DEFAULT erweitern:

```
cpufreq.default_governor=performance
```

```
sudo update-grub
```

Neustart erforderlich. Überprüfung:

```
cat /sys/devices/system/cpu/cpu0/cpufreq/scaling_governor
```

Alternativ kann `cpupower` für temporäre Änderungen verwendet werden:

```
sudo apt install linux-cpupower
cpupower frequency-set -g performance
```

---

## 2. CPU Schlafzustände begrenzen

```
sudo nano /etc/default/grub
```

GRUB_CMDLINE_LINUX_DEFAULT erweitern:

```
amd_pstate=active processor.max_cstate=2
```

> **Hinweis AMD Zen**: AMD Zen-Prozessoren exportieren per ACPI nur C1 und C2 an das Betriebssystem. Tiefere Hardware-C-States (C6) werden firmware-autonom verwaltet und sind über `processor.max_cstate` nicht steuerbar. Der Wert `2` stellt hier sicher, dass alle verfügbaren OS-sichtbaren C-States genutzt werden, ohne wirkungslose Werte zu setzen.
>
> Bei **Intel-Prozessoren** sind tiefere ACPI-C-States (C3, C6, C8, C10) sichtbar und steuerbar — hier kann `processor.max_cstate=3` sinnvoll sein, um C6+ mit 170–680 µs Aufwachlatenz zu vermeiden.
>
> `amd_pstate=active` ist seit Kernel 6.5 Standard für Zen 2+ und kann weggelassen werden.

```
sudo update-grub
```

Neustart erforderlich.

---

## 3. Programm bevorzugt ausführen (Affinity + Priorität)

Beispiel Starter:

```bash
nano ~/run_realtime_app.sh
```

```bash
#!/bin/bash
exec taskset -c 4-11 chrt -f 45 "$@"
```

> **Hinweis zur Priorität**: SCHED_FIFO-Prioritäten reichen von 1–99. Kernel-Migrations-Threads laufen auf Priorität 50 (`sched_set_fifo()`). Eine Anwendungspriorität von 45 liegt unterhalb dieser kritischen Kernel-Threads, aber deutlich über normalen Prozessen. Werte über 50 können Kernel-Housekeeping-Threads preemptieren und zu Systeminstabilität führen.

```
chmod +x ~/run_realtime_app.sh
```

Programm starten:

```
./run_realtime_app.sh ./programm
```

---

## 4. Optional: CPU-Isolation

Nur wenn Hintergrundlast vorhanden:

```bash
sudo nano /etc/default/grub
```

ergänzen:

```
isolcpus=4-11
```

> **Hinweis**: `isolcpus` gilt seit Kernel 5.4 als semi-deprecated. Die modernere Alternative sind **cgroup v2 cpusets**, die zur Laufzeit ohne Neustart konfiguriert werden können. Für einen einfachen Desktop-Anwendungsfall bleibt `isolcpus` jedoch die unkompliziertere Variante.

---

## 5. Speicherverhalten moderat halten

```bash
sudo nano /etc/sysctl.d/60-desktop.conf
```

```ini
vm.swappiness=20
vm.dirty_ratio=20
vm.dirty_background_ratio=10
vm.vfs_cache_pressure=100
```

```bash
sudo sysctl --system
```

---

### Ergebnis dieses Profils

Der Kernel reagiert schneller, da Rechenzeit garantiert wird.

---

---

# Teil B — Low-Latency Kernel (Liquorix)

Ziel: Scheduler arbeitet korrekt → Störungen entfernen

**Wichtig: KEIN isolcpus / KEIN taskset**

---

## 1. Adaptiver CPU-Governor

Auf Debian per Kernel-Boot-Parameter:

```
sudo nano /etc/default/grub
```

GRUB_CMDLINE_LINUX_DEFAULT erweitern:

```
cpufreq.default_governor=schedutil
```

```
sudo update-grub
```

Neustart erforderlich. EPP setzen (für persistente Anwendung eine systemd-Unit oder udev-Regel erstellen):

```
echo balance_performance | sudo tee /sys/devices/system/cpu/cpu*/cpufreq/energy_performance_preference
```

---

## 2. C-States und Energiesteuerung

```
sudo nano /etc/default/grub
```

> **AMD Zen**: Da nur C1/C2 OS-sichtbar sind, ist keine C-State-Begrenzung nötig. Tiefere Hardware-C-States werden firmware-autonom verwaltet und helfen dem thermischen Budget.
>
> **Intel**: `processor.max_cstate=5` kann hier sinnvoll sein, um moderate Schlafzustände zu erlauben und gleichzeitig tiefste Zustände (C8/C10 mit 280–680 µs Latenz) zu vermeiden.

Für AMD Zen genügt:

```
amd_pstate=active
```

Für Intel:

```
processor.max_cstate=5
```

```
sudo update-grub
```

---

## 3. Interrupt-Shielding (sehr wichtig)

```
sudo systemctl disable --now irqbalance
```

```
for i in /proc/irq/*/smp_affinity_list; do echo 0-3 | sudo tee "$i" 2>/dev/null; done
```

CPU 0-3 = System/Interrupts
Rest = Anwendung

> **Hinweis**: Manche IRQs sind hardwaregebunden und lehnen die Änderung ab — das `2>/dev/null` unterdrückt diese erwarteten Fehler. Für persistente Konfiguration kann alternativ `irqbalance` mit `IRQBALANCE_BANNED_CPULIST="4-15"` konfiguriert werden, statt es zu deaktivieren — das ist wartungsfreundlicher und passt sich an neue Hardware-IRQs an.

---

## 4. NVMe Energiesparen deaktivieren

Bevorzugte Methode über Kernel-Parameter (deaktiviert NVMe Autonomous Power State Transitions):

```
sudo nano /etc/default/grub
```

GRUB_CMDLINE_LINUX_DEFAULT erweitern:

```
nvme_core.default_ps_max_latency_us=0
```

```
sudo update-grub
```

Alternativ per udev-Regel (weniger zuverlässig, da `power/control` am PCI-Device hängt):

```bash
sudo nano /etc/udev/rules.d/60-nvme-latency.rules
```

```
ACTION=="add|change", SUBSYSTEM=="pci", DRIVER=="nvme", ATTR{power/control}="on"
```

```bash
sudo udevadm control --reload-rules
sudo udevadm trigger
```

> **Hintergrund**: NVMe-SSDs können Aufwachlatenzen von 5–22 ms haben (z. B. Samsung 950 Pro State 4: 22 ms Exit-Latenz). Das ist länger als ein kompletter Frame bei 60 Hz.

---

## 5. Speicher-Writeback glätten

```bash
sudo nano /etc/sysctl.d/99-lowlatency.conf
```

```ini
vm.swappiness=10
vm.dirty_background_ratio=3
vm.dirty_ratio=10
vm.vfs_cache_pressure=100
```

```bash
sudo sysctl --system
```

---

## 6. Anwendung nur leicht priorisieren

Starter:

```bash
nano ~/run_lowlatency_app.sh
```

```bash
#!/bin/bash
exec nice -n -10 "$@"
```

---

### Ergebnis dieses Profils

Keine maximale Leistung — sondern minimale Frametime-Spikes.

---

# Gesamtvergleich

| Bereich            | Standardkernel          | Liquorix             |
| ------------------ | ----------------------- | -------------------- |
| Governor           | performance             | schedutil            |
| CPU-Bindung        | ja                      | nein                 |
| Interrupt-Trennung | optional                | wichtig              |
| NVMe APST          | optional deaktivieren   | deaktiviert          |
| Writeback          | normal                  | geglättet            |
| Ziel               | Reaktionszeit erzwingen | Störungen verhindern |

---

## Wichtigste Regel

> Standardkernel braucht Priorisierung — Low-Latency-Kernel braucht Ruhe.

Wenn beide gleich konfiguriert werden, verschlechtert sich das Ergebnis fast immer.
