# Abschluss

Aktualisiert den Changelog in `index.md` (DE + EN) und erstellt einen Git-Commit. Wird nach abgeschlossener Arbeit an Dokumentationsseiten aufgerufen.

## Argumente

`$ARGUMENTS`: Optionale Commit-Nachricht

| Aufruf | Beschreibung |
|--------|-------------|
| `/abschluss` | Changelog + Commit, Nachricht wird aus Aenderungen abgeleitet |
| `/abschluss "Kurzbeschreibung"` | Changelog + Commit mit vorgegebener Nachricht |

---

## Pre-Flight

| Voraussetzung | Pruefung | Schwere |
|---------------|---------|---------|
| Aenderungen vorhanden | `git status` zeigt modifizierte/neue Dateien | Blocker |
| Build fehlerfrei | `mkdocs build` laeuft ohne Fehler | Blocker |

Bei Blocker: AskUserQuestion — Problem melden, Abbruch anbieten.

---

## Phase 1 — Aenderungen analysieren

1. **Git-Status pruefen:**
```
Bash: git status
Bash: git diff --name-only
```

2. **Geaenderte Dokumentationsseiten identifizieren:**
   - Nur Dateien unter `docs/` sind changelog-relevant
   - Research-Dateien, Konfiguration etc. werden nicht im Changelog erwaehnt

3. **Art der Aenderungen bestimmen:**
   - Neue Seiten (bisher nicht in git)
   - Ueberarbeitete Seiten (modifiziert)
   - Strukturaenderungen (mkdocs.yml, Navigation)

---

## Phase 2 — Changelog aktualisieren

### 2.1 Changelog-Eintraege formulieren

Eintraege beschreiben **was sich fuer den Leser aendert**, nicht die technische Umsetzung:

- Neue Seite: `Neue Seite [Seitenname](pfad.md) — Kurzbeschreibung`
- Ueberarbeitung: `[Seitenname](pfad.md) ueberarbeitet: Was hat sich geaendert`
- Erweiterung: `[Seitenname](pfad.md) ergaenzt: Was wurde hinzugefuegt`
- Korrektur: `[Seitenname](pfad.md) korrigiert: Was wurde berichtigt`

### 2.2 Eintraege einfuegen

**Datei:** `docs/de/index.md` unter `## Letzte Aenderungen`
**Datei:** `docs/en/index.md` unter `## Recent Changes`

Regeln:
- Neuer Datumsblock (`### YYYY-MM-DD`) **ueber** allen bestehenden Eintraegen
- Falls der aktuelle Tag bereits existiert: Eintraege dort anfuegen (nicht doppelt)
- Bestehende Eintraege NIE loeschen
- DE und EN muessen inhaltlich identisch sein (uebersetzt)

---

## Phase 3 — Build pruefen

```
Bash: mkdocs build
```

Bei Fehlern: Korrigieren und erneut bauen. Erst nach erfolgreichem Build weiter.

---

## Phase 4 — Git-Commit

### 4.1 Dateien stagen

Alle geaenderten Dokumentations- und Konfigurationsdateien einzeln stagen:

```
Bash: git add docs/de/... docs/en/... mkdocs.yml research/...
```

**NICHT stagen:** `.DS_Store`, temporaere Dateien, `.env`, Credentials.

### 4.2 Commit erstellen

Commit-Nachricht:
- Falls `$ARGUMENTS` gesetzt: Diese Nachricht verwenden
- Falls leer: Aus den Aenderungen eine praegende, einzeilige Nachricht ableiten

Format:
```
git commit -m "$(cat <<'EOF'
{Commit-Nachricht}

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>
EOF
)"
```

**NICHT pushen.** Der Push erfolgt nur auf explizite User-Anweisung.

---

## Phase 5 — Zusammenfassung

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
ABSCHLUSS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

CHANGELOG:
├─ DE: {Anzahl} neue Eintraege in index.md
└─ EN: {Anzahl} neue Eintraege in index.md

COMMIT:
├─ Nachricht: {Commit-Nachricht}
├─ Dateien:   {Anzahl} geaendert
└─ Hash:      {Short-Hash}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## Hinweise

- **Kein Push:** Niemals automatisch pushen. Nur auf explizite Anweisung
- **Keine History loeschen:** Bestehende Changelog-Eintraege bleiben erhalten
- **Bilingual:** DE- und EN-Changelog muessen synchron aktualisiert werden
- **Datumsformat:** ISO 8601 (`YYYY-MM-DD`)
- **Commit-Stil:** Einzeilig, im Imperativ, beschreibt die Aenderung praegnant
