## XRoads

[XRoads](../glossary.md#xroads) ist eine Bibliothek für [X-Plane](../glossary.md#x-plane) 11 & 12, die die Realitätsnähe von [Ortho4XP](../glossary.md#ortho4xp)-Orthobildern verbessert. Die Bibliothek blendet standardmäßig angezeigte Straßenpolygone aus Datenbanken wie OSM aus, insbesondere bei ZL17+ Orthos. Dadurch werden die tatsächlichen Straßen aus den Satellitenbildern sichtbar, während Brücken, Autobahnen, Schnellstraßen und Eisenbahnschienen weiterhin dargestellt werden. Die Geschwindigkeit der AI-Fahrzeuge wird auf 70 % der ursprünglichen Geschwindigkeit reduziert (anpassbar über den Parameter "-v"), was zu realistischeren Verkehrsverhältnissen führt. Eine automatisch generierte library.txt ermöglicht die gezielte Steuerung der transparenten Straßen. In Bereichen ohne Ortho-Kacheln bleiben die Autogen-Straßen sichtbar.

Download: [XRoads](https://forums.x-plane.org/index.php?/files/file/67227-xroads-transparent-roads-for-ortho4xp/)

### Installation unter Linux

Für die Erstellung des Executables wird in das XRoads-Verzeichnis gewechselt und der Befehl `make xroads` ausgeführt. Bei installierten Makefile- und C-Compiler-Paketen wird das Executable mit diesem Aufruf generiert.

