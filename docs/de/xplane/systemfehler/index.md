# Systemfehler in X-Plane unter Linux

Wenn X-Plane unter Linux nicht wie erwartet funktioniert, hilft eine systematische Diagnose. Diese Seite verweist auf die relevanten Abschnitte der Dokumentation.

## Performance-Probleme

FPS-Einbrüche, Stutter und Engpässe werden behandelt in:

**[Performance](../setup_diagnose/performance.md)**

## GPU-Crashes (Device Loss)

Ein Device Loss ist ein Crash der GPU, signalisiert durch `VK_ERROR_DEVICE_LOST`. Ursachen, Debugging-Herausforderungen und die Aftermath-Diagnose werden erklärt in:

**[Geräteverluste](geraeteverluste.md)**

- Definition und Ursachen von Device Losses
- Warum GPU-Debugging schwierig ist (asynchrone Ausführung, limitierte Tools)
- `--aftermath` für detaillierte GPU-Crash-Analyse
- Häufige Missverständnisse (VRAM ist nicht die Ursache)

## Diagnose und CLI-Parameter

Log-Dateien, Safe Mode, gezielte Subsystem-Deaktivierung und reproduzierbare Benchmarks:

**[Diagnose und CLI-Parameter](diagnose.md)**

## Support

- Offizielle Dokumentation: <https://www.x-plane.com/support>
- X-Plane-Forum: <https://forums.x-plane.org> — bei Fehlermeldungen immer `Log.txt`, Fehlerbeschreibung und Reproduktionsschritte bereithalten
