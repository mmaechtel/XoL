# Diagnose und CLI-Parameter

Die Kommandozeile ist unter Linux das mächtigste Werkzeug zur Fehlersuche. Log-Dateien, Safe Mode, gezielte Subsystem-Deaktivierung und reproduzierbare Benchmarks werden ausführlich behandelt in:

**[Konfiguration → Fehlerbehebung](../setup_diagnose/config.md#fehlerbehebung)**

- Log-Dateien lesen und interpretieren (`Log.txt`, Rotation, was suchen)
- Safe Mode mit `--safe_mode=GFX`, `--safe_mode=PLG` etc.
- Audio isolieren (`--no_sound`), Controller isolieren (`--no_joysticks`)
- Fullscreen-Probleme unter Wayland (`--window`, `--full`)
- Performance-Tests (`--fps_test`, `--require_fps`)
- Launch-Scripte mit Profilen (`--pref`, `--dref`)
