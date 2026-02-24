# Run F — Ergebnisse: zram + XEL-Config Validierung

**Datum:** 2026-02-22
**System:** Ryzen 9 9800X3D 8C/16T, 96 GB RAM, RTX 4090 24 GB, 3x NVMe
**Kernel:** Liquorix 6.18 (PDS)
**Workload:** X-Plane 12 + XEarthLayer + QEMU/KVM
**Änderungen seit Run E:** zram 32GB lz4 (pri=100), XEL network_concurrent 128→64, disk_io 64→32, max_tiles_per_cycle 200→100

---

## 0. Testbedingungen

| Parameter | Wert |
|-----------|------|
| Teil 1 | 90 Min (13:27–14:57), X-Plane Crash um 14:23:38 + Neustart |
| Teil 2 | 53 Min (15:06–15:59), stabiler Flug |
| Gesamtdauer | 143 Min aktives Monitoring |
| Route | Norditalien (Venedig/LIPZ → Alpen), dichter VATSIM-Verkehr |
| zram | 32 GB lz4, pri=100, manuell aktiviert (udev-Race-Fix ausstehend) |
| NVMe-Swap | nvme2n1p5, pri=-2 (Fallback) |

### NVMe-Naming (geändert seit Run E!)

| Run F | Run E | Hardware | Rolle |
|-------|-------|----------|-------|
| **nvme2n1** | nvme0n1 | SN850X 8TB | EFI, **Swap-Partition**, xplane_data RAID0 |
| nvme1n1 | nvme1n1 | SN850X 8TB | Root, Home, xplane_data RAID0 |
| nvme0n1 | nvme2n1 | 990 PRO 4TB | xplane_data RAID0 only |

---

## 1. Erwartungen vs. Ergebnisse

| Metrik | Run E | Erwartung F | **Ergebnis F** | Bewertung |
|--------|-------|-------------|----------------|-----------|
| Direct Reclaim max | 2.122.555/s | 0 oder <1.000/s | **762.842/s** (Teil 1), **0/s** (Teil 2) | Teilweise erreicht |
| Alloc Stalls max | 13.383/s | 0 | **10.900/s** (Teil 1), **0/s** (Teil 2) | Teilweise erreicht |
| TLB Shootdowns (IRQ) avg | 9.574/s | <10.000/s | **23.973/s** (Teil 1), **557/s** (Teil 2) | Teil 2 erreicht |
| Major Faults avg | 377/s | <300/s | **860/s** (Teil 1), **76/s** (Teil 2) | Erwartet (zram-Swap-In) |
| NVMe-Swap genutzt? | ja (11.595 MB) | ~0 MB | **Nein** (zram absorbiert 100%) | **Erreicht** |
| Write-Lat avg (Swap-NVMe) | 16,1 ms | <5 ms | **6,0 ms** (non-zero avg) | Knapp verfehlt |
| Write-Lat max (Swap-NVMe) | 699 ms | <150 ms | **476 ms** (Teil 1), **44 ms** (Teil 2) | Teil 2 erreicht |
| EMFILE-Errors | 3.474 | 0 | **2.116** | Verbessert, nicht gelöst |
| DSF-Load max | 63.385 ms | <10.000 ms | **22.116 ms** | Verbessert, nicht erreicht |
| Dirty Pages avg | 39 MB | ~30 MB | **2,4 MB** | **Weit übertroffen** |

---

## 2. Kernbefunde

### 2.1 zram — Voller Erfolg

zram hat **100% des Swap-Traffics absorbiert**. Die NVMe-Swap-Partition wurde nie angesprochen.

| Metrik | Wert |
|--------|------|
| zram Peak-Nutzung | 25.813 MB (78,8% von 32 GB) |
| zram Kompression | 17,1 GB → 14,6 GB (Ratio 1,17:1) |
| NVMe-Swap Used (Ende) | 2.814 MB (Altlast vom Boot, kein neuer Traffic) |
| Write-Volume nvme2n1 | 25,1 GB (Run E) → **3,6 GB** (Run F) = **-86%** |
| Write-Rate nvme2n1 avg | 4,8 MB/s (Run E) → **0,44 MB/s** (Run F) = **-91%** |

### 2.2 Dirty Pages — Dramatische Verbesserung

| Metrik | Run E | Run F | Veränderung |
|--------|-------|-------|-------------|
| Dirty Pages avg | 39 MB | **2,4 MB** | **-94%** |
| Dirty Pages max | — | 97,7 MB | — |

Ohne Swap-IO-Konkurrenz auf der NVMe flusht der Writeback-Path die Dirty Pages prompt.

### 2.3 Write-Latenz — Erheblich besser, Tail-Latenz bleibt

**nvme2n1 (Swap-Drive) — Non-Zero Write Samples:**

| Metrik | Run E | Run F | Veränderung |
|--------|-------|-------|-------------|
| avg | 11,7 ms | **6,0 ms** | **-49%** |
| p99 | 298,8 ms | **143,0 ms** | **-52%** |
| max | 699 ms | **476 ms** (Teil 1) / **44 ms** (Teil 2) | **-32% / -94%** |
| Samples >200 ms | 1,6% | **0,5%** | **-69%** |

**IO Utilization p95:** 100% (Run E) → **36,9%** (Run F) — Drive ist deutlich weniger gesättigt.

### 2.4 Zwei-Phasen-Verhalten: Teil 1 vs. Teil 2

Das auffälligste Ergebnis: **Teil 1 und Teil 2 zeigen völlig unterschiedliche Profile.**

| Metrik | Teil 1 (90 Min) | Teil 2 (53 Min) |
|--------|-----------------|-----------------|
| Direct Reclaim max | 762.842/s | **0/s** |
| Alloc Stalls max | 10.900/s | **0/s** |
| TLB Shootdowns avg | 23.973/s | **557/s** |
| TLB Shootdowns max | 7.687.952/s | **488.700/s** |
| Major Faults avg | 860/s | **76/s** |
| Context Switches max | 1.945.373/s | **100.793/s** |
| Write-Lat max (nvme2n1) | 476 ms | **44 ms** |

**Erklärung:** Teil 1 enthält den X-Plane-Crash, Neustart, und die initiale Szenerieladung über neue Regionen — massive Speicherdruckphasen, in denen kswapd und Direct Reclaim aktiv werden. Teil 2 ist stabiler Flug mit warmem Cache. Das Zwei-Phasen-Muster bestätigt: **zram löst das Steady-State-Problem vollständig, aber initiale Szenerieladungen erzeugen weiterhin Memory-Pressure-Spitzen.**

### 2.5 Kausalkette Teil 1 — Memory-Pressure-Kaskaden

Periodische Stürme alle 10–15 Minuten während Szenerieübergängen:

```
kswapd-Scan 2,1M pages/s
  → Direct Reclaim 505K–762K/s
    → Alloc Stalls bis 10.900/s
      → TLB Shootdowns 7,7M/s (Page-Invalidierungen über alle Cores)
        → Context Switches 1,9M/s
          → Page Re-Faults 1,68M/s
```

### 2.6 EMFILE-Errors — Reduziert, nicht gelöst

| Metrik | Run E | Run F | Veränderung |
|--------|-------|-------|-------------|
| EMFILE-Count | 3.474 | **2.116** | **-39%** |
| Bursts | 1 (4s) | **2** (je 1–2s) | Kürzer, aber 2 Events |

**Burst 1 (10:35 UTC, 1.343 Errors):** XEL-Startup — Cache-Scan über 4.054.759 Dateien. Unabhängig von der Concurrency-Config, XEL-internes Problem.

**Burst 2 (13:25 UTC, 773 Errors):** Initiale DSF-Szenerieladung — 12 DDS-Jobs gleichzeitig + FUSE + Chunk-Downloads überschreiten FD-Budget.

Dazwischen: **2h 50min fehlerfreier Betrieb** mit 150.098 erfolgreichen Downloads.

### 2.7 DSF-Ladezeiten — Deutlich besser

| Metrik | Run E | Run F | Veränderung |
|--------|-------|-------|-------------|
| DSF max | 63.385 ms | **22.116 ms** | **-65%** |
| DSF ≥ 20s | 4 | **1** | **-75%** |
| DSF ≥ 10s | 9 | **5** | **-44%** |

Die katastrophalen 40–63s DSF-Stalls aus Run E sind eliminiert. Worst Case ist jetzt 22s beim initialen Szenerieladen.

---

## 3. Performance-Einbruch — Beobachtete Fakten

### 3.1 Zeitlinie (13:44–13:48 CET) — GPU-Aushungerung durch Memory-Pressure

#### Phase 1: DSF-Laden (13:44:10–13:46:50)

X-Plane lädt neue DSF-Tiles. VRAM steigt um 3.000 MiB in 40 Sekunden.

| Zeit | VRAM (MiB) | X-Plane CPU% | Event |
|------|-----------|-------------|-------|
| 13:44:10 | 18.098 | 332% | DSF-Laden beginnt |
| 13:44:28 | 18.872 | 467% | Threads 97→130, IO-Burst |
| 13:44:42 | 20.914 | 385% | VRAM steigt schnell |
| 13:44:51 | 21.170 | **259%** | CPU-Dip (IO-bound) |

Kein Memory-Pressure — kswapd idle, Available RAM bei ~40 GB. Normales Verhalten bei Szenerieübergängen.

#### Phase 2: XEL-Thread-Explosion + Swap-Storm (13:47:05–13:48:00)

XEarthLayer spawnt ~275 Threads und beginnt Ortho-Streaming (100–330 MB/s IO), während X-Plane noch DSF-Tiles lädt. **Gemessene Kausalkette:**

| Zeit | Event | Messwert |
|------|-------|----------|
| 13:47:05 | X-Plane Swap-In beginnt | io_read=50 MB/s |
| 13:47:07 | Massiver Swap-In | io_read=182 MB/s |
| 13:47:12 | XEL Thread-Explosion | 39→175 Threads, 502% CPU |
| 13:47:16 | XEL Peak | 272 Threads, 931% CPU |
| 13:47:20 | Page Faults Peak | **1.678.510/s** |
| 13:47:25 | X-Plane Swap-In Burst | io_read=1.645 MB/s |
| 13:47:28 | X-Plane Peak IO | **io_read=7.805 MB/s** |
| 13:47:29 | Context Switches Peak | **1.350.948/s** |
| 13:47:40 | Alloc Stalls | **6.573/s**, Direct Scan 505K/s |
| 13:47:58 | Alle 3 NVMe 100% util | Swap + Tiles gleichzeitig |

**GPU-Aushungerung (gemessen):**

| Zeit | GPU Util | GPU Power | Normalniveau |
|------|---------|-----------|--------|
| 13:47:13 | 42% | 198 W | 80%, 275 W |
| 13:47:27 | **35%** | **154 W** | |
| 13:47:32 | **32%** | **157 W** | |

**Ursache:** CPU/Memory-Subsystem liefert nicht schnell genug Daten an die GPU → FPS-Einbruch. Die GPU ist idle, weil der Render-Thread durch Memory-Pressure blockiert ist.

#### Phase 3: Wiederholte Reclaim-Events (13:48–14:20)

Fünf Memory-Pressure-Kaskaden, Swap steigt progressiv:

| Zeit | Alloc Stalls/s | Swap Used |
|------|---------------|-----------|
| 13:58:26 | **10.900/s** | 14.048 MB |
| 14:06:17 | 3.072/s | ~15.500 MB |
| 14:17:52 | 5.624/s | ~17.585 MB |
| 14:19:55 | 9.119/s | 22.042 MB |

Swap wächst in 43 Minuten von 9.691 MB auf 22.891 MB (13 GB Zuwachs via zram).

### 3.2 Kausalkette Performance-Einbruch

```
XEL Thread-Explosion (272 Threads, 931% CPU)
  + X-Plane DSF-Laden gleichzeitig
    → RAM-Bedarf übersteigt Available → kswapd-Scan 2,1M pages/s
      → Direct Reclaim 505K–762K/s (Prozesse warten auf Speicher)
        → Alloc Stalls bis 10.900/s
          → TLB Shootdowns 7,7M/s (Page-Invalidierungen über alle Cores)
            → Context Switches 1,9M/s
              → Page Re-Faults 1,68M/s
```

Jede Kaskade dauerte 30–60 Sekunden. Zwischen den Kaskaden: normaler Betrieb.

---

## 4. Crash — Beobachtete Fakten und Hypothesen

### 4.1 Beobachtete Fakten

#### Ausgeschlossen

| Ursache | Evidenz |
|---------|---------|
| OOM Kill | Kein OOM in dmesg/journalctl, 38 GB available |
| Segfault | Kein Segfault im Kernel-Log |
| IO-Stall | Alle NVMe idle zum Crash-Zeitpunkt |
| Aktive Memory Pressure | Kein Direct Reclaim bei 14:23:00, kswapd-Burst bei 14:23:15 war moderat (242K/s vs. Peaks von 2,1M/s) |

#### GPU-Verhalten vor Crash

| Zeit | GPU Util | GPU Power | VRAM (MiB) | X-Plane CPU% |
|------|---------|-----------|------------|-------------|
| 14:23:00 | **6%** | 36 W | 22.594 (92%) | 525% |
| 14:23:15 | **3%** | 23 W | 22.594 | 525% |
| 14:23:33 | **0%** | 23 W | 22.594 | laufend |
| 14:23:37 | 1% | 23 W | 22.594 | laufend |
| **14:23:38** | — | — | 3.468 | **CRASH**: RSS→0, Threads 97→2 |

**Kritische Beobachtung:** GPU Utilization war **bereits bei 6%** um 14:23:00, bevor der kswapd-Burst um 14:23:15 einsetzte. Die GPU war schon am Sterben, bevor Memory-Pressure überhaupt auftrat.

#### X-Plane Log

`X-Plane-12/Output/Log Archive/Log-2026-02-22-1422.txt` (28.234 Zeilen):

- Letzte reguläre Meldung: `GMT: 13:19:07: Saving situation file: AUTOSAVED_SITUATION`
- 10.658 xswiftbus "probe missed" Meldungen
- Kein Crash-Handler, kein Stack-Trace, kein `VK_ERROR_DEVICE_LOST` im Log — abruptes Ende

#### journalctl (14:22–14:24 CET)

| Zeit | Quelle | Meldung |
|------|--------|---------|
| 14:22:01 | swift | "Suspicious probe value 0.0000" |
| 14:22:08 | swift | Aircraft Timeout 15.708ms |
| 14:22:38 | swift | "Too many queued messages (58), bulk send!" |
| 14:22:41 | swift | "Invalid situation, diff. 12.200ms" |
| 14:23:11 | swift | DBus Timeout — xswiftbus antwortet nicht mehr |
| 14:23:19 | User | Desktop sichtbar (Wofi geöffnet) |
| 14:23:38 | swift | "XPlane xSwiftBus service unregistered" — Exit |

#### dmesg / Kernel-Log

Keine NVIDIA Xid-Errors, keine GPU-bezogenen Kernel-Meldungen. NVIDIA 580.x verwendet GSP-Firmware, die GPU-Resets intern abhandelt. Ob ein Reset stattfand, ist **nicht verifizierbar** — die Daten fehlen.

### 4.2 Diagnose: Vulkan Device Loss

Das Symptommuster ist konsistent mit **Vulkan Device Loss** (`VK_ERROR_DEVICE_LOST`):

| Symptom | Beobachtet | Passt zu Device Loss |
|---------|-----------|---------------------|
| GPU bei 0%, Prozess läuft weiter | Ja (14:23:00–14:23:38) | Ja |
| Log endet abrupt ohne Crash-Handler | Ja | Ja |
| Kein Kernel-Signal (OOM/Segfault) | Ja | Ja |
| VRAM wird schlagartig freigegeben | Ja (22.594→3.468 MiB) | Ja |

Laminar Research beschreibt den Mechanismus:

> *"Command buffers get 2 seconds to execute, otherwise the operating system will reset the GPU."*
> *"By the time the CPU realizes the GPU is dead, it's too late to gather data anymore."*
> — [What's up with device losses in X-Plane anyways?](https://developer.x-plane.com/2025/05/whats-up-with-device-losses-in-x-plane-anyways/) (Mai 2025)

**Konfidenz: HOCH** — alle beobachteten Symptome passen, keine Symptome widersprechen.

### 4.3 Trigger-Hypothesen — Wahrscheinlichkeitsbewertung

Der Device Loss steht fest. Was den GPU-Hang **ausgelöst** hat, ist mit den vorhandenen Daten **nicht bestimmbar**. Es fehlen: NVIDIA Xid-Daten (GSP unterdrückt), X-Plane Aftermath-Diagnostik (`--aftermath` war nicht aktiv), GPU-Temperatur/Throttle-Logs.

Die folgenden Hypothesen sind nach verfügbarer Evidenz bewertet.

#### H1: Gamescope VK_KHR_present_wait Deadlock

**Hypothese:** Gamescopes WSI-Layer deadlockt mit NVIDIAs `VK_KHR_present_wait`-Implementierung auf dem X11-Pfad. Frame-Präsentation stoppt, Command-Buffers stauen sich, 2s-Timeout wird überschritten.

**Evidenz dafür:**

- **Gamescope war aktiv** — bestätigt durch Startskript `~/bin/run_xplane.sh`: alle Profile (0–7) starten X-Plane via `gamescope --prefer-vk-device NVIDIA -f -W 3840 -H 2160 -r 60 -- ./X-Plane-x86_64`
- **X11-Pfad erzwungen** — Skript setzt `SDL_VIDEODRIVER=x11`, `XDG_SESSION_TYPE=x11`, `GDK_BACKEND=x11`, `QT_QPA_PLATFORM=xcb`
- Dokumentierter Bug: [gamescope #1592](https://github.com/ValveSoftware/gamescope/issues/1592), mehrfach reproduziert auf RTX 4080/4090
- Der Wayland-Fix (NVIDIA 575.51.02, Bug #4924590) **greift nicht** — das Skript erzwingt den X11-Pfad
- Der **X11-spezifische VK_KHR_present_wait-Bug** (DRI3-Synchronisation) ist weiterhin offen, auch in NVIDIA 590.x ([NVIDIA Forum](https://forums.developer.nvidia.com/t/the-possible-root-cause-of-the-vk-khr-present-wait-and-vulkan-related-freezes/328932))
- `NVPRESENT_ENABLE_SMOOTH_MOTION=1` (Profil 1–7) fügt eine zusätzliche Frame-Pacing-Ebene hinzu, die mit `VK_KHR_present_wait` interagieren kann
- Symptome identisch: Frame friert ein, Audio/Prozess laufen weiter, GPU stoppt
- `GAMESCOPE_WSI_HIDE_PRESENT_WAIT_EXT=1` ist **nicht** gesetzt — Workaround nicht aktiv

**Evidenz dagegen:**

- Nur ein beobachteter Crash in 143 Min Monitoring — bei einem systematischen Deadlock wäre eine höhere Frequenz zu erwarten (wobei Race-Conditions stochastisch sind)

**Wahrscheinlichkeit: HOCH** — gamescope + X11-Pfad + offener X11-Bug + keine Workaround-Variable. Alle Voraussetzungen für den bekannten Bug sind erfüllt.

**Testplan:** `run_xplane_x11.sh` existiert als direkter X11-Start **ohne** gamescope — ideales Kontrollexperiment.

#### H2: VRAM-Exhaustion → Allocation-Timeout

**Hypothese:** Bei 92% VRAM-Auslastung (1.970 MiB frei) schlägt eine Vulkan-Allokation fehl. X-Planes Texture Pager (seit 12.2.0: bis zu 5 Retries mit Defragmenter-Wartezeit) verlängert die Command-Buffer-Laufzeit über 2 Sekunden.

**Evidenz dafür:**

- VRAM bei 92% ist hoch, X-Plane 12.2+ Retry-Logik dokumentiert ([Release Notes](https://www.x-plane.com/kb/x-plane-12-2-0-release-notes/))
- 40+ AI-Flugzeuge (CSL-Modelle) + FUSE-Ortho beanspruchen VRAM

**Evidenz dagegen:**

- 1.970 MiB frei ≈ 2 GB — nicht kritisch für eine einzelne Allokation
- VRAM war seit ~14:00 stabil bei 22.594 MiB — keine progressive Verschlechterung
- Laminar stellt klar: VRAM-Erschöpfung und Device Loss sind **verschiedene Probleme**

**Wahrscheinlichkeit: NIEDRIG** als alleiniger Trigger. Plausibel als verstärkender Faktor, wenn ein anderer Trigger bereits vorliegt.

#### H3: NVIDIA Driver-Bug (Vulkan-Synchronisation)

**Hypothese:** Interner NVIDIA-Driver-Bug verursacht GPU-Hang, unabhängig von der Anwendung.

**Evidenz dafür:**

- 580.x hatte dokumentierte Vulkan-Probleme: Swapchain-Hang nach Device Loss (580.65.06), GTK4-Regression (580.65.06)
- GSP-Firmware (seit Driver 555+) handelt Recovery intern ab — Xid-Errors werden nicht propagiert, was Diagnose unmöglich macht

**Evidenz dagegen:**

- Die genannten Bugs sind in 580.65.06 gefixt, User hat 580.126.18
- Kein spezifischer bekannter Bug in 580.126.18, der dieses Szenario beschreibt

**Wahrscheinlichkeit: MÖGLICH** — ohne Xid-Daten und GSP-Logs nicht verifizierbar. Driver-Bugs lassen sich erst nach Aktivierung der Debug-Logs bewerten.

#### H4: X-Plane GPU-Fault (Shader/Buffer-Fehler)

**Hypothese:** X-Plane submittet einen fehlerhaften Vulkan-Command (z.B. Out-of-Bounds Shader-Zugriff, korrupter Push-Buffer), der die GPU zum Hängen bringt.

**Evidenz dafür:**

- Laminar bestätigt, dass GPU-Faults in X-Plane auftreten können
- `--aftermath` wurde genau dafür entwickelt (injiziert Checkpoints in die Command-Submission)

**Evidenz dagegen:**

- Kein bekannter X-Plane 12.3/12.4 Bug, der systematisch Device Loss verursacht
- Keine Hinweise im X-Plane-Log

**Wahrscheinlichkeit: MÖGLICH** — ohne `--aftermath`-Daten nicht bewertbar.

#### H5: Memory Pressure → Render-Thread-Stall → Command-Buffer-Timeout

**Hypothese:** Eine Memory-Pressure-Kaskade (Direct Reclaim, TLB-Shootdowns) blockiert den Render-Thread so lange, dass Command-Buffers das 2s-Timeout überschreiten.

**Evidenz dafür:**

- 5 Kaskaden in 43 Minuten dokumentiert, TLB-Peaks bis 7,7M/s
- Theoretisch kann ein gesperrter Render-Thread die GPU aushungern

**Evidenz dagegen:**

- **Zeitlinie widerspricht:** GPU war um 14:23:00 bereits bei 6% Utilization — **vor** dem kswapd-Burst um 14:23:15 (242K pages/s, moderat)
- Die 5 vorherigen Kaskaden (13:47–14:20) waren jeweils deutlich schwerer (bis 10.900 Stalls/s) und verursachten **keinen** Crash
- Der kswapd-Burst bei 14:23:15 könnte sogar **Folge** des GPU-Sterbens sein (veränderte Speicherzugriffsmuster)

**Wahrscheinlichkeit: NIEDRIG** als direkter Trigger. Die Zeitlinie ist inkompatibel — die GPU starb vor der Pressure.

### 4.4 Zusammenfassung Trigger-Bewertung

| # | Hypothese | Wahrscheinlichkeit | Fehlende Daten |
|---|-----------|-------------------|----------------|
| H1 | Gamescope present_wait Deadlock (X11-Pfad) | **HOCH** (gamescope+X11 bestätigt, Bug offen) | Kontrolltest ohne gamescope |
| H2 | VRAM Allocation Timeout | NIEDRIG (als Verstärker: MITTEL) | Aftermath-Diagnostik |
| H3 | NVIDIA Driver-Bug | MÖGLICH | GSP-Logs, Xid-Daten |
| H4 | X-Plane GPU-Fault | MÖGLICH | Aftermath-Diagnostik |
| H5 | Memory Pressure → Thread-Stall | **NIEDRIG** (Zeitlinie widerspricht) | Direct-Reclaim-Tracepoints |

**Fazit:** Die vorhandenen Monitoring-Daten reichen aus, um den Device Loss zu **diagnostizieren**, aber nicht, um den Trigger zu **identifizieren**. Run G muss gezielt die fehlenden Daten erheben.

---

## 5. Gesamtbewertung Tuning

### Erreicht

1. **zram absorbiert 100% des Swap** — NVMe-Swap nicht angesprochen
2. **Write-Volumen Swap-Drive -86%** — IO-Kontention eliminiert
3. **Dirty Pages -94%** — Writeback prompt
4. **Steady-State exzellent** — alle Metriken in Teil 2 im grünen Bereich
5. **DSF-Worst-Case 63s → 22s**
6. **EMFILE -39%**

### Nicht erreicht

1. **Memory-Pressure bei Szenerieübergängen** — Direct Reclaim und TLB-Shootdowns in Teil 1 weiterhin signifikant
2. **EMFILE nicht eliminiert** — 1.343 vom XEL-Cache-Startup (4M+ Dateien, XEL-intern)
3. **DSF > 10s** — 5 Fälle bei initialer Ladung
4. **Write-Latenz-Tail 476ms** in Teil 1 (Btrfs-Metadata unter Last)

### Crash-Einordnung

Vulkan Device Loss — **kein Tuning-Problem**. Trigger unbekannt, Diagnostik-Daten fehlen. Kein Bezug zu den umgesetzten sysctl/IO/zram-Änderungen.

---

## 6. Priorisierter Aktionsplan Run G

### Ziel

Zwei Fragen beantworten:

1. **Was hat den GPU-Hang ausgelöst?** → Diagnostik-Instrumentierung
2. **Lassen sich die Memory-Pressure-Spitzen bei Szenerieübergängen reduzieren?** → XEL-Tuning

### Prio 1 — Gamescope/present_wait isolieren (höchste Crash-Wahrscheinlichkeit)

Startskript-Analyse bestätigt: `run_xplane.sh` startet gamescope mit erzwungenem X11-Pfad. Der offene X11-VK_KHR_present_wait-Bug ([NVIDIA Forum](https://forums.developer.nvidia.com/t/the-possible-root-cause-of-the-vk-khr-present-wait-and-vulkan-related-freezes/328932)) trifft exakt diese Konfiguration.

| # | Test | Wie | Was es beweist |
|---|------|-----|---------------|
| 1a | **Kontrollflug ohne gamescope** | `run_xplane_x11.sh` statt `run_xplane.sh` verwenden. Gleiche Route, gleiche Dauer, gleiche Plugins. | Kein Crash → gamescope ist Trigger. Crash → gamescope ist nicht (allein) schuld. |
| 1b | **Alternativ: Workaround testen** | In `run_xplane.sh` vor dem gamescope-Aufruf hinzufügen: `export GAMESCOPE_WSI_HIDE_PRESENT_WAIT_EXT=1` | Kein Crash → present_wait bestätigt. Crash → anderer Trigger. |

**Empfehlung:** Zuerst 1a (ohne gamescope), weil es die sauberste Isolation ist. 1b nur, wenn gamescope für den Workflow zwingend benötigt wird.

### Prio 2 — Crash-Diagnostik (einmalig einrichten, vor jedem Flug aktiv)

Diese Maßnahmen erzeugen **kein** oder **vernachlässigbares** Performance-Overhead. Sie liefern Daten für den Fall, dass der Crash auch ohne gamescope auftritt.

| # | Maßnahme | Was es liefert | Aufwand |
|---|----------|---------------|---------|
| 2a | **NVIDIA GSP-Firmware-Logs aktivieren** | Xid-Errors, die GSP aktuell unterdrückt | `/etc/modprobe.d/nvidia-debug.conf`: `options nvidia NVreg_EnableGpuFirmwareLogs=1 NVreg_RmMsg="gsp@3^t,@4^t"` + `update-initramfs -u` + Reboot |
| 2b | **X-Plane mit `--aftermath` starten** | GPU-Crash-Checkpoints — identifiziert den fehlerhaften Draw/Dispatch-Call bei Device Loss | Startparameter `./X-Plane --aftermath` (in Startskript einbauen) |
| 2c | **Xid-Monitor im Hintergrund** | Echtzeit-Protokoll aller GPU-Events | `journalctl -k --grep="NVRM\|Xid" -f > /tmp/sysmon_out/xid.log &` |
| 2d | **dmesg-Snapshot vor/nach Flug** | Kernel-Meldungen die sonst im Ringbuffer verloren gehen | `dmesg -T > pre.log` / `dmesg -T > post.log` |
| 2e | **Journal-Persistenz + Rate-Limit deaktivieren** | Verhindert Verlust von GPU-Meldungen bei Burst | `/etc/systemd/journald.conf.d/no-ratelimit.conf`: `RateLimitIntervalSec=0` |

### Prio 3 — Erweitertes GPU-Monitoring (in sysmon.py integrieren)

Low-Overhead-Erweiterungen für die bestehende Monitoring-Infrastruktur.

| # | Erweiterung | Was es liefert | Overhead |
|---|------------|---------------|----------|
| 2a | **nvidia-smi CSV-Logging** (1s-Intervall) | GPU-Temp, Clocks, Throttle-Reasons, PCIe-Link-Status — lückenlose GPU-Zustandshistorie bis zum Crash | Vernachlässigbar |
| | `nvidia-smi --query-gpu=timestamp,power.draw,temperature.gpu,clocks.current.graphics,clocks.current.memory,memory.used,utilization.gpu,clocks_event_reasons.active,pcie.link.gen.gpucurrent,pcie.link.width.current --format=csv --loop=1` | | |
| 2b | **NVML-Erweiterungen in sysmon.py** | PCIe TX/RX Throughput, Throttle-Reason-Bitmask, Performance-State | Null (NVML bereits initialisiert) |
| 2c | **vmstat-Felder erweitern** | `pswpin`/`pswpout` (Swap-IO), `workingset_refault_anon`/`file` (Thrashing), `thp_fault_fallback` (Fragmentierung) | Null (Datei wird bereits gelesen) |

### Prio 4 — Memory-Pressure-Tracing (bpftrace-Sidecar)

Separate Prozesse neben sysmon.py. Liefern per-Event-Auflösung statt Sekunden-Aggregation.

| # | Tracepoint | Was es liefert | Overhead |
|---|-----------|---------------|----------|
| 3a | **Direct Reclaim** (`vmscan:mm_vmscan_direct_reclaim_begin/end`) | Exakte Dauer jedes Reclaim-Events pro Prozess. Zeigt ob X-Plane-Render-Thread betroffen ist. | Niedrig (Event-basiert) |
| 3b | **Slow IO** (`block:block_rq_issue/complete`, Filter >5ms) | NVMe-IO-Ausreißer mit Device und Sektor. Korreliert mit DSF-Stalls. | Niedrig (nur Ausreißer) |
| 3c | **DMA Fence Waits** (`dma_fence:dma_fence_wait_start/end`) | CPU-Wartezeiten auf GPU-Completion. Zeigt ob GPU die CPU blockiert. | Niedrig |

### Prio 5 — Post-Crash-Sofortmaßnahmen

Falls ein weiterer Device Loss auftritt:

1. **Sofort** (vor Reboot): `sudo nvidia-bug-report.sh` → `/tmp/nvidia-freeze-$(date +%s).log.gz`
2. Falls nvidia-smi hängt: `sudo nvidia-bug-report.sh --safe-mode`
3. `dmesg -T > /tmp/dmesg_crash.log`
4. `journalctl -k --since "30 min ago" --grep="NVRM\|Xid\|drm\|nvidia" > /tmp/journal_crash.log`

### Prio 6 — Tuning-Tests (optional, nach Crash-Klärung)

| # | Maßnahme | Ziel |
|---|----------|------|
| 5a | XEL `max_concurrent_jobs` 12 → 8 | EMFILE Burst 2 reduzieren |
| 5b | XEL `prefetch.mode = disabled` (einmalig) | Isoliert XEL-Prefetch als Ursache der Thread-Explosionen |

### Nicht umsetzen (kein Handlungsbedarf)

| Maßnahme | Begründung |
|----------|------------|
| Plan B (nvme1n1p4 Swap) | zram absorbiert 100% bei 79% Peak |
| zram auf 48 GB erhöhen | 79% Peak bietet 21% Headroom, reicht für diese Flugdauer |
| Vulkan Validation Layers | Zu hohes Overhead für einen Flug-Run, nur für isolierte Reproduktion |
| PSI-Monitoring | Liquorix kompiliert ohne CONFIG_PSI, vmstat+Tracepoints liefern bessere Daten |

---

## 7. Monitoring-Daten

| Teil | Verzeichnis | Dauer | Szenario |
|------|-------------|-------|----------|
| F/1 | `monitoring/run_F_part1/` | 90 Min | Crash, Neustart, initiale Szenerieladung |
| F/2 | `monitoring/run_F_part2/` | 53 Min | Stabiler Flug, warmer Cache |
| Crash-Log | `X-Plane-12/Output/Log Archive/Log-2026-02-22-1422.txt` | — | 28.234 Zeilen |

### zram-Status nach Flug

```
NAME       ALGORITHM DISKSIZE  DATA COMPR TOTAL STREAMS MOUNTPOINT
/dev/zram0 lz4            32G 17,1G 14,6G   15G         [SWAP]
```

### Swap-Status nach Flug

```
Filename            Type       Size        Used       Priority
/dev/nvme2n1p5      partition  124999676   2814092    -2
/dev/zram0          partition  33554428    18367656   100
```

### Peak-Werte Teil 1

| Metrik | Peak | Zeitpunkt |
|--------|------|-----------|
| Page Faults/s (minor) | 1.678.510 | 13:47:20 |
| Major Faults/s | 159.072 | 14:23:15 |
| Alloc Stalls/s | 10.900 | 13:58:26 |
| Context Switches/s | 1.350.948 | 13:47:29 |
| kswapd Scan/s | 2.136.613 | 13:47:28 |
| Direct Reclaim Scan/s | 762.842 | 13:57:54 |
| TLB Shootdowns/s (IRQ) | 7.687.952 | 13:47:47 |
| X-Plane io_read | 7.805 MB/s | 13:47:28 |
| XEL CPU% | 1.052% | 13:47:20 |
| Swap Used | 22.911 MB | 14:15:40 |
| VRAM bei Crash | 22.594 MiB (92%) | 14:23:32 |
| GPU Util Tiefpunkt | 0% | 14:23:33 |
