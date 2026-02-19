---
title: Glossar
description: "Glossar zu X-Plane- und Linux-Begriffen — CPU-Governor, Vulkan, VRAM, Wayland, Mesa, Kernel-Parameter, Szenerie-Formate und mehr erklärt."
tags:
  - reference
---
# Glossar

## A

### Airport Enhancement Package (AEP)

Ein Szenerie-Addon von X-Codr Designs für X-Plane, das Standard-Flughäfen durch detailliertere Modelle, höher aufgelöste Texturen und neue Technologien verbessert. Es ersetzt Flughafengebäude, Fassaden, Bodenobjekte, statische Fahrzeuge sowie Landebahnlichter, Baken und Navigationshilfen durch modernere Versionen. [Mehr Details](addon/scenery_addons/aep.md)

### ALSA (Advanced Linux Sound Architecture)

Das Standard-Audio-Subsystem im Linux-Kernel, das die Schnittstelle zwischen Audio-Hardware und Anwendungen bildet. ALSA stellt die Gerätetreiber bereit, auf denen höhere Audio-Schichten wie PulseAudio oder PipeWire aufbauen. X-Plane nutzt ALSA nicht direkt, sondern kommuniziert über FMOD mit PulseAudio/PipeWire.

### APST (Autonomous Power State Transitions)

Ein NVMe-Energiespar-Feature, das SSDs automatisch in stromsparende Zustände versetzt. Kann zu Mikro-Rucklern führen, wenn die SSD für das Laden von Szenerie-Daten aus dem Tiefschlaf aufgeweckt werden muss. Für X-Plane empfiehlt sich die Deaktivierung über den Kernel-Parameter `nvme_core.default_ps_max_latency_us=0`.

### ANV

Der Open-Source-Vulkan-Treiber für Intel-GPUs innerhalb des Mesa-Treiberstacks. ANV ist der Standard-Vulkan-Treiber auf Linux-Systemen mit Intel-Arc- und integrierten Intel-Grafikkarten und wird von X-Plane 12 direkt genutzt.

### Autogen

Automatisch generierte 3D-Objekte (Gebäude, Vegetation) in X-Plane, die auf Basis von Landnutzungsdaten platziert werden. Autogen füllt die Landschaft abseits handmodellierter Flughäfen und Städte. Die Darstellungsdichte wird in den X-Plane-Grafikeinstellungen über „Objects" gesteuert.

### AutoOrtho

Ein Tool für X-Plane, das Orthofotos direkt in den Flugsimulator integriert. Es ermöglicht das Streaming von hochauflösenden Luftbildern als Bodenstruktur, ohne dass diese vorher heruntergeladen und konvertiert werden müssen. Die Software kann entweder als vorgefertigte Binary oder aus dem Quellcode installiert werden.

## B

### Binary

Eine vorkompilierte, ausführbare Datei eines Programms. Im Gegensatz zur Installation aus dem Quellcode kann eine Binary direkt ausgeführt werden, ohne dass weitere Kompilierungsschritte notwendig sind.

### Blade Element Theory

Eine Berechnungsmethode in der Aerodynamik, bei der ein Flugzeug in viele kleine Segmente zerlegt wird, um die Luftströmung und Kräfte in Echtzeit zu simulieren.

### Bodenmarkierungen

Die Markierungen und Beläge auf Flughäfen in X-Plane. Im [Airport Enhancement Package (AEP)](addon/scenery_addons/aep.md) werden diese durch neue, hochauflösende Texturen ersetzt, die X-Plane 12's Wettereffekte unterstützen und realistische Muster ohne Wiederholungen erzeugen.

### BORE (Burst-Oriented Response Enhancer)

Ein CPU-Scheduler, der im Liquorix-Kernel den Standard-Scheduler EEVDF ersetzt. BORE optimiert die Reaktionszeit für interaktive Anwendungen, indem er CPU-intensive Burst-Phasen bevorzugt behandelt. Relevant für X-Plane, da der Simulator in unregelmäßigen Bursts hohe CPU-Last erzeugt. Siehe [Liquorix](linux/optimizations/liquorix.md).

### Btrfs (B-tree Filesystem)

Ein Copy-on-Write-Dateisystem für Linux mit Funktionen wie Snapshots, transparenter Kompression und Prüfsummen. Bietet gegenüber Ext4 mehr Funktionalität, kann bei fragmentierungsempfindlichen Workloads wie dem Laden großer Szenerie-Dateien aber langsamer sein.

## C

### Compositor

Ein Programm, das die Inhalte mehrerer Fenster zum endgültigen Bildschirmbild zusammensetzt. Unter Wayland übernimmt der Compositor gleichzeitig die Rolle von Display-Server und Fenstermanager (z.B. Mutter bei GNOME, KWin bei KDE). Unter X11 ist der Compositor ein separates Programm, das von Fullscreen-Anwendungen umgangen werden kann.

### CPU-Affinität

Die Zuordnung von Prozessen oder Threads zu bestimmten CPU-Kernen. Durch CPU-Affinität kann der X-Plane-Hauptthread auf einem dedizierten Kern laufen, während Hintergrundprozesse und Interrupts auf andere Kerne verlagert werden. Konfiguration über `taskset` oder den Kernel-Parameter `isolcpus`. Siehe [Systemtuning](linux/system/systemtuning.md).

### CPU Governor

Die Strategie des Kernels zur dynamischen Anpassung der CPU-Taktfrequenz. `performance` hält die maximale Frequenz dauerhaft, `ondemand` passt sie nach Bedarf an. Für X-Plane wird `performance` empfohlen, um Latenz durch Frequenzwechsel zu vermeiden. Siehe [Systemtuning](linux/system/systemtuning.md).

### C-States (CPU Idle States)

Energiesparzustände moderner CPUs. Höhere C-States (C3, C6) sparen mehr Strom, benötigen aber mehr Zeit zum Aufwachen. Für X-Plane können tiefe C-States zu Latenzspitzen führen. Einschränkung über den Kernel-Parameter `processor.max_cstate` oder BIOS-Einstellungen. Siehe [Systemtuning](linux/system/systemtuning.md).

### Custom Scenery

Ein Verzeichnis in X-Plane, in dem zusätzliche Szenerie-Dateien gespeichert werden. Hier werden auch die von AutoOrtho generierten Ortho-Texturen eingebunden.

## D

### DDS (DirectDraw Surface)

Ein Texturformat von Microsoft, das in X-Plane für Szenerie- und Orthofoto-Texturen verwendet wird. DDS-Dateien enthalten GPU-komprimierte Bilddaten (oft im DXT/BC-Format), die ohne Dekompression direkt in den VRAM geladen werden können. Ortho4XP erzeugt DDS-Dateien aus heruntergeladenen Satellitenbildern.

### Display-Server

Software, die Grafikausgabe und Eingabegeräte für Anwendungen verwaltet. X11 (Xorg) und Wayland sind die beiden Display-Server-Protokolle unter Linux. X-Plane 12 unterstützt nur X11. Siehe [Display-Server](linux/optimizations/displayserver.md).

### Docker

Eine Plattform zur Containerisierung von Anwendungen, die es ermöglicht, Software in standardisierten Einheiten (Containern) zu verpacken und auszuführen. Docker vereinfacht die Bereitstellung und Verwaltung von Anwendungen in unterschiedlichen Umgebungen.

### DKMS (Dynamic Kernel Module Support)

Ein Framework, das die automatische Neukompilierung von Kernel-Modulen bei Kernel-Updates ermöglicht. Besonders wichtig für Treiber wie Nvidia, die nicht im Standard-Kernel enthalten sind.

### DRM/KMS (Direct Rendering Manager / Kernel Mode Setting)

Das Grafik-Subsystem im Linux-Kernel, das GPU-Zugriff und Bildschirmausgabe verwaltet. DRM stellt die Schnittstelle zwischen Userspace-Treibern (Mesa, Nvidia) und der GPU-Hardware her. KMS übernimmt die Bildschirmauflösung und den Modewechsel direkt im Kernel, was flimmerfreies Booten und schnelles VT-Switching ermöglicht.

### DSF (Distribution Scenery Format)

X-Planes natives Dateiformat für Szenerie-Kacheln. Jede DSF-Datei beschreibt eine ein-Grad-mal-ein-Grad-Kachel der Erdoberfläche und enthält Geländemesh, Landnutzungsdaten, Objektplatzierungen und Straßennetze. Orthofotos und Meshes von Drittanbietern ersetzen einzelne Schichten innerhalb dieses Formats.

### Dynamische Bibliotheken

Auch als Shared Libraries bezeichnet, sind wiederverwendbare Programmcode-Sammlungen, die zur Laufzeit von verschiedenen Programmen geladen und gemeinsam genutzt werden können. Sie haben typischerweise die Endung .so (shared object) unter Linux und ermöglichen effizientere Speichernutzung und einfachere Updates.

## E

### EEVDF (Earliest Eligible Virtual Deadline First)

Der Standard-CPU-Scheduler im Linux-Kernel seit Version 6.6, Nachfolger des CFS (Completely Fair Scheduler). EEVDF priorisiert Aufgaben basierend auf virtuellen Deadlines und kann die Latenz interaktiver Anwendungen verbessern. Der Liquorix-Kernel verwendet stattdessen den BORE-Scheduler.

### evdev

Event Device — die Linux-Eingabeschnittstelle im Kernel, die Eingabegeräte über `/dev/input/event*` bereitstellt. X-Plane nutzt SDL2 mit evdev-Backend zur Controller-Erkennung. Nicht zu verwechseln mit dem älteren Joystick-Interface (`/dev/input/js*`).

### Ext4 (Fourth Extended Filesystem)

Das Standard-Dateisystem der meisten Linux-Distributionen. Ext4 ist ausgereift, stabil und bietet gute Performance bei sequentiellen und zufälligen Zugriffen. Für X-Plane empfohlen, da die vorhersagbare I/O-Leistung beim Laden von Szenerien vorteilhaft ist. Siehe [Dateisystem](linux/optimizations/filesystem.md).

## F

### FAA

Federal Aviation Administration - die US-amerikanische Luftfahrtbehörde, die Standards für Flugsimulationen und Trainingsgeräte festlegt.

### Flughafenelemente

Die verschiedenen Komponenten eines Flughafens in X-Plane, wie Gebäude, Fassaden, Bodenobjekte, statische Fahrzeuge, Landebahnlichter, Baken und Navigationshilfen. Das [Airport Enhancement Package (AEP)](addon/scenery_addons/aep.md) verbessert diese Elemente durch detailliertere Modelle und höher aufgelöste Texturen.

### Flughafenvegetation

Die 3D-Vegetationselemente auf Flughäfen in X-Plane. Im [Airport Enhancement Package (AEP)](addon/scenery_addons/aep.md) wird die Standard-Flughafenvegetation durch neue, detailliertere 3D-Modelle ersetzt, die für eine realistischere Darstellung sorgen.

### FMOD

Eine proprietäre Audio-Engine von Firelight Technologies. X-Plane 12 verwendet FMOD Studio 2.02 für die gesamte Audioausgabe. Unter Linux kommuniziert FMOD mit PulseAudio oder PipeWire.

### FPS (Frames per Second)

Die Anzahl der Bilder, die der Simulator pro Sekunde berechnet und darstellt. Höhere FPS bedeuten flüssigere Darstellung, wobei gleichmäßige Frame Times wichtiger sind als der reine FPS-Wert. X-Plane zeigt die aktuelle FPS über die integrierte Leistungsanzeige. Siehe [Performance](xplane/setup_diagnose/performance.md).

### Frame Time

Die Zeit in Millisekunden, die der Simulator für die Berechnung und Darstellung eines einzelnen Bildes benötigt. Gleichmäßige Frame Times sind für ein flüssiges Simulationserlebnis wichtiger als eine hohe Framerate. Schwankungen (Frame-Time-Spikes) äußern sich als Ruckler. Siehe [Performance](xplane/setup_diagnose/performance.md).

### FUSE (Filesystem in Userspace)

Eine Schnittstelle, die es erlaubt, Dateisysteme im Benutzerraum statt im Kernel zu implementieren. AutoOrtho nutzt FUSE, um gestreamte Orthofotos als virtuelles Dateisystem bereitzustellen, das X-Plane wie ein normales Szenerie-Verzeichnis liest.

## G

### Global Airports

Der Eintrag `*GLOBAL_AIRPORTS*` in X-Planes scenery_packs.ini, der die Standard-Flughäfen enthält — viele davon von der Community über das X-Plane Gateway beigesteuert. In der Ladereihenfolge sollte Global Airports unterhalb von Custom-Airport-Szenerien, aber über Autogen, Orthofotos und Mesh-Schichten stehen. Eine falsche Position kann zu schwebenden Flughäfen oder verdeckten Rollwegen führen. Siehe [Szenerien-Komponenten](scenery/aufbau_quellen/scenery_components.md).

### GRUB (Grand Unified Bootloader)

Der Standard-Bootloader der meisten Linux-Distributionen. Kernel-Parameter für Performance-Optimierungen (C-States, NVMe-Einstellungen, CPU-Isolation) werden in der GRUB-Konfiguration unter `/etc/default/grub` im Parameter `GRUB_CMDLINE_LINUX_DEFAULT` eingetragen. Siehe [Systemtuning](linux/system/systemtuning.md).

### GUI (Graphical User Interface)

Eine grafische Benutzeroberfläche, die die Interaktion mit einem Programm durch grafische Elemente wie Fenster, Buttons und Menüs ermöglicht. Bei AutoOrtho dient die GUI zur Konfiguration des X-Plane-Verzeichnisses und zum Laden von Ortho-Sets.

## H

### HDR

High Dynamic Range - ein Grafikverfahren, das einen besonders großen Helligkeitsbereich darstellen kann, was zu realistischeren Lichteffekten führt.

## I

### I/O-Scheduler

Der Algorithmus im Kernel, der die Reihenfolge von Lese- und Schreibzugriffen auf Datenträger optimiert. Für NVMe-SSDs wird `none` (No-Op) empfohlen, da die SSD-interne Verwaltung effizienter ist als eine Software-Umordnung. Für SATA-SSDs ist `mq-deadline` eine gute Wahl. Siehe [Dateisystem](linux/optimizations/filesystem.md).

### IRQ (Interrupt Request)

Ein Signal, mit dem Hardware-Geräte (GPU, NVMe-SSD, USB-Controller) den Prozessor auffordern, Daten zu verarbeiten. Durch gezieltes IRQ-Pinning können Interrupts auf bestimmte CPU-Kerne gelegt werden, um den X-Plane-Hauptthread nicht zu stören. Siehe [Systemtuning](linux/system/systemtuning.md).

### irqbalance

Ein Userspace-Daemon, der Hardware-Interrupts auf CPU-Kerne verteilt. irqbalance passt sich automatisch an neue Geräte an und berücksichtigt Kernel-Einschränkungen für verwaltete Interrupts (MSI-X). Über die Einstellung `IRQBALANCE_BANNED_CPULIST` in `/etc/default/irqbalance` lassen sich bestimmte Kerne von der Interrupt-Verteilung ausschließen, um sie für die Anwendung freizuhalten. Siehe [Systemtuning](linux/system/systemtuning.md).

## K

### Kernel-Modul

Ein Stück Code, das zur Laufzeit in den Linux-Kernel geladen werden kann, ohne das System neu zu starten. Nvidia-Treiber, Dateisystem-Treiber und Hardware-Unterstützung werden typischerweise als Kernel-Module bereitgestellt. DKMS sorgt dafür, dass Module bei Kernel-Updates automatisch neu kompiliert werden.

### Kernel-Parameter

Konfigurationswerte, die beim Systemstart über den Bootloader (GRUB) an den Kernel übergeben werden. Für X-Plane relevante Parameter umfassen `processor.max_cstate` (C-States), `nvme_core.default_ps_max_latency_us` (NVMe-Energiesparen) und `isolcpus` (CPU-Isolation). Konfiguration in `/etc/default/grub`. Siehe [Systemtuning](linux/system/systemtuning.md).

### KVM (Kernel-based Virtual Machine)

Eine in den Linux-Kernel integrierte Virtualisierungslösung, die es ermöglicht, virtuelle Maschinen mit nahezu nativer Leistung auszuführen. KVM nutzt Hardware-Virtualisierungsfunktionen moderner Prozessoren für effiziente Virtualisierung.

## L

### Latenz

Die Verzögerung zwischen einer Aktion und ihrer sichtbaren Auswirkung. In X-Plane relevant als Eingabelatenz (Controller → Steuerausschlag), Render-Latenz (Berechnung → Anzeige) und I/O-Latenz (Szenerie-Anforderung → Daten verfügbar). Systemtuning zielt darauf ab, alle drei Latenzarten zu minimieren.

### ldd

Ein Kommandozeilenprogramm unter Linux, das alle dynamischen Bibliotheksabhängigkeiten einer ausführbaren Datei anzeigt. Es ist ein wichtiges Diagnosewerkzeug, um fehlende oder inkompatible Bibliotheken zu identifizieren, die für die Ausführung eines Programms wie X-Plane erforderlich sind.

### Linux

Ein freies, quelloffenes Betriebssystem, das sich besonders durch seine Stabilität, Sicherheit und Anpassungsfähigkeit auszeichnet.

### Liquorix-Kernel

Eine optimierte Version des Linux-Kernels, die auf Performance ausgerichtet ist. Bietet oft bessere Reaktionszeiten und Leistung für Desktop-Systeme und Gaming.

## M

### Mesa

Der Open-Source-Grafiktreiber-Stack für Linux, der OpenGL- und Vulkan-Implementierungen für AMD (RADV), Intel und andere GPUs bereitstellt. Mesa enthält auch die Zink-Übersetzungsschicht. Die Umgebungsvariable `MESA_LOADER_DRIVER_OVERRIDE` wird nur von Mesa-Treibern ausgewertet, nicht von Nvidia.

### Mesh

Das Höhenmodell (Terrain Mesh) in X-Plane, das die dreidimensionale Geländeform definiert — Berge, Täler, Küstenlinien. Das Standard-Mesh kann durch höher aufgelöste Meshes von Drittanbietern ersetzt werden. In der scenery_packs.ini wird das Mesh typischerweise unterhalb der Orthofoto-Schicht platziert.

## N

### noatime

Eine Mount-Option für Linux-Dateisysteme, die das Aktualisieren des Zugriffszeitstempels beim Lesen von Dateien unterdrückt. Reduziert unnötige Schreibzugriffe auf die SSD und verbessert die I/O-Performance, besonders beim Laden großer Szenerie-Verzeichnisse. Siehe [Dateisystem](linux/optimizations/filesystem.md).

### Nouveau

Der Standard-Open-Source-Treiber für Nvidia-Grafikkarten in Linux. Wird oft deaktiviert, wenn der proprietäre Nvidia-Treiber installiert wird.

### Nvidia-Treiber

Proprietäre Treibersoftware von Nvidia für ihre Grafikkarten. Bietet im Vergleich zum Open-Source-Treiber Nouveau oft bessere Performance und mehr Funktionen, besonders für 3D-Anwendungen und Gaming.

### NVMe (Non-Volatile Memory Express)

Ein Protokoll für den Zugriff auf SSDs über die PCIe-Schnittstelle. NVMe-SSDs bieten deutlich höhere Durchsatz- und niedrigere Latenzwerte als SATA-SSDs. Für X-Plane relevant wegen schnellerer Szenerie-Ladezeiten. Das Energiespar-Feature APST sollte für optimale Performance deaktiviert werden.

## O

### OpenGL

Eine plattformübergreifende Grafikschnittstelle, die in X-Plane 12 zugunsten von Vulkan als primäre Render-API abgelöst wurde. OpenGL wird weiterhin von einigen Plugins für ihre Darstellung genutzt. Die Zink-Übersetzungsschicht in Mesa ermöglicht es, diese OpenGL-Aufrufe innerhalb der Vulkan-Pipeline zu verarbeiten.

### Ortho4XP

Ein Tool zur Erstellung von fotorealistischen Landschaftstexturen für X-Plane aus verschiedenen Satellitenbildquellen.

### Orthofotos

Orthofotos (oder Orthophotos) sind maßstabsgetreue, verzerrungsfreie Luftbilder der Erdoberfläche. Sie werden in X-Plane als hochauflösende Bodentexturen verwendet, um eine realistische Darstellung der Landschaft zu erreichen.

### Overlay (Szenerie)

Eine Szenerie-Schicht in X-Plane, die über einer Basis-Szenerie liegt und diese ergänzt oder ersetzt. Overlays enthalten typischerweise Flughäfen, Gebäude oder Straßen, während die Basis-Schicht Geländemesh und Orthofotos bereitstellt. Die Reihenfolge in der scenery_packs.ini bestimmt, welche Overlays Vorrang haben. Siehe [Szenerien-Komponenten](scenery/aufbau_quellen/scenery_components.md).

## P

### PBR

Physically Based Rendering - ein Grafikverfahren, das physikalische Eigenschaften von Materialien und Licht simuliert, um realistische Darstellungen zu erzeugen.

### PDS (Priority and Deadline based Skiplist)

Der CPU-Scheduler des Liquorix-Kernels, der den Mainline-Scheduler EEVDF ersetzt. PDS nutzt eine Skiplist-Datenstruktur für effiziente Aufgabenauswahl und priorisiert nach Deadlines. In Kombination mit kürzeren Preemption-Fenstern und einer Timer-Frequenz von 1000 Hz bietet er niedrigere Latenz für interaktive Anwendungen. Anders als EEVDF liefert PDS nicht die Auslastungssignale, die der `schedutil`-Governor benötigt. Siehe [Systemtuning](linux/system/systemtuning.md).

### PipeWire

Ein modernes Audio- und Video-Framework für Linux, das PulseAudio und JACK ersetzen soll. PipeWire bietet niedrigere Latenz und bessere Integration mit professionellen Audio-Workflows. FMOD in X-Plane kommuniziert über die PulseAudio-kompatible Schnittstelle mit PipeWire.

### Plugin

Eine Softwareerweiterung, die zusätzliche Funktionen zu X-Plane hinzufügt. Plugins können von Drittanbietern entwickelt werden.

### Preemption

Die Fähigkeit des Kernels, laufende Aufgaben zu unterbrechen, um höher priorisierten Aufgaben CPU-Zeit zu geben. Mehr Preemption bedeutet geringere Latenz, aber auch mehr Overhead. Der Liquorix-Kernel nutzt Full Preemption für minimale Reaktionszeiten. Siehe [Systemtuning](linux/system/systemtuning.md).

### PulseAudio

Ein Audio-Server für Linux, der die Audioströme mehrerer Anwendungen mischt und an die Hardware weiterleitet. Wird zunehmend durch PipeWire ersetzt, ist aber auf vielen Systemen noch im Einsatz. FMOD in X-Plane kommuniziert über die PulseAudio-Schnittstelle — sowohl mit PulseAudio selbst als auch mit PipeWire über dessen Kompatibilitätsschicht.

### pyenv

Ein Werkzeug zur Verwaltung verschiedener Python-Versionen auf einem System. Es ermöglicht die Installation und Nutzung mehrerer Python-Versionen nebeneinander, ohne das System-Python zu beeinflussen.

## R

### RADV

Der Open-Source-Vulkan-Treiber für AMD-GPUs innerhalb des Mesa-Treiberstacks. RADV ist der Standard-Vulkan-Treiber auf Linux-Systemen mit AMD-Grafikkarten und wird von X-Plane 12 direkt genutzt.

## S

### scenery_packs.ini

Eine Konfigurationsdatei im Custom Scenery-Ordner von X-Plane, die die Ladereihenfolge der installierten Szenerien festlegt. AutoOrtho fügt hier automatisch Einträge mit dem Präfix `z_ao_` hinzu.

### SDL2 (Simple DirectMedia Layer)

Eine plattformübergreifende Multimedia-Bibliothek, die X-Plane 12 unter Linux für Fensterverwaltung, Eingabegeräte und Joystick-Erkennung verwendet. SDL2 kommuniziert mit dem Display-Server (X11/XWayland) und dem Eingabe-Subsystem (evdev).

### Shader Cache

Ein Zwischenspeicher für kompilierte GPU-Shader-Programme. X-Plane kompiliert Shader beim ersten Laden einer Szene, was zu Rucklern führen kann. Der Shader Cache speichert die kompilierten Ergebnisse, sodass nachfolgende Ladevorgänge schneller ablaufen. Unter Linux liegt der Cache in `~/.cache/`. Siehe [Konfiguration](xplane/setup_diagnose/config.md).

### Single-CPU

Eine historische Bezeichnung für X-Planes Architektur. Single-Core-Performance bleibt zwar wichtig, aber X-Plane 12 verteilt seit Version 12.4 einen erheblichen Teil der Frame-Arbeit auf mehrere Kerne.

### SimHeaven (X-World)

Ein Szenerie-Framework für X-Plane, das 3D-Gebäude, Vegetation und andere Autogen-Objekte auf Basis von OpenStreetMap-Daten generiert. SimHeaven X-World ergänzt Orthofoto-Tools wie AutoOrtho um die 3D-Schicht, die Orthofotos allein nicht bieten können. Bei Verwendung von SimHeaven sind die in AutoOrtho enthaltenen yOrtho-Overlays nicht erforderlich.

### SoftIRQ (Software Interrupt)

Ein verzögerter Interrupt-Verarbeitungsmechanismus im Linux-Kernel. Anders als Hardware-IRQs, die sofort behandelt werden, werden SoftIRQs nach Abschluss des Hardware-Interrupt-Handlers verarbeitet und übernehmen weniger zeitkritische Aufgaben wie Netzwerkpaket-Verarbeitung und Block-Device-Completion. Die Spalte `%soft` in `mpstat` zeigt die SoftIRQ-Zeit pro Kern — relevant für die Verifikation, dass Interrupt-Shielding sowohl Hardware-IRQs als auch SoftIRQs von den Applikations-Kernen fernhält. Siehe [Systemtools](linux/system/systemtools.md).

### sysctl

Ein Werkzeug zur Anzeige und Änderung von Kernel-Parametern zur Laufzeit. Im Gegensatz zu GRUB-Kernel-Parametern, die nur beim Booten wirken, können sysctl-Werte jederzeit angepasst werden. Relevante Einstellungen für X-Plane umfassen VM-Swappiness und Netzwerk-Buffer. Konfiguration über `/etc/sysctl.d/`.

### systemd

Das Init-System und Service-Management-Framework der meisten Linux-Distributionen. systemd startet und verwaltet Systemdienste, Timer und Mount-Punkte. Für X-Plane relevant durch Timer wie `fstrim.timer` (SSD-TRIM), Service-Units für irqbalance und die Konfiguration von CPU-Governor-Einstellungen beim Systemstart.

## T

### Tearing

Ein sichtbares Bildartefakt, bei dem Teile zweier aufeinanderfolgender Frames gleichzeitig angezeigt werden, erkennbar als horizontaler Riss im Bild. Tritt auf, wenn die GPU einen neuen Frame liefert, während der Monitor noch den vorherigen darstellt. V-Sync verhindert Tearing, kann aber Eingabelatenz erhöhen. Unter X11 im Fullscreen-Modus ist Tearing selten ein Problem.

### Tick Rate (HZ)

Die Frequenz, mit der der Linux-Kernel seine interne Timer-Unterbrechung auslöst. Ein höherer Tick (z.B. 1000 Hz beim Liquorix-Kernel) ermöglicht feinere Scheduling-Granularität und niedrigere Latenz, erzeugt aber mehr Overhead. Der Standard-Kernel nutzt typischerweise 250 Hz. Siehe [Liquorix](linux/optimizations/liquorix.md).

### TRIM

Ein Befehl, der dem SSD-Controller mitteilt, welche Datenblöcke nicht mehr benötigt werden. Regelmäßiges TRIM (via `fstrim.timer` oder die Mount-Option `discard`) erhält die Schreibgeschwindigkeit der SSD und verhindert Leistungseinbrüche bei großen Szenerie-Installationen. Siehe [Dateisystem](linux/optimizations/filesystem.md).

## V

### VRAM (Video RAM)

Der Arbeitsspeicher auf der Grafikkarte, in dem Texturen, Shader, Framebuffer und andere Grafikdaten gespeichert werden. X-Plane mit hochauflösenden Orthofotos kann mehrere Gigabyte VRAM belegen. Reicht der VRAM nicht aus, müssen Texturen zwischen GPU- und Systemspeicher verschoben werden, was zu Rucklern führt.

### Vulkan API

Eine moderne, plattformübergreifende Grafikschnittstelle mit geringem Overhead, die von X-Plane für die Grafikdarstellung verwendet wird. Im Vergleich zu OpenGL bietet Vulkan oft bessere Performance durch effizientere CPU-Nutzung und direktere GPU-Kontrolle.

## W

### Wayland

Ein modernes Display-Server-Protokoll für Linux, Nachfolger von X11. Der Compositor übernimmt sowohl Display-Server- als auch Fenstermanager-Aufgaben. Wayland bietet bessere Sicherheit und unabhängige Monitor-Refresh-Rates, aber X-Plane 12 kann kein natives Wayland und nutzt stattdessen XWayland. Siehe [Display-Server](linux/optimizations/displayserver.md).

### Wine (Wine Is Not an Emulator)

Ein Kompatibilitätslayer, der es ermöglicht, Windows-Programme unter Linux auszuführen. Wine übersetzt Windows-API-Aufrufe in POSIX-Aufrufe, ohne Windows selbst zu emulieren.

## X

### X11 (Xorg)

Das klassische Display-Server-Protokoll für Linux, im Einsatz seit 1984. Ein zentraler X-Server verwaltet alle Grafik- und Eingabeoperationen. X-Plane spricht X11 nativ. Siehe [Display-Server](linux/optimizations/displayserver.md).

### X-Plane

Ein hochrealistischer Flugsimulator, der für verschiedene Plattformen (Windows, macOS, Linux) verfügbar ist.

### XWayland

Eine Kompatibilitätsschicht, die einen vollständigen X11-Server innerhalb einer Wayland-Session betreibt. Wenn eine X11-Anwendung (wie X-Plane) auf einem Wayland-Desktop startet, übernimmt XWayland automatisch die Übersetzung. Der zusätzliche Übersetzungsschritt kostet Latenz. Siehe [Wayland-Session](linux/optimizations/displayserver_wayland.md).

### Xroads

Eine Bibliothek für X-Plane 11 & 12, die die Darstellung von Straßen in Ortho4XP-Szenerien optimiert.

## Z

### Zink

Eine OpenGL-Übersetzungsschicht innerhalb von Mesa, die OpenGL-Befehle in Vulkan-Befehle übersetzt. X-Plane 12 liefert einen eigenen Zink-Treiber mit, damit Plugins, die OpenGL für ihre Darstellung nutzen, innerhalb der Vulkan-Renderpipeline funktionieren.

### ZL (Zoom Level)

Die Zoomstufe von Orthofotos, die deren Auflösung bestimmt. Höhere ZL-Werte bedeuten detailliertere Bilder: ZL16 entspricht etwa vier Metern pro Pixel, ZL17 zwei Metern, ZL18 einem Meter. Höhere Zoomstufen benötigen deutlich mehr Speicherplatz und Bandbreite. Siehe [Einführung Orthofotografie](scenery/orthophotography/orthophotography_intro.md).

## 3

### 32-Bit-Kompatibilität

Die Fähigkeit eines 64-Bit-Linux-Systems, 32-Bit-Anwendungen und -Bibliotheken auszuführen und zu unterstützen. Für manche Programme oder Plugins, die noch nicht für 64-Bit-Architekturen optimiert wurden, kann dies erforderlich sein. Unter Debian wird die 32-Bit-Unterstützung durch Hinzufügen der i386-Architektur und Installation entsprechender Bibliotheken aktiviert.
