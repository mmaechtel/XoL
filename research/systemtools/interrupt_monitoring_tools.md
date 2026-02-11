# Research: Interrupt-Monitoring und -Analyse unter Linux

Recherche-Datum: 2026-02-09
Kontext: Ergaenzung fuer `systemtools.md` und `systemtuning.md` — Verifizierung von IRQ-Shielding und Interrupt-Affinitaet

---

## 1. /proc/interrupts — Kernel-Interface fuer Interrupt-Zaehler

### Quelle

- [The /proc Filesystem — Linux Kernel Documentation](https://docs.kernel.org/filesystems/proc.html)
- [proc_interrupts(5) — man7.org](https://man7.org/linux/man-pages/man5/proc_interrupts.5.html)

### Format

```
           CPU0       CPU1       CPU2       CPU3
  0:         48          0          0          0  IR-IO-APIC   2-edge      timer
  1:          0          0          0          3  IR-IO-APIC   1-edge      i8042
  8:          0          0          1          0  IR-IO-APIC   8-edge      rtc0
 16:          0          0          0         28  IR-IO-APIC  16-fastedge  i801_smbus
126:          0          0          0          0  PCI-MSI 327680-edge      xhci_hcd
130:    1284562          0          0          0  PCI-MSI 524288-edge      nvme0q0
NMI:        142        138        129        134   Non-maskable interrupts
LOC:    4823901    3912845    3748291    3601287   Local timer interrupts
RES:     238471     189234     175892     163201   Rescheduling interrupts
```

### Spalten-Bedeutung

| Spalte | Bedeutung |
|--------|-----------|
| IRQ-Nummer (links) | Interrupt-Request-Kennung (numerisch oder symbolisch) |
| CPU0..CPUn | Zaehler: wie oft dieser Interrupt auf dem jeweiligen CPU-Kern bedient wurde (seit Boot) |
| Handler-Typ | Interrupt-Controller-Typ (`IR-IO-APIC`, `PCI-MSI`, etc.) |
| Trigger-Modus | `edge`, `fastedge`, `level` — wie der Interrupt ausgeloest wird |
| Geraetename | Zugeordnetes Hardware-Geraet |

### Spezielle Eintraege (nicht-numerische IRQs)

| Kennung | Bedeutung |
|---------|-----------|
| NMI | Non-Maskable Interrupts (Hardware-Watchdog, kritische Fehler) |
| LOC | Local APIC Timer Interrupts (pro CPU) |
| RES | Rescheduling Interrupts (IPI: eine CPU signalisiert einer anderen, den Scheduler zu aktivieren) |
| CAL | Function-Call Interrupts (IPI: Remote-Funktionsaufruf) |
| TLB | TLB Flush Interrupts (IPI: Translation Lookaside Buffer Invalidierung) |
| ERR | IO-APIC Bus Errors |
| SPU | Spurious Interrupts |
| TRM | Thermal Event Interrupts |

### Echtzeit-Monitoring mit watch

```bash
# Alle Interrupts, Aktualisierung jede Sekunde
watch -n 1 cat /proc/interrupts

# Nur NVMe-Interrupts beobachten
watch -n 1 'grep nvme /proc/interrupts'

# Nur die Spalten der Applikations-Kerne (z.B. CPU2+CPU3) filtern
watch -n 1 'cat /proc/interrupts | awk "{print \$1, \$4, \$5, \$NF}"'
```

### Interrupt-Rate berechnen (Delta pro Sekunde)

`/proc/interrupts` enthaelt kumulative Zaehler seit Boot. Um die aktuelle Rate zu ermitteln, muessen zwei Samples verglichen werden:

```bash
# Einzeiler: Interrupt-Delta ueber 1 Sekunde fuer ein bestimmtes Geraet
A=$(grep nvme0 /proc/interrupts | awk '{s=0; for(i=2;i<=NF-3;i++) s+=$i; print s}'); \
sleep 1; \
B=$(grep nvme0 /proc/interrupts | awk '{s=0; for(i=2;i<=NF-3;i++) s+=$i; print s}'); \
echo "NVMe IRQs/sec: $((B - A))"
```

### Top-Interrupt-Verursacher identifizieren

```bash
# Geraete nach Gesamt-Interrupt-Anzahl sortiert
awk 'NR>1 && /^[[:space:]]*[0-9]/ {
    sum=0; for(i=2;i<=NF-3;i++) sum+=$i;
    if(sum>0) printf "%12d  %s\n", sum, $NF
}' /proc/interrupts | sort -rn | head -20
```

---

## 2. irqtop / lsirq — Echtzeit-Interrupt-Monitoring

### Quellen

- [irqtop(1) — man7.org](https://man7.org/linux/man-pages/man1/irqtop.1.html)
- [lsirq(1) — man7.org](https://man7.org/linux/man-pages/man1/lsirq.1.html)
- [pizhenwei/irqtop — GitHub](https://github.com/pizhenwei/irqtop) (historisch, merged in util-linux v2.36)
- [util-linux/util-linux Issue #1109](https://github.com/util-linux/util-linux/issues/1109)

### Verfuegbarkeit auf Debian

**irqtop** wurde in **util-linux v2.36** aufgenommen (upstream). Auf Debian Bookworm:

- `lsirq` ist im Paket **`util-linux-extra`** enthalten
- `irqtop` war in Bookworm zeitweise als separates Paket (`irqtop`, Ruby-basiert) verfuegbar; die util-linux-Version ist in `util-linux-extra` enthalten

```bash
# Installation (Debian Bookworm)
sudo apt install util-linux-extra

# Pruefung
which irqtop lsirq
```

### irqtop — Echtzeit-Ansicht

Zeigt Interrupts im `top`-Stil mit automatischer Aktualisierung:

```bash
# Standard-Aufruf
sudo irqtop

# Aktualisierung alle 2 Sekunden, nur SoftIRQs
sudo irqtop -d 2 -S

# Nur bestimmte CPUs anzeigen
sudo irqtop -C 0,1

# Nach Delta sortieren (zeigt aktive Interrupts oben)
sudo irqtop -s DELTA

# Batch-Modus (fuer Skripte, nicht interaktiv)
sudo irqtop -b -n 5 -d 1
```

**Interaktive Tasten:**

| Taste | Sortierung |
|-------|------------|
| i | Nach IRQ-Nummer |
| t | Nach Gesamt-Zaehler (Standard) |
| d | Nach Delta (Aenderung seit letztem Update) |
| n | Nach Geraetename |
| q | Beenden |

### lsirq — Einmalige Snapshot-Ansicht

```bash
# Alle Interrupts auflisten
lsirq

# Nach Interrupt-Zaehler sortieren (hoechste zuerst)
lsirq -s COUNT

# Nur Interrupts mit mehr als 1000 Ereignissen
lsirq -t 1000

# JSON-Ausgabe (fuer Skript-Verarbeitung)
lsirq -J

# SoftIRQs anzeigen
lsirq -S
```

### Bekannte Einschraenkung

Die util-linux-Version von irqtop/lsirq zeigt **keine per-CPU-Zaehler** an — nur Gesamtwerte. Fuer per-CPU-Analyse ist `/proc/interrupts` direkt oder `mpstat -I CPU` erforderlich. Siehe [GitHub Issue #1109](https://github.com/util-linux/util-linux/issues/1109).

---

## 3. perf (linux-perf) — Performance-Counter-Analyse

### Quellen

- [perf-stat(1) — man7.org](https://man7.org/linux/man-pages/man1/perf-stat.1.html)
- [perf-top(1) — man7.org](https://www.man7.org/linux/man-pages/man1/perf-top.1.html)
- [perf-sched(1) — man7.org](https://man7.org/linux/man-pages/man1/perf-sched.1.html)
- [Perf Wiki Tutorial — kernel.org](https://perf.wiki.kernel.org/index.php/Tutorial)
- [Perf events and tool security — kernel.org](https://www.kernel.org/doc/html/latest/admin-guide/perf-security.html)

### Installation auf Debian

```bash
# Debian Bookworm
sudo apt install linux-perf

# Pruefung
perf --version
```

Das Paket heisst `linux-perf` (nicht `linux-tools` wie auf Ubuntu). Es installiert die zum laufenden Kernel passende Version.

### perf stat — Interrupt- und Scheduling-Zaehler

```bash
# Standard-Statistiken fuer einen Befehl (inkl. context-switches, cpu-migrations)
sudo perf stat -- sleep 10

# Beispiel-Ausgabe:
#          0      context-switches          #    0.000 /sec
#          0      cpu-migrations            #    0.000 /sec
#          0      page-faults               #    0.000 /sec

# Spezifische Events zaehlen
sudo perf stat -e context-switches,cpu-migrations,page-faults -- sleep 10

# Systemweite Messung ueber 10 Sekunden
sudo perf stat -a -e context-switches,cpu-migrations -- sleep 10

# An laufenden Prozess anhaengen (X-Plane PID)
sudo perf stat -p $(pgrep -f X-Plane) -e context-switches,cpu-migrations sleep 30

# Nur bestimmte CPUs messen
sudo perf stat -a -C 2,3 -e context-switches,cpu-migrations -- sleep 10
```

**Verfuegbare Software-Events (relevant):**

| Event | Bedeutung |
|-------|-----------|
| context-switches | Anzahl Kontext-Wechsel |
| cpu-migrations | Wie oft ein Prozess zwischen CPUs verschoben wurde |
| page-faults | Seitenfehler (Minor + Major) |
| task-clock | CPU-Zeit des Tasks in ms |

### perf top — Echtzeit-Hotspot-Analyse

Zeigt in Echtzeit, welche Kernel- und Userspace-Funktionen die meiste CPU-Zeit verbrauchen:

```bash
# Systemweite Echtzeit-Ansicht
sudo perf top

# Nur bestimmte CPUs ueberwachen (Applikations-Kerne)
sudo perf top -C 2,3

# Nur Kernel-Funktionen
sudo perf top --kernel

# An bestimmten Prozess gebunden
sudo perf top -p $(pgrep -f X-Plane)
```

**Nutzen fuer IRQ-Analyse:** Wenn Interrupt-Handler (z.B. `nvme_irq`, `xhci_irq`) in der Top-Liste erscheinen, verbrauchen sie signifikante CPU-Zeit auf dem jeweiligen Kern.

### perf sched — Scheduling-Latenz erkennen

```bash
# Scheduling-Events aufzeichnen (10 Sekunden)
sudo perf sched record -- sleep 10

# Latenz-Bericht: zeigt pro Task die Wartezeit
sudo perf sched latency

# Beispiel-Ausgabe:
#  Task                  |   Runtime ms  | Switches | Avg delay ms | Max delay ms
# X-Plane-render         |    8234.571   |    412   |    0.023     |    1.247

# Zeitverlauf mit einzelnen Scheduling-Events
sudo perf sched timehist

# Nur bestimmte CPUs
sudo perf sched timehist -C 2,3

# Mit Wakeup-Events (zeigt wer wen aufweckt)
sudo perf sched timehist -w
```

**Drei Schluesselwerte in timehist:**

| Spalte | Bedeutung |
|--------|-----------|
| Wait time | Zeit zwischen Entfernung von der CPU und naechster Ausfuehrung |
| Sch delay | Zeit zwischen "runnable" und tatsaechlicher Ausfuehrung (Scheduling-Verzoegerung) |
| Run time | Tatsaechliche Ausfuehrungszeit |

**Relevanz:** Hohe "Sch delay"-Werte auf den Applikations-Kernen deuten darauf hin, dass Interrupts oder andere Tasks den Render-Thread verdraengen.

---

## 4. mpstat — Interrupt-Statistiken pro CPU

### Quelle

- [mpstat(1) — man7.org](https://man7.org/linux/man-pages/man1/mpstat.1.html)

### Installation

```bash
sudo apt install sysstat
```

### Verwendung

```bash
# Hardware-Interrupts pro CPU pro Sekunde
mpstat -I CPU 1

# Alle Interrupt-Typen (HW + SW)
mpstat -I ALL 1

# Nur bestimmte CPUs
mpstat -I CPU -P 0,1,2,3 1

# CPU-Auslastung mit IRQ/SoftIRQ-Anteil
mpstat -P ALL 1
```

**Relevante Spalten in mpstat -P ALL:**

| Spalte | Bedeutung |
|--------|-----------|
| %irq | Prozent CPU-Zeit fuer Hardware-Interrupts |
| %soft | Prozent CPU-Zeit fuer Software-Interrupts |
| %idle | Leerlaufzeit |

**Nutzen:** Zeigt direkt, ob die abgeschirmten Kerne (z.B. CPU2+CPU3) tatsaechlich weniger IRQ-Last haben als die Housekeeping-Kerne (CPU0+CPU1).

---

## 5. ftrace / trace-cmd — Kernel-Tracing fuer Interrupt-Latenz

### Quellen

- [ftrace — Function Tracer (kernel.org)](https://docs.kernel.org/trace/ftrace.html)
- [Timerlat Tracer (kernel.org)](https://docs.kernel.org/trace/timerlat-tracer.html)
- [trace-cmd-record(1) — man7.org](https://man7.org/linux/man-pages/man1/trace-cmd-record.1.html)
- [trace-cmd — Debian Bookworm](https://packages.debian.org/bookworm/trace-cmd)

### Installation

```bash
# trace-cmd ist der Userspace-Frontend fuer ftrace
sudo apt install trace-cmd
```

### ftrace irqsoff-Tracer (direkt)

Misst die laengste Zeitspanne, in der Interrupts deaktiviert waren:

```bash
cd /sys/kernel/tracing/

# Tracer aktivieren
echo irqsoff > current_tracer
echo 1 > tracing_on

# Schwellenwert zuruecksetzen
echo 0 > tracing_max_latency

# Workload ausfuehren (z.B. X-Plane laufen lassen)
sleep 30

# Tracing stoppen und Ergebnis lesen
echo 0 > tracing_on
cat trace
```

### ftrace preemptirqsoff-Tracer

Kombiniert: misst die laengste Zeit, in der entweder Interrupts oder Preemption (oder beides) deaktiviert waren:

```bash
echo preemptirqsoff > /sys/kernel/tracing/current_tracer
echo 0 > /sys/kernel/tracing/tracing_max_latency
echo 1 > /sys/kernel/tracing/tracing_on
# ... Workload ...
echo 0 > /sys/kernel/tracing/tracing_on
cat /sys/kernel/tracing/trace
```

### trace-cmd (komfortabler)

```bash
# IRQ-Off-Latenz aufzeichnen
sudo trace-cmd record -p irqsoff sleep 10
sudo trace-cmd report

# Preemption + IRQ kombiniert
sudo trace-cmd record -p preemptirqsoff sleep 10
sudo trace-cmd report

# Interrupt-Events aufzeichnen
sudo trace-cmd record -e irq sleep 10
sudo trace-cmd report
```

### timerlat-Tracer (Wakeup-Latenz)

Misst die tatsaechliche Wakeup-Latenz eines periodischen Kernel-Threads — aehnlich wie `cyclictest`, aber als eingebauter Tracer:

```bash
cd /sys/kernel/tracing/

echo timerlat > current_tracer
cat trace

# Beispiel-Ausgabe:
#  TASK-PID  CPU# ||||  TIMESTAMP    ID   CONTEXT    LATENCY
#  <idle>-0  [000] d.h1  54.029328: #1   irq        timer_latency    932 ns
#  <...>-867 [000] ....  54.029339: #1   thread     timer_latency  11700 ns
```

**Zwei Messwerte pro Zyklus:**

| Kontext | Misst |
|---------|-------|
| irq (Hardirq) | Latenz vom Timer-Ablauf bis zum Hardirq-Handler (Hardware/Firmware-Einfluss, SMIs) |
| thread | Latenz vom Timer-Ablauf bis der Thread tatsaechlich laeuft (gesamte Scheduling-Kette) |

**Konfiguration:**

```bash
# Welche CPUs messen
echo 0-3 > /sys/kernel/tracing/tracing_cpumask

# Timer-Periode (Standard: 1000 us = 1 ms)
echo 1000 > /sys/kernel/tracing/timerlat_period_us

# Tracing stoppen wenn Latenz Schwellenwert ueberschreitet
echo 100 > /sys/kernel/tracing/tracing_thresh
```

---

## 6. /proc/irq/*/smp_affinity_list — IRQ-Affinitaet pruefen

### Quelle

- [SMP IRQ affinity — kernel.org](https://docs.kernel.org/core-api/irq/irq-affinity.html)

### Dateien

| Pfad | Format | Beispiel |
|------|--------|---------|
| `/proc/irq/<N>/smp_affinity` | Hexadezimale Bitmaske | `f` = CPU 0-3, `f0` = CPU 4-7 |
| `/proc/irq/<N>/smp_affinity_list` | CPU-Liste (lesbar) | `0-3`, `4,5,6,7`, `0-1` |
| `/proc/irq/default_smp_affinity` | Standard fuer neue IRQs | `ffffffff` = alle CPUs |

### Einzelnen IRQ pruefen

```bash
# Welche CPUs duerfen IRQ 130 bedienen?
cat /proc/irq/130/smp_affinity_list

# Bitmaske lesen
cat /proc/irq/130/smp_affinity
```

### Alle IRQ-Affinitaeten auflisten (One-Liner)

```bash
# Kompakt: IRQ-Nummer und zugewiesene CPUs
for d in /proc/irq/[0-9]*/; do
    irq=$(basename "$d")
    cpus=$(cat "$d/smp_affinity_list" 2>/dev/null)
    name=$(awk -v irq="$irq:" '$1==irq {print $NF}' /proc/interrupts 2>/dev/null)
    printf "IRQ %4s → CPU %-10s  %s\n" "$irq" "$cpus" "$name"
done
```

```bash
# Kurzform: nur IRQ und CPU-Liste
for f in /proc/irq/*/smp_affinity_list; do
    echo "$(dirname $f | xargs basename): $(cat $f)"
done
```

### Verifizierung: Interrupt-Shielding funktioniert?

Nach dem Konfigurieren von IRQ-Affinitaet (z.B. alle IRQs auf CPU 0-1, Applikation auf CPU 2-3) muss geprueft werden:

**Schritt 1 — Affinitaet pruefen (statisch):**

```bash
# Alle IRQs finden, die noch auf den geschuetzten Kernen (2,3) laufen duerfen
for d in /proc/irq/[0-9]*/; do
    irq=$(basename "$d")
    cpus=$(cat "$d/smp_affinity_list" 2>/dev/null)
    # Pruefen ob CPU 2 oder 3 in der Liste
    if echo "$cpus" | grep -qE '(^|,| )(2|3)(,| |$|-)'  ; then
        name=$(awk -v irq="$irq:" '$1==irq {print $NF}' /proc/interrupts 2>/dev/null)
        echo "WARNUNG: IRQ $irq ($name) kann noch auf CPU 2/3 laufen (affinity: $cpus)"
    fi
done
```

**Schritt 2 — Tatsaechliche Interrupt-Verteilung pruefen (dynamisch):**

```bash
# Interrupt-Zaehler der geschuetzten Kerne beobachten
# Die Zaehler fuer CPU2 und CPU3 sollten nicht (oder kaum) steigen
watch -n 1 'awk "NR==1 || /^[[:space:]]*[0-9]/" /proc/interrupts | awk "{print \$1, \$4, \$5, \$NF}"'
```

```bash
# mpstat: IRQ-Anteil pro CPU — CPU 2+3 sollten nahe 0% irq/soft zeigen
mpstat -P ALL 1 5
```

**Schritt 3 — perf stat auf den geschuetzten Kernen:**

```bash
# Kontextwechsel und Migrationen auf den Applikations-Kernen zaehlen
# Sollten minimal sein bei gutem Shielding
sudo perf stat -a -C 2,3 -e context-switches,cpu-migrations -- sleep 10
```

---

## 7. Zusammenfassung: Tool-Auswahl nach Anwendungsfall

| Anwendungsfall | Empfohlenes Tool | Befehl |
|----------------|-----------------|--------|
| Interrupt-Zaehler ansehen | /proc/interrupts | `cat /proc/interrupts` |
| Interrupt-Rate beobachten | irqtop oder watch | `sudo irqtop -s DELTA` |
| Per-CPU IRQ-Rate | mpstat | `mpstat -I CPU 1` |
| Top Interrupt-Verursacher | lsirq | `lsirq -s COUNT` |
| IRQ-Affinitaet pruefen | /proc/irq/*/smp_affinity_list | `for f in /proc/irq/*/smp_affinity_list; ...` |
| Scheduling-Latenz messen | perf sched | `sudo perf sched record -- sleep 10` |
| CPU-Hotspot finden | perf top | `sudo perf top -C 2,3` |
| IRQ-Off-Latenz messen | trace-cmd + irqsoff | `sudo trace-cmd record -p irqsoff` |
| Wakeup-Latenz messen | timerlat | `echo timerlat > current_tracer` |
| Shielding verifizieren | mpstat + /proc/interrupts | Kombination (siehe Abschnitt 6) |

---

## 8. Installations-Zusammenfassung (Debian Bookworm)

```bash
# Basis-Tools (irqtop, lsirq)
sudo apt install util-linux-extra

# Performance-Counter (perf stat, perf top, perf sched)
sudo apt install linux-perf

# Interrupt-Statistiken pro CPU (mpstat)
sudo apt install sysstat

# Kernel-Tracing (trace-cmd als ftrace-Frontend)
sudo apt install trace-cmd
```

**Hinweis:** `perf` und `trace-cmd` benoetigen Root-Rechte oder angepasste `/proc/sys/kernel/perf_event_paranoid`-Einstellungen:

```bash
# Aktuellen Wert pruefen
cat /proc/sys/kernel/perf_event_paranoid

# Fuer Debugging temporaer lockern (erfordert root)
sudo sysctl kernel.perf_event_paranoid=1

# Werte:
#  -1  = Keine Einschraenkungen
#   0  = Nur raw tracepoint access eingeschraenkt
#   1  = Nur CPU-Events ohne Kernel-Tracing (Standard Debian)
#   2  = Nur User-Space-Events
```

---

## Quellen

1. [The /proc Filesystem — Linux Kernel Documentation](https://docs.kernel.org/filesystems/proc.html)
2. [proc_interrupts(5) — man7.org](https://man7.org/linux/man-pages/man5/proc_interrupts.5.html)
3. [SMP IRQ affinity — Linux Kernel Documentation](https://docs.kernel.org/core-api/irq/irq-affinity.html)
4. [irqtop(1) — man7.org](https://man7.org/linux/man-pages/man1/irqtop.1.html)
5. [lsirq(1) — man7.org](https://www.man7.org/linux/man-pages/man1/lsirq.1.html)
6. [pizhenwei/irqtop — GitHub](https://github.com/pizhenwei/irqtop) (merged into util-linux v2.36)
7. [util-linux Issue #1109 — per-CPU counters](https://github.com/util-linux/util-linux/issues/1109)
8. [perf-stat(1) — man7.org](https://man7.org/linux/man-pages/man1/perf-stat.1.html)
9. [perf-top(1) — man7.org](https://www.man7.org/linux/man-pages/man1/perf-top.1.html)
10. [perf-sched(1) — man7.org](https://man7.org/linux/man-pages/man1/perf-sched.1.html)
11. [Perf Wiki Tutorial — kernel.org](https://perf.wiki.kernel.org/index.php/Tutorial)
12. [mpstat(1) — man7.org](https://man7.org/linux/man-pages/man1/mpstat.1.html)
13. [ftrace — Function Tracer (kernel.org)](https://docs.kernel.org/trace/ftrace.html)
14. [Timerlat Tracer (kernel.org)](https://docs.kernel.org/trace/timerlat-tracer.html)
15. [trace-cmd-record(1) — man7.org](https://man7.org/linux/man-pages/man1/trace-cmd-record.1.html)
16. [trace-cmd — Debian Bookworm Package](https://packages.debian.org/bookworm/trace-cmd)
17. [linux-perf — Debian Bookworm Package](https://packages.debian.org/bookworm/linux-perf)
18. [Perf events and tool security — kernel.org](https://www.kernel.org/doc/html/latest/admin-guide/perf-security.html)
