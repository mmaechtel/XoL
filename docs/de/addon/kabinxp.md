# KabinXP

KabinXP ist ein leichtgewichtiges Cabin-Announcement-Plugin für [X-Plane](../glossary.md#x-plane) 12. Es spielt benutzerdefinierte Audiodateien (Kapitänsdurchsagen, Sicherheitsbriefings, Boarding-Sounds) per Klick während des Fluges ab. Das Plugin wird mit einer leeren Sound-Bibliothek geliefert — eigene Audiodateien werden bereitgestellt und pro Airline oder Livery organisiert.

## Hintergrund

- **Entwickler:** Kadikoy34
- **Download:** [forums.x-plane.org](https://forums.x-plane.org/files/file/98298-kabinxp/)
- **Plattformen:** Windows, macOS, Linux
- **Kompatibilität:** X-Plane 12

## Funktionsumfang

- **Eigene Audio-Bibliothek:** Wird leer geliefert — WAV-, MP3- oder FLAC-Dateien selbst bereitstellen
- **Livery-spezifische Sound-Packs:** Jede Livery kann einen eigenen Ansagen-Ordner haben, wird beim Laden automatisch erkannt
- **3D Spatial Audio:** Sounds werden positionsgenau im Flugzeug-Inneren platziert
- **Eigene Unterordner:** Bis zu 10 Unterordner pro Ansagen-Ordner, UI-Buttons passen sich automatisch an
- **Drag-and-Arrange Buttons:** Ansagen-Buttons per Drag-and-Drop umsortieren
- **Persistente Layouts:** Button-Reihenfolge wird pro Livery gespeichert und beim nächsten Flug wiederhergestellt
- **Live-Anzeige:** Zeigt an, welche Ansage gerade abgespielt wird

## Mehrwert in der Flugsimulation

KabinXP bringt Kabinenatmosphäre, ohne ein bestimmtes Flugzeug oder eine Preset-Bibliothek vorauszusetzen. Da eigene Audiodateien verwendet werden, funktioniert es mit jeder Airline-Livery und in jeder Sprache. Die Livery-spezifische Erkennung sorgt dafür, dass beim Wechsel von einer Lufthansa- zu einer Ryanair-Livery automatisch die passenden Durchsagen geladen werden — keine manuelle Konfiguration nötig.

## Installation

**Download:** [forums.x-plane.org](https://forums.x-plane.org/files/file/98298-kabinxp/)

Als eigenständiges Plugin nach `Resources/plugins/KabinXP/` installieren. In jedem Livery-Verzeichnis einen Sound-Ordner anlegen und Audiodateien (WAV, MP3 oder FLAC) hinterlegen. KabinXP erkennt die Livery beim Laden des Flugzeugs und zeigt die verfügbaren Ansagen in der UI an.

### Linux-Hinweise

KabinXP ist ein kompiliertes Plugin. Vor der Installation prüfen, ob der Download eine `lin.xpl`-Binärdatei enthält. Falls nur Windows- und macOS-Binaries vorhanden sind, unterstützt das Plugin Linux nicht nativ.

## Quellen

- [KabinXP — forums.x-plane.org](https://forums.x-plane.org/files/file/98298-kabinxp/)
- [KabinXP — x-plane.to](https://x-plane.to/file/2078/kabinxp)
