# Faktencheck: Display Server Seiten (EN + DE)

**Datum:** 2026-02-10
**Geprüfte Seiten:** `displayserver.md`, `displayserver_wayland.md`, `displayserver_x11.md`
**Primärquellen verifiziert:** davidjusto.com, zamundaaa.github.io, wiki.debian.org, libinput docs, Intel Support, NVIDIA docs

---

## Status: Faktencheck abgeschlossen, Korrekturen ausstehend

---

## Fehler (6) — Korrekturbedarf

### 1. Debian-Defaults falsch
**Datei:** `displayserver.md:17`
**Behauptung:** "Wayland is the default session on Debian 12+ (GNOME) and Debian 13+ (KDE)"
**Befund:** GNOME nutzt Wayland als Default seit Debian 10 (Buster, 2019), nicht erst seit 12. KDE auf Debian 12 nutzt X11 als Default (plasma-workspace-wayland ist separates Paket). KDE Wayland erst ab Debian 13 (Plasma 6).
**Korrektur:** "Debian 10+ (GNOME)" oder für XoL-Kontext "Debian 12 (GNOME)" akzeptabel. KDE-Claim "Debian 13+" korrekt. Research-Paper-Tabelle ebenfalls korrigieren (Debian 12 KDE: X11, nicht Wayland).

### 2. Hugl-Tabelle unvollständig
**Datei:** `displayserver.md:68-73`
**Befund:** XWayland-Zeile fehlt (49/38/20 ms). Auch FreeSync-Zeile fehlt.
**Korrektur:** XWayland-Zeile ergänzen — besonders relevant, da X-Plane genau diesen Pfad nutzt.

### 3. "Median" vs "Mean" unklar
**Datei:** `displayserver.md:55` (Spaltenüberschrift "Median Input-to-Photon Latency")
**Befund:** Justo-Quelle zeigt Balkendiagramm mit "mean latencies from 100 measurements". Ob Median oder Mean, muss am Original nochmal geprüft werden — Unterschied bei 100 Messungen gering, aber Bezeichnung sollte stimmen.
**Korrektur:** Spalte neutral als "Input-to-Photon Latency" bezeichnen oder am Originalartikel verifizieren.

### 4. MESA_VK_WSI_PRESENT_MODE nur für Mesa-Treiber
**Datei:** `displayserver_wayland.md:70`
**Befund:** Kommentar "prevents tearing via vblank sync" fehlt der Hinweis, dass nur Mesa-basierte Treiber (AMD RADV, Intel ANV) betroffen sind. NVIDIA proprietär: keine Wirkung.
**Korrektur:** Kommentar ergänzen: "(Mesa drivers only — AMD, Intel)"

### 5. nvidia_drm.modeset=1 seit Treiber 560 Default
**Datei:** `displayserver_wayland.md:109`
**Befund:** Seit NVIDIA-Treiber 560 (Aug 2024) ist modeset=1 der Default. Manuelles Setzen nur für Treiber 555-559 nötig. Inkonsistenz mit nvidia.md.
**Korrektur:** "`nvidia_drm.modeset=1` active (default since driver 560; verify with `cat /sys/module/nvidia_drm/parameters/modeset`)"

### 6. "X11 with compositor adds a full frame of latency" zu pauschal
**Datei:** `displayserver.md:74`
**Befund:** Stimmt nur für FIFO/VSync-Modus. Im Mailbox-Modus verschwindet der Overhead (37 vs 38 ms). Hugl erklärt das architektonisch für den FIFO-Fall.
**Korrektur:** Einschränken auf VSync: "In VSync (FIFO) mode, X11 with a compositor adds a full frame of latency compared to Wayland."

---

## Nuancen (4) — verbesserbar, aber akzeptabel

### 7. "~7 ms overhead" als allgemeine XWayland-Aussage
**Datei:** `displayserver.md:35`
**Befund:** Die ~7ms stammen aus einer Studie (Justo, CS2, 400fps, VSync off, 360Hz, RTX 4090). Hugls Daten zeigen nur ~2ms XWayland-Overhead (Mailbox). Hardware- und konfigurationsabhängig.

### 8. Justo-Testbedingungen nicht dokumentiert
**Datei:** `displayserver.md:76-82`
**Fehlend:** Testspiel (Counter-Strike 2), VSync off, VRR off, Allow Tearing on, 400fps engine-capped, Fedora 43.

### 9. SDL_VIDEODRIVER=wayland "unpredictable results"
**Datei:** `displayserver_wayland.md:121`
**Befund:** Etwas zu stark. Justos Messungen zeigen native Wayland (7.14ms) fast identisch mit X11. Besser: "not tested/supported by Laminar; results vary."

### 10. "XWayland cannot position windows freely"
**Datei:** `displayserver_wayland.md:49`
**Befund:** Wayland-Designprinzip, nicht XWayland-spezifisch. Besser: "Wayland does not allow applications to position windows — XWayland inherits this limitation."

---

## Korrekt (17) — keine Änderung nötig

| # | Behauptung | Quelle |
|---|---|---|
| 11 | X11 seit 1984, Version 11 von 1987 | Wikipedia, X.org |
| 12 | Justo-Messwerte (6.88/7.14/14.45/6.91 ms) | davidjusto.com verifiziert |
| 13 | Justo-Hardware (9950X3D, RTX 4090, AW2725DF, KWin 6.5.4, NVIDIA 580.119.02) | davidjusto.com verifiziert |
| 14 | Arduino Pro Micro + TEMT6000, 100 Messungen | davidjusto.com verifiziert |
| 15 | Hugl-Werte (59/37/—, 41/38/19, 49/36/20) | zamundaaa.github.io verifiziert |
| 16 | Joysticks via /dev/input, Display-Server-unabhängig | libinput-Doku, Arch Wiki |
| 17 | libinput unterstützt keine Joysticks | libinput offizielle Doku |
| 18 | X-Plane hat kein natives Wayland-Backend | X-Plane 12.1.3 Release Notes |
| 19 | GDK_BACKEND=x11 seit X-Plane 12.1.3 automatisch | X-Plane 12.1.3 Release Notes |
| 20 | NVIDIA Treiber 555+ für Wayland | NVIDIA Docs, Arch Wiki |
| 21 | NVIDIA <555: X11 mandatory | NVIDIA Docs (Explicit Sync) |
| 22 | Intel Arc X11 Rendering-Glitches | Intel Support Article 000092987 |
| 23 | Intel empfiehlt Wayland für Arc | Intel Support Docs |
| 24 | KDE Compositor-Bypass bei Fullscreen (X11) | KDE Doku |
| 25 | Mutter Direct Scanout statt Compositor-Bypass | GNOME Doku |
| 26 | X11 Single Refresh Rate für alle Monitore | Arch Wiki |
| 27 | X11 keine Input-Isolation zwischen Fenstern | Wayland Architecture Docs |
