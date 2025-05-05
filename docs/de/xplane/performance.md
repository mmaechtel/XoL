# X-Plane Performance

Die Performance von X-Plane ist ein entscheidender Faktor für ein flüssiges und realistisches Flugerlebnis. In diesem Kapitel werden verschiedene Aspekte der Performance-Messung und -Optimierung betrachtet.

## Performance-Metriken

X-Plane bietet verschiedene Möglichkeiten, die Performance zu messen und zu überwachen:

### FPS (Frames per Second)

Die FPS-Anzeige ist die grundlegendste Metrik für die Performance in X-Plane. Sie zeigt an, wie viele Bilder pro Sekunde das System berechnet und darstellt. Die Anzeige befindet sich standardmäßig in der oberen linken Ecke des Bildschirms, ist aber nicht aktiviert. In einigen Installationen ist die Anzeige bereits auf einem Hotkey (z.B. Shift+Strg+F) belegt, dieser kann jedoch in den Tastaturbelegungen angepasst werden. Für ein flüssiges Flugerlebnis sollte die FPS-Rate konstant über 30 FPS liegen. Eine Rate unter 19 FPS führt zu ruckeligen Bewegungen und beeinträchtigt die Spielbarkeit, während 25–35 FPS für die meisten Nutzer akzeptabel sind. Ab 50 FPS wird die Simulation als sehr flüssig empfunden.

### Frame Time

Die Frame Time ist eine wichtige Metrik, die die Zeit misst, die für die Berechnung eines einzelnen Frames benötigt wird. Diese Messung ist besonders wertvoll für die Identifizierung von Performance-Engpässen, da sie zeigt, wo genau im Berechnungsprozess Verzögerungen auftreten. Die Frame Time kann über den integrierten X-Plane Performance Monitor eingesehen werden, der detaillierte Einblicke in die verschiedenen Phasen der Frame-Generierung bietet.

### CPU- und GPU-Auslastung

Die Überwachung der CPU- und GPU-Auslastung ist ein entscheidender Aspekt der Performance-Analyse. Diese Metriken helfen dabei, Hardware-Engpässe zu identifizieren und zu verstehen, ob der Prozessor oder die Grafikkarte der limitierende Faktor ist. Für die Überwachung stehen verschiedene System-Monitoring-Tools zur Verfügung, wie beispielsweise `htop` für die CPU-Auslastung oder `nvidia-smi` für NVIDIA-Grafikkarten. Diese Tools liefern detaillierte Informationen über die aktuelle Auslastung und können bei der Optimierung der Systemressourcen helfen.

## Performance-Messung

### Interne Tools

#### X-Plane Performance Monitor

Der integrierte Performance Monitor von X-Plane bietet detaillierte Einblicke in:

- Frame Time
- CPU-Auslastung
- GPU-Auslastung
- Speichernutzung
- Netzwerk-Performance


Um die FPS-Darstellung einzublenden, sind folgende Schritte erforderlich:

1. Die Data Output-Einstellungen in X-Plane öffnen
2. Die FPS-Anzeige aktivieren („frame rate" oder „freq/sec")
3. Optional: Weitere Metriken wie CPU- und GPU-Zeit aktivieren

#### Microprofiler

Der Microprofiler in X-Plane ist ein leistungsstarkes Diagnosetool, das im Entwicklermenü (Developer Menu) verfügbar ist und detaillierte Einblicke in die Performance der Simulation bietet. Er hilft dabei, Engpässe in der CPU- und GPU-Leistung zu identifizieren, indem er die Zeit aufschlüsselt, die verschiedene Aufgaben während der Frame-Generierung benötigen.

##### Was ist der Microprofiler?

Der Microprofiler ist ein Entwicklerwerkzeug, das die Zeit misst, die verschiedene Teile der X-Plane-Simulation für die Berechnung und das Rendern eines Frames benötigen. Im Gegensatz zur einfachen FPS-Anzeige (Frames per Second), die lediglich die Bildrate und grobe CPU-/GPU-Zeiten anzeigt, bietet der Microprofiler eine detaillierte Aufschlüsselung der einzelnen Prozesse, die zur Erstellung eines Frames beitragen.

Der Microprofiler zeigt:

- Zeitaufwand pro Aufgabe: Wie viel Zeit (in Millisekunden) für bestimmte Aufgaben wie Physikberechnungen, Szenerie-Rendering, Wolken-Darstellung oder Plugin-Verarbeitung benötigt wird
- CPU- und GPU-Auslastung: Welche Komponente (CPU oder GPU) den Frame-Zyklus begrenzt
- Engpässe: Welche spezifischen Prozesse die meiste Zeit in Anspruch nehmen und somit die FPS reduzieren

##### Aktivierung und Nutzung

Um den Microprofiler in X-Plane zu aktivieren, geht man wie folgt vor:

1. Öffnen des Entwicklermenüs:

    - X-Plane starten und eine beliebige Szene laden (z. B. ein Flugzeug auf einer Startbahn)
    - Maus an den oberen Bildschirmrand bewegen, um die Menüleiste anzuzeigen
    - Auf "Developer" klicken (in manchen Versionen kann es "Entwickler" oder ähnlich heißen, je nach Sprache)

2. Aktivieren des Microprofilers:

    - Im Entwicklermenü die Option "Toggle Microprofiler" oder "Show Microprofiler" wählen
    - Eine grafische Anzeige erscheint auf dem Bildschirm, die die Performance-Daten in Echtzeit darstellt

3. Alternative Methode über die Konfigurationsdatei:

    - In X-Plane Professional oder bei modifizierten Installationen kann der Microprofiler über die JSON-Konfigurationsdatei aktiviert werden
    - Den Eintrag "developer::toggle_microprofiler": "visible" setzen, um die Option sichtbar zu machen
    - Dies erfordert Zugriff auf die Konfigurationsdatei und ist für fortgeschrittene Nutzer gedacht

4. Keyboard-Shortcut (optional):

    - Keine standardmäßige Tastenkombination für den Microprofiler in X-Plane
    - Plugins wie "FlyWithLua" können verwendet werden, um eigene Shortcuts zu definieren

##### Angezeigte Daten und Interpretation

Der Microprofiler liefert eine visuelle Darstellung der Frame-Generierungszeit, aufgeteilt in verschiedene Kategorien:

1. Framezeit (Gesamtzeit pro Frame):

    - Definition: Die gesamte Zeit in Millisekunden, die benötigt wird, um einen Frame zu berechnen und zu rendern
    - Formel: Framezeit = 1000 ms / FPS
    - Beispiel: Bei 30 FPS beträgt die Framezeit 1000/30 ≈ 33,3 ms

2. Aufgabenkategorien:

    - Physikberechnungen (Flight Model): Zeit für die Berechnung des Flugverhaltens (z. B. Aerodynamik, Triebwerke)
    - Szenerie-Rendering: Zeit für das Zeichnen von Landschaften, Gebäuden, Straßen
    - Wolken und Wetter: Zeit für die Darstellung von Wolken, Regen oder Nebel
    - Plugins: Zeit, die von installierten Plugins beansprucht wird
    - Swapchain Acquire: Zeit für die Synchronisation zwischen CPU und GPU
    - Andere Aufgaben: KI-Flugzeuge, ATC, Netzwerkkommunikation oder VR-Rendering

3. CPU- und GPU-Zeit:

    - CPU-Zeit: Zeit für Berechnungen auf der CPU (z. B. Physik, Plugins, Szenerie-Logik)
    - GPU-Zeit: Zeit für das Rendern von Grafiken (z. B. Texturen, Schatten, Wolken)
    - Interpretation:
        - Hohe CPU-Zeit: CPU ist der Engpass
        - Hohe GPU-Zeit: GPU ist der Engpass

##### Rechenbeispiel

Angenommen, der Microprofiler zeigt folgende Werte:

- FPS: 30
- Framezeit gesamt: 33,3 ms
- Aufgabenaufteilung:
    - Physikberechnung: 10 ms
    - Szenerie-Rendering: 8 ms
    - Wolken/Wetter: 7 ms
    - Plugins: 5 ms
    - Swapchain Acquire: 3 ms
- CPU-Zeit gesamt: 20 ms
- GPU-Zeit gesamt: 13 ms

Nun lässt sich genauer analysieren, welche Teile (z.B. auch Addons) welche Art von Beitrag an der CPU und GPU Belastung ausmachen.


### Externe Tools

!!! info "Hinweis"
    Diese Dokumentation ist noch nicht vollständig und befindet sich im Aufbau (Work in Progress).

#### System-Monitoring

- **htop**: Detaillierte CPU- und Speichernutzung
- **nvidia-smi**: NVIDIA-spezifische Performance-Metriken
- **glxgears**: Einfaches Tool zur Überprüfung der OpenGL-Performance

#### Overlay-Tools

- **MangoHUD**: Ein Overlay für Linux, das Performance-Metriken anzeigt
- **GOverlay**: Grafische Benutzeroberfläche für MangoHUD
- **vulkaninfo**: Detaillierte Informationen zur Vulkan-Implementierung

#### Benchmarking-Tools

- **Phoronix Test Suite**: Umfassende Benchmarking-Suite
- **Unigine Heaven**: Grafikkarten-Benchmark
- **GLmark2**: OpenGL-Benchmark 

## Praktische Optimierungstipps

Basierend auf der FPS-Darstellung und dem Microprofiler können gezielte Optimierungen vorgenommen werden:

- **CPU-Optimierung**:

    - Reduzierung der Anzahl der Szenerie-Objekte und KI-Flugzeuge
    - Senkung der Physikberechnungen pro Frame („Flight Models per Frame" auf 2–4 setzen)
    - Verwendung weniger komplexer Add-ons
    - Reduzierung der Wolkendetails

- **GPU-Optimierung**:

    - Reduzierung der Texturauflösung („Texture Quality" auf Medium oder High)
    - Deaktivierung oder Reduzierung von Kantenglättung und Schatten
    - Anpassung der Wolkenqualität

- **Allgemein**:

    - Testen in einer einfachen Szenerie, um die Basis-FPS zu ermitteln
    - Verwendung von externen Tools für zusätzliche Metriken
    - Regelmäßige Überprüfung der Performance mit dem Microprofiler
