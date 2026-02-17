# Embed Videos

Bettet MP4-Videos aus `docs/assets/video/{de,en}/` in die Dokumentation ein. Sprachregel: `video/de/` → nur `docs/de/`, `video/en/` → nur `docs/en/`.

## Argumente

`$ARGUMENTS`: Optionaler Verzeichnisname (Filter)

| Aufruf | Beschreibung |
|--------|-------------|
| `/embed-videos` | Alle unverarbeiteten Videos einbetten |
| `/embed-videos X11_vs_Wayland` | Nur Videos aus diesem Unterverzeichnis |

---

## Phase 1 — Pre-Flight + Scan

### 1.1 Voraussetzungen pruefen

| Voraussetzung | Pruefung | Schwere |
|---------------|---------|---------|
| MP4-Dateien vorhanden | `Glob: docs/assets/video/**/*.mp4` | Blocker |
| `md_in_html` Extension | In `mkdocs.yml` unter `markdown_extensions` | Blocker |
| ffmpeg installiert | `which ffmpeg` | Blocker |
| STATUS-Datei | `research/VIDEO_STATUS.md` existiert (sonst anlegen) | Auto-fix |
| Navigation | `videos.md` in beiden Nav-Baeumen in `mkdocs.yml` | Auto-fix |

Bei Blocker: AskUserQuestion — Problem melden, Abbruch anbieten.

**Navigation Auto-fix** (falls `videos.md` fehlt):

- DE: Unter "Uebersicht", nach "Erste Schritte": `- Videos: de/videos.md`
- EN: Unter "Overview", nach "Getting Started": `- Videos: en/videos.md`

### 1.2 INBOX verarbeiten

```
Glob: docs/assets/video/{de,en}/INBOX/*.mp4
```

Fuer jede gefundene MP4-Datei:

1. Zielverzeichnis erstellen: `docs/assets/video/{lang}/{basisname}/` (Basisname = Dateiname ohne `.mp4`)
2. Datei verschieben: `mv INBOX/{datei}.mp4 {basisname}/{datei}.mp4`
3. Meldung ausgeben

Falls INBOX leer: **Fallback auf Downloads-Verzeichnis**.

**Fallback: Downloads-Verzeichnis**

```
Glob: ~/Downloads/*.mp4
```

Falls MP4-Dateien in `~/Downloads/` vorhanden:

1. Liste der gefundenen MP4-Dateien anzeigen
2. Per AskUserQuestion fragen: Welche Videos sollen uebernommen werden? (multiSelect)
3. Fuer jedes ausgewaehlte Video per AskUserQuestion die Sprache abfragen: DE oder EN?
4. Dateien in die passende INBOX verschieben: `mv ~/Downloads/{datei}.mp4 docs/assets/video/{lang}/INBOX/`
5. INBOX-Verzeichnis bei Bedarf anlegen: `mkdir -p docs/assets/video/{lang}/INBOX/`
6. Danach zurueck zum INBOX-Verarbeitungsschritt (Zielverzeichnis erstellen, verschieben)

Falls auch Downloads leer: Ueberspringen.

### 1.3 Scan + Namenskonvention

1. **Alle MP4s finden:**
```
Glob: docs/assets/video/{de,en}/**/*.mp4
```

2. **Sprache erkennen:** Pfad `video/de/` → `de`, Pfad `video/en/` → `en`

3. **Argument-Filter:** Wenn `$ARGUMENTS` gesetzt, nur matching Videos

4. **STATUS-Datei laden:** `research/VIDEO_STATUS.md` lesen, bereits eingebettete (Status `eingebettet`) ueberspringen

5. **Namenskonvention pruefen:** Fuer jedes Video: Verzeichnisname == Video-Basisname (ohne `.mp4`)?
   - Falls nicht: AskUserQuestion mit Umbenennungsvorschlag
   - Bei Zustimmung: Verzeichnis umbenennen, bestehende Pfade in `docs/` anpassen

**Ergebnis:** Liste unverarbeiteter Videos mit Sprache, Verzeichnis, Dateiname.

Falls leer: Meldung und Skill beenden.

---

## Phase 2 — Pro Video: Checkliste

Fuer **jedes** unverarbeitete Video die folgenden Schritte **in dieser Reihenfolge** abarbeiten:

### [ ] 2.1 Poster generieren

Pruefen ob Bild mit gleichem Basisnamen existiert (`.jpg`, `.jpeg`, `.png`, `.webp`):
```
Glob: docs/assets/video/{lang}/{subdir}/{basename}.*
```

Falls kein Poster: Generieren mit ffmpeg (Frame bei Sekunde 10):
```bash
ffmpeg -ss 10 -i "docs/assets/video/{lang}/{subdir}/{file}.mp4" -frames:v 1 -q:v 2 "docs/assets/video/{lang}/{subdir}/{basename}.jpg"
```

### [ ] 2.2 In `videos.md` einfuegen

Seite `docs/{lang}/videos.md` anlegen falls nicht vorhanden:

**DE:**
```markdown
---
title: Videos
---

# Videos

Videosammlung rund um X-Plane auf Linux.
```

**EN:**
```markdown
---
title: Videos
---

# Videos

Video collection for X-Plane on Linux.
```

Video-Block anfuegen (vor `## Quellen`/`## Sources`, sonst am Ende):

```html

<div class="video-card" markdown>

### {Titel (Dateiname, Unterstriche → Leerzeichen)}

<video controls width="100%" preload="metadata" poster="../assets/video/{lang}/{subdir}/{basename}.jpg">
  <source src="../assets/video/{lang}/{subdir}/{file}.mp4" type="video/mp4">
</video>

</div>
```

### [ ] 2.3 In thematische Seite einbetten

Zielseite ueber Zuordnungstabelle bestimmen (siehe unten). Dann Video-Block einfuegen — **oben auf der Seite** nach Titel/Einleitung, vor dem ersten `##`-Abschnitt. Falls bereits ein `<video>` im Kopfbereich: darunter anfuegen.

```html

<div class="video-container" markdown>
<video controls width="100%" preload="metadata" poster="{relativer-pfad-poster}">
  <source src="{relativer-pfad}" type="video/mp4">
</video>
</div>
```

Relativen Pfad ueber Pfadlogik-Tabelle bestimmen (siehe unten).

### [ ] 2.4 `VIDEO_STATUS.md` aktualisieren

Zeile anfuegen:
```markdown
| {Dateiname} | {Verzeichnis} | {Zielseiten} | eingebettet | {YYYY-MM-DD} |
```

---

## Phase 3 — Build + QS

| Pruefung | Wie |
|----------|-----|
| Build | `SKILL_RULES.md` → **Build pruefen** |
| Pfade korrekt | Relative Pfade stimmen mit Verzeichnistiefe ueberein |
| Sprachtrennung | DE-Videos nur in `docs/de/`, EN-Videos nur in `docs/en/` |
| Poster | `poster`-Attribut in allen `<video>`-Tags gesetzt |
| STATUS | Alle verarbeiteten Videos in `research/VIDEO_STATUS.md` |

Bei Fehlern: Direkt korrigieren, Build wiederholen.

### Featured-Video aktualisieren?

Nach erfolgreichem Build per AskUserQuestion fragen:

> "Soll das Featured-Video auf der Startseite aktualisiert werden?"
> - Option 1: "{neuestes Video}" als Featured setzen (mit Angabe welches Video)
> - Option 2: Nein, Featured-Video beibehalten

Bei Zustimmung: Den bestehenden `<video>`-Block im Featured-Abschnitt auf `docs/{lang}/index.md` durch das neue Video **ersetzen**. Sprachregel beachten (DE-Video → DE-index, EN-Video → EN-index).

---

## Phase 4 — Zusammenfassung

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
EMBED VIDEOS: Zusammenfassung
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

EINGEBETTET:
├─ {video1.mp4} ({lang})
│   ├─ videos.md
│   └─ {zielseite.md}
├─ {video2.mp4} ({lang})
│   ├─ videos.md
│   └─ {zielseite.md}
└─ ...

BUILD: {OK / Fehler}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### Video-Link-Check (optional)

Per AskUserQuestion fragen:

> "Sollen alle Video-Links in den Docs geprueft werden?"
> - Option 1: Ja, alle pruefen
> - Option 2: Nein, direkt zum Commit

Bei Zustimmung: Alle `<source src="...">` und `poster="..."` Attribute in `docs/{de,en}/` extrahieren. Fuer jeden Pfad pruefen, ob die referenzierte Datei tatsaechlich existiert (per `ls` auf dem aufgeloesten Pfad). Defekte Links auflisten und Korrektur anbieten.

---

## Referenz: Zuordnungstabelle

Das Unterverzeichnis (oder der Dateiname bei Videos ohne Unterverzeichnis) bestimmt die Zielseite. Case-insensitive Teilstring-Suche.

| Verzeichnis/Dateiname enthaelt | Zielseite(n) |
|-------------------------------|-------------|
| `xol`, `Xplane_on_Linux`, `X-Plane_unter`, `X-Plane_on` | `intro.md` |
| `X11`, `Wayland`, `display` | `displayserver.md` |
| `tuning`, `system`, `smoother`, `two_paths` | `systemtuning_intro.md` |
| `nvidia` | `nvidia.md` |
| `config` | `xplane/config.md` |
| `liquorix` | `liquorix.md` |
| `scenery`, `szenerie`, `scenery_packs`, `welt`, `richtig_gebaut`, `mastering` | `scenery_components.md` |
| `ortho`, `streaming` | `addon/orthophotography_intro.md` |
| `performance`, `puzzle`, `rätsel` | `performance_overview.md` |
| `toliss`, `ecosystem`, `briefing`, `gate`, `cockpit` | `addon/toliss_ecosystem.md` |
| `atc`, `vatsim`, `flight_ops` | `flight_operations/overview.md` |
| `network`, `kvm` | `kvm.md` |
| `filesystem`, `nvme`, `storage` | `filesystem.md` |
| `wine`, `proton` | `wine.md` |
| `addon`, `plugin` | AskUserQuestion (mehrere moegliche Zielseiten unter `addon/`) |

**Fallback:** Kein Muster passt → AskUserQuestion mit Verzeichnisname und Seitenliste.

## Referenz: Pfadlogik

Der relative Pfad zum Video haengt von der Verzeichnistiefe der Zielseite ab:

| Seite liegt in | Relativer Pfad |
|----------------|---------------|
| `docs/{lang}/*.md` | `../assets/video/{lang}/{subdir}/{file}.mp4` |
| `docs/{lang}/xplane/*.md` | `../../assets/video/{lang}/{subdir}/{file}.mp4` |
| `docs/{lang}/addon/*.md` | `../../assets/video/{lang}/{subdir}/{file}.mp4` |
| `docs/{lang}/flight_operations/*.md` | `../../assets/video/{lang}/{subdir}/{file}.mp4` |

Falls Video direkt in `video/{lang}/` liegt (kein Unterverzeichnis), entfaellt `{subdir}/`.

---

## Hinweise

- **Videos liegen auf NFS-Share**, nicht im Git-Repo. `docs/assets/video` ist ein Symlink. Share muss gemountet sein.
- **Namenskonvention:** Verzeichnisname = Video-Basisname (z.B. `Mein_Video/Mein_Video.mp4`)
- **Kein Ueberschreiben:** Bereits eingebettete Videos (Status `eingebettet`) werden uebersprungen
- **Dateiname als Titel:** Unterstriche → Leerzeichen, Extension entfernt
- **Keine Auto-Commits:** Nutze `/abschluss` fuer Git-Commits
- **Featured-Video:** Wird am Ende per Rueckfrage angeboten, nicht automatisch ersetzt
