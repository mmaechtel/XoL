---
description: "AutoHaze ist ein FlyWithLua-Skript für X-Plane 12, das den Standard-Dunst durch Trübung aus echten Satelliten-Aerosol- und Wetterdaten ersetzt."
---
# AutoHaze — Dunstkorrektur mit Echtdaten

AutoHaze ist ein [FlyWithLua](../scripting/flywithlua.md)-Skript, das sich des gleichförmigen Dunstes annimmt, den [X-Plane](../../glossary.md#x-plane) 12 an klaren Tagen zeigt. Statt eines festen Standard-Trübungswerts leitet es den Dunst aus gemessenen Atmosphärendaten für die tatsächliche Flugzeugposition ab — Satelliten-Aerosolwerte, Bodenwetter und Grenzschichthöhe.

## Hintergrund

- **Entwickler:** MrBitsy
- **Download:** [forums.x-plane.org](https://forums.x-plane.org/files/file/99665-autohaze/)
- **Plattformen:** Windows, macOS, Linux (eine Helper-Binary je Plattform)
- **Kompatibilität:** X-Plane 12
- **Abhängigkeit:** [FlyWithLua NG+](../scripting/flywithlua.md), kostenlose API-Schlüssel für die Online-Abfragen
- **Lizenz:** Kostenloser Download, Spendenlink auf der Download-Seite

## Das Problem

Nach Angaben des Entwicklers leitet X-Plane 12 den Dunst vorrangig aus der METAR-Sichtweite ab. Ein METAR deckelt diesen Wert — bei 9999 m nach ICAO, bei 10 Statute Miles in den USA. Sobald die Bedingungen besser sind als die Obergrenze, erhält der Simulator also keinen brauchbaren Sichtwert mehr und fällt auf eine Standard-Trübung zurück. Das Ergebnis ist derselbe milchige Himmel über der Mojave-Wüste wie über der indogangetischen Tiefebene, und er dünnt mit der Höhe nicht aus: Der Blick in FL300 wirkt so trüb wie der in geringer Höhe.

## Datenquellen

AutoHaze fragt mehrere Dienste ab und rechnet deren Messwerte in einen Trübungswert um:

| Quelle | Liefert | Wirkung |
| --- | --- | --- |
| CAMS (Copernicus) | Satellitengemessene Aerosol-optische Dicke an der Flugzeugposition | Regionale Unterschiede — klare Luft über Kalifornien vs. dichter Dunst über Nordindien |
| VisualCrossing / OpenWeatherMap | Bodensicht, Luftfeuchte, Temperatur, Taupunkt, Wind | Feinabstimmung für bodennahe Bedingungen |
| Open-Meteo | Reale Grenzschichthöhe | Dunst dünnt im Steigflug aus |

Die Umrechnung nutzt die Koschmieder- und Linke-Trübungsgleichungen statt einer empirischen Wertetabelle.

## Funktionsumfang

- **Positionsabhängiger Dunst:** Die Trübung folgt dem Flugzeug, nicht einem globalen Standardwert
- **Höhenskalierung:** Oberhalb der realen Grenzschicht geht der Dunst in klare Luft über
- **Regenkopplung:** Die Sicht ändert sich mit der Regenmenge am Flugzeug, statt während eines Schauers fest zu bleiben
- **Weiche Übergänge:** Trübungsänderungen werden immer überblendet, nie sprunghaft gesetzt
- **Hintergrund-Helper:** Alle HTTP-Abfragen laufen in einem eigenen Helper-Prozess, dadurch blitzt kein Konsolenfenster auf und der Simulator pausiert nicht
- **Persistente Einstellungen:** CAMS-Vorgabe und Abfrageintervall werden beim Start aus dem letzten manuellen Speicherstand wiederhergestellt
- **Tastenkürzel:** Das AutoHaze-Fenster lässt sich unter *Settings → AutoHaze* auf eine Tastenkombination legen

## Mehrwert in der Flugsimulation

Dunst ist ein zentraler Entfernungshinweis, und X-Plane 12 liegt ausgerechnet in der häufigsten Situation daneben — bei Sichtweiten oberhalb der METAR-Obergrenze. In der Praxis geht die Korrektur meist in eine Richtung: An wirklich klaren Tagen verschwindet der Standard-Dunstschleier und die Sicht öffnet sich. Über Regionen mit hoher Aerosolbelastung oder in feuchter bodennaher Luft schlägt sie andersherum aus und wird dichter als der Default. Das Herausteigen aus der Dunstschicht in die klare Luft wird damit zu einem sichtbaren Ereignis statt zu einer Dauerkulisse. AutoHaze setzt am Dunst an; die Wetterlage selbst kommt von X-Plane oder aus einer Quelle wie [NOAA Weather](../scenery_addons/noaa_weather.md). Wie sich beide zusammen verhalten, dokumentiert keine der Quellen, und beide schreiben auf sichtbezogene Werte — beim Parallelbetrieb also ein Auge darauf haben. [X-ProTurb](xproturb.md) folgt derselben Idee, einen Effekt aus echten Atmosphärendaten abzuleiten, wirkt aber auf die Turbulenz und überschneidet sich nicht.

## Installation

**Download:** [forums.x-plane.org](https://forums.x-plane.org/files/file/99665-autohaze/)

Das Paket wird als ZIP-Archiv ausgeliefert und enthält das Skript, die Installationsanleitung und den Helper für alle drei Plattformen. Archiv entpacken und den Inhalt nach `Resources/plugins/FlyWithLua/Scripts/` kopieren — alle Dateien können dort liegen bleiben, AutoHaze lädt den zum Betriebssystem passenden Helper.

!!! warning "ZIP entpacken, keine Einzeldateien laden"

    Das ZIP-Paket existiert genau dafür, die Dateinamen der macOS- und Linux-Helper zu erhalten. Beim Einzeldownload können sie sich ändern, und AutoHaze findet den Helper für das laufende System dann nicht mehr.

!!! note "Linux-Besonderheiten"

    Offizieller Linux- und macOS-Support besteht ab Version 2.4; der Entwickler schreibt ausdrücklich, dass er weder ein Mac- noch ein Linux-System besitzt und auf Rückmeldungen angewiesen ist. Zwei spätere Korrekturen sind unter Linux relevant: Der Helper löst sich inzwischen sauber von X-Plane, sodass ein Absturz des Simulators nicht mehr Teile davon am Entladen hindert, und die Helper-Binaries bringen CA-Zertifikate mit, was die SSL-Fehler behebt, die einige Distributionen bei den API-Abfragen erzeugt haben. Sein Protokoll schreibt der Helper nach `AutoHaze-helper.log` im FlyWithLua-Verzeichnis — die erste Anlaufstelle, wenn keine Daten ankommen.

Der Live-Modus benötigt kostenlose API-Schlüssel für die Wetterdienste. Der Entwickler vermerkt, dass die HTTP-Abfragen über Python laufen und unter Windows 10 und neuer keine Zusatzsoftware nötig ist; eine entsprechende Aussage für Linux fehlt in der Quelle, ob der Linux-Helper also eine eigene Laufzeitumgebung mitbringt oder ein System-Python erwartet, ist nicht dokumentiert. Auf jeder für X-Plane genutzten Distribution ist Python ohnehin vorhanden.

## Quellen

- [AutoHaze — forums.x-plane.org](https://forums.x-plane.org/files/file/99665-autohaze/)
