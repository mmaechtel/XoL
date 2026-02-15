# DK Toliss Callout

DK Toliss Callout ist ein [FlyWithLua](flywithlua.md)-Skript, das automatische Sprachansagen des Flight Mode Annunciator (FMA) für ToLiss-Airbus-Flugzeuge bereitstellt. Bei Änderungen der Autopilot-Modi (CLB, OP CLB, SPEED, NAV, G/S) gibt das Skript den neuen Modus per Text-to-Speech aus.

## Hintergrund

- **Entwickler:** cxn0026
- **Download:** [X-Plane.org](https://forums.x-plane.org/files/file/91367-toliss-airbus-fma-callout-flywithlua-script/)
- **Plattformen:** Windows, macOS, Linux (reines Lua)
- **Kompatibilität:** X-Plane 12
- **Preis:** Kostenlos
- **Abhängigkeit:** [FlyWithLua NG+](flywithlua.md)

Das Skript liest die blauen FMA-Werte aus dem oberen FMA-Feld auf dem PFD. Magenta-Werte sind noch nicht implementiert. Aufgrund der Komplexität beim Auslesen der FMA-Daten aus ToLiss-Flugzeugen können Ansagen gelegentlich ausbleiben, abhängig von Variablenänderungen. Verifiziert auf der A319 und A320neo — sollte auch mit anderen ToLiss-Airbus-Typen funktionieren.

## Funktionsumfang

- **Automatische FMA-Ansagen:** Gibt Autopilot-Modusänderungen per TTS aus
- **Anpassbarer TTS-Text:** Der von der Sprach-Engine ausgesprochene Text lässt sich bearbeiten
- **Echtzeit-Überwachung:** Erkennt FMA-Änderungen, sobald sie auftreten

## Mehrwert in der Flugsimulation

FMA-Callouts sind in echten Airbus-Cockpits Standardverfahren — der Pilot Monitoring gibt Modusänderungen bekannt, um das gemeinsame Situationsbewusstsein aufrechtzuerhalten. Dieses Skript automatisiert das Verfahren für den Einzelpilotenbetrieb, erhöht den Realismus bei ToLiss-Airbus-Flügen und hilft, Autopilot-Modusübergänge zu verfolgen, ohne ständig den FMA-Bereich abzulesen.

## Installation

**Download:** [X-Plane.org](https://forums.x-plane.org/files/file/91367-toliss-airbus-fma-callout-flywithlua-script/)

Die `.lua`-Datei in `Resources/plugins/FlyWithLua/Scripts/` ablegen.

### Linux-Hinweise

Keine Linux-spezifischen Probleme bekannt. Das Skript nutzt X-Planes eingebautes TTS über `XPLMSpeakString()`. Für hörbare Ausgabe unter Linux ist [XLinSpeak](xlinspeak.md) erforderlich.

## Quellen

- [Toliss Airbus FMA Callout — X-Plane.org](https://forums.x-plane.org/files/file/91367-toliss-airbus-fma-callout-flywithlua-script/)
