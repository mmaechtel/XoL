---
description: "Bay's Lighting Mod ist eine Beleuchtungsüberarbeitung für X-Plane 12 — Flughafen-, Beacon-, Nacht- und Cockpitbeleuchtung, Wolkenstreuung und Sichtweite."
---
# Bay's Lighting Mod

Bay's Lighting Mod ersetzt das Beleuchtungssystem von [X-Plane](../../glossary.md#x-plane) 12 durch einen überarbeiteten Satz aus Texturen, Sprites und Parametern. Betroffen sind Flughafen- und Beacon-Lichter, die Nachtbeleuchtung, die atmosphärische Streuung, die Cockpitbeleuchtung und die Sichtweite — mit dem erklärten Ziel, den Simulator besser aussehen zu lassen, ohne den Realismus zu opfern.

## Hintergrund

- **Entwickler:** baylor703
- **Download:** [forums.x-plane.org](https://forums.x-plane.org/files/file/97497-bays-lighting-mod/)
- **Plattformen:** Keine Plattformeinschränkung angegeben — das Paket enthält Texturen und ein Lua-Skript, keine Binary
- **Kompatibilität:** X-Plane 12
- **Abhängigkeit:** [FlyWithLua NG+](../scripting/flywithlua.md)
- **Lizenz:** Kostenloser Download, Spenden über Patreon

Das Paket ist nicht mit anderen Lighting-Mods kompatibel — es kann immer nur einer davon aktiv sein.

## Funktionsumfang

- **Flughafen- und Beacon-Beleuchtung:** Überarbeitete Anflug-, Rollweg- und Beacon-Lichter sowie geänderte Positions- und Beacon-Lichter am Flugzeug
- **Nachtbeleuchtung:** Neue Sprites für die 3D-Lichter und überarbeitete Effekte um sie herum
- **Fernbeleuchtung:** Der Übergang von den nahen „3D"-Lichtern zu den entfernten, eingebackenen Lichttexturen ist auf nahezu nahtlos abgestimmt — vorausgesetzt, Ortho-Szenerien sind abgeschaltet
- **Wolken und Streuung:** Geänderte atmosphärische Streuung und Wolkenbeleuchtung
- **Cockpitbeleuchtung:** Verbesserte Innenraumbeleuchtung
- **Dämmerung:** Überarbeitete Farb- und Lichtcharakteristik in den Dämmerungsstunden
- **Sichtweite:** Größere Spreizung zwischen klaren und trüben Bedingungen — dieselbe Größe, die [AutoHaze](../flylua_scripts/autohaze.md) laufend aus Echtdaten neu berechnet, beim Parallelbetrieb also ein Auge auf das Ergebnis haben

## Nachtflug und Orthofotos

X-Plane zeichnet die Nachtbeleuchtung in zwei Schichten: nahe am Flugzeug als einzelne 3D-Lichter, weiter außen als eingebackene Lichttexturen, die auf dem Boden liegen. [Orthofoto](../../scenery/orthophotography/index.md)-Szenerien ersetzen diese Bodentexturen. Eine Terrain-Definition kann über `LIT_TEX` ein eigenes Nacht-Overlay deklarieren, Ortho-Kacheln bringen in der Regel aber keines mit — die entfernte Schicht entfällt damit, die 3D-Lichter enden abrupt in geringer Entfernung zum Flugzeug, dahinter ist alles schwarz. Das passiert mit und ohne installierten Mod; es folgt aus dem Schichtaufbau der X-Plane-Nachtbeleuchtung.

!!! tip "Ortho für Nachtflüge abschalten"

    Die Empfehlung des Entwicklers lautet, Ortho-Szenerien für Nachtflüge generell zu deaktivieren — im Dunkeln sind Ortho-Bodentexturen ohnehin kaum sichtbar, während die entfernte Lichtschicht bis zum Horizont reicht. Für [Ortho-Streaming](../../scenery/ortho_streaming/index.md)-Setups bedeutet das, die Streaming-Schicht vor dem Abflug abzuschalten, statt Einstellungen des Mods zu ändern.

## Mehrwert in der Flugsimulation

Die Standard-Nachtbeleuchtung von X-Plane 12 hat eine sichtbare Kante dort, wo die 3D-Lichter in die Bodentexturen übergehen, und die Hauptarbeit des Mods steckt darin, diese Kante zu schließen. Die Überarbeitung reicht bis in Dämmerung und Wolkenstreuung — die visuelle Charakteristik ändert sich damit über einen ganzen Flug hinweg und nicht erst nach Einbruch der Dunkelheit. Wie weit die größere Sichtweiten-Spreizung trägt, ist eine Aussage des Entwicklers und hängt stark vom übrigen Szenerie-Setup ab.

## Installation

**Download:** [forums.x-plane.org](https://forums.x-plane.org/files/file/97497-bays-lighting-mod/)

Zwei Schritte, beide ausführlich in der beiliegenden Readme beschrieben:

1. Den Ordner `Resources` aus dem Archiv in das X-Plane-12-Hauptverzeichnis kopieren und die Überschreiben-Abfrage bestätigen — erscheint keine Abfrage, ist der Ordner an der falschen Stelle gelandet.
2. `bays_lighting.lua` nach `Resources/plugins/FlyWithLua/Scripts/` kopieren.

Der Download enthält zusätzlich die Standard-Lichtdateien samt Anleitung zum Zurückspielen, die Änderung lässt sich also ohne Neuinstallation des Simulators rückgängig machen.

!!! warning "Überschreiben innerhalb von Resources"

    Der Mod überschreibt Standarddateien in `Resources`. Vor der Installation eine Kopie des Originalverzeichnisses anlegen. Ein X-Plane-Update spielt diese Dateien wieder als Standard zurück und entfernt den Mod damit — das erneute Installieren gehört zur Update-Routine.

## Quellen

- [Bay's Lighting Mod — forums.x-plane.org](https://forums.x-plane.org/files/file/97497-bays-lighting-mod/)
