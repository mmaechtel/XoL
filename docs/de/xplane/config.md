# X-Plane Konfiguration

!!! info "Hinweis"
    Diese Dokumentation ist noch nicht vollständig und befindet sich im Aufbau (Work in Progress).

Hier finden Sie wichtige Informationen zur Konfiguration von X-Plane unter Linux.

## Grundlegende Einstellungen

### Grafik-Einstellungen
* Vulkan vs. OpenGL: Vor- und Nachteile
* Monitor-Auflösung und Bildwiederholrate
* Anti-Aliasing und Texturqualität
* Schatten und Reflexionen
* Wetter- und Wolkenqualität
* Zusätzliche Grafikoptionen für Nvidia/AMD

#### Hinweise zur Bildqualität
Kantenflimmern (Aliasing) kann durch Anpassung des MSAA-Reglers im Grafikmenü reduziert werden. Eine höhere MSAA-Einstellung führt zu einer deutlichen Verringerung des Flimmerns, geht jedoch mit einem erhöhten GPU-Leistungsbedarf einher. 

Die Nutzung von AMD FSR verstärkt das Kantenflimmern signifikant. Es wird daher empfohlen, zunächst FSR zu deaktivieren und in der nativen Auflösung zu rendern, bevor MSAA aktiviert wird. 

Die Aktivierung von FXAA (eine einfache Option in den Grafikeinstellungen) hat einen minimalen Effekt auf das Kantenflimmern. Diese Option ist leistungsneutral, führt jedoch zu einer leichten Bildunschärfe.

##### Optimierungsempfehlungen:
1. FSR deaktivieren (Regler auf Maximum)
2. Multisampling (MSAA) schrittweise erhöhen
   - Nach jeder Anpassung Performance und Bildqualität prüfen
   - Bei Bedarf weitere Stufen hinzufügen
3. FXAA optional aktivieren
   - Auswirkung auf Bildschärfe berücksichtigen

Falls diese Maßnahmen nicht zu einer zufriedenstellenden Bildqualität führen, sollte die Verwendung eines Monitors mit höherer Auflösung in Betracht gezogen werden. Eine höhere native Auflösung reduziert das Kantenflimmern signifikant, erfordert jedoch eine entsprechend leistungsfähige Grafikkarte.

### Audio-Einstellungen
* Audio-Engine (OpenAL vs. FMOD)
* Lautstärkeregelung für verschiedene Soundquellen
* 3D-Audio-Einstellungen
* Externe Soundkarten-Konfiguration
* Mikrofon-Einstellungen für Online-Flug

### Steuerung
* Joystick/Gamepad-Kalibrierung
* Tastaturbelegung
* Ruderpedale-Konfiguration
* Multi-Monitor-Setup
* VR-Controller-Einstellungen

## Performance-Optimierung

### Rendering-Optionen
* Objektdichte und Sichtweite
* Autogen-Gebäude und Vegetation
* Wasser- und Wolkeneffekte
* Flugzeug- und Verkehrsdichte
* Wetterkomplexität

### Speicherverwaltung
* VRAM-Nutzung optimieren
* RAM-Auslagerung konfigurieren
* Cache-Einstellungen
* Ortho4XP-Tile-Management
* Szenerie-Ladestrategien 