# Content Audit — begin.md

| Feld | Wert |
|------|------|
| **Datei** | `docs/en/begin.md` |
| **Titel** | Getting Started with X-Plane on Linux |
| **Zeilen** | 229 |
| **Aufwand** | M (Medium) |
| **Audit-Datum** | 2026-02-13 |
| **Gesamtbewertung** | **C** — Teilweise fehlerhaft oder veraltet, Überarbeitung nötig |

**Begründung C:** Mehrere faktische Fehler (Installer-Name/-Format, Paketname `vulkan-utils`), veraltete Kernaussage (Single-Core-Limitation seit 12.4 überholt), duplizierter Absatz, und mehrere nicht durch Quellen gestützte Empfehlungen (Swap, Root-Partition, DE-Kompatibilität). Die Seite ist funktional, aber in ihrer aktuellen Form inhaltlich unzuverlässig.

---

## Detail-Tabelle

| # | Zeile | Abschnitt | Behauptung | Typ | Bewertung | Quelle / Beleg | Empfehlung | Entscheidung |
|---|-------|-----------|------------|-----|-----------|----------------|------------|:------------:|
| 1 | 7, 11, 31 | System Requirements | "X-Plane heavily utilizes single-core performance" / "primarily uses one CPU core for flight physics" / "due to its single-core limitation" | AKT | **WARN** | developer.x-plane.com Blog (12/2025): "The glorious multi-core future is now the boring present" — seit 12.4 wird Scene-Graph-Traversal (bis 75% der Frame-Time) parallel auf mehrere Cores verteilt. | Umformulieren: Single-Core bleibt wichtig, aber X-Plane 12 nutzt seit 12.4 Multi-Threading für wesentliche Frame-Arbeit. "Single-core limitation" streichen. | Korrigieren |
| 2 | 10–23 | Recommended Requirements | CPU i7/i9 bzw. Ryzen 7/9, 32 GB RAM, 8 GB VRAM, 250 GB SSD | REL | **WARN** | x-plane.com/kb/x-plane-12-system-requirements: Offiziell empfohlen: i5-12600K / Ryzen 5 3500, 16–24 GB RAM, 8 GB VRAM (RTX 3070). XoL-Werte sind durchgehend höher. | Klarstellen, dass dies XoL-Empfehlungen für Addon-Heavy-Setups sind, nicht Laminars offizielle Specs. Oder offizielle Werte referenzieren und XoL-Empfehlung als Ergänzung. | Korrigieren |
| 3 | 19 | Storage Space | "base installation already requires about 70 GB" | FAK | **FAIL** | x-plane.com/kb/digital-download-install: "the entire scenery package takes over 60 GB". Steam-Mindestanforderung: 23 GB. Basis-Installation (ohne alle Szenerien): ~25 GB. Vollinstall mit allen Regionen: ~75–80 GB. | Korrigieren: "Die Basis-Installation benötigt ca. 25 GB, mit allen Szenerien-Regionen ca. 75–80 GB." | Korrigieren |
| 4 | 48 | Installation Tips | "choose GNOME or KDE Plasma for best compatibility" | FAK | **WARN** | Keine Laminar-Quelle nennt DE-Anforderungen. X-Plane nutzt Vulkan/OpenGL direkt, unabhängig vom Desktop. | Umformulieren: "Jede gängige Desktop-Umgebung funktioniert. GNOME und KDE bieten die größte Community-Unterstützung und beste Wayland-Integration." | Korrigieren |
| 5 | 49 | Installation Tips | "swap space of at least half your RAM size (e.g., 16 GB swap for 32 GB RAM)" | FAK | **WARN** | Debian Wiki/Installer-Guide: "as much swap as system memory" (wird als veraltet eingestuft). Arch Wiki: "4 GiB" ohne Hibernation, "RAM-Größe" mit Hibernation. "Halbe RAM" stammt aus keiner Standardquelle. | Zweistufige Empfehlung: ~4 GB ohne Hibernation, RAM-Größe mit Hibernation. | Korrigieren |
| 6 | 50 | Installation Tips | "separate partitions for / (root, at least 100 GB) and /home" | DET | **WARN** | Debian Install Guide: 15 GB empfohlen für Root. Arch Wiki: 23–32 GB. 100 GB ist 3–5× überdimensioniert, sofern X-Plane in /home installiert wird (wie auf Zeile 101 empfohlen). | Auf 30–50 GB reduzieren oder begründen, warum 100 GB nötig (z.B. wenn zusätzliche Kernel + DKMS-Module Platz brauchen). | Korrigieren |
| 7 | 70 + 74 | Installing X-Plane 12 | Identischer Absatz dupliziert: "X-Plane 12 is available both through Steam…" | DET | **FAIL** | — (Struktureller Fehler, kein Quellenbezug) | Duplikat in Zeile 74 entfernen. | Korrigieren |
| 8 | 83 | Standalone Version | "Download the installer (approximately 1 GB)" | FAK | **FAIL** | x-plane.com/desktop/try-it: Installer ist `X-Plane12InstallerLinux.zip`, ein Bootstrap von ~25 MB. Die 1 GB-Angabe ist falsch — der Installer selbst ist klein, das Spiel wird erst während der Installation heruntergeladen. | Korrigieren: Installer-Download ist ein kleiner Bootstrap (~25 MB). | Korrigieren |
| 9 | 97–98 | Standalone Version | Installer-Dateiname `X-Plane-installer.run` + `chmod +x` + `./X-Plane-installer.run` | FAK | **FAIL** | x-plane.com/desktop/try-it: Datei heißt `X-Plane12InstallerLinux.zip`. Format ist ZIP, nicht `.run`. | Komplett korrigieren: `unzip X-Plane12InstallerLinux.zip`, dann extrahiertes Binary ausführen. | Korrigieren |
| 10 | 106 | Download process | "70-150 GB depending on selection" | FAK | **WARN** | x-plane.com/kb/digital-download-install: "over 60 GB" für das komplette Szenerien-Paket. Vollinstallation ~75–80 GB. 150 GB ist ohne Drittanbieter-Addons nicht erreichbar. | Korrigieren auf "25–80 GB je nach Auswahl der Szenerien-Regionen". | Korrigieren |
| 11 | 133 | After Installation | FPS-Anzeige mit `Shift+Ctrl+F` | FAK | **OK** | Bestätigt durch Tastaturlayout-Referenz (defkey.com/x-plane-12-shortcuts). | — | Belassen |
| 12 | 148 | Checking Dependencies | `ldd X-Plane-x86_64` (Executable-Name) | FAK | **OK** | x-plane.com/kb/x-plane-64-bit-faq: "The 64-bit version is called… X-Plane-x86_64… on Linux" | — | Belassen |
| 13 | 178 | Resolving Missing Dependencies | `sudo apt install libvulkan1 mesa-vulkan-drivers vulkan-utils` | FAK | **FAIL** | packages.debian.org: `vulkan-utils` existiert weder in Bookworm noch in Trixie. Paket wurde zu **`vulkan-tools`** umbenannt. | `vulkan-utils` → `vulkan-tools` | Korrigieren |
| 14 | 189 | Resolving Missing Dependencies | `sudo apt install libgl1-mesa-glx libgl1-mesa-dri` | AKT | **WARN** | packages.debian.org: `libgl1-mesa-glx` ist in Bookworm ein Transitional-Dummy, in Trixie entfernt. Ersetzt durch `libgl1` + `libglx-mesa0`. | `libgl1-mesa-glx` → `libgl1`. `libgl1-mesa-dri` bleibt korrekt. | Korrigieren |
| 15 | 196 | 32-Bit Compatibility | `sudo apt install libgl1-mesa-glx:i386 libvulkan1:i386` | AKT | **WARN** | Wie #14 — `libgl1-mesa-glx:i386` → `libgl1:i386`. Rest korrekt. `dpkg --add-architecture i386` Prozedur ist korrekt bestätigt. | `libgl1-mesa-glx:i386` → `libgl1:i386` | Korrigieren |
| 16 | 204 | Common Missing Dependencies | Tabelle: `libgl1-mesa-glx` als Paket für `libGL.so.1` | AKT | **WARN** | Wie #14. | Tabelleneintrag: `libgl1-mesa-glx` → `libgl1` | Korrigieren |
| 17 | 63 | After Installation | `sudo apt install build-essential dkms git curl wget nano` | REL | **OK** | DKMS ist essenziell für NVIDIA-Treiber (`nvidia-kernel-dkms`) und Liquorix-Kernel. Wird zwar als Dependency von nvidia-kernel-dkms gezogen, explizite Installation ist aber klarer und schadet nicht. | — | Belassen |
| 18 | 101 | Standalone Version | Installationspfad `/home/[username]/X-Plane 12/` | FAK | **OK** | Standardpfad bestätigt. Konsistent mit Troubleshooting-Zeile 215 (`~/X-Plane 12/Log.txt`). | — | Belassen |
| 19 | 215 | Troubleshooting | Log-Datei bei `~/X-Plane 12/Log.txt` | FAK | **OK** | Standardpfad für X-Plane-Log. | — | Belassen |
| 20 | 184 | Resolving Missing Dependencies | `sudo apt install libasound2 libasound2-plugins libpulse0` | AKT | **OK** | `libasound2` existiert in Bookworm. In Trixie umbenannt zu `libasound2t64` (t64-Transition), wird aber via Provides aufgelöst. `libasound2-plugins` und `libpulse0` existieren in beiden Releases. | Für Trixie-Kompatibilität optional Hinweis auf t64-Transition, aber kein akuter Handlungsbedarf. | Belassen |

---

## Zusammenfassung Findings

| Bewertung | Anzahl | Details |
|-----------|--------|---------|
| **FAIL** | 5 | #3 (Install-Größe), #7 (Duplikat), #8 (Installer-Größe), #9 (Installer-Name), #13 (vulkan-utils) |
| **WARN** | 7 | #1 (Single-Core), #2 (Requirements), #4 (DE-Kompatibilität), #5 (Swap), #6 (Root-Partition), #10 (Download-Größe), #14–16 (libgl1-mesa-glx) |
| **OK** | 6 | #11, #12, #17, #18, #19, #20 |
| **N/V** | 0 | — |

---

## Struktur-Review (Schritt 2)

| Aspekt | Bewertung | Anmerkung |
|--------|-----------|-----------|
| Fehlende Themen | OK | Seite deckt den Getting-Started-Pfad vollständig ab. Steam-Installation bewusst ausgelassen (dokumentiert). |
| Überflüssiges | WARN | Zeile 124–131 ("Optimize performance settings"): Grafikeinstellungen sind plattformunabhängig und werden auf `config.md` behandelt. Hier nur knapper Verweis nötig. |
| Zielgruppe | OK | Richtet sich an Linux-erfahrene User — passt. ldd-Abschnitt ist wertvoll und zielgruppengerecht. |
| Struktur | WARN | Duplikat-Absatz (#7). Außerdem: Die Seite springt von Debian-Installation direkt zu X-Plane-Installation ohne Grafiktreiber-Hinweis. Da `nvidia.md` und `liquorix.md` als nächste Schritte empfohlen werden, wäre ein kurzer Hinweis-Block "Nächste Schritte: Grafiktreiber installieren → nvidia.md" am Ende hilfreich. |
| Querverweise | WARN | Kein Verweis auf `nvidia.md`, `liquorix.md` oder `systemtuning.md` als logische Folgeschritte. `config.md` wird nicht referenziert, obwohl Zeile 124–131 Grafikeinstellungen behandelt. Glossar-Verweise (ldd, Vulkan, dynamic libraries) sind vorhanden und korrekt. |
| Markdown/Format | OK | Konsistente 4-Space-Indentation, korrekte Code-Blocks mit `bash`, Überschriften ohne Doppelpunkt vor Listen. Leerzeilen nach Headings vorhanden. |

---

## Quellen

| Kürzel | URL |
|--------|-----|
| XP-SysReq | https://www.x-plane.com/kb/x-plane-12-system-requirements/ |
| XP-Install | https://www.x-plane.com/kb/digital-download-install/ |
| XP-Download | https://www.x-plane.com/desktop/try-it/ |
| XP-64bit | https://www.x-plane.com/kb/x-plane-64-bit-faq/ |
| XP-DevBlog | https://developer.x-plane.com/2025/12/the-glorious-multi-core-future-is-now-the-boring-present/ |
| Steam | https://store.steampowered.com/app/2014780/XPlane_12/ |
| Deb-Swap | https://wiki.debian.org/Swap |
| Deb-Partitioning | https://www.debian.org/releases/stable/amd64/apcs03.en.html |
| Arch-Partitioning | https://wiki.archlinux.org/title/Partitioning |
| Deb-vulkan-tools | https://packages.debian.org/bookworm/vulkan-tools |
| Deb-libgl1-mesa-glx | https://packages.debian.org/bookworm/libgl1-mesa-glx |
| Deb-NVIDIA | https://wiki.debian.org/NvidiaGraphicsDrivers |
