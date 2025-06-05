# X-Plane Konfiguration

!!! info "Hinweis"
    Diese Dokumentation ist noch nicht vollständig und befindet sich im Aufbau (Work in Progress).

Hier finden Sie wichtige Informationen zur Konfiguration von X-Plane unter Linux.

## Grundlegende Einstellungen

### Grafik-Einstellungen

Die Grafik-Einstellungen umfassen die Wahl zwischen Vulkan und OpenGL mit ihren jeweiligen Vor- und Nachteilen, die Einstellung der Monitor-Auflösung und Bildwiederholrate, die Konfiguration von Anti-Aliasing und Texturqualität, sowie die Anpassung von Schatten und Reflexionen. Zusätzlich gibt es spezielle Grafikoptionen für Nvidia- und AMD-Grafikkarten, die Wetter- und Wolkenqualität beeinflussen.

#### Anti-Aliasing in X-Plane

Aliasing ist ein Phänomen, das durch die diskrete Abtastung eines kontinuierlichen Signals entsteht, wie durch das **Nyquist-Shannon-Theorem** beschrieben. Dieses Theorem besagt, dass die Abtastfrequenz mindestens doppelt so hoch wie die höchste Signal-Frequenz sein muss, um Aliasing-Artefakte zu vermeiden. In der Computergrafik führt eine unzureichende Abtastfrequenz zu Treppeneffekten, insbesondere an Kanten, die nicht mit dem Pixelgitter ausgerichtet sind.

In X-Plane stehen verschiedene Anti-Aliasing-Techniken zur Verfügung. **SSAA (Super Sampling Anti-Aliasing)** erhöht die Auflösung des gerenderten Bildes, beispielsweise von 1920x1080 auf 3840x2160 bei 2x SSAA. Der Speicher- und Rechenaufwand wächst dabei quadratisch, weshalb diese Technik in neueren Versionen von X-Plane nicht mehr verwendet wird.

**FXAA (Fast Approximate Anti-Aliasing)** ist eine Post-Processing-Technik zur Kantenglättung. Sie ist rechenleistungsschonend und benötigt keinen zusätzlichen Speicher, kann aber zu unscharfen Instrumenten führen, besonders bei 1080p. Bei 4K-Auflösungen zeigt FXAA bessere Ergebnisse.

**MSAA (Multi-Sample Anti-Aliasing)** ist eine hardware-implementierte Technik mit Abdeckungsmaske pro Pixel. Sie ist besonders effektiv an geometrischen Kanten, hat aber Schwierigkeiten mit transparenten Geometrien. In X-Plane 12.1 wurden diese Probleme durch Alpha-to-Coverage und Alpha-to-One verbessert.

X-Plane nutzt Deferred Rendering, bei dem Metadaten in einem G-Buffer gespeichert werden. Dies reduziert Overdraw, erhöht jedoch die Komplexität bei MSAA, da Beleuchtungsschritte pro Sample ausgeführt werden müssen. Die Renderpipeline umfasst zahlreiche Zwischenschritte, die die Komplexität weiter erhöhen.

Nicht alle Aliasing-Artefakte sind auf MSAA-Mängel zurückzuführen. Post-Processing-Effekte wie Screen-Space Reflections (SSR) können Artefakte verursachen, etwa durch ungenaue Reflexionen (z.B. Himmel auf Objekten). Diese Artefakte sind nicht geometrischer Natur und können daher von MSAA nicht behoben werden. FXAA kann solche Kanten glätten, entfernt jedoch nicht die zugrunde liegende fehlerhafte Information.


#### Innenraumbeleuchtung und PBR

Die Beleuchtung in X-Plane basiert auf **Physically Based Rendering (PBR)**, was zu realistischen, aber auch komplexen Lichteffekten führt. Besonders in Innenräumen wie dem Cockpit kann dies zu unerwarteten Beleuchtungseffekten führen. X-Plane ist grundsätzlich in der Lage, zwischen Innen- und Außenbereichen zu unterscheiden. Dies wird besonders deutlich beim Wechsel in die freie Kamera (Taste "C"), da sich die Innenraumbeleuchtung entsprechend anpasst. Dennoch können externe Lichtquellen wie Himmelslicht oder atmosphärische Effekte (z.B. Sonnenuntergang) die Innenraumbeleuchtung beeinflussen.

Die PBR-Implementierung in X-Plane simuliert realistische Lichtreflexionen und -absorptionen. Materialien werden durch ihre Umgebung beeinflusst - ein Cockpit in einem pinkfarbenen Hangar würde eine entsprechende Tönung annehmen. Wetterbedingungen wie ein orangefarbener Sonnenuntergang wirken sich auf die Cockpitbeleuchtung aus, und jedes Material reagiert unterschiedlich auf Licht, basierend auf seinen physikalischen Eigenschaften.

Die aktuelle Renderpipeline von X-Plane hat einige technische Einschränkungen. Jeder Pixel wird unabhängig und parallel berechnet, ohne Kontext über die umgebende Geometrie. Die Erkennung von Abschirmungen, zum Beispiel wenn ein Cockpit den Himmel nicht "sehen" sollte, ist rechentechnisch aufwendig. Besonders bei schmalen Geometrien wie Cockpitkanten oder Flügelkurven können ungewollt Licht von der Umgebung aufgenommen werden.

Screen-Space Reflections (SSR) können zu sichtbaren Artefakten führen. Schimmernde Reflexionen, wie bei nassem Asphalt, können durch fehlende Denoising-Techniken entstehen. Die fehlende Strahlkohärenz (Ray Coherency) kann zu ungleichmäßigen Reflexionen führen. Eine vollständige Lösung dieser Probleme würde erhebliche Rechenleistung erfordern und die Bildrate drastisch reduzieren.

Die Optimierung der Innenraumbeleuchtung und die Reduzierung von Beleuchtungsartefakten haben eine hohe Priorität in der Entwicklung von X-Plane. Diese Probleme gehören zu den häufigsten Beschwerden, die potenzielle Nutzer von X-Plane 12 abschrecken. Die Komplexität der Implementierung erfordert jedoch sorgfältige Abwägungen zwischen visueller Qualität und Performance.

#### Treiberbasierte MSAA

MSAA kann auch über den Grafiktreiber erzwungen werden. Dies führt zu einer schnelleren Ausführung, aber auch zu ungenauerer Beschattung, da die komplexe X-Plane Renderpipeline nicht berücksichtigt wird. Die Treiberimplementierung kann die spezifischen Anforderungen der X-Plane Renderpipeline nicht vollständig berücksichtigen.

#### Optimierungsempfehlungen

Für optimale Bildqualität empfehlen wir folgende Schritte: Zunächst sollte FSR deaktiviert werden (Regler auf Maximum). Anschließend kann Multisampling (MSAA) schrittweise erhöht werden, wobei nach jeder Anpassung Performance und Bildqualität zu prüfen sind. Bei Bedarf können weitere Stufen hinzugefügt werden. FXAA kann optional aktiviert werden, wobei die Auswirkung auf die Bildschärfe zu berücksichtigen ist.

Falls diese Maßnahmen nicht zu einer zufriedenstellenden Bildqualität führen, sollte die Verwendung eines Monitors mit höherer Auflösung in Betracht gezogen werden. Eine höhere native Auflösung reduziert das Kantenflimmern signifikant, erfordert jedoch eine entsprechend leistungsfähige Grafikkarte.

#### Fazit und Ausblick

Aliasing ist ein komplexes Problem, das durch physikalische Grenzen (Nyquist-Shannon-Theorem) und die Komplexität moderner Renderpipelines erschwert wird. Eine Lösung erfordert Verbesserungen in der Renderpipeline, etwa durch optimierte SSR-Implementierungen. In X-Plane wird kontinuierlich an Optimierungen gearbeitet.

### Audio-Einstellungen

Die Audio-Konfiguration umfasst die Auswahl der Audio-Engine zwischen OpenAL und FMOD, die präzise Lautstärkeregelung für verschiedene Soundquellen, die Konfiguration von 3D-Audio-Einstellungen, die Einrichtung externer Soundkarten und die Optimierung der Mikrofon-Einstellungen für den Online-Flug.

### Steuerung

Die Steuerungskonfiguration beinhaltet die präzise Kalibrierung von Joystick und Gamepad, die Anpassung der Tastaturbelegung, die Konfiguration der Ruderpedale, das Einrichten eines Multi-Monitor-Setups und die Feinabstimmung der VR-Controller-Einstellungen.

## Performance-Optimierung

### Rendering-Optionen

Die Rendering-Optionen umfassen die detaillierte Einstellung von Objektdichte und Sichtweite, die Konfiguration von Autogen-Gebäuden und Vegetation, die Anpassung von Wasser- und Wolkeneffekten, die Steuerung der Flugzeug- und Verkehrsdichte sowie die Einstellung der Wetterkomplexität.

### Speicherverwaltung

Die Speicherverwaltung beinhaltet die Optimierung der VRAM-Nutzung, die Konfiguration der RAM-Auslagerung, die Anpassung der Cache-Einstellungen, das Management von Ortho4XP-Tiles und die Implementierung effizienter Szenerie-Ladestrategien. 