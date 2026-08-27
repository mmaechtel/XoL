---
description: "XPAIS Marine Traffic zeigt echten AIS-Schiffsverkehr aus dem AISStream-Feed in X-Plane 12 — natives Linux-Plugin, quelloffen, seit Juli 2026 archiviert."
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

    Nicht zu verwechseln mit dem ähnlich benannten **XP AIS-Traffic** von nestasko in den X-Plane.org-Foren: ein eigenständiges Projekt, das als unterstützte Plattform X-Plane 12 und Windows 64-bit nennt. Der Autor bezeichnet Linux- und macOS-Unterstützung als fest eingeplant, ohne Termin — Stand August 2026 existiert kein Linux-Build.

## Funktionsweise

Zwei Threads mit sauber getrennten Zuständigkeiten: `ais_client` hält die WebSocket-Verbindung über TLS und fasst die X-Plane-API nie an, während alles Simulator-seitige im Flight-Loop-Thread läuft. Für ein Plugin ist das die richtige Bauform — das SDK von X-Plane ist nicht thread-sicher, und Netzwerk-Jitter erreicht so nie die Frame-Schleife.

Schiffe werden **60 Sekunden hinter der Echtzeit** dargestellt. Das klingt nach einem Mangel und ist tatsächlich der ehrlichere Weg: Im eingeschwungenen Zustand interpoliert das Plugin zwischen zwei bekannten AIS-Positionen, statt eine geratene Position vorauszurechnen. Nur am vorderen Rand — direkt nachdem ein Schiff auftaucht oder wenn sein Feed stockt — rechnet es kurz und begrenzt voraus. Die Schiffe bewegen sich dadurch gleichmäßig und müssen nie springen, wenn die nächste Meldung einer Vorhersage widerspricht.

Die Rümpfe stammen aus X-Planes eigenen Standard-Schiffsobjekten, ausgewählt nach AIS-Typcode sowie nach gemeldeter Länge und Breite. [OpenSceneryX](https://www.opensceneryx.com/) ist optional, aber empfehlenswert: X-Plane 12 liefert keine Passagierschiff-Modelle mit, ohne die Bibliothek fallen Kreuzfahrtschiffe und Fähren auf einen allgemeinen Frachtrumpf zurück, kleine Passagierboote auf ein Yacht-Modell.

## Installation

Das Plugin wird aus dem Quellcode gebaut. Benötigt werden `cmake`, ein C++17-Compiler und die OpenSSL-Entwicklungsdateien — unter Debian:

```bash
sudo apt install cmake g++ libssl-dev
```

Das X-Plane-SDK liegt im Repository bei, ein separater Download entfällt — der Build holt allerdings IXWebSocket und nlohmann/json zur Configure-Zeit, benötigt also Netzzugang:

```bash
./build.sh            # baut nach dist/XPAISTraffic/
./build.sh install    # kopiert in die X-Plane-Installation
```

Zielverzeichnis ist `X-Plane 12/Resources/plugins/XPAISTraffic/`. Ein AISStream-API-Key ist zwingend — die Registrierung ist kostenlos — und wird in die `config.ini` eingetragen:

```ini
[AIS]
ApiKey=<Schlüssel>

[Logging]
Debug=true

[Display]
ShowTraffic=true
Labels=false
Wakes=false
HideNoHeading=false
OpenSceneryX=true
```

Ohne gültigen Schlüssel erscheinen keine Schiffe. Das Plugin protokolliert nach `logs/xpaistraffic.log` — die erste Anlaufstelle, wenn die Kontaktzahl bei null bleibt.

## Bedienung

Das Menü **Plugins → XP AIS Traffic** enthält die Laufzeit-Einstellungen samt aktueller Kontaktzahl. Rund um stark befahrene Häfen wird die groß — Tester meldeten etwa 3.000 Kontakte im Bereich EHAM.

| Menüpunkt | Wirkung |
|-----------|---------|
| Show traffic | Hauptschalter |
| Show labels | Schiffsname, Kurs und Geschwindigkeit über dem Schiff |
| Show wakes | Unfertig, vorgabemäßig aus |
| Hide vessels w/o heading (HDG 000) | Blendet Schiffe ohne gemeldeten Kurs aus |
| Use OpenSceneryX ships (if installed) | Bevorzugt die besseren Rümpfe, sofern vorhanden |
| Contacts: N | Laufende Zahl der verfolgten Schiffe — bei abgeschaltetem Verkehr steht dort `Contacts: (off)` |

Der HDG-000-Filter behebt eine Eigenheit der Daten: Ankernde und stillliegende Schiffe senden häufig weder True Heading noch Kurs über Grund und zeigen deshalb allesamt nach Norden. Der Filter ist standardmäßig aus, und der Entwickler benennt seine Grenze offen — AIS bietet keine Möglichkeit, „kein Kurs gemeldet" von „fährt tatsächlich nach Norden" zu unterscheiden, ein echtes Nordkurs-Schiff verschwindet also mit.

Kielwasser-Effekte sind vorhanden, aber standardmäßig aus, da sie nie fertiggestellt wurden. Sie referenzieren X-Planes eigene `wake.png`, statt sie zu kopieren.

!!! note "„Draw boats and balloons" abschalten"

    X-Planes eigener Schiffsverkehr ist positionsgeschlossen. Schreibbare Positions-Datarefs gibt es nur unter `sim/world/boat/*` mit `override_boats`, und die betreffen allein Träger und Fregatte — die Umgebungsboote lassen sich von außen nicht setzen, weshalb AIS-Schiffe auch deren prozedurales Kielwasser nicht erben können.

    X-Planes eigenen Verkehr eingeschaltet zu lassen, schadet aktiv: Seine synthetischen Boote haben nichts mit dem echten Verkehr zu tun und doppeln als Geister direkt neben den AIS-Schiffen. Die Schiffe des Plugins werden unabhängig davon instanziert und erscheinen unabhängig von dieser Einstellung.

    Die README im Repository sagt das Gegenteil — Einstellung anlassen. Der Entwickler hat das im Forum-Thread nachträglich korrigiert; die Korrektur ist die neuere Aussage.

## Grenzen

Zwei Punkte führt das Projekt als bewusste Entwurfsentscheidung und nicht als Mangel, weil sie auf einen Renderer für Live-AIS nicht zutreffen:

- **Keine Kollisionsvermeidung:** Schiffe erscheinen exakt dort, wo AIS sie verortet — auch ineinander
- **Kein Liegeplatz- oder Hafen-Skripting:** Alles kommt aus dem Live-Feed, nichts ist choreografiert

Die Lücken, die das Projekt selbst als Lücken benennt, sind andere: Passagierschiffe brauchen OpenSceneryX, um passend auszusehen, die Rümpfe der Autotransporter sind eine bewusste Mischung, und die Optik wurde im Simulator nie feinabgestimmt.

Zwei weitere Grenzen liegen an den Daten, nicht am Plugin:

- **Schwankende Abdeckung:** Die AIS-Qualität hängt von Transpondern, Küstenstationen und Satellitenempfang ab. Manche Regionen sind schlicht leer — Tester fanden in der Straße von Hormus überhaupt keine Daten
- **Datenqualität:** Gefälschte oder doppelte AIS-Einträge kommen vor und lassen sich vom Plugin nicht korrigieren

## Quellen

- [XPAIS-Marine-Traffic](https://codeberg.org/xbard/XPAIS-Marine-Traffic) — Repository, README und Bauanleitung (archiviert)
- [XPAIS Marine Traffic — Linux build](https://forums.x-plane.org/forums/topic/348448-xpais-marine-traffic-linux-build/) — Entwicklungs-Thread mit den Erläuterungen des Entwicklers
- [AISStream](https://aisstream.io/) — AIS-Datenquelle, Registrierung für den API-Key
