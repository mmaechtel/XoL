# Einführung

<div class="video-container" markdown>
<video controls width="100%" preload="metadata" poster="../assets/video/de/X-Plane_unter_Linux__Doku-Tour/X-Plane_unter_Linux__Doku-Tour.jpg">
  <source src="../assets/video/de/X-Plane_unter_Linux__Doku-Tour/X-Plane_unter_Linux__Doku-Tour.mp4" type="video/mp4">
</video>
</div>

??? abstract "Was X-Plane besonders macht"

    [X-Plane](glossary.md#x-plane) hebt sich von anderen Flugsimulatoren durch seinen simulationsorientierten Ansatz ab. Die Flugphysik basiert auf der [Blade Element Theory](glossary.md#blade-element-theory) — statt vorgefertigter Tabellen werden Strömung und Kräfte in Echtzeit für jedes Flugzeugsegment berechnet. Das erstreckt sich auf Triebwerks- und Systemsimulation sowie Wetter mit atmosphärischen Effekten.

    Die Rendering-Engine nutzt [PBR](glossary.md#pbr) für physikalisch korrekte Materialdarstellung, kombiniert mit dynamischer Beleuchtung, atmosphärischen Effekten, Echtzeit-Reflexionen und [HDR](glossary.md#hdr)-Rendering. Der Fokus liegt auf realistischer statt künstlerischer Interpretation.

    Die offene [Plugin](glossary.md#plugin)-Architektur von X-Plane ermöglicht tiefgreifende Anpassungen — von eigenen Flugzeugmodellen über FlyWithLua-Skripte bis hin zu Tools von Drittanbietern. Die Simulations-Engine wird aktiv weiterentwickelt, wobei X-Plane 12 einen erheblichen Teil der Rendering-Arbeit auf mehrere CPU-Kerne verteilt, während der Physik-Hauptthread an einen einzelnen Kern gebunden bleibt.

## Warum X-Plane unter Linux?

Die kurze Antwort: Weil der gesamte Stack offen ist. Der Linux-Kernel, die GPU-Treiber ([Mesa](glossary.md#mesa)/[RADV](glossary.md#radv) für AMD, [ANV](glossary.md#anv) für Intel), der Display-Server, das Dateisystem — alles Open Source. Das ist kein ideologischer Punkt, sondern ein praktischer: Open Source ist der Grund, warum sich ein Linux-System für X-Plane auf eine Weise optimieren lässt, die auf einer geschlossenen Plattform schlicht nicht möglich ist.

Jede Optimierung, die diese Dokumentation beschreibt — vom CPU-Scheduling über Interrupt-Routing bis zur Shader-Cache-Konfiguration — existiert, weil der Quellcode verfügbar ist, die Schnittstellen dokumentiert sind und die Community den Stack kontinuierlich verbessert. [Zink](glossary.md#zink), die OpenGL-zu-Vulkan-Übersetzungsschicht, die für die Plugin-Kompatibilität von X-Plane entscheidend ist, ist ein Open-Source-Mesa-Projekt. Die Vulkan-Treiber, die X-Planes Rendering antreiben, werden offen entwickelt. Performance-Verbesserungen fließen direkt aus Community-Beiträgen ein.

Diese Transparenz hat konkrete Auswirkungen auf die Flugsimulation:

- **Kernel-Tuning:** Präzise Kontrolle über CPU-Governor, Interrupt-Affinität und Scheduling — behandelt in [System-Tuning](systemtuning.md) und [Liquorix-Kernel](liquorix.md)
- **Keine Hintergrund-Störungen:** Keine automatischen Updates oder Telemetrie, die während des Fluges um CPU-Zyklen konkurrieren. Die Systemleistung ist vorhersagbar.
- **Display-Server-Wahl:** [Wayland oder X11](displayserver.md) lassen sich je nach GPU und Compositor-Verhalten auswählen
- **Treiber-Kontrolle:** GPU-Treiberversion, Persistence Mode und Energieverwaltung sind frei konfigurierbar — siehe [Nvidia-Treiber](nvidia.md)
- **Dateisystem-Optimierung:** Mount-Optionen, I/O-Scheduler und TRIM lassen sich für schnelles Szenerie-Laden anpassen — siehe [Dateisystem](filesystem.md)
- **Nachvollziehbarkeit:** Wenn Mikroruckler auftreten, lässt sich die Ursache bis auf Kernel-Ebene zurückverfolgen — Scheduler-Entscheidungen, Interrupt-Timing, Treiber-Verhalten. Nichts ist eine Black Box.
- **Stabilität:** Debian Stable bietet eine vorhersagbare Basis ohne überraschende OS-Upgrades, erzwungene Neustarts oder Breaking Changes während einer Session.

Der Kompromiss: Einrichtung und Tuning erfordern mehr Aufwand als unter Windows. Aber dies ist keine Plattform, auf der eine Checkliste reicht — derselbe Kernel-Parameter kann die Performance verbessern oder verschlechtern, je nachdem welcher Kernel läuft. Diese Dokumentation liefert das Hintergrundwissen für fundierte Entscheidungen: wie Scheduling und Latenz funktionieren, warum zwei Kernel gegensätzliche Tuning-Strategien brauchen, und wo jede Optimierung einen messbaren Unterschied macht. [Erste Schritte](begin.md) behandelt Systemvoraussetzungen und Installation.

Quellen:

- [Offizielle X-Plane-Website](https://www.x-plane.com/)
