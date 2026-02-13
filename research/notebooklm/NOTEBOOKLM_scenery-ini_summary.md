# Die scenery packs ini — Wie X-Plane die Welt zusammensetzt

## Warum diese Datei so wichtig ist

Wenn X-Plane startet und eine Landschaft aufbaut, dann sieht es die Welt nicht als ein einziges großes Ganzes. Stattdessen arbeitet der Simulator mit einem Stapel aus einzelnen Schichten. Jede Schicht liefert einen anderen Baustein: Die eine formt die Berge und Täler, die nächste legt Satellitenbilder darüber, eine weitere pflanzt Bäume und Häuser, und ganz oben kommen die handmodellierten Flughäfen. Welche Schichten geladen werden und in welcher Reihenfolge, das steuert eine einzige Textdatei: die scenery packs ini. Sie liegt im Ordner Custom Scenery des X-Plane-Verzeichnisses und ist im Grunde eine Prioritätenliste. Was weiter oben steht, hat Vorrang. Was weiter unten steht, bildet die Basis. Und genau diese Reihenfolge entscheidet darüber, ob die Landschaft korrekt dargestellt wird oder ob Flughäfen in der Luft schweben, Häuser auf Seen stehen oder Texturen sich gegenseitig überdecken.

## Die Bausteine der X-Plane-Welt

Bevor wir über die Reihenfolge sprechen, müssen wir verstehen, aus welchen Bausteinen X-Plane überhaupt eine Landschaft zusammensetzt. Im Kern sind es drei Hauptkomponenten.

Der erste Baustein ist das Mesh, also englisch für Netz oder Gitter. Das Mesh ist die dreidimensionale Grundform der Landschaft. Man kann es sich vorstellen wie eine riesige Decke aus kleinen Dreiecken, die über die Erde gelegt wird. Diese Dreiecke definieren, wie hoch ein Berg ist, wie tief ein Tal liegt und wie steil ein Hang abfällt. Ohne Mesh wäre die Welt einfach flach, wie ein Blatt Papier. Das Mesh liefert also die Struktur, aber noch keine Farben oder Details. Es ist wie der Rohbau eines Hauses: Die Wände stehen, aber es fehlt noch alles andere.

Der zweite Baustein sind die Orthos, also Orthofotografien. Das sind Luft- oder Satellitenbilder, die wie ein riesiges Foto auf das Mesh geklebt werden. Erst durch die Orthos sieht man Straßen, Felder, Wälder und Flüsse. Ohne Orthos wäre das Mesh nur eine graue, leblose Hügellandschaft. Die Standard-Orthos, die X-Plane mitliefert, sind recht grob. Deshalb nutzen viele Simmer zusätzliche Werkzeuge wie Ortho4XP oder Streaming-Lösungen wie AutoOrtho und XEarthLayer, um deutlich höher aufgelöste Satellitenbilder zu verwenden.

Der dritte Baustein ist das Autogen. Das steht für automatisch generiert und meint dreidimensionale Objekte, die X-Plane anhand von Datenquellen wie OpenStreetMap in die Landschaft setzt. In Wohngebieten erscheinen Häuser, in Waldgebieten Bäume, an Straßen Laternen und Leitplanken. Autogen bringt Tiefe und Leben in die ansonsten flache Satellitenansicht. Pakete wie SimHeaven X-World erweitern diese Funktion erheblich, mit regionalen Baustilen, korrekten Gebäudehöhen und detaillierten Vegetationszonen.

Diese drei Bausteine — Mesh, Ortho und Autogen — arbeiten zusammen wie Fundament, Tapete und Möbel. Und die scenery packs ini bestimmt, in welcher Reihenfolge X-Plane sie aufeinander stapelt.

## Die korrekte Reihenfolge

Jetzt wird es konkret. In der scenery packs ini steht jede Zeile für einen Szenerie-Ordner. Die Reihenfolge von oben nach unten bestimmt die Priorität: Was weiter oben steht, hat Vorrang und kann Einträge darunter überdecken. Das bedeutet: Die Basis, also die Schichten mit der niedrigsten Priorität, stehen ganz unten. Die speziellen, handgemachten Inhalte stehen ganz oben. Daraus ergibt sich eine logische Schichtung.

Weit unten stehen die Mesh-Dateien. Sie bilden das Fundament, die dreidimensionale Grundform der Erde. Alles andere baut darauf auf. Typische Einträge sind hier hochauflösende Mesh-Pakete wie HD Mesh oder spezielle Mesh-Dateien, die mit Flughafen-Szenerien mitgeliefert werden.

Eine Stufe darüber kommen die lokalen Ortho-Szenerien. Das sind die Satellitenbilder, die auf das Mesh gelegt werden. Sie brauchen das Mesh als Unterlage, müssen aber unter dem Autogen stehen, damit die dreidimensionalen Objekte korrekt darauf platziert werden können.

Darüber liegen die Autogen-Objekte und Bibliotheken. SimHeaven X-World zum Beispiel mit seinen europäischen Stadttexturen, Wäldern und Straßennetzen. Diese Schicht setzt Häuser, Bäume und andere Objekte auf die Kombination aus Mesh und Ortho.

Noch eine Stufe höher kommen spezielle Objekte wie Windräder, Sendemasten oder Stromleitungen. Sie sollen über dem allgemeinen Autogen sichtbar sein und nicht davon verdeckt werden.

Dann folgt der Eintrag Global Airports. Das ist ein spezieller Platzhalter, den X-Plane selbst verwaltet. Er enthält die Standard-Flughäfen, von denen viele über das X-Plane Gateway von der Community erstellt wurden. Dieser Eintrag muss über dem Autogen stehen, damit Flughäfen nicht von Häusern oder Bäumen zugebaut werden. Gleichzeitig muss er unter den Custom Sceneries stehen, damit handgemachte Flughafenpakete die Standard-Versionen ersetzen können.

Ganz oben in der Datei stehen die Custom Sceneries und Landmarks. Das sind detaillierte Flughafenpakete oder besondere Sehenswürdigkeiten wie der Eiffelturm in Paris. Sie haben die höchste Priorität, weil sie alles darunter überschreiben sollen. Ein detaillierter Flughafen wie das Aerosoft Frankfurt ersetzt damit automatisch den Standard-Flughafen aus dem Gateway.

Was passiert, wenn die Reihenfolge nicht stimmt? Die Fehler sind oft sofort sichtbar. Steht ein Mesh über einer Custom Scenery, kann der Flughafen plötzlich in der Luft schweben, weil das Mesh eine andere Geländehöhe definiert als der Flughafen erwartet. Steht das Autogen über dem Flughafen, wachsen Bäume mitten auf der Landebahn. Und wenn ein Ortho-Paket über einem Custom Airport steht, können die handmodellierten Texturen des Flughafens von den Satellitenbildern überdeckt werden. All das lässt sich vermeiden, wenn man die Schichtung versteht und einhält.

Wenn man sich diese Reihenfolge einprägen will, hilft ein einfaches Bild: Man baut von unten nach oben. Zuerst kommt das Mesh als Fundament. Dann die lokalen Satellitenbilder. Dann stellt man Möbel auf mit dem Autogen. Dann kommen besondere Bauwerke. Und ganz oben steht das Namensschild: der spezifische Flughafen, der alles darunter ersetzt. Ganz unten, noch unter dem Mesh, stehen die Ortho-Streaming-Dienste als Sicherheitsnetz.

## Warum Ortho-Streamer ganz nach unten gehören

Jetzt kommen wir zum vielleicht wichtigsten Punkt für alle, die Streaming-Lösungen wie AutoOrtho oder XEarthLayer nutzen. Diese Dienste laden Satellitenbilder in Echtzeit aus dem Internet herunter, während man fliegt. Sie brauchen eine stabile Internetverbindung und liefern Orthofotos für praktisch die ganze Welt, ohne dass man vorher etwas vorbereiten muss. Das klingt fantastisch, und das ist es auch. Aber wo gehören diese Streamer in der scenery packs ini hin?

Die Antwort lautet: ganz nach unten. Und zwar aus einem bestimmten Grund, der das Herzstück der ganzen Prioritätenlogik darstellt.

X-Plane arbeitet die scenery packs ini von oben nach unten durch. Wenn es für einen bestimmten Bereich der Welt einen Eintrag weiter oben findet, verwendet es diesen und ignoriert alles darunter für diesen Bereich. Das bedeutet: Wenn man lokale Ortho4XP-Kacheln für eine bestimmte Region hat und diese in der ini über dem Streaming-Dienst stehen, dann wird X-Plane immer die lokalen Kacheln verwenden. Die lokalen Daten haben Vorrang, sie sind ja weiter oben in der Prioritätenliste. Nur wenn X-Plane für einen bestimmten Bereich keine lokale Szenerie findet, arbeitet es sich weiter nach unten durch und landet schließlich beim Streaming-Dienst. Erst dann wird das Satellitenbild aus dem Internet geladen.

Genau das ist das Fallback-Prinzip. Der Ortho-Streamer ist das Sicherheitsnetz ganz unten. Alles Lokale, was darüber steht, wird bevorzugt. Erst wenn nichts Lokales vorhanden ist, springt der Streamer ein und liefert das Bild aus dem Netz. Das hat mehrere Vorteile. Die lokalen Kacheln, die man vielleicht aufwendig mit Ortho4XP in hoher Auflösung generiert hat, werden nie von den gestreamten Bildern überschrieben. Man behält die beste Qualität dort, wo man sie bewusst erstellt hat. Gleichzeitig hat man eine weltweite Abdeckung für alle anderen Gebiete, ohne Vorbereitung.

In der Praxis sieht das so aus: Man hat seine Heimatregion mit Ortho4XP in Zoomstufe siebzehn oder achtzehn generiert. Diese Kacheln stehen in der ini über dem Streaming-Eintrag. Fliegt man nun über die Heimatregion, sieht man die lokalen, hochauflösenden Bilder. Fliegt man dagegen spontan nach Griechenland oder Kanada, wo keine lokalen Kacheln existieren, greift X-Plane auf den Streaming-Dienst zurück und lädt die Bilder in Echtzeit herunter.

Es ist ein bisschen wie bei einem Navigationssystem im Auto: Wenn man eine detaillierte Offline-Karte für die Heimatstadt hat, nutzt das System diese. Für unbekannte Gebiete schaltet es auf die Online-Karte um. Genau so funktioniert das Zusammenspiel zwischen lokalen Ortho-Kacheln und dem Streaming-Dienst in X-Plane.

Die Overlays, also die Anpassungsschichten, die zum Beispiel die Einebnung von Flughafengeländen und Straßeninformationen enthalten, gehören dagegen über den Streaming-Eintrag. Auch hier gilt dasselbe Prinzip: Was oben steht, hat Vorrang.

## Statisch und Streaming kombinieren

Diese Schichtlogik ermöglicht eine besonders elegante Kombination, die viele erfahrene Simmer nutzen. Man generiert mit Ortho4XP lokale Kacheln für die Regionen, die man am häufigsten befliegt. Typischerweise sind das ein bis fünf Heimatflughäfen und vielleicht einige beliebte Streckenabschnitte. Diese lokalen Kacheln werden in hoher Zoomstufe erstellt, etwa siebzehn bis neunzehn, und liefern maximale Detailtreue. Sie brauchen keine Internetverbindung und sind sofort in voller Qualität verfügbar.

Für den Rest der Welt lässt man einen Streaming-Dienst arbeiten. AutoOrtho mit dem ProgrammingDinosaur Fork, oder XEarthLayer für Linux-Nutzer, liefern dann Satellitenbilder überall dort, wo keine lokalen Kacheln vorhanden sind. Beim ersten Überflug einer neuen Region werden die Bilder heruntergeladen und in einem lokalen Cache gespeichert. Fliegt man dieselbe Strecke später noch einmal, kommen die Bilder direkt aus dem Cache, ohne erneuten Download. Der Speicherverbrauch bleibt trotzdem überschaubar, weil der Streaming-Cache sich selbst verwaltet und alte, selten genutzte Kacheln automatisch entfernt, wenn der konfigurierte Speicherplatz erreicht ist. Im Gegensatz zu Ortho4XP, wo jede generierte Kachel dauerhaft auf der Festplatte bleibt, reguliert der Streaming-Cache seine Größe also von selbst.

In der scenery packs ini stehen dann die lokalen Ortho4XP-Kacheln über dem Streaming-Eintrag. So ist sichergestellt, dass X-Plane für die Heimatregion immer die lokalen Daten verwendet. Für alle anderen Gebiete fällt es automatisch auf den Streaming-Dienst zurück. Das ist das Beste aus beiden Welten: höchste Qualität zu Hause, spontane Abdeckung überall sonst.

Man kann sogar noch einen Schritt weitergehen. Ortho4XP kann nicht nur Texturen generieren, sondern auch hochauflösende Mesh-Daten, also präzisere Höhenmodelle. Diese Mesh-Daten lassen sich mit den gestreamten Texturen kombinieren, sodass man eine bessere Geländedarstellung erhält, ohne lokale Texturdaten speichern zu müssen. Besonders in Bergregionen wie den Alpen oder entlang von Küsten macht das einen spürbaren Unterschied.

## Zusammenfassung und Empfehlungen

Die scenery packs ini ist das Herzstück der Szenerie-Verwaltung in X-Plane. Sie bestimmt, wie der Simulator die Welt aus einzelnen Schichten zusammensetzt. Die goldene Regel lautet: Was oben steht, hat Vorrang. Custom Sceneries ganz oben, Global Airports und Autogen in der Mitte, lokale Orthos und Mesh weiter unten.

Streaming-Dienste für Orthofotos gehören ganz nach unten, unter alles andere, auch unter das lokale Mesh. So werden sie zum Sicherheitsnetz: Alles Lokale, das darüber eingetragen ist, wird von X-Plane bevorzugt. Nur wo nichts Lokales vorhanden ist, springt der Streamer ein und lädt die Daten aus dem Internet. Das ermöglicht eine clevere Kombinationsstrategie: höchste Qualität für die Heimatregion durch lokale Kacheln, weltweite Abdeckung ohne Vorbereitung durch Streaming.

Wer die Reihenfolge seiner scenery packs ini im Griff hat, vermeidet schwebende Flughäfen, überdeckte Texturen und merkwürdige Darstellungsfehler. Es lohnt sich, die Datei nach jeder Installation neuer Szenerien zu überprüfen. Und wer auf Nummer sicher gehen will, kann Werkzeuge wie xOrganizer verwenden, die die Reihenfolge automatisch optimieren und Konflikte erkennen.
