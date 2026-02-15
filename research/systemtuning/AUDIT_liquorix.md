# AUDIT: liquorix.md

| Feld | Wert |
|------|------|
| **Datei** | `docs/en/liquorix.md` |
| **Titel** | Liquorix Kernel on Debian |
| **Zeilen** | 140 |
| **Aufwand** | M |
| **Audit-Datum** | 2026-02-15 |
| **Gesamtbewertung** | **D** |

---

## Detail-Tabelle

| # | Zeile | Abschnitt | Behauptung | Typ | Bewertung | Quelle / Beleg | Empfehlung | Entscheidung |
|---|-------|-----------|------------|-----|-----------|----------------|------------|:------------:|
| 1 | 3 | Intro | "maintained by the community" | FAK | WARN | Liquorix wird primär von einer Einzelperson (Steven Barrett / damentz) gepflegt, nicht von einer Community. GitHub zeigt einen Hauptcontributor. | Präzisieren: "maintained by Steven Barrett" oder "a community project maintained by a single developer" | |
| 2 | 11 | Prerequisites | "Minimum 8 GB RAM for optimal performance" | FAK | WARN | Keine offizielle Quelle nennt RAM-Anforderungen. liquorix.net bewirbt sogar "Compressed Swap" (zram) als Feature. | Entfernen oder als X-Plane-Empfehlung umformulieren (nicht Liquorix-spezifisch) | |
| 3 | 34 | Installation | GPG-Key-URL `linux-liquorix-keyring.gpg` | FAK | **FAIL** | URL gibt HTTP 404 zurück. Korrekte URL laut `install-liquorix.sh`: `https://liquorix.net/liquorix-keyring.gpg` | URL korrigieren zu `liquorix-keyring.gpg` | |
| 4 | 39 | Installation | Repository-Setup mit `/usr/share/keyrings/` und `lsb_release` | FAK | **FAIL** | Offizielles Skript nutzt `/etc/apt/keyrings/` (moderner Debian-Standard), erkennt Codename über `apt-cache policy`, und setzt `arch=amd64`. Drei Abweichungen vom offiziellen Installationsweg. | Installationsbefehle an `install-liquorix.sh` angleichen oder One-Liner empfehlen | |
| 5 | 51 | Installation | Paketnamen `linux-image-liquorix-amd64 linux-headers-liquorix-amd64` | FAK | OK | Bestätigt durch `install-liquorix.sh`: `apt-get install -y linux-image-liquorix-amd64 linux-headers-liquorix-amd64` | — | |
| 6 | 68 | Installation | Beispielversion `6.6.0-1-liquorix-amd64` | AKT | WARN | Veraltet. Aktuell: `6.18.10-1-liquorix-amd64`. Version 6.6 stammt von Ende 2023. | Aktuelle Version verwenden oder Meta-Formulierung ("a Liquorix kernel version, e.g. `6.x.y-N-liquorix-amd64`") | |
| 7 | 72 | Features | "improved process scheduling mechanisms, optimized timer interrupts, and adjusted CPU governor settings" | DET | WARN | Vage Marketingsprache ohne konkreten Inhalt. Tatsächliche Kernfeatures: PDS-Scheduler, 1000 Hz Timer, Full Preempt, Zen Interactive Tuning. | Konkrete Features benennen statt vager Umschreibungen | |
| 8 | 74 | Features | "compatibility with Debian Security Advisories" | FAK | **FAIL** | DSAs gelten nur für Pakete im offiziellen Debian-Archiv. Liquorix ist nicht im Archiv, wird nicht vom Debian Security Team betreut. Kein SECURITY.md, keine dokumentierte CVE-Policy. | Falschaussage entfernen. Ersetzen durch: Liquorix folgt upstream, aber DSAs gelten nicht. | |
| 9 | 76 | Features | "driver integration has been particularly optimized, leading to improved compatibility with gaming peripherals" | FAK | **FAIL** | Keine Quelle belegt spezielle Treiberoptimierungen in Liquorix. Die Kernel-Config zeigt Standard-Treiberkonfiguration. Vorteil ist lediglich der neuere Upstream-Kernel mit neueren Treibern. | Entfernen. Ersetzen durch Hinweis auf neueren Upstream-Kernel. | |
| 10 | 80 | Why Liquorix? | "uses the **EEVDF scheduler** (Earliest Eligible Virtual Deadline First)" | FAK | **FAIL** | **Falsch.** Liquorix nutzt den **PDS-Scheduler** (Priority and Deadline based Skiplist). Belege: (1) `journalctl -k -b`: "sched/alt: PDS CPU Scheduler v6.18-r1 by Alfred Chen", (2) `/proc/config.gz`: `CONFIG_SCHED_PDS=y`, (3) liquorix.net: "PDS Process Scheduler". EEVDF ist der Mainline-Scheduler seit Kernel 6.6 — Liquorix ersetzt ihn explizit durch PDS. | Korrigieren zu PDS-Scheduler. Gesamten "Why Liquorix?"-Abschnitt überarbeiten. | |
| 11 | 80 | Why Liquorix? | "shorter preemption windows and a higher timer frequency" | FAK | OK | Bestätigt: `CONFIG_HZ=1000` (vs. Debian 250 Hz), `CONFIG_PREEMPT=y` (vs. Debian `PREEMPT_LAZY`/`PREEMPT_DYNAMIC`). liquorix.net: "1000hz tick rate", "Hard Kernel Preemption". | — | |
| 12 | 82–83 | Why Liquorix? | "scheduler considers their wake frequency and cache locality" | FAK | **FAIL** | Diese Beschreibung passt auf EEVDF (virtual runtime, eligibility), nicht auf PDS. PDS nutzt eine Skiplist-Datenstruktur mit Prioritäten und Deadlines — ein anderes Modell. | Scheduler-Verhaltensbeschreibung für PDS neu formulieren | |
| 13 | 84 | Why Liquorix? | "A generic kernel needs forced prioritization (fixed CPU assignment, SCHED_FIFO) because it reacts conservatively" | DET | WARN | Übertrieben. Stock-Kernel "profitiert von" manueller Priorisierung bei latenzempfindlichen Workloads, "braucht" sie aber nicht. Viele Workloads laufen ohne. | "needs" abschwächen zu "benefits from" | |
| 14 | 86 | Why Liquorix? | "Fixed CPU pinning or aggressive priority escalation are counterproductive under Liquorix" | FAK | WARN | Plausibel aus Scheduler-Theorie (taskset(1) entzieht dem Scheduler Freiheitsgrade, SCHED_FIFO umgeht PDS-Fairness). Keine Liquorix/PDS-spezifische Quelle belegt dies direkt. | Abschwächen: "can be counterproductive" statt "are counterproductive". Theoretische Basis transparent machen. | |
| 15 | 134 | Resources | Forum-URL `techpatterns.com/forums/forum-34.html` | AKT | OK | Forum aktiv, letzter Post: 2026-02-02. Maintainer damentz ist aktiv. | — | |
| 16 | 136 | Resources | GitHub-URL `github.com/damentz/liquorix-package/issues` | AKT | OK | Aktiv, 4 offene Issues, 335 Stars. | — | |

---

## Struktur-Review

| Aspekt | Bewertung | Anmerkung |
|--------|-----------|-----------|
| Fehlende Themen | WARN | Kein Hinweis auf den offiziellen One-Liner-Installer (`curl ... \| sudo bash`), der die manuelle Installation erheblich vereinfacht. Kein Hinweis auf `CONFIG_CPU_FREQ_DEFAULT_GOV_PERFORMANCE=y` (Default-Governor ist `performance`, nicht `schedutil` — relevant für systemtuning.md-Querverweis). |
| Überflüssiges | WARN | "Features and Compatibility"-Abschnitt (Z. 70–76) enthält überwiegend vage Marketingsprache ohne Linux-spezifischen oder faktischen Gehalt. "Conclusion" (Z. 138–140) wiederholt Intro ohne Mehrwert. |
| Zielgruppe | OK | Installation und Maintenance sind auf richtigem Level. "Why Liquorix?" ist konzeptionell gut, inhaltlich aber falsch. |
| Struktur | WARN | "Features and Compatibility" und "Why Liquorix?" überlappen thematisch. Besser zusammenführen. "Support > Documentation and Resources" könnte schlanker sein. |
| Querverweise | OK | Link zu systemtuning.md vorhanden (Z. 88). Link zu nvidia.md + DKMS vorhanden (Z. 123). |
| Markdown/Format | WARN | Z. 18, 25, 49, 56, 94: Einleitungssätze vor Code-Blöcken ohne Leerzeile zum Block. Z. 101: Text vor Nummerierter Liste ohne Leerzeile. |

---

## Gesamtbewertung: D

6 FAIL-Findings, davon 1 kritischer Faktenfehler (falscher Scheduler) und 2 Installation-Blocker (GPG-URL 404, veraltete Setup-Befehle). Der "Why Liquorix?"-Abschnitt basiert auf dem falschen Scheduler und muss komplett überarbeitet werden. Der "Features and Compatibility"-Abschnitt enthält unbelegte Behauptungen. Die Seite braucht eine grundlegende Überarbeitung.

---

## Korrekturen umgesetzt (2026-02-15)

Alle FAIL- und WARN-Findings korrigiert. Seite grundlegend überarbeitet:

### Inhaltliche Korrekturen

| Finding | Aktion |
|---------|--------|
| #3 GPG-URL 404 | URL korrigiert zu `liquorix-keyring.gpg` |
| #4 Repository-Setup | Keyring-Pfad → `/etc/apt/keyrings/`, Codename via `/etc/os-release`, `arch=amd64` ergänzt |
| #8 DSA-Kompatibilität | Komplett ersetzt durch ehrlichen Sicherheitshinweis (nicht von DSAs abgedeckt, Single Maintainer) |
| #9 Treiberoptimierung | Unbelegte Behauptung entfernt |
| #10 Falscher Scheduler | EEVDF → PDS korrigiert, mit Quelle (journalctl, /proc/config.gz, liquorix.net) |
| #12 Scheduler-Beschreibung | Komplett neu geschrieben für PDS (Skiplist-Datenstruktur, Prioritäten/Deadlines) |
| #1 "Community maintained" | → "maintained by Steven Barrett" |
| #2 8 GB RAM | Entfernt (keine offizielle Quelle) |
| #6 Beispielversion | `6.6.0` → `6.18.10` aktualisiert |
| #7 Vage Features | Ersetzt durch konkrete Vergleichstabelle (PDS, 1000 Hz, Full Preempt, Governor, Tick) |
| #13 "needs forced prioritization" | → "benefits from explicit tuning" |
| #14 "are counterproductive" | → "can be counterproductive" |

### Strukturelle Änderungen

- "Features and Compatibility" und "Why Liquorix?" zusammengeführt zu einem "Why Liquorix?"-Abschnitt mit Vergleichstabelle
- "Conclusion" entfernt (wiederholte Intro ohne Mehrwert)
- Offizieller One-Liner-Installer als "Quick Install (Recommended)" ergänzt
- Neue Diagnose-Befehle im Troubleshooting: `cpupower frequency-info`, `dmesg | grep sched`

### Lektorat

Seite nach Korrekturen als Ganzes geprüft. Ergebnis: Guter Lesefluss, klare Progression (Intro → Installation → Why → Maintenance → Support). Vergleichstabelle vermittelt technische Unterschiede effektiv. Keine Redundanzen, einheitliche Terminologie, angemessener Detailgrad.

### Markdown-Check

MARKDOWN_RULES.txt geprüft. Alle Code-Blöcke mit Leerzeile vor und nach dem Block. Listen-Einrückung konsistent (4 Spaces). Keine fehlenden Leerzeilen nach Überschriften. Kein Doppelpunkt am Ende von Überschriften vor Listen.

### Build

`mkdocs build` — Markdown-Verarbeitung fehlerfrei. Build bricht bei Video-Symlink ab (NFS-Share nicht gemountet) — nicht durch unsere Änderungen verursacht. Maps-Warnungen sind bekannte Pre-existing Issues.
