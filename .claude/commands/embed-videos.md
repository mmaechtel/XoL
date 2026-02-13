# Embed Videos

Bettet MP4-Videos aus `docs/assets/video/` als HTML5-`<video>`-Tags in die Dokumentation ein. Erstellt/aktualisiert eine zentrale Video-Seite und bettet Videos zusaetzlich in thematisch passende Seiten ein.

## Argumente

`$ARGUMENTS`: Optionaler Verzeichnisname

| Aufruf | Beschreibung |
|--------|-------------|
| `/embed-videos` | Alle unverarbeiteten Videos einbetten |
| `/embed-videos X11_vs_Wayland` | Nur Videos aus diesem Unterverzeichnis |

---

## Pre-Flight

| Voraussetzung | Pruefung | Schwere |
|---------------|---------|---------|
| MP4-Dateien vorhanden | `Glob: docs/assets/video/**/*.mp4` liefert Treffer | Blocker |
| `md_in_html` Extension | In `mkdocs.yml` unter `markdown_extensions` aktiv | Blocker |
| STATUS-Datei | `research/VIDEO_STATUS.md` existiert (sonst anlegen) | Auto-fix |

Bei Blocker: AskUserQuestion — Problem melden, Abbruch anbieten.

---

## Phase 1 — Scan

1. **Alle MP4s finden:**
```
Glob: docs/assets/video/**/*.mp4
```

2. **Argument-Filter anwenden:**
   - Wenn `$ARGUMENTS` gesetzt: Nur Videos deren Elternverzeichnis den Wert enthaelt
   - Wenn leer: Alle Videos

3. **STATUS-Datei laden:**
```
Read: research/VIDEO_STATUS.md
```

4. **Unverarbeitete identifizieren:**
   - Videos die noch nicht in der STATUS-Datei mit Status `eingebettet` stehen
   - Leere Verzeichnisse (ohne MP4) ignorieren

**Ergebnis:** Liste unverarbeiteter Videos mit Verzeichnis und Dateiname.

Falls keine unverarbeiteten Videos: Meldung ausgeben und Skill beenden.

---

## Phase 2 — Video-Seite

Zentrale Seite `docs/de/videos.md` und `docs/en/videos.md` anlegen oder aktualisieren.

### 2.1 Seiten anlegen (falls nicht vorhanden)

**DE (`docs/de/videos.md`):**
```markdown
---
title: Videos
---

# Videos

Videosammlung rund um X-Plane auf Linux.
```

**EN (`docs/en/videos.md`):**
```markdown
---
title: Videos
---

# Videos

Video collection for X-Plane on Linux.
```

### 2.2 Videos einbetten

Fuer jedes unverarbeitete Video einen Block an die Seite anfuegen (vor einem eventuellen `## Quellen`/`## Sources` Abschnitt, sonst am Ende):

**DE:**
```html

## {Video-Titel (aus Dateiname, Unterstriche durch Leerzeichen)}

<div class="video-container" markdown>
<video controls width="100%" preload="metadata">
  <source src="../assets/video/{dir}/{file}.mp4" type="video/mp4">
</video>
</div>
```

**EN:** Gleiche Struktur, Ueberschrift ggf. uebersetzt.

### 2.3 Poster-Erkennung

Falls im selben Verzeichnis eine Bilddatei mit gleichem Basisnamen existiert (`.jpg`, `.jpeg`, `.png`, `.webp`):
```
Glob: docs/assets/video/{dir}/{basename}.*
```
→ `poster`-Attribut ergaenzen:
```html
<video controls width="100%" preload="metadata" poster="../assets/video/{dir}/{basename}.jpg">
```

### 2.4 Navigation in mkdocs.yml

Pruefen ob `videos.md` bereits in der Navigation steht. Falls nicht:

**DE:** Unter "Uebersicht", nach "Erste Schritte":
```yaml
- Videos: de/videos.md
```

**EN:** Unter "Overview", nach "Getting Started":
```yaml
- Videos: en/videos.md
```

---

## Phase 3 — Thematische Einbettung + Featured-Video

Jedes Video wird zusaetzlich zur Video-Seite in die thematisch passende Dokumentationsseite eingebettet.

### 3.0 Featured-Video auf der Startseite

Die Startseite (`index.md`) zeigt immer genau EIN Video als Featured-Video (das neueste). Bei jedem Skill-Durchlauf:

1. Das neueste eingebettete Video identifizieren (= das gerade verarbeitete)
2. Den bestehenden `<video>`-Block im `## Video`-Abschnitt auf `index.md` (DE + EN) durch das neue Video **ersetzen** (nicht hinzufuegen)
3. Der "Alle Videos →" / "All Videos →" Link bleibt bestehen

Das ersetzte Video ist weiterhin auf `videos.md` und ggf. seiner thematischen Seite verfuegbar.

### 3.1 Verzeichnis-Zuordnung

Das Elternverzeichnis des Videos bestimmt die Zielseite(n):

| Verzeichnis enthaelt | Zielseite(n) |
|----------------------|-------------|
| `xol`, `Xplane_on_Linux` | `index.md` (nur thematisch) |
| `X11`, `Wayland`, `display` | `displayserver.md` |
| `tuning`, `system` | `systemtuning.md` |
| `nvidia` | `nvidia.md` |
| `config` | `xplane/config.md` |
| `liquorix` | `liquorix.md` |
| `scenery`, `szenerie` | `scenery.md` |
| `ortho` | `addon/orthophotography_intro.md` |
| `performance` | `xplane/performance.md` |

**Matching:** Case-insensitive Teilstring-Suche im Verzeichnisnamen.

**Fallback:** Wenn kein Muster passt → AskUserQuestion mit Verzeichnisname und Liste der verfuegbaren Seiten.

### 3.2 Pfadlogik

Der relative Pfad zum Video haengt von der Tiefe der Zielseite ab:

| Seite liegt in | Relativer Pfad |
|----------------|---------------|
| `docs/de/*.md` oder `docs/en/*.md` | `../assets/video/{dir}/{file}.mp4` |
| `docs/de/xplane/*.md` oder `docs/en/xplane/*.md` | `../../assets/video/{dir}/{file}.mp4` |
| `docs/de/addon/*.md` oder `docs/en/addon/*.md` | `../../assets/video/{dir}/{file}.mp4` |
| `docs/de/flight_operations/*.md` | `../../assets/video/{dir}/{file}.mp4` |

### 3.3 Einbettungsort

Das Video wird in der Zielseite platziert:
- **Bevorzugt:** Vor dem Abschnitt `## Quellen` (DE) bzw. `## Sources` (EN)
- **Fallback:** Am Ende der Seite

Das HTML-Fragment:

```html

## Video

<div class="video-container" markdown>
<video controls width="100%" preload="metadata">
  <source src="{relativer-pfad}" type="video/mp4">
</video>
</div>
```

Falls bereits ein `## Video`-Abschnitt existiert: Neues `<video>`-Tag unter den bestehenden anfuegen (kein doppelter Heading).

**Wichtig:** Immer beide Sprachversionen (DE + EN) der Zielseite bearbeiten.

---

## Phase 4 — Status aktualisieren

`research/VIDEO_STATUS.md` aktualisieren.

### Datei anlegen (falls nicht vorhanden):

```markdown
# Video Status

| Video | Verzeichnis | Zielseiten | Status | Datum |
|-------|-------------|------------|--------|-------|
```

### Zeile pro Video anfuegen:

```markdown
| {Dateiname} | {Verzeichnis} | {Liste der Zielseiten} | eingebettet | {YYYY-MM-DD} |
```

---

## Phase 5 — Qualitaetspruefung

| Pruefung | Wie |
|----------|-----|
| HTML-Tags korrekt | Jeder `<video>`-Block hat `controls`, `width="100%"`, `preload="metadata"`, korrekte `<source>` |
| Pfade korrekt | Relative Pfade stimmen mit der Verzeichnistiefe der jeweiligen Seite ueberein |
| Bilingual | Jede Einbettung existiert in DE und EN |
| Poster | Falls Bild vorhanden: `poster`-Attribut gesetzt |
| STATUS aktuell | Alle verarbeiteten Videos in `research/VIDEO_STATUS.md` |
| Build | `mkdocs build` ausfuehren — keine Fehler |

Bei Fehlern: Direkt korrigieren, dann Build wiederholen.

---

## Phase 6 — Zusammenfassung

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
EMBED VIDEOS: Zusammenfassung
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

VERARBEITET:
├─ Videos gesamt:    {N}
├─ Neu eingebettet:  {M}
└─ Bereits vorhanden: {N-M}

EINBETTUNGEN:
├─ videos.md (DE+EN): {Anzahl} Videos
├─ Thematische Seiten:
│   ├─ {seite1.md}: {video1.mp4}
│   ├─ {seite2.md}: {video2.mp4}
│   └─ ...
└─ Poster erkannt:   {Anzahl}

NAVIGATION:
├─ mkdocs.yml:  {Aktualisiert / Bereits vorhanden}
└─ Build:       {OK / Fehler}

STATUS:
└─ research/VIDEO_STATUS.md: {Aktualisiert}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## Phase 7 — Video-Verzeichnis oeffnen

```bash
open docs/assets/video/
```

---

## Hinweise

- **Kein Ueberschreiben:** Bereits eingebettete Videos (Status `eingebettet`) werden uebersprungen
- **Leere Verzeichnisse:** Werden ignoriert (z.B. `X11_vs_Wayland/` ohne MP4)
- **Dateiname als Titel:** Unterstriche werden durch Leerzeichen ersetzt, Extension entfernt
- **Keine Auto-Commits:** Der Skill erstellt keine Git-Commits. Nutze `/abschluss` dafuer
