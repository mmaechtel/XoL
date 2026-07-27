# Umsetzungsstand: Plugin-Faktencheck

**Datum:** 2026-07-27 (begonnen 2026-07-20)
**Branch:** `faktencheck-plugins-2026-07`
**Stand:** ABGESCHLOSSEN — 46 von 46 Seiten umgesetzt, Review-Zyklus durchlaufen, Working Tree sauber

---

## Ablauf und Endstand

1. **Umsetzung (46/46 Seiten).** Alle Findings aus `diff-data.json`, alle 17
   AUTO-Findings aus `auto-per-page.json` und alle Ja-Entscheidungen aus
   `umsetzen.json` sind umgesetzt; ein Commit pro Seite. Nein-Entscheidungen
   wurden nicht umgesetzt und sind in den jeweiligen Commits vermerkt.
   Seiten 23–46 wurden von Haiku-Subagenten umgesetzt (Betreiber-Vorgabe:
   guenstige Modelle), sequenziell in drei Gruppen.
2. **Opus-Review (alle 46 Paare).** Ergebnis: 9 kritische, 11 mittlere,
   9 Hinweis-Findings — u.a. drei vom Haiku-Durchgang erfundene Aussagen
   (XCamera Legacy-Build, KOSP "automatische Triebwerksauswahl",
   LiveTraffic Steam-Pfad) und zwei vergessene AUTO-Findings (AutoGate).
3. **Fix-Pass (18 Commits, `5bd1a9e`..`b24dfa9`).** Alle Findings behoben,
   gegen die Original-Corrections gegengeprueft. Einzige bewusste Ausnahme:
   `simbrief_simple_ofp.md` blieb unveraendert (war bereits korrekt;
   "last update" ist die belegte Formulierung).
4. **Opus-Nachpruefung.** Alle 28 Findings als behoben verifiziert,
   **EN fuer freigabereif erklaert.** Betreiber-Entscheidung: EN ist ab
   jetzt die Referenz (Truth), DE wird 1:1 daran ausgerichtet.
5. **DE-Ausrichtungspass (5 Commits, `908c07a`..`de0fb63`).** Alle 46 Paare
   geprueft, 5 DE-Seiten angeglichen (avitab, kabinxp, xroad, datareftool,
   skunkcrafts_updater); Binary-Genus in geaenderten Zeilen auf feminin
   vereinheitlicht. EN==DE-Zeilenzahl bei allen 46 Paaren.

Alle `mkdocs build`-Laeufe sauber (nur INFO). Stagnationshinweise
vereinheitlicht auf "— letztes Release <Monat Jahr>, seitdem unverändert".

## Bewusst offen gelassen

- **KabinXP Fat-Plugin-Hinweis:** zurueckgestellt (unbelegt), unveraendert.
- **XP Walkaround Z44:** Windows-Vorbehalt trotz Nein-Empfehlung
  aufgenommen — ausdrueckliche Betreiber-Vorgabe.
- **Commit-Sprachen gemischt** (24 englische Titel aus den Subagenten-Gruppen).
  Nur relevant, falls vor dem Merge gesquasht wird.
- Vorbestehende Altlasten ausserhalb des Branch-Diffs (z.B. "Kabinakustik"-Tippfehler
  in kosp_project.md, "Bausatz"/"Toolkit" in autogate.md, uebersetzter
  `spd-say`-String in xchecklist.md) — nicht Teil dieses Faktenchecks.

## Restschritte

- Changelog-Sammeleintrag 2026-07-27 in `docs/{de,en}/index.md` (mit diesem
  Stand committet).
- Merge nach `main` bzw. `/abschluss` — Entscheidung des Betreibers.

---

## Eingangsdaten

Rohdaten (Findings, Entscheidungen, AUTO-Liste, Format-README):
`research/addons/faktencheck-2026-07-20/`. Review-Seite der Freigabe:
`https://claude.ai/code/artifact/aa32a2fa-7ad1-476e-9b2f-93367c99232c`.
