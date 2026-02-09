# Lektorat: config.md — Redaktionelle Empfehlungen

Dieses Dokument ist das Briefing für die Umsetzung (Phase 3). Es bewertet jeden Abschnitt aus dem Research-Paper auf seinen **tatsächlichen Mehrwert** für die Zielgruppe und gibt konkrete Empfehlungen zu Umfang, Tiefe und Tonalität.

---

## Zielgruppe und Leitfrage

**Leser:** Linux-Nutzer, der X-Plane 12 bereits installiert hat und fliegen will. Hat grundlegende Linux-Kenntnisse (Terminal, Pakete installieren). Ist kein Entwickler, aber technikaffin.

**Leitfrage bei jedem Abschnitt:** *Würde ein Linux-Nutzer das selbst herausfinden, indem er die offizielle X-Plane-Doku liest? Wenn ja → weglassen. Wenn nein → das ist unser Mehrwert.*

**Tonalität:** Sachlich-pragmatisch, keine Textbuch-Erklärungen. Direkte Handlungsanweisungen bevorzugen. "Mach X, weil Y" statt "X ist ein Konzept, das..."

---

## Abschnitt-für-Abschnitt-Bewertung

### 1. Vulkan unter Linux

**Empfehlung: KURZ halten (5-8 Sätze max)**

| Unterthema | Mehrwert? | Empfehlung |
|------------|-----------|------------|
| "Vulkan ist einzige API" | Gering — steht in den System Requirements | 1 Satz: "X-Plane 12 nutzt ausschließlich Vulkan." Fertig. |
| Treiber-Mindestversionen | Mittel — aber besser als Verweis auf nvidia.md / (zukünftig) mesa.md | Kurze Tabelle (3 Zeilen), Verweis auf Treiberseiten |
| Zink | **HOCH** — das findet niemand in der offiziellen Doku | Eigener Unterabschnitt, erklären was es ist, warum AMD-Nutzer profitieren, wann es Probleme macht |
| RADV vs. NVIDIA | Gering — gehört in mesa.md / nvidia.md | Weglassen, Verweis genügt |

**Redaktionelle Entscheidung:** Zink ist die Geschichte hier. Der Rest ist Kontext. Das Ben-Supnik-Zitat weglassen — wirkt wie Lückenfüller.

---

### 2. Shader-Cache

**Empfehlung: ÜBERNEHMEN, praxisnah formulieren**

| Unterthema | Mehrwert? | Empfehlung |
|------------|-----------|------------|
| Zwei separate Cache-Systeme | **HOCH** — das steht nirgends gesammelt | Klar erklären: XP hat seinen eigenen, Mesa hat einen zweiten |
| Pfade | **HOCH** — "wo muss ich löschen wenn was kaputt ist?" | Exakte Pfade, Copy-Paste-fähig |
| Mesa Cache auf SSD umleiten | Mittel — Nischenthema | Kurzer Hinweis mit Env-Variable |
| Wann löschen? | **HOCH** — häufige Frage | Konkrete Symptome nennen: "Wenn nach Treiberupdate Grafikfehler auftreten" |

**Redaktionelle Entscheidung:** Fokus auf "Was mache ich wenn...?" — nicht auf Architektur-Erklärung.

---

### 3. Umgebungsvariablen

**Empfehlung: SELEKTIV — nur was nachweislich hilft**

| Variable | Mehrwert? | Empfehlung |
|----------|-----------|------------|
| `MESA_SHADER_CACHE_DIR` | Mittel | Übernehmen als Tipp |
| `MESA_SHADER_CACHE_MAX_SIZE` | Mittel | Übernehmen als Tipp |
| `MESA_VK_WSI_PRESENT_MODE` | **HOCH** — Tearing-Lösung für AMD-Nutzer | Übernehmen mit Erklärung: mailbox vs. immediate |
| `RADV_TEX_ANISO` | Gering — X-Plane hat eigenen Aniso-Slider | Weglassen |
| `RADV_FORCE_VRS` | **NICHT übernehmen** — nicht mit X-Plane getestet, könnte Artefakte erzeugen | Erwähnen als "experimentell", keine Empfehlung |
| `__GL_*` (NVIDIA) | **Anti-Mehrwert** — Leser probiert es aus und wundert sich warum nichts passiert | Übernehmen als "Diese Variablen sind irrelevant für X-Plane 12" — spart Suchzeit |

**Redaktionelle Entscheidung:** Keine Riesen-Tabelle. Nur 3-4 Variablen die tatsächlich helfen, mit konkretem Anwendungsfall. Die NVIDIA-Warnung ist Mehrwert durch Verhinderung von Zeitverschwendung.

---

### 4. Display-Server (X11 vs. Wayland)

**Empfehlung: KNAPP — Verweis auf zukünftige wayland.md**

| Unterthema | Mehrwert? | Empfehlung |
|------------|-----------|------------|
| "X11 empfohlen" | **HOCH** — klare Handlungsempfehlung | 2-3 Sätze: X-Plane hat kein natives Wayland, XWayland hat Overhead, X11 bevorzugen |
| Compositor-Bypass erklärt | Gering — zu technisch für die Zielgruppe | 1 Satz reicht |
| Bekannte Wayland-Probleme | Mittel — aber alles behoben | Weglassen — die Bug-Tabelle am Ende deckt das ab |
| Wie prüfe ich meinen Display-Server? | **HOCH** — praktische Hilfe | `echo $XDG_SESSION_TYPE` als Quick-Check |

**Redaktionelle Entscheidung:** Admonition-Box ("Tipp"), kein eigener großer Abschnitt. Wird ohnehin eine eigene wayland.md bekommen.

---

### 5. Audio

**Empfehlung: KNAPP — nur das PipeWire-Problem**

| Unterthema | Mehrwert? | Empfehlung |
|------------|-----------|------------|
| "FMOD ist Audio-Engine" | Gering — irrelevant für den Nutzer | Weglassen oder 1 Satz |
| PipeWire-Workaround | **HOCH** — konkretes Linux-Problem mit Lösung | Übernehmen mit Befehlen |
| OpenAL Soft | Gering — Legacy, betrifft kaum jemanden | Weglassen |
| `--no_sound` als Diagnose | **HOCH** — steht im CLI-Abschnitt, hier querverweisen | Verweis |

**Redaktionelle Entscheidung:** 1 Admonition-Box mit dem PipeWire-Fix. Nicht mehr. Audio bekommt eine eigene Seite.

---

### 6. Controller

**Empfehlung: SELEKTIV — nur die Linux-Fallstricke**

| Unterthema | Mehrwert? | Empfehlung |
|------------|-----------|------------|
| SDL2/HIDAPI/evdev Erklärung | Gering — zu technisch, hilft nicht direkt | 1 Satz Kontext, mehr nicht |
| udev-Regeln | **HOCH** — DAS Linux-Controller-Problem Nr. 1 | Übernehmen, aber Verweis auf offizielle Anleitung statt Regel kopieren |
| Konfigurationsdateien und Pfade | Mittel — nützlich für Backup | Pfade-Tabelle übernehmen |
| .joy-Dateien die mitgeliefert werden | Gering — irrelevant | Weglassen |
| Bekannte Probleme | **HOCH** — "Gerät verschwindet nach Standby" ist klassisch | Die 3-4 häufigsten Probleme mit Lösung |
| `--no_joysticks` als Diagnose | **HOCH** | Verweis auf CLI-Abschnitt |

**Redaktionelle Entscheidung:** Fokus: "Dein Controller geht nicht? Hier ist warum und wie du es fixst." Wird ohnehin eine eigene input_devices.md geben.

---

### 7. Debugging

**Empfehlung: DAS HERZSTÜCK — hier liegt der größte Mehrwert**

| Unterthema | Mehrwert? | Empfehlung |
|------------|-----------|------------|
| Log.txt Pfad und Rotation | **HOCH** — ab 12.2.0 geändert, kaum dokumentiert | Übernehmen |
| CLI-Parameter mit Linux-Anwendungsfällen | **SEHR HOCH** — DER Mehrwert dieser Seite | Vollständig übernehmen. Nicht Parameter erklären, sondern Szenarien: "Plugin crasht? → `--safe_mode=PLG`" |
| `--safe_mode` granulare Optionen | **SEHR HOCH** — in offizieller Doku kaum erklärt | Detailliert mit Beispielen |
| `--pref` und `--dref` | **HOCH** — Launch-Scripte sind Linux-Stärke | Beispiel-Script zeigen |
| Benchmark-Modus | **HOCH** — reproduzierbare Tests, Scripting | Übernehmen mit Beispiel |
| Vulkan Validation Layers | Mittel — nur für Entwickler | Kurz, mit Warnung |
| Aftermath | **HOCH** — kennt kaum jemand | Übernehmen: wann nutzen, was es bringt |
| GDB | Mittel — Nische, aber genau der Typ Nutzer den wir ansprechen | Übernehmen als "Fortgeschritten"-Abschnitt |
| DataRef-Debugging | Gering — gehört in performance.md oder plugins.md | Weglassen oder kurzer Verweis |

**Redaktionelle Entscheidung:** Diesen Abschnitt als Stärke der Seite spielen. Szenario-basiert aufbauen:

1. "X-Plane startet nicht" → `--safe_mode`, Log.txt prüfen
2. "Schlechte Performance" → `--fps_test`, Benchmark-Scripting
3. "Grafikfehler / Device Loss" → `--aftermath`, Validation Layers
4. "Plugin-Problem" → `--safe_mode=PLG`, `--debug_gl`
5. "Crash" → GDB, Core Dumps

---

### 8. Bekannte Linux-Bugs

**Empfehlung: ÜBERNEHMEN, aber anders aufbereiten**

Die Tabelle aus dem Research-Paper ist eine Auflistung. Für den Leser nützlicher wäre eine **Gruppierung nach Symptom:**

| Symptom | Mögliche Ursache | Fix / Workaround | Behoben in |
|---------|-------------------|------------------|------------|
| X-Plane startet nicht | AMD GPU + älterer Mesa | Mesa aktualisieren | 12.2.0 |
| X-Plane startet nicht | Ubuntu 24.10 + NVIDIA | NVIDIA-Treiber aktualisieren | 12.2.0 |
| Hängt beim Start | IPv6 + Kernel 6.9+ | Netzwerk deaktivieren oder updaten | 12.1.0 |
| Kein Vollbild | XWayland / bestimmte DEs | `--window=` nutzen, X11 wechseln | 12.2.0 |
| Grafikfehler (Wasser, Vegetation) | AMD GPU | X-Plane aktualisieren | 12.2.0 |
| Screenshot-Fehler | AMD GPU | X-Plane aktualisieren | 12.3.0 |

**Redaktionelle Entscheidung:** Nur Bugs die den Leser **heute noch treffen könnten** (weil er eine ältere Version hat). Rein historische Bugs (die jeder mit aktuellem XP nicht mehr sieht) → weglassen oder in einen eingeklappten "Historisch"-Block.

---

### 9. Performance-Monitoring-Tools

**Empfehlung: KNAPP — Verweis auf performance.md**

Die performance.md behandelt das Thema bereits. Hier nur den **Linux-spezifischen Aspekt** ergänzen:

- `nvidia-smi` / `radeontop` / `intel_gpu_top` → 1 Satz pro Tool (kennt die Zielgruppe vermutlich)
- MangoHud → kurzer Hinweis, Verweis auf nvidia.md wo es bereits erwähnt wird
- `GALLIUM_HUD` → weglassen (zu nischig)

---

## Seitenstruktur: Empfohlener Aufbau

```
# X-Plane Konfiguration unter Linux

(Einleitung: 2-3 Sätze. "X-Plane 12 ist eine Cross-Plattform-Anwendung.
Die allgemeinen Grafikeinstellungen sind in der offiziellen Doku beschrieben.
Diese Seite behandelt ausschließlich, was unter Linux anders ist.")

## Vulkan und Zink
(Kurzer Kontext + Zink-Erklärung mit Performance-Zahlen)

## Shader-Cache
(Zwei Caches, Pfade, wann löschen)

## Umgebungsvariablen
(3-4 nützliche Variablen, NVIDIA-Warnung)

## Display-Server
(X11 empfohlen, Quick-Check, Verweis)

## Audio
(PipeWire-Fix, fertig)

## Controller
(udev ist Pflicht, häufige Probleme)

## Fehlerbehebung                          ← Hauptabschnitt, größter Mehrwert
### Log-Dateien
### Diagnose-Start mit CLI-Parametern      ← szenariobasiert
### GPU-Debugging (Aftermath, Validation)
### Crash-Analyse (GDB)

## Bekannte Probleme
(Symptom-basierte Tabelle)
```

---

## Gewichtung der Abschnitte (Zeichenbudget-Empfehlung)

| Abschnitt | Anteil | Begründung |
|-----------|--------|------------|
| Vulkan und Zink | 10% | Kurz, Kontext |
| Shader-Cache | 10% | Praxisnah, kompakt |
| Umgebungsvariablen | 8% | Wenige, aber wichtige |
| Display-Server | 5% | Admonition, Verweis |
| Audio | 5% | Admonition, Verweis |
| Controller | 10% | Häufiges Problem, aber knapp |
| **Fehlerbehebung** | **35%** | **Herzstück, größter Mehrwert** |
| Bekannte Probleme | 12% | Symptom-Tabelle |
| Einleitung + Verweise | 5% | Kurz |

---

## Was NICHT auf diese Seite gehört

| Thema | Warum nicht | Wo stattdessen |
|-------|------------|-----------------|
| Grafikeinstellungen (Texture, Shadows etc.) | Plattformunabhängig, offizielle Doku | Verweis auf x-plane.com/kb |
| GPU-Einstellungsprofile | Keine offiziellen Daten, zu spekulativ | Nirgends — nicht übernehmen |
| AA/PBR-Theorie (aktueller Inhalt) | Akademisch, kein Handlungswert | Entfernen |
| .joy-Dateiformat-Spezifikation | Zu detailliert, Nische | Zukünftige input_devices.md |
| FMOD-Architektur | Irrelevant für Endnutzer | Nirgends |
| DataRef-Vollständig | Entwickler-Thema | performance.md oder plugins.md |
| "Wie installiere ich X-Plane" | Andere Seite (begin.md) | — |
| Allgemeine Linux-Grundlagen | Vorwissen der Zielgruppe | — |

---

## Querverweise (in der fertigen Seite)

| Stelle in config.md | Verweis auf | Art |
|---------------------|-------------|-----|
| Vulkan-Treiber NVIDIA | nvidia.md | Inline-Link |
| Vulkan-Treiber AMD/Intel | "(geplant: mesa.md)" | Hinweis |
| Display-Server | "(geplant: wayland.md)" | Hinweis |
| Audio | "(geplant: audio.md)" | Hinweis |
| Controller | "(geplant: input_devices.md)" | Hinweis |
| Performance-Monitoring | performance.md | Inline-Link |
| CPU-Governor, USB-Autosuspend | systemtuning.md | Inline-Link |
| MangoHud | nvidia.md | Inline-Link |

---

## Glossar-Einträge

Nur Begriffe, die der Leser auf **dieser Seite** zum ersten Mal sieht:

| Begriff | Nötig? | Begründung |
|---------|--------|------------|
| Zink | **Ja** | Nicht allgemein bekannt, zentral für die Seite |
| FMOD | **Ja** | Wird erwähnt, kurze Erklärung hilft |
| evdev | **Ja** | Linux-Input-Subsystem, nicht jedem geläufig |
| RADV | **Ja** | Mesa-Vulkan-Treiber, Abgrenzung zu proprietär |
| ACO | **Nein** | Zu technisch, wird nicht auf der Seite erklärt |

---

## Zusammenfassung für den Lektor

1. **Das Herzstück dieser Seite ist der Fehlerbehebungs-Abschnitt.** Dort liegt der meiste Mehrwert gegenüber der offiziellen Doku. Szenariobasiert aufbauen, nicht als Parameterliste.

2. **Alles andere ist Zuarbeit** — knapp halten, damit der Leser schnell zu den Informationen kommt, die er sonst nirgends findet.

3. **Bestehendes komplett ersetzen.** Die aktuelle config.md mit AA-Theorie und Aufzählungs-Stichpunkten hat keinen Mehrwert. Kein Versuch, Teile zu retten.

4. **Jeder Abschnitt muss die Frage beantworten:** "Was muss ich als Linux-Nutzer anders machen als ein Windows-Nutzer?" Wenn die Antwort "nichts" ist → weglassen.

5. **Keine Erklärungen von Dingen, die der Leser googeln kann.** Kein "Was ist Vulkan?", kein "Was ist PipeWire?". Stattdessen: "Hier ist das Problem, hier ist die Lösung."
