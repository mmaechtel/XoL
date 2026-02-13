# CLAUDE.md — research

## Zweck

Wissensbasis für die XoL-Dokumentation (X-Plane on Linux).
Publizierte Referenz: `docs/en/*.md` (englische Seiten als Primärquelle, DE-Seiten sind Spiegel).

Recherchen zu: X-Plane-Konfiguration, Display-Server, Systemtuning, Monitoring-Tools, Audio, Szenerie, Addons.

## Index

`INDEX.md` mappt Research-Dateien auf Docs-Seiten (mit Relevanz HOCH/MITTEL/KEINE).
`/research` soll den Index nutzen, um nur relevante Dateien zu lesen.

### INDEX.md Format

```markdown
## <kategorie>

Docs: `docs/en/<seite>.md`

### HOCH
- <subdir>/<datei>.md -> <ziel-seite>.md[, <ziel-seite>.md]

### MITTEL
- <subdir>/<datei>.md -> <ziel-seite>.md

### KEINE
- <subdir>/<datei>.md

### LÜCKEN
- <thema> (<relevanz>) -> <vorgeschlagene-ziel-seite>.md (Quelle: <research-datei>.md)
```

- Pro Zielseite (oder Seitengruppe) ein `##`-Abschnitt
- Vier Sektionen: `### HOCH`, `### MITTEL`, `### KEINE`, `### LÜCKEN` (optional)
- Format pro Eintrag: `<pfad-relativ-zu-research/> -> <ziel-docs-datei(en)>`
- Bei KEINE: kein `->` Mapping (Datei ist für dieses Slide-Set irrelevant)
- Mehrere Ziel-Seiten mit Komma trennen

## Struktur

```
research/
├── xplane-config/          # X-Plane Konfiguration, Grafikeinstellungen, Performance
├── display-server/         # Wayland, X11, XWayland, Display-Server-Wahl
├── systemtools/            # Linux-Monitoring-Tools (CPU, I/O, Interrupts)
├── systemtuning/           # Kernel-Tuning, Latenzreduktion, CPU-Governor
├── audio/                  # PipeWire, PulseAudio, FMOD, Controller
├── szenerie/               # Ortho-Systeme, Cache-Verhalten, scenery_packs.ini
├── addons/                 # Wine-basierte Addons, XOrganizer
├── notebooklm/             # TTS-optimierte Skripte für NotebookLM Audio Overview
├── analyses/               # Persistierte Skill-Ergebnisse (/research, /audit, /faktencheck)
├── AUDIT_FLOW.md           # Content-Audit Prozess (Flow, Template, Regeln)
├── AUDIT_STATUS.md         # Audit-Fortschritt + Zyklushistorie
├── VIDEO_STATUS.md         # Tracker: welches Video wo eingebettet ist
├── INDEX.md                # Relevanz-Mapping: Research -> Docs-Seiten
├── README.md               # Content-Inventory mit Kurzbeschreibungen
└── trusted-sources.md      # Priorisierte Domain-Whitelist für WebFetch
```

## Trusted Sources

`trusted-sources.md` definiert vertrauenswürdige Domains für WebFetch. Skills dürfen NUR URLs von gelisteten Domains aktiv lesen. Suchergebnis-Snippets (WebSearch) sind davon nicht betroffen.

Die Liste kann jederzeit um weitere Domains ergänzt werden.

## Regeln

- Sprache: Deutsch (Research-Dokumente und Lektorate)
- Quellen immer dokumentieren (Autor, Jahr, URL)
- **Quellenaktualität: nur Quellen ab 2024 aufwärts verwenden** (ältere Quellen nur, wenn keine aktuellere Alternative existiert und die Information nachweislich stabil ist)
- Fokus: X-Plane 12, Linux (Debian Stable/Testing als Referenzplattform)
- Keine Duplikation von Inhalten aus `docs/`
- **WebFetch nur für Trusted Sources** (siehe `trusted-sources.md`)
- Versionsnummern minimieren (Entscheidungsbaum in `AUDIT_FLOW.md`)
- Lektorat-/Faktencheck-Dateien mit Präfix `LEKTORAT_` bzw. `FAKTENCHECK_`
- Audit-Ergebnisse mit Präfix `AUDIT_`
