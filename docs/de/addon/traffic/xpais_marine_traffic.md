---
description: "XPAIS Marine Traffic stellt echten AIS-Schiffsverkehr aus dem AISStream-Feed in X-Plane 12 dar — ein nativer Linux-Plugin, quelloffen, seit Juli 2026 archiviert."
---
# XPAIS Marine Traffic

XPAIS Marine Traffic bringt echte Schiffe aufs Wasser. Das Plugin abonniert den Feed von [AISStream](https://aisstream.io/), empfängt die Positionsmeldungen, die Schiffe über AIS (Automatic Identification System) aussenden, und stellt sie in [X-Plane](../../glossary.md#x-plane) 12 an ihrer tatsächlichen Position dar — was [LiveTraffic](livetraffic.md) für den Flugverkehr leistet, macht XPAIS für die Seefahrt.

## Hintergrund

- **Entwickler:** CheckCanopy (xbard)
- **Repository:** [codeberg.org/xbard/XPAIS-Marine-Traffic](https://codeberg.org/xbard/XPAIS-Marine-Traffic) (quelloffen, GPL-3.0)
- **Plattform:** Linux (Bau aus dem Quellcode)
- **Kompatibilität:** X-Plane 12
- **Voraussetzung:** kostenloser AISStream-API-Key

!!! warning "Archiviert — keine Weiterentwicklung"

    Das Repository wurde am 2026-07-07 auf schreibgeschützt gesetzt, der letzte Commit stammt vom 2026-06-16. Der Code bleibt verfügbar und baubar, es wird aber weder Fehlerkorrekturen noch neue Funktionen geben. Wer das Plugin einsetzt, ist auf sich gestellt.

    Nicht zu verwechseln mit dem ähnlich benannten **XP AIS Traffic** von nestasko in den X-Plane.org-Foren: ein eigenständiges, quellgeschlossenes Projekt, dessen unterstützte Plattform ausschließlich Windows 64-bit ist. Der Autor führt Linux-Unterstützung als Roadmap-Punkt — Stand August 2026 existiert kein Linux-Build.

## Funktionsweise

Zwei Threads mit sauber getrennten Zuständigkeiten: `ais_client` hält die WebSocket-Verbindung über TLS und fasst die X-Plane-API nie an, während alles Simulator-seitige im Flight-Loop-Thread läuft. Für ein Plugin ist das die richtige Bauform — das SDK von X-Plane ist nicht thread-sicher, und Netzwerk-Jitter erreicht so nie die Frame-Schleife.

Schiffe werden **60 Sekunden hinter der Echtzeit** dargestellt. Das klingt nach einem Mangel und ist tatsächlich der ehrlichere Weg: Das Plugin interpoliert zwischen zwei bekannten AIS-Positionen, statt eine geratene Position vorauszurechnen. Die Schiffe bewegen sich dadurch gleichmäßig und müssen nie springen, wenn die nächste Meldung einer Vorhersage widerspricht.

Die Rümpfe stammen aus X-Planes eigenen Standard-Schiffsobjekten, ausgewählt nach AIS-Typcode sowie nach gemeldeter Länge und Breite. [OpenSceneryX](https://www.opensceneryx.com/) ist optional, aber empfehlenswert: X-Plane 12 liefert keine Passagierschiff-Modelle mit, ohne die Bibliothek fallen Fähren und Kreuzfahrtschiffe auf Yacht-Rümpfe zurück.

## Installation

Das Plugin wird aus dem Quellcode gebaut. Benötigt werden `cmake`, ein C++17-Compiler und die OpenSSL-Entwicklungsdateien — unter Debian:

```bash
sudo apt install cmake g++ libssl-dev
```

Das X-Plane-SDK liegt im Repository bei, ein separater Download entfällt:

```bash
./build.sh            # baut nach dist/XPAISTraffic/
./build.sh install    # kopiert in die X-Plane-Installation
```

Zielverzeichnis ist `X-Plane 12/Resources/plugins/XPAISTraffic/`. Ein AISStream-API-Key ist zwingend — die Registrierung ist kostenlos — und wird in die `config.ini` eingetragen:

```ini
[AIS]
ApiKey=<Schlüssel>

[Display]
ShowTraffic=true
Labels=false
OpenSceneryX=true
```

Ohne gültigen Schlüssel erscheinen keine Schiffe. Das Plugin protokolliert nach `logs/xpaistraffic.log` — die erste Anlaufstelle, wenn die Kontaktzahl bei null bleibt.

## Bedienung

Das Menü **Plugins → XP AIS Traffic** enthält die Laufzeit-Einstellungen samt aktueller Kontaktzahl. Rund um stark befahrene Häfen wird die groß — Tester meldeten etwa 3.000 Kontakte im Bereich EHAM.

| Menüpunkt | Wirkung |
|-----------|---------|
| Show traffic | Hauptschalter |
| Show labels | Schiffsname, Kurs und Geschwindigkeit über dem Schiff |
| Use OpenSceneryX ships | Bevorzugt die besseren Rümpfe, sofern vorhanden |
| Hide vessels w/o heading (HDG 000) | Blendet Schiffe ohne gemeldeten Kurs aus |
| Contacts: N | Laufende Zahl der verfolgten Schiffe |

Der HDG-000-Filter behebt eine Eigenheit der Daten: Ankernde und stillliegende Schiffe senden häufig weder True Heading noch Kurs über Grund und zeigen deshalb allesamt nach Norden. Der Filter ist standardmäßig aus, und der Entwickler benennt seine Grenze offen — AIS bietet keine Möglichkeit, „kein Kurs gemeldet" von „fährt tatsächlich nach Norden" zu unterscheiden, ein echtes Nordkurs-Schiff verschwindet also mit.

Kielwasser-Effekte sind vorhanden, aber standardmäßig aus, da sie nie fertiggestellt wurden. Sie referenzieren X-Planes eigene `wake.png`, statt sie zu kopieren.

!!! note "„Show ships and balloons" abschalten"

    X-Planes eigener Schiffsverkehr ist positionsgeschlossen: Er erzeugt synthetische Boote stochastisch entlang der Dichtekarte `shipping-lanes-for-boats.png` und steuert sie selbst. Es gibt kein öffentliches Dataref und keinen SDK-Aufruf, um ein Schiff an eine bestimmte Position zu setzen — AIS-Schiffe lassen sich dort also nicht einspeisen, weshalb sie auch das prozedurale Kielwasser nicht erben können.

    X-Planes eigenen Verkehr eingeschaltet zu lassen, schadet aktiv: Seine synthetischen Boote haben nichts mit dem echten Verkehr zu tun und doppeln als Geister direkt neben den AIS-Schiffen. Die Schiffe des Plugins werden unabhängig davon instanziert und erscheinen unabhängig von dieser Einstellung.

    Die README im Repository sagt das Gegenteil — Einstellung anlassen. Der Entwickler hat das im Forum-Thread nachträglich korrigiert; die Korrektur ist die neuere Aussage.

## Grenzen

Über den Archiv-Status hinaus benennt das Projekt seine Grenzen deutlich:

- **Keine Kollisionsvermeidung:** Schiffe erscheinen exakt dort, wo AIS sie verortet — auch ineinander
- **Kein Liegeplatz- oder Hafen-Skripting:** Alles kommt aus dem Live-Feed, nichts ist choreografiert
- **Schwankende Abdeckung:** Die AIS-Qualität hängt von Transpondern, Küstenstationen und Satellitenempfang ab. Manche Regionen sind schlicht leer — Tester fanden in der Straße von Hormus überhaupt keine Daten
- **Datenqualität:** Gefälschte oder doppelte AIS-Einträge kommen vor und lassen sich vom Plugin nicht korrigieren

## Quellen

- [XPAIS-Marine-Traffic](https://codeberg.org/xbard/XPAIS-Marine-Traffic) — Repository, README und Bauanleitung (archiviert)
- [XPAIS Marine Traffic — Linux build](https://forums.x-plane.org/forums/topic/348448-xpais-marine-traffic-linux-build/) — Entwicklungs-Thread mit den Erläuterungen des Entwicklers
- [AISStream](https://aisstream.io/) — AIS-Datenquelle, Registrierung für den API-Key
