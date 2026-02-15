# XRoads

[XRoads](../glossary.md#xroads) ist eine Szenerie-Bibliothek für [X-Plane](../glossary.md#x-plane) 11 & 12, die standardmäßig angezeigte Straßenpolygone bei [Ortho4XP](../glossary.md#ortho4xp)-Orthobildern ausblendet, sodass die tatsächlichen Straßen aus den Satellitenbildern sichtbar werden.

## Hintergrund

- **Typ:** Szenerie-Bibliothek (kein Plugin)
- **Repository:** [github.com/melbo911/xroads](https://github.com/melbo911/xroads)
- **Quelle:** [forums.x-plane.org](https://forums.x-plane.org/index.php?/files/file/67227-xroads-transparent-roads-for-ortho4xp/) (Community-Projekt)
- **Plattformen:** Windows, macOS, Linux
- **Kompatibilität:** X-Plane 11 und X-Plane 12
- **Preis:** Kostenlos

## Funktionsumfang

- **Transparente Straßen:** Blendet Straßenpolygone aus OSM-Datenbanken aus, insbesondere bei ZL17+ [Orthofotos](../glossary.md#orthofotos)
- **Selektive Darstellung:** Brücken, Autobahnen, Schnellstraßen und Eisenbahnschienen bleiben sichtbar
- **AI-Fahrzeuggeschwindigkeit:** Reduziert auf 70 % (anpassbar über den Parameter `-v`) für realistischere Verkehrsverhältnisse
- **Automatische library.txt:** Ermöglicht die gezielte Steuerung der transparenten Straßen
- **Autogen-Fallback:** In Bereichen ohne Ortho-Kacheln bleiben die Standard-Straßen sichtbar

## Mehrwert in der Flugsimulation

Bei Ortho-Szenerien mit Zoomstufe 17 oder höher werden die Straßen im Satellitenbild so detailliert dargestellt, dass die von X-Plane überlagerten Autogen-Straßenpolygone störend wirken — sie liegen oft leicht versetzt über den realen Straßen. XRoads löst dieses Problem, indem es die überlagerten Polygone transparent macht. Brücken und Autobahnen werden beibehalten, da sie im Satellitenbild oft schwer erkennbar sind.

## Installation

**Download:** [XRoads](https://forums.x-plane.org/index.php?/files/file/67227-xroads-transparent-roads-for-ortho4xp/)

### Kompilierung auf Linux

XRoads wird als Quellcode ausgeliefert und muss auf Linux kompiliert werden. Voraussetzung sind `make` und ein C-Compiler:

```bash
sudo apt install build-essential
```

Anschließend im XRoads-Verzeichnis:

```bash
make xroads
```

Das erzeugte Executable wird dann auf die Ortho-Szenerien angewendet, um die `library.txt` zu generieren. Die resultierende Bibliothek wird als Szenerie-Ordner in `Custom Scenery/` abgelegt.

## Quellen

- [XRoads — GitHub](https://github.com/melbo911/xroads)
- [XRoads — forums.x-plane.org](https://forums.x-plane.org/index.php?/files/file/67227-xroads-transparent-roads-for-ortho4xp/)
