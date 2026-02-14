# Verify Commands

Testet dokumentierte Shell-Befehle interaktiv auf dem aktuellen Debian-System. Prueft ob die in einer Docs-Seite gezeigten Befehle tatsaechlich funktionieren und die beschriebene Ausgabe erzeugen.

**Wichtig:** Jeder Befehl wird dem User VORHER gezeigt. Ausfuehrung NUR nach expliziter Freigabe.

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

| Kategorie | Beschreibung | Verhalten |
|-----------|-------------|-----------|
| `INSTALL` | `apt install` Befehle | Paket-Verfuegbarkeit mit `apt list` pruefen, NICHT installieren |
| `SAFE` | Lesende Befehle ohne sudo | Direkt ausfuehrbar nach Freigabe |
| `SUDO-READ` | Lesende Befehle mit sudo | Ausfuehrbar nach Freigabe, braucht Root |
| `SUDO-WRITE` | Befehle die System-State aendern (z.B. Governor setzen) | Nur mit ausdruecklicher Warnung |
| `INTERACTIVE` | Interaktive TUI-Programme (htop, btop, s-tui, glances) | Nicht ausfuehrbar — nur Installationscheck |
| `LONG-RUNNING` | Dauer-Monitoring (watch, Endlos-Loops) | Timeout-Version anbieten |
| `HARDWARE` | Braucht spezifische Hardware (NVMe, GPU) | Hardware-Pruefung vorschalten |
| `LOOP` | For-Schleifen, mehrzeilige Skripte | Als Ganzes zeigen, User entscheidet |

---

## Phase 2 — Uebersicht zeigen

Dem User eine Tabelle aller extrahierten Befehle praesentieren:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
VERIFY COMMANDS: <dateiname>
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

BEFEHLE GEFUNDEN: <Anzahl>

│ #  │ Kategorie    │ Abschnitt        │ Befehl (gekuerzt)
│  1 │ INSTALL      │ Installation     │ sudo apt install htop btop ...
│  2 │ INTERACTIVE  │ htop             │ htop
│  3 │ SAFE         │ cpupower         │ cpupower -c all frequency-info -p
│  ...

KATEGORIEN:
├─ SAFE / SUDO-READ:  <n> (testbar)
├─ INSTALL:            <n> (Paket-Check)
├─ INTERACTIVE:        <n> (nur Installationscheck)
├─ SUDO-WRITE:         <n> (aendert System — mit Warnung)
├─ LONG-RUNNING:       <n> (mit Timeout)
├─ HARDWARE:           <n> (Hardware-Pruefung)
└─ LOOP:               <n> (mehrzeilig)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

Per AskUserQuestion fragen:

- **Welche Kategorien testen?** (Mehrfachauswahl)
- Optional: **Bestimmte Nummern ueberspringen?**

---

## Phase 3 — Interaktiver Test-Durchlauf

Fuer jeden freigegebenen Befehl, in der Reihenfolge der Quelldatei:

### 3.1 Befehl vorstellen

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[<N>/<Total>] <Abschnitt>
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Zeile:      <Zeilennummer>
Kategorie:  <SAFE|SUDO-READ|...>
Beschreibung: <Was der Befehl laut Doku tun soll>

Befehl:
  <exakter Befehl aus der Doku>
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### 3.2 User-Entscheidung

Per AskUserQuestion fragen:

| Option | Beschreibung |
|--------|-------------|
| **Ausfuehren** | Befehl wie gezeigt ausfuehren |
| **Aendern** | User gibt modifizierten Befehl ein (z.B. anderes Device, anderer Intervall) |
| **Ueberspringen** | Zum naechsten Befehl |
| **Abbrechen** | Test-Durchlauf beenden |

### 3.3 Befehl ausfuehren

Kategorieabhaengige Ausfuehrung:

**INSTALL:**

```bash
# Nicht installieren — nur pruefen ob Paket verfuegbar
apt list <paketname> 2>/dev/null
# Und ob bereits installiert
dpkg -l <paketname> 2>/dev/null | grep -E "^ii"
```

**SAFE / SUDO-READ:**

- Direkt ausfuehren via Bash-Tool
- Timeout: 10 Sekunden (falls Befehl haengt)

**SUDO-WRITE:**

- Zusaetzliche Warnung: "Dieser Befehl aendert den System-State"
- Aktuellen Zustand VORHER erfassen (z.B. aktuellen Governor lesen vor Governor-Wechsel)
- Nach Test: Originalzustand wiederherstellen und User informieren

**INTERACTIVE:**

- Nur pruefen ob das Programm installiert und aufrufbar ist:
  ```bash
  which <programm> && <programm> --version 2>/dev/null || <programm> --help 2>/dev/null | head -3
  ```

**LONG-RUNNING:**

- Timeout-Version anbieten: z.B. `mpstat -P ALL 1 3` statt `mpstat -P ALL 1`
- `watch`-Befehle: einmalig statt in Schleife ausfuehren

**HARDWARE:**

- Vorher pruefen ob Hardware vorhanden:
  ```bash
  # NVMe
  ls /dev/nvme* 2>/dev/null
  # GPU
  lspci | grep -i "vga\|3d\|display"
  ```
- Falls nicht vorhanden: ueberspringen mit Hinweis

**LOOP:**

- Gesamtes Skript zeigen
- Bei Freigabe: ausfuehren mit angemessenem Timeout

### 3.4 Ergebnis bewerten

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

### 3.5 Weiter zum naechsten Befehl

Automatisch mit dem naechsten Befehl fortfahren (zurueck zu 3.1).

---

## Phase 4 — Zusammenfassung

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

FAILS/WARNS:
│  <Nr>. <Befehl> — <Was schiefging oder abweicht>
│  ...
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

Falls FAIL/WARN-Befehle gefunden wurden, dem User vorschlagen:

- Doku-Befehl korrigieren?
- Fehlende Pakete installieren?
- Hinweis in der Doku ergaenzen?

**NICHT automatisch committen.** Falls Doku-Aenderungen noetig sind, `/abschluss` verwenden.

---

## Hinweise

- **Immer fragen:** Kein Befehl wird ohne explizite User-Freigabe ausgefuehrt
- **Kein Blind-Install:** `apt install` wird NIE ausgefuehrt — nur Verfuegbarkeits-Check
- **State wiederherstellen:** Bei SUDO-WRITE den Originalzustand nach dem Test wiederherstellen
- **Timeouts:** Alle Befehle mit angemessenem Timeout ausfuehren (Default: 10s)
- **Hardware-Checks:** Vor Hardware-spezifischen Befehlen pruefen ob die Hardware existiert
- **NVMe-Device:** Falls `/dev/nvme0n1` nicht existiert, nach vorhandenen Block-Devices suchen und dem User alternatives Device vorschlagen
- **Output-Laenge:** Lange Outputs auf 30 Zeilen kuerzen, vollen Output bei Bedarf zeigen
- **Debian-Referenz:** Tests beziehen sich auf Debian Stable/Testing — andere Distros koennen abweichen
