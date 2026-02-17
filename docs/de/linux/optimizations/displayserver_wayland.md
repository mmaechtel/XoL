---
description: "X-Plane in einer Wayland-Session via XWayland betreiben: Latenz-Overhead, bekannte Probleme, Umgebungsvariablen und GPU-spezifische Fehlersuche."
---
# Wayland-Session mit X-Plane

Wer eine Wayland-Session für den Desktop nutzt, kann X-Plane trotzdem verwenden — über die XWayland-Kompatibilitätsschicht. Diese Seite erklärt was passiert, was zu erwarten ist und wie Probleme gelöst werden.

## Was passiert

```
Desktop  → Wayland → Compositor → GPU → Monitor   (nativ)
X-Plane  → X11 → XWayland → Compositor → GPU → Monitor   (übersetzt)
```

Desktop-Anwendungen sprechen natives Wayland und kommunizieren direkt mit dem Compositor. X-Plane kann kein Wayland — es spricht X11. XWayland springt automatisch als Übersetzer ein: ein vollständiger X11-Server, der innerhalb der Wayland-Session läuft.

X-Plane merkt keinen Unterschied. Es spricht X11 wie gewohnt. Aber der zusätzliche Übersetzungsschritt kostet Latenz und eine Extra-Bildkopie.

---

## XWayland-Overhead

XWayland verdoppelt die Eingabelatenz im Vergleich zu nativem X11 oder Wayland ungefähr (~7 ms vs. ~14 ms in Hardware-Messungen). Der genaue Overhead hängt von GPU, Display und Konfiguration ab. Detaillierte Messungen und Compositor-Vergleiche: [Display-Server-Übersicht](displayserver.md#latenz-im-vergleich).

---

## Prüfen ob X-Plane XWayland nutzt

In einer Wayland-Session sollte X-Plane als XWayland-Client erscheinen. Zur Prüfung:

```bash
# Alle X11/XWayland-Clients auflisten
xlsclients -l
```

Wenn X-Plane in der Liste erscheint, läuft es über XWayland. Falls nichts erscheint, bietet `xprop` eine weitere Prüfmöglichkeit — auf das X-Plane-Fenster klicken. Zeigt es X11-Properties an, läuft die Anwendung über XWayland.

---

## Bekannte Probleme

| Symptom | Ursache | Lösung |
|---------|---------|--------|
| Fullscreen falsche Größe/Position bei Multi-Monitor | Wayland erlaubt Anwendungen keine freie Fensterpositionierung — XWayland erbt diese Einschränkung | X-Plane im Fenstermodus starten oder zu [X11-Session](displayserver_x11.md) wechseln |
| Identity-Login schlägt fehl oder zeigt leere Seite | Browser-Komponente braucht X11-Backend | `GDK_BACKEND=x11` setzen (automatisch seit X-Plane 12.1.3) |
| X-Plane pausiert bei Workspace-Wechsel | Wayland-Compositors suspendieren nicht-sichtbare Anwendungen | Auf X-Planes Workspace bleiben oder Fenstermodus verwenden |
| Screen Tearing | Compositor unterstützt kein Tearing-Control | VSync in X-Plane aktivieren oder eine aktuelle KDE-Plasma-Version verwenden |
| Maus entweicht dem X-Plane-Fenster | Pointer Constraints nicht vollständig implementiert | `SDL_VIDEODRIVER=x11` setzen oder Fullscreen verwenden |
| Schwarzer Bildschirm nach Alt-Tab | VRR-Interaktion mit XWayland-Fullscreen | VRR deaktivieren oder Fenstermodus verwenden |

---

## Umgebungsvariablen

Diese Variablen können bei XWayland-Problemen helfen. Vor dem Start von X-Plane setzen:

```bash
# X11-Backend in SDL2 erzwingen (normalerweise automatisch)
export SDL_VIDEODRIVER=x11

# X11-Backend für GTK erzwingen (Identity-Login-Browser)
export GDK_BACKEND=x11

# Vulkan-Presentation-Mode setzen (nur Mesa-Treiber — AMD, Intel)
export MESA_VK_WSI_PRESENT_MODE=mailbox
```

Um diese dauerhaft zu setzen, in einen [Desktop-Eintrag](displayserver_x11.md#desktop-eintrag) oder das Shell-Profil eintragen.

---

## Desktop-Eintrag

Die Grundeinrichtung ist identisch mit der [X11-Session](displayserver_x11.md#desktop-eintrag). Für Wayland mit AMD- oder Intel-GPUs zusätzlich die Presentation-Mode-Variable setzen:

```ini
Exec=env SDL_VIDEODRIVER=x11 GDK_BACKEND=x11 MESA_VK_WSI_PRESENT_MODE=mailbox /path/to/X-Plane-x86_64
```

`MESA_VK_WSI_PRESENT_MODE=mailbox` gilt nur für Mesa-Treiber (AMD, Intel) und kann die Latenz unter XWayland reduzieren. NVIDIA-Nutzer sollten diese Variable weglassen.

---

## GPU-spezifische Hinweise

### AMD (RADV)

Wayland funktioniert gut auf AMD mit exzellenter Treiberunterstützung und ohne besondere Konfiguration. Wenn X-Plane in der Wayland-Session ohne Probleme läuft, gibt es keinen zwingenden Grund zu X11 zu wechseln.

### NVIDIA

Wayland auf NVIDIA erfordert aktuelle Treiber mit Explicit-Sync-Unterstützung. Ältere Treiber verursachen Grafikfehler, Input-Lag oder Abstürze unter Wayland.

**Mindestanforderungen für Wayland**

- NVIDIA-Treiber 555 oder neuer
- Kernel 6.8 oder neuer
- `nvidia_drm.modeset=1` aktiv (Standard seit Treiber 560; prüfen mit `cat /sys/module/nvidia_drm/parameters/modeset`)

Falls der Treiber älter als 555 ist, eine [X11-Session](displayserver_x11.md) verwenden — Wayland funktioniert dann nicht zuverlässig.

### Intel Arc

Intel empfiehlt offiziell Wayland für Arc-GPUs. X11/Xorg hat bekannte Rendering-Glitches auf Arc-Hardware. Bei einer Arc-GPU kann das Beibehalten der Wayland-Session (mit X-Plane über XWayland) die bessere Gesamterfahrung sein.

---

## Was ist mit nativem Wayland?

`SDL_VIDEODRIVER=wayland` zwingt SDL2, eine native Wayland-Verbindung zu versuchen. X-Plane 12 hat kein natives Wayland-Backend, und diese Konfiguration wird von Laminar Research weder getestet noch unterstützt — die Ergebnisse reichen von Abstürzen und Rendering-Fehlern bis zum stillen Zurückfallen auf XWayland.

!!! warning "Natives Wayland nicht erzwingen"
    `SDL_VIDEODRIVER=wayland` ist für X-Plane **nicht empfohlen**. X-Plane 12 hat kein natives Wayland-Backend und diese Konfiguration liefert unvorhersehbare Ergebnisse. Bei Problemen ist der erste Troubleshooting-Schritt, diese Variable zu entfernen.

---

## Wann zu X11 wechseln

Ein Wechsel zu einer [X11-Session](displayserver_x11.md) sollte erwogen werden bei:

- Anhaltenden Fullscreen- oder Multi-Monitor-Problemen
- Spürbarer Eingabelatenz im Vergleich zu Windows oder X11
- NVIDIA-GPU mit Treibern älter als 555
- Wunsch nach dem einfachsten, zuverlässigsten X-Plane-Setup

Für Nutzer mit funktionierendem Wayland-Desktop ohne X-Plane-Probleme ist es in Ordnung, auf Wayland zu bleiben.

---

## Weiterführende Kapitel

| Thema | Seite | Schwerpunkt |
|---|---|---|
| Display-Server-Übersicht | [Display-Server](displayserver.md) | Protokollvergleich und Latenzmessungen |
| X11-Session | [X11-Session](displayserver_x11.md) | Alternative: direktes X11 ohne XWayland-Overhead |
| Nvidia-Treiber | [Nvidia-Treiber](nvidia.md) | Wayland-Treiberanforderungen (Explicit Sync) |
| Latenz und Vorhersagbarkeit | [Latenz und Vorhersagbarkeit](../../fundamentals/performance/latency.md) | XWayland-Latenz-Overhead verstehen |
| Konfiguration | [Konfiguration](../../xplane/setup_diagnose/config.md) | X-Plane Display- und Rendering-Einstellungen |
