# Little XpConnect

Little XpConnect ist ein [Plugin](../glossary.md#plugin) für [X-Plane](../glossary.md#x-plane) 11/12, das als Brücke zwischen X-Plane und dem Flugplanungs- und Navigationswerkzeug [Little Navmap](https://github.com/albar965/littlenavmap) dient.

## Hintergrund

- **Entwickler:** Alexander Barthel (albar965)
- **Repository:** [github.com/albar965/littlexpconnect](https://github.com/albar965/littlexpconnect) (Open Source, GPL-3.0)
- **Plattformen:** Windows, macOS, Linux (native Binaries)
- **Kompatibilität:** X-Plane 11 und X-Plane 12
- **Preis:** Kostenlos

Das Plugin wird aktiv gepflegt und ist im Little-Navmap-Download-Archiv enthalten — es wird nicht separat heruntergeladen.

## Funktionsumfang

- **Flugdaten-Übertragung:** Position, Geschwindigkeit, Heading, Höhe, Autopilot-Einstellungen, Treibstoff, Gewicht
- **Wetterdaten:** Temperatur, Druck, Sichtweite, Wind, Vereisung
- **AI/Multiplayer-Flugzeuge:** Positionen über TCAS-Interface
- **Schiffspositionen:** Träger und Fregatte
- **Shared Memory IPC:** Kommunikation über Shared Memory — kein Netzwerkport für lokale Verbindungen
- **Konfigurierbare Abtastrate:** 50–500 ms Intervall für Dataref-Abfragen

### Netzwerk-Betrieb

Für den Betrieb von Little Navmap auf einem anderen Rechner wird **Little Navconnect** (ebenfalls im Download enthalten) auf dem X-Plane-Rechner gestartet. Es liest den Shared Memory und leitet die Daten über TCP-Port **51968** weiter.

## Mehrwert in der Flugsimulation

Little Navmap ist eines der umfangreichsten kostenlosen Flugplanungs- und Navigationswerkzeuge. Little XpConnect ermöglicht die Echtzeit-Anzeige der Flugzeugposition auf der Little-Navmap-Karte, Moving Map während des Flugs und die Überwachung aller Flugparameter. Das Plugin arbeitet über Shared Memory statt Netzwerk, was minimale Latenz und keinen Konfigurationsaufwand für lokale Setups bedeutet.

## Installation

**Download:** Im [Little Navmap-Archiv](https://github.com/albar965/littlenavmap/releases) enthalten.

Den Ordner `Little Xpconnect` aus dem Archiv nach `Resources/plugins/` kopieren. Das Plugin kann auch über das Little-Navmap-Menü (`Tools`) installiert/aktualisiert werden.

Es werden keine zusätzlichen Systempakete benötigt. Es sind keine Linux-spezifischen Probleme bekannt.

**Konfigurationsdatei:** `$HOME/.config/ABarthel/little_xpconnect.ini`

## Quellen

- [Little XpConnect — GitHub](https://github.com/albar965/littlexpconnect)
- [Little Navmap — GitHub](https://github.com/albar965/littlenavmap)
- [Little Navmap — Dokumentation](https://www.littlenavmap.org/)
