# Performance

X-Plane ist ein Hybrid aus Echtzeit-Physiksimulation, massivem Daten-I/O und — bei Ortho-Streaming — kontinuierlichem Netzwerkverkehr. Diese drei Lastdimensionen konkurrieren um gemeinsame Ressourcen: CPU-Zyklen, Cache, Memory-Bandbreite und PCIe-Lanes. Der Engpass wechselt dynamisch — beim Laden dominiert die SSD, im Flug die CPU, beim Streaming das Netzwerk. Die Kapitel in dieser Sektion erklären, wo die Engpässe entstehen und wie sie sich gegenseitig verstärken.

Der Hauptthread bleibt der zentrale Flaschenhals: Physik, Avionics und Render-Vorbereitung laufen sequentiell auf einem Kern. Multi-Threading für Scenery-Processing entlastet diesen Kern, verbessert aber primär die schlimmsten Einzelframes (P95/P99), nicht den FPS-Durchschnitt. VRAM-Management liegt vollständig bei X-Plane — kein Streaming-Tool greift direkt auf den Grafikspeicher zu. Der Bedarf wächst exponentiell mit dem Zoom Level, und das Verhalten bei Überlauf unterscheidet sich unter Linux fundamental je nach GPU-Treiber. Frame-Time-Perzentile offenbaren, was FPS-Durchschnitte verschleiern.

- **[Zusammenspiel](performance_overview.md)** — CPU, I/O und Netzwerk: Engpässe erkennen
- **[CPU & RAM](cpu_ram.md)** — Threading-Modell, Kern-Verteilung und Arbeitsspeicher als Zwischenstufe
- **[GPU & VRAM](gpu_vram.md)** — Texture Paging, Treiber-Unterschiede und Frame-Time-Analyse
