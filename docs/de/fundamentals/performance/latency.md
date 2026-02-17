# Latenz und Vorhersagbarkeit

X-Plane berechnet eine komplexe Welt mit Physik, Wetter, Szenerie und Eingabegeräten. Dabei entscheidet nicht die maximale Rechenleistung über die Ergebnisqualität, sondern die zeitliche Vorhersagbarkeit — wie gleichmäßig jeder einzelne Frame berechnet wird. Dieses Kapitel erklärt, warum Latenz das eigentliche Problem ist und welche Systemquellen sie verursachen. Die drei Lastdimensionen (CPU, I/O, Netzwerk) und ihre Wechselwirkungen beschreibt das Kapitel [Lastdimensionen](performance_overview.md).

## Performance und Latenz — ein wichtiger Unterschied

Wer von „Performance" spricht, meint oft hohe FPS. Das ist bei Shootern oder Rennspielen richtig — dort zählt Durchsatz: möglichst viele Bilder pro Sekunde. Bei einem Flugsimulator wie X-Plane liegt der Fall anders.

X-Plane berechnet eine komplexe Welt mit Physik, Wetter, Szenerie und Eingabegeräten. Einzelne Frames sind aufwändig, und die Ziel-Framerate liegt typisch bei 25–35 [FPS](../../glossary.md#fps-frames-per-second). Entscheidend ist nicht der Durchschnitt, sondern die **Gleichmäßigkeit** — also die [Frame-Time](../../glossary.md#frame-time)-Konsistenz. Ein System, das stabil 35 FPS liefert, erzeugt flüssigere Bewegung als eines, das zwischen 25 und 50 schwankt.

Die Ursache für Ungleichmäßigkeit ist in den meisten Fällen nicht fehlende Rechenleistung, sondern **[Latenz](../../glossary.md#latenz)** — kurze Verzögerungen durch Systemereignisse, die den Hauptthread unterbrechen.

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

**Scheduling**

Der Linux-Scheduler entscheidet, wann ein Thread Rechenzeit bekommt. Ein konservativer Scheduler wartet länger, bevor er reagiert — das spart Energie, erhöht aber die Latenz. Moderne Scheduler nutzen Deadline-basierte Aufgabenauswahl und adaptive [Preemption](../../glossary.md#preemption), sodass latenzsensitive Threads effizienter eingeplant werden.

**Energieverwaltung**

Nicht die CPU-Last verursacht Ruckler, sondern Übergänge zwischen Energiestufen. Wenn ein Kern aus einem tiefen Schlafzustand aufwacht, entstehen Verzögerungen von bis zu mehreren hundert Mikrosekunden. Auch [NVMe](../../glossary.md#nvme-non-volatile-memory-express)-SSDs im Energiesparmodus erzeugen spürbare Aufwachlatenzen (Details unter [NVMe Energiesparen deaktivieren](../../linux/system/systemtuning.md#nvme-energiesparen-deaktivieren)).

**Interrupts**

Hardware-Interrupts (USB-Geräte, Netzwerk, Storage) unterbrechen den laufenden Thread. Ein einzelner Interrupt zur falschen Zeit kann eine Frame-Deadline verletzen:

```
periodischer Hauptthread + zufälliger Interrupt = verpasste Deadline
```

**Speicher/IO**

Der Kernel optimiert Durchsatz durch gebündelte Hintergrundarbeit (Writeback, Cache-Bereinigung, Paging). Das erzeugt seltene, aber spürbare Blockierungen — besonders beim Laden großer Ortho-Texturen.

---

## Weiterführende Kapitel

| Thema | Seite | Schwerpunkt |
|---|---|---|
| Kernel-Tuning | [Kernel-Tuning](../../linux/system/systemtuning.md) | Konkrete Parameter für beide Kernel-Profile |
| Lastdimensionen | [Lastdimensionen](performance_overview.md) | CPU, I/O, Netzwerk — Engpässe erkennen |
| CPU & RAM | [CPU & RAM](cpu_ram.md) | Threading-Modell, Hauptthread als Engpass |
| GPU & VRAM | [GPU & VRAM](gpu_vram.md) | Frame-Time-Perzentile, VRAM-Druck |
| Low-Latency-Kernel | [Liquorix](../../linux/optimizations/liquorix.md) | Scheduler, Preemption-Tuning |
| Warum Latenz zählt | [Warum Latenz zählt](../../linux/system/latency.md) | Einführung und Video |
| Monitoring | [System Monitoring](../../linux/system/systemtools.md) | Latenz messen und verifizieren |
