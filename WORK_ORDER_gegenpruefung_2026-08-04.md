# Arbeitsanweisung — Gegenprüfung des Faktenchecks abschließen

Erstellt 2026-08-03. Direkt als Prompt verwendbar: diese Datei lesen und
abarbeiten.

## Ausgangslage

Repo `/home/maechtel/Work/Git/XoL` — MkDocs, „X-Plane 12 unter Linux",
bilingual DE/EN. Am 2026-08-03 wurden zwei Seiten überarbeitet und einem
Faktencheck durch fünf Agenten unterzogen. Rund 20 Korrekturen wurden eingebaut,
committet (`b8878b9`) und deployt — **aber ohne adversarische Gegenprüfung**.
Genau die fehlt noch, und sie hat in einer früheren Runde 18 von 84 Befunden
verworfen.

Parallel kamen drei weitere Ergänzungen dazu (`b2e0b0a`, `7f46939`), die
ihren eigenen Faktencheck bereits hinter sich haben, aber dieselbe
Gegenprüfung noch brauchen.

## Prüfgegenstand

| Seite | Umfang | Stand |
|---|---|---|
| `docs/{de,en}/scenery/orthophotography/ortho4xp.md` | 583 Zeilen | überarbeitet, 20 Korrekturen ungeprüft |
| `docs/{de,en}/scenery/ortho_streaming/xpme.md` | 151 Zeilen | neu angelegt |
| `docs/{de,en}/addon/traffic/xpais_marine_traffic.md` | 96 Zeilen | neu angelegt |
| `docs/{de,en}/addon/toliss/toliss_mods.md` | 86 Zeilen | um zwei Flügelmods erweitert |
| `docs/{de,en}/scenery/aufbau_quellen/scenery_sources.md` | 104 Zeilen | um X-World Pro erweitert |

Alle fünf Paare sind derzeit zeilengleich zwischen DE und EN.

## Belege im Repo

- `research/szenerie/fc1_parameter.md` — Parameter gegen Upstream
- `research/szenerie/fc2_orthoforge.md` — OrthoForge und xpconnect.me
- `research/szenerie/fc3_streaming.md` — Streaming-Kapitel
- `research/szenerie/fc4_lidar_altbestand.md` — LiDAR und Altbestand
- `research/szenerie/fc5_xpme.md` — XPME-Seite
- `research/szenerie/VERIFIED_FACTS.md` — am Quellcode verifizierte Defaults
- `research/addons/FAKTENCHECK_toliss_mods.md` — enthält 3 offene Punkte
- `research/addons/FAKTENCHECK_xpais_marine_traffic.md` — enthält 1 offenen Punkt

Lokale Ortho4XP-Installation zum Nachprüfen:
`/mnt/xplane_data/docker/Ortho4XP/` — byte-identisch mit shred86/master v1.40.13.

---

## Aufgabe 1 — Adversarische Gegenprüfung (wichtigster Teil)

Setz mehrere Agenten an, die **nicht bestätigen, sondern widerlegen** sollen:
je Korrektur die Gegenthese belegen oder daran scheitern. Im Zweifel gilt eine
Korrektur als nicht gesichert.

**Bereits selbst am Quellcode verifiziert — nur kurz bestätigen, keine Mühe
hineinstecken:**

- `default_website` heißt `Arc`, nicht `ES`
- `skip_downloads` umschließt `skip_converts` im Code, unterdrückt also beides
- `cover_extent` ist ein Rand um die Bounding-Box, kein Radius
- OrthoForge-Defaults identisch mit Ortho4XP, ausser `water_tech=XP12`
- `magick identify -verbose` gibt keine Mipmap-Anzahl aus
- `LOAD_CENTER` schreibt die Texturgröße fest als `4096`

**Das eigentliche Ziel — je ein einzelner Agent, ungeprüft:**

- `ratio_bathy` als Bathymetrie-Multiplikator statt Transparenz
- `masking_mode=3steps` mit der a/b/c-Bedeutung
- `road_level=3` bringt Residential/Unclassified, Secondary steckt schon in `1`
- `masking_mode=rocks` nur „abrupter", nicht „für alpine Ufer"
- `imprint_masks_to_dds` Default `True` bei oscarpilote
- `custom_overlay_src_alternate` und `max_download_slots` als fork-only
- `1302 flatten 1` als korrekte Schreibweise, Setzen als XP12-Fix
- sonny.4lima.de deckt nur Europa ab
- 0,5″-US-Kacheln tragen USGS-3DEP-, nicht Sonny-Zuschreibung
- `orthoforge-data.html` führt ausschließlich OSM
- XPME hat keine belegte Rückgabefrist
- AutoOrtho ist Apache-2.0, XEarthLayer MIT
- XPME-Startreihenfolge ohne die erschlossene Begründung zum Einhängepunkt
- Die `seq`-Bereiche im LiDAR-Bash-Skript (`-90 10 80` / `-180 10 170`)

**Dazu die drei parallelen Ergänzungen**, deren Faktenchecks noch nicht
gegengeprüft sind: die beiden ToLiss-Flügelmods (Durantula Wing Enhancement,
RealWings) samt der Aussage, dass beide als Alternativen zu behandeln sind;
XPAIS Marine Traffic einschließlich des archivierten Repositories und der
Notwendigkeit, X-Planes eigenen Schiffsverkehr abzuschalten; X-World Pro
einschließlich der Linux-Falle mit der Vegetationsbibliothek und dem von Hand
anzulegenden Symlink. Die vier offenen Punkte aus den beiden
`research/addons/FAKTENCHECK_*`-Berichten mit erledigen.

## Aufgabe 2 — Zwei ungeklärte Punkte

- **shred86-Wiki:** Zwei Agenten widersprechen sich beim letzten Stand — einmal
  Juni 2026, einmal Juni 2024. Auflösen.
- **Forum-Links:** Die Ortho4XP-Seite verlinkt zweimal
  `https://forums.x-plane.org/index.php?/forums/forum/310-ortho4xp/`. Ein Agent
  hielt die `index.php`-Form für veraltet. Beide Formen liefern 403 auf
  automatisierte Abrufe, die Frage ist offen. Notfalls per Browser klären, nicht
  per HTTP-Abruf.

## Aufgabe 3 — DE-Lektorat der neuen Passagen

Das deutsche Lektorat lief **vor** den 20 Korrekturen. Die neu übersetzten
Stellen hat niemand gegengelesen. Prüfen auf Übersetzungsqualität, Terminologie
gegen `docs/de/glossary.md`, durchgängiges `ß` statt `ss`, Anredekonvention
(unpersönlich, kein „Sie") und Strukturgleichheit zu EN.

Die drei parallelen Ergänzungen dabei mitnehmen.

---

## Regeln

- `docs/MARKDOWN_RULES.txt` und `CLAUDE.md` lesen und anwenden. **EN ist
  Leitfassung**, DE wird strukturgleich angeglichen.
- Jede Feststellung braucht URL oder Dateipfad plus wörtliches Zitat. Ohne Beleg
  gilt **UNBELEGBAR** — nichts plausibel ergänzen.
- Quellen ab 2024. Ausnahme: Quellcode und stabile Spezifikationen.
- `forums.x-plane.org` blockt automatisierte Abrufe (403). Nicht darauf stützen,
  keine Abrufversuche verschwenden.
- Nicht als Quelle: supergoodcode.com, dsogaming.com, hardwaretimes.com,
  questions.x-plane.com, steamcommunity.com, x-plane.to.
- **Geschützte Anker**, dürfen nicht umbenannt werden — drei Seiten verlinken sie:
  `#building-packages-for-ortho-streaming` / `#pakete-fur-ortho-streaming-bauen`,
  `#lidar-data-integration` / `#integration-von-lidar-daten`.
- Keine aktuellen Release-Versionsnummern auf Tool-Seiten. Harte
  Mindestanforderungen ausgenommen — Python 3.10 bei OrthoForge ist belegt und
  bleibt.
- Nur Linux-Spezifika. Plattformunabhängige X-Plane-Einstellungen gehören nicht
  in die Doku.
- `mkdocs build` braucht `/mnt/videos` gemountet, sonst bricht er am
  Video-Symlink ab, bevor er die Seiten erreicht.
- Deploy: `./update_emvisio.sh root@emvisio.de`, `--dry` für den Probelauf.
  Changelog in `docs/{lang}/index.md` **immer zuletzt**, maximal drei
  Datumsblöcke, DE und EN inhaltlich identisch.
- Server-Zugriff besteht: `ssh root@emvisio.de`. Apache, Ubuntu 24.04.
  Die emvisio-vhosts liegen in `/etc/apache2/sites-available/emvisio-ssl.conf`
  und `emvisio-de-le-ssl.conf`; andere Sites auf derselben Maschine nicht
  anfassen.

## Ergebnis

Die widerlegten und die bestätigten Korrekturen **getrennt vorlegen, bevor
etwas geändert wird**. Was widerlegt wird, wird zurückgenommen oder neu
formuliert.
