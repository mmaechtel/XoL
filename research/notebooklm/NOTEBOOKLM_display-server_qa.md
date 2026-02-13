# Display Server — X elf oder Wayland für X-Plane

## Warum ist die Display-Server-Wahl überhaupt ein Thema?

Seit Debian zwölf startet GNOME standardmäßig mit Wayland, seit Debian dreizehn auch KDE. Viele merken das gar nicht, denn der Desktop funktioniert einfach. Aber X-Plane merkt es sehr wohl. Es spricht nämlich kein Wayland. X-Plane kennt nur X elf, das klassische Display-Server-Protokoll von neunzehnhundertvierundachtzig. Und genau hier beginnt die interessante Diskussion.

Wenn man X-Plane auf einer Wayland-Session startet, springt automatisch XWayland ein. Das ist ein vollständiger X-elf-Server der innerhalb der Wayland-Session läuft. X-Plane redet X elf wie gewohnt, XWayland übersetzt ins Wayland-Protokoll, der Compositor schickt alles an die GPU. Das klingt erstmal elegant, wie ein Simultandolmetscher der im Hintergrund arbeitet. Aber jede Übersetzung kostet etwas.

Und hier ist der entscheidende Punkt. Es geht nicht darum ob Wayland schlecht ist. Wayland ist modern, effizient, und löst echte Architekturprobleme von X elf. Aber X-Plane kann kein natives Wayland. Es ist wie ein englischsprachiger Pilot der über einen Dolmetscher mit dem Tower kommuniziert. Es funktioniert, aber der direkte Draht wäre schneller. Laminar Research hat das in den Release Notes von Version zwölf Punkt eins Punkt drei sogar bestätigt: sie erzwingen intern das X-elf-Backend für die Browser-Komponente. Das sagt eigentlich alles über den aktuellen Stand.

## Wie viel Latenz kostet die XWayland-Übersetzung wirklich?

Es gibt Hardware-Messungen dazu, und die sind überraschend eindeutig. David Justo hat mit einem Arduino und einem Lichtsensor die Input-to-Photon-Latenz gemessen, also die Zeit vom Tastendruck bis zur sichtbaren Reaktion auf dem Monitor. Natives Wayland lag bei rund sieben Millisekunden, X elf bei knapp sieben, Windows elf ebenfalls bei knapp sieben. Praktisch identisch, egal welches System.

XWayland allerdings: über vierzehn Millisekunden. Das Doppelte.

Jetzt kommt der berechtigte Einwand: Vierzehn Millisekunden, ist das wirklich spürbar? Bei hundertvierundvierzig Hertz ist ein Frame knapp sieben Millisekunden lang. XWayland fügt also etwa einen Frame Verzögerung hinzu. Für einen kompetitiven Ego-Shooter wäre das ein echtes Problem. Für einen Flugsimulator? Eher eine akademische Größe. Trotzdem, wer sich an Frame Times stört und jede Quelle von Micro-Stutter eliminieren will, hat hier einen messbaren Hebel.

Aber es gibt noch eine zweite Perspektive die den Punkt weiter schärft. Xaver Hugl, KDE-Kernentwickler, hat den Compositor-Einfluss untersucht. Sein Ergebnis: Wayland mit aktivem Compositor erreicht in der Mailbox-Presentation-Mode sechsunddreißig Millisekunden. X elf ohne Compositor: achtunddreißig. Kaum ein Unterschied. Aber X elf mit Compositor springt auf neunundfünfzig Millisekunden, ein ganzes Frame mehr.

Das heißt im Klartext: Wayland schlägt composited X elf deutlich. Und hier wird es fast ironisch. Natives Wayland ist sogar effizienter als X elf mit aktivem Compositor, und wer nutzt heute schon keinen Compositor? Transparente Fenster, Schatten, Animationen, all das braucht einen Compositor. Unter X elf kann man den Compositor für Fullscreen-Anwendungen umgehen, KDE macht das sogar automatisch. Aber unter Wayland ist der Compositor fest eingebaut, er ist gleichzeitig der Display Server. Dafür ist er von Anfang an auf niedrige Latenz ausgelegt. Nur hat X-Plane eben kein natives Wayland-Backend, und damit kann es von dieser Effizienz nicht profitieren. Die Übersetzungsschicht XWayland frisst den Vorteil wieder auf.

## Ändert die GPU etwas an der Empfehlung?

Einen erheblichen Unterschied, und das wird oft unterschätzt. AMD-Nutzer mit dem RADV-Vulkan-Treiber aus dem Mesa-Projekt haben die komfortabelste Situation. Wayland funktioniert auf AMD-Karten ausgereift, ohne nennenswerte Probleme. Der Desktop profitiert von Features wie per-Monitor Refresh Rates und Variable Refresh Rate, kurz VRR. X-Plane geht trotzdem über XWayland, aber der Overhead ist moderat. AMD-Nutzer können ohne schlechtes Gewissen auf Wayland bleiben, wenn alles läuft.

Ja, aber bei NVIDIA sieht die Welt ganz anders aus. Wayland war auf NVIDIA-Karten lange ein echtes Desaster. Flickering, schwarze Bildschirme, Frames in falscher Reihenfolge. Der Durchbruch kam mit Explicit Sync, einer Methode bei der Anwendung, Treiber und Compositor explizit synchronisieren wann ein Frame fertig gerendert ist. Dafür braucht man mindestens Treiber fünfhundertfünfundfünfzig und Kernel sechs Punkt acht. Wer ältere Treiber hat, muss zwingend eine X-elf-Session verwenden, alles andere führt zu Grafikfehlern. Mit aktuellen Treibern funktioniert Wayland, aber X-Plane hat denselben XWayland-Umweg wie auf AMD.

Und dann gibt es noch den Intel-Arc-Sonderfall. Intel empfiehlt offiziell Wayland statt Xorg für Arc-GPUs, also Graphics Processing Units. Der Grund: Xorg hat auf Arc-Hardware bekannte Rendering-Glitches. Wer eine Arc-Karte nutzt, fährt mit einer Wayland-Session besser, selbst wenn X-Plane den XWayland-Overhead hat. Der stabilere Desktop gleicht den kleinen Nachteil mehr als aus.

Die GPU-Empfehlung betrifft also die Desktop-Session, nicht X-Plane selbst. X-Plane spricht immer X elf, egal welcher Display Server drumherum läuft.

## Sind Joysticks und Fluggeräte vom Display Server betroffen?

Nein, und das ist einer der am häufigsten missverstandenen Punkte. Joysticks, Throttles und Ruderpedale kommunizieren direkt mit dem Linux-Kernel über die evdev-Schnittstelle. Sie haben mit dem Display Server überhaupt nichts zu tun. Die libinput-Dokumentation sagt das sogar explizit: libinput kümmert sich bewusst nicht um Joysticks, weil jede Abstraktion nur unnötige Komplexität und Verzögerung einführen würde.

Thrustmaster, VKB, Virpil, Logitech, egal welches Gerät, es funktioniert unter X elf und Wayland identisch. Das ist für viele eine echte Erleichterung, weil die Sorge verständlich ist. Neuer Display Server, neue Probleme? Nicht bei Fluggeräten.

Wo der Display Server allerdings eine Rolle spielt ist bei Maus und Tastatur. Unter X elf konfiguriert man die Maus über das Werkzeug xinput, unter Wayland über die Compositor-Einstellungen in GNOME oder KDE. Für präzises Cockpit-Klicken lohnt es sich die Mausbeschleunigung abzuschalten und ein flaches Profil zu wählen. Das geht unter beiden Systemen, nur der Konfigurationsweg ist ein anderer.

## Welche Probleme sind typisch unter Wayland?

Das häufigste ist Fullscreen auf mehreren Monitoren. Wayland erlaubt Anwendungen nicht, ihre Fenster frei zu positionieren. XWayland erbt diese Einschränkung. X-Plane kann im Fullscreen auf einem Multi-Monitor-Setup falsch positioniert sein oder ein falsches Seitenverhältnis zeigen. Das betrifft besonders Nutzer die mit zwei oder drei Bildschirmen fliegen. Die Lösung ist entweder der Fenstermodus oder der Wechsel auf eine X-elf-Session.

Dann gibt es das Workspace-Problem. Wayland-Compositors suspendieren Anwendungen die nicht sichtbar sind. Wer während eines Langstreckenflugs auf einen anderen Workspace wechselt, kann erleben dass X-Plane das Rendering komplett pausiert. Unter X elf rendert die Anwendung im Hintergrund weiter. Für manche ist das ein Dealbreaker, für andere völlig irrelevant, je nachdem wie man den Simulator nutzt.

Gelegentlich treten schwarze Bildschirme nach Alt-Tab auf, besonders wenn VRR aktiv ist. Das hängt meist mit der Interaktion zwischen XWayland und der adaptiven Bildwiederholrate zusammen. Und Screen Tearing kann vorkommen wenn der Compositor das Tearing Control Protokoll nicht unterstützt. Aktuelle Versionen von KDE Plasma und GNOME haben das aber im Griff, KDE seit Version sechs Punkt vier und GNOME seit Mutter neunundvierzig Punkt zwei.

Was man auf keinen Fall tun sollte: In der SDL-Umgebungsvariable für den Video-Treiber den Wert wayland erzwingen. X-Plane hat kein natives Wayland-Backend, Laminar Research testet diese Konfiguration nicht, und die Ergebnisse reichen von Abstürzen über Grafikfehler bis zu einem stillen Fallback auf XWayland. Also Finger weg.

## Wann X elf, wann Wayland?

Wer die einfachste und zuverlässigste Lösung für X-Plane will, wählt eine X-elf-Session. Am Login-Screen bei GDM, dem GNOME Display Manager, auf GNOME on Xorg klicken, bei SDDM, dem KDE Display Manager, auf Plasma X elf. Damit ist der XWayland-Overhead eliminiert, Fullscreen funktioniert sauber, Multi-Monitor ist stabil, und der Identity-Login braucht keine Workarounds. Diese Auswahl merkt sich der Display Manager, man muss sie nicht bei jedem Login wiederholen.

Wer bereits auf Wayland arbeitet und keine Probleme bemerkt, kann genauso gut bleiben. Die rund sieben Millisekunden XWayland-Overhead sind in der Praxis kaum spürbar. Die Wayland-Vorteile beim Desktop, besonders bei mehreren Monitoren mit unterschiedlichen Refresh Rates, können den kleinen Nachteil aufwiegen.

Der entscheidende Faktor ist das eigene Setup und die eigene Wahrnehmung. Wer Frame Times analysiert und jede Latenzquelle jagt, wechselt auf X elf. Wer einen modernen Desktop mit VRR und per-Monitor Refresh schätzt und X-Plane problemlos läuft, bleibt auf Wayland. Beide Wege sind legitim. Und das Beste daran: Man kann jederzeit wechseln. Einfach beim nächsten Login die andere Session auswählen, ohne irgendetwas am System zu ändern. Die Session-Wahl am Login-Screen ist der einzige Hebel, und er lässt sich jederzeit umlegen.
