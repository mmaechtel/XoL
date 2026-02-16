# Geräteverluste in X-Plane

## Einleitung

Geräteverluste („device losses") sind ein bekanntes, jedoch schwer zu analysierendes Problem in X-Plane. Ziel ist es, die Natur von Geräteverlusten, ihre Ursachen, Herausforderungen beim Debugging und Maßnahmen zur Problemlösung zu erläutern.

## Definition und Ursachen

Ein Geräteverlust ist ein Absturz der Grafikprozessoreinheit (GPU), vergleichbar mit einem Softwareabsturz auf der CPU, jedoch mit spezifischen Herausforderungen. GPUs führen Shader aus – kleine Programme, die Aufgaben wie die Transformation von Vertexdaten, Pixelberechnungen oder das Culling von Objekten übernehmen. X-Plane nutzt zahlreiche Shader-Module, die jeweils viele Shader-Varianten enthalten. Ein Geräteverlust tritt auf, wenn ein Shader oder ein GPU-Befehl fehlerhaft ausgeführt wird, signalisiert durch den Vulkan-Fehlercode `VK_ERROR_DEVICE_LOST`.

## Herausforderungen beim Debugging

Das Debugging von Geräteverlusten ist komplex aufgrund folgender Faktoren:

1. **Asynchrone Ausführung**: CPU und GPU arbeiten asynchron, wobei die CPU oft mehrere Frames voraus ist. Ein Absturz wird erst verzögert erkannt, was die Ursachenanalyse erschwert.
2. **Begrenzte Debugging-Tools**: Shader können nicht schrittweise inspiziert werden. Der GPU-Zustand ist nur nach der Ausführung zugänglich, bei einem Absturz stehen oft nur fragmentierte Daten zur Verfügung.
3. **Latenz bei der Erkennung**: Das Betriebssystem und der Grafiktreiber priorisieren die Wiederherstellung der GPU, was zu Verzögerungen und visuellen Artefakten führt, bevor X-Plane den Fehler registriert.

## Maßnahmen zur Problemlösung

Zur Untersuchung von Geräteverlusten wird der Kommandozeilenparameter `--aftermath` empfohlen (siehe auch [Konfiguration → GPU-Debugging](../config.md#gpu-debugging) für den schnellen CLI-Einstieg). Dies aktiviert die Aftermath-Bibliothek (unterstützt für Nvidia, AMD und Intel GPUs), die detaillierte Diagnosedaten sammelt. Bei einem Absturz wird die Meldung "Encountered a GPU crash!" angezeigt, und die gesammelten Daten unterstützen Entwickler bei der Ursachenfindung. Aftermath verursacht jedoch einen Leistungseinbruch und sollte gezielt eingesetzt werden.

In X-Plane 12.2 wurde die Aftermath-Unterstützung überarbeitet, um pro Zeichen- oder Dispatch-Befehl Checkpoints in den Befehlsstrom einzufügen. Diese feingranularen Daten ermöglichen eine präzisere Analyse des GPU-Zustands nach einem Absturz. Frühere Versionen wie 12.06 und 12.1.0 reduzierten Geräteverluste signifikant, etwa durch Workarounds für Nvidia-Treiberfehler.

## Missverständnisse

Ein häufiges Missverständnis ist, dass Geräteverluste durch unzureichenden Videospeicher (VRAM) verursacht werden – dies ist nicht der Fall. Plugins oder Szenerien können nur indirekt Geräteverluste auslösen, etwa durch Modifikationen an Shader-Pfaden. A/B-Tests mit deaktivierten Plugins sind bei reproduzierbaren Abstürzen hilfreich, bei seltenen Geräteverlusten jedoch oft ineffektiv.

## Fazit

Geräteverluste in X-Plane sind GPU-Abstürze, die durch die Komplexität von Shadern und die asynchrone CPU-GPU-Interaktion schwer zu debuggen sind. Werkzeuge wie Aftermath und verbesserte Implementierungen in X-Plane 12.2 erleichtern die Diagnose. Nutzer können durch das Einreichen von Absturzberichten mit aktiviertem Aftermath zur Problemlösung beitragen. Zukünftige Entwicklungen könnten die Häufigkeit solcher Fehler weiter reduzieren.

## Literatur

- "What's up with device losses in X-Plane anyways?". Verfügbar unter: <https://developer.x-plane.com>. Zugriff: 2024-05-09. 