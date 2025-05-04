# **XoL**: Running **X**-Plane **o**n **L**inux

Diese Dokumentation richtet sich an Linux-erfahrene Benutzer, die X-Plane unter Linux betreiben möchten. Eine funktionierende Linux-Installation wird vorausgesetzt.

Die hier gezeigten Beispiele basieren auf Debian Linux, lassen sich aber leicht auf andere Distributionen übertragen. Die grundlegenden Konzepte und Vorgehensweisen bleiben dabei gleich - lediglich die spezifischen Paketmanager-Befehle oder Repository-Konfigurationen müssen entsprechend angepasst werden.

## Inhalt der Dokumentation

Die Dokumentation deckt folgende Hauptbereiche ab:

- **X-Plane Konfiguration**: Optimale Einstellungen für X-Plane unter Linux
- **Performance-Optimierung**: Kernel, Treiber und Systemeinstellungen für beste Leistung
- **Addons**: Installation und Konfiguration wichtiger Erweiterungen wie AutoOrtho
- **Fehlerbehebung**: Typische Probleme und deren Lösungen

## Struktur der Anleitungen

Die technischen Anleitungen sind modular aufgebaut. Sie können je nach Bedarf einzelne Komponenten implementieren oder das Gesamtsystem nach Ihren Anforderungen anpassen.

Jede Anleitung:

- Beschreibt das Ziel und den Nutzen der Änderung
- Zeigt die notwendigen Schritte
- Erklärt wichtige Konfigurationsoptionen
- Bietet Hinweise zur Fehlerbehebung

## Beitragen

Diese Dokumentation ist ein offenes Projekt. Wenn Sie Verbesserungen oder Ergänzungen haben, können Sie über GitHub dazu beitragen:

- Erstellen Sie Issues für Fehler oder Vorschläge
- Reichen Sie Pull Requests für Änderungen ein
- Teilen Sie Ihre Erfahrungen in den Diskussionen

## Letzte Änderungen

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
