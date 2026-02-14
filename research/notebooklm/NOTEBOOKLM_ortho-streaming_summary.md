# Ortho-Streaming für X-Plane unter Linux — Drei Wege zu fotorealistischen Bodentexturen

## Warum Ortho-Streaming?

Wer mit X-Plane unter Linux fliegt, kennt das Problem: Die Standard-Bodentexturen des Simulators wirken aus niedriger Höhe oft künstlich. Felder, Straßen und Siedlungen sind generisch, das Gelände sieht überall ähnlich aus. Orthofotos lösen das, indem sie echte Satellitenbilder als Bodentexturen verwenden. Plötzlich sieht man die tatsächliche Landschaft unter sich, mit realen Straßenverläufen, echten Waldkanten und erkennbaren Gebäuden.

Traditionell musste man diese Bilder vorab herunterladen und konvertieren, zum Beispiel mit Ortho4XP. Das funktioniert, hat aber einen gewaltigen Nachteil: Pro Region fallen mehrere Gigabyte an, und wer die ganze Welt abdecken will, braucht Terabyte an Speicherplatz. Genau hier setzt Ortho-Streaming an. Statt vorab alles herunterzuladen, werden die Satellitenbilder erst dann geladen, wenn das Flugzeug sich einer Region nähert. Das spart enormen Speicherplatz und ermöglicht spontanes Fliegen überall auf der Welt, ohne stundenlange Vorbereitung.

Aktuell gibt es drei Streaming-Lösungen für X-Plane unter Linux: AutoOrtho in der aktiven Weiterentwicklung durch ProgrammingDinosaur, XEarthLayer als performante Rust-Alternative, und XPME als Newcomer mit einzigartigen Features. Jede verfolgt einen anderen Ansatz, und die Wahl hängt stark vom eigenen Nutzungsprofil ab.

## Wie funktioniert das technisch?

Alle drei Lösungen nutzen dasselbe Grundprinzip: ein virtuelles Dateisystem über FUSE, also Filesystem in Userspace. Das ist eine Linux-Schnittstelle, die es Programmen erlaubt, ein Dateisystem bereitzustellen, ohne dafür Kernel-Code schreiben zu müssen. Das Streaming-Tool erstellt einen virtuellen Ordner im Custom Scenery Verzeichnis von X-Plane. Wenn X-Plane eine Texturdatei aus diesem Ordner lesen will, fängt FUSE den Zugriff ab und leitet ihn an das Streaming-Tool weiter. Das Tool prüft zuerst seinen lokalen Cache, und falls die Textur dort nicht vorliegt, lädt es die benötigten Satellitenbilder vom Kartenanbieter herunter, wandelt sie in das DDS-Format um, also DirectDraw Surface, ein GPU-optimiertes Texturformat, und liefert das Ergebnis an X-Plane zurück. Für den Simulator sieht das aus wie ein ganz normales Szenerie-Verzeichnis.

Unter Linux gibt es dabei einen wichtigen Konfigurationsschritt, den man nicht vergessen darf. In der FUSE-Konfigurationsdatei muss die Option user allow other aktiviert sein. Ohne diese Einstellung kann das Streaming-Tool die gemounteten Verzeichnisse nicht für andere Prozesse sichtbar machen, und X-Plane sieht die Texturen schlicht nicht. Außerdem empfiehlt es sich, das File-Descriptor-Limit zu erhöhen, denn die Streaming-Tools öffnen gleichzeitig viele kleine Dateien. Das Standard-Limit von eintausendvierundzwanzig reicht oft nicht aus und kann zu schwer nachvollziehbaren Fehlern führen.

Damit das funktioniert, muss das Streaming-Tool immer vor X-Plane gestartet werden, denn X-Plane indexiert seine Szenerien beim Start. In der scenery packs ini stehen die Streaming-Einträge ganz unten. Das hat einen wichtigen Grund: Einträge weiter oben haben höhere Priorität. Lokale Szenerien wie handmodellierte Flughäfen oder hochauflösende Ortho4XP-Kacheln werden also immer bevorzugt. Nur wenn für eine Region keine lokale Szenerie existiert, greift X-Plane auf die gestreamten Texturen zurück. So lassen sich beide Welten kombinieren: lokale Kacheln in höchster Qualität für die Heimatflughäfen und Streaming für den Rest der Welt.

## AutoOrtho: Der Platzhirsch

AutoOrtho ist die bekannteste und am weitesten verbreitete Streaming-Lösung. Das Original von kubilus1 wird seit Anfang zweitausendvierundzwanzig nicht mehr gepflegt. Die aktive Weiterentwicklung läuft über den Fork von ProgrammingDinosaur, der mittlerweile weit über das Original hinausgewachsen ist.

Die vielleicht wichtigste Neuerung ist die native C-Pipeline für die Texturverarbeitung. Früher lief die gesamte Bildverarbeitung in Python, was bei hoher Last zu Engpässen führte. Die C-Pipeline übernimmt jetzt die JPEG-Dekodierung und DDS-Kompression und erreicht damit deutlich kürzere Ladezeiten. Vier Pipeline-Modi stehen zur Wahl: Auto wählt automatisch die beste Kombination, Native nutzt ausschließlich C, Hybrid mischt beide Ansätze, und Python dient als Fallback auf das alte Verhalten.

Besonders praktisch ist die SimBrief-Integration. Wer seinen Flugplan in SimBrief erstellt, kann ihn in AutoOrtho importieren. Das Tool lädt dann vorab die Satellitenkacheln entlang der geplanten Route herunter, noch bevor der Flug beginnt. In Kombination mit Dynamic Zoom, das die Auflösung automatisch an die Flughöhe anpasst, sorgt das für ein deutlich flüssigeres Erlebnis: Hohe Auflösung in Bodennähe, niedrigere Stufen in Reiseflughöhe, wo man die Details ohnehin nicht sieht.

Ein Alleinstellungsmerkmal des Forks ist der Seasons-Support. AutoOrtho kann die Farbsättigung der Ortho-Bilder an die Jahreszeit anpassen, sodass die Bodentexturen zum winterlichen oder herbstlichen Erscheinungsbild von X-Plane zwölf passen. Dafür werden die Szenerie-Pakete einmalig vom X-Plane elf Format ins X-Plane zwölf Format konvertiert.

Für Linux-Nutzer stehen vorgefertigte Binaries bereit, die für verschiedene Ubuntu-Versionen gebaut werden. Wer Debian nutzt, greift in der Regel zum Build für die nächstkompatible Ubuntu-Version. Alternativ lässt sich AutoOrtho aus dem Quellcode installieren, was eine Python-Umgebung über pyenv erfordert. Die Binary-Installation ist deutlich einfacher und für die meisten Nutzer der empfohlene Weg.

Das Cache-System wurde mit der aktuellen Hauptversion grundlegend überarbeitet. Statt tausender einzelner JPEG-Dateien pro Region werden die heruntergeladenen Bildkacheln jetzt in kompakte Bundle-Dateien konsolidiert. Das löst ein langjähriges Problem: Verzeichnisse mit zehntausenden kleinen Dateien belasteten das Dateisystem und verlangsamten den Cache-Zugriff. Die neuen Bundles sind effizienter und lassen sich über die grafische Oberfläche bequem verwalten. Wenn das konfigurierte Cache-Limit erreicht wird, entfernt AutoOrtho automatisch die ältesten Einträge.

AutoOrtho unterstützt fünf Kartenanbieter: Bing, Google, Here, Yandex und Apple Maps. Die Plattformunterstützung ist breit: Windows, Linux und macOS mit Apple Silicon. Die Lizenz ist Apache zwei null, der Code ist vollständig Open Source.

## XEarthLayer: Die Rust-Alternative

XEarthLayer verfolgt einen anderen Ansatz. Das Projekt wurde Ende zweitausendfünfundzwanzig von Sam de Freyssinet gestartet, einem Softwareentwickler der von Windows auf Linux gewechselt hat und mit den bestehenden Lösungen nicht zufrieden war. Die Implementierung erfolgt in Rust, was sich in Speichersicherheit und potenziell besserer Performance niederschlägt.

Das Kernfeature von XEarthLayer ist das adaptive Prefetch-System. Anders als einfaches positionsbasiertes Vorladen unterscheidet XEarthLayer zwischen zwei Flugphasen. Im Ground Mode, also bei niedriger Geschwindigkeit am Boden oder im Landeanflug, werden Kacheln in konzentrischen Ringen um die aktuelle Position vorgeladen. Im Cruise Mode bei höherer Geschwindigkeit berechnet das System die voraussichtliche Flugroute und lädt Kacheln entlang des projizierten Pfades. Das System kalibriert sich selbst, indem es den Tile-Generierungsdurchsatz beim initialen Laden misst und die Prefetch-Strategie entsprechend anpasst.

Besonders clever ist der Circuit Breaker Mechanismus. Wenn X-Plane gerade aktiv Szenen lädt und viele Texturanfragen gleichzeitig stellt, pausiert XEarthLayer automatisch das Prefetching und gibt allen Ressourcen den Echtzeit-Anfragen Vorrang. So wird sichergestellt, dass die aktuell sichtbaren Kacheln immer zuerst geladen werden.

Damit das adaptive Prefetching funktioniert, muss in X-Plane die ForeFlight-Telemetrie aktiviert sein. XEarthLayer empfängt darüber Positions- und Geschwindigkeitsdaten über UDP, also das User Datagram Protocol. Ohne Telemetrie fällt das System auf eine einfachere Strategie zurück, die Flugdaten aus den FUSE-Anfragen ableitet.

XEarthLayer bietet sechs Kartenanbieter: Bing, Google, Apple, ArcGIS, MapBox und USGS. Regionale Szenerie-Pakete werden über eine eigene Paketverwaltung per Kommandozeile installiert. Die Pakete enthalten die Mesh-Daten und Terrain-Definitionen, die XEarthLayer für die jeweiligen Regionen benötigt.

XEarthLayer wird ausschließlich über die Kommandozeile bedient. Für Debian und Ubuntu gibt es fertige Pakete im deb-Format, für Fedora rpm-Pakete, und für Arch Linux ein Paket im Arch User Repository. Nach der Installation führt ein Setup-Assistent durch die Grundkonfiguration: X-Plane-Verzeichnis, Cache-Pfad und Hardware-Erkennung. Während des Betriebs zeigt ein Terminal-Dashboard in Echtzeit Cache-Statistiken, Download-Fortschritt und Systemgesundheit an.

Ein wichtiger Punkt: XEarthLayer läuft ausschließlich unter Linux. Windows und macOS werden nicht unterstützt. Das Projekt ist unter der MIT-Lizenz als Open Source verfügbar und richtet sich explizit an Linux-Nutzer, die maximale Streaming-Performance suchen.

## XPME: Der Neuling mit Alleinstellungsmerkmalen

X-Plane Map Enhancement, kurz XPME, ist die jüngste der drei Lösungen auf Linux. Der Entwickler derekhe pflegt seit Ende zweitausendeinundzwanzig eine ähnliche Lösung für den Microsoft Flight Simulator. Die X-Plane-Variante gibt es seit Anfang zweitausendvierundzwanzig, allerdings zunächst nur für Windows. Linux-Support existiert erst seit Anfang Februar zweitausendsechsundzwanzig und befindet sich im frühen Beta-Stadium.

XPME bringt zwei Features mit, die keine der anderen Lösungen bietet: saisonale Texturen und Nachttexturen. Die saisonalen Texturen passen die Satellitenbilder an Standort und Datum an, sodass beispielsweise europäische Landschaften im Winter bräunlicher und kahler erscheinen. Die Nachttexturen ersetzen die Bodentexturen bei Dunkelheit durch spezielle Nachtansichten mit Beleuchtung. Beide Features sind allerdings der kostenpflichtigen Pro-Version vorbehalten, die etwa dreißig US-Dollar pro Jahr kostet.

Technisch unterscheidet sich XPME grundlegend von den anderen beiden: Es basiert auf einem Dot-NET-Backend mit einer Electron-Oberfläche. Für Linux bedeutet das eine erhebliche Abhängigkeit: Dot-NET zehn null wird benötigt, und das ist derzeit noch eine Preview-Version von Microsoft, die nicht in den Standard-Paketquellen von Debian oder Fedora enthalten ist. Die Installation erfordert das Hinzufügen des Microsoft-APT-Repositorys. Bisher wurde XPME unter Linux nur auf Ubuntu vierundzwanzig null vier getestet, Debian-Kompatibilität ist wahrscheinlich aber nicht bestätigt.

Der Quellcode von XPME ist nicht öffentlich. Es handelt sich um ein Closed-Source-Projekt mit einem Freemium-Modell. Die kostenlose Version bietet grundlegendes Streaming mit Bing, ArcGIS und Google Maps. Die Pro-Version schaltet höhere Auflösungen, zusätzliche Kartenquellen, die erwähnten Saison- und Nachttexturen sowie ein Preload-Feature frei.

## CPU-Tuning: Streaming und X-Plane gleichzeitig

Ein praktisches Thema, das alle drei Lösungen betrifft: die CPU-Last. Ortho-Streaming ist rechenintensiv, besonders die DDS-Kompression der heruntergeladenen Satellitenbilder. Wenn das Streaming-Tool alle verfügbaren CPU-Kerne auslastet, leidet X-Plane, denn der Simulator ist stark auf seinen Hauptthread angewiesen.

XEarthLayer dokumentiert das Problem am ausführlichsten. Drei Einstellungen bilden eine Hierarchie: die Anzahl der Worker-Threads für die Tile-Generierung, die Obergrenze für gleichzeitige CPU-intensive Operationen wie DDS-Encoding, und die maximale Anzahl paralleler Tile-Jobs insgesamt. Der effektivste Hebel ist die Begrenzung der gleichzeitigen DDS-Kompressionen, denn die verschlingen den größten CPU-Anteil.

Als Faustregel gilt: Wenn X-Plane parallel läuft, sollte man das Streaming-Tool auf die Hälfte der physischen CPU-Kerne beschränken. Bei einem System mit acht Kernen und Hyperthreading also auf etwa vier bis sechs gleichzeitige CPU-intensive Operationen. AutoOrtho bietet ähnliche Konfigurationsmöglichkeiten über die Pipeline-Thread-Anzahl und die Buffer-Pool-Größe.

Interessanterweise erkennt XEarthLayer den Speichertyp automatisch über Linux-Kernel-Schnittstellen und passt die Anzahl gleichzeitiger Festplatten-Operationen entsprechend an. Für eine NVMe-SSD erlaubt es über hundert parallele Zugriffe, für eine klassische Festplatte nur wenige. Das ist ein Beispiel dafür, wie die Linux-exklusive Ausrichtung von XEarthLayer dem Tool erlaubt, betriebssystemspezifische Optimierungen zu nutzen, die eine plattformübergreifende Lösung nicht implementieren würde.

Ein weiterer Aspekt des CPU-Tunings betrifft die Netzwerk-Parallelität. Je mehr gleichzeitige Downloads laufen, desto schneller füllt sich der Cache, aber desto mehr CPU-Zeit wird auch für die TLS-Verschlüsselung und Bildverarbeitung benötigt. Bei einer ohnehin langsamen Internetverbindung bringt es wenig, die CPU-Threads hochzudrehen, weil die Threads dann die meiste Zeit auf Downloads warten. Die adaptiven Systeme beider Open-Source-Lösungen berücksichtigen das und drosseln automatisch, wenn das Netzwerk zum Engpass wird.

## Welche Lösung passt zu wem?

Die Wahl hängt von den eigenen Prioritäten ab. AutoOrtho ist die ausgereifteste Lösung mit der breitesten Feature-Palette. SimBrief-Integration, Seasons, Dynamic Zoom und die C-Pipeline machen es zum Schweizer Taschenmesser unter den Streaming-Tools. Die grafische Oberfläche erleichtert die Konfiguration, und die aktive Entwicklung mit wöchentlichen Updates sorgt für schnelle Bugfixes. Wer eine bewährte Lösung sucht, die einfach funktioniert, ist hier richtig.

XEarthLayer richtet sich an Linux-Nutzer, die das Maximum an Streaming-Performance herausholen wollen und sich auf der Kommandozeile wohlfühlen. Die Rust-Implementierung und das adaptive Prefetch-System versprechen effizienten Ressourceneinsatz. Dafür fehlt eine grafische Oberfläche, und die Plattformunterstützung beschränkt sich auf Linux. Wer ausschließlich unter Linux fliegt und technisch versiert ist, findet hier eine leistungsfähige Alternative.

XPME ist aktuell nur für experimentierfreudige Nutzer zu empfehlen. Die saisonalen Texturen und Nachttexturen sind einzigartig und reizvoll, aber der Linux-Support steckt noch in den Kinderschuhen. Die Abhängigkeit von einer Preview-Version des Dot-NET-Frameworks, der fehlende Debian-Test und das Closed-Source-Modell mahnen zur Vorsicht. Wer neugierig ist, kann XPME auf Ubuntu ausprobieren, sollte aber mit Instabilitäten rechnen. Für produktiven Einsatz unter Debian ist es noch zu früh.

Alle drei Lösungen lassen sich übrigens mit statischen Ortho4XP-Kacheln kombinieren. Lokale Kacheln in höchster Auflösung für die Heimatflughäfen, Streaming für den Rest der Welt. Die scenery packs ini sorgt automatisch dafür, dass lokale Daten Vorrang haben. So bekommt man das Beste aus beiden Welten.

Ein letzter Hinweis zur Internetanbindung: Alle drei Lösungen profitieren von einer schnellen und stabilen Verbindung, aber die Anforderungen unterscheiden sich. AutoOrtho empfiehlt mindestens einhundert Megabit pro Sekunde, XEarthLayer nennt fünfhundert Megabit als empfohlenen Wert. In der Praxis ist die Netzwerkbandbreite oft der eigentliche Flaschenhals, nicht die CPU. Eine langsame Verbindung bedeutet nicht, dass Streaming unmöglich ist, aber es dauert länger bis die Kacheln erscheinen, und bei schnellen Überflügen können vorübergehend unscharfe oder fehlende Texturen sichtbar sein. Die Prefetch-Systeme beider Open-Source-Lösungen mildern das ab, indem sie vorausschauend laden, doch bei einer wirklich langsamen Leitung stößt auch das cleverste Prefetching an seine Grenzen.
