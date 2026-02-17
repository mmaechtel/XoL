# Systemfehler in X-Plane unter Linux

Wenn X-Plane unter Linux nicht wie erwartet funktioniert, hilft systematisches Eingrenzen. Device Losses — GPU-Crashes mit dem Vulkan-Fehlercode `VK_ERROR_DEVICE_LOST` — sind besonders schwer zu analysieren, weil CPU und GPU asynchron arbeiten und der Crash erst mit Verzögerung erkannt wird. Das Aftermath-Tool injiziert Checkpoints in den GPU-Befehlsstrom und rekonstruiert den Zustand zum Zeitpunkt des Fehlers. CLI-Parameter wie Safe Mode und Subsystem-Isolierung grenzen die Ursache systematisch ein.

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
