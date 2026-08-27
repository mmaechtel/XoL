# Work Order — SEO-Ausbau der Dokumentation

**Stand:** 2026-08-27 · Branch `claude/seo-optimization-1rrhow`
**Basis:** Commit `b2bb19f` (JSON-LD @graph, Sitemap-x-default, site_name-Fix,
.htaccess-Auslieferung, 13 Descriptions gekürzt, /seo-check um Titel-Prüfung
erweitert). Dieser Work Order deckt die verbliebenen Punkte ab.

**Lesen vor jeder Phase:** `docs/MARKDOWN_RULES.txt`, `SKILL_RULES.md`,
`CLAUDE.md`. EN führt, DE zieht nach, Formatierung identisch.

---

## Entscheidungen (getroffen)

| Punkt | Entscheidung |
|---|---|
| Bot-Abwehr (`emvisio-botblock.conf`) | Prüft der Betreiber selbst — blockiert sie Googlebot/Bingbot, ist alles Weitere wirkungslos. Check: Search Console → Live-URL-Test |
| Verwaiste Blogposts (KCLE, KDEN, KLAX) | **Entfernen** (Phase 0) |
| `navigation.prune` | **Aktivieren** (Phase 0) — −46 % Seitengewicht (104→61 KB Median), Sidebar zeigt nur den aktiven Zweig |

## Arbeitsregeln für alle Phasen

- **Titel setzen = `title:`-Frontmatter**, niemals den H1 ändern. Der sichtbare
  Seitenkopf bleibt. Nav-Beschriftungen kommen aus `mkdocs.yml > nav`
  (Sektionslabels) und bleiben unberührt — nach jedem Batch im Build gegenprüfen.
- Titel-Budget: 30–40 Zeichen Kern; Suffix ` - XoL - X-Plane on Linux` (25 Z.)
  kommt dazu, Gesamt < 65. Kein „X-Plane on Linux" im Kern doppeln, wenn
  vermeidbar — das Suffix liefert es schon.
- Sektions-Intros: 100–180 Wörter echter Orientierungstext (was ist hier, für
  wen, in welcher Reihenfolge lesen) — kein Keyword-Teppich. Interne Links auf
  die wichtigsten Kindseiten.
- **Verifikation je Batch:** `mkdocs build`, dann: `<title>` < 65 Zeichen,
  Description 50–160, JSON-LD `json.loads`-valide, Nav-Labels unverändert,
  hreflang/canonical intakt.
- **Changelog** (`docs/{lang}/index.md`): nur die Content-Phasen (Intros,
  Blog-Entfernung nein). Ein komprimierter Eintrag am Ende, `index.md` zuletzt.
- Commit je Phase/Batch auf diesem Branch, Push nach Verifikation.

---

## Phase 0 — Technik: prune + Blog-Rückbau

**Status:** [ ] offen

1. `mkdocs.yml`: `navigation.expand` entfernen, `navigation.prune` ergänzen
   (beide zusammen sind laut Material-Doku inkompatibel; prune braucht den
   Wegfall von expand). Messwert Referenz: Median 104→61 KB, Summe 14,4→7,7 MB.
2. Blogposts entfernen: `docs/{en,de}/blog/{kcle-cleveland,kden-denver,klax-los-angeles}.md`
3. RSS-Rückbau: `docs/assets/rss/` (Feed + Template), `scripts/generate_rss.py`,
   RSS-Discovery-Link in `overrides/main.html`, RSS-Zeile in `CLAUDE.md`
4. `pub-blog`-Plugin aus `mkdocs.yml` nehmen, wenn der Build danach fehlerfrei
   ist; sonst drinlassen und notieren
5. Verifikation: Build ohne ERROR, Sitemap enthält keine `blog/`-URLs mehr,
   Seitengrößen wie gemessen

---

## Phasen 1–5 — Titel + Sektions-Intros, je Sektion ein Batch

Pro Batch: erst `title:`-Frontmatter (EN+DE), dann Intro-Ausbau der dünnen
Indexseiten (EN führt, DE zieht nach). Titel unten sind **Vorschläge** — beim
Abarbeiten gegen den Seiteninhalt prüfen und ggf. verwerfen („OK lassen" ist
ein gültiges Ergebnis, z. B. bei etablierten Eigennamen).

### Phase 1 — Grundlagen & Linux  **Status:** [ ] offen

| Datei | Titel-Vorschlag EN | Intro? (Ist-Wörter) |
|---|---|---|
| `fundamentals/index.md` | X-Plane Performance Fundamentals | ja (63) |
| `fundamentals/performance/index.md` | Performance: CPU, GPU, I/O Basics | nein |
| `linux/system/index.md` | Linux System Tuning for X-Plane | nein (109) |
| `linux/optimizations/index.md` | Linux Optimizations: Drivers & Kernel | nein |
| `linux/extensions/index.md` | Linux Utilities: KVM, Docker, Wine | ja (94) |

### Phase 2 — X-Plane & Szenerie  **Status:** [ ] offen

| Datei | Titel-Vorschlag EN | Intro? |
|---|---|---|
| `xplane/index.md` | X-Plane Setup & Diagnostics | nein (101) |
| `scenery/index.md` | X-Plane Scenery on Linux | nein |
| `scenery/aufbau_quellen/index.md` | Scenery Structure & Sources | ja (89) |
| `scenery/orthophotography/index.md` | Orthophotography for X-Plane | ja (86) |
| `scenery/ortho_streaming/index.md` | Ortho Streaming for X-Plane | nein |
| `scenery/autogen/index.md` | Autogen Scenery for X-Plane | ja (99) |

### Phase 3 — Addons I (Scripting, ToLiss, Sounds)  **Status:** [ ] offen

| Datei | Titel-Vorschlag EN | Intro? |
|---|---|---|
| `addon/index.md` | Linux-Compatible X-Plane Addons | nein |
| `addon/scripting/index.md` | X-Plane Scripting: Lua & Python | ja (62) |
| `addon/toliss/index.md` | ToLiss Ecosystem (OK lassen prüfen) | nein (114) |
| `addon/toliss/mods/index.md` | ToLiss Aircraft Mods | ja (96) |
| `addon/sounds/index.md` | X-Plane Sound Addons | ja (41) |
| `addon/toliss/mods/easy_freighter.md` | — (Titel OK) | ja, Content-Seite (74) |

### Phase 4 — Addons II (Cockpit, Tools, Traffic, Scenery-Plugins, KVM)  **Status:** [ ] offen

| Datei | Titel-Vorschlag EN | Intro? |
|---|---|---|
| `addon/cockpit/index.md` | Cockpit & Camera Addons | nein |
| `addon/tools/index.md` | X-Plane Utility Plugins | ja (90) |
| `addon/traffic/index.md` | Traffic & Ground Ops Addons | ja (98) |
| `addon/scenery_addons/index.md` | X-Plane Scenery Plugins | ja (88) |
| `addon/kvm/index.md` | Windows-only Addons via KVM | ja (54) |

### Phase 5 — Flight Ops & Meta-Seiten  **Status:** [ ] offen

| Datei | Titel-Vorschlag EN | Intro? |
|---|---|---|
| `flight_operations/atc/index.md` | ATC Procedures Gate to Gate | nein (101) |
| `flight_operations/vatsim/index.md` | VATSIM Online Flying | ja (48) |
| `flight_operations/weather/index.md` | Weather Briefing for X-Plane | ja (56) |
| `glossary.md` | X-Plane & Linux Glossary | nein |
| `about.md` | About XoL (OK lassen prüfen) | nein |
| `Maps.md` | Airport & Scenery Maps | nein |
| `videos.md` | Video Guides & Tutorials | ja (41) |

DE-Titel je Batch sinngleich bilden (gleiche Längenregel), nicht 1:1 übersetzen.

---

## Phase 6 — VideoObject-Markup  **Status:** [ ] offen

8 Videos je Sprache auf `videos.md`, derzeit ohne strukturierte Daten. Google
verlangt je Video mindestens `name`, `description`, `thumbnailUrl`, `uploadDate`.

1. `scripts/generate_video_meta.py` anlegen — läuft **lokal** (Share gemountet):
   liest `docs/assets/video/{de,en}/`, holt Dauer per `ffprobe`, Upload-Datum
   aus Datei-mtime, schreibt `scripts/video_meta.json` (wird committet)
2. Beschreibungen je Video (1–2 Sätze, EN+DE) in die JSON ergänzen — manuell
3. `overrides/main.html`: auf den Videos-Seiten `VideoObject`-Liste als JSON-LD
   aus der JSON injizieren (`contentUrl` = mp4, `thumbnailUrl` = Poster-jpg)
4. Verifikation: JSON-LD valide, Rich-Results-Test einer Videos-URL

**Abhängigkeit:** Schritt 1 braucht den gemounteten Share → lokaler Lauf durch
den Betreiber, Ergebnis-JSON committen. Container kann Schritt 3–4 danach.

---

## Phase 7 — llms.txt vervollständigen  **Status:** [ ] offen

Derzeit 19 von 137 Seiten gelistet. Statt Handpflege:

1. `scripts/generate_llms.py` — liest alle `docs/en/**/*.md`-Frontmatter
   (description) + Nav-Struktur, erzeugt `llms.txt` mit festem Kopfblock
   (Site, Sprachen, Lizenz, Quelle) und vollständiger Sektionsliste
2. In `CLAUDE.md` bei den Befehlen ergänzen; vor Deploy laufen lassen
3. Verifikation: alle Links stimmen gegen `site/` (Stichprobe + Zähler)

---

## Abschluss  **Status:** [ ] offen

- Changelog-Eintrag (DE+EN, ein Datumsblock, komprimiert): neue Sektions-Intros
  und Video-Auszeichnung — Titel-/Meta-Arbeit nicht einzeln aufführen
- `TODO.md`-Zeile auf „erledigt" setzen bzw. entfernen
- Finaler Build + Stichprobe (Titel, Descriptions, JSON-LD, Sitemap)
- Deploy durch Betreiber, danach: Search Console — Sitemap neu einreichen,
  Live-URL-Test (auch wegen Bot-Abwehr, Punkt Betreiber)

## Backlog (nicht Teil dieses Work Orders)

- `use_directory_urls: false` → saubere URLs ohne `.html` (Redirect-Konzept nötig)
- OG-Locale-Tags (`og:locale`, `og:locale:alternate`) im Social-Layout
- `easy_freighter.md` inhaltlich ausbauen (74 Wörter) — steht in Phase 3 nur
  als Intro-Fix; echter Ausbau via `/research-topic`
