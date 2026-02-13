# Faktencheck

Prueft eine fertig umgesetzte Dokumentationsseite gegen Primaerquellen. Korrigiert Fehler in DE + EN, bereinigt Versionsnummern und ergaenzt einen Quellenabschnitt am Seitenende. Entspricht Phase 4 des Dokumentations-Workflows.

## Argumente

`$ARGUMENTS`: Dateiname der zu pruefenden Seite (ohne Pfad, ohne Sprachprefix)

| Aufruf | Beschreibung |
|--------|-------------|
| `/faktencheck nvidia.md` | Prueft `docs/en/nvidia.md` + DE-Gegenstueck |
| `/faktencheck xplane/config.md` | Prueft `docs/en/xplane/config.md` + DE |

---

## Pre-Flight

| Voraussetzung | Pruefung | Schwere |
|---------------|---------|---------|
| Argument gesetzt | `$ARGUMENTS` darf nicht leer sein | Blocker |
| EN-Seite existiert | `docs/en/$ARGUMENTS` muss existieren | Blocker |
| DE-Seite existiert | `docs/de/$ARGUMENTS` muss existieren | Blocker |
| Status mindestens `umgesetzt` | Eintrag in `TODO.md` pruefen | Warnung |

Bei Blocker: Fehlermeldung ausgeben und abbrechen.

---

## Phase 1 — Bestandsaufnahme

### 1.1 Seiten einlesen

```
Read: docs/en/$ARGUMENTS  (Pruefgrundlage — Quellen sind englisch)
Read: docs/de/$ARGUMENTS  (wird spaeter angeglichen)
```

### 1.2 Research-Papers lesen

```
Glob: research/**/*<thema>*.md
```

Bestehende Research-Papers und Lektorate als Kontext laden. Nicht erneut recherchieren was bereits verifiziert wurde.

### 1.3 Pruefbare Behauptungen extrahieren

Aus der EN-Seite alle pruefbaren Aussagen identifizieren:

**Extrahieren:**

- Konkrete Befehle und ihre beschriebene Wirkung
- Konfigurationswerte und ihre behauptete Auswirkung
- Kausalaussagen ("X bewirkt Y", "weil Z")
- Kompatibilitaetsaussagen ("funktioniert mit/ohne Z")
- Vergleichsaussagen ("X ist schneller/besser als Y")
- Voraussetzungen und Abhaengigkeiten ("erfordert Paket X")

**Nicht pruefen:**

- Allgemeinwissen ("SSDs sind schneller als HDDs")
- Subjektive Wertungen ("fuehlt sich fluessiger an")
- Reine UI-Beschreibungen
- Ueberschriften, Einleitungssaetze ohne faktischen Gehalt

---

## Phase 2 — Verifikation (parallele Subagents)

### 2.1 Quellenstrategie

Primaerquellen in Reihenfolge der Zuverlaessigkeit:

1. Offizielle Projektdokumentation
2. GitHub-Repositories (READMEs, Changelogs, Issues)
3. Arch Wiki
4. Debian-spezifisch (wiki, packages, manpages)
5. Man-Pages

**Quellenaktualitaet:** Nur ab 2024. Aeltere nur bei stabiler Information (Kernel-Docs, POSIX).

### 2.2 Parallele Pruefung

Fuer jede Behauptung (oder thematische Gruppe) einen Subagent starten:

- WebSearch fuer aktuelle Informationen
- WebFetch fuer freigegebene Domains
- Jedes Finding mit Direkt-Zitat oder konkretem Datenpunkt belegen
- Nicht verifizierbare Claims als N/V markieren

### 2.3 Bewertung

Pro Behauptung eine Bewertung vergeben:

| Bewertung | Bedeutung |
|-----------|-----------|
| **OK** | Korrekt und angemessen |
| **WARN** | Technisch nicht falsch, aber ungenau/unvollstaendig/veraltet |
| **FAIL** | Falsch oder irrefuehrend, muss korrigiert werden |
| **N/V** | Nicht verifizierbar (keine oeffentliche Quelle) |

---

## Phase 3 — Faktencheck-Dokument schreiben

**Datei:** `research/<kategorie>/FAKTENCHECK_<dateiname>.md`

**Struktur:**

```markdown
# Faktencheck: <Seitenname> (EN + DE)

**Datum:** YYYY-MM-DD
**Gepruefte Seiten:** `<dateiname_en>`, `<dateiname_de>`
**Primaerquellen verifiziert:** <Liste der Domains>

---

## Fehler (<Anzahl>) — Korrekturbedarf

### 1. <Kurzbezeichnung>
**Datei:** `<dateiname>:<zeile>`
**Behauptung:** <Zitat aus der Seite>
**Befund:** <Was die Primaerquelle sagt, mit Direkt-Zitat>
**Korrektur:** <Konkrete Formulierung fuer die Korrektur>

## Nuancen (<Anzahl>) — verbesserbar, aber akzeptabel

### N. <Kurzbezeichnung>
**Datei:** `<dateiname>:<zeile>`
**Befund:** <Was ungenau ist und warum>

## Korrekt (<Anzahl>) — keine Aenderung noetig

| # | Behauptung | Quelle |
|---|------------|--------|
```

---

## Phase 4 — Ergebnisse vorlegen

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
FAKTENCHECK: <dateiname>
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

BEHAUPTUNGEN:
├─ Geprueft:  <Anzahl>
├─ OK:        <Anzahl>
├─ WARN:      <Anzahl>
├─ FAIL:      <Anzahl>
└─ N/V:       <Anzahl>

FEHLER (Korrekturbedarf):
│  1. <Kurzbezeichnung> (Zeile <N>)
│  2. ...

NUANCEN (verbesserbar):
│  1. <Kurzbezeichnung> (Zeile <N>)
│  2. ...

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

Per AskUserQuestion den User fragen:

1. **Fehler:** Welche FAIL-Findings sollen korrigiert werden? (Default: alle)
2. **Nuancen:** Welche WARN-Findings sollen verbessert werden?
3. **N/V:** Behauptungen belassen oder entfernen?

---

## Phase 5 — Korrekturen umsetzen

### 5.1 EN-Seite korrigieren

Fuer jedes freigegebene Finding:

1. Korrektur in `docs/en/$ARGUMENTS` einarbeiten
2. Gegen das Finding gegenlesen (keine neuen Fehler einfuehren)

### 5.2 DE-Seite anpassen

DE-Seite an die korrigierte EN-Version angleichen:

1. `docs/de/$ARGUMENTS` lesen
2. Alle Korrekturen uebertragen (nicht 1:1 uebersetzen, sondern sinnerhaltend anpassen)

### 5.3 Versionsnummern bereinigen

Entscheidungsbaum aus `research/AUDIT_FLOW.md` anwenden:

- Harte Mindestanforderungen → behalten
- Verhaltens-Grenzen → behalten + Verifikationsbefehl
- Illustrative Versionen → entfernen oder Meta-Formulierung
- Tabellen mit Versionen → behalten

### 5.4 Quellenabschnitt ergaenzen

Am Ende beider Seiten (EN + DE) einen Quellenabschnitt einfuegen:

```markdown
## Sources / Quellen

- [<Titel>](<URL>) — <Kurzbeschreibung>
```

Nur offizielle, belastbare Quellen. Maximal 5-8 Eintraege.

---

## Phase 6 — Abschluss

### 6.1 Markdown-Check

`docs/MARKDOWN_RULES.txt` lesen und auf beide Seiten anwenden. Verstoesse automatisch korrigieren.

### 6.2 Build pruefen

```
Bash: mkdocs build
```

Bei Fehlern: Korrigieren und erneut bauen.

### 6.3 TODO.md aktualisieren

Status des Themas auf `geprueft` setzen.

### 6.4 Zusammenfassung

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
FAKTENCHECK ABGESCHLOSSEN: <dateiname>
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

KORREKTUREN:
├─ FAIL korrigiert:     <Anzahl>
├─ WARN verbessert:     <Anzahl>
├─ Versionen bereinigt: <Anzahl>
└─ Quellen ergaenzt:    <Anzahl>

DATEIEN GEAENDERT:
├─ docs/en/<dateiname>
├─ docs/de/<dateiname>
├─ research/<kat>/FAKTENCHECK_<dateiname>.md
└─ TODO.md

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**NICHT committen.** Der Commit erfolgt ueber `/abschluss`.

---

## Hinweise

- **EN first:** Pruefung immer auf der EN-Seite (Quellen sind englisch). DE wird nachgezogen.
- **Primaerquellen:** Nur offizielle Docs, Kernel-Docs, Arch Wiki, GitHub. Keine Foren/Blogs.
- **Quellenaktualitaet:** Nur ab 2024, aeltere nur bei stabiler Information.
- **Belegpflicht:** Jedes FAIL/WARN braucht ein Direkt-Zitat, nicht nur eine URL.
- **Referenzplattform:** Debian Stable/Testing. Distributionsabweichungen sind kein Fehler.
- **Versionsnummern:** Entscheidungsbaum in `research/AUDIT_FLOW.md` beachten.
- **Markdown-Regeln:** `docs/MARKDOWN_RULES.txt` automatisch anwenden.
- **Kein Commit:** Der Commit erfolgt ueber `/abschluss`.
