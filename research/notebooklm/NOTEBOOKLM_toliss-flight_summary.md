# Vom Briefing bis zum Gate — Ein Flug mit dem ToLiss-Airbus und seinen Plugins

## Flugplanung

Ein Flug beginnt nicht im Cockpit, sondern am Schreibtisch. In SimBrief wird die Route geplant, Treibstoff berechnet, Wind und Wetter berücksichtigt. Das Ergebnis ist ein Operational Flight Plan, kurz OFP, wie ihn echte Airlines verwenden. Soweit nichts Ungewöhnliches. Die Toliss Airbusse können dies automatisch an die Maschine übertragen lassen. Die Schnittstelle von simbrief zu weiteren Plugins die im weiteren besprochen werden stellt darüber hinaus das Plugin simbrief_hub von hotbos dar.

Das AviTab selbst ist dabei weit mehr als ein PDF-Viewer.AviTab-Browser zeigt die aktuelle Position auf Navigraph-Charts für den Taxi und Anflug. Wer parallel auf einem zweiten Monitor mit LittleMap arbeiten möchte, nutzt Little XpConnect. Dieses Plugin überträgt alle Flugdaten an Little Navmap, ein externes Navigationsprogramm.

## Cockpit und Vorbereitung

Bevor der erste Schalter umgelegt wird, kümmert sich ToLiss Init um die Grundeinstellung. Das FlyWithLua-Skript wartet, bis beide Batterien aktiviert sind, und wendet dann nach etwa fünfzehn Sekunden die persönlichen Cockpit-Präferenzen an. ND-Modus, ND-Reichweite, Marker Beeps, externe Stromversorgung und mehr, alles wird automatisch so eingestellt, wie man es bevorzugt. FlyWithLua ist dabei das unsichtbare Fundament: Eine Lua-Scripting-Engine, die zahlreichen ToLiss-Erweiterungen überhaupt erst die Grundlage gibt.

XCamera ersetzt derweil das Standard-Kamerasystem von X-Plane durch etwas deutlich Flexibleres. Für jeden Flugzeugtyp lassen sich eigene Kamerapositionen definieren, und die Community teilt ihre besten Konfigurationen. Bezier-Kurven sorgen für cinematische Übergänge zwischen den Ansichten, ein Walk Mode erlaubt freie Bewegung durch die Kabine, und die G-Loaded Camera ersetzt die frühere Cinema Verite Funktion durch ein verbessertes Bewegungsgefühl. Wer ein Head-Tracking-System nutzt, kann es über OpenTrack direkt einbinden.

Für das Multi-Monitor-Setup kommt XTextureExtractor zum Einsatz. Dieses Plugin extrahiert die Cockpit-Instrumente als Texturen und streamt sie über das Netzwerk auf externe Displays. Das Navigation Display auf einem Tablet neben dem Monitor, die Engine-Anzeigen auf einem Raspberry Pi, das alles ist möglich. Über vierzig Flugzeuge werden mit vorkonfigurierten Definitionen unterstützt, darunter die gesamte ToLiss-Flotte.

Und falls das Wetter winterlich ist, sorgt der Windshield Icing Mod dafür, dass die Frontscheibe realistisch vereist. Ein kleines Detail, das die Immersion spürbar erhöht.

## Boarding und Bodendienste

Jetzt wird es lebendig auf dem Vorfeld. TOBUS, ein weiteres FlyWithLua-Skript aus dem ToLiss-Ökosystem, simuliert das Boarding der Passagiere. In Echtzeit steigt das Gewicht des Flugzeugs, der Schwerpunkt verschiebt sich, und man kann zwischen drei Geschwindigkeitsmodi wählen: Real für geduldige Piloten, Fast für den Normalflug und Instant für die Eiligen.

Parallel dazu arbeiten die ToLiss Ground Services. Dieses Skript verwaltet automatisch Bremsklötze und externe Stromversorgung, und zwar in beide Richtungen. Nach der Landung erkennt es anhand der angezogenen Parkbremse und niedriger Triebwerksdrehzahl, dass das Flugzeug steht. Automatisch werden die Chocks gesetzt und die Ground Power Unit angeschlossen. Beim Abflug ist es umgekehrt: Sobald die APU, also die Auxiliary Power Unit, bereit ist und die Türen geschlossen sind, werden die Bremsklötze entfernt und die externe Stromversorgung getrennt. Das klingt simpel, aber genau diese Automatismen machen den Unterschied zwischen einer Simulation und einem Erlebnis.

Über openSAM fährt die Fluggastbrücke ans Flugzeug. Dieses Open-Source-Plugin von hotbso liest die SAM-Definitionen der Szenerie und animiert die Jetways entsprechend. Währenddessen spielt ToLiss Announcements die passenden Kabinendurchsagen ab, vom Willkommensgruß bis zu den Sicherheitshinweisen.

## Pushback und Rollen

Die Türen sind geschlossen, die Freigabe ist erteilt, Zeit für den Pushback. Better Pushback zeigt eine Overhead-Ansicht des Flughafens, in der sich die Pushback-Route per Mausklick planen lässt. Kurven, Geraden, der Endpunkt, alles wird vorab definiert. Ein dreidimensionaler Schlepper dockt am Bugfahrwerk an, und der Pushback läuft vollautomatisch. Der Pilot kann sich währenddessen auf das Triebwerkstarten konzentrieren. Der empfohlene Fork von olivierbutler fügt zusätzlich einen manuellen Modus und Magic Squares für Schnellzugriffe hinzu.

Nach dem Pushback folgt das Rollen zur Startbahn, und hier zeigt Follow the Greens sein Können. Dieses Plugin simuliert ein A-SMGCS, ein Advanced Surface Movement Guidance and Control System, wie es auf großen Flughäfen wie München, London Heathrow oder Dubai im Einsatz ist. Grüne Mittellinienlichter leuchten progressiv auf und zeigen den Weg. An Kreuzungen halten rote Stop Bars das Flugzeug an, bis die Route frei ist. Besonders beeindruckend ist das Geschwindigkeitsmanagement der vierten Ausbaustufe: Eine Lichtsequenz wandert schneller oder langsamer über den Boden und signalisiert dem Piloten, ob er beschleunigen oder bremsen soll. Der Algorithmus berücksichtigt dabei Rollbahnbreiten und Einbahnregelungen.

## Start und Reiseflug

Auf der Startbahn übernehmen die V-Speed Callouts die operationellen Ansagen: Spoiler-Bestätigung, Reverse Green, Bremsansagen und die Geschwindigkeitsmarke bei siebzig Knoten. Bei der Landung melden sie Fahrwerk, Klappen und Geschwindigkeit. Parallel dazu meldet sich der Pilot Monitoring Callout, kurz PMCO, mit den standardisierten Ansagen des Pilot Monitoring. Verschiedene Stimmpakete stehen zur Wahl, männlich und weiblich, alle konform zu den Airbus-Standardprozeduren.

Wer noch mehr Unterstützung im Cockpit möchte, installiert Speedy Copilot. Dieses umfangreichere Skript simuliert einen kompletten Ersten Offizier mit eigenem Handbuch und Stimmpaketen aus fünf Ländern.

Draußen vor dem Fenster zeigt LiveTraffic echten Flugverkehr. Das Plugin empfängt ADS-B Daten, also Automatic Dependent Surveillance Broadcast, von kostenlosen Quellen wie adsb.fi und stellt die realen Flugzeuge mit korrekten Kennungen und Routen dar. Auf dem TCAS-Display, dem Traffic Collision Avoidance System, im Cockpit erscheinen die anderen Maschinen als Verkehrspunkte, genau wie im echten Flugzeug. Dreidimensionaler Sound simuliert vorbeifliegende Triebwerke, und das System berechnet sogar Start- und Landezeitpunkte der umliegenden Flugzeuge.

In der Reiseflughöhe bietet sich ein Blick auf die AviTab Moving Map an, während XCamera die Außenansicht aus verschiedenen Perspektiven zeigt. Little Navmap auf dem zweiten Monitor verfolgt den Fortschritt entlang der Route.

## Anflug, Landung und Docking

Der Sinkflug beginnt, und die Atmosphäre im Cockpit verdichtet sich. AviTab zeigt jetzt die Approach Charts für den Zielflughafen, während Little Navmap auf dem zweiten Monitor die verbleibende Distanz herunterzählt. PMCO meldet die Höhenmarken und Konfigurationsänderungen. Fahrwerk ausgefahren, Klappen gesetzt, Landebahn in Sicht.

Nach dem Aufsetzen analysiert XGS die Landequalität. Sinkrate in Fuß pro Minute, G-Kräfte, Aufsetzgeschwindigkeit, Aufsetzentfernung von der Schwelle, seitliche Abweichung von der Mittellinie, alles wird erfasst und bewertet. Für ToLiss-Flugzeuge nutzt XGS sogar einen speziellen Erkennungsmodus über die Kompression der Hauptfahrwerkstreben, was besonders präzise Ergebnisse liefert. Eine konfigurierbare Bewertungsskala gibt Rückmeldung, von einer butterweichen Landung bis hin zur harten Landung, die eine Inspektion erfordert.

Alternative kann auch die KI den kompletten Flug über "My FS Flights" analysieren.

Follow the Greens leitet danach zum zugewiesenen Gate. Dort übernimmt das Visual Docking Guidance System. AutoDGS bietet an über fünftausend Flughäfen automatische Einweisung, wahlweise als animierter Marshaller am Boden oder als elektronisches Safedock-Display. Alternativ stellt openSAM an Szenerien mit SAM-Unterstützung die gleiche Funktionalität bereit. Beide Systeme zeigen Azimut und verbleibende Rollstrecke bis zur Parkposition an.

Ist die Position erreicht, fährt die Fluggastbrücke heran, die Bremsklötze werden gesetzt, die Ground Power Unit angeschlossen. TOBUS startet das Deboarding, und die Kabinendurchsagen verabschieden die Passagiere.

## Das Zusammenspiel

Was diesen Flug besonders macht, ist nicht das einzelne Plugin. Jedes für sich löst ein konkretes Problem, vom Pushback über die Rollwegführung bis zur Landeanalyse. Aber zusammen erzählen sie eine Geschichte. Die Flugplanung fließt nahtlos ins Cockpit, die Bodendienste reagieren auf den Flugzustand, die Callouts begleiten jeden Flugabschnitt, und am Ende steht eine detaillierte Auswertung der Landung.

Bemerkenswert ist dabei, wie viele dieser Plugins von einer kleinen Gruppe von Entwicklern stammen. hotbso allein verantwortet den SimBrief Connector, AutoDGS, openSAM und XGS. Das ToLiss-Ökosystem mit seinen FlyWithLua-Skripten wird von der Community gepflegt und erweitert. Und das Beste daran: Fast alle diese Erweiterungen sind kostenlos und quelloffen.

Man startet vielleicht mit einem oder zwei Plugins und merkt schnell, wie jede weitere Ergänzung den Flug ein Stück realistischer macht. Es ist nicht ein einzelner großer Moment, sondern die Summe vieler kleiner Details, die aus einer Flugsimulation ein Erlebnis machen. Vom Briefing bis zum Gate, jeder Abschnitt hat seine eigenen Helfer, und zusammen verwandeln sie den ToLiss-Airbus in etwas, das sich erstaunlich nah an der Realität anfühlt.
