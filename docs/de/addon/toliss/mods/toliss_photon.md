---
description: "ToLiss Photon überarbeitet Außen- und Cockpitbeleuchtung der ToLiss A319, A320, A321 und A330-900 — natives Plugin, eigener Linux-Installer, GPLv3."
---
# ToLiss Photon

ToLiss Photon überarbeitet die Beleuchtung der ToLiss-Airbus-Flotte in [X-Plane](../../../glossary.md#x-plane) 12. Sämtliche Außenlichter werden in den OBJ-Dateien des Flugzeugs neu angelegt, ein natives Plugin übernimmt das Blinkverhalten von Beacon und Strobe, und optional wird eine Cockpitbeleuchtung von Gus Rodrigues mitinstalliert. Welche Lampentechnik das Flugzeug verwendet — Halogen und Xenon, LED oder eine Mischung —, lässt sich im Simulator umschalten und wird pro Livery gespeichert.

## Hintergrund

- **Entwickler:** schmal (Cockpitbeleuchtung: Gus Rodrigues, mit Genehmigung integriert)
- **Download:** [forums.x-plane.org](https://forums.x-plane.org/files/file/100717-toliss-photon-complete-lighting-mod-for-toliss-a330a319a320a321/)
- **Quellcode:** [github.com/ischmal](https://github.com/ischmal/toliss-photon-lighting)
- **Plattformen:** Windows, macOS, Linux (Installer und Plugin je Plattform gebaut, Linux als x86_64)
- **Kompatibilität:** X-Plane 12, ToLiss A319, A320 (CEO/NEO), A321 (CEO/NEO) und A330-900
- **Abhängigkeit:** Keine — kompiliertes natives Plugin, weder [FlyWithLua](../../scripting/flywithlua.md) noch [XPPython3](../../scripting/xppython3.md) erforderlich
- **Lizenz:** GPL-3.0, kostenloser Download

## Funktionsweise

X-Plane zeichnet zwei Arten von Licht: Billboards, also 2D-Sprites, die einer Lichtquelle ihr Leuchten auf dem Bildschirm geben, und Spill Lights, die tatsächlich die Umgebung ausleuchten. Ein Billboard braucht eine Richtung, um überzeugend zu wirken — am hellsten frontal, verblassend, sobald die Kamera wegschwenkt. Vielen Standard-Billboards des ToLiss fehlt diese Richtung, sie leuchten über volle 360 Grad gleich hell, was der Hauptgrund für ihr flaches Erscheinungsbild ist.

Photon schreibt jedes Licht in den OBJ-Dateien neu, gibt jedem eine Richtung (ausgenommen oberes und unteres Beacon, die tatsächlich von allen Seiten sichtbar sind) und liest eigene Datarefs aus, damit dasselbe Licht wahlweise als Halogen oder als LED erscheint. Das Blinken selbst kommt vom Plugin: Es überschreibt in jedem Frame die Helligkeits-Datarefs des Simulators für Beacon und Strobe — dieselben, die ToLiss selbst bespielt — und ersetzt die Sinus-Blende des Originals durch das Verhalten der jeweiligen Lampentechnik.

## Funktionsumfang

- **Außenbeleuchtung:** Alle Außenlichter neu aufgebaut, überzogene Standard-Intensität reduziert, einzelne Lichter zwischen Halogen und LED umschaltbar
- **Beacon und Strobe:** LED-Beacons blinken, statt weich ein- und auszublenden; Xenon-Blitzröhren zünden schlagartig mit kaum wahrnehmbarem Nachleuchten
- **Farbcharakteristik:** Halogen wirkt sichtbar wärmer mit entsättigten Positionslichtern; weiße LEDs kaltweiß mit stark gesättigtem Rot und Grün; das Xenon-Beacon zieht durch das rote Glas leicht ins Pink
- **Cockpitbeleuchtung:** Bei der Installation optional, umschaltbar zwischen altem Halogen, neuem Halogen und LED
- **Displayleuchten:** Display Units, MCDUs und DCDUs erhalten eine eigene Hintergrundbeleuchtung — unabhängig von der Cockpitbeleuchtung und auch auf dem A330-900 verfügbar
- **Anpassung im Simulator:** Beleuchtungsoptionen lassen sich bei geladenem Flugzeug ändern, ohne Neustart und ohne erneute Installation
- **Pro Livery:** Einstellungen werden für jede Livery getrennt gespeichert

## Lichtprofile

Statt eines einzelnen Erscheinungsbilds bringt der Mod Profile mit, die die Lampentechnik nach Flugzeuggeneration bündeln.

| Profil | Außenbeleuchtung |
| --- | --- |
| Classic | Durchgehend Halogen, Xenon-Blitzröhren für Strobes und Beacons |
| Hybrid LED | LED für Positions- und Antikollisionslichter, Halogen für die Ausleuchtung |
| Full LED | Alle Außenlichter als LED |
| Auto | Profil wird automatisch aus der Ausstattung des Flugzeugs gewählt |
| Custom | Taxi-, Takeoff-, Runway-Turnoff-, Landing-, Wing-Inspection-, Positions-, Beacon-, Strobe- und Logo-Lichter einzeln einstellbar |

Die Cockpitbeleuchtung bietet drei eigene Varianten — warmes Orange, ein helleres Amber und Kaltweiß — und steht für den A330-900 nicht zur Verfügung. Lichtdesign, Platzierung und Texturen stammen von Gus Rodrigues; Photon macht sie lediglich im Simulator umschaltbar.

## Mehrwert in der Flugsimulation

Das Standard-Beacon blendet ein und aus wie ein aufheizender Glühfaden, was kein Beacon tut — es ist entweder eine Xenon-Blitzröhre oder eine LED. Mit dieser Diskrepanz begann das Projekt, und die Korrektur ist bei jeder Bodenbewegung und in jeder Außenansicht sichtbar. Die Profile für die Lampentechnik legen eine zweite Ebene darüber: Dasselbe Muster lässt sich mit Halogen und Xenon oder als reines LED-Flugzeug ausstatten, passend zur getragenen Bemalung. Wie viel das wert ist, hängt davon ab, wie oft das Flugzeug von außen oder bei Nacht zu sehen ist; der Cockpitteil zahlt sich nur bei Nachtflügen im ToLiss aus.

## Installation

**Download:** [forums.x-plane.org](https://forums.x-plane.org/files/file/100717-toliss-photon-complete-lighting-mod-for-toliss-a330a319a320a321/) oder [GitHub Releases](https://github.com/ischmal/toliss-photon-lighting/releases)

Der Linux-Download ist ein `.tar.gz` mit dem Installer, dem Ordner `data/` mit Lichtobjekten, Cockpittexturen und Plugin sowie einer `README.txt`. Von Hand wird nichts verschoben — das Archiv kann im Download-Ordner liegen bleiben:

1. Das gesamte Archiv entpacken und Installer und `data/` zusammenlassen; der Installer liest `data/` neben sich selbst.
2. In diesem Ordner ein Terminal öffnen und `./photon-installer` starten — vorher `chmod +x photon-installer`, falls das Ausführungsrecht das Entpacken nicht überlebt hat.
3. Den Schritten folgen: Der Installer erkennt X-Plane 12 selbst und fragt anschließend Flugzeug, Wing-Variante und die optionale Cockpitbeleuchtung ab.

Derselbe Installer entfernt den Mod auch wieder und spielt die ToLiss-Originaldateien zurück.

!!! note "Linux-Besonderheiten"

    Das Installer-Fenster wird auf der GPU gezeichnet. Bleibt es schwarz oder leer — VM, Remote-Sitzung, alte Treiber —, rendert `./photon-installer --software` es auf der CPU, und `./photon-installer-console` ist derselbe Installer als Textprogramm. Die Schaltfläche „Durchsuchen“ für den X-Plane-Pfad ruft `zenity` oder `kdialog` auf; auf einem minimalen Desktop ohne beides lässt sich der Pfad direkt eintippen. Das Linux-Paket ist ausschließlich für x86_64 gebaut, einen ARM-Build gibt es nicht.

!!! warning "Nach den Wing-Mods installieren"

    Bei A319, A320 und A321 hängen die Lichtpositionen von der Flügelgeometrie ab. Sowohl der [Durantula-Mod](durantula_wing_mod.md) als auch [RealWings](realwings.md) werden unterstützt, Photon muss aber zu dem Flügel passen, der tatsächlich gezeichnet wird — bei RealWings patcht der Installer dessen eigene Lichtobjekte, bei Durantula spielt er eine für diesen Flügel gebaute Variante ein — und deshalb **nach** dem Wing-Mod laufen. Wird ein Wing-Installer später erneut ausgeführt, ist auch der Photon-Installer erneut fällig.

!!! warning "Ein ToLiss-Update entfernt den Mod"

    Die Beleuchtung steckt in den OBJ-Dateien des Flugzeugs, und ein ToLiss-Update über den SkunkCraftsUpdater spielt diese im Originalzustand zurück. Der Installer erkennt das — er schreibt eine Versionsmarkierung in die OBJ und prüft, ob sie noch vorhanden ist —, nach jedem Flugzeug-Update muss der Mod aber neu installiert werden. Die Originaldateien liegen unter `Photon Backup Files/` im Flugzeugordner.

Gus Rodrigues' [A320 Family Light Mod](https://forums.x-plane.org/files/file/93337-a320-light-mod/) muss für das Cockpit nicht separat installiert werden — dieser Teil kommt mit Photon. Wird sein Paket anschließend von Hand installiert, überschreibt es die Außenlichter von Photon, da es ein eigenes Lichtobjekt mitbringt; bei der Außenbeleuchtung sind die beiden Mods Alternativen, kein Stapel.

!!! tip "Performance"

    Das Plugin bringt ein eigenes Werkzeug zur Performance-Analyse mit, erreichbar über den Einstellungs-Tab seines Fensters. Es misst das Cockpit mit jedem Effekt von Photon einzeln abgeschaltet — was ein Feature an Frames kostet, lässt sich damit auf der Maschine ermitteln, die es tatsächlich rendern muss, statt fremde Zahlen zu übernehmen.

## Quellen

- [ToLiss Photon — forums.x-plane.org](https://forums.x-plane.org/files/file/100717-toliss-photon-complete-lighting-mod-for-toliss-a330a319a320a321/)
- [toliss-photon-lighting — GitHub](https://github.com/ischmal/toliss-photon-lighting) — Quellcode, Readme und Releases
