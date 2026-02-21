---
description: "Smoke & Steam for SimHeaven ergänzt SimHeaven X-World um partikelbasierte Rauch- und Dampfeffekte an industriellen Schornsteinen und Kühltürmen."
---
# Smoke & Steam for SimHeaven

Smoke & Steam for SimHeaven ist eine Szenerie-Erweiterung für [X-Plane](../../glossary.md#x-plane), die partikelbasierte Rauch- und Dampfeffekte an industriellen Schornsteinen und Kühltürmen aus [SimHeaven X-World](../../glossary.md#simheaven-x-world) hinzufügt. Die Effekte decken X-World-Objekte weltweit ab und nutzen das native Partikelsystem von X-Plane 12.

## Hintergrund

- **Typ:** Szenerie-Erweiterung (Partikel-Bibliothek, keine Plugin-Abhängigkeit)
- **Autor:** Günther Kremp (Partikeleffekte von Helfried Miersch)
- **Distribution:** [X-Plane.org Forums](https://forums.x-plane.org/files/file/94841-smoke-steam-for-chimneys-coolingtowers-for-simheaven-10-xp12/) (Freeware, nur nicht-kommerzielle Nutzung)
- **Plattformen:** Windows, macOS, Linux (Standard-Szenerieordner, plattformunabhängig)
- **Kompatibilität:** Nur X-Plane 12
- **Abhängigkeit:** [SimHeaven X-World](../../glossary.md#simheaven-x-world) muss installiert sein

Die Erweiterung installiert sich als eigenständige Partikel-Bibliothek (`simHeaven_X-World_Particles_Library`), die auf bestehende Schornstein- und Kühlturm-Objekte aus X-World verweist. X-World selbst wird von Armin „PilotBalu" (SimHeaven) entwickelt und ist als Freeware auf [simheaven.com](https://simheaven.com) verfügbar.

??? abstract "Technischer Hintergrund: Partikelsystem in X-Plane 12"

    X-Plane 12 unterstützt Partikel-Emitter in Szenerie-Objekten (DSF). Jede OBJ-Datei kann über die `PARTICLE_SYSTEM`-Direktive eine `.pss`-Partikelsystem-Definition referenzieren und `EMITTER`-Quellen an bestimmten Positionen platzieren. Emitter laufen kontinuierlich — ideal für dauerhafte Effekte wie Schornsteinrauch — während *Effects* zeitlich begrenzte Sequenzen sind (z. B. Explosionen). Das Partikelerscheinungsbild (Textur, Opazität, Skalierung, Lebensdauer) wird pro Partikeltyp in der `.pss`-Datei definiert.

## Funktionsumfang

- **Rauch** an industriellen Schornsteinen aus SimHeaven X-World
- **Dampf** an Kühltürmen aus SimHeaven X-World
- Weltweite Abdeckung — Effekte erscheinen überall, wo X-World passende Objekte platziert
- Kleinere Schornsteine und Kühltürme sind bewusst ausgenommen, um die Bildrate auf leistungsschwächerer Hardware zu schonen

## Mehrwert in der Flugsimulation

X-Planes Standard-Szenerie animiert keine Industrieanlagen — Schornsteine und Kühltürme bleiben statische Objekte ohne visuelle Aktivität. Diese Erweiterung ergänzt eine visuelle Ebene, die Industriegebiete während des VFR-Flugs bereits aus der Entfernung erkennbar macht: aufsteigende Rauchsäulen und Dampffahnen dienen als Orientierungspunkte und erhöhen den wahrgenommenen Realismus der Bodenumgebung. Unter Linux installiert sich das Paket als gewöhnlicher Szenerieordner ohne Plugin-Abhängigkeiten.

## Installation

**Download:** [X-Plane.org Forums](https://forums.x-plane.org/files/file/94841-smoke-steam-for-chimneys-coolingtowers-for-simheaven-10-xp12/) | [SimHeaven](https://simheaven.com)

1. Die ZIP-Datei in ein Verzeichnis **außerhalb** von X-Plane entpacken
2. Den Ordner `simHeaven_X-World_Particles_Library` nach `X-Plane 12/`[Custom Scenery](../../glossary.md#custom-scenery)`/` kopieren
3. Den Ordner in der [scenery_packs.ini](../../glossary.md#scenery_packsini) **oberhalb** von X-World registrieren

**Ladereihenfolge in scenery_packs.ini**

```
SCENERY_PACK Custom Scenery/simHeaven_X-World_Particles_Library/
SCENERY_PACK Custom Scenery/simHeaven_X-World_Europe_.../
SCENERY_PACK Custom Scenery/simHeaven_X-World_Vegetation_Library/
```

---

## Weiterführende Kapitel

| Thema | Seite | Fokus |
|---|---|---|
| Szeneriekomponenten | [Wie X-Plane die Welt aufbaut](../aufbau_quellen/scenery_components.md) | scenery_packs.ini-Ladereihenfolge und Schicht-Interaktion |
| Szeneriequellen | [Quellen](../aufbau_quellen/scenery_sources.md) | Übersicht der Szenerie-Anbieter und Datenbanken |

---

## Quellen

- [Smoke & Steam for Chimneys & Coolingtowers — X-Plane.org Forums](https://forums.x-plane.org/files/file/94841-smoke-steam-for-chimneys-coolingtowers-for-simheaven-10-xp12/)
- [SimHeaven — X-World Downloads](https://simheaven.com/xp12-sceneries/)
- [Partikelsystem in X-Plane 12 — Laminar Research Developer Docs](https://developer.x-plane.com/article/x-plane-11-particle-system/)
