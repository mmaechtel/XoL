---
description: "XPME streamt Satellitenbilder über ein virtuelles Dateisystem in X-Plane 12 — Linux-Einrichtung, Gratis- gegen Pro-Stufe und Einordnung."
---
# XPME (X-Plane Map Enhancement)

**X-Plane Map Enhancement (XPME)** ist eine dritte Streaming-Lösung neben [AutoOrtho](autoortho.md) und [XEarthLayer](xearthlayer.md). Es lädt Satellitenbilder zur Laufzeit und setzt sie an die Stelle der Bodentexturen von X-Plane, erfüllt also dieselbe Aufgabe wie die beiden etablierten Werkzeuge: weltweite [Orthofoto](../../glossary.md#orthofotos)-Abdeckung, ohne die Kacheln vorher offline zu erzeugen. Entwickler ist `derekhe`, Dokumentation und Bestellformular liegen auf `aiflygo.com`; die Anwendung ist Closed Source, GitHub dient nur der Auslieferung der Release-Binaries.

XPME ist eine Produktfamilie für zwei Simulatoren — Microsoft Flight Simulator und X-Plane. Nur die X-Plane-Seite ist hier von Belang, und sie hat eine eigene Dokumentation, eigene Basispakete und eine eigene Lizenz.

Der entscheidende Unterschied zu den Alternativen ist das Lizenzmodell. XPME ist Freemium: Die kostenlose Stufe ist benutzbar, aber gedeckelt, und ausgerechnet die Eigenschaften, die man mit Ortho-Streaming verbindet — hochauflösende Bodentexturen und Vorabladen — liegen hinter einem kostenpflichtigen Abonnement. AutoOrtho und XEarthLayer sind kostenlos und quelloffen. Das ist kein Urteil über die Qualität, aber das Erste, was vor der Einrichtungsarbeit abzuwägen ist.

!!! warning "Pro ist ein Abonnement, kein Kauf"
    Das Bestellformular unter `k.aiflygo.com/purchase` weist die Lizenz für X-Plane 12 mit **5 $ für 30 Tage** und **40 $ für 365 Tage** aus. Das Formular baut seine Preisanzeige dynamisch auf, die aktuellen Beträge sind also dort vor dem Bezahlen zu prüfen. Eine dauerhafte Lizenz gibt es nicht.

    Eine Lizenz gilt für genau einen PC und ist an die Hardware gebunden — ein Wechsel von CPU oder Datenträger sowie eine Neuinstallation des Systems können sie ungültig machen. Laut Anbieter lässt sich eine Lizenz mit Benutzernamen und Kauf-E-Mail auf ein neues Gerät umziehen. Die kommerzielle Nutzung ist ohne ausdrückliche schriftliche Genehmigung untersagt. Die Zahlung läuft über PayPal oder Buy Me a Coffee. Die Lizenzbedingungen nennen eine Rückgabefrist: *„The refund period is 7 days after I sent out the license."*

## Funktionsweise

XPME hängt ein **virtuelles Dateisystem** in den Szenerie-Baum von X-Plane ein und beantwortet Texturzugriffe aus dem Netz statt von der Platte — nach demselben Prinzip, das unter [Wie Ortho-Streaming funktioniert](how_streaming_works.md) beschrieben ist. Welche Einhänge-Schicht je Plattform zum Einsatz kommt, verrät die Abhängigkeitsliste: WinFSP unter Windows, FUSE-T unter macOS und [FUSE](../../glossary.md#fuse-filesystem-in-userspace) 3 unter Linux. Die Bilddaten werden geholt, nach [DDS](../../glossary.md#dds-directdraw-surface) komprimiert und an den Simulator übergeben; die Dokumentation nennt die DDS-Konvertierung als Hauptquelle der CPU-Last.

Anders als AutoOrtho und XEarthLayer liest XPME das Gelände-[Mesh](../../glossary.md#mesh) nicht aus der Szenerie von X-Plane. Es liefert **Basispakete** mit — regionale [DSF](../../glossary.md#dsf-distribution-scenery-format)- und Terrain-Daten, erzeugt mit einem angepassten [Ortho4XP](../../glossary.md#ortho4xp)-Fork auf ZL16 — die dieselbe Rolle einnehmen wie die DSF/TER-Pakete bei XEarthLayer.

Die Basispakete lassen sich nicht von Hand installieren. Sie liegen auf Cloudflare und werden vom eingebauten Downloader geholt, der `aria2` als Übertragungs-Backend nutzt. Wer hinter restriktiven Netzen sitzt, wird auf einen HTTP-Proxy oder ein VPN verwiesen.

In der Oberfläche wählbare Kartenquellen sind Bing, ArcGIS, Google und Apple. Ein Wechsel der Quelle im Flug ist möglich, wirkt aber nicht sofort — X-Plane muss die betroffenen Texturen neu laden.

**Was nicht dokumentiert ist**

- **Cache-Architektur.** Die Einstellungen bieten einen leerbaren Bild-Cache, und die Dokumentation warnt vor langsamen Datenträgern, doch eine Beschreibung von Cache-Stufen, Dimensionierung oder Verdrängung ist nicht veröffentlicht.
- **Zoomstufen der Bilddaten.** ZL16 bezieht sich auf das Mesh in den Basispaketen. Für die gestreamten Bilddaten ist in keiner der beiden Stufen eine Zoomstufe genannt.
- **Was „hochauflösende Bodentexturen" bedeutet.** Die Pro-Eigenschaft ist nur werblich beschrieben; keine Auflösung, keine Zoomstufe, keine Zahlen.

Nichts davon lässt sich aus dem Verhalten von AutoOrtho oder XEarthLayer ableiten — die Umsetzungen haben nichts miteinander zu tun, und die von XPME ist nicht einsehbar.

---

## Kostenlose Stufe und Pro-Abonnement

Die Anbieter-FAQ ist bei der Aufteilung eindeutig:

| Aspekt | Kostenlos | Pro |
|---|---|---|
| Kartenquellen | ArcGIS, Bing, Google Maps | Weitere Quellen, höhere Bildqualität, häufigere Aktualisierungen |
| Einstellung der Bildqualität | Nur mittel | Hohe Qualitätsstufen verfügbar |
| Farbanpassung der Karte | Nein | Ja |
| Vorabladen | Nein | Ja |
| Hochauflösende Bodentexturen | Nein | Ja |
| Neue Funktionen | Später | Zuerst |
| Preis | Kostenlos | 5 $ / 30 Tage, 40 $ / 365 Tage, eine Lizenz pro PC |

Zwei Punkte wiegen schwerer als der Rest. **Vorabladen** ist das vom Anbieter selbst empfohlene Mittel gegen die beiden häufigsten Beschwerden — unscharfe Bilder und Ruckler, wenn Kacheln zu spät eintreffen — und es ist Pro vorbehalten. **Hochauflösende Bodentexturen** sind die Eigenschaft, die XPME überhaupt erst mit dem vergleichbar macht, was AutoOrtho und XEarthLayer kostenlos liefern. Die kostenlose Stufe ist daher eher als funktionsfähige Erprobung der Verarbeitungskette zu verstehen denn als Dauerzustand.

Das Geld kauft dabei Verpackung und Bequemlichkeit, nicht die Bilddaten: Das Urheberrecht an den Kartendaten liegt bei den Kartenanbietern, und der Anbieter erklärt das Werkzeug ausdrücklich als reines Unterhaltungsprodukt.

## Systemvoraussetzungen

| Voraussetzung | Detail |
|---|---|
| Betriebssystem | Linux x86_64 mit FUSE 3 |
| Simulator | X-Plane 12 (X-Plane 11 funktioniert bei manchen, wird aber nicht offiziell unterstützt) |
| Laufzeitumgebung | .NET-10-Laufzeit und ASP.NET-Core-10-Laufzeit |
| Download-Hilfsprogramm | `aria2` |
| Speicher | SSD für Basispakete und Cache — die Dokumentation rät ausdrücklich von Festplatten und externen Laufwerken ab |
| Internetverbindung | Schnell und latenzarm; der Client öffnet vorgabemäßig rund 200 parallele Verbindungen |
| Arbeitsspeicher | Reichlich Reserve; die Dokumentation beschreibt das Werkzeug als speicherintensiv und bietet in den erweiterten Einstellungen eine Option „Memory Optimization" |

Die Abhängigkeit von .NET 10 ist die, die zuerst zu prüfen ist. Die Distributionen paketieren .NET in sehr unterschiedlichem Takt, und unter Debian stable ist das Paket `dotnet-runtime-10.0` unter Umständen nicht aus den Standard-Paketquellen verfügbar — dann ist die Microsoft-Paketquelle oder ein Backport der Distribution nötig.

## Installation unter Linux

Zuerst die Abhängigkeiten installieren. Für Debian-basierte Systeme dokumentiert der Anbieter diesen Befehl:

```bash
sudo apt install libfuse3-dev aria2 dotnet-runtime-10.0 aspnetcore-runtime-10.0
```

Anschließend die Anwendung aus dem [Release-Repository](https://github.com/derekhe/xplane-map-enhancement-release/releases) holen. Für Linux gibt es ein `.AppImage` und ein `_amd64.deb`:

```bash
# Debian-Paket
sudo dpkg -i xplane-map-enhancement_<version>_amd64.deb

# oder AppImage — keine Installation, nur ausführbar machen
chmod +x xplane-map-enhancement-<version>.AppImage
./xplane-map-enhancement-<version>.AppImage
```

!!! warning "Linux-Builds erscheinen nicht in jedem Release"
    Nicht jedes Release bringt Linux-Dateien mit. Mehrere Releases enthalten nur die Windows-`.exe` und das macOS-`.dmg`, darunter auch neuere — `.AppImage` und `.deb` erscheinen in den meisten Releases, aber nicht verlässlich im jeweils neuesten. Vor dem Herunterladen die Dateiliste des Releases prüfen und notfalls auf das jüngste Release ausweichen, das einen Linux-Build enthält.

Nach dem ersten Start in den Einstellungen den **Pfad für die Basispakete** auf eine schnelle SSD legen und dann in der Ansicht „Downloader" die zu befliegenden Regionen auswählen und installieren. Die Downloads laufen nacheinander und können groß werden. Der Anbieter dokumentiert die Reihenfolge in beide Richtungen: XPME öffnen und auf „Start" drücken, bevor X-Plane startet, und beim Beenden zuerst X-Plane schließen, dann auf „Stop" — damit ist laut Anbieter sichergestellt, dass alle Vorgänge des Werkzeugs sauber aufgeräumt werden.

## Bekannte Einschränkungen unter Linux

Nur das, was der Anbieter dokumentiert oder die Release-Historie belegt:

- **Unregelmäßige Linux-Builds.** Siehe den Hinweis oben. Es gibt keine Zusage für eine Linux-Datei pro Release, ein Update kann also bedeuten, eine Weile auf einer älteren Version zu bleiben.
- **Windows-zentrierte Dokumentation.** Einrichtungsanleitungen, FAQ und Fehlerbehebung sind für Windows geschrieben. Hinweise zu WinFSP, NTFS-Anforderungen, Virenscanner-Ausnahmen und Auslagerungsdatei betreffen Linux nicht und haben dort keine dokumentierte Entsprechung. Der Kern des Auslagerungsdatei-Hinweises gilt allerdings auch hier: Das Werkzeug braucht Speicherreserve.
- **Szenerie-Konflikte.** Ortho4XP und X-Plane HD Mesh Scenery überschreiben die Basispakete von XPME und sind als bekannte Konflikte benannt — sie müssen entfernt oder deaktiviert werden. XPME mit vorhandenen [statischen Kacheln](static_plus_streaming.md) zu mischen wird also nicht so unterstützt wie bei AutoOrtho oder XEarthLayer.
- **Hohe CPU-Last beim Laden ist zu erwarten.** Der Anbieter erklärt, X-Plane 12 sei für diese Art des Texturaustauschs nicht ausgelegt und die Bildverarbeitung samt DDS-Konvertierung von Natur aus aufwendig. Vorabladen mit eingeschalteten hochauflösenden Texturen wird ausdrücklich als möglicher Auslöser für schlechtere Simulator-Leistung genannt.
- **Basispakete lassen sich nicht von Hand installieren.** Erreicht der eingebaute Downloader die auf Cloudflare liegenden Pakete nicht, ist das dokumentierte Mittel ein Proxy oder ein VPN — einen Offline-Weg gibt es nicht.
- **Gemeldete Linux-Probleme** im Issue-Tracker des Projekts betreffen unter anderem eine FUSE-Einhängeoption, die die lokale Bibliothek ablehnt (`fuse: unknown option '-o max_threads=200'`), sowie ein Exit-Code-Problem unter Arch Linux. Der Tracker ist die nützlichste Stelle für einen Blick vor der Installation; der X-Plane-Forumsthread blockt automatisierte Abrufe, es stützt sich hier nichts darauf.

---

## Vergleich mit AutoOrtho und XEarthLayer

| Dimension | XPME | AutoOrtho | XEarthLayer |
|---|---|---|---|
| Quellcode | Geschlossen | Offen (Apache-2.0) | Offen (MIT) |
| Kosten | Kostenlose Stufe gedeckelt, Pro im Abo | Kostenlos | Kostenlos |
| Plattform | Windows, macOS, Linux | Windows, Linux, macOS (Apple Silicon) | Nur Linux |
| Einhänge-Schicht | WinFSP / FUSE-T / FUSE 3 | FUSE | FUSE |
| Geländedaten | Eigene Basispakete (Ortho4XP-basiert, ZL16), eingebauter Downloader | Nutzt die X-Plane-Szenerie plus Overlay-Downloads | DSF/TER-Pakete über `xearthlayer packages install` |
| Kartenquellen | Bing, ArcGIS, Google, Apple (drei davon in der kostenlosen Stufe) | Bing, Google, Here, Yandex, Apple | Bing, Google, Apple, ArcGIS, MapBox, USGS |
| Zoomstufe der Bilddaten | Nicht dokumentiert | Bis ZL18 | Anbieterabhängig |
| Cache | Nicht dokumentiert (über die Oberfläche leerbar) | Größe konfigurierbar, automatische Verdrängung | Dreistufig, konfigurierbar |
| Konfiguration | [GUI](../../glossary.md#gui-graphical-user-interface) | GUI | CLI und `config.ini` |
| Mit Ortho4XP-Kacheln kombinierbar | Nein — dokumentierter Konflikt | Ja | Ja |

**Welches System passt besser?**

- **Linux-Nutzer, die maximale Kontrolle wollen**: XEarthLayer und AutoOrtho sind offen, kostenlos, bis auf Thread-Zahlen und Cache-Stufen einstellbar, und ihr Verhalten lässt sich nachvollziehen, wenn etwas schiefgeht. XPME bietet davon nichts — sein Innenleben ist undokumentiert, und seine Linux-Builds sind nicht je Release zugesichert.

- **Nutzer, die bereits Ortho4XP-Kacheln pflegen**: XPME ist das falsche Werkzeug. Ortho4XP ist ein dokumentierter Konflikt und muss weichen, während [statische Kacheln mit Streaming zu kombinieren](static_plus_streaming.md) bei den anderen beiden ein unterstützter Arbeitsablauf ist.

- **Nutzer mehrerer Simulatoren**: XPME ist das einzige der drei, das auch den Microsoft Flight Simulator abdeckt. Beide Seiten sind getrennte Anwendungen mit eigenen Lizenzen und eigenen Basispaketen — es ist also ein Anbieter und eine Arbeitsweise, keine gemeinsame Installation. Für beide Simulatoren zugleich bleibt es hier trotzdem die einzige Möglichkeit.

---

## Weiterführende Kapitel

| Thema | Seite | Schwerpunkt |
|---|---|---|
| AutoOrtho | [AutoOrtho](autoortho.md) | Kostenloses Streaming mit breiter Plattformunterstützung |
| XEarthLayer | [XEarthLayer](xearthlayer.md) | Rust-basiertes Linux-Streaming mit GPU-Encoding |
| Funktionsweise Streaming | [Wie Ortho-Streaming funktioniert](how_streaming_works.md) | Kette DSF → .ter → DDS, FUSE-Abfangen, Caching |
| Ortho4XP | [Ortho4XP](../orthophotography/ortho4xp.md) | Statische Ortho-Kacheln offline erzeugen |
| Statisch + Streaming | [Statisch + Streaming](static_plus_streaming.md) | Lokale Kacheln mit Streaming kombinieren |
| Dateisystem | [Dateisystem](../../linux/optimizations/filesystem.md) | I/O-Abstimmung für Basispakete und Cache |

---

## Quellen

- [X-Plane Map Enhancement Releases](https://github.com/derekhe/xplane-map-enhancement-release/releases)
- [Download und Installation](https://www.aiflygo.com/docs/xplane-map-enhancement/download/) — AIFlyGo
- [Anwendung und Konfiguration](https://www.aiflygo.com/docs/xplane-map-enhancement/usage/) — AIFlyGo
- [FAQ](https://www.aiflygo.com/docs/xplane-map-enhancement/faq/) — AIFlyGo
- [Lizenzbedingungen](https://www.aiflygo.com/docs/license/) — AIFlyGo
- [Bestellformular](https://k.aiflygo.com/purchase) — AIFlyGo
