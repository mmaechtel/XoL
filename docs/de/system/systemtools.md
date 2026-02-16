# Linux-Systemtools

Die Einstellungen aus dem [Systemtuning](systemtuning.md) lassen sich nicht blind anwenden — sie müssen verifiziert werden. Wirkt der Governor tatsächlich? Landen Interrupts auf den richtigen Kernen? Wacht die [NVMe](../glossary.md#nvme-non-volatile-memory-express) aus dem Schlafmodus auf?

Diese Seite beschreibt Monitoring-Tools, die genau das prüfen. Jedes Tool wird mit seinem Hauptzweck und den wichtigsten Befehlen vorgestellt. Querverweise zum Systemtuning zeigen, welche Einstellung mit welchem Tool verifiziert wird.

## Installation

Alle empfohlenen Tools in einem Befehl:

```bash
sudo apt install htop btop sysstat linux-cpupower s-tui powertop iotop-c ioping nvme-cli glances util-linux-extra nmon
```

Das Paket `sysstat` enthält `mpstat` und `iostat`. Das Paket `linux-cpupower` enthält `cpupower` und `turbostat`. Das Paket `util-linux-extra` enthält `lsirq`.

---

## CPU-Monitoring

### htop — Prozesse und CPU-Auslastung

Interaktiver Prozess-Viewer mit farbigen Per-Core-Balken im Header. Zeigt auf einen Blick, welche Kerne unter Last sind und welche Prozesse die CPU beanspruchen.

```bash
htop
```

**Wichtige Hotkeys**

| Taste | Funktion |
|-------|----------|
| `H` | User-Threads ein/ausblenden (X-Plane nutzt viele Threads) |
| `t` | Baumansicht (zeigt Thread-Hierarchie) |
| `P` | Nach CPU-Verbrauch sortieren |
| `F4` | Filter (z.B. nach "X-Plane") |

Die Spalte **PROCESSOR** zeigt, auf welchem CPU-Kern ein Prozess zuletzt ausgeführt wurde — nützlich um zu prüfen, ob die Interrupt-Trennung aus dem [Systemtuning](systemtuning.md#3-interrupt-shielding) funktioniert.

**Limitierung:** Zeigt keine CPU-Frequenz, keine [C-States](../glossary.md#c-states-cpu-idle-states) und keine Interrupt-Aufschlüsselung pro Core.

### btop — System-Dashboard

Moderner System-Monitor mit Zeitverlaufs-Graphen für CPU, RAM, Disk-I/O und Netzwerk in einem Fenster. Gut um Korrelationen zu erkennen — z.B. CPU-Last-Spitzen während Szenerie-Laden.

```bash
btop
```

Unterstützt Maus-Bedienung, Prozess-Filter (`f`), Baumansicht (`e`) und Layout-Presets (`p`).

**Limitierung:** CPU-Frequenz nur als Gesamtwert, keine Per-Core-Frequenz. Keine [IRQ](../glossary.md#irq-interrupt-request)-Statistiken.

### cpupower — Governor prüfen und setzen

Zeigt den aktiven [CPU-Frequenz-Governor](../glossary.md#cpu-governor) und kann ihn ändern. Essentiell um zu prüfen, ob der im [Systemtuning](systemtuning.md#1-cpu-governor) konfigurierte Governor tatsächlich aktiv ist.

```bash
# Aktive Policy (Governor und Frequenzbereich) aller Cores anzeigen
cpupower -c all frequency-info -p

# Verfügbare Governors
cpupower frequency-info -g

# Aktiver cpufreq-Treiber
cpupower frequency-info -d

# Governor setzen (z.B. performance für Profil A)
sudo cpupower frequency-set -g performance
```

### s-tui — Governor-Verifikation und Thermal-Throttling

Terminal-Tool mit vier Echtzeit-Graphen: CPU-Frequenz, Auslastung, Temperatur und Leistungsaufnahme. Macht den Effekt eines Governor-Wechsels sofort sichtbar.

```bash
sudo s-tui
```

**Governor-Verifikation:** Mit `performance`-Governor bleiben alle Kerne auf Maximalfrequenz. Mit `ondemand` steigt die Frequenz unter Last und fällt im Leerlauf. Fällt die Frequenz bei hoher Temperatur → Thermal Throttling.

Optional mit Stress-Test: `sudo apt install stress-ng`, dann im s-tui-Menü den Stress-Modus aktivieren.

Verifiziert: [Profil A Governor](systemtuning.md#1-cpu-governor) und [Profil B Governor](systemtuning.md#1-adaptiver-cpu-governor)

### turbostat — Hardware-Frequenzen und C-States

Zeigt die **tatsächlichen Hardware-Frequenzen pro Core** (nicht nur was der Governor meldet), C-State-Residency und Leistungsaufnahme. Benötigt Root.

```bash
# Standardübersicht
sudo turbostat --interval 2

# Fokussiert: Frequenz und Last pro Core
sudo turbostat --interval 1 --show Core,CPU,Avg_MHz,Bzy_MHz,Busy%,IRQ,CoreTmp

# In Datei loggen (während eines Flugs)
sudo turbostat --interval 2 --out turbostat_session.log
```

**Wichtige Spalten**

| Spalte | Bedeutung |
|--------|-----------|
| `Bzy_MHz` | Taktrate während aktiver Phasen — die echte Geschwindigkeit |
| `Busy%` | Anteil der Zeit im aktiven Zustand (C0) |
| `CPU%c1`, `CPU%c3`, … | C-State-Residency — verfügbare States hardware-abhängig |
| `IRQ` | Interrupts pro Intervall und Core |

!!! note "AMD-Hinweis"
    turbostat funktioniert auf AMD Zen-Prozessoren. Die verfügbaren Spalten hängen von der MSR-Unterstützung des Prozessors ab — einige Intel-spezifische Spalten (z.B. bestimmte Package-Level-Metriken) erscheinen auf AMD-Systemen nicht.

Verifiziert: [C-States](systemtuning.md#2-cpu-schlafzustände-begrenzen) und Governor-Wirksamkeit

### mpstat — Per-Core-Statistiken und Interrupt-Verteilung

Präziseste Per-Core-Aufschlüsselung: zeigt User-, System-, I/O-Wait-, **IRQ-** und **[SoftIRQ](../glossary.md#softirq-software-interrupt)-Anteil** pro CPU-Kern. Unverzichtbar für die Verifikation des Interrupt-Shielding.

```bash
# Alle Cores, 1-Sekunden-Intervall
mpstat -P ALL 1

# Einzelne Interrupts pro CPU pro Sekunde
mpstat -I CPU 1

# Alles: CPU + Interrupts + NUMA
mpstat -A 1
```

**Interrupt-Shielding prüfen:** Die Applikations-Kerne (z.B. CPU 4–15) sollten nahe 0% in den Spalten `%irq` und `%soft` zeigen. Steigen die Werte dort an, erreichen Interrupts die geschützten Kerne.

Verifiziert: [Interrupt-Shielding](systemtuning.md#3-interrupt-shielding) (Profil B)

---

## IO-Monitoring

### iotop — Welcher Prozess verursacht IO?

Zeigt Disk-Read/Write-Raten pro Prozess in Echtzeit. Identifiziert ob Stutter von X-Plane selbst, einem Compositor, journald oder einem anderen Hintergrundprozess kommen.

```bash
# Nur aktive IO-Prozesse, halbe Sekunde Refresh
sudo iotop -oPd 0.5

# Akkumuliert: wer hat insgesamt am meisten gelesen
sudo iotop -oPa
```

### iostat — Device-Level-Latenz

Zeigt Durchsatz, IOPS, Queue-Tiefe und **durchschnittliche Request-[Latenz](../glossary.md#latenz)** pro Device. Der Schlüsselwert ist `r_await` — die durchschnittliche Read-Latenz in Millisekunden.

```bash
# Extended Stats für NVMe, 1-Sekunden-Intervall
iostat -xdth -p nvme0n1 1
```

**Wichtige Felder**

| Feld | Bedeutung |
|------|-----------|
| `r_await` | Durchschnittliche Read-Latenz (ms) — Spikes deuten auf Probleme |
| `%util` | Device-Auslastung — bei 100% ist das Device gesättigt |
| `aqu-sz` | Queue-Länge — hohe Werte bedeuten wartende Requests |

**NVMe [APST](../glossary.md#apst-autonomous-power-state-transitions)-Signatur:** Ein plötzlicher Sprung in `r_await` von <1 ms auf 50–500 ms nach einer Idle-Phase deutet auf NVMe-Aufwachlatenz hin.

### ioping — Disk-Latenz messen

Misst individuelle IO-Request-Latenzen, ähnlich wie `ping` für Netzwerk. Direktestes Tool zur Erkennung von NVMe-Aufwachlatenzen.

```bash
# Direct IO-Latenz (Cache umgangen, wahre Device-Latenz)
sudo ioping -c 20 -D /dev/nvme0n1

# Ortho-Texture-Reads simulieren: 256K sequentiell
sudo ioping -c 50 -s 256k -D -L /dev/nvme0n1
```

**NVMe APST Wake-Up-Test:**

```bash
# 5x idle + Messung — erster Request nach Idle zeigt Wake-Up-Latenz
for i in $(seq 1 5); do
    sleep 5
    sudo ioping -c 1 -D /dev/nvme0n1
done
```

Zeigt der erste Request 10–500 ms während Folgeanfragen <0.1 ms zeigen, ist APST Wake-Up die Ursache.

Verifiziert: [NVMe Energiesparen](systemtuning.md#4-nvme-energiesparen-deaktivieren) (Profil B)

### nvme-cli — NVMe Power States abfragen

Zeigt die Power States des NVMe-Laufwerks mit ihren Entry/Exit-Latenzen. Ergänzt ioping um die Ursache: welcher Power State verursacht die Verzögerung.

```bash
# Power States mit Latenzen anzeigen
sudo nvme id-ctrl /dev/nvme0 | grep -A 5 "ps "

# APST-Konfiguration prüfen
sudo nvme get-feature /dev/nvme0 -f 0x0c -H

# Aktuellen Power State prüfen
sudo nvme get-feature /dev/nvme0 -f 0x02 -H
```

---

## Interrupt-Analyse

### /proc/interrupts — Interrupt-Zähler lesen

Das Kernel-Interface für Interrupt-Statistiken. Zeigt pro IRQ die Anzahl der Interrupts auf jedem CPU-Kern seit dem Boot.

```bash
# Alle Interrupts anzeigen
cat /proc/interrupts

# NVMe-Interrupts beobachten (Echtzeit)
watch -n 1 'grep nvme /proc/interrupts'
```

**Wichtige Spalten**

| Spalte | Bedeutung |
|--------|-----------|
| IRQ-Nummer | Interrupt-Kennung |
| CPU0..CPUn | Zähler pro Kern (seit Boot) |
| Handler-Typ | `IR-IO-APIC`, `PCI-MSI`, etc. |
| Gerätename | Zugeordnete Hardware |

Spezielle Einträge: **LOC** = Local Timer Interrupts (pro CPU), **RES** = Rescheduling Interrupts (IPI), **NMI** = Non-Maskable Interrupts.

### lsirq — Sortierter Interrupt-Snapshot

`lsirq` liefert einen sortierten Snapshot der Interrupt-Zähler. Teil des Pakets `util-linux-extra`.

```bash
# Nach Gesamtzähler sortiert (aktivste IRQs oben)
lsirq -s TOTAL

# Nur Zähler für bestimmte CPUs anzeigen
lsirq -C 0-3

# Softirqs statt Hardware-Interrupts
lsirq -S
```

Für Echtzeit-Monitoring `watch -n 1 lsirq -s TOTAL` oder die oben beschriebenen `/proc/interrupts`-Methoden verwenden.

### Interrupt-Shielding verifizieren

Nach dem Konfigurieren des [Interrupt-Shielding](systemtuning.md#3-interrupt-shielding) (Profil B) muss geprüft werden, ob die Applikations-Kerne tatsächlich von Interrupts verschont bleiben.

**Schritt 1 — IRQ-Anteil pro Core prüfen:**

```bash
# CPU 4-15 sollten ~0% in %irq und %soft zeigen
mpstat -P ALL 1 5
```

**Schritt 2 — Interrupt-Zähler beobachten:**

```bash
# Zähler der geschützten Kerne sollten nicht steigen
watch -n 1 'grep -E "^[[:space:]]*[0-9]" /proc/interrupts'
```

**Schritt 3 — IRQ-Affinität direkt prüfen:**

```bash
# Alle IRQ-Affinitäten auflisten
for d in /proc/irq/[0-9]*/; do
    irq=$(basename "$d")
    cpus=$(cat "$d/smp_affinity_list" 2>/dev/null)
    name=$(awk -v irq="$irq:" '$1==irq {print $NF}' /proc/interrupts 2>/dev/null)
    printf "IRQ %4s -> CPU %-10s  %s\n" "$irq" "$cpus" "$name"
done
```

---

## System-Dashboards

### glances — Alles auf einen Blick

Umfassendes System-Dashboard mit CPU, RAM, Disk-I/O (inkl. Latenz), Netzwerk, Sensoren und Prozessliste in einem Fenster.

```bash
# Terminal-Dashboard
glances

# Web-UI-Modus (Zugriff über http://localhost:61208)
glances -w
```

Der **Web-UI-Modus** ist ideal für X-Plane im Vollbild: das Monitoring läuft auf einem zweiten Gerät (Tablet, Laptop) im Browser. Mit der Taste `L` (Großbuchstabe) wird die Disk-IO-Latenz-Ansicht aktiviert — direkt relevant für die Erkennung von NVMe-Aufwachlatenzen.

### powertop — C-States und Energieverhalten

Diagnostik-Tool für Energieverbrauch und Power-Management. Der wichtigste Tab ist **Idle Stats** — zeigt die C-State-Residency pro Core. Benötigt Root.

```bash
sudo powertop
```

**Relevante Tabs**

| Tab | Zeigt |
|-----|-------|
| **Idle Stats** | C-State-Residency pro Core — tiefe C-States verursachen Aufwachlatenz |
| **Frequency Stats** | P-State/Turbo-Nutzung — läuft die CPU mit der erwarteten Frequenz? |
| **Device Stats** | Welche Geräte verursachen Wakeups |

```bash
# HTML-Report generieren (für Dokumentation)
sudo powertop --html=powertop_report.html
```

!!! warning "auto-tune vermeiden"
    `powertop --auto-tune` aktiviert aggressive Energiespar-Einstellungen — das **Gegenteil** der Empfehlungen aus dem [Systemtuning](systemtuning.md). Nicht für latenz-sensitive Anwendungen verwenden.

Verifiziert: [C-States](systemtuning.md#2-cpu-schlafzustände-begrenzen) und [C-States Liquorix](systemtuning.md#2-c-states-und-energiesteuerung)

---

## Szenario-Tabelle

| Was will ich prüfen? | Tool | Befehl |
|---------------------|------|--------|
| Welcher Core ist unter Last? | htop | `htop` (Header-Balken) |
| CPU + RAM + Disk gleichzeitig | btop | `btop` |
| Welcher Governor ist aktiv? | cpupower | `cpupower -c all frequency-info -p` |
| Governor-Wechsel visuell prüfen | s-tui | `sudo s-tui` |
| Echte Hardware-Frequenz pro Core | turbostat | `sudo turbostat --show Core,CPU,Bzy_MHz,Busy%` |
| C-State-Residency prüfen | powertop | `sudo powertop` (Tab: Idle Stats) |
| Interrupt-Shielding verifizieren | mpstat | `mpstat -I CPU -P ALL 1` |
| Interrupt-Quellen identifizieren | lsirq | `watch -n 1 lsirq -s TOTAL` |
| Welcher Prozess verursacht IO? | iotop | `sudo iotop -oPd 0.5` |
| NVMe-Latenz messen | ioping | `sudo ioping -c 20 -D /dev/nvme0n1` |
| NVMe APST Wake-Up testen | ioping | `sleep 5 && sudo ioping -c 1 -D /dev/nvme0n1` |
| NVMe Power States anzeigen | nvme-cli | `sudo nvme get-feature /dev/nvme0 -f 0x02 -H` |
| Alles überwachen (Web-UI) | glances | `glances -w` |
| Session aufzeichnen | nmon | `nmon -f -s 5 -c 720` |

---

??? abstract "Fortgeschritten: nmon — Batch-Recording"

    nmon zeichnet System-Metriken im Hintergrund in CSV-Dateien auf. Ideal um eine komplette Flug-Session aufzuzeichnen und danach zu analysieren.

    ```bash
    sudo apt install nmon

    # 1 Stunde aufzeichnen (5-Sekunden-Intervall, 720 Snapshots)
    nmon -f -s 5 -c 720

    # 2 Stunden aufzeichnen (10-Sekunden-Intervall)
    nmon -f -s 10 -c 720
    ```

    Die Aufzeichnung läuft im Hintergrund. Die Datei wird automatisch benannt (`hostname_YYYYMMDD_HHMM.nmon`). Zur Visualisierung `nmonchart` verwenden, das die CSV-Daten in interaktive HTML-Charts konvertiert.

??? abstract "Fortgeschritten: fatrace — Datei-Zugriffe beobachten"

    fatrace zeigt Echtzeit-Datei-Zugriffs-Events aller Prozesse mit vollem Pfad. Beantwortet: "Welche Dateien liest X-Plane beim Szenerie-Wechsel?"

    ```bash
    sudo apt install fatrace

    # Welche Dateien liest X-Plane gerade?
    sudo fatrace -t -f R -C X-Plane -o /tmp/xplane_reads.log

    # Hintergrundprozesse die während des Flugs auf Disk schreiben
    sudo fatrace -t -f W -s 120 -o /tmp/writes_during_flight.log
    ```

    Ausgabe immer in Datei umleiten (`-o`), da Terminal-Ausgabe selbst Disk-IO erzeugt.

??? abstract "Fortgeschritten: perf und trace-cmd — Kernel-Level-Analyse"

    Für tiefgehende Scheduling- und Interrupt-Latenz-Analyse. Diese Tools erfordern Root und ein Verständnis der Linux-Kernel-Interna.

    ```bash
    sudo apt install linux-perf trace-cmd
    ```

    **perf sched** — Scheduling-Latenz erkennen:

    ```bash
    # Scheduling-Events aufzeichnen
    sudo perf sched record -- sleep 10
    sudo perf sched latency
    ```

    Zeigt pro Task die durchschnittliche und maximale Scheduling-Verzögerung. Hohe Werte auf Applikations-Kernen deuten darauf hin, dass Interrupts oder andere Tasks den Render-Thread verdrängen.

    **trace-cmd** — IRQ-Off-Latenz messen:

    ```bash
    sudo trace-cmd record -p irqsoff sleep 10
    sudo trace-cmd report
    ```

    Misst die längste Zeitspanne, in der Interrupts deaktiviert waren — ein Indikator für Kernel-seitige Verzögerungen.

---

## Quellen

- [htop-dev/htop](https://github.com/htop-dev/htop) — Interaktiver Prozess-Viewer
- [aristocratos/btop](https://github.com/aristocratos/btop) — System-Monitor
- [sysstat/sysstat](https://github.com/sysstat/sysstat) — mpstat, iostat, pidstat
- [amanusk/s-tui](https://github.com/amanusk/s-tui) — CPU-Monitoring und Stress-Test
- [nicolargo/glances](https://github.com/nicolargo/glances) — System-Dashboard mit Web-UI
- [fenrus75/powertop](https://github.com/fenrus75/powertop) — Power-Management-Diagnostik
- [koct9i/ioping](https://github.com/koct9i/ioping) — Disk-IO-Latenz-Messung
- [linux-nvme/nvme-cli](https://github.com/linux-nvme/nvme-cli) — NVMe-Management
