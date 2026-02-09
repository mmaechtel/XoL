---
title: Glossar
description: Begriffserklärungen rund um X-Plane und Linux
tags:
  - reference
---

# Glossar

## A
### Airport Enhancement Package (AEP)
Ein Szenerie-Addon von X-Codr Designs für X-Plane, das Standard-Flughäfen durch detailliertere Modelle, höher aufgelöste Texturen und neue Technologien verbessert. Es ersetzt Flughafengebäude, Fassaden, Bodenobjekte, statische Fahrzeuge sowie Landebahnlichter, Baken und Navigationshilfen durch modernere Versionen. [Mehr Details](../addon/aep.md)

### AutoOrtho
Ein Tool für X-Plane, das Orthofotos direkt in den Flugsimulator integriert. Es ermöglicht das Streaming von hochauflösenden Luftbildern als Bodenstruktur, ohne dass diese vorher heruntergeladen und konvertiert werden müssen. Die Software kann entweder als vorgefertigte Binary oder aus dem Quellcode installiert werden.

## B
### Bodenmarkierungen
Die Markierungen und Beläge auf Flughäfen in X-Plane. Im [Airport Enhancement Package (AEP)](../addon/aep.md) werden diese durch neue, hochauflösende Texturen ersetzt, die X-Plane 12's Wettereffekte unterstützen und realistische Muster ohne Wiederholungen erzeugen.

### Binary
Eine vorkompilierte, ausführbare Datei eines Programms. Im Gegensatz zur Installation aus dem Quellcode kann eine Binary direkt ausgeführt werden, ohne dass weitere Kompilierungsschritte notwendig sind.

### Blade Element Theory
Eine Berechnungsmethode in der Aerodynamik, bei der ein Flugzeug in viele kleine Segmente zerlegt wird, um die Luftströmung und Kräfte in Echtzeit zu simulieren.

## C
### Compositor
Ein Programm, das die Inhalte mehrerer Fenster zum endgültigen Bildschirmbild zusammensetzt. Unter Wayland übernimmt der Compositor gleichzeitig die Rolle von Display-Server und Fenstermanager (z.B. Mutter bei GNOME, KWin bei KDE). Unter X11 ist der Compositor ein separates Programm, das von Fullscreen-Anwendungen umgangen werden kann.

### Custom Scenery
Ein Verzeichnis in X-Plane, in dem zusätzliche Szenerie-Dateien gespeichert werden. Hier werden auch die von AutoOrtho generierten Ortho-Texturen eingebunden.

## D
### Display-Server
Software, die Grafikausgabe und Eingabegeräte für Anwendungen verwaltet. X11 (Xorg) und Wayland sind die beiden Display-Server-Protokolle unter Linux. X-Plane 12 unterstützt nur X11. Siehe [Display-Server](../displayserver.md).

### Docker
Eine Plattform zur Containerisierung von Anwendungen, die es ermöglicht, Software in standardisierten Einheiten (Containern) zu verpacken und auszuführen. Docker vereinfacht die Bereitstellung und Verwaltung von Anwendungen in unterschiedlichen Umgebungen.

### DKMS (Dynamic Kernel Module Support)
Ein Framework, das die automatische Neukompilierung von Kernel-Modulen bei Kernel-Updates ermöglicht. Besonders wichtig für Treiber wie Nvidia, die nicht im Standard-Kernel enthalten sind.

### Dynamische Bibliotheken
Auch als Shared Libraries bezeichnet, sind wiederverwendbare Programmcode-Sammlungen, die zur Laufzeit von verschiedenen Programmen geladen und gemeinsam genutzt werden können. Sie haben typischerweise die Endung .so (shared object) unter Linux und ermöglichen effizientere Speichernutzung und einfachere Updates.

## E
### evdev
Event Device — die Linux-Eingabeschnittstelle im Kernel, die Eingabegeräte über `/dev/input/event*` bereitstellt. X-Plane nutzt SDL2 mit evdev-Backend zur Controller-Erkennung. Nicht zu verwechseln mit dem älteren Joystick-Interface (`/dev/input/js*`).

## F
### FAA
Federal Aviation Administration - die US-amerikanische Luftfahrtbehörde, die Standards für Flugsimulationen und Trainingsgeräte festlegt.

### FMOD
Eine proprietäre Audio-Engine von Firelight Technologies. X-Plane 12 verwendet FMOD Studio 2.02 für die gesamte Audioausgabe. Unter Linux kommuniziert FMOD mit PulseAudio oder PipeWire.

### Flughafenelemente
Die verschiedenen Komponenten eines Flughafens in X-Plane, wie Gebäude, Fassaden, Bodenobjekte, statische Fahrzeuge, Landebahnlichter, Baken und Navigationshilfen. Das [Airport Enhancement Package (AEP)](../addon/aep.md) verbessert diese Elemente durch detailliertere Modelle und höher aufgelöste Texturen.

### Flughafenvegetation
Die 3D-Vegetationselemente auf Flughäfen in X-Plane. Im [Airport Enhancement Package (AEP)](../addon/aep.md) wird die Standard-Flughafenvegetation durch neue, detailliertere 3D-Modelle ersetzt, die für eine realistischere Darstellung sorgen.

### GUI (Graphical User Interface)
Eine grafische Benutzeroberfläche, die die Interaktion mit einem Programm durch grafische Elemente wie Fenster, Buttons und Menüs ermöglicht. Bei AutoOrtho dient die GUI zur Konfiguration des X-Plane-Verzeichnisses und zum Laden von Ortho-Sets.

## H
### HDR
High Dynamic Range - ein Grafikverfahren, das einen besonders großen Helligkeitsbereich darstellen kann, was zu realistischeren Lichteffekten führt.

## K
### KVM (Kernel-based Virtual Machine)
Eine in den Linux-Kernel integrierte Virtualisierungslösung, die es ermöglicht, virtuelle Maschinen mit nahezu nativer Leistung auszuführen. KVM nutzt Hardware-Virtualisierungsfunktionen moderner Prozessoren für effiziente Virtualisierung.

## L
### ldd
Ein Kommandozeilenprogramm unter Linux, das alle dynamischen Bibliotheksabhängigkeiten einer ausführbaren Datei anzeigt. Es ist ein wichtiges Diagnosewerkzeug, um fehlende oder inkompatible Bibliotheken zu identifizieren, die für die Ausführung eines Programms wie X-Plane erforderlich sind.

### Linux
Ein freies, quelloffenes Betriebssystem, das sich besonders durch seine Stabilität, Sicherheit und Anpassungsfähigkeit auszeichnet.

### Liquorix-Kernel
Eine optimierte Version des Linux-Kernels, die auf Performance ausgerichtet ist. Bietet oft bessere Reaktionszeiten und Leistung für Desktop-Systeme und Gaming.

## N
### Nouveau
Der Standard-Open-Source-Treiber für Nvidia-Grafikkarten in Linux. Wird oft deaktiviert, wenn der proprietäre Nvidia-Treiber installiert wird.

### Nvidia-Treiber
Proprietäre Treibersoftware von Nvidia für ihre Grafikkarten. Bietet im Vergleich zum Open-Source-Treiber Nouveau oft bessere Performance und mehr Funktionen, besonders für 3D-Anwendungen und Gaming.

## O
### Ortho4XP
Ein Tool zur Erstellung von fotorealistischen Landschaftstexturen für X-Plane aus verschiedenen Satellitenbildquellen.

### Orthofotos
Orthofotos (oder Orthophotos) sind maßstabsgetreue, verzerrungsfreie Luftbilder der Erdoberfläche. Sie werden in X-Plane als hochauflösende Bodentexturen verwendet, um eine realistische Darstellung der Landschaft zu erreichen.

## P
### PBR
Physically Based Rendering - ein Grafikverfahren, das physikalische Eigenschaften von Materialien und Licht simuliert, um realistische Darstellungen zu erzeugen.

### Plugin
Eine Softwareerweiterung, die zusätzliche Funktionen zu X-Plane hinzufügt. Plugins können von Drittanbietern entwickelt werden.

### pyenv
Ein Werkzeug zur Verwaltung verschiedener Python-Versionen auf einem System. Es ermöglicht die Installation und Nutzung mehrerer Python-Versionen nebeneinander, ohne das System-Python zu beeinflussen.

## R
### RADV
Der Open-Source-Vulkan-Treiber für AMD-GPUs innerhalb des Mesa-Treiberstacks. RADV ist der Standard-Vulkan-Treiber auf Linux-Systemen mit AMD-Grafikkarten und wird von X-Plane 12 direkt genutzt.

## S
### scenery_packs.ini
Eine Konfigurationsdatei im Custom Scenery-Ordner von X-Plane, die die Ladereihenfolge der installierten Szenerien festlegt. AutoOrtho fügt hier automatisch Einträge mit dem Präfix `z_ao_` hinzu.

### Single-CPU
Beschreibt die aktuelle Architektur von X-Plane, bei der die Hauptsimulation auf einem einzelnen Prozessorkern läuft.

## V
### Vulkan API
Eine moderne, plattformübergreifende Grafikschnittstelle mit geringem Overhead, die von X-Plane für die Grafikdarstellung verwendet wird. Im Vergleich zu OpenGL bietet Vulkan oft bessere Performance durch effizientere CPU-Nutzung und direktere GPU-Kontrolle.

## W
### Wayland
Ein modernes Display-Server-Protokoll für Linux, Nachfolger von X11. Der Compositor übernimmt sowohl Display-Server- als auch Fenstermanager-Aufgaben. Wayland bietet bessere Sicherheit und unabhängige Monitor-Refresh-Rates, aber X-Plane 12 kann kein natives Wayland und nutzt stattdessen XWayland. Siehe [Display-Server](../displayserver.md).

### Wine (Wine Is Not an Emulator)
Ein Kompatibilitätslayer, der es ermöglicht, Windows-Programme unter Linux auszuführen. Wine übersetzt Windows-API-Aufrufe in POSIX-Aufrufe, ohne Windows selbst zu emulieren.

## X
### X11 (Xorg)
Das klassische Display-Server-Protokoll für Linux, im Einsatz seit 1984. Ein zentraler X-Server verwaltet alle Grafik- und Eingabeoperationen. X-Plane spricht X11 nativ. Siehe [Display-Server](../displayserver.md).

### X-Plane
Ein hochrealistischer Flugsimulator, der für verschiedene Plattformen (Windows, macOS, Linux) verfügbar ist.

### XWayland
Eine Kompatibilitätsschicht, die einen vollständigen X11-Server innerhalb einer Wayland-Session betreibt. Wenn eine X11-Anwendung (wie X-Plane) auf einem Wayland-Desktop startet, übernimmt XWayland automatisch die Übersetzung. Der zusätzliche Übersetzungsschritt kostet Latenz. Siehe [Wayland-Session](../displayserver_wayland.md).

### Xroads
Eine Bibliothek für X-Plane 11 & 12, die die Darstellung von Straßen in Ortho4XP-Szenerien optimiert.

## Z
### Zink
Eine OpenGL-Übersetzungsschicht innerhalb von Mesa, die OpenGL-Befehle in Vulkan-Befehle übersetzt. X-Plane 12 liefert einen eigenen Zink-Treiber mit, damit Plugins, die OpenGL für ihre Darstellung nutzen, innerhalb der Vulkan-Renderpipeline funktionieren.

## 3
### 32-Bit-Kompatibilität
Die Fähigkeit eines 64-Bit-Linux-Systems, 32-Bit-Anwendungen und -Bibliotheken auszuführen und zu unterstützen. Für manche Programme oder Plugins, die noch nicht für 64-Bit-Architekturen optimiert wurden, kann dies erforderlich sein. Unter Debian wird die 32-Bit-Unterstützung durch Hinzufügen der i386-Architektur und Installation entsprechender Bibliotheken aktiviert. 