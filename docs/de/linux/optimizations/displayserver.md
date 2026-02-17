# Display-Server

X-Plane 12 hat keine native Wayland-Unterstützung. Wie es sich mit dem Bildschirm verbindet, hängt davon ab, welche Display-Server-Session am Login-Screen gewählt wird. Diese Seite erklärt die drei beteiligten Protokolle und hilft bei der Entscheidung.

<div class="video-container" markdown>
<video controls width="100%" preload="metadata" aria-label="Video: X11 vs. Wayland für X-Plane" poster="../../../assets/video/de/X11_vs_Wayland/X11_vs_Wayland.jpg">
  <source src="../../../assets/video/de/X11_vs_Wayland/X11_vs_Wayland.mp4" type="video/mp4">
</video>
</div>

## Drei Protokolle

### X11 (Xorg)

Das klassische Display-Server-Protokoll, entwickelt seit 1984 (X11-Version von 1987). Ein zentraler X-Server verwaltet alle Grafik- und Eingabeoperationen. Anwendungen senden Zeichenbefehle an den Server, der alles rendert und an die GPU weiterleitet.

X-Plane spricht X11 nativ. In einer X11-Session kommuniziert X-Plane direkt mit dem X-Server — keine Übersetzung, kein Overhead.

### Wayland

Der moderne Nachfolger von X11. Statt eines zentralen Servers übernimmt der **Compositor** (z.B. Mutter bei GNOME, KWin bei KDE) die Rolle von Display-Server und Fenstermanager gleichzeitig. Anwendungen rendern direkt in GPU-Puffer und übergeben sie dem Compositor.

Wayland bietet Per-Monitor-Refresh-Rates und native VRR-Unterstützung (Variable Refresh Rate). Wayland ist seit Debian 10 die Standard-Session für GNOME. Für KDE wird Wayland ab Debian 13 (Plasma 6) der Standard.

X-Plane **kann** kein natives Wayland.

### XWayland

Eine Kompatibilitätsschicht — ein vollständiger X11-Server, der **innerhalb** einer Wayland-Session läuft. Wenn eine X11-Anwendung (wie X-Plane) auf einem Wayland-Desktop startet, übernimmt XWayland automatisch die Übersetzung zwischen X11 und dem Wayland-Compositor.

Die Anwendung merkt keinen Unterschied — sie spricht X11 wie gewohnt. Aber der zusätzliche Übersetzungsschritt kostet Latenz und eine Extra-Bildkopie bei Fenster-Anwendungen.

---

## Was passiert bei X-Plane?

| | X11-Session | Wayland-Session |
|---|---|---|
| **Desktop-Apps** | X11 → X-Server → GPU | Wayland → Compositor → GPU |
| **X-Plane** | X11 → X-Server → GPU | X11 → XWayland → Compositor → GPU |
| **Extra-Overhead** | Keiner | ~7 ms Latenz, Extra-Bildkopie |
| **Fullscreen** | Compositor-Bypass möglich | XWayland-Fullscreen eingeschränkt |
| **Multi-Monitor** | Alle Monitore teilen eine Refresh-Rate | Per-Monitor-Refresh-Rate, aber XWayland-Fullscreen problematisch |
| **Joysticks/HOTAS** | `/dev/input` (Kernel direkt) | `/dev/input` (Kernel direkt) |

Joysticks, Throttles und Ruderpedale umgehen den Display-Server komplett. Sie kommunizieren direkt mit dem Kernel über `/dev/input`. Die Wahl des Display-Servers hat **keinen Einfluss** auf Flug-Peripherie.

!!! tip "Empfehlung"
    Eine **X11-Session** für X-Plane verwenden. Das eliminiert den XWayland-Overhead und bietet das zuverlässigste Fullscreen- und Multi-Monitor-Verhalten. Details: [X11-Session für X-Plane](displayserver_x11.md)

    Wer Wayland für den Desktop behalten möchte: X-Plane funktioniert über XWayland — mit einigen Einschränkungen. Details: [Wayland-Session mit X-Plane](displayserver_wayland.md)

---

## Latenz im Vergleich

### Hardware-Messungen (David Justo)

Testaufbau: AMD Ryzen 9 9950X3D, NVIDIA RTX 4090, Dell AW2725DF 360 Hz OLED

| Display-Server | Input-to-Photon-Latenz |
|----------------|-------------------------------|
| X11 | 6,88 ms |
| Natives Wayland | 7,14 ms |
| XWayland | 14,45 ms |
| Windows 11 | 6,91 ms |

Natives Wayland liegt gleichauf mit X11. XWayland **verdoppelt** die Eingabelatenz durch die Übersetzungsschicht.

### Compositor-Latenz (Xaver Hugl, KDE-Entwickler)

Messungen bei 120 Hz mit verschiedenen Vulkan-Presentation-Modes

| Konfiguration | FIFO (VSync) | Mailbox | Immediate (Tearing) |
|---------------|-------------|---------|---------------------|
| X11 mit Compositor | 59 ms | 37 ms | — |
| X11 ohne Compositor | 41 ms | 38 ms | 19 ms |
| Wayland | 49 ms | 36 ms | 20 ms |
| XWayland | 49 ms | 38 ms | 20 ms |

Wayland mit aktivem Compositor erreicht die Werte von X11 **ohne** Compositor bei Mailbox und Immediate. Im VSync-Modus (FIFO) fügt X11 mit Compositor einen vollen Frame Latenz hinzu. Im Mailbox-Modus verschwindet der Unterschied.

??? abstract "Zu diesen Messungen"

    Die Messungen von David Justo verwenden einen Hardware-Sensor (Arduino Pro Micro + TEMT6000-Fototransistor) für die tatsächliche Input-to-Photon-Latenz. Testanwendung: Counter-Strike 2 (400 fps Engine-Cap, VSync aus, VRR aus, Allow Tearing an). Testbedingungen: KWin 6.5.4, NVIDIA-Treiber 580.119.02, Fedora 43, 100 Messungen pro Konfiguration.

    Die Messungen von Xaver Hugl stammen vom KDE-Compositor-Entwickler und vergleichen Presentation-Modes auf einem 120-Hz-Display.

    Beide Messreihen wurden mit aktueller Hardware und aktuellen Treibern durchgeführt. Die Ergebnisse können auf älteren Systemen abweichen.

---

## GPU-Empfehlungen

| GPU | Wayland-Desktop | X-Plane-Session | Hinweise |
|-----|----------------|-----------------|----------|
| **AMD (RADV)** | Ausgereift | X11 empfohlen | Wayland-Desktop funktioniert problemlos, aber X-Plane geht trotzdem über XWayland |
| **NVIDIA** | Gut (Treiber 555+) | X11 empfohlen | Ältere Treiber (<555): X11-Session Pflicht. Aktuelle Treiber: Wayland-Desktop möglich |
| **Intel Arc** | Ausgereift | X11 empfohlen | Intel empfiehlt offiziell Wayland für den Desktop. X11 hat bekannte Rendering-Glitches auf Arc |

Die GPU-Empfehlung betrifft die **Desktop-Session**, nicht X-Plane selbst. X-Plane spricht immer X11 — entweder direkt (X11-Session) oder über XWayland (Wayland-Session).

!!! note "Intel Arc: Sonderfall"
    Intel Arc GPUs haben bekannte Rendering-Glitches unter X11/Xorg. Bei einer Arc-GPU kann eine Wayland-Session die bessere Wahl für den Desktop sein, auch wenn X-Plane dann über den XWayland-Umweg läuft.

---

## Eingabegeräte

### Joysticks, Throttles, Ruderpedale

Flug-Peripherie ist von der Display-Server-Wahl **nicht betroffen**. Sie kommuniziert direkt mit dem Linux-Kernel:

- Zugriff über `/dev/input/eventX` (evdev-Interface)
- Zugriff über `/dev/input/jsX` (Legacy Joystick-API)
- Verwaltet vom Kernel, nicht von Wayland oder X11
- libinput handhabt explizit keine Joysticks

Thrustmaster, VKB, Virpil oder Logitech-Hardware funktioniert identisch unter X11 und Wayland.

### Maus und Tastatur

Maus- und Tastatur-Eingaben **unterscheiden** sich zwischen den Display-Servern:

- **X11:** Verwaltet von Xorg mit xinput-Konfiguration
- **Wayland:** Verwaltet vom Compositor über libinput

Für präzises Cockpit-Klicken in X-Plane empfiehlt es sich, die Mausbeschleunigung zu deaktivieren:

- **X11:** `xinput --set-prop "Gerät" "libinput Accel Profile Enabled" 0 1` (aktiviert Flat-Profil)
- **Wayland:** Compositor-Einstellungen (GNOME Einstellungen → Maus, KDE Systemeinstellungen → Eingabegeräte)

---

## Welche Session soll ich verwenden?

```bash
# Aktuellen Session-Typ prüfen
echo $XDG_SESSION_TYPE
```

Ausgabe: `x11` oder `wayland`

| Situation | Empfehlung | Seite |
|-----------|-----------|-------|
| Einfachstes, zuverlässigstes X-Plane-Setup gewünscht | X11-Session | [X11-Session](displayserver_x11.md) |
| Bereits auf Wayland, X-Plane läuft problemlos | Auf Wayland bleiben | [Wayland-Session](displayserver_wayland.md) |
| Fullscreen- oder Multi-Monitor-Probleme | Zu X11 wechseln | [X11-Session](displayserver_x11.md) |
| Intel Arc GPU mit X11-Desktop-Glitches | Wayland-Session | [Wayland-Session](displayserver_wayland.md) |
| NVIDIA mit Treiber älter als 555 | X11-Session (Pflicht) | [X11-Session](displayserver_x11.md) |

---

## Weiterführende Kapitel

| Thema | Seite | Schwerpunkt |
|---|---|---|
| X11-Session | [X11-Session](displayserver_x11.md) | Empfohlenes X-Plane-Setup — direkter X11-Pfad |
| Wayland-Session | [Wayland-Session](displayserver_wayland.md) | X-Plane über XWayland — Einrichtung und Troubleshooting |
| Nvidia-Treiber | [Nvidia-Treiber](nvidia.md) | GPU-Treiberanforderungen für X11 und Wayland |
| Kernel-Tuning | [Kernel-Tuning](../system/systemtuning.md) | Latenzoptimierung auf Systemebene |
| Latenz und Vorhersagbarkeit | [Latenz und Vorhersagbarkeit](../../fundamentals/performance/latency.md) | Eingabelatenz — Theorie und Messung |
| Konfiguration | [Konfiguration](../../xplane/setup_diagnose/config.md) | X-Plane Display- und Rendering-Einstellungen |

---

## Quellen

- [Wayland Architecture](https://wayland.freedesktop.org/architecture.html) — Offizielles Wayland-Projekt
- [Arch Wiki — Wayland](https://wiki.archlinux.org/title/Wayland) — Umfassende Referenz
- [David Justo — Input-to-Photon Latency](https://davidjusto.com/articles/m2p-latency/) — Hardware-Latenzmessungen
- [Xaver Hugl — Gaming on Wayland](https://zamundaaa.github.io/wayland/2021/12/14/about-gaming-on-wayland.html) — KDE-Entwickler-Analyse
- [libinput — What is libinput](https://wayland.freedesktop.org/libinput/doc/latest/what-is-libinput.html) — Eingabegeräte-Handling
