# Monitoring

Startet eine Monitoring-Session fuer X-Plane 12 Flugsimulation, zeichnet System- und Applikations-Metriken auf und erstellt nach dem Ende eine strukturierte Performance-Analyse.

## Argumente

`$ARGUMENTS`: Optionale Dauer in Minuten

| Aufruf | Beschreibung |
|--------|-------------|
| `/monitoring` | Fragt interaktiv nach Dauer und Optionen |
| `/monitoring 90` | 90-Minuten-Session, ueberspringt Dauer-Frage |

---

## Referenzdokumente

Diese Dateien VOR Beginn laden und als Kontext verwenden:

| Datei | Zweck | Wann lesen |
|-------|-------|-----------|
| `monitoring/README.md` | Architektur-Ueberblick (3-Layer-Modell) | Phase 1 |
| `monitoring/FEATURES.md` | CLI-Optionen, CSV-Spalten, Tracepoint-Details | Phase 1 |
| `monitoring/ANALYSIS_RULES.txt` | **Analyse-Regelwerk** (Schwellwerte, Korrelationsketten, Known Signatures) | Phase 3 |
| `monitoring/ANALYSE_HISTORY.md` | Tuning-Historie (Runs A-G) fuer Vergleich mit neuen Runs | Phase 3 |

---

## Phase 1 — Setup & Start

### 1.1 Konfiguration erfragen

Falls `$ARGUMENTS` leer, AskUserQuestion verwenden:

**Frage 1: Dauer**

| Option | Wert |
|--------|------|
| 20 Min (Kurztest) | `-d 1200` |
| 60 Min (Standard) | `-d 3600` |
| 90 Min (Langflug) | `-d 5400` |
| 120 Min (Maximal) | `-d 7200` |

**Frage 2: bpftrace-Sidecar**

| Option | Beschreibung |
|--------|-------------|
| Ja (empfohlen) | Layer 2 mitlaufen lassen — liefert Direct Reclaim Attribution, Slow IO, DMA Fence |
| Nein | Nur Layer 1 (sysmon.py) — reicht fuer Grundanalyse |

Falls `$ARGUMENTS` eine Zahl enthaelt: Dauer = Argument in Minuten, Sidecar = Ja (Default).

### 1.2 Run-Verzeichnis vorbereiten

Run-Verzeichnis unter `/tmp/` mit Zeitstempel benennen:

```
RUN_DIR="/tmp/sysmon_run_$(date +%Y%m%d_%H%M)"
```

### 1.3 Monitoring starten

sysmon.py im Hintergrund starten:

```bash
python3 monitoring/sysmon.py -d <SEKUNDEN> -o "$RUN_DIR" &
SYSMON_PID=$!
```

Dem User die Ausgabe zeigen und bestaetigen dass sysmon.py laeuft.

### 1.4 Sidecar-Befehl ausgeben (wenn gewaehlt)

Den sudo-Befehl NICHT selbst ausfuehren — dem User anzeigen zum manuellen Starten:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
MONITORING GESTARTET
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  sysmon.py: PID <PID>, Dauer <N> Min, Output: <RUN_DIR>

  Bitte in einem separaten Terminal starten:

  sudo bash monitoring/sysmon_trace.sh -o <RUN_DIR>

  Dann X-Plane + XEarthLayer starten und Flug beginnen.
  Monitoring endet automatisch nach <N> Minuten.
  Oder jederzeit mit /monitoring-stop beenden.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### 1.5 Warten

Der Skill pausiert hier. Der User fliegt. Zwei Wege zum Fortfahren:

**A) Timer laeuft ab:** sysmon.py beendet sich automatisch nach der konfigurierten Dauer. Der User meldet sich zurueck (z.B. "fertig", "Analyse starten", "Flug beendet").

**B) User bricht vorzeitig ab:** User sagt "stop" oder "fertig" vor Timer-Ende. Dann sysmon.py stoppen:

```bash
kill $SYSMON_PID
```

In beiden Faellen: Dem User mitteilen dass er `sysmon_trace.sh` im anderen Terminal mit Ctrl+C stoppen soll (falls gestartet).

---

## Phase 2 — Daten einsammeln

### 2.1 Run-Verzeichnis pruefen

```
Glob: <RUN_DIR>/*.csv
Glob: <RUN_DIR>/trace_*.log
```

Pruefen welche Dateien vorhanden sind. Erwartete Dateien:

- **Immer:** cpu.csv, mem.csv, io.csv, vram.csv, vmstat.csv, psi.csv, irq.csv, proc.csv, freq.csv
- **Wenn X-Plane lief:** xplane_events.csv
- **Wenn Sidecar lief:** trace_reclaim.log, trace_io_slow.log, trace_fence.log
- **Crash-Diagnostik:** dmesg_pre.log, dmesg_post.log, gpu_events.log

Fehlende Dateien notieren aber nicht als Fehler werten.

### 2.2 Application Logs identifizieren

XEarthLayer-Log suchen:

```
Glob: ~/.xearthlayer/xearthlayer.log
```

X-Plane Log suchen — die RICHTIGE Log finden:

1. Pruefe ob `xplane_events.csv` existiert (sysmon.py hat Log bereits korreliert)
2. Falls nicht: Pruefe `~/X-Plane-12/Log.txt` — ist der Zeitstempel innerhalb des Monitoring-Fensters?
3. Falls Log.txt neuer als die CSV-Dateien: Suche in `~/X-Plane-12/Output/Log Archive/` nach der passenden archivierten Log

### 2.3 Session-Metadaten bestimmen

Aus den CSV-Dateien extrahieren:

- **Start-Timestamp:** Erste Zeile von cpu.csv, Spalte 1 (Unix Epoch)
- **End-Timestamp:** Letzte Zeile von cpu.csv, Spalte 1
- **Dauer:** End - Start in Sekunden
- **Sample-Count:** Zeilenanzahl cpu.csv (minus Header)

---

## Phase 3 — Analyse

**ANALYSIS_RULES.txt ist das massgebliche Regelwerk.** Dieses Dokument lesen und die 6 Phasen der Analyse durchlaufen.

```
Read: monitoring/ANALYSIS_RULES.txt
```

### 3.1 Daten laden

Die CSV-Dateien sind potentiell gross (90-Min-Session = ~25.000 Zeilen in cpu.csv). Strategie:

- **Uebersicht:** Erste und letzte 50 Zeilen jeder CSV lesen fuer Start/End-Zustand
- **Schluessel-Metriken:** vmstat.csv komplett lesen (1s-Resolution, ~5.400 Zeilen fuer 90 Min — handhabbar)
- **Gezielte Tiefe:** Nur die Zeitfenster detailliert lesen in denen allocstall_s > 0 oder andere Anomalien auftreten
- **XEL-Log:** Nach Event-Typ filtern statt komplett lesen (Log kann 28.000+ Zeilen haben)

### 3.2 Analyse-Phasen ausfuehren

Gemaess ANALYSIS_RULES.txt Sections 1-5:

1. **Overview & Session Context** — Workload, RAM, Phasen-Erkennung
2. **Per-Subsystem Deep Dive** — Memory, CPU, GPU, Disk IO, XEL, X-Plane
3. **Cross-Correlation** — Stutter Chain, IO Latency Chain, Swap Storm Chain, XEL Tile-Loading Storm
4. **Temporal Pattern Analysis** — Drei-Phasen-Modell, Stall-Cluster
5. **Comparison** — Falls fruehere Runs vorhanden (ANALYSE_HISTORY.md laden)

### 3.3 XEL-Log Korrelation

Aus dem XEL-Log die performance-relevanten Events extrahieren und mit den System-Metriken korrelieren:

- **Circuit Breaker Events** (resource-pool-basiert seit PR #61) → vmstat allocstall_s Zeitfenster
- **Turn Events** → io.csv Read-Spikes 5-15s spaeter
- **Prefetch Cache Hit Rate** → mem.csv available_mb Verlauf
- **Flight Phase Transitions** → Drei-Phasen-Grenzen
- **DDS Generation Bursts** → cpu.csv user% Spikes

### 3.4 Parallele Subagents fuer grosse Datenmengen

Bei langen Sessions (> 60 Min) die Analyse auf parallele Subagents aufteilen:

```
Task (subagent_type=general-purpose): "Analysiere vmstat.csv + mem.csv:
  Finde alle allocstall_s > 0 Events, berechne Drei-Phasen-Grenzen,
  Memory-Statistiken pro Phase. Datei: <RUN_DIR>/vmstat.csv"

Task (subagent_type=general-purpose): "Analysiere io.csv:
  Per-Device Throughput/Latenz-Statistiken, IO-Spikes > 100 MB/s,
  NVMe-Latenz-Cluster (10-11ms Pattern). Datei: <RUN_DIR>/io.csv"

Task (subagent_type=general-purpose): "Parse XEL Log fuer Zeitfenster
  <START> bis <END>: Circuit Breaker Events (resource-pool), Turn Events, Prefetch
  Cache Hit Rates, Flight Phases. Datei: ~/.xearthlayer/xearthlayer.log"
```

### 3.5 Quality Checklist

Gemaess ANALYSIS_RULES.txt Section 7 vor Abschluss pruefen:

- [ ] Alle CSV-Dateien gelesen oder als fehlend notiert
- [ ] Drei-Phasen-Grenzen identifiziert mit Minutenangaben
- [ ] Jeder allocstall > 0 Event hat eine wahrscheinliche Ursache
- [ ] Cross-Korrelation durchgefuehrt (Stalls ↔ IO ↔ Swap ↔ GPU ↔ XEL)
- [ ] XEL-Log geparst und korreliert
- [ ] Flight Phases aus XEL dem Drei-Phasen-Modell zugeordnet
- [ ] Circuit Breaker Events mit Resource-Pool-Auslastung abgeglichen (post-PR #61: sollte selten sein)
- [ ] Trace-Logs geparst und integriert (falls vorhanden)
- [ ] Findings nach Schweregrad sortiert
- [ ] Empfehlungen spezifisch und umsetzbar
- [ ] Vergleich mit frueheren Runs (falls Daten vorhanden)

---

## Phase 4 — Bericht erstellen

### 4.1 Bericht-Datei schreiben

Bericht als Markdown in das Monitoring-Verzeichnis schreiben:

```
monitoring/ANALYSE_RUN_<LABEL>_<DATUM>.md
```

`<LABEL>` aus dem Run-Verzeichnisnamen ableiten oder den User fragen (z.B. "H", "I", "test_01").

### 4.2 Bericht-Format

Gemaess ANALYSIS_RULES.txt Section 4:

```markdown
# Run <LABEL> — Ergebnisse: <Dauer>-Minuten <Flugtyp>

**Datum:** <YYYY-MM-DD>
**System:** <CPU>, <RAM> GB RAM, <GPU> <VRAM> GB, <Storage>
**Kernel:** <Kernel-Version>
**Workload:** <Prozesse aus proc.csv>
**Aenderungen seit Run <vorheriger>:** <was sich geaendert hat>

---

## 0. Testbedingungen
(Dauer, Samples, Tuning-Parameter, Sidecar-Status)

## 1. Erwartungen vs. Ergebnisse
(Tabelle mit Key Metrics, Vergleich zu vorherigem Run)

## 2. Kernbefunde
### 2.1 Drei-Phasen-Verhalten
### 2.2 Memory Pressure
### 2.3 XEarthLayer Streaming Activity
### 2.4 Direct Reclaim (falls Trace-Daten)
### 2.5 Alloc-Stall-Cluster

## 3. GPU / VRAM

## 4. Disk IO

## 5. CPU & Frequenz

## 6. Per-Process

## 7. Vergleich Run <vorheriger> → Run <aktuell>

## 8. Handlungsempfehlungen
### 8.1-N Konkrete, priorisierte Massnahmen

## 9. Zusammenfassung
```

### 4.3 ANALYSE_HISTORY.md aktualisieren

Den neuen Run als Eintrag in `monitoring/ANALYSE_HISTORY.md` anfuegen:

- Neuer Abschnitt am Ende mit Run-Label, Datum, Key Metrics
- Ggf. Tuning-Aenderungen dokumentieren

---

## Phase 5 — Abschluss

### 5.1 Zusammenfassung ausgeben

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
MONITORING-ANALYSE ABGESCHLOSSEN
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

SESSION:
├─ Dauer:        <N> Minuten (<Samples> Samples)
├─ Run-Dir:      <RUN_DIR>
├─ Sidecar:      <Ja/Nein>
└─ XEL-Log:      <Ja/Nein>

KEY FINDINGS:
├─ [CRITICAL] <Finding 1>
├─ [WARNING]  <Finding 2>
└─ [INFO]     <Finding 3>

PHASEN:
├─ Warm-up:     Min 0–<N>
├─ Ramp-up:     Min <N>–<M>  (<X> Alloc Stalls)
└─ Steady:      Min <M>–Ende (<Y> Alloc Stalls)

BERICHT:
└─ monitoring/ANALYSE_RUN_<LABEL>_<DATUM>.md

TOP-3 EMPFEHLUNGEN:
  1. <Empfehlung>
  2. <Empfehlung>
  3. <Empfehlung>

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### 5.2 Dateien NICHT committen

Monitoring-Analysen werden NICHT automatisch committed. Der User entscheidet ob und wann committed wird (ggf. via `/abschluss`).

---

## Hinweise

- **sysmon.py laeuft als User:** Kein sudo noetig. Wird direkt gestartet.
- **sysmon_trace.sh braucht sudo:** Wird NICHT automatisch gestartet. Der Befehl wird dem User angezeigt.
- **XEL-Log wird NICHT rotiert:** `~/.xearthlayer/xearthlayer.log` enthaelt moeglicherweise mehrere Sessions. Nur Events innerhalb des Monitoring-Zeitfensters auswerten.
- **X-Plane Log Archive:** Falls `Log.txt` neuer als die CSV-Dateien ist, die archivierte Log aus `~/X-Plane-12/Output/Log Archive/` verwenden.
- **Grosse CSV-Dateien:** Nicht komplett in den Kontext laden. Gezielt Zeitfenster und Schluessel-Spalten lesen.
- **ANALYSIS_RULES.txt ist bindend:** Alle Schwellwerte, Korrelationsketten und Known Signatures aus diesem Dokument verwenden. Keine eigenen Schwellwerte erfinden.
- **Vergleich mit frueheren Runs:** `monitoring/ANALYSE_HISTORY.md` und vorhandene `ANALYSE_RUN_*.md` laden fuer Kontext.
- **Run-Verzeichnisse:** Bleiben unter `/tmp/` — bei Reboot weg. User darauf hinweisen bei wichtigen Runs das Verzeichnis zu sichern (z.B. nach `monitoring/run_<label>/`).
