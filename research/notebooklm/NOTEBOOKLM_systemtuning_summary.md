# Systemtuning für X-Plane unter Linux — Latenz verstehen und gezielt reduzieren

## Warum Latenz wichtiger ist als Durchsatz

Bevor wir in die Details einsteigen, eine Einordnung. Linux-Distributionen unterscheiden sich nicht nur im Paketmanager oder in der Desktop-Umgebung, sondern vor allem im Zusammenspiel zwischen Kernel und Systemsoftware. Allgemein-Distributionen wie Debian oder Ubuntu optimieren auf Stabilität und breite Hardware-Kompatibilität. Gaming-orientierte Distributionen wie Nobara oder Pop OS liefern bereits voreingestellte Kernel-Parameter für niedrige Latenz. Wer eine solche Distribution verwendet, sollte die folgenden Empfehlungen nicht blind übernehmen — dort kann doppeltes Tuning zu schlechteren Ergebnissen führen. Die folgenden Anleitungen basieren auf Debian als Ausgangspunkt, einer bewusst neutralen Distribution, die man gezielt optimieren kann.

Wer an Leistung denkt, denkt meistens an möglichst viele Bilder pro Sekunde. Bei einem Shooter oder Rennspiel stimmt das auch — da geht es um Durchsatz, um maximale Framerate. Aber ein Flugsimulator wie X-Plane funktioniert grundlegend anders. X-Plane berechnet eine komplexe Welt mit Physik, Wetter, Szenerie und Eingabegeräten. Einzelne Frames sind aufwändig, und die Ziel-Framerate liegt typischerweise bei fünfundzwanzig bis fünfunddreißig Bildern pro Sekunde. Das klingt erstmal wenig, aber genau hier liegt der entscheidende Punkt: Was zählt, ist nicht der Durchschnitt, sondern die Gleichmäßigkeit. Fachleute nennen das Frame-Time-Konsistenz.

Ein System, das stabil fünfunddreißig Bilder pro Sekunde liefert, erzeugt eine deutlich flüssigere Bewegung als eines, das zwischen fünfundzwanzig und fünfzig schwankt. Die hohen Spitzen bringen nichts, aber die Einbrüche spürt man sofort. Jedes Mal, wenn ein einzelnes Frame zu spät kommt, entsteht ein Mikroruckler. Das sind diese kurzen Hänger, die man spürt, obwohl der Prozessor und die Grafikkarte eigentlich nicht ausgelastet sind. Auch eine verzögerte Reaktion von Joystick oder Ruderpedalen gehört zu den typischen Symptomen.

Die Ursache für diese Ungleichmäßigkeit ist meist nicht fehlende Rechenleistung, sondern Latenz — kurze Verzögerungen durch Systemereignisse, die den Hauptthread der Anwendung unterbrechen. Die zentrale Erkenntnis für alles was folgt lautet daher: Für X-Plane ist zeitliche Vorhersagbarkeit wichtiger als rohe Rechenleistung. Ein System, das zuverlässig jedes einzelne Frame pünktlich abliefert, fühlt sich besser an als eines mit höherem Durchschnitt aber gelegentlichen Aussetzern.

## Die vier Quellen der Systemlatenz

Wenn Latenz das Problem ist, muss man verstehen, woher sie kommt. Und sie entsteht nicht an einer einzigen Stelle, sondern aus vier unabhängigen Kategorien. Das ist wichtig, denn jede Kategorie braucht eine eigene Lösung. Man kann nicht an einer Stelle drehen und erwarten, dass alle Probleme verschwinden.

Die erste Kategorie ist das Scheduling. Der Linux-Scheduler entscheidet, wann welcher Thread CPU-Zeit bekommt. Ein konservativer Scheduler, wie ihn allgemeine Distributionen verwenden, wartet länger, bevor er reagiert. Das spart Strom und ist fair gegenüber allen Prozessen, erhöht aber die Latenz für die Anwendung, die gerade dringend Rechenzeit braucht. Das typische Symptom sind Ruckler nach Lastspitzen, weil der Scheduler nicht schnell genug auf die veränderte Situation umschaltet.

Die zweite Kategorie ist die Energieverwaltung. Und hier muss man umdenken: Nicht die CPU-Last verursacht Ruckler, sondern die Übergänge zwischen Energiezuständen. Moderne Prozessoren haben verschiedene Schlafzustände, sogenannte C-States. Wenn ein Prozessorkern aus einem tiefen Schlafzustand aufwacht, können Verzögerungen von mehreren hundert Mikrosekunden entstehen. Das klingt wenig, reicht aber aus, um eine Frame-Deadline zu reißen. Noch gravierender sind NVMe-SSDs, also schnelle Solid State Drives mit direkter Anbindung an den Prozessor, wenn sie sich im Energiesparmodus befinden. Die können Aufwachlatenzen im Millisekundenbereich haben — das ist länger als ein komplettes Frame bei sechzig Hertz.

Die dritte Kategorie sind Interrupts. Hardware-Interrupts von USB-Geräten, Netzwerk oder Speicher unterbrechen den laufenden Thread. Ein einzelner Interrupt zum falschen Zeitpunkt kann dazu führen, dass eine Frame-Deadline verpasst wird. Man stelle sich einen regelmäßig arbeitenden Hauptthread vor, der wie ein Uhrwerk läuft. Dann kommt ein zufälliger Interrupt dazwischen, unterbricht den Thread für ein paar Mikrosekunden, und das Frame wird nicht rechtzeitig fertig. Das Ergebnis ist ein sichtbarer Ruckler.

Die vierte Kategorie ist das Speicher- und I/O-Subsystem. Der Kernel optimiert den Durchsatz durch gebündelte Hintergrundarbeit — Writeback, Cache-Bereinigung und Paging. Diese Operationen sind im Durchschnitt effizient, erzeugen aber seltene, dafür spürbare Blockierungen. Das fällt besonders auf, wenn X-Plane große Ortho-Texturen nachlädt und gleichzeitig der Kernel gerade beschließt, seinen Schreibpuffer auf die Festplatte zu leeren.

## Zwei Kernel, zwei grundverschiedene Strategien

Hier wird es richtig interessant, denn hier liegt der Kern des ganzen Themas. Linux bietet nicht nur einen Kernel. Auf Debian kann man neben dem Standardkernel auch den Liquorix-Kernel installieren. Und diese beiden Kernel brauchen grundlegend verschiedene Tuning-Strategien. Das ist der wichtigste Punkt überhaupt, und den muss man wirklich verstanden haben, bevor man irgendetwas an seinem System ändert.

Der Standardkernel von Debian verhält sich wie eine offene Steuerung. Er priorisiert Fairness und Durchsatz. Alle Prozesse werden gleich behandelt, der Scheduler reagiert konservativ auf Laständerungen. Das ist für einen Server oder einen Bürorechner genau richtig, aber für einen Flugsimulator, der auf jede Millisekunde angewiesen ist, zu träge. Tuning bedeutet hier: der Anwendung aktiv Vorrang geben. Man muss dem System explizit sagen, was wichtig ist, weil der Kernel es von alleine nicht erkennt.

Der Liquorix-Kernel hingegen verhält sich wie eine geschlossene Regelschleife. Er verwendet den PDS-Scheduler — das steht für Priority and Deadline based Skiplist. Dieser Scheduler arbeitet mit kürzeren Preemption-Fenstern und einer Timerfrequenz von tausend Hertz, also der doppelten Auflösung des Standardkernels. Er reagiert selbstständig auf Laständerungen und erkennt latenzsensitive Threads automatisch. Tuning bedeutet hier das genaue Gegenteil: externe Störquellen beseitigen, damit der Scheduler ungestört seine Arbeit machen kann.

Und jetzt kommt der Punkt, den man sich unbedingt merken muss: Dieselbe Einstellung kann bei den beiden Kerneln gegenteilige Ergebnisse liefern. Ein Performance-Governor hilft dem Standardkernel, weil er die Reaktionszeit verkürzt. Beim Liquorix-Kernel kann er aber kontraproduktiv sein, weil der thermische Spielraum verloren geht, den der Kernel für Burst-Leistung braucht. CPU-Isolation hilft dem Standardkernel, weil sie Konkurrenz durch Hintergrundprozesse verhindert. Beim Liquorix verhindert sie aber die adaptive Optimierung des Schedulers, der Threads intelligent zwischen Kernen verschieben will.

## Profil A: Den Standardkernel beschleunigen

Beim Standardkernel ist das Ziel klar: Der Scheduler reagiert zu langsam, also muss man die Anwendung aktiv bevorzugen. Man erzwingt sozusagen die Reaktionsfähigkeit.

Der erste und wichtigste Hebel ist der CPU-Governor. Man stellt ihn auf Performance, also einen festen hohen Takt. Das verkürzt die Reaktionszeit und kompensiert die fehlende Lastvorhersage des konservativen Schedulers. Das kann man temporär über einen Systembefehl ändern oder dauerhaft über einen Kernel-Boot-Parameter einrichten, sodass die Einstellung jeden Neustart überlebt.

Der zweite Hebel sind die CPU-Schlafzustände, die sogenannten C-States. Tiefe Schlafzustände sparen Strom, aber das Aufwachen dauert. Hier gibt es einen wichtigen Unterschied zwischen AMD und Intel. Bei AMD-Zen-Prozessoren sind nur die Stufen eins und zwei für das Betriebssystem sichtbar. Tiefere Schlafzustände werden von der Firmware autonom verwaltet und lassen sich gar nicht über das Betriebssystem begrenzen. Bei Intel-Prozessoren hingegen sind viele weitere Stufen steuerbar, und hier lohnt es sich, die tiefsten zu begrenzen, weil deren Aufwachlatenzen spürbar werden.

Der dritte Hebel ist die direkte Priorisierung der Anwendung. Man kann X-Plane an bestimmte CPU-Kerne binden und mit erhöhter Scheduling-Priorität starten. Ein Startskript kombiniert beides: Kernzuweisung über taskset und Echtzeitpriorität über chrt. Eine Priorität von fünfundvierzig liegt unterhalb kritischer Kernel-Threads wie Interrupt-Handler, die bei fünfzig laufen, aber deutlich über normalen Prozessen. Ergänzend kann man CPU-Isolation nutzen, um bestimmte Kerne komplett von normalen Prozessen freizuhalten. Das gilt allerdings als veraltet — die modernere Alternative sind cpusets, die sich zur Laufzeit konfigurieren lassen.

Beim Speicherverhalten setzt man moderate Werte für Swappiness und Writeback-Grenzen. Die Idee ist ein Mittelweg: nicht so aggressiv, dass der Durchsatz leidet, aber ausreichend gezähmt, um große Blockierungen beim Schreiben zu vermeiden.

Das Ergebnis dieses Profils: Der Kernel reagiert schneller, weil Rechenzeit für die Anwendung garantiert wird.

## Profil B: Liquorix in Ruhe arbeiten lassen

Beim Liquorix-Kernel dreht sich die gesamte Philosophie um. Keine CPU-Isolation, kein Core-Pinning, keine aggressive Echtzeitpriorität. All das würde den PDS-Scheduler behindern, der Threads selbstständig optimal platzieren will.

Der CPU-Governor wird auf ondemand gesetzt, nicht auf Performance. Warum? Weil ein dauerhaft hoher Takt den thermischen Spielraum aufbraucht. Wenn die CPU schon auf Maximum läuft, kann sie bei Lastspitzen nicht mehr boosten. Ondemand hingegen hält den Takt im Leerlauf niedrig und fährt bei Bedarf schnell hoch. Das gibt dem Prozessor Luft zum Atmen und ermöglicht höhere Boost-Takte, wenn sie wirklich gebraucht werden. Ergänzend kann man die Energy Performance Preference auf balance performance setzen, was dem Prozessor signalisiert, bei der Abwägung zwischen Energiesparen und Leistung eher Richtung Leistung zu tendieren. Warum nicht schedutil, das eigentlich der modernere Governor wäre? Weil der Liquorix-Kernel den PDS-Scheduler verwendet und nicht den Standard-CFS, den Completely Fair Scheduler, oder EEVDF, den Earliest Eligible Virtual Deadline First Scheduler. Schedutil braucht Auslastungssignale von genau diesen Standard-Schedulern und ist deshalb im Liquorix-Kernel gar nicht einkompiliert. Ondemand passt die CPU-Frequenz ebenfalls lastabhängig an, arbeitet aber unabhängig vom Scheduler und funktioniert daher mit jedem Kernel.

Die wichtigste Maßnahme unter Liquorix ist das Interrupt-Shielding. Hardware-Interrupts werden auf die ersten Kerne konzentriert, damit der Scheduler die übrigen Kerne ungestört für die Anwendung nutzen kann. Dafür konfiguriert man den irqbalance-Dienst mit einer Ausschlussliste. Die Kerne null bis drei übernehmen System und Interrupts, der Rest bleibt für die Anwendung frei. Irqbalance ist dabei intelligenter als manuelle Zuweisung: Es passt sich automatisch an neue Hardware an und verteilt die Last gleichmäßig auf die erlaubten Kerne.

Wichtig zu wissen: Moderne Kernel verwenden für bestimmte Geräte wie NVMe-SSDs und Grafikkarten sogenannte Managed Interrupts. Deren Verteilung kontrolliert der Kernel selbst, und manuelle Änderungen werden abgelehnt. Das ist kein Fehler, sondern ein gewollter Schutzmechanismus.

NVMe-Energiesparen wird unter Liquorix komplett deaktiviert. Die Aufwachlatenzen von NVMe-SSDs im Energiesparmodus können länger sein als ein ganzes Frame. Über einen Kernel-Boot-Parameter lässt sich das zuverlässig abschalten. Zur Laufzeit ist das schwieriger, weil der entsprechende Systemparameter nur auf neu initialisierte Geräte wirkt, nicht auf bereits aktive.

Der Speicher-Writeback wird geglättet: niedrigere Schwellwerte sorgen dafür, dass Daten häufiger in kleinen Portionen geschrieben werden statt selten in großen Blöcken. Das verhindert einzelne lange Blockierungsereignisse, die sonst genau dann auftreten könnten, wenn X-Plane gerade eine Szenerie nachlädt. Der Unterschied zum Standardkernel-Profil ist hier subtil aber wichtig: Beim Standardkernel setzt man moderate Werte, weil man den Durchsatz nicht zu stark drosseln will. Beim Liquorix setzt man aggressivere Werte, weil man auch seltene Blockierungen vermeiden will und der Scheduler den Rest ohnehin intelligent handhabt.

Die Priorisierung ist bewusst leicht gehalten. Ein moderater nice-Wert von minus zehn reicht aus. Kein taskset, kein chrt, keine Echtzeitpriorität. Der PDS-Scheduler erkennt latenzsensitive Threads an ihrem Aufwachverhalten und behandelt sie bevorzugt — solange man ihn nicht durch zu aggressive Eingriffe daran hindert.

Das Ergebnis: Nicht maximale Leistung, sondern minimale Frametime-Spikes. Der Scheduler optimiert frei, weil externe Störungen reduziert sind.

## Die goldene Regel und was man daraus mitnehmen kann

Standardkernel braucht Priorisierung — Liquorix braucht Ruhe. Wenn beide gleich konfiguriert werden, verschlechtert sich das Ergebnis fast immer. Der Standardkernel braucht einen festen Hochleistungstakt, CPU-Bindung und aktive Priorisierung. Der Liquorix-Kernel braucht einen adaptiven Governor, keine CPU-Bindung und dafür konsequentes Interrupt-Shielding. Die Speichereinstellungen unterscheiden sich ebenfalls: moderate Werte beim Standardkernel, geglättete Werte beim Liquorix.

Man kann beide Kernel parallel installiert haben und beim Booten über GRUB, den Bootloader, wählen. Sowohl eine einmalige Kernelwahl als auch eine dauerhafte Umstellung sind möglich. Wichtig ist nur, dass man nach dem Wechsel auch das passende Tuning-Profil aktiviert. Die falschen Speichereinstellungen oder der falsche Governor zum falschen Kernel sind schlimmer als gar kein Tuning.

Drei konkrete Empfehlungen zum Schluss. Erstens: Latenz vor Durchsatz. Wenn X-Plane ruckelt, obwohl die Hardware nicht ausgelastet ist, liegt es fast immer an einer der vier Latenzquellen. Nicht mehr Leistung ist die Lösung, sondern weniger Störungen.

Zweitens: Den Kernel kennen. Bevor man irgendetwas einstellt, prüft man mit dem Befehl uname minus r, welchen Kernel man verwendet. Enthält die Ausgabe das Wort Liquorix, braucht man Profil B. Andernfalls Profil A. Die Profile sind bewusst gegensätzlich, und das Mischen führt zu schlechteren Ergebnissen.

Drittens: Nicht alles auf einmal ändern. Die meisten Einstellungen wie der Governor, die Speicherparameter oder der irqbalance-Dienst lassen sich zur Laufzeit anpassen und sofort testen. Nur C-State-Limits, NVMe-Energiesparen und CPU-Isolation erfordern einen Neustart über den Bootloader. So kann man schrittweise optimieren und die Auswirkung jeder einzelnen Änderung beobachten, bevor man die nächste vornimmt. Am besten startet man mit dem Governor und den Speichereinstellungen — die lassen sich sofort testen und bei Bedarf zurücksetzen. Interrupt-Shielding über irqbalance ist der nächste logische Schritt unter Liquorix. Und erst wenn man mit diesen Grundlagen zufrieden ist, nimmt man sich die Boot-Parameter vor, die einen Neustart erfordern.
