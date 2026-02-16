# Plan: Szenerien-Dateien in eigenes Verzeichnis verschieben

## Ausgangslage

`scenery.md` und `scenery_components.md` liegen in `docs/{lang}/` (Root).
Laut MARKDOWN_RULES.txt ist das die letzte ausstehende Verschiebung.

## Zielstruktur

```
docs/{lang}/scenery/
├── index.md               # Neuer Section Index (Übersichtsseite)
├── scenery.md             # Szenerien (bisher Root)
└── scenery_components.md  # Komponenten (bisher Root)
```

`addon/xorganizer.md` bleibt in `addon/` — wird nur in der Nav unter Szenerien eingehängt.

## Schritte

### 1. Verzeichnisse anlegen + Dateien verschieben

```bash
mkdir -p docs/de/scenery docs/en/scenery
git mv docs/de/scenery.md docs/de/scenery/scenery.md
git mv docs/de/scenery_components.md docs/de/scenery/scenery_components.md
git mv docs/en/scenery.md docs/en/scenery/scenery.md
git mv docs/en/scenery_components.md docs/en/scenery/scenery_components.md
```

### 2. Section Index erstellen

Neue `docs/{lang}/scenery/index.md` anlegen (DE + EN).
Kurze Übersicht mit Links auf die drei Unterseiten (Komponenten, Szenerien, XOrganizer).

### 3. Links IN den verschobenen Dateien anpassen

**scenery_components.md** (7 Glossar-Links + 3 Addon-Links):
- `glossary.md#...` → `../glossary.md#...` (7x, DE + EN)
- `addon/ortho4xp.md` → `../addon/ortho4xp.md`
- `addon/orthophotography_intro.md` → `../addon/orthophotography_intro.md`
- `addon/xorganizer.md` → `../addon/xorganizer.md`

**scenery.md** (3 Addon-Links):
- `../addon/ortho4xp.md` → bleibt `../addon/ortho4xp.md` (gleiche Tiefe nach Move)
- `../addon/autoortho.md` → bleibt `../addon/autoortho.md`
- `../addon/xroad.md` → bleibt `../addon/xroad.md`

### 4. Links VON anderen Dateien anpassen

| Datei | Alter Link | Neuer Link |
|-------|-----------|-----------|
| `de/glossary.md` (2x) | `../scenery_components.md` | `scenery/scenery_components.md` |
| `en/glossary.md` (2x) | `../scenery_components.md` | `scenery/scenery_components.md` |
| `de/addon/static_plus_streaming.md` | `../scenery.md` | `../scenery/scenery.md` |
| `en/addon/static_plus_streaming.md` | `../scenery.md` | `../scenery/scenery.md` |

### 5. mkdocs.yml Nav aktualisieren

```yaml
# VORHER
- Szenerien:
    - Komponenten: de/scenery_components.md
    - Szenerien: de/scenery.md
    - XOrganizer: de/addon/xorganizer.md

# NACHHER
- Szenerien:
    - de/scenery/index.md
    - Komponenten: de/scenery/scenery_components.md
    - Szenerien: de/scenery/scenery.md
    - XOrganizer: de/addon/xorganizer.md
```

Beide Sprachbäume (DE + EN).

### 6. MARKDOWN_RULES.txt aktualisieren

- Verzeichnisbaum: `scenery/` Eintrag ergänzen
- "Noch im Root — ausstehende Verschiebungen": Szenerien-Eintrag entfernen (letzter TODO erledigt)

### 7. TODO.md aktualisieren

Szenerien-Section als erledigt markieren.

### 8. Build + Verify

```bash
mkdocs build
```

Alle Links prüfen, keine Warnings erwartet.

## Hinweis: Glossar-Links prüfen

Die Links in `glossary.md` verwenden `../scenery_components.md` obwohl beide im Root liegen.
Das funktioniert vermutlich wegen MkDocs URL-Auflösung (Output-URLs vs. Source-Pfade).
Nach dem Move auf `scenery/scenery_components.md` muss geprüft werden, ob die neuen
Glossar-Links korrekt auflösen. Im Zweifel mit `mkdocs build` und Browser testen.
