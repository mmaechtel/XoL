# Research: Smoke & Steam for Chimneys & Coolingtowers (SimHeaven XP12)

**Recherche-Datum:** 2026-02-21
**Primärquelle:** https://forums.x-plane.org/files/file/94841-smoke-steam-for-chimneys-coolingtowers-for-simheaven-10-xp12/
**Ziel-Docs-Seite:** `docs/{lang}/scenery/autogen/smoke_steam_simheaven.md`

---

## 1. Fakten (gesichert)

### Produkt-Steckbrief

| Feld | Wert |
|------|------|
| **Name** | Smoke & Steam for Chimneys & Coolingtowers for SimHeaven 1.0 XP12 |
| **Autor** | Günther Kremp |
| **Partikeleffekte** | Helfried Miersch (Partikeldesign) |
| **X-World-Entwickler** | Armin „PilotBalu" (SimHeaven) |
| **Typ** | Szenerie-Erweiterung (Partikel-Bibliothek) |
| **Distribution** | [X-Plane.org Forums](https://forums.x-plane.org/files/file/94841-smoke-steam-for-chimneys-coolingtowers-for-simheaven-10-xp12/) (Freeware, nicht-kommerziell) |
| **Kompatibilität** | Nur X-Plane 12 |
| **Plattformen** | Windows, macOS, Linux (plattformunabhängige Szenerieordner) |
| **Abhängigkeit** | SimHeaven X-World muss installiert sein |
| **Lizenz** | Freeware, keine kommerzielle Nutzung |

### Was es tut

- Fügt realistische **Raucheffekte** an industriellen Schornsteinen hinzu
- Fügt **Dampfeffekte** an Kühltürmen hinzu
- Wirkt auf Objekte aus **SimHeaven X-World** weltweit (R2_Library wird **nicht** erwähnt)
- Kleinere Schornsteine und Kühltürme erhalten **bewusst keine Effekte** — Performance-Schutz für ältere Hardware
- Nutzt das native XP12-Partikelsystem

### Technische Grundlage

- **X-Plane 12 Partikelsystem:** Seit XP 11.30 verfügbar (PARTICLE_SYSTEM + EMITTER-Direktiven in OBJ8-Dateien, .pss Partikeldefinitionsdateien)
- **Schlüsseländerung XP 12.1.0:** Partikel können direkt in DSF-Objekten (Szenerie-Objekte) verwendet werden. Vorher war das Partikelsystem auf Flugzeuge und Plugin-Objekte beschränkt. Laminar Research entfernte gleichzeitig das alte „Smoke Puff"-System komplett.
- **Emitter vs. Effects:** Emitter laufen kontinuierlich (ideal für Schornsteine) — sie sind an Szenerie-Objekte gebunden und erzeugen fortlaufend Partikel. Effects sind zeitlich begrenzte Sequenzen (z.B. Explosionen).
- Die Partikeleffekte wurden von **Helfried Miersch** mit dem XP12-Partikelsystem erstellt und Günther Kremp zur Verfügung gestellt.
- **X-World** wurde von **Armin „PilotBalu"** (SimHeaven) entwickelt — er stellt die Szenerie-Objekte (Schornsteine, Kühltürme), an die die Partikel gebunden werden.

### Installation

1. ZIP-Datei in ein Verzeichnis **außerhalb** von X-Plane entpacken
2. Den Ordner `simHeaven_X-World_Particles_Library` nach `X-Plane 12/Custom Scenery/` kopieren
3. In `scenery_packs.ini` **oberhalb** von X-World registrieren
4. X-Plane starten — Effekte sind sofort aktiv

### Szeneriereihenfolge (scenery_packs.ini)

```
simHeaven_X-World_Particles_Library    ← ÜBER X-World
simHeaven_X-World_Europe_...           ← X-World Kontinentpakete
simHeaven_X-World_Vegetation_Library   ← Vegetationsbibliothek
```

### Kontext: Günther Kremp

- Community-Autor, bekannt für die **VFR Objects (GK)**-Serie für SimHeaven
- VFR Objects: ~40 regionale Pakete für deutsche Gebiete (Schwarzwald bis Ostseeküste)
- Nutzt Objekte aus der Sketchup 3D Gallery
- XP12- und XP11-Versionen verfügbar
- VFR Objects (GK) XP12 benötigt R2_Library und OpenSceneryX
- Wurde mit „Tipp der Redaktion" im FS Magazin (1/2020) ausgezeichnet

### Kontext: SimHeaven X-World Pro

- **Angekündigt:** Januar 2026 auf simheaven.com
- X-World Pro wird Rauch- und Dampfeffekte **nativ** enthalten
- Zusätzliche Partikeleffekte: Springbrunnen, Geysire, Wasserfontänen
- X-World Pro erweitert die kostenlose X-World-Basis um weitere Features (zeitgesteuerte Verkehrsdichte, lokalisierte Objekte, Agrarflächen)
- **Status:** In Entwicklung, kein Release-Datum bekannt

### Klarstellung: R2_Library

- R2_Library wird auf der Produktseite **nicht als Abhängigkeit erwähnt**
- Einzige Abhängigkeit ist SimHeaven X-World
- Frühere Recherche-Annahmen (R2_Library als Objektquelle) waren falsch — basierend auf Sekundärquellen, die das Addon mit Günther Kremps VFR Objects (GK) vermischten (die tatsächlich R2_Library benötigen)

---

## 2. Quellenübersicht

| Quelle | Typ | Inhalt | Bewertung |
|--------|-----|--------|-----------|
| [X-Plane.org Forums File #94841](https://forums.x-plane.org/files/file/94841-smoke-steam-for-chimneys-coolingtowers-for-simheaven-10-xp12/) | Primär | Download-Seite, Beschreibung, Installation | Hoch (Originalquelle, aber HTTP 403 bei WebFetch) |
| [SimHeaven X-World Pro](https://simheaven.com/x-world-pro/) | Primär | Ankündigung mit Rauch/Dampf-Feature | Hoch |
| [SimHeaven Homepage](https://simheaven.com/) | Primär | Screenshots smoke+steam1–4, Ankündigung | Hoch |
| [XP Developer: Particle System](https://developer.x-plane.com/article/x-plane-11-particle-system/) | Referenz | Technische Partikelsystem-Doku | Hoch |
| [XP Developer: 12.1.0 Notes](https://developer.x-plane.com/2024/02/a-few-notes-on-12-1-0-for-developers/) | Referenz | DSF-Partikelunterstützung bestätigt | Hoch |
| [XP 12.1.0 Release Notes](https://www.x-plane.com/kb/x-plane-12-1-0-release-notes/) | Referenz | Scenery particles randomized, neue Particle FX | Hoch |
| [VFR Objects (GK) XP12 — SimHeaven](https://simheaven.com/simdownloads/vfr-objects-gk-xp12/) | Sekundär | Autor-Kontext | Mittel |

---

## 3. Offene Fragen / Limitierungen der Recherche

1. **Exaktes Release-Datum** nicht bekannt. Version ist 1.0.

2. **Genaue Anzahl betroffener Objekte** (wie viele Schornsteine/Kühltürme erhalten Effekte) ist nicht dokumentiert — die Beschreibung sagt „weltweit", aber nur größere Objekte.

3. **Screenshots** der SimHeaven-Homepage zeigen smoke+steam-Effekte (Bilder smoke+steam1–4), aber es ist nicht eindeutig, ob diese zum Standalone-Addon oder zum kommenden X-World Pro gehören.

4. ~~R2_Library-Abhängigkeit~~ — **geklärt:** Wird nicht erwähnt, keine Abhängigkeit.

---

## 4. Bewertung für XoL-Dokumentation

### Relevanz: MITTEL-HOCH

- **Pro:** Freeware-Addon, das SimHeaven X-World visuell signifikant aufwertet. Passt perfekt in die Autogen-Sektion neben XPNetwork Europa. Plattformunabhängig, keine Plugin-Abhängigkeit, einfache Installation.
- **Pro:** Illustriert das XP12-Partikelsystem für Szenerie — technisch interessant als Referenz.
- **Pro:** Ergänzt die bestehende SimHeaven-Dokumentation (SimHeaven ist bereits im Glossar und in Querverweisen präsent).

### Bedenken

- **Contra:** Verhältnis zum kommenden X-World Pro unklar — wenn X-World Pro erscheint und diese Effekte nativ enthält, könnte das Standalone-Addon überflüssig werden.
- **Contra:** Kompaktes Addon mit wenig Konfigurationsmöglichkeiten — Seite wird kürzer als XPNetwork Europa.

### Empfehlung

Seite erstellen, **kompakt** halten (kürzer als XPNetwork Europa). Fokus auf:

- Was es tut (Rauch/Dampf für SimHeaven-Objekte)
- Technischer Hintergrund (XP12-Partikelsystem, Emitter in Szenerie-Objekten)
- Installation (Ordner + scenery_packs.ini-Reihenfolge)
- Performance-Hinweis (bewusst nur größere Objekte)

**Primärquelle verifiziert** (User hat Seiteninhalt bereitgestellt, 2026-02-21).
