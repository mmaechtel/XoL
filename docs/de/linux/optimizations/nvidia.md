---
description: "NVIDIA-Treiberinstallation auf Debian für X-Plane: Paketverwaltung und manuelle Methode, Liquorix-Header, Kernel-Mode-Setting und Performance-Tuning."
---
# Offizieller Nvidia-Treiber

Debian stellt NVIDIA-Treiber über den Paketmanager bereit — die empfohlene Methode für die meisten Anwender. Wer die allerneueste Treiberversion benötigt, kann alternativ den manuellen Installer (`.run`-Datei) von NVIDIA verwenden.

Diese Seite behandelt beide Ansätze und enthält Hinweise für [Liquorix-Kernel](../../glossary.md#liquorix-kernel)-Nutzer.

## Voraussetzungen

- Kompatible Nvidia-Grafikkarte
- Debian installiert und aktualisiert
- Root- oder Sudo-Rechte
- Für die Paketmanager-Methode: `non-free` und `non-free-firmware` in `/etc/apt/sources.list` aktiviert
- Optional: Liquorix-Kernel (falls genutzt)

## Empfohlen: Paketmanager

Die einfachste und zuverlässigste Methode. Der Debian-Pakettreiber integriert sich automatisch mit DKMS, initramfs und Secure Boot.

```bash
sudo apt update && sudo apt upgrade -y
sudo apt install nvidia-driver
```

Nach der Installation das System neu starten. Verifikation mit:

```bash
nvidia-smi
```

Details und Fehlerbehebung im [Debian Wiki: NvidiaGraphicsDrivers](https://wiki.debian.org/NvidiaGraphicsDrivers/).

## Alternative: Manuelle Installation (.run-Datei)

Diese Methode nur verwenden, wenn der Debian-Pakettreiber zu alt ist oder Probleme mit bestimmter Hardware verursacht.

### System-Vorbereitung

Das System wird aktualisiert:

```bash
sudo apt update && sudo apt upgrade -y
```

Für den Standard-Debian-Kernel werden Kernel-Header und Build-Tools installiert:

```bash
sudo apt install linux-headers-$(uname -r) build-essential dkms
```

**Hinweis zum [Liquorix-Kernel](../../glossary.md#liquorix-kernel)**: Die Liquorix-Kernel-Header sind ein separates Paket und müssen explizit installiert werden. [DKMS](../../glossary.md#dkms-dynamic-kernel-module-support) wird empfohlen, damit das NVIDIA-Modul bei Kernel-Updates automatisch neu kompiliert wird:

```bash
sudo apt install linux-headers-liquorix-amd64 dkms
```

Mit `uname -r` lässt sich der aktive Kernel prüfen — die Ausgabe sollte `liquorix` enthalten.

### Treiber-Installation

1. Die Seite [https://www.nvidia.com/Download/index.aspx](https://www.nvidia.com/Download/index.aspx) aufrufen
2. Grafikkarte, „Linux 64-bit" und Treiberversion auswählen
3. Die `.run`-Datei (z.B. `NVIDIA-Linux-x86_64-<VERSION>.run`) ins Home-Verzeichnis herunterladen

Wechsel in den Nicht-Grafik-Modus mit `systemctl`:

1. Standard-Boot-Target ändern:

```bash
sudo systemctl set-default multi-user.target
```

2. System neu starten:

```bash
sudo reboot
```

Das System bootet in eine Textkonsole ohne Grafikoberfläche.

Zur `.run`-Datei navigieren und ausführbar machen:

```bash
chmod +x NVIDIA-Linux-x86_64-*.run
```

Installation starten:

```bash
sudo ./NVIDIA-Linux-x86_64-*.run
```

Dem Installationsassistenten folgen:

- Lizenz akzeptieren
- Bei Bedarf „Ja" für 32-Bit-Kompatibilitätsbibliotheken wählen
- Deaktivierung des [Nouveau](../../glossary.md#nouveau)-Treibers bestätigen
- Bei der DKMS-Registrierung den Standard („Yes") akzeptieren

### Installation prüfen

Treiber überprüfen:

```bash
nvidia-smi
```

Eine Ausgabe mit GPU-Details bestätigt die erfolgreiche Installation.

### Zurück in den Grafik-Modus

Standard-Boot-Target zurücksetzen:

```bash
sudo systemctl set-default graphical.target
```

System erneut starten:

```bash
sudo reboot
```

## Fehlerbehebung

- **Schwarzer Bildschirm**: Der `.run`-Installer blacklistet den Nouveau-Treiber automatisch über `/etc/modprobe.d/`. Falls der Grafik-Modus dennoch nicht startet (z.B. weil Nouveau im initramfs eingebettet ist), `nouveau.modeset=0` in `/etc/default/grub` unter `GRUB_CMDLINE_LINUX_DEFAULT` hinzufügen und `sudo update-grub` ausführen.
- **Fehlende Abhängigkeiten**: Bei Standard-Kerneln `linux-headers-$(uname -r)` prüfen; beim Liquorix-Kernel sicherstellen, dass sowohl `linux-headers-liquorix-amd64` als auch `dkms` installiert sind.

## Performance-Optimierung

### Treiber-Einstellungen (nur X11)

Unter X11 bietet `nvidia-settings` Kompositions-Optionen zur Reduzierung von Screen [Tearing](../../glossary.md#tearing). Diese Einstellungen sind **unter [Wayland](displayserver_wayland.md) nicht verfügbar und nicht nötig**, da der Compositor dies nativ handhabt.

```bash
nvidia-settings
```

Unter „X Server Display Configuration" → „Advanced":

- **Force Full Composition Pipeline**: Verhindert Tearing, indem die gesamte Bildausgabe über die Kompositions-Engine der GPU geleitet wird. Kann die Eingabelatenz erhöhen — einzeln testen.
- **Force Composition Pipeline**: Ähnlich, aber weniger aggressiv. Verhindert die meisten Tearing-Artefakte mit geringerem Latenz-Einfluss.

Diese Einstellungen sind optional. Nur aktivieren, wenn Tearing beim Spielen tatsächlich sichtbar ist. Bei Performance-Problemen jederzeit deaktivierbar.

### Kernel-Parameter

Beim `.run`-Installer ist `nvidia-drm.modeset=1` **nicht** standardmäßig aktiviert und muss manuell gesetzt werden. Dieser Parameter aktiviert [Kernel Mode Setting (KMS)](../../glossary.md#drmkms-direct-rendering-manager-kernel-mode-setting) für NVIDIA, was für Wayland erforderlich ist und die Display-Handhabung verbessert.

In `/etc/default/grub` unter `GRUB_CMDLINE_LINUX_DEFAULT` hinzufügen:

```
nvidia-drm.modeset=1
```

Danach [GRUB](../../glossary.md#grub-grand-unified-bootloader) aktualisieren:

```bash
sudo update-grub
```

Aktuelle Einstellung prüfen:

```bash
cat /sys/module/nvidia_drm/parameters/modeset
```

Ein Wert von `Y` bestätigt, dass KMS aktiv ist.

!!! note "Paketmanager-Installation"
    Bei Installation über `apt install nvidia-driver` konfiguriert Debian modeset möglicherweise automatisch über `/etc/modprobe.d/`. Den aktuellen Wert prüfen, bevor ein GRUB-Parameter hinzugefügt wird.

### MangoHud (optional)

Für erweitertes Performance-Monitoring über die eingebaute [FPS](../../glossary.md#fps-frames-per-second)-Anzeige von X-Plane (Strg+Shift+F) hinaus:

```bash
sudo apt install mangohud
```

MangoHud liefert detaillierte GPU/CPU-Metriken, Frame-Time-Graphen und [VRAM](../../glossary.md#vram-video-ram)-Auslastung als In-Game-Overlay. Weitere Informationen zur Performance-Analyse unter [Systemtuning](../system/systemtuning.md) und [System-Monitoring](../system/systemtools.md).

---

## Weiterführende Kapitel

| Thema | Seite | Schwerpunkt |
|---|---|---|
| Display-Server | [Display-Server](displayserver.md) | X11 vs Wayland für X-Plane |
| X11-Session | [X11-Session](displayserver_x11.md) | Empfohlene Session mit Compositor-Bypass |
| Wayland-Session | [Wayland-Session](displayserver_wayland.md) | Wayland-Anforderungen und XWayland |
| Liquorix Kernel | [Liquorix Kernel](liquorix.md) | DKMS-Header für Kernelmodul-Bau |
| Kernel-Tuning | [Kernel-Tuning](../system/systemtuning.md) | GRUB-Parameter und Systemoptimierung |
| GPU & VRAM | [GPU & VRAM](../../fundamentals/performance/gpu_vram.md) | GPU-Performance-Theorie und VRAM-Management |

---

## Quellen

- [Debian Wiki: NvidiaGraphicsDrivers](https://wiki.debian.org/NvidiaGraphicsDrivers/) — Offizielle Debian-NVIDIA-Installationsanleitung
- [NVIDIA Driver Download](https://www.nvidia.com/Download/index.aspx) — Offizielle Treiber-Download-Seite
- [NVIDIA Driver README: KMS](https://download.nvidia.com/XFree86/Linux-x86_64/580.126.09/README/kms.html) — Kernel Mode Setting Dokumentation
- [NVIDIA Open GPU Kernel Modules](https://github.com/NVIDIA/open-gpu-kernel-modules) — Open-Source-Kernelmodul-Architektur und unterstützte GPUs
