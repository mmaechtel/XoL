# XoL Content Audit — Flow & Arbeitsplan

## Ziel

Systematische Prüfung aller EN-Kapitel auf Faktenrichtigkeit, Aktualität, Relevanz und Detailgrad. DE-Seiten werden nach jeder Runde an die geprüfte EN-Version angeglichen.

**Referenzplattform:** Debian Stable/Testing. Abweichungen auf anderen Distributionen sind kein Fehler, sofern der Text keine distributionsunabhängige Gültigkeit behauptet.

---

## Audit-Flow (pro Kapitel)

```
┌─────────────────────────────────────────────────────┐
│  SCHRITT 1 — Deep Analysis (Claude, autonom)        │
│                                                     │
│  Kapitel lesen, prüfbare Behauptungen extrahieren.  │
│  Gegen Primärquellen prüfen (WebFetch/WebSearch).   │
│  Audit-Tabelle erstellen + Gesamtbewertung.         │
│                                                     │
│  ► Output: research/<kat>/AUDIT_<datei>.md          │
└──────────────────────┬──────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────┐
│  SCHRITT 2 — Expert Review (Claude, autonom)        │
│                                                     │
│  Zweiter Durchgang mit Fokus auf:                   │
│  - Fehlende Themen (nur wenn unverzichtbar)         │
│  - Überflüssiges (nicht Linux-spezifisch?)          │
│  - Zielgruppen-Passung (zu technisch? zu flach?)    │
│  - Strukturelle Kohärenz (Reihenfolge, Querverw.)   │
│  Empfehlungen in Audit-Tabelle ergänzen.            │
│                                                     │
│  ► Output: im selben AUDIT_<datei>.md ergänzt       │
└──────────────────────┬──────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────┐
│  SCHRITT 3 — Review mit User                        │
│                                                     │
│  Audit-Tabelle + Empfehlungen vorlegen.             │
│  User entscheidet pro Finding (Entscheidung-Spalte):│
│  - Korrigieren (Fehler/Ungenauigkeit)               │
│  - Ergänzen (fehlendes Thema)                       │
│  - Kürzen (überflüssig/off-topic)                   │
│  - Belassen (akzeptabel)                            │
└──────────────────────┬──────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────┐
│  SCHRITT 4 — Korrekturen umsetzen (EN)              │
│                                                     │
│  4a. Freigegebene Änderungen in EN-Seite einarbeit. │
│  4b. Jede Korrektur gegen Audit-Finding gegenlesen. │
│  4c. mkdocs build zur Prüfung.                      │
│  4d. Fortschritts-Tracker mit Datum aktualisieren.  │
└──────────────────────┬──────────────────────────────┘
                       │
                       ▼
              ═══ Nächstes Kapitel ═══

┌─────────────────────────────────────────────────────┐
│  SCHRITT 5 — DE-Angleichung (nach jeder Runde)      │
│                                                     │
│  Nach Abschluss einer Runde (nicht erst am Ende!):  │
│  DE-Seiten an geprüfte EN-Versionen der Runde       │
│  anpassen.                                          │
└─────────────────────────────────────────────────────┘
```

---

## Sitzungs-Management

- Jedes Kapitel wird in einer eigenen Konversation auditiert (Schritt 1+2 zusammen).
- Output wird persistiert nach `research/<kategorie>/AUDIT_<dateiname>.md`, bevor die Sitzung endet.
- Fortschritts-Tracker in `AUDIT_STATUS.md` wird nach jedem abgeschlossenen Schritt mit Datum aktualisiert.
- **Startbefehl pro Kapitel:** `Audit <dateiname> gemäß research/AUDIT_FLOW.md`
- Schritt 3 (User-Review) kann in derselben oder einer neuen Sitzung stattfinden.
- Schritt 4 (Korrekturen) erfolgt nach User-Freigabe, ggf. in neuer Sitzung.

---

## Audit-Tabelle (Template)

Pro Kapitel wird diese Tabelle in `research/<kategorie>/AUDIT_<dateiname>.md` ausgefüllt:

### Kopf

| Feld | Wert |
|------|------|
| **Datei** | `docs/en/example.md` |
| **Titel** | Page Title |
| **Zeilen** | 000 |
| **Aufwand** | S / M / L |
| **Audit-Datum** | YYYY-MM-DD |
| **Gesamtbewertung** | (siehe unten) |

**Aufwand-Kategorien:**

| Kategorie | Zeilenumfang | Erwartete Dauer |
|-----------|-------------|-----------------|
| S (Small) | <100 Zeilen | ~15 min |
| M (Medium) | 100–250 Zeilen | ~30 min |
| L (Large) | 250+ Zeilen | ~45 min |

### Bewertungsskala

| Note | Bedeutung |
|------|-----------|
| A | Korrekt, vollständig, gut strukturiert — keine Änderungen nötig |
| B | Im Kern korrekt, kleinere Ungenauigkeiten oder Lücken |
| C | Teilweise fehlerhaft oder veraltet, Überarbeitung nötig |
| D | Grundlegende Probleme, Neuschreiben einzelner Abschnitte nötig |

### Detail-Tabelle

| # | Zeile | Abschnitt | Behauptung | Typ | Bewertung | Quelle / Beleg | Empfehlung | Entscheidung |
|---|-------|-----------|------------|-----|-----------|----------------|------------|:------------:|
| 1 | 42 | H2/H3-Ref | Konkrete Aussage | FAK | OK | URL + Zitat | — | |
| 2 | 78 | H2/H3-Ref | Andere Aussage | AKT | WARN | URL + Zitat | Aktion | |

**Typ-Codes:**

| Code | Prüfdimension | Frage |
|------|---------------|-------|
| **FAK** | Faktenprüfung | Ist die Aussage faktisch korrekt? Gegen Primärquelle verifiziert? |
| **AKT** | Aktualität / Haltbarkeit | Ist die Information aktuell? Wird sie beim nächsten Release veralten? Enthält sie unnötige Versionsnummern? |
| **REL** | Relevanz | Ist das Linux-spezifisch und gehört auf diese Seite? |
| **DET** | Detailgrad | Ist der Detailgrad für die Zielgruppe angemessen (zu viel / zu wenig)? |

**Bewertung pro Eintrag:**

- **OK** — Korrekt und angemessen
- **WARN** — Technisch nicht falsch, aber ungenau/unvollständig/veraltet
- **FAIL** — Falsch oder irreführend, muss korrigiert werden
- **N/V** — Nicht verifizierbar (keine öffentliche Quelle). Wird in Schritt 3 dem User vorgelegt.

**Beleganforderung:** Jedes FAIL- und WARN-Finding muss ein Direkt-Zitat oder einen konkreten Datenpunkt aus der Quelle enthalten — nicht nur eine URL. Wenn die Quelle nicht abrufbar ist oder die relevante Information nicht enthält, Bewertung auf N/V setzen.

**Entscheidung-Spalte:** Bleibt in Schritt 1+2 leer. Wird in Schritt 3 vom User ausgefüllt: `Korrigieren` / `Ergänzen` / `Kürzen` / `Belassen`.

### Struktur-Review (Schritt 2)

| Aspekt | Bewertung | Anmerkung |
|--------|-----------|-----------|
| Fehlende Themen | — | Nur melden wenn für das Kernziel der Seite unverzichtbar. Konkreten Lesernutzen benennen. |
| Überflüssiges | — | Was ist nicht Linux-spezifisch oder gehört woanders hin? |
| Zielgruppe | — | Passt der Detailgrad zur Zielgruppe (Linux-Einsteiger mit X-Plane-Erfahrung)? |
| Struktur | — | Logische Reihenfolge? Gute H2/H3-Gliederung? |
| Querverweise | — | Verweise auf andere Seiten korrekt und vollständig? |
| Markdown/Format | — | Einhaltung der MARKDOWN_RULES.txt? |

---

## Was ist eine prüfbare Behauptung?

### Extrahieren (prüfen)

- Konkrete Befehle und ihre beschriebene Wirkung
- Konfigurationswerte und ihre behauptete Auswirkung
- Kausalaussagen ("X bewirkt Y", "weil Z")
- Kompatibilitätsaussagen ("funktioniert mit/ohne Z")
- Vergleichsaussagen ("X ist schneller/besser als Y")
- Voraussetzungen und Abhängigkeiten ("erfordert Paket X")

### Nicht prüfen

- Allgemeinwissen ("SSDs sind schneller als HDDs")
- Subjektive Wertungen ("fühlt sich flüssiger an")
- Reine UI-Beschreibungen ("Klicken Sie auf Einstellungen")
- Wiederholungen einer bereits auf anderer Seite geprüften Aussage (Verweis genügt)
- Überschriften, Einleitungssätze ohne faktischen Gehalt

---

## Quellenaktualität (Tiered)

**Generelle Untergrenze: nur Quellen ab 2024 aufwärts.** Ältere Quellen nur, wenn keine aktuellere Alternative existiert und die Information nachweislich stabil ist (z.B. Kernel-Docs, POSIX-Standards, Architektur-Grundlagen). Zusätzlich nach Informationstyp differenziert:

| Informationstyp | Anforderung | Beispiel |
|-----------------|-------------|---------|
| **Versionsspezifisch** (Treiber, X-Plane, Mesa, Debian-Pakete) | Quelle muss zur aktuell dokumentierten Version passen (nicht älter als 12 Monate) | NVIDIA-Treiberversion, Mesa-Release |
| **Stabile APIs / Konfiguration** (sysctl, Kernel-Parameter, Protokolle) | Quelle muss korrekt sein, Alter egal. Arch Wiki, Kernel-Docs, Man-Pages sind zeitlos gültig solange der beschriebene Parameter existiert. | `vm.swappiness`, X11-Protokoll |
| **Distributionsspezifisch** (Debian-Defaults, Paketnamen, Pfade) | Quelle muss zur dokumentierten Debian-Version passen | Paketname in Trixie vs. Bookworm |
| **Bei Widerspruch** | Neuere Quelle gewinnt immer | — |

---

## Versionsnummern — Entscheidungsbaum

```
Ist die Version eine harte Mindestanforderung?
  (z.B. "erfordert Treiber 555+")
  → JA: Behalten. In Tabelle oder Inline-Code formatieren.

Ist die Version eine Verhaltens-Grenze?
  (z.B. "Default geändert ab Treiber 560")
  → JA: Behalten. Verifikationsbefehl ergänzen, wenn möglich.

Ist die Version rein illustrativ?
  (z.B. "getestet mit Kernel 6.8.3")
  → NEIN: Entfernen oder in klappbaren Block (??? abstract) verschieben.

Steht die Version in einer Tabelle?
  (Treiber-Mindestversionen, Kompatibilitäts-Matrix)
  → JA: Behalten. Tabellen sind das richtige Format für Versionsinformationen.

Im Zweifel:
  → Meta-Formulierung verwenden ("in aktuellen Versionen", "ab der
    aktuellen Stable-Version") und Verifikationsbefehl ergänzen.
```

---

## Kurzcheck-Protokoll

Für bereits geprüfte Seiten (config.md, displayserver*.md) — reduzierter Aufwand:

1. Bestehenden Faktencheck lesen (`research/*/FAKTENCHECK_*.md`)
2. Prüfen, ob alle dokumentierten Korrekturen korrekt eingearbeitet wurden
3. Struktur-Review durchführen (Tabelle aus Schritt 2)
4. Nur neue oder seit dem letzten Check geänderte Abschnitte gegen Quellen prüfen
5. Gesamtnote vergeben

Erwartete Dauer: ~25% eines Full Audit.

---

## Kapitel-Reihenfolge

Priorisierung: Kernseiten zuerst (höchste Leserrelevanz), dann Peripherie.
Nach jeder Runde: DE-Angleichung für die Seiten dieser Runde.

### Runde 1 — Kern-Dokumentation (Full Audit)

| # | Datei | Titel | Zeilen | Aufwand | Prio |
|---|-------|-------|--------|---------|------|
| 1 | `begin.md` | Getting Started | 228 | M | Einstiegsseite — erste Impression |
| 2 | `nvidia.md` | Nvidia Driver | 164 | M | Meistgenutzte GPU-Plattform |
| 3 | `liquorix.md` | Liquorix Kernel | 139 | M | Kernel-Empfehlung |
| 4 | `systemtuning.md` | System Tuning | 441 | L | Größte Seite, höchstes Fehlerrisiko |
| 5 | `systemtools.md` | System Tools | 421 | L | Companion zu #4 |
| 6 | `filesystem.md` | Filesystem | 160 | M | Grundlegendes System-Setup |
| 7 | `xplane/performance.md` | X-Plane Performance | 206 | M | Zentrale Optimierungsseite |

→ Danach: DE-Angleichung Runde 1

### Runde 2 — Bereits geprüft (Kurzcheck)

| # | Datei | Titel | Zeilen | Aufwand |
|---|-------|-------|--------|---------|
| 8 | `xplane/config.md` | X-Plane Config | 335 | S (Kurzcheck) |
| 9 | `displayserver.md` | Display Server Overview | 155 | S (Kurzcheck) |
| 10 | `displayserver_x11.md` | X11 Session | 139 | S (Kurzcheck) |
| 11 | `displayserver_wayland.md` | Wayland Session | 141 | S (Kurzcheck) |

→ Danach: DE-Angleichung Runde 2

### Runde 3 — Scenery & Addons

| # | Datei | Titel | Zeilen | Aufwand |
|---|-------|-------|--------|---------|
| 12 | `scenery_components.md` | World Building Explained | 163 | M |
| 13 | `addon/ortho4xp.md` | Ortho4XP | 221 | M |
| 14 | `addon/autoortho.md` | AutoOrtho | 242 | M |
| 15 | `addon/xearthlayer.md` | XEarthLayer | 133 | M |
| 16 | `addon/static_plus_streaming.md` | Static + Streaming | 109 | M |

→ Danach: DE-Angleichung Runde 3

### Runde 4 — Peripherie & Erweiterungen

| # | Datei | Titel | Zeilen | Aufwand |
|---|-------|-------|--------|---------|
| 17 | `kvm.md` | KVM | 90 | S |
| 18 | `docker.md` | Docker | 102 | M |
| 19 | `wine.md` | Wine | 95 | S |
| 20 | `addon/xorganizer.md` | XOrganizer | 95 | S |
| 21 | `pyenv.md` | pyenv | 161 | M (Light Check) |
| 22 | `zsh.md` | zsh | 82 | S (Light Check) |

→ Danach: DE-Angleichung Runde 4

### Runde 5 — Flight Operations & Referenz

| # | Datei | Titel | Zeilen | Aufwand |
|---|-------|-------|--------|---------|
| 23 | `flight_operations/weather.md` | Weather | 120 | M |
| 24 | `flight_operations/clearance.md` | Clearance | 62 | S |
| 25 | `flight_operations/vatsim.md` | VATSim | 41 | S |
| 26 | `glossary.md` | Glossary | 150 | M |
| 27 | `intro.md` | Introduction | 76 | S |

→ Danach: DE-Angleichung Runde 5

### Nicht im Audit

| Datei | Grund |
|-------|-------|
| `index.md` | Changelog, kein Inhalt |
| `linux.md` | Übersichtsseite, kaum Inhalt (28 Zeilen) |
| `xplane/systemfehler.md` | Stub (38 Zeilen) |
| `xplane/geraeteverluste.md` | Stub (34 Zeilen) |
| `scenery.md` | Stub (52 Zeilen, überwiegend Links) |
| `addon/orthophotography_intro.md` | Stub (41 Zeilen, reine Einleitung) |
| `addon/xroad.md` | Stub (8 Zeilen) |
| `addon/aep.md` | Stub (30 Zeilen) |
| `flight_operations/overview.md` | Stub (8 Zeilen) |
| `about.md` | Meta-Seite, kein technischer Inhalt (23 Zeilen) |
| `blog/*.md` | Erfahrungsberichte, kein technischer Inhalt |
| `Maps.md` | Karten-Embed, kein Prüfbedarf |

---

## Fortschritts-Tracker

**→ Siehe `research/AUDIT_STATUS.md`** — lebende Statusdatei, getrennt von dieser Prozess-Definition. Wird über Audit-Zyklen hinweg geführt.

---

## Arbeitsweise pro Kapitel

### Schritt 1 — Deep Analysis

1. EN-Seite vollständig lesen
2. Prüfbare Behauptungen extrahieren (siehe "Was ist eine prüfbare Behauptung?")
3. Gegen Primärquellen prüfen:
    - Kernel-Docs, Arch Wiki, offizielle Projekt-Docs
    - GitHub-Repos (READMEs, Issues, Changelogs)
    - Man-Pages, Debian-Paketinfos
4. Audit-Tabelle mit allen Findings ausfüllen
    - Jedes FAIL/WARN mit Direkt-Zitat aus Quelle belegen
    - Nicht verifizierbare Claims als N/V markieren
5. Gesamtnote vergeben (A/B/C/D)
6. **Output nach `research/<kategorie>/AUDIT_<dateiname>.md` schreiben**

### Schritt 2 — Expert Review

1. Lückenanalyse: Was fehlt für die Kernaufgabe der Seite? (Nur melden wenn unverzichtbar — konkreten Lesernutzen benennen. Vollständigkeit ist kein Ziel.)
2. Relevanzfilter: Was ist plattformunabhängig und gehört nicht hierher?
3. Strukturbewertung: Logischer Aufbau? Gute H2/H3-Gliederung?
4. Querverweise: Links zu anderen Seiten korrekt?
5. Empfehlungen in Audit-Tabelle ergänzen
6. **Output im selben AUDIT_<dateiname>.md ergänzen**

### Schritt 3 — User-Review

1. Audit-Tabelle + Empfehlungen dem User vorlegen
2. User füllt Entscheidung-Spalte aus pro Finding
3. Entscheidungen werden im AUDIT-Dokument festgehalten

### Schritt 4 — Korrekturen

1. Freigegebene Änderungen in EN-Seite einarbeiten
2. Jede Korrektur gegen das entsprechende Audit-Finding gegenlesen (keine neuen Fehler einführen)
3. `mkdocs build` zur Prüfung
4. Fortschritts-Tracker in `research/AUDIT_STATUS.md` mit Datum aktualisieren

---

## Regeln

- **EN first:** Alle Prüfungen und Korrekturen zuerst in EN. DE-Angleichung nach jeder Runde.
- **Primärquellen:** Nur offizielle Docs, Kernel-Docs, Arch Wiki, GitHub. Keine Foren/Blogs.
- **Quellenaktualität:** Generell nur Quellen ab 2024 aufwärts. Zusätzlich nach Informationstyp differenziert (siehe Abschnitt "Quellenaktualität").
- **Versionsnummern:** Nach Entscheidungsbaum (siehe Abschnitt "Versionsnummern").
- **Belegpflicht:** FAIL/WARN-Findings brauchen Direkt-Zitate, nicht nur URLs. Sonst N/V.
- **Referenzplattform:** Debian Stable/Testing. Distributionsabweichungen sind kein Fehler.
- **Linux-Fokus:** Plattformunabhängige X-Plane-Settings sind out of scope.
- **Vollständigkeits-Bremse:** "Fehlende Themen" nur melden wenn für Kernziel der Seite unverzichtbar.
- **Bereits geprüfte Seiten** (config.md, displayserver*.md): Kurzcheck-Protokoll anwenden.
- **Stubs** (<50 Zeilen oder reine Link-/Einleitungsseiten): Nicht auditen, in "Nicht im Audit" gelistet.

---

## Qualitätssicherung

### Halluzinations-Schutz

- Jedes FAIL/WARN muss ein konkretes Zitat oder einen Datenpunkt aus der Primärquelle enthalten.
- "Quelle bestätigt" ohne Zitat ist nicht akzeptabel — das umgeht die Verifikation.
- Wenn eine Quelle nicht abrufbar ist: N/V setzen, nicht als OK raten.

### Falsch-Positiv-Schutz

- Bewertungen beziehen sich immer auf Debian Stable/Testing als Referenzplattform.
- Abweichungen auf Arch, Fedora etc. sind kein Fehler, sofern der Text keine universelle Gültigkeit behauptet.
- Vor einem FAIL prüfen: Ist die Aussage im Kontext der Seite gemeint oder allgemein?

### Scope-Schutz

- Die Seiten sollen fokussiert bleiben. Ergänzungsempfehlungen brauchen eine Begründung mit konkretem Lesernutzen.
- "Man könnte noch X ergänzen" ist keine valide Empfehlung. "Ohne X kann der Leser Schritt Y nicht ausführen" schon.
