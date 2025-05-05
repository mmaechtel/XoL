# **XoL**: Running **X**-Plane **o**n **L**inux

Diese Dokumentation richtet sich an Linux-erfahrene Benutzer, die X-Plane unter Linux betreiben möchten. Eine funktionierende Linux-Installation wird vorausgesetzt.

Die hier gezeigten Beispiele basieren auf Debian Linux, lassen sich aber leicht auf andere Distributionen übertragen. Die grundlegenden Konzepte und Vorgehensweisen bleiben dabei gleich - lediglich die spezifischen Paketmanager-Befehle oder Repository-Konfigurationen müssen entsprechend angepasst werden.

## Inhalt der Dokumentation

Die Dokumentation umfasst die wichtigsten Bereiche der X-Plane-Konfiguration unter Linux. Im Fokus stehen die optimalen Einstellungen für X-Plane, die Performance-Optimierung durch Kernel, Treiber und Systemeinstellungen, sowie die Installation und Konfiguration wichtiger Erweiterungen wie AutoOrtho. Zusätzlich werden häufige Probleme und deren Lösungen ausführlich behandelt. Ein besonderer Schwerpunkt liegt auf der Performance-Analyse mit integrierten und externen Tools, der Optimierung des Dateisystems für schnelle Ladezeiten und der hardware-spezifischen Anpassung für maximale Leistung.

## Struktur der Anleitungen

Die technischen Anleitungen sind modular aufgebaut und ermöglichen eine flexible Implementierung. Einzelne Komponenten können nach Bedarf umgesetzt oder das gesamte System nach den Anforderungen angepasst werden. Jede Anleitung beschreibt das Ziel und den Nutzen der Änderung, zeigt die notwendigen Schritte auf, erklärt wichtige Konfigurationsoptionen und bietet Tipps zur Fehlerbehebung. Die Anleitungen sind dabei in logische Abschnitte gegliedert: Grundlegende Systemoptimierung, Performance-Monitoring und -Analyse, Hardware-spezifische Anpassungen sowie fortgeschrittene Konfigurationen für spezielle Anwendungsfälle.

## Beitragen

Diese Dokumentation ist ein offenes Projekt. Verbesserungen oder Ergänzungen können über GitHub beigetragen werden:

- Issues für Fehler oder Vorschläge erstellen
- Pull Requests für Änderungen einreichen
- Erfahrungen in den Diskussionen im Footer dieser Webseite (z.B. über den Discord-Link) teilen

## Letzte Änderungen

### 2025-05-05
- Neue [Dateisystem-Dokumentation](filesystem.md)
- Discord Community-Kanal hinzugefügt
    - Link in der Fußzeile der deutschen und englischen Version verfügbar
    - Treten Sie unserer Community für Diskussionen und Support bei

### 2025-05-04
- [Szenerien Dokumentation](scenery.md) überarbeitet
    - Formatierung der Listen korrigiert (Einrückung, Leerzeichen)
    - Englische Version an deutsche Version angepasst
    - [Ressourcen/Maps Kapitel](scenery.md#ressourcen) überarbeitet
        - Selbst erstellte WorldMaps und deren Zweck hervorgehoben
        - Einschränkungen der ICAO-Code Suche für X-Plane 12 Szenerien dokumentiert
- [Ortho4XP Anleitung](addon/ortho4xp.md) erweitert
    - Neues Kapitel [Optimierung der Dateigröße](addon/ortho4xp.md#optimierung-der-dateigröße) hinzugefügt

### 2025-05-03
- [Szenerien Dokumentation](scenery.md) erweitert
    - Neues Kapitel [Szenerie Tips](blog/kcle-cleveland.html) hinzugefügt
        - Sammlung nützlicher Tipps und Tricks für die Szenerieverwaltung
        - Best Practices für die Organisation und Optimierung von Szenerien
    - RSS Feed erstellt
        - Automatische Generierung aus englischen Blog-Einträgen
        - Verfügbar unter `assets/rss/blog.xml`
