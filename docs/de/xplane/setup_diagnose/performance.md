---
description: "Performance-Analyse von X-Plane 12 unter Linux: Microprofiler für CPU/GPU-Engpässe, MangoHUD-Frametime-Overlay, GPU-Monitoring und Optimierungstipps."
---
# X-Plane Performance unter Linux

X-Plane 12 ist eine Cross-Plattform-Anwendung — die allgemeinen Grafikeinstellungen (Texturen, Schatten, Wolken, Antialiasing) funktionieren auf allen Betriebssystemen gleich und sind im [X-Plane 12 Desktop Manual](https://www.x-plane.com/manuals/desktop/) beschrieben. Diese Seite behandelt die Performance-**Analyse** unter Linux: interne Diagnose-Tools, Linux-spezifische Monitoring-Werkzeuge und gezielte Optimierungsempfehlungen. Die Linux-Grafikeinstellungen selbst sind unter [Konfiguration](config.md) dokumentiert, Systemtuning unter [Systemtuning](../../linux/system/systemtuning.md).

## Interne Diagnose-Tools

### FPS-Anzeige

Die FPS-Anzeige (Frames per Second) ist das einfachste Werkzeug zur Performance-Einschätzung. Sie zeigt, wie viele Bilder pro Sekunde berechnet werden — doch der Durchschnittswert allein ist wenig aussagekräftig. Entscheidend ist die Frame Time: die Zeit in Millisekunden, die ein einzelnes Bild benötigt. Ein stabiler FPS-Wert von 30 (≈ 33 ms pro Frame) liefert ein flüssigeres Ergebnis als ein schwankender Durchschnitt von 40 FPS mit regelmäßigen Spikes auf 60 ms.

**Richtwerte**

| FPS | Frame Time | Bewertung |
|-----|------------|-----------|
| 50+ | < 20 ms | Sehr flüssig |
| 30–49 | 20–33 ms | Flüssig |
| 20–29 | 33–50 ms | Akzeptabel |
| < 20 | > 50 ms | Deutliche Ruckler |

**Aktivierung:** Im Menü unter *Settings → Data Output* die Option *frame rate* aktivieren. Die Anzeige erscheint in der oberen linken Bildschirmecke. Alternativ lässt sich die FPS-Anzeige per Tastenkürzel `Shift+Strg+F` ein- und ausblenden — sofern die Belegung nicht geändert wurde.

### Microprofiler

Während die FPS-Anzeige nur das Gesamtergebnis zeigt, schlüsselt der Microprofiler die Frame-Generierung in einzelne Aufgaben auf. So lässt sich erkennen, ob Physikberechnungen, Szenerie-Rendering, Plugins oder die GPU den Engpass verursachen.

**Aktivierung:** Im Menü *Developer → Toggle Microprofiler* wählen. Eine grafische Echtzeitanzeige erscheint, die die Zeitverteilung pro Frame darstellt.

**Aufgabenkategorien**

| Kategorie | Was wird gemessen | Typische Werte (30 FPS) |
|-----------|-------------------|-------------------------|
| Flight Model | Physik und Aerodynamik | 5–15 ms |
| Scenery | Landschaft, Gebäude, Straßen | 5–10 ms |
| Clouds/Weather | Wolken, Regen, Nebel | 3–8 ms |
| Plugins | Installierte Plugins und Addons | 2–10 ms |
| Swapchain Acquire | CPU/GPU-Synchronisation | 1–5 ms |

**CPU-bound vs. GPU-bound erkennen**

Die Gesamtzeit teilt sich in CPU-Zeit (Physik, Plugins, Szenerie-Logik) und GPU-Zeit (Texturen, Schatten, Wolken). Liegt die CPU-Zeit deutlich über der GPU-Zeit, ist der Prozessor der Engpass — Grafikeinstellungen zu senken bringt dann wenig. Umgekehrt hilft bei GPU-Engpässen eine Reduktion von Texturqualität, Schatten oder Antialiasing. Die Tabelle im Abschnitt [Optimierungstipps](#optimierungstipps) ordnet jedem Engpass konkrete Maßnahmen zu.

**Rechenbeispiel**

| Komponente | Zeit |
|------------|------|
| **Framezeit gesamt** | **33,3 ms (30 FPS)** |
| Physikberechnung | 10 ms |
| Szenerie-Rendering | 8 ms |
| Wolken/Wetter | 7 ms |
| Plugins | 5 ms |
| Swapchain Acquire | 3 ms |
| **CPU-Zeit gesamt** | **20 ms** |
| **GPU-Zeit gesamt** | **13 ms** |

In diesem Beispiel ist die CPU mit 20 ms der limitierende Faktor. Physikberechnungen und Plugin-Last sind die größten Einzelposten — hier setzen die Optimierungen an.

## Externe Tools

X-Plane zeigt **was** langsam ist — Linux-Tools zeigen **warum**. Die internen Diagnose-Tools (Microprofiler, FPS-Anzeige) identifizieren Engpässe innerhalb der Simulation. Externe Tools liefern die System-Perspektive: GPU-Auslastung, CPU-Frequenz, I/O-Wartezeiten und thermische Drosselung.

### MangoHUD — In-Game Performance Overlay

MangoHUD ist ein Vulkan-Layer-Overlay, das Performance-Metriken direkt im Spiel einblendet.

**Installation und Start**

```bash
sudo apt install mangohud
mangohud ./X-Plane-x86_64
```

**Angezeigte Metriken**

- FPS und Frame-Time-Graph
- GPU-Last, Temperatur, Takt und [VRAM](../../glossary.md#vram-video-ram)-Nutzung
- CPU-Last, Temperatur und Frequenz pro Kern
- RAM-Nutzung

**Frame-Time-Graph** — das wichtigste Werkzeug: Spikes zeigen Ruckler, die der FPS-Durchschnitt verbirgt. Ein stabiler Graph bei 33 ms (30 FPS) ist besser als ein schwankender bei 25 ms Durchschnitt.

**Konfiguration**

MangoHUD lässt sich über eine Konfigurationsdatei anpassen. Für X-Plane empfiehlt sich eine kompakte Darstellung:

`~/.config/MangoHud/X-Plane-x86_64.conf`

```ini
fps
frame_timing
gpu_stats
gpu_temp
gpu_core_clock
gpu_mem_clock
vram
cpu_stats
cpu_temp
cpu_mhz
ram
position=top-left
font_size=20
```

**Tastenkürzel**

| Kürzel | Funktion |
|--------|----------|
| `Shift_R+F12` | Overlay ein/aus |
| `Shift_L+F2` | CSV-Logging starten/stoppen |

CSV-Logging zeichnet die Messwerte auf und eignet sich für Post-Flug-Analyse. Das Log-Verzeichnis wird über `output_folder` in der MangoHUD-Konfiguration festgelegt — ohne diese Einstellung landen Logs im `$HOME`-Verzeichnis.

### GPU-Monitoring

| GPU | Tool | Installation | Befehl |
|-----|------|-------------|--------|
| NVIDIA | nvidia-smi | (im Treiber enthalten) | `nvidia-smi dmon` |
| AMD | radeontop | `sudo apt install radeontop` | `sudo radeontop` |
| Intel | intel_gpu_top | `sudo apt install intel-gpu-tools` | `sudo intel_gpu_top` |

Für NVIDIA-Karten lässt sich ein kompakter CSV-Monitor starten:

```bash
nvidia-smi --query-gpu=utilization.gpu,utilization.memory,temperature.gpu,clocks.gr,power.draw --format=csv -l 2
```

**GPU-Bottleneck erkennen**

- GPU 95–100 % + niedrige FPS → GPU-bound (Grafikeinstellungen reduzieren)
- GPU < 70 % + niedrige FPS → CPU-bound (Microprofiler prüfen, welcher Thread blockiert)

## Diagnose-Workflows

Die folgende Tabelle verbindet typische Symptome mit der passenden Werkzeugkette. Details zu den Linux-Tools finden sich unter [System Monitoring](../../linux/system/systemtools.md).

| Symptom | Werkzeugkette | Was prüfen |
|---------|--------------|------------|
| Mikroruckler im Flug | MangoHUD Frame-Time + `iostat` | NVMe-Aufwachlatenz (APST) |
| Niedrige FPS bei geringer GPU-Last | Microprofiler + `htop` | CPU-bound — welcher Thread blockiert? |
| Stutter bei Szenerie-Wechsel | `iotop` + `fatrace` | Welche Dateien werden gelesen? |
| FPS-Einbruch nach Treiber-Update | MangoHUD Vergleich vorher/nachher | Shader-Cache löschen, Treiber-Regression? |
| Periodische Ruckler alle ~30 s | `mpstat -I CPU 1` | IRQ-Sturm auf Applikations-Kernen? |

## Optimierungstipps

Der Microprofiler zeigt, wo die Frame-Zeit verloren geht. Die folgende Tabelle ordnet jedem Engpass die wirksamste Maßnahme zu.

| Engpass | Maßnahme | Einstellung |
|---------|----------|-------------|
| CPU (Physik) | Flight Models reduzieren | Flight Models per Frame: 2–4 |
| CPU (Plugins) | Aufwändige Addons deaktivieren | — |
| CPU (Szenerie) | Objektdichte reduzieren | Object Density senken |
| CPU (Traffic) | KI-Flugzeuge reduzieren | Flight Configuration: weniger AI Aircraft |
| GPU (Texturen) | Texturqualität senken | Texture Quality: Medium oder High |
| GPU (Schatten) | Schatten und Antialiasing reduzieren | Shadow Quality und MSAA-Stufe senken |
| GPU (Wolken) | Wolkenqualität anpassen | Cloud Quality senken |

Für Linux-spezifische Optimierungen (CPU-Governor, Interrupt-Routing, Speicherparameter) siehe [Systemtuning](../../linux/system/systemtuning.md). Benchmarking-Methoden und Rendering-Optionen sind unter [Konfiguration](config.md) dokumentiert.

---

## Weiterführende Kapitel

| Thema | Seite | Schwerpunkt |
|---|---|---|
| Lastdimensionen | [Lastdimensionen](../../fundamentals/performance/performance_overview.md) | Konzeptioneller Rahmen: CPU-, GPU-, VRAM-, I/O-Engpässe |
| Latenz und Vorhersagbarkeit | [Latenztheorie](../../fundamentals/performance/latency.md) | Frame-Time-Analyse, Jitter, Scheduling-Theorie |
| CPU & RAM | [CPU & RAM](../../fundamentals/performance/cpu_ram.md) | CPU-Architektur, Thread-Scheduling, Speicherbandbreite |
| GPU & VRAM | [GPU & VRAM](../../fundamentals/performance/gpu_vram.md) | GPU-Pipeline, VRAM-Budget, Texturkompression |
| Nvidia-Treiber | [Nvidia-Treiber](../../linux/optimizations/nvidia.md) | Treiberinstallation, nvidia-smi, GPU-Konfiguration |
| Geräteverluste | [Geräteverluste](../systemfehler/geraeteverluste.md) | GPU-Crashes: Ursachen, Aftermath-Debugging, Lösung |

---

## Quellen

- [MangoHUD — GitHub](https://github.com/flightlessmango/MangoHud)
- [X-Plane 12 — Desktop Manual](https://www.x-plane.com/manuals/desktop/)
- [nvidia-smi Documentation](https://developer.nvidia.com/nvidia-system-management-interface)
