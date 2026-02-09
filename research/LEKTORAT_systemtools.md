# Lektorat: systemtools.md — Linux-Systemtools für Performance-Analyse

Datum: 2026-02-09
Research-Papers: `cpu_monitoring_tools.md`, `io_monitoring_tools.md`, `interrupt_monitoring_tools.md`, `Linux_Monitoring_Tools_Combined.md`

---

## 1. Redaktionelle Bewertung der recherchierten Tools

### Aufnahme empfohlen (hoher Mehrwert, direkte Relevanz zu systemtuning.md)

| Tool | Kategorie | Begründung | Haltbarkeit |
|------|-----------|------------|-------------|
| htop | CPU | Standard-Tool, jeder kennt es, visueller Einstieg | Sehr hoch — stabil seit Jahren |
| btop | CPU | Modernes Dashboard, zeigt CPU+RAM+Disk+Net gleichzeitig | Hoch — aktiv entwickelt |
| cpupower | CPU | Governor prüfen und setzen — direkt aus systemtuning.md referenzierbar | Sehr hoch — Kernel-Tool |
| s-tui | CPU | Governor-Verifikation mit Graphen, Thermal-Throttling-Erkennung | Hoch — stabil |
| turbostat | CPU | Einziges Tool für echte Hardware-Frequenzen + C-States pro Core | Sehr hoch — Kernel-Tool |
| mpstat | CPU+IRQ | Per-Core-Aufschlüsselung inkl. %irq/%soft — IRQ-Shielding-Verifikation | Sehr hoch — sysstat |
| powertop | Power | C-State-Residency, P-States — validiert systemtuning.md Parameter | Sehr hoch — Intel-maintained |
| iotop | IO | Per-Prozess IO-Bandwidth — wer verursacht Stutter? | Hoch — iotop-c aktiv |
| iostat | IO | Device-Level-Latenz (r_await) — NVMe-Sättigung erkennen | Sehr hoch — sysstat |
| ioping | IO | Direkteste NVMe APST Wake-Up-Erkennung | Hoch — stabil |
| nvme-cli | IO | NVMe Power States direkt abfragen — ergänzt ioping | Sehr hoch — Kernel-Tool |
| glances | Dashboard | Web-UI ideal für Fullscreen-Gaming, breite Metrik-Abdeckung | Hoch — aktiv entwickelt |
| /proc/interrupts | IRQ | Kernel-Interface, Basis für alles — muss erklärt werden | Maximal — Kernel-API |
| irqtop/lsirq | IRQ | Komfortablere Interrupt-Ansicht als raw /proc/interrupts | Hoch — Teil von util-linux |

### Kurze Erwähnung (nützlich, aber Nische)

| Tool | Begründung |
|------|------------|
| nmon | Batch-Recording für Post-Analyse gut, aber Nischen-Workflow |
| fatrace | Datei-Level-Tracing — nützlich aber speziell |

### Weglassen oder nur als Hinweis

| Tool | Begründung |
|------|------------|
| dool | Kein Debian-Paket, fragliche Maintenance — nicht empfehlenswert |
| blktrace | Zu komplex für die Zielgruppe, Block-Layer-Wissen nötig |
| perf | Mächtig aber komplex — nur als Hinweis für Fortgeschrittene |
| ftrace/trace-cmd | Kernel-Level-Tracing — zu spezialisiert |

---

## 2. Versionsspezifische Informationen

| Information | Bewertung | Behandlung |
|-------------|-----------|------------|
| Debian-Paketnamen | Stabil über Releases | Im Text verwenden |
| Paket-Versionsnummern (z.B. htop 3.2.2) | Ändern sich mit jedem Release | Weglassen — nur Paketnamen |
| turbostat AMD-Support seit Kernel 5.13 | Historisch, alle aktuellen Kernel | Meta-Formulierung: "auf aktuellen Kernels" |
| btop Issue #190 (per-core freq) | Kann sich ändern | Nicht erwähnen — nur Fähigkeit beschreiben |
| glances 3.x vs 4.x | Ändert sich | Nur erwähnen dass Debian-Version älter sein kann |
| util-linux v2.36 für irqtop | Alle aktuellen Debian-Versionen | Weglassen |

---

## 3. Quellen-Bewertung

| Quelle | Qualität | Nutzbar? |
|--------|----------|----------|
| GitHub-Repos (htop, btop, sysstat, etc.) | Primärquelle | Ja — für Quellenabschnitt |
| packages.debian.org | Primärquelle | Ja — Paketinfo |
| docs.kernel.org | Primärquelle | Ja — /proc/interrupts, IRQ affinity |
| Arch Wiki | Sekundärquelle, hohe Qualität | Ja — CPU frequency scaling, NVMe |
| man7.org (Manpages) | Primärquelle | Ja — Referenz |

---

## 4. Seitenstruktur-Plan

### Titel

DE: "Linux-Systemtools"
EN: "Linux System Tools"

### Nav-Position

`Linux > Optimierungen` (nach Systemtuning, vor Dateisystem)

### Gliederung

```
# Linux-Systemtools

Einleitung: Warum Monitoring für Latenz-Tuning wichtig ist.
Verweis auf systemtuning.md — diese Tools verifizieren ob die
dort beschriebenen Einstellungen tatsächlich wirken.

## Installation

Alle empfohlenen Pakete in einem Befehl.

## CPU-Monitoring

### htop — Prozesse und CPU-Auslastung
- Per-Core-Balken, Prozessliste, PROCESSOR-Spalte
- Relevante Hotkeys: H (Threads), t (Baumansicht), P (CPU-Sort)
- Stärke: schneller visueller Überblick

### btop — System-Dashboard
- CPU+RAM+Disk+Net in einem Fenster
- Zeitverlaufs-Graphen
- Stärke: Korrelationen erkennen

### cpupower — Governor prüfen und setzen
- frequency-info: aktueller Governor, Frequenz, Treiber
- frequency-set: Governor wechseln
- Querverweise auf systemtuning.md (Profil A/B Governor)

### s-tui — Governor-Verifikation und Thermal-Throttling
- Frequenz-Graph + Temperatur-Graph
- Governor-Wechsel visuell überprüfen
- Thermal Throttling erkennen
- Optional: Stress-Test

### turbostat — Hardware-Frequenzen und C-States
- Bzy_MHz: echte Taktrate unter Last
- C-State-Residency pro Core
- IRQ-Zähler pro Core
- AMD-Hinweis
- Querverweise auf systemtuning.md (C-States, Governor)

### mpstat — Per-Core-Statistiken und Interrupt-Verteilung
- %usr, %sys, %irq, %soft pro Core
- -I CPU: Hardware-Interrupts pro Core pro Sekunde
- Shielding-Verifikation: Applikations-Cores sollten ~0% irq zeigen
- Querverweise auf systemtuning.md (Interrupt-Shielding)

## IO-Monitoring

### iotop — Welcher Prozess verursacht IO?
- Nur aktive IO: -o Flag
- Stutter-Verursacher identifizieren

### iostat — Device-Level-Latenz
- r_await: durchschnittliche Read-Latenz
- %util: Device-Sättigung
- NVMe APST-Signatur: plötzlicher r_await-Sprung

### ioping — Disk-Latenz messen
- Direct IO für wahre Device-Latenz
- NVMe APST Wake-Up-Test
- Querverweise auf systemtuning.md (NVMe APST)

### nvme-cli — NVMe Power States abfragen
- Power States mit Entry/Exit-Latenz anzeigen
- APST-Konfiguration prüfen
- Ergänzt ioping

## Interrupt-Analyse

### /proc/interrupts — Interrupt-Zähler lesen
- Format erklären (Spalten)
- watch für Echtzeit-Beobachtung
- Nur die wichtigsten Einträge erklären (NMI, LOC, RES)

### irqtop und lsirq — Komfortablere Ansicht
- irqtop: top-Stil mit Delta-Sortierung
- lsirq: Snapshot mit Sortierung nach Zähler

### Interrupt-Shielding verifizieren
- Kombination: mpstat -I CPU + /proc/interrupts
- Prüfung: geschützte Cores zeigen ~0% IRQ-Last
- Verweis auf systemtuning.md Profil B

## System-Dashboards

### glances — Alles auf einen Blick
- Web-UI-Modus: monitoring von anderem Gerät
- Disk-IO-Latenz-Ansicht (L-Taste)
- Ideal für X-Plane im Fullscreen

### powertop — C-States und Energieverhalten
- Idle Stats Tab: C-State-Residency
- Frequency Stats Tab: P-States
- Warnung: --auto-tune ist kontraproduktiv für Gaming
- Querverweise auf systemtuning.md (C-States)

## Szenario-Tabelle

Tabelle: "Was will ich prüfen?" → "Welches Tool?" → "Befehl"

## Quellen

Max 8 Quellen, nur Primärquellen.
```

---

## 5. Designentscheidungen

### Querverweise zu systemtuning.md

Die Seite wird zum **Companion** von systemtuning.md. Jedes Tool-Kapitel, das einen systemtuning.md-Parameter verifiziert, bekommt einen expliziten Querverweis. Struktur: "Dieses Tool verifiziert ob [Einstellung X] aus dem [Systemtuning](systemtuning.md) tatsächlich wirkt."

### Abstufung: Basis vs. Fortgeschritten

- **Haupttext**: htop, btop, cpupower, s-tui, iotop, iostat, ioping, glances — Tools die jeder nutzen kann
- **Eigene Abschnitte**: turbostat, mpstat, powertop, nvme-cli, /proc/interrupts — brauchen Root oder tieferes Verständnis
- **Klappbare Blöcke** (`??? abstract`): nmon (Batch-Recording), fatrace (Datei-Tracing), perf/ftrace (Kernel-Tracing) — nur für Interessierte

### Kein Versionsballast

- Paketnamen ja, Versionsnummern nein
- "Auf aktuellen Debian-Versionen verfügbar" statt "ab Bookworm 12"
- AMD/Intel-Unterschiede nur wo funktional relevant (turbostat, powertop)

### Szenario-Tabelle am Ende

Nicht nach Tool sortiert, sondern nach Frage:
- "Etwas ruckelt während des Flugs" → glances -w
- "Governor-Einstellung prüfen" → cpupower + s-tui
- "NVMe-Latenz testen" → ioping + nvme-cli
- "Interrupt-Shielding verifizieren" → mpstat -I CPU
- "Session aufzeichnen und später analysieren" → nmon -f

---

## 6. Offene Fragen

Keine — Recherche ist vollständig, Struktur klar. Umsetzung kann beginnen.

---

## 7. TODO.md-Update

Status für `systemtools.md` ändern: `offen` → `geplant`
