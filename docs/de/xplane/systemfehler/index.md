# Systemfehler in X-Plane unter Linux

Wenn X-Plane unter Linux nicht wie erwartet funktioniert, hilft eine systematische Diagnose. Diese Seite verweist auf die relevanten Abschnitte der Dokumentation.

## Diagnose und CLI-Parameter

Die Kommandozeile ist unter Linux das mächtigste Werkzeug zur Fehlersuche. Log-Dateien, Safe Mode, gezielte Subsystem-Deaktivierung und reproduzierbare Benchmarks werden ausführlich behandelt in:

**[Konfiguration → Fehlerbehebung](../config.md#fehlerbehebung)**

- Log-Dateien lesen und interpretieren (`Log.txt`, Rotation, was suchen)
- Safe Mode mit `--safe_mode=GFX`, `--safe_mode=PLG` etc.
- Audio isolieren (`--no_sound`), Controller isolieren (`--no_joysticks`)
- Fullscreen-Probleme unter Wayland (`--window`, `--full`)
- Performance-Tests (`--fps_test`, `--require_fps`)
- Launch-Scripte mit Profilen (`--pref`, `--dref`)

## GPU-Crashes (Device Loss)

Ein Device Loss ist ein Crash der GPU, signalisiert durch `VK_ERROR_DEVICE_LOST`. Ursachen, Debugging-Herausforderungen und die Aftermath-Diagnose werden erklärt in:

**[Geräteverluste](geraeteverluste.md)**

- Definition und Ursachen von Device Losses
- Warum GPU-Debugging schwierig ist (asynchrone Ausführung, limitierte Tools)
- `--aftermath` für detaillierte GPU-Crash-Analyse
- Häufige Missverständnisse (VRAM ist nicht die Ursache)

## Performance-Probleme

FPS-Einbrüche, Stutter und Engpässe werden behandelt in:

**[Performance](../performance.md)**

## Support

- Offizielle Dokumentation: <https://www.x-plane.com/support>
- X-Plane-Forum: <https://forums.x-plane.org> — bei Fehlermeldungen immer `Log.txt`, Fehlerbeschreibung und Reproduktionsschritte bereithalten
