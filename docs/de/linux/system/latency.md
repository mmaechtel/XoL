# Warum Latenz zählt

<div class="video-container" markdown>
<video controls width="100%" preload="metadata" aria-label="Video: System-Tuning für X-Plane" poster="../../../assets/video/de/System-Tuning_für_X-Plane/System-Tuning_für_X-Plane.jpg">
  <source src="../../../assets/video/de/System-Tuning_für_X-Plane/System-Tuning_für_X-Plane.mp4" type="video/mp4">
</video>
</div>

Für X-Plane zählt nicht maximaler Durchsatz, sondern zeitliche Vorhersagbarkeit — ein stabiles 35-FPS-Bild wirkt flüssiger als eines, das zwischen 25 und 50 schwankt. Mikro-Ruckler entstehen selten durch fehlende Rechenleistung, sondern durch Latenz: Scheduling-Verzögerungen, CPU-Aufwachzeiten aus Schlafzuständen, Interrupts zur falschen Zeit und blockierende Speicheroperationen. Die Tuning-Seite zeigt zwei Kernel-Profile — das Standard-Profil erzwingt Priorität für die Anwendung, das Liquorix-Profil entfernt externe Störquellen —, die jeweils auf das Scheduling-Modell des Kernels abgestimmt sind. Die gleichen Parameter auf dem falschen Kernel angewendet verschlechtern das Ergebnis.

Die Monitoring-Seite liefert die Werkzeuge, um jede Tuning-Maßnahme zu verifizieren: Ist der Governor tatsächlich aktiv? Landen Interrupts auf den geschützten Kernen? Verursacht die NVMe Aufwach-Latenzen? Jedes Tool — von turbostat über mpstat bis ioping — ist einer konkreten Tuning-Einstellung zugeordnet.

Die theoretischen Grundlagen — warum Latenz wichtiger ist als Durchsatz und welche Systemquellen Latenz erzeugen — beschreibt das Kapitel [Latenz und Vorhersagbarkeit](../../fundamentals/performance/latency.md).

- **[Tuning](systemtuning.md)** — Kernel-Parameter, CPU-Governor, Interrupt-Affinität, NVMe-Tuning
- **[Monitoring](systemtools.md)** — btop, turbostat, perf, mpstat und weitere Analyse-Tools
