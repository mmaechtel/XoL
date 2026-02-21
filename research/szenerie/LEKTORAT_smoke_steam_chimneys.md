# Lektorat: Smoke & Steam for Chimneys & Coolingtowers

**Datum:** 2026-02-21
**Grundlage:** `research/szenerie/smoke_steam_chimneys.md`
**Zielseite:** `docs/{lang}/scenery/autogen/smoke_steam_simheaven.md`
**Vorlage:** `docs/en/scenery/autogen/xpnetwork_europa.md`

---

## 1. Informationsbewertung

| Information | Relevanz | Haltbarkeit | Quelle | Aufnehmen? |
|---|---|---|---|---|
| Produktname, Autor, Lizenz | Hoch | Stabil | X-Plane.org Forums | Ja |
| Partikeleffekte von Helfried Miersch | Mittel | Stabil | WebSearch-Ergebnisse | Ja, im Background |
| XP12-Partikelsystem (EMITTER/PSS) | Mittel | Stabil (API) | Developer Docs | Ja, als technischer Kontext |
| DSF-Partikel seit XP 12.1.0 | Hoch | Stabil (Feature) | Developer Blog | Ja, erklärt warum nur XP12 |
| Installation (3 Schritte) | Hoch | Stabil | WebSearch + Forum | Ja |
| scenery_packs.ini-Reihenfolge | Hoch | Stabil | Üblich für SimHeaven | Ja |
| SimHeaven X-World als Abhängigkeit | Hoch | Stabil | Bestätigt | Ja |
| R2_Library | Irrelevant | — | Nicht erwähnt auf Produktseite | Nein — keine Abhängigkeit |
| Nur größere Objekte erhalten Effekte | Hoch | Stabil | Produktseite (Originaltext) | Ja — Performance-Hinweis |
| X-World-Entwickler: Armin „PilotBalu" | Mittel | Stabil | Produktseite (Credits) | Ja, im Background |
| VFR Objects (GK) Autor-Kontext | Niedrig | Stabil | SimHeaven | Nein — zu weit weg vom Thema |
| X-World Pro Ankündigung | Niedrig | Instabil (Zukunft) | SimHeaven | Nein — spekulativ |
| Performance-Angabe "keeping performance high" | Niedrig | Marketing | Beschreibung | Nein — nicht belastbar |

---

## 2. Versionsspezifische Inhalte

| Inhalt | Entscheidung | Begründung |
|---|---|---|
| „XP 12.1.0 für DSF-Partikel" | Meta-Formulierung | „X-Plane 12 with particle system support for scenery objects" — keine Versionsnummer nötig |
| „Version 1.0" im Produktnamen | Im Titel akzeptabel | Teil des offiziellen Namens |

---

## 3. Seitenstruktur (Plan)

Kompakte Seite nach XPNetwork-Europa-Vorlage, aber kürzer (das Addon ist deutlich einfacher).

```
# Smoke & Steam for SimHeaven

Einleitungssatz (was es tut, für welchen Simulator)

## Background / Hintergrund
- Bullet-Liste (Typ, Autor, Distribution, Plattformen, Kompatibilität)
- Fließtext: Technischer Kontext (XP12-Partikelsystem, Emitter in Szenerie-Objekten)

## Features / Funktionsumfang
- Raucheffekte an Schornsteinen
- Dampfeffekte an Kühltürmen
- Weltweite Abdeckung (überall wo SimHeaven X-World Objekte stehen)
- Emitter-basiert (kontinuierlich, performant)

## Value in Flight Simulation / Mehrwert in der Flugsimulation
- VFR-Immersion: Rauch und Dampf als visuelle Orientierungspunkte
- Standard-X-Plane hat keine Rauch/Dampf-Effekte an Szenerie-Objekten
- Linux: Keine Plugin-Abhängigkeit, reines Szenerie-Addon

## Installation
- Download-Link
- 3 Schritte (entpacken, kopieren, scenery_packs.ini)
- scenery_packs.ini-Reihenfolge als Code-Block

## Further Reading / Weiterführende Kapitel
- Scenery Components (scenery_packs.ini)
- Scenery Sources (Anbieterübersicht)

## Sources / Quellen
- X-Plane.org Forums Download
- SimHeaven Homepage
- X-Plane Developer: Particle System
```

---

## 4. Querverweise

| Aktion | Datei | Art |
|---|---|---|
| Neue Seite verlinken | `docs/{lang}/scenery/autogen/index.md` | Eintrag in Autogen-Index |
| SimHeaven-Glossar prüfen | `docs/{lang}/glossary.md` | Bestehender Eintrag ausreichend |
| mkdocs.yml Nav | `mkdocs.yml` | Beide Sprachbäume |
| Scenery Sources erwähnen | `docs/{lang}/scenery/aufbau_quellen/scenery_sources.md` | Optional: SimHeaven-Absatz ergänzen |

---

## 5. Status

1. ~~Primärquelle nicht verifiziert~~ — **Erledigt:** User hat Seiteninhalt am 2026-02-21 bereitgestellt.

2. ~~R2_Library-Abhängigkeit unklar~~ — **Geklärt:** R2_Library wird auf der Produktseite nicht erwähnt. Keine Abhängigkeit.

3. **X-World Pro Zukunft:** Nicht in der Doku erwähnen — spekulativ, kein Release-Datum, könnte das Standalone-Addon obsolet machen.
