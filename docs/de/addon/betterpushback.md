# Better Pushback

Better Pushback ist ein [Plugin](../glossary.md#plugin) für [X-Plane](../glossary.md#x-plane) 11/12, das realistische Pushback-Operationen mit Route-Planer, 3D-Schleppfahrzeug und mehrsprachiger Sprachausgabe simuliert.

## Hintergrund

- **Original:** [skiselkov/BetterPushbackC](https://github.com/skiselkov/BetterPushbackC) (archiviert seit Dezember 2025)
- **Empfohlener Fork:** [olivierbutler/BetterPusbackMod](https://github.com/olivierbutler/BetterPusbackMod) (aktiv gepflegt)
- **Lizenz:** CDDL 1.0 (Open Source)
- **Plattformen:** Windows, macOS, Linux (native Binaries)
- **Kompatibilität:** X-Plane 11 und X-Plane 12
- **Preis:** Kostenlos

Das Original-Repository wird nicht mehr gepflegt. Der olivierbutler-Fork (BetterPusbackMod) ist der empfohlene Download für X-Plane 12, mit Funktionserweiterungen wie manuellem Push-Modus und Magic-Squares-Shortcuts.

## Funktionsumfang

- **Overhead-Planungsansicht:** Vogelperspektive auf das Vorfeld, Pushback-Route per Mausklick zeichnen (Kurven, Geraden, Richtungswechsel)
- **Vollautomatischer Pushback:** Nach Routenplanung läuft der Pushback autonom — der Pilot kann sich auf das Startup-Verfahren konzentrieren
- **Manueller Modus:** Pushback ohne Vorausplanung, Steuerung per Joystick-Buttons oder Tasten (nur Mod-Fork)
- **Vorwärtsschleppen:** Flugzeug kann auch vorwärts geschleppt werden
- **3D-Schleppfahrzeug:** Animiertes Tug-Modell mit korrekter Physik-Simulation
- **Mehrsprachige Ground Crew:** Sprachausgabe in verschiedenen Sprachen simuliert lokales Bodenpersonal
- **Magic Squares:** Schnellzugriff-Buttons für häufige Operationen (nur Mod-Fork)

## Mehrwert in der Flugsimulation

Better Pushback ersetzt die rudimentäre Standard-Pushback-Funktion von X-Plane durch eine realistische Alternative. Die Routenplanung per Overhead-View ermöglicht präzise Pushback-Pfade um Hindernisse herum. Im automatischen Modus kann das Startup-Verfahren parallel zum Pushback abgearbeitet werden. Der manuelle Modus eignet sich für schnelle Repositionierungen ohne Vorausplanung.

## Installation

**Download:** [GitHub Releases (olivierbutler-Fork)](https://github.com/olivierbutler/BetterPusbackMod/releases) oder [forums.x-plane.org](https://forums.x-plane.org/files/file/90556-better-pushback-for-x-plane-1112/)

Die ZIP-Datei nach `Resources/plugins/` entpacken. Es entsteht der Ordner `BetterPushback/` mit der Linux-Binary unter `lin_x64/BetterPushback.xpl`.

Alle Abhängigkeiten sind statisch gelinkt — es werden keine zusätzlichen Systempakete benötigt.

**Hinweise:**

- Bei Updates immer den gesamten `BetterPushback/`-Ordner ersetzen (nicht nur die Binary)
- Das Plugin-Verzeichnis darf kein Symlink sein — bei Symlinks lädt das Plugin nicht (ohne Fehlermeldung)

### ALSOFT Real-Time-Priority-Warnung

Im `Log.txt` kann folgende Meldung erscheinen:

```
[ALSOFT] (EE) Failed to set real-time priority for thread: Operation not permitted (1)
```

Diese Warnung ist nicht-fatal und beeinträchtigt die Audio-Wiedergabe nicht. Die eingebettete openal-soft-Bibliothek versucht, Realtime-Scheduling für Audio-Threads zu setzen, wofür standardmäßig die Berechtigung fehlt. Reagiert das Plugin trotz dieser Warnung nicht, sollten andere Ursachen geprüft werden (z.B. Konflikte mit Flugzeug-Plugins).

## Quellen

- [BetterPusbackMod — GitHub (olivierbutler-Fork)](https://github.com/olivierbutler/BetterPusbackMod)
- [BetterPushbackC — GitHub (Original, archiviert)](https://github.com/skiselkov/BetterPushbackC)
- [Better Pushback — forums.x-plane.org](https://forums.x-plane.org/files/file/90556-better-pushback-for-x-plane-1112/)
