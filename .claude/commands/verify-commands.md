# Verify Commands

Testet dokumentierte Shell-Befehle auf dem aktuellen Debian-System. Prueft ob die in einer Docs-Seite gezeigten Befehle tatsaechlich funktionieren und die beschriebene Ausgabe erzeugen.

**Zwei-Phasen-Modell:**

- **Phase 3 (autonom):** Read-only-Befehle ohne Root werden selbstaendig ausgefuehrt. Bei Fehlern wird der korrekte Befehl ermittelt.
- **Phase 4 (interaktiv):** Befehle mit sudo oder Schreibzugriff werden dem User VORHER gezeigt. Ausfuehrung NUR nach expliziter Freigabe.

## Argumente

`$ARGUMENTS`: Dateiname der zu pruefenden Seite (ohne Pfad, ohne Sprachprefix)

| Aufruf | Beschreibung |
|--------|-------------|
| `/verify-commands systemtools.md` | Testet Befehle aus `docs/en/systemtools.md` |
| `/verify-commands filesystem.md` | Testet Befehle aus `docs/en/filesystem.md` |

---

## Pre-Flight

| Voraussetzung | Pruefung | Schwere |
|---------------|---------|---------|
| Argument gesetzt | `$ARGUMENTS` darf nicht leer sein | Blocker |
| EN-Seite existiert | `docs/en/$ARGUMENTS` muss existieren | Blocker |
| Debian-basiertes System | `cat /etc/os-release` pruefen | Warnung |

Bei Blocker: Fehlermeldung ausgeben und abbrechen.

---

## Phase 1 — Befehle extrahieren

### 1.1 Seite lesen

```
Read: docs/en/$ARGUMENTS
```

### 1.2 Befehle aus Code-Bloecken extrahieren

Alle `bash`-Code-Bloecke identifizieren. Pro Befehl erfassen:

- **Zeile** in der Quelldatei
- **Abschnitt** (H2/H3-Ueberschrift)
- **Befehl** (exakter Text)
- **Beschreibung** (Kommentar-Zeile darueber oder Kontext aus dem Fliesstext)
- **Kategorie** (siehe 1.3)

### 1.3 Befehle kategorisieren

Jeden Befehl einer Kategorie zuordnen:

| Kategorie | Beschreibung | Phase |
|-----------|-------------|-------|
| `INSTALL` | `apt install` Befehle | **autonom** — Paket-Verfuegbarkeit mit `apt list` pruefen, NICHT installieren |
| `SAFE` | Lesende Befehle ohne sudo | **autonom** — direkt ausfuehren |
| `INTERACTIVE` | Interaktive TUI-Programme (htop, btop, s-tui, glances) | **autonom** — nur Installationscheck |
| `LONG-RUNNING` | Dauer-Monitoring (watch, Endlos-Loops) ohne sudo | **autonom** — Timeout-Version |
| `SUDO-READ` | Lesende Befehle mit sudo | **interaktiv** — braucht Root |
| `SUDO-WRITE` | Befehle die System-State aendern (z.B. Governor setzen) | **interaktiv** — mit Warnung |
| `HARDWARE` | Braucht spezifische Hardware (NVMe, GPU) | Phase haengt davon ab ob sudo noetig ist |
| `LOOP` | For-Schleifen, mehrzeilige Skripte | Phase haengt davon ab ob sudo noetig ist |

**Zuordnungsregel fuer Mischkategorien:**

- HARDWARE/LOOP **ohne sudo** → autonom (Phase 3)
- HARDWARE/LOOP **mit sudo** → interaktiv (Phase 4)

---

## Phase 2 — Uebersicht zeigen

Dem User eine Tabelle aller extrahierten Befehle praesentieren:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
VERIFY COMMANDS: <dateiname>
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

BEFEHLE GEFUNDEN: <Anzahl>

PHASE 3 — AUTONOM (read-only, kein Root):
│ #  │ Kategorie       │ Abschnitt        │ Befehl (gekuerzt)
│  1 │ INSTALL         │ Installation     │ sudo apt install htop btop ...
│  2 │ SAFE            │ cpupower         │ cpupower -c all frequency-info -p
│  3 │ INTERACTIVE     │ htop             │ htop
│  ...

PHASE 4 — INTERAKTIV (sudo / schreibend):
│ #  │ Kategorie       │ Abschnitt        │ Befehl (gekuerzt)
│  8 │ SUDO-READ       │ turbostat        │ sudo turbostat --show ...
│  9 │ SUDO-WRITE      │ cpupower         │ sudo cpupower frequency-set -g ...
│  ...

ZUSAMMENFASSUNG:
├─ Autonom (Phase 3):     <n> Befehle
└─ Interaktiv (Phase 4):  <n> Befehle
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

Per AskUserQuestion den User fragen:

- **Phase 3 starten?** (Autonomer Durchlauf aller read-only Befehle)
- Optional: **Bestimmte Nummern ueberspringen?**

---

## Phase 3 — Autonomer Test (read-only, kein Root)

Alle INSTALL, SAFE, INTERACTIVE, LONG-RUNNING (ohne sudo), HARDWARE (ohne sudo) und LOOP (ohne sudo) Befehle **selbstaendig** ausfuehren. Kein AskUserQuestion pro Befehl.

### 3.1 Ausfuehrung

Befehle parallel oder sequentiell via Bash-Tool ausfuehren:

**INSTALL:**

```bash
# Nicht installieren — nur pruefen ob Paket verfuegbar
apt list <paketname> 2>/dev/null
# Und ob bereits installiert
dpkg -l <paketname> 2>/dev/null | grep -E "^ii"
```

**SAFE:**

- Direkt ausfuehren via Bash-Tool
- Timeout: 10 Sekunden

**INTERACTIVE:**

- Nur pruefen ob das Programm installiert und aufrufbar ist:
  ```bash
  which <programm> && <programm> --version 2>/dev/null || <programm> --help 2>/dev/null | head -3
  ```

**LONG-RUNNING (ohne sudo):**

- Begrenzte Version ausfuehren: z.B. `mpstat -P ALL 1 2` statt `mpstat -P ALL 1`
- `watch`-Befehle: den inneren Befehl einmalig ausfuehren

**HARDWARE (ohne sudo):**

- Vorher pruefen ob Hardware vorhanden:
  ```bash
  ls /dev/nvme* 2>/dev/null  # NVMe
  lspci | grep -i "vga\|3d\|display"  # GPU
  ```
- Falls nicht vorhanden: als SKIP markieren

**LOOP (ohne sudo):**

- Ausfuehren mit angemessenem Timeout

### 3.2 Bei Fehlern: Korrekten Befehl ermitteln

Wenn ein Befehl fehlschlaegt (Exit-Code != 0, unerwarteter Output):

1. **Ursache analysieren:** Falscher Parameter? Programm nicht installiert? Permission denied (→ braucht doch sudo)?
2. **Korrekten Befehl ermitteln:** Hilfe-Seite pruefen (`--help`), Parameter anpassen, alternativen Befehl finden
3. **Korrektur notieren:** Originaler Befehl, Fehler, korrigierter Befehl — fuer Phase 5

### 3.3 Ergebnis-Tabelle

Nach Abschluss dem User die Ergebnisse zeigen:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
PHASE 3 ABGESCHLOSSEN (autonom)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

│  # │ Befehl (gekuerzt)              │ Ergebnis │ Anmerkung
│  1 │ apt list htop btop ...          │ OK       │ alle Pakete installiert
│  2 │ cpupower frequency-info -p      │ OK       │ Governor: ondemand
│  3 │ ioping -c 20 -D /dev/nvme0n1   │ FAIL     │ Permission denied → braucht sudo
│  ...

KORREKTURBEDARF:
│  3. Zeile 175: `ioping ...` → `sudo ioping ...` (Permission denied)
│  ...
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

Per AskUserQuestion fragen:

- **Weiter mit Phase 4?** (Interaktiver Durchlauf der sudo/write-Befehle)

---

## Phase 4 — Interaktiver Test (sudo / schreibend)

Fuer jeden sudo- oder schreibenden Befehl, in der Reihenfolge der Quelldatei:

### 4.1 Befehl vorstellen

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[<N>/<Total>] <Abschnitt>
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Zeile:      <Zeilennummer>
Kategorie:  <SUDO-READ|SUDO-WRITE|...>
Beschreibung: <Was der Befehl laut Doku tun soll>

Befehl:
  <exakter Befehl aus der Doku>
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### 4.2 User-Entscheidung

Per AskUserQuestion fragen:

| Option | Beschreibung |
|--------|-------------|
| **Ausfuehren** | Befehl wie gezeigt ausfuehren |
| **Aendern** | User gibt modifizierten Befehl ein (z.B. anderes Device, anderer Intervall) |
| **Ueberspringen** | Zum naechsten Befehl |
| **Abbrechen** | Test-Durchlauf beenden |

Befehle in Gruppen von 3-5 praesentieren wenn sie thematisch zusammengehoeren, damit der User mit einer Antwort mehrere freigeben kann.

### 4.3 Befehl ausfuehren

Kategorieabhaengige Ausfuehrung:

**SUDO-READ:**

- Direkt ausfuehren via Bash-Tool
- Timeout: 10 Sekunden

**SUDO-WRITE:**

- Zusaetzliche Warnung: "Dieser Befehl aendert den System-State"
- Aktuellen Zustand VORHER erfassen (z.B. aktuellen Governor lesen vor Governor-Wechsel)
- Nach Test: Originalzustand wiederherstellen und User informieren

**HARDWARE (mit sudo):**

- Vorher pruefen ob Hardware vorhanden
- Falls nicht vorhanden: ueberspringen mit Hinweis

**LOOP (mit sudo):**

- Gesamtes Skript zeigen
- Bei Freigabe: ausfuehren mit angemessenem Timeout

**LONG-RUNNING (mit sudo):**

- Timeout-Version anbieten: z.B. `mpstat -P ALL 1 3` statt `mpstat -P ALL 1`
- `watch`-Befehle: inneren Befehl einmalig ausfuehren

### 4.4 Ergebnis bewerten

Nach der Ausfuehrung:

- **Output zeigen** (gekuerzt auf max 30 Zeilen)
- **Bewertung:**

| Ergebnis | Bedeutung |
|----------|-----------|
| OK | Befehl funktioniert, Output entspricht Beschreibung |
| WARN | Befehl funktioniert, aber Output weicht von Beschreibung ab |
| FAIL | Befehl schlaegt fehl (Exit-Code != 0, Programm nicht gefunden) |
| SKIP | Uebersprungen (Hardware fehlt, User-Entscheidung) |

- Bei WARN/FAIL: kurze Erklaerung was abweicht

### 4.5 Weiter zum naechsten Befehl

Automatisch mit dem naechsten Befehl fortfahren (zurueck zu 4.1).

---

## Phase 5 — Zusammenfassung

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
VERIFY COMMANDS ABGESCHLOSSEN: <dateiname>
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

ERGEBNISSE:
├─ Getestet:     <Anzahl>
├─ OK:           <Anzahl>
├─ WARN:         <Anzahl>
├─ FAIL:         <Anzahl>
└─ SKIP:         <Anzahl>

DETAILS:
│  # │ Befehl (gekuerzt)              │ Ergebnis │ Anmerkung
│  1 │ apt install htop btop ...       │ OK       │ alle Pakete installiert
│  3 │ cpupower frequency-info -p      │ OK       │ Governor: ondemand
│  5 │ turbostat --show ...            │ FAIL     │ Permission denied (kein sudo)
│  ...

KORREKTURBEDARF:
│  <Nr>. Zeile <N>: `<alter Befehl>` → `<korrigierter Befehl>` (<Grund>)
│  ...
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### 5.1 Ergebnis-Dokument schreiben

**Datei:** `research/<kategorie>/VERIFY_<dateiname>.md`

Kategorie gemaess CLAUDE.md Research-Kategorien bestimmen. Ergebnis-Tabelle, Korrekturbedarf und Datum festhalten. Falls die Datei existiert: **ueberschreiben** (Verify-Ergebnisse sind immer systemspezifisch und nur der letzte Lauf ist relevant).

### 5.2 Korrekturen vorschlagen

Falls FAIL/WARN-Befehle gefunden wurden, dem User vorschlagen:

- Doku-Befehl korrigieren? (EN + DE)
- Fehlende Pakete installieren?
- Hinweis in der Doku ergaenzen?

Freigegebene Korrekturen direkt in `docs/en/$ARGUMENTS` und `docs/de/$ARGUMENTS` einarbeiten.

**NICHT automatisch committen.** Falls Doku-Aenderungen noetig sind, `/abschluss` verwenden.

---

## Hinweise

- **Autonom vs. Interaktiv:** Kein sudo und read-only → autonom. Alles andere → User fragen.
- **Kein Blind-Install:** `apt install` wird NIE ausgefuehrt — nur Verfuegbarkeits-Check
- **State wiederherstellen:** Bei SUDO-WRITE den Originalzustand nach dem Test wiederherstellen
- **Timeouts:** Alle Befehle mit angemessenem Timeout ausfuehren (Default: 10s)
- **Hardware-Checks:** Vor Hardware-spezifischen Befehlen pruefen ob die Hardware existiert
- **NVMe-Device:** Falls `/dev/nvme0n1` nicht existiert, nach vorhandenen Block-Devices suchen und dem User alternatives Device vorschlagen
- **Output-Laenge:** Lange Outputs auf 30 Zeilen kuerzen, vollen Output bei Bedarf zeigen
- **Debian-Referenz:** Tests beziehen sich auf Debian Stable/Testing — andere Distros koennen abweichen
- **Fehlerkorrektur:** Bei FAIL in Phase 3 den korrekten Befehl ermitteln (--help, manpage) und als Korrekturvorschlag notieren
- **Platzhalter erkennen:** Befehle mit `<device>`, `<pid>`, `<path>` oder aehnlichen Platzhaltern in spitzen Klammern sind keine woertlichen Befehle. Vor Ausfuehrung durch echte Systemwerte ersetzen (z.B. `/dev/nvme0n1`, aktuelle PID). Bei Unsicherheit: User fragen
