---
title: Glossar
description: Begriffserklärungen rund um X-Plane und Linux
tags:
  - reference
---

# Glossar

## A
### AutoOrtho
Ein Tool für X-Plane, das Orthofotos direkt in den Flugsimulator integriert. Es ermöglicht das Streaming von hochauflösenden Luftbildern als Bodenstruktur, ohne dass diese vorher heruntergeladen und konvertiert werden müssen. Die Software kann entweder als vorgefertigte Binary oder aus dem Quellcode installiert werden.

## B
### Binary
Eine vorkompilierte, ausführbare Datei eines Programms. Im Gegensatz zur Installation aus dem Quellcode kann eine Binary direkt ausgeführt werden, ohne dass weitere Kompilierungsschritte notwendig sind.

### Blade Element Theory
Eine Berechnungsmethode in der Aerodynamik, bei der ein Flugzeug in viele kleine Segmente zerlegt wird, um die Luftströmung und Kräfte in Echtzeit zu simulieren.

## C
### Custom Scenery
Ein Verzeichnis in X-Plane, in dem zusätzliche Szenerie-Dateien gespeichert werden. Hier werden auch die von AutoOrtho generierten Ortho-Texturen eingebunden.

## D
### Docker
Eine Plattform zur Containerisierung von Anwendungen, die es ermöglicht, Software in standardisierten Einheiten (Containern) zu verpacken und auszuführen. Docker vereinfacht die Bereitstellung und Verwaltung von Anwendungen in unterschiedlichen Umgebungen.

### DKMS (Dynamic Kernel Module Support)
Ein Framework, das die automatische Neukompilierung von Kernel-Modulen bei Kernel-Updates ermöglicht. Besonders wichtig für Treiber wie Nvidia, die nicht im Standard-Kernel enthalten sind.

## F
### FAA
Federal Aviation Administration - die US-amerikanische Luftfahrtbehörde, die Standards für Flugsimulationen und Trainingsgeräte festlegt.

## G
### GUI (Graphical User Interface)
Eine grafische Benutzeroberfläche, die die Interaktion mit einem Programm durch grafische Elemente wie Fenster, Buttons und Menüs ermöglicht. Bei AutoOrtho dient die GUI zur Konfiguration des X-Plane-Verzeichnisses und zum Laden von Ortho-Sets.

## H
### HDR
High Dynamic Range - ein Grafikverfahren, das einen besonders großen Helligkeitsbereich darstellen kann, was zu realistischeren Lichteffekten führt.

## K
### KVM (Kernel-based Virtual Machine)
Eine in den Linux-Kernel integrierte Virtualisierungslösung, die es ermöglicht, virtuelle Maschinen mit nahezu nativer Leistung auszuführen. KVM nutzt Hardware-Virtualisierungsfunktionen moderner Prozessoren für effiziente Virtualisierung.

## L
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

## S
### scenery_packs.ini
Eine Konfigurationsdatei im Custom Scenery-Ordner von X-Plane, die die Ladereihenfolge der installierten Szenerien festlegt. AutoOrtho fügt hier automatisch Einträge mit dem Präfix `z_ao_` hinzu.

### Single-CPU
Beschreibt die aktuelle Architektur von X-Plane, bei der die Hauptsimulation auf einem einzelnen Prozessorkern läuft.

## W
### Wine (Wine Is Not an Emulator)
Ein Kompatibilitätslayer, der es ermöglicht, Windows-Programme unter Linux auszuführen. Wine übersetzt Windows-API-Aufrufe in POSIX-Aufrufe, ohne Windows selbst zu emulieren.

## X
### X-Plane
Ein hochrealistischer Flugsimulator, der für verschiedene Plattformen (Windows, macOS, Linux) verfügbar ist.

### Xroads
Eine Bibliothek für X-Plane 11 & 12, die die Darstellung von Straßen in Ortho4XP-Szenerien optimiert. 