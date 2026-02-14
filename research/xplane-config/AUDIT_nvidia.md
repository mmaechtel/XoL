# Audit: nvidia.md

## Kopf

| Feld | Wert |
|------|------|
| **Datei** | `docs/en/nvidia.md` |
| **Titel** | Official Nvidia Driver |
| **Zeilen** | 165 |
| **Aufwand** | M (Medium) |
| **Audit-Datum** | 2026-02-14 |
| **Gesamtbewertung** | **C** — Teilweise fehlerhaft, irreführende Beschreibungen, wesentliche Lücke (apt-Methode fehlt) |

---

## Detail-Tabelle

| # | Zeile | Abschnitt | Behauptung | Typ | Bewertung | Quelle / Beleg | Empfehlung | Entscheidung |
|---|-------|-----------|------------|-----|-----------|----------------|------------|:------------:|
| 1 | 1–3 | Official Nvidia Driver | Seite behandelt ausschließlich die .run-Installer-Methode, ohne `apt install nvidia-driver` zu erwähnen | REL | FAIL | Debian Wiki: "these are **the most recommended drivers for most users** with long-term support (LTS). Other packaging methods should generally only be used in case these drivers cause some problems." — [wiki.debian.org/NvidiaGraphicsDrivers](https://wiki.debian.org/NvidiaGraphicsDrivers/) | Seite umstrukturieren: apt-Methode als Standard voranstellen, .run als Alternative für bleeding-edge-Treiber. Oder zumindest prominent auf die apt-Alternative hinweisen. | |
| 2 | 118–130 | Performance Modes | `nvidia-smi -pm 1` wird als "Performance Mode" beschrieben, der "keeps the GPU in a higher performance state" | FAK | FAIL | NVIDIA Docs: "Persistence Mode is the term for a user-settable driver property that keeps a target GPU initialized even when no clients are connected to it." — [docs.nvidia.com/deploy/driver-persistence](https://docs.nvidia.com/deploy/driver-persistence/persistence-mode-legacy.html). Beeinflusst NICHT GPU-Taktraten oder Leistungsstufen. Auf Desktop-Systemen mit laufendem Display-Server wirkungslos. Zudem als "near end-of-life" eingestuft. | Abschnitt entfernen oder komplett umschreiben. Persistence Mode ist für CUDA-Server, nicht für Gaming-Desktops relevant. | |
| 3 | 134–150 | Kernel Parameters | "In Debian 12, most NVIDIA optimizations are already enabled by default" — im Kontext des .run-Installers ist das falsch | FAK | FAIL | NVIDIA README (580.x): "NVIDIA's DRM KMS support is still considered experimental. It is disabled by default." — [download.nvidia.com/.../kms.html](https://download.nvidia.com/XFree86/Linux-x86_64/580.126.09/README/kms.html). Der .run-Installer setzt `nvidia-drm.modeset=1` NICHT automatisch. Nur Distro-Pakete (Arch ab 560.35) setzen es per modprobe.d. Debian-Wiki weist Nutzer an, modprobe.d-Datei manuell zu erstellen. | Klarstellen, dass `nvidia-drm.modeset=1` beim .run-Installer manuell gesetzt werden muss. "Debian 12"-Referenz auf aktuelle Version anpassen oder generisch formulieren. | |
| 4 | 107–114 | Driver Settings | Force Full/Force Composition Pipeline als allgemeine Empfehlung ohne Hinweis auf X11-Beschränkung | FAK | WARN | Arch Wiki: Settings stehen unter "Avoid screen tearing on Xorg" — [wiki.archlinux.org/title/NVIDIA/Troubleshooting](https://wiki.archlinux.org/title/NVIDIA/Troubleshooting). Auf Wayland wirkungslos und nicht verfügbar. Bekannter Bug: GPU-Crash mit `VK_KHR_present_wait` bei ForceFullCompositionPipeline. | Klar als X11-only kennzeichnen. Hinweis ergänzen, dass Wayland-Compositors dies nativ handhaben. | |
| 5 | 112–114 | Driver Settings | "Force Composition Pipeline: Improves image quality and stability" | FAK | FAIL | ForceCompositionPipeline verbessert NICHT die Bildqualität. Es erzwingt GPU-seitige Komposition, was Tearing auf X11 behebt. Keine Quelle belegt "improved image quality". | Beschreibung korrigieren: verhindert Tearing auf X11, hat keinen Einfluss auf Bildqualität. | |
| 6 | 26 | System Preparation | "kernel headers are already available through the Liquorix package sources after the kernel is installed" — impliziert automatische Installation | FAK | WARN | Liquorix install-script installiert explizit zwei Pakete: `linux-image-liquorix-amd64` UND `linux-headers-liquorix-amd64` — [liquorix.net/install-liquorix.sh](https://liquorix.net/install-liquorix.sh). Headers sind ein separates Paket, nicht automatisch enthalten. | Klarstellen, dass `linux-headers-liquorix-amd64` separat installiert werden muss. | |
| 7 | 26 | System Preparation | "the Nvidia driver needs [DKMS] to compile the kernel module dynamically" | FAK | WARN | NVIDIA nvidia-installer `option_table.h`: DKMS-Registration ist opt-in (Default: ja, wenn DKMS erkannt). Driver "braucht" DKMS nicht — DKMS ermöglicht automatische Neukompilierung bei Kernel-Updates. — [github.com/NVIDIA/nvidia-installer](https://github.com/NVIDIA/nvidia-installer/blob/main/option_table.h) | "benötigt" durch "wird empfohlen für" ersetzen. | |
| 8 | 26 | System Preparation | Beispiel Liquorix-Version `6.6.0-1-liquorix-amd64` | AKT | WARN | Illustrative Versionsnummer. Aktuell: 6.18.x. Per Entscheidungsbaum: illustrative Versionen entfernen. | Version entfernen, nur Muster beschreiben (z.B. "contains 'liquorix'"). | |
| 9 | 35, 56, 61 | Driver Installation | Illustrative Treiber-Version `550.54.14` in Dateiname und Befehlen | AKT | WARN | Illustrativ, veraltet (aktuell: 580.x/590.x). Per Entscheidungsbaum entfernen oder mit Platzhalter ersetzen. | Platzhalter verwenden: `NVIDIA-Linux-x86_64-<VERSION>.run` | |
| 10 | 94 | Troubleshooting | `nouveau.modeset=0` in GRUB als Troubleshooting ohne Kontext | DET | WARN | NVIDIA .run-Installer schreibt automatisch `/etc/modprobe.d/nvidia-installer-disable-nouveau.conf` mit `blacklist nouveau` und `options nouveau modeset=0` — [github.com/NVIDIA/nvidia-installer misc.c](https://github.com/NVIDIA/nvidia-installer/blob/main/misc.c). GRUB-Parameter ist nur nötig als Fallback wenn nouveau im initramfs eingebettet ist. | Kontext ergänzen: Installer handhabt dies normalerweise. GRUB-Parameter nur als Fallback für initramfs-Sonderfälle. | |
| 11 | 134 | Kernel Parameters | "In Debian 12" — Versions-Referenz | AKT | WARN | Aktuelle Debian-Version: Bookworm (12), Testing: Trixie (13). Generische Formulierung bevorzugen. | "In Debian 12" durch "In current Debian versions" oder "In Debian Bookworm and later" ersetzen. | |
| 12 | 155–157 | Additional Optimizations | `sudo apt install mangohud` | FAK | OK | In Debian Bookworm (0.6.8-2) und Trixie (0.7.2-2) verfügbar — [packages.debian.org](https://packages.debian.org/trixie/mangohud) | — | |
| 13 | 159 | Additional Optimizations | "X-Plane already offers a built-in FPS display (Ctrl+Shift+F)" | FAK | OK | Bestätigt durch DefKey und X-Plane Manual — [defkey.com/x-plane-12-shortcuts](https://defkey.com/x-plane-12-shortcuts) | — | |
| 14 | 33 | Driver Installation | Download-URL `https://www.nvidia.com/Download/index.aspx` | FAK | OK | URL funktioniert, leitet zur aktuellen Download-Seite weiter. | — | |
| 15 | 40 | Driver Installation | `sudo systemctl set-default multi-user.target` für Wechsel zum Text-Modus | FAK | OK | Standard-systemd-Befehl, korrekt. | — | |
| 16 | 67 | Driver Installation | "Confirm disabling the Nouveau driver when asked" | FAK | OK | .run-Installer fragt standardmäßig, bestätigt durch nvidia-installer Quellcode. | — | |

---

## Struktur-Review (Schritt 2)

| Aspekt | Bewertung | Anmerkung |
|--------|-----------|-----------|
| Fehlende Themen | **FAIL** | `apt install nvidia-driver` als Standard-Debian-Methode fehlt komplett. Für eine Debian-fokussierte Doku ist das eine kritische Lücke — die meisten Leser sollten apt verwenden. |
| Überflüssiges | **WARN** | Abschnitt "Performance Modes" (nvidia-smi -pm 1) ist für Desktop-Gaming irrelevant und faktisch falsch beschrieben. Kann ersatzlos entfernt werden. |
| Zielgruppe | OK | Detailgrad passt für Linux-erfahrene User. |
| Struktur | **WARN** | Die Seite hat keinen H1-Titel (`#`), sondern startet mit H2 (`##`). Inkonsistent mit anderen Seiten. Keine "Sources"-Sektion am Ende. |
| Querverweise | **WARN** | Kein Verweis auf [Display Server](displayserver.md) (relevant für Wayland vs X11 bei nvidia-settings). Kein Verweis auf [System Tuning](systemtuning.md) für GPU-Performance. |
| Markdown/Format | Prüfung in Phase 4 | |

---

## User-Entscheidung (Schritt 3)

- **FAIL-Findings:** Alle 4 korrigieren ✓
- **WARN-Findings:** Alle 7 verbessern ✓
- **Struktur:** Alle Empfehlungen umsetzen (H1, Sources, Querverweise) ✓

---

## Korrekturen umgesetzt (Schritt 4)

### Inhaltliche Korrekturen (EN)

| # | Finding | Umsetzung |
|---|---------|-----------|
| 1 | apt-Methode fehlt | Neuer Abschnitt "Recommended: Package Manager" mit `apt install nvidia-driver`. .run-Methode als "Alternative" repositioniert. |
| 2 | "Performance Modes" falsch | Abschnitt ersatzlos entfernt. Persistence Mode ist für CUDA-Server, nicht Desktop-Gaming. |
| 3 | modeset-Default falsch | Komplett umgeschrieben: Klarstellung dass .run-Installer modeset NICHT setzt, mit Verifikationsbefehl (`cat /sys/module/...`). Note-Block für apt-Methode ergänzt. |
| 4 | Force Composition X11-only | Abschnittstitel auf "Driver Settings (X11 Only)" geändert, Wayland-Hinweis mit Link zu displayserver_wayland.md ergänzt. |
| 5 | "Improves image quality" | Beschreibung korrigiert: verhindert Tearing, nicht "verbessert Bildqualität". |
| 6 | Liquorix-Headers | Klargestellt als separates Paket, expliziter apt-Befehl: `apt install linux-headers-liquorix-amd64 dkms`. |
| 7 | DKMS "benötigt" | Umformuliert: "is recommended so the NVIDIA module is automatically recompiled". |
| 8 | Illustrative Liquorix-Version | Entfernt. Stattdessen: "output should contain 'liquorix'". |
| 9 | Illustrative Treiberversion 550.x | Ersetzt durch Platzhalter: `NVIDIA-Linux-x86_64-<VERSION>.run` und Wildcard `*.run`. |
| 10 | nouveau.modeset=0 ohne Kontext | Kontext ergänzt: Installer blacklistet automatisch, GRUB-Parameter als Fallback für initramfs-Fälle. |
| 11 | "In Debian 12" | Versions-Referenz entfernt. Generisch formuliert. |

### Strukturelle Korrekturen

- H1-Titel (`# Official Nvidia Driver`) statt H2
- Sources-Abschnitt mit 4 Quellen ergänzt
- Querverweise auf Display Server (Wayland) und System Tuning/Monitoring ergänzt

### Lektorat

- Textfluss nach Rewrite geprüft: logisch von empfohlen → alternativ → troubleshooting → optimierung
- Konsistenter Ton, einheitlicher Detailgrad
- Keine Redundanzen, klare Abschnitte
- "Important Notes"-Abschnitt (Allgemeinplätze) entfernt

### Markdown-Check

- EN: Sauber nach Rewrite
- DE: `bash`-Tag bei GRUB-Parameter entfernt (Zeile 135 → kein Tag)
