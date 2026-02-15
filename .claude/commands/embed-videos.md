# Embed Videos

Bettet MP4-Videos aus `docs/assets/video/{de,en}/` als HTML5-`<video>`-Tags in die Dokumentation ein. Videos sind sprachgetrennt: `video/de/` → nur `docs/de/`, `video/en/` → nur `docs/en/`. Erstellt/aktualisiert eine zentrale Video-Seite und bettet Videos zusaetzlich in thematisch passende Seiten ein.

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
| ffmpeg installiert | `which ffmpeg` liefert Pfad | Blocker |
| STATUS-Datei | `research/VIDEO_STATUS.md` existiert (sonst anlegen) | Auto-fix |

Bei Blocker: AskUserQuestion — Problem melden, Abbruch anbieten.

---

## Phase 1 — Scan

1. **Alle MP4s finden:**
```
Glob: docs/assets/video/{de,en}/**/*.mp4
```

2. **Sprache erkennen:**
   - Pfad `docs/assets/video/de/...` → Sprache `de`
   - Pfad `docs/assets/video/en/...` → Sprache `en`
   - Videos ausserhalb von `de/` oder `en/` → Fehler melden

3. **Argument-Filter anwenden:**
   - Wenn `$ARGUMENTS` gesetzt: Nur Videos deren Pfad den Wert enthaelt
   - Wenn leer: Alle Videos

4. **STATUS-Datei laden:**
```
Read: research/VIDEO_STATUS.md
```

5. **Unverarbeitete identifizieren:**
   - Videos die noch nicht in der STATUS-Datei mit Status `eingebettet` stehen
   - Leere Verzeichnisse (ohne MP4) ignorieren

**Ergebnis:** Liste unverarbeiteter Videos mit Sprache, Verzeichnis und Dateiname.

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

**Sprachregel:** DE-Videos (`video/de/`) → nur `docs/de/videos.md`. EN-Videos (`video/en/`) → nur `docs/en/videos.md`.

Fuer jedes unverarbeitete Video einen Block an die passende Sprachversion anfuegen (vor einem eventuellen `## Quellen`/`## Sources` Abschnitt, sonst am Ende):

```html

<div class="video-card" markdown>

### {Video-Titel (aus Dateiname, Unterstriche durch Leerzeichen)}

<video controls width="100%" preload="metadata">
  <source src="../assets/video/{lang}/{subdir}/{file}.mp4" type="video/mp4">
</video>

</div>
```

Dabei ist `{lang}` = `de` oder `en`, `{subdir}` = Unterverzeichnis unter `de/` bzw. `en/` (entfaellt wenn Video direkt in `de/` oder `en/` liegt).

### 2.3 Poster-Bild erstellen oder erkennen

Fuer jedes unverarbeitete Video pruefen, ob bereits eine Bilddatei mit gleichem Basisnamen existiert (`.jpg`, `.jpeg`, `.png`, `.webp`):
```
Glob: docs/assets/video/{lang}/{subdir}/{basename}.*
```

**Falls kein Poster vorhanden:** Mit ffmpeg ein Poster-Bild aus dem Video generieren (Frame bei Sekunde 10):
```bash
ffmpeg -ss 10 -i "docs/assets/video/{lang}/{subdir}/{file}.mp4" -frames:v 1 -q:v 2 "docs/assets/video/{lang}/{subdir}/{basename}.jpg"
```

**In jedem Fall** das `poster`-Attribut in allen `<video>`-Tags setzen:
```html
<video controls width="100%" preload="metadata" poster="../assets/video/{lang}/{subdir}/{basename}.jpg">
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

Jede Sprach-Startseite zeigt genau EIN Video als Featured-Video (das neueste der jeweiligen Sprache). Bei jedem Skill-Durchlauf:

1. Das neueste eingebettete Video identifizieren (= das gerade verarbeitete)
2. **Sprachregel:** DE-Video → nur `docs/de/index.md`, EN-Video → nur `docs/en/index.md`
3. Den bestehenden `<video>`-Block im `## Featured Video`-Abschnitt auf der passenden `index.md` durch das neue Video **ersetzen** (nicht hinzufuegen)
4. Der "Alle Videos →" / "All Videos →" Link bleibt bestehen

Das ersetzte Video ist weiterhin auf `videos.md` und ggf. seiner thematischen Seite verfuegbar.

### 3.1 Verzeichnis-Zuordnung

Das Unterverzeichnis (unterhalb von `de/` bzw. `en/`) bestimmt die Zielseite(n). Bei Videos direkt in `de/` oder `en/` (ohne Unterverzeichnis) wird der Dateiname fuer das Matching verwendet.

| Verzeichnis/Dateiname enthaelt | Zielseite(n) |
|-------------------------------|-------------|
| `xol`, `Xplane_on_Linux` | `index.md` (nur thematisch) |
| `X11`, `Wayland`, `display` | `displayserver.md` |
| `tuning`, `system` | `systemtuning.md` |
| `nvidia` | `nvidia.md` |
| `config` | `xplane/config.md` |
| `liquorix` | `liquorix.md` |
| `scenery`, `szenerie`, `scenery_packs` | `scenery_components.md` |
| `ortho` | `addon/orthophotography_intro.md` |
| `performance` | `performance_overview.md` |
| `toliss`, `ecosystem` | `addon/toliss_ecosystem.md` |
| `atc`, `vatsim`, `flight_ops` | `flight_operations/overview.md` |
| `network`, `kvm` | `kvm.md` |
| `filesystem`, `nvme`, `storage` | `filesystem.md` |
| `wine`, `proton` | `wine.md` |
| `addon`, `plugin` | AskUserQuestion (zu viele moegliche Zielseiten unter `addon/`) |

**Matching:** Case-insensitive Teilstring-Suche im Unterverzeichnisnamen oder Dateinamen.

**Sprachregel:** DE-Video → nur `docs/de/{zielseite}`, EN-Video → nur `docs/en/{zielseite}`.

**Fallback:** Wenn kein Muster passt → AskUserQuestion mit Verzeichnisname und Liste der verfuegbaren Seiten.

### 3.2 Pfadlogik

Der relative Pfad zum Video haengt von der Tiefe der Zielseite ab. `{lang}` ist `de` oder `en`, `{subdir}` das optionale Unterverzeichnis:

| Seite liegt in | Relativer Pfad |
|----------------|---------------|
| `docs/{lang}/*.md` | `../assets/video/{lang}/{subdir}/{file}.mp4` |
| `docs/{lang}/xplane/*.md` | `../../assets/video/{lang}/{subdir}/{file}.mp4` |
| `docs/{lang}/addon/*.md` | `../../assets/video/{lang}/{subdir}/{file}.mp4` |
| `docs/{lang}/flight_operations/*.md` | `../../assets/video/{lang}/{subdir}/{file}.mp4` |

Falls das Video direkt in `video/{lang}/` liegt (kein Unterverzeichnis), entfaellt `{subdir}/`.

### 3.3 Einbettungsort

Das Video wird **oben auf der Zielseite** platziert — nach Titel und ggf. Einleitungstext (Admonitions, Intro-Absaetze), aber **vor dem ersten inhaltlichen Abschnitt** (## Ueberschrift). Das entspricht der etablierten Konvention auf allen bestehenden Seiten (scenery_components.md, intro.md, displayserver.md).

**NICHT** unten vor `## Quellen`/`## Sources` — dort geht das Video unter und wird selten gesehen.

Das HTML-Fragment (ohne eigene ## Ueberschrift, da es im Seitenkopf steht):

```html

<div class="video-container" markdown>
<video controls width="100%" preload="metadata">
  <source src="{relativer-pfad}" type="video/mp4">
</video>
</div>
```

Falls die Seite bereits ein `<video>`-Tag im Kopfbereich hat: Neues Video darunter anfuegen.

**Wichtig:** Nur die zur Video-Sprache passende Docs-Version bearbeiten. DE-Video → nur `docs/de/`, EN-Video → nur `docs/en/`.

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
| Pfade korrekt | Relative Pfade stimmen mit der Verzeichnistiefe der jeweiligen Seite ueberein, `{lang}/` Segment vorhanden |
| Sprachtrennung | DE-Videos nur in `docs/de/`, EN-Videos nur in `docs/en/` — keine Kreuz-Verlinkung |
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

VERLINKUNGEN (wohin und warum):
├─ {video1.mp4}
│   ├─ videos.md ({lang})        — zentrale Videosammlung
│   ├─ {zielseite.md} ({lang})   — thematisch: Verzeichnis "{subdir}" matched Regel "{muster}" → {zielseite}
│   └─ index.md ({lang}, featured) — neuestes Video dieser Sprache ersetzt bisheriges Featured
├─ {video2.mp4}
│   ├─ ...
│   └─ ...
└─ Zuordnungsregeln: siehe Phase 3.1 (Verzeichnis-Zuordnung)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## Phase 7 — Video-Verzeichnis oeffnen

```bash
xdg-open docs/assets/video/
```

---

## Hinweise

- **Videos liegen auf NFS-Share**, nicht im Git-Repo. `docs/assets/video` ist ein Symlink auf `/mnt/videos/XoL/video` (Linux). Das Share muss gemountet sein, bevor der Skill laeuft. Neue Videos werden direkt auf dem Share abgelegt (nicht ins Repo committed).
- **Kein Ueberschreiben:** Bereits eingebettete Videos (Status `eingebettet`) werden uebersprungen
- **Leere Verzeichnisse:** Werden ignoriert (z.B. `X11_vs_Wayland/` ohne MP4)
- **Dateiname als Titel:** Unterstriche werden durch Leerzeichen ersetzt, Extension entfernt
- **Keine Auto-Commits:** Der Skill erstellt keine Git-Commits. Nutze `/abschluss` dafuer
