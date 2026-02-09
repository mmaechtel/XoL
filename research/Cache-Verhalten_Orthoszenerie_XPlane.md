# Cache-Verhalten von Orthoszenerie-Systemen unter X-Plane in Abhängigkeit vom individuellen Flugverhalten: Eine vergleichende Analyse von Ortho4XP und AutoOrtho

## Zusammenfassung (Abstract)

Die vorliegende Arbeit untersucht das Cache-Verhalten zweier architektonisch unterschiedlicher Orthofoto-Szenerie-Systeme im Kontext des Flugsimulators X-Plane: Ortho4XP als Vertreter eines statisch-persistenten Modells mit vorab generierten DDS-Tiles, sowie AutoOrtho als Vertreter eines On-Demand-Streaming-Modells mit eigenem Festplatten-Cache. Im Mittelpunkt steht die Frage, wie unterschiedliche Spielerprofile – habituelles Anfliegen identischer Flughäfen versus explorativer Flugstil mit ständig wechselnden Destinationen – die Effizienz des jeweiligen Caching-Ansatzes, den Speicherverbrauch und die wahrgenommene Ladeperformance beeinflussen. Es wird gezeigt, dass die beiden Systeme für komplementäre Spielerprofile optimiert sind: Ortho4XP entfaltet seine Stärken bei habituellem Flugverhalten mit hoher räumlicher Wiederholung, während AutoOrtho durch sein hybrides Streaming-Cache-Modell dem explorativen Spieler strukturelle Vorteile bietet – jedoch nur unter der Voraussetzung einer stabilen Internetverbindung.

---

## 1. Einleitung

Orthofoto-Szenerie bezeichnet die Verwendung satellitengestützter oder luftbildbasierter Fotografien als Bodentexturen in Flugsimulatoren. Unter X-Plane haben sich zwei architektonisch grundverschiedene Ansätze zur Bereitstellung solcher Texturen etabliert, deren jeweilige Eignung maßgeblich vom individuellen Flugverhalten des Nutzers abhängt.

*Ortho4XP* verfolgt einen Offline-First-Ansatz: Der Nutzer generiert vor dem Flug Szenerie-Kacheln (Tiles) im DDS-Format, die dauerhaft auf der lokalen Festplatte abgelegt werden. X-Plane liest diese Tiles zur Laufzeit wie reguläre Szeneriedaten ein. Der gesamte Datenbestand ist vollständig lokal vorgehalten; eine Internetverbindung wird zur Laufzeit nicht benötigt. Die Tiles verbleiben ohne zeitliche Begrenzung auf dem Datenträger – ein Eviction findet nur durch manuelles Eingreifen des Nutzers statt.

*AutoOrtho* verfolgt einen grundlegend anderen Ansatz: Orthofoto-Texturen werden erst zur Laufzeit bei Bedarf (on demand) von Kartenservern über das Internet heruntergeladen und über ein virtuelles Dateisystem an X-Plane ausgeliefert. Entscheidend ist jedoch, dass AutoOrtho keineswegs ein rein flüchtiges System darstellt. Heruntergeladene Tiles werden in einem eigenen, persistenten Festplatten-Cache abgelegt. Bei erneutem Besuch derselben Region können die Tiles direkt aus diesem lokalen Cache geladen werden, ohne erneuten Netzwerkzugriff. Es handelt sich somit um ein hybrides Modell: Streaming bei Erstbesuch, lokaler Cache-Zugriff bei Wiederbesuch.

Diese architektonische Divergenz – insbesondere der Unterschied zwischen vorab generiertem Vollbestand (Ortho4XP) und bedarfsgesteuertem Aufbau mit Cache (AutoOrtho) – hat tiefgreifende Auswirkungen auf das systemische Verhalten beider Lösungen in Abhängigkeit vom Spielerprofil.

## 2. Architektur der Caching-Modelle im Detail

### 2.1 Ortho4XP: Pre-Generated Persistent Storage

Das Caching-Modell von Ortho4XP lässt sich als zweistufig beschreiben.

Die erste Stufe bildet der persistente Tile-Speicher auf der Festplatte. Tiles werden im Vorfeld durch einen CPU- und netzwerkintensiven Generierungsprozess erzeugt: Quellbilder werden von Kartendiensten heruntergeladen, in DDS-Texturen konvertiert und zusammen mit Mesh-Daten als vollständige Szenerieordner abgelegt. Typische Zoomstufen liegen zwischen ZL 14 und ZL 19, wobei jede Erhöhung um eine Stufe den Speicherbedarf pro Kachel vervierfacht. Ein 1°×1°-Tile bei ZL 17 beansprucht je nach Region und Quelldienst zwischen 1 und 8 GB. Dieser Speicher wächst ausschließlich durch aktive Nutzergenerierung und schrumpft ausschließlich durch manuelles Löschen. Es existiert keine automatische Verdrängungsstrategie.

Die zweite Stufe bildet der Laufzeit-Cache in RAM und VRAM. Zur Simulationszeit lädt X-Plane die benötigten DDS-Texturen in konzentrischen Ringen um die Flugzeugposition in den Arbeitsspeicher und überträgt sichtbare Tiles in den VRAM der GPU. Entfernt sich das Flugzeug, werden nicht mehr sichtbare Texturen nach einem LRU-ähnlichen Verfahren verdrängt. Diese Stufe verhält sich identisch zu nativem X-Plane-Szenerie-Loading, da Ortho4XP-Tiles aus Sicht der Engine reguläre Szeneriedaten darstellen.

### 2.2 AutoOrtho: On-Demand Streaming mit persistentem Disk-Cache

AutoOrtho implementiert ein dreistufiges Cache-Modell.

Die erste Stufe bildet der Netzwerk-Layer. Bei Erstbesuch einer Region werden die benötigten Orthofoto-Kacheln live von Kartenservern (z. B. Bing Maps, ArcGIS, Google) heruntergeladen. Dieser Vorgang ist latenzabhängig und setzt eine stabile Internetverbindung mit ausreichender Bandbreite voraus. Die Tiles werden in Echtzeit konvertiert und über ein virtuelles Dateisystem (typischerweise FUSE-basiert) an X-Plane übergeben.

Die zweite Stufe bildet der lokale Festplatten-Cache. Einmal heruntergeladene Tiles werden von AutoOrtho in einem eigenen Cache-Verzeichnis auf der lokalen Festplatte abgelegt. Dieser Cache ist persistent: Bei erneutem Anfliegen derselben Region wird das Tile direkt von der Platte gelesen, ohne Netzwerkzugriff. Der Festplatten-Cache kann je nach Konfiguration einer Größenbeschränkung unterliegen. Wird die konfigurierte Maximalgröße erreicht, greift ein Eviction-Mechanismus, der ältere oder seltener genutzte Tiles entfernt, um Platz für neue zu schaffen. Hierin liegt ein fundamentaler Unterschied zu Ortho4XP: Der Cache ist selbstverwaltend und kann seine Größe aktiv regulieren.

Die dritte Stufe bildet, analog zu Ortho4XP, der Laufzeit-Cache in RAM und VRAM, der von X-Plane selbst verwaltet wird.

### 2.3 Tabellarischer Architekturvergleich

| Dimension | Ortho4XP | AutoOrtho |
|---|---|---|
| Datenbeschaffung | Vorab (offline) | On demand (zur Laufzeit) |
| Festplatten-Persistenz | Permanent, kein Eviction | Persistent mit konfigurierbarem Eviction |
| Internetbedarf zur Laufzeit | Nein | Ja (bei Cache-Miss) |
| Initialaufwand pro Region | Hoch (Generierung) | Null (erst bei Bedarf) |
| Speicherwachstum | Manuell gesteuert | Selbstregulierend |
| Maximale Latenz bei Erstbesuch | Keine (vorab generiert) | Netzwerkabhängig |
| Maximale Latenz bei Wiederbesuch | Festplatten-I/O | Festplatten-I/O (aus Cache) |

## 3. Spielerprofile und differenzielle Cache-Interaktion

### 3.1 Profil A: Habitueller Spieler (hohe räumliche Wiederholung)

Dieser Spielertyp fliegt wiederholt dieselben Routen und Flughäfen an, beispielsweise regelmäßige Verbindungen zwischen zwei bis fünf Stammflughäfen. Aus caching-theoretischer Perspektive handelt es sich um ein Zugriffsmuster mit hoher temporaler und räumlicher Lokalität.

**Verhalten unter Ortho4XP:**
Ortho4XP ist für dieses Profil nahezu ideal optimiert. Nach einer einmaligen, zeitintensiven Generierungsphase der Stammregionen befindet sich der gesamte benötigte Datenbestand dauerhaft auf der lokalen Festplatte. Die Cache-Trefferquote auf Festplattenebene konvergiert gegen 100 %. Es entstehen keine Netzwerkzugriffe, keine Latenzschwankungen und keine Abhängigkeit von externen Diensten. Die Ladeperformance wird ausschließlich durch die sequentielle Lesegeschwindigkeit des Datenträgers determiniert, was insbesondere auf NVMe-SSDs zu exzellenten Ergebnissen führt. Der Speicherverbrauch ist endlich, planbar und vollständig genutzt – jedes gespeicherte Byte dient einem wiederkehrenden Zweck. Der Nutzer bezahlt einmalig mit Generierungszeit und erhält dafür eine dauerhaft optimale Performance. Das System befindet sich im thermodynamischen Gleichgewicht: Es wird weder Energie (Netzwerkbandbreite, CPU-Zyklen) zugeführt noch muss Cache verdrängt werden.

**Verhalten unter AutoOrtho:**
AutoOrtho erreicht für den habituellen Spieler nach einer Aufwärmphase ein vergleichbares Leistungsniveau. Beim ersten Anflug jeder Stammregion müssen die Tiles über das Netzwerk heruntergeladen werden, was initial zu Latenz und potentiellem Texture-Streaming (sichtbares Nachladen, Unschärfe beim Annähern) führen kann. Nach dem ersten vollständigen Besuch aller Stammregionen befinden sich die relevanten Tiles im lokalen Festplatten-Cache, und das System verhält sich fortan ähnlich wie Ortho4XP: Tiles werden lokal gelesen, ohne Netzwerkzugriff. Die Performance-Parität wird erreicht – allerdings unter zwei Vorbehalten. Erstens besteht das Risiko, dass der Eviction-Mechanismus bei begrenzter Cache-Größe auch regelmäßig benötigte Tiles verdrängt, was zu unerwarteten Re-Downloads führen kann. Zweitens ist die initiale Aufwärmphase bei AutoOrtho in den eigentlichen Flugsimulationsbetrieb eingebettet, während sie bei Ortho4XP als separater Vorabprozess externalisiert ist. Der habituelle Spieler erfährt die Latenz also während des Fluges, nicht davor.

**Bewertung für Profil A:**
Ortho4XP besitzt einen strukturellen Vorteil für habituelle Spieler, da der einmalige Generierungsaufwand sich über zahlreiche identische Zugriffe amortisiert und keinerlei Laufzeitabhängigkeiten bestehen. AutoOrtho kann nach vollständiger Cache-Erwärmung eine vergleichbare Performance erreichen, unterliegt jedoch dem Risiko ungewollter Eviction und der Abhängigkeit von einer initialen Netzwerkphase.

### 3.2 Profil B: Explorativer Spieler (geringe räumliche Wiederholung)

Dieser Spielertyp zeichnet sich durch ein Zugriffsmuster mit geringer räumlicher und temporaler Lokalität aus. Jeder Flug führt in eine zuvor unbesuchte oder selten besuchte Region. Neue Destinationen dominieren gegenüber Wiederholungen.

**Verhalten unter Ortho4XP:**
Für den explorativen Spieler offenbart Ortho4XP erhebliche strukturelle Schwächen. Jede neue Destination erfordert einen vollständigen Generierungszyklus, der vor dem Flug durchgeführt werden muss. Dieser Zyklus umfasst den Download der Quellbilder, die CPU-intensive Konvertierung in DDS-Texturen und die Erstellung der Mesh-Daten – ein Prozess, der je nach Regionsgröße und Zoomstufe zwischen 30 Minuten und mehreren Stunden dauern kann. Der Nutzer wird dadurch in seiner Spontanität massiv eingeschränkt: Ein impulsiver Flug nach Madeira erfordert eine mehrstündige Vorbereitungsphase. Darüber hinaus wächst der persistente Speicherverbrauch monoton und unbegrenzt. Jede besuchte Region hinterlässt zwischen 1 und 8 GB (bei ZL 17) auf der Festplatte, die dort ohne automatische Verdrängung verbleiben. Bei einem explorativen Spieler, der monatlich zehn neue Regionen anfliegt, akkumulieren sich innerhalb eines Jahres 120 Regionen mit einem Gesamtvolumen von 120–960 GB. Da kaum Wiederzugriffe stattfinden, sinkt der effektive Nutzungsgrad des Speichers – definiert als Verhältnis der tatsächlichen Lesezugriffe zur gespeicherten Datenmenge – asymptotisch gegen null. Es entsteht ein Akkumulationsparadox: ein wachsender Datenfriedhof aus hochauflösenden Tiles, die ihren Zweck bereits nach einem einzigen Flug erfüllt haben.

**Verhalten unter AutoOrtho:**
AutoOrtho adressiert die Schwächen von Ortho4XP für explorative Spieler in mehreren Dimensionen. Der offensichtlichste Vorteil ist die Eliminierung der Vorab-Generierungsphase. Der Nutzer kann jeden beliebigen Flughafen der Welt spontan anfliegen, ohne Vorbereitungszeit. Beim Erstbesuch einer Region werden die Tiles on demand heruntergeladen und direkt an X-Plane ausgeliefert. Die heruntergeladenen Tiles werden im lokalen Festplatten-Cache abgelegt. Bei einer konfigurierten Cache-Größenbeschränkung greift der Eviction-Mechanismus automatisch: Selten oder nie wiederholt angeflogene Regionen werden verdrängt, um Platz für neue Destinationen zu schaffen. Dieses Verhalten entspricht exakt dem Zugriffsmuster des explorativen Spielers – Tiles, die nicht mehr benötigt werden, werden automatisch entfernt, ohne manuelles Eingreifen. Der Speicherverbrauch bleibt damit langfristig stabil und bewegt sich innerhalb der konfigurierten Obergrenze. Der wesentliche Nachteil manifestiert sich in der Netzwerklatenz beim Erstbesuch. Da der explorative Spieler per Definition überwiegend Cache-Misses produziert, wird bei nahezu jedem Flug ein signifikanter Anteil der Tiles live gestreamt. Dies führt in Abhängigkeit von der verfügbaren Bandbreite und der Server-Antwortzeit zu sichtbaren Ladeeffekten: Tiles erscheinen zunächst in niedriger Auflösung und werden progressiv nachgeschärft, oder es kommt zu kurzzeitigem Texture-Popping. Die wahrgenommene visuelle Qualität während der ersten Flugminuten ist daher typischerweise geringer als bei vorab generierten Ortho4XP-Tiles.

**Bewertung für Profil B:**
AutoOrtho besitzt einen deutlichen strukturellen Vorteil für explorative Spieler. Die Eliminierung des Vorab-Generierungsaufwands, das selbstregulierende Cache-Management und die potentiell globale Abdeckung ohne Speicherexplosion machen es zum geeigneteren System für dieses Nutzungsprofil. Der Preis ist eine Abhängigkeit von der Netzwerkinfrastruktur und eine reduzierte visuelle Sofortqualität beim Erstbesuch.

## 4. Formale Cache-Analyse

### 4.1 Definitionen

Sei $N$ die Gesamtzahl der angeflogenen Regionen über einen Beobachtungszeitraum, $U$ die Anzahl der dabei eindeutig besuchten (unique) Regionen und $V$ die Anzahl der Wiederbesuche, sodass $N = U + V$. Der Wiederholungsgrad $R$ sei definiert als:

$$R = \frac{V}{N} = 1 - \frac{U}{N}$$

Für den habituellen Spieler gilt $R \to 1$ (wenige eindeutige Regionen, viele Wiederbesuche), für den explorativen Spieler $R \to 0$ (jeder Flug eine neue Region).

### 4.2 Cache-Trefferquote

**Ortho4XP** (vollständig vorab generiert):
Die Festplatten-Trefferquote $H_{\text{O4XP}}$ beträgt per Definition 100 % für alle generierten Regionen, da alle Tiles permanent vorliegen. Für nicht generierte Regionen ist sie 0 % – der Nutzer kann dort schlicht nicht fliegen (bzw. fliegt ohne Orthoszenerie). Es gilt:

$$H_{\text{O4XP}} = \frac{n_{\text{generiert}}}{n_{\text{angefragt}}}$$

wobei $n_{\text{generiert}}$ die Anzahl der vorab generierten Regionen und $n_{\text{angefragt}}$ die Anzahl der angefragten Regionen bezeichnet.

**AutoOrtho** (on demand mit Disk-Cache):
Die Festplatten-Trefferquote $H_{\text{AO}}$ hängt vom Zusammenspiel zwischen Wiederholungsgrad und Cache-Kapazität ab. Sei $C$ die maximale Anzahl von Regionen, die der Disk-Cache aufnehmen kann, und sei ein LRU-Eviction angenommen. Dann gilt approximativ:

$$H_{\text{AO}} \approx \begin{cases} R & \text{wenn } U > C \text{ (Cache-Überlauf)} \\ \frac{V + \min(U, C)}{N} & \text{wenn } U \leq C \text{ (Cache ausreichend)} \end{cases}$$

Im zweiten Fall (Cache fasst alle eindeutigen Regionen) konvergiert $H_{\text{AO}}$ nach vollständiger Erwärmung gegen 100 %, da jede Region nach dem Erstbesuch lokal verfügbar ist.

### 4.3 Speicherverbrauch über die Zeit

**Ortho4XP:**
Der kumulative Speicherverbrauch $S_{\text{O4XP}}(t)$ wächst proportional zur Anzahl der generierten eindeutigen Regionen:

$$S_{\text{O4XP}}(t) = \sum_{i=1}^{U(t)} s_i$$

wobei $s_i$ die Größe des Tiles der $i$-ten eindeutigen Region bezeichnet. Da kein Eviction stattfindet, ist $S_{\text{O4XP}}$ eine monoton steigende Funktion. Für den habituellen Spieler konvergiert sie gegen einen Grenzwert (die Summe aller Stammregionen); für den explorativen Spieler wächst sie unbegrenzt.

**AutoOrtho:**
Der Speicherverbrauch $S_{\text{AO}}(t)$ ist durch die konfigurierte Cache-Obergrenze $S_{\max}$ beschränkt:

$$S_{\text{AO}}(t) \leq S_{\max} \quad \forall t$$

Nach Erreichen von $S_{\max}$ verdrängt der Eviction-Mechanismus alte Tiles, sodass der Speicherverbrauch auf einem Plateau verharrt. Dies gilt unabhängig vom Spielerprofil.

### 4.4 Effektiver Nutzungsgrad des Speichers

Der effektive Nutzungsgrad $\eta$ sei definiert als das Verhältnis der Gesamtzahl der Cache-Hits $H$ zum kumulativen Speicherverbrauch:

$$\eta = \frac{H}{\bar{S}}$$

wobei $\bar{S}$ den mittleren Speicherverbrauch über den Beobachtungszeitraum bezeichnet.

Für Ortho4XP beim explorativen Spieler gilt: $H$ wächst langsam (wenige Wiederbesuche), $\bar{S}$ wächst schnell (jede Region bleibt permanent gespeichert), sodass $\eta \to 0$ – eine maximal ineffiziente Speichernutzung.

Für AutoOrtho beim explorativen Spieler gilt: $H$ ist ebenfalls niedrig, aber $\bar{S}$ ist durch $S_{\max}$ begrenzt, sodass $\eta$ zwar niedrig, aber stabil bleibt.

Für beide Systeme beim habituellen Spieler gilt: $H$ wächst proportional zur Anzahl der Flüge, $\bar{S}$ konvergiert gegen einen festen Wert, sodass $\eta$ unbegrenzt wächst – eine zunehmend effizientere Speichernutzung mit jeder Wiederholung.

## 5. Laufzeitperformance und Nutzererfahrung

### 5.1 Texture Loading und visuelle Qualität

Ein zentraler Unterschied in der Nutzererfahrung betrifft das Texture-Loading-Verhalten.

Ortho4XP liefert bei vorab generierten Regionen sofortige volle Texturqualität. Die DDS-Tiles liegen im nativen Format der Rendering-Engine vor und werden ohne Konvertierungsverzögerung in den VRAM geladen. Der Nutzer sieht zu keinem Zeitpunkt niedrigaufgelöste Zwischenzustände oder Nachladeeffekte – vorausgesetzt, die Region wurde vorab generiert. Die visuelle Konsistenz ist maximal.

AutoOrtho implementiert typischerweise ein progressives Ladeschema. Bei Cache-Hits (Wiederbesuch, Tile im Disk-Cache vorhanden) ist die Erfahrung vergleichbar mit Ortho4XP: Tiles werden von der lokalen Festplatte geladen und stehen in voller Auflösung zur Verfügung. Bei Cache-Misses (Erstbesuch) zeigt sich jedoch ein charakteristisches Streaming-Verhalten: Tiles werden zunächst in niedriger Zoomstufe angezeigt und progressiv durch höher aufgelöste Varianten ersetzt, sobald diese heruntergeladen sind. Dieses Verhalten ist bei schnellen Überflügen über unbekanntes Terrain besonders sichtbar und manifestiert sich als „Einschärfen" der Bodentextur. Die visuelle Qualität im stationären Zustand (nach vollständigem Download) ist jedoch gleichwertig.

### 5.2 Abhängigkeit von externen Faktoren

Ortho4XP ist nach Abschluss der Generierungsphase vollständig autark. Die Performance hängt ausschließlich von lokalen Hardwareparametern ab: Festplatten-I/O, verfügbarer RAM und VRAM-Kapazität. Dieser Determinismus macht das System robust und vorhersagbar.

AutoOrtho führt eine Abhängigkeit von der Netzwerkinfrastruktur ein, die sich je nach Spielerprofil unterschiedlich auswirkt. Für den habituellen Spieler mit aufgewärmtem Cache ist die Netzwerkabhängigkeit nach der Aufwärmphase vernachlässigbar. Für den explorativen Spieler ist sie hingegen ein permanenter Faktor, da nahezu jeder Flug Netzwerkzugriffe erfordert. Schwankungen in Bandbreite, Latenz oder Serververfügbarkeit wirken sich direkt auf die Texturqualität und Ladezeit aus.

## 6. Synthese: Optimale Systemwahl in Abhängigkeit vom Spielerprofil

Die vorangegangene Analyse legt eine klare Zuordnung nahe, die in folgender Matrix zusammengefasst werden kann:

| Dimension | Habituell × Ortho4XP | Habituell × AutoOrtho | Explorativ × Ortho4XP | Explorativ × AutoOrtho |
|---|---|---|---|---|
| Cache-Trefferquote | ★★★★★ (100 %) | ★★★★☆ (hoch nach Aufwärmung) | ★★★★★ (aber nur generierte Regionen) | ★★☆☆☆ (dominiert von Misses) |
| Speichereffizienz | ★★★★★ (vollständig genutzt) | ★★★★☆ (genutzt, Eviction-Risiko) | ★☆☆☆☆ (Datenfriedhof) | ★★★★☆ (selbstregulierend) |
| Spontanität | ★★☆☆☆ (Vorabgenerierung) | ★★★★★ (sofort fliegbar) | ★☆☆☆☆ (stundenlange Vorbereitung) | ★★★★★ (sofort fliegbar) |
| Visuelle Konsistenz | ★★★★★ (sofort volle Qualität) | ★★★★☆ (nach Cache-Aufwärmung) | ★★★★★ (wo generiert) | ★★★☆☆ (progressives Laden) |
| Offline-Fähigkeit | ★★★★★ (vollständig) | ★★☆☆☆ (nur gecachte Regionen) | ★★★★★ (wo generiert) | ★☆☆☆☆ (kaum Cache-Hits) |
| Langfristiger Speicher | ★★★★★ (stabil, planbar) | ★★★★★ (stabil, begrenzt) | ★☆☆☆☆ (unbegrenztes Wachstum) | ★★★★☆ (stabil durch Eviction) |

Die optimale Konfiguration ergibt sich als diagonale Zuordnung: Der habituelle Spieler profitiert maximal von Ortho4XP, der explorative Spieler von AutoOrtho.

## 7. Hybride Spielerprofile und Mischstrategien

In der Praxis bewegen sich die meisten Nutzer auf einem Kontinuum zwischen den Extremprofilen. Ein typischer Spieler unterhält möglicherweise drei bis vier Stammflughäfen, unternimmt aber gelegentlich explorative Flüge in unbekannte Regionen.

Für dieses hybride Profil bieten sich Mischstrategien an. Eine technisch elegante Lösung wäre die parallele Nutzung beider Systeme: Ortho4XP für die Stammregionen, die dauerhaft in höchster Qualität und ohne Netzwerkabhängigkeit zur Verfügung stehen; AutoOrtho für alle übrigen Regionen, die spontan und ohne Vorabgenerierung angeflogen werden können. Die Szenerie-Priorisierung von X-Plane erlaubt prinzipiell eine solche Schichtung, bei der lokale Ortho4XP-Tiles Vorrang vor den AutoOrtho-Tiles erhalten.

Alternativ könnte AutoOrtho allein eingesetzt werden, wobei die Cache-Größe so dimensioniert wird, dass die Stammregionen dauerhaft im Cache verbleiben und nur explorative Tiles dem Eviction unterliegen. Dies setzt allerdings voraus, dass der Eviction-Algorithmus die Zugriffshäufigkeit berücksichtigt (LFU statt reinem LRU), da andernfalls auch regelmäßig geflogene Tiles verdrängt werden könnten, wenn zwischenzeitlich viele explorative Flüge stattfinden.

## 8. Fazit

Das Cache-Verhalten von Orthoszenerie-Software unter X-Plane ist fundamental an das räumliche Wiederholungsmuster des individuellen Spielverhaltens gekoppelt. Die beiden dominierenden Systeme – Ortho4XP und AutoOrtho – implementieren architektonisch komplementäre Caching-Strategien, die jeweils für unterschiedliche Spielerprofile optimiert sind.

Ortho4XP verkörpert ein deterministisches, vollständig lokales Modell mit maximaler Performance und Vorhersagbarkeit, das seinen vollen Nutzen bei repetitiven Zugriffsmustern entfaltet, jedoch bei explorativen Mustern unter unkontrolliertem Speicherwachstum und prohibitivem Vorabaufwand leidet.

AutoOrtho verkörpert ein adaptives, netzwerkabhängiges Modell mit selbstregulierendem Festplatten-Cache, das explorativen Spielern maximale Flexibilität und Spontanität bietet, jedoch bei jedem Erstbesuch den Preis netzwerkbedingter Latenz und progressiven Textur-Ladens zahlt. Der lokale Disk-Cache stellt dabei sicher, dass wiederholt besuchte Regionen ohne erneuten Netzwerkzugriff in voller Qualität verfügbar sind – ein entscheidender Mechanismus, der AutoOrtho auch für Mischprofile attraktiv macht.

Die bewusste Wahl zwischen beiden Systemen – oder ihre kombinierte Nutzung – auf Basis einer ehrlichen Einschätzung des eigenen Spielverhaltens stellt somit eine nicht-triviale Optimierungsentscheidung dar, die signifikante Auswirkungen auf Speicherverbrauch, visuelle Qualität und Nutzererfahrung hat.

---

*Schlüsselwörter: Orthoszenerie, X-Plane, Ortho4XP, AutoOrtho, Tile-Caching, On-Demand-Streaming, Disk-Cache, Eviction, Cache-Effizienz, Spielerverhalten, Speichermanagement, Flugsimulation*
