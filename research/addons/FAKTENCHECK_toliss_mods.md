# Faktencheck: ToLiss Mods (EN + DE)

**Datum:** 2026-08-03
**Geprüfte Seiten:** `docs/en/addon/toliss/toliss_mods.md`, `docs/de/addon/toliss/toliss_mods.md`
**Anlass:** Neuer Abschnitt „Durantula Wing Enhancement MOD" ergänzt, bestehende Abschnitte mitgeprüft
**Primärquellen verifiziert:** github.com/iy4vet, raw.githubusercontent.com, forums.x-plane.org (nur indirekt, siehe Quellenlage)

---

## Quellenlage

`forums.x-plane.org` liefert auf **WebFetch** durchgängig HTTP 403, `web.archive.org` ist
ebenfalls blockiert. **Über die Chrome-Automatisierung sind die Forum-Seiten dagegen direkt
lesbar** — das ist der Weg für alle künftigen x-plane.org-Prüfungen. Der erste Durchgang
(Durantula) lief noch ohne Chrome und stützte sich auf die vom Nutzer bereitgestellten
Listings; im zweiten Durchgang wurden die betroffenen Seiten direkt gegengelesen und
bestätigt (siehe „Nachverifikation").

---

## Fehler (1) — korrigiert

### 1. Falscher Autor des Carda-Installers

**Datei:** `toliss_mods.md` (Carda-Abschnitt)
**Behauptung:** „The **Carda Engine Installer** by Todaloo automates the `.acf` patching step."
— zugleich als „Installer-Entwickler: iy4vet" gelistet und auf Datei 99205 verlinkt.
**Befund:** Es gibt zwei verschiedene Installer:

| Datei | Titel | Autor |
|-------|-------|-------|
| 94704 | Carda Engine Installer for Toliss A320 Family | Todaloo |
| 99205 | Carda Engine Mod Installer for ToLiss A319 / A320 / A321 | iy4vet |

Der verlinkte Installer (99205) sowie die im Linux-Hinweis genannten Dateinamen
(`install-carda-linux-x64`, `install_carda.py`) gehören zu iy4vet — GitHub-Repo
`xplane-toliss-carda-installer`, GPLv3, Python. Die Seite hat beide Projekte vermischt.
**Korrektur:** Name auf „Carda Engine Mod Installer" von iy4vet geändert, Todaloos älterer
Installer als separates Projekt erwähnt.

---

## Korrekt (Durantula-Abschnitt) — belegte Behauptungen

| # | Behauptung | Quelle |
|---|------------|--------|
| 1 | Mod besteht aus zwei unabhängigen Teilen (Flaps, Wingflex) | Installer-README: „The mod provides two optional components" |
| 2 | Flaps-Teil entfernt Original-Klappen-/Fairing-Geometrie aus den Flügel-OBJs und liefert neue Meshes plus Texturen | Installer-README + Listing (`flaps.png` / `flaps_NML.png` nach `objects/`) |
| 3 | Bei CEO-Triebwerken wird überlappende Triebwerks-„Kit"-Geometrie aus den Carda-OBJs bzw. der Original-`engines.obj` entfernt | Installer-Listing, Abschnitt „Flaps" |
| 4 | Wingflex ersetzt die ToLiss-eigenen Winglet-Animationen durch natives `wing_tip_deflection_deg` und setzt Flügel-Dämpfung in der `.acf` | Installer-README: „Replaces older animation systems with X-Plane's native wing deflection animations and configures wing damping properties" |
| 5 | Paintkit „New Wing Textures" ist nicht automatisiert, Livery manuell nach `liveries/` | Installer-Listing |
| 6 | Manuelle Installation erfordert Texteditor + Plane Maker | Installer-README: „modifications that would otherwise require manual editing in Notepad++ and Plane Maker" |
| 7 | Installer matcht auf Geometrie-/Animationsinhalt statt Zeilennummern, mehrfach ausführbar | Installer-Listing |
| 8 | Backups als `*.durantula.bak` | Installer-README + Listing |
| 9 | Native Binaries für Linux x64 und ARM64 | Installer-Listing (Plattform-Tabelle) |
| 10 | `install_durantula.py` mit Python 3.10+, keine externen Abhängigkeiten | Installer-README: „Python 3.10+ required", „No external dependencies" |
| 11 | Nicht-interaktiv über `--aircraft`, `--parts`, `--flaps-engine`, `--textures` | Installer-Listing (Flag-Tabelle) |
| 12 | Nach ToLiss-Update via SkunkCraftsUpdater erneut ausführen | Installer-README + Listing |
| 13 | Installer GPL-3.0 | github.com/iy4vet — Repo `xplane-toliss-durantula-installer`, Python, GPLv3 |
| 14 | Mod von Durantula2405, Modellierung/Animation Giorgi_Z4 | Forum-Listing 88518 |

---

## Nicht übernommen

- **Versionsnummern** (Mod 2.2.3, Installer 1.1r1, Mod-Ordner `..._V1.2` / `..._V1.3`) — gemäß
  Plugin-Versionskonvention weggelassen, da rein illustrativ. `Python 3.10+` bleibt als harte
  Mindestanforderung.
- **Dateigröße (~294 MB)** — volatil, kein Nutzwert.
- **Literale Animations-Bezeichnung `anim/winglex`** aus dem Installer-Listing — offenkundiger
  Tippfehler der Quelle (winglet flex); stattdessen umschrieben, um keinen falschen Bezeichner
  zu dokumentieren.

---

## Nachverifikation per Chrome (2026-08-03)

Alle zuvor offenen Punkte über die Chrome-Automatisierung direkt am Forum geklärt:

| Punkt | Ergebnis |
|-------|----------|
| Mod 88518 | Bestätigt: „Toliss A319, A320 and A321 — Wing Enhancement MOD", 294,43 MB, eingestellt 2023-10-25, zuletzt aktualisiert 2026-06-25, 13.766 Downloads |
| Carda-Installer 99205 | Autor **iy4vet** bestätigt (Titelzeile „By iy4vet"), zuletzt aktualisiert 2026-04-06. Trotz Forum-Kategorie „Payware Utilities" ein normaler kostenloser Download („Download this file", kein Preis, keine Kaufschranke) — die Kategorie ist irreführend, der Punkt ist erledigt |
| Durantula-Installer | Stabile Forum-Datei-URL weiterhin nicht ermittelbar; verlinkt bleibt das GitHub-Repo als Quelle der Binaries |

---

## Faktencheck RealWings (2026-08-03)

**Geprüfte Quellen:** Forum-Dateien 99042 / 99352 / 99442 (per Chrome direkt gelesen),
`github.com/iy4vet/xplane-toliss-realwings-installer` (README + `install_realwings.py`)

### Aktualität — aktiv gepflegt

| Download | Version | Eingestellt | Zuletzt aktualisiert |
|----------|---------|-------------|----------------------|
| RealWings319 | 1.1.1 | — | 2026 |
| RealWings320 | 1.1.1 | 2026-03-31 | 2026-05-20 („Added CEO version") |
| RealWings321 | 1.1.0 | 2026-04-05 | 2026-05-17 (Texturtiefe, Wingflex-Schattenlinien) |

Alle drei innerhalb der letzten drei Monate aktualisiert, der Installer ebenfalls. Der Mod ist
aktuell; keine Stale-Kennzeichnung nötig.

### Belegte Behauptungen

| # | Behauptung | Quelle |
|---|------------|--------|
| 1 | Neu modellierte Flügel, neue 4K-Texturen, Substance-3D-Painter-Paintkit, neue Fensterrahmen | Forum-Beschreibung, wortgleich auf allen drei Dateien |
| 2 | Kompatibel mit Cardas CFM/IAE-Triebwerken | Forum-Beschreibung: „Fully compatible with Carda's CFM/IAE engines" |
| 3 | Rein visuell, keine Originaldateien von ToLiss, kein Eingriff in den Systemcode | Forum-Beschreibung, Disclaimer |
| 4 | Nur X-Plane 12 | Forum-Beschreibung: „Currently only for X-Plane 12" |
| 5 | Von GeoBuilds gemeinsam mit Durantula2405 | Forum-Beschreibung: „made 100% by myself and @Durantula2405" |
| 6 | Varianten je Muster: A319 nur CEO; A320/A321 je NEO, CEO-Sharklets, CEO-Wingtips | Installer-README, Abschnitt „Supported Aircraft & Variants" |
| 7 | Nur eine Variante gleichzeitig aktiv, erneuter Lauf wechselt | Installer-README: „Only one variant remains active at a time; re-running switches between them" |
| 8 | Installer ersetzt Flügel-OBJs an korrekter Position, entfernt obsolete Geometrie, korrigiert Triebwerkskoordinaten bei erkanntem Carda-Mod | Installer-README |
| 9 | Verschachtelte `CEO/`- / `NEO/`-Ordner werden automatisch zusammengeführt (A320/A321) | Installer-README |
| 10 | Linux-Binaries `install-realwings-linux-x64` / `-arm64`, `install_realwings.py` mit Python 3.10+ ohne Abhängigkeiten | Installer-README |
| 11 | Flags `--aircraft`, `--variant`, `--frames`, `--aircraft-dir` | Installer-README |
| 12 | GPL-3.0 | GitHub-Repo-Metadaten + README |

### Bewusst zurückhaltend formuliert

- **Verhältnis RealWings ↔ Durantula:** Beide bearbeiten dieselben Flügel-OBJs (RealWings
  ersetzt, Durantula editiert). **Keine** der beiden Projektdokumentationen sagt etwas zur
  Kombination — weder Freigabe noch Ausschluss. Der Warnhinweis auf der Seite behauptet
  deshalb keine Inkompatibilität, sondern nennt die Überschneidung und empfiehlt, die beiden
  als Alternativen zu behandeln. Sollte sich später ein belastbarer Beleg finden, präzisieren.
- **Backup-Suffix:** Der Durantula-Installer schreibt `*.durantula.bak` und begründet das
  ausdrücklich mit Kollisionsfreiheit gegenüber SkunkCrafts. Der RealWings-Installer nutzt
  laut Quellcode (`def _backup(filepath: Path, suffix: str = ".bak")`) das generische `.bak`.
  Auf der Seite nicht erwähnt — für Leser ohne Nutzwert, für spätere Prüfungen hier notiert.
- **Dateigrößen und Versionsnummern** (RealWings321 358,21 MB, Versionen 1.1.x) nicht
  übernommen — volatil bzw. gemäß Plugin-Versionskonvention.

---

## Korrekturen aus der Gegenprüfung (2026-08-04)

Vollständiger Bericht: `research/GEGENPRUEFUNG_2026-08-04.md`.

- **Fünf Belegstellen sind keine wörtlichen Zitate.** „The mod provides two optional components",
  „Replaces older animation systems with X-Plane's native wing deflection animations and configures
  wing damping properties", „Python 3.10+ required", der Abschnittsname „Supported Aircraft &
  Variants" und „Only one variant remains active at a time; re-running switches between them"
  stehen so nicht in den aktuellen READMEs. Inhaltlich hält jeder Punkt, die Belegspalte ist aber
  nicht zitierfähig.
- **`anim/winglex` ist kein Tippfehler der Quelle.** Es ist der echte ToLiss-Bezeichner; der
  Installer matcht auf die literale Zeichenkette (`install_durantula.py:316`, Abschnittskopf
  „Wingflex: the 'anim/winglex' → 'wing_tip_deflection_deg' replacement"). Die frühere Einordnung
  unter „Nicht übernommen" ist damit hinfällig.
- **Durantula liefert keine neue Flügelgeometrie**, sondern Klappen und Klappenträger plus die
  Wingflex-Umstellung. Auf der Seite korrigiert.
- **RealWings folgt nicht derselben Architektur** wie der Durantula-Installer: Es löscht die
  Carda-„kit"-TRIS und die A319-`engines.obj`-Zeilen über fest codierte Zeilennummern
  (`_CARDA_TRIS_TARGETS`), obwohl sein Changelog „no hard-coded line numbers" behauptet. Daraus
  folgt der konkrete Konflikt mit einem vorher installierten Durantula-Mod.
- **Giorgi_Z4 bestätigt** (Forum-Datei 88518, wörtlich: „Many thanks to @Giorgi_Z4 for modeling and
  animating!"), ebenso alle RealWings-Beschreibungsmerkmale (Forum-Datei 99352).
- **Nicht dokumentiert war** der manuelle Schritt, den Ordner `objects/RealWings3XX/` einer Livery
  in den passenden Livery-Ordner zu kopieren; ergänzt.
