---
description: "Ortho4XP-Tiles mit AutoOrtho-Streaming in X-Plane kombinieren. Anleitung für scenery_packs.ini-Priorität, Mesh-Generierung und LiDAR-Daten."
---
# Statische Orthofotos + Streaming kombinieren

Diese Kombination ist besonders für **hybride Spieler** geeignet — Nutzer, die ihre Stammflughäfen in höchster Qualität genießen möchten, aber auch gelegentlich neue Regionen erkunden. Einen Überblick über die verschiedenen Spielerprofile bietet die [Einführung in die Orthofotographie](../orthophotography/orthophotography_intro.md#welches-system-passt-zu-welchem-spielerprofil).

Das Prinzip ist einfach: **Ortho4XP** generiert hochauflösende, lokale Kacheln (bis ZL19) für die bevorzugten Fluggebiete, während eine **Streaming-Lösung** (z. B. AutoOrtho) die globale Abdeckung für alle übrigen Regionen übernimmt. X-Planes Szenerie-Priorisierung sorgt dafür, dass die lokalen Ortho4XP-Kacheln automatisch Vorrang vor den gestreamten Texturen erhalten.

Die Vorteile dieser Kombination:

- **Stammregionen** in maximaler Auflösung ohne Internetabhängigkeit
- **Spontanes Fliegen** überall auf der Welt ohne Vorabgenerierung
- **Optimierte Speichernutzung** — nur für die wichtigsten Regionen wird lokaler Speicher belegt

## Einrichtung

### 1. Ortho4XP-Kacheln generieren

Für die bevorzugten Fluggebiete werden zunächst Ortho4XP-Kacheln generiert. Empfohlene Einstellungen:

- **Zoom-Level 17–19** für maximale Qualität
- **Overlays aktivieren**, sofern nicht [SimHeaven](../aufbau_quellen/scenery_sources.md) verwendet wird
- Als Bildquelle stehen u. a. **Bing** und **Google** zur Verfügung

### 2. scenery_packs.ini konfigurieren

Die korrekte Reihenfolge in der `scenery_packs.ini` ist entscheidend — die Ortho4XP-Kacheln müssen **vor** den Streaming-Einträgen stehen, damit sie Vorrang erhalten. Das folgende Beispiel zeigt die Konfiguration am Beispiel von AutoOrtho (bei anderen Streaming-Lösungen sind die Verzeichnisnamen entsprechend anzupassen):

```
SCENERY_PACK Custom Scenery/yAutoOrtho_Overlays/
SCENERY_PACK Custom Scenery/zOrtho4XP_+47+011/
SCENERY_PACK Custom Scenery/zOrtho4XP_+48+011/
SCENERY_PACK Custom Scenery/z_ao_eur/
SCENERY_PACK Custom Scenery/z_autoortho/
```

## Empfohlene Abdeckungsstrategie

| Gebiet | Ortho-Quelle | Zoom-Level | Hinweis |
|---|---|---|---|
| Stammflughäfen (50 km Radius) | Ortho4XP | ZL17–19 | Maximale Qualität für Anflug und Umgebung |
| Hauptflugrouten | Ortho4XP | ZL16–17 | Korridore entlang der Route |
| Alle übrigen Gebiete | Streaming | ZL16 (Standard) | Automatisch, keine Vorbereitung nötig |

## Fehlerbehebung

**Überlappende Kacheln**: Wenn mehrere Ortho-Quellen für dieselbe Region vorhanden sind, entscheidet die Reihenfolge in der `scenery_packs.ini` über die Priorität. Ortho4XP-Einträge sollten immer vor den Streaming-Einträgen stehen.

**Performance-Probleme**: Zu viele hochauflösende Ortho4XP-Kacheln können die Ladezeiten erhöhen. In diesem Fall die Abdeckung auf die wichtigsten Regionen reduzieren oder niedrigere Zoom-Level verwenden.

## Ortho4XP-Meshes für Streaming nutzen

Ortho4XP kann nicht nur Texturen, sondern auch **Meshes** generieren — also präzisere Höhenmodelle. Diese Meshes lassen sich mit gestreamten Texturen kombinieren, um eine bessere Geländedarstellung zu erreichen, ohne lokale Texturdaten vorhalten zu müssen.

!!! note "Beispiele am Beispiel AutoOrtho"
    Die folgenden Verzeichnisstrukturen und `scenery_packs.ini`-Einträge beziehen sich auf AutoOrtho. Das Prinzip ist bei anderen Streaming-Lösungen identisch — die Verzeichnisnamen sind entsprechend anzupassen.

### Vorteile

- Höhere Auflösung der Geländedarstellung
- Präzisere topographische Merkmale (Berge, Täler, Küsten)
- Verbesserte Flughafen-Topographie durch Ortho Patches

### Ortho4XP-Einstellungen für reine Mesh-Generierung

Um nur Meshes ohne Texturen zu erzeugen, werden in Ortho4XP folgende Parameter gesetzt:

| Parameter | Wert | Beschreibung |
|---|---|---|
| `skip_downloads` | Aktiviert | Überspringt den Bilddownload |
| `skip_converts` | Aktiviert | Überspringt das DDS-Rendering |
| Build Mesh | Aktiviert | Erzeugt das Höhenmodell |
| Build Overlays | Deaktiviert | Keine Overlays nötig |
| Build Imagery | Deaktiviert | Keine Texturen nötig |
| Mesh-Level | 1–2 | Höherer Wert = detaillierteres Gelände |

Die übrigen Parameter werden im [Ortho4XP-Kapitel](../orthophotography/ortho4xp.md#wichtige-parameter) erläutert; die speziell für Mesh-only-Builds nötigen Einstellungen behandelt [Pakete für Ortho-Streaming bauen](../orthophotography/ortho4xp.md#pakete-fur-ortho-streaming-bauen).

### Verzeichnisstruktur

Ortho4XP erzeugt pro Kachel (z. B. `zOrtho4XP_+51+00`) drei Verzeichnisse: `Earth Nav Data`, `terrain` und `textures`. Da AutoOrtho beim Start jedes Verzeichnis einzeln mountet, würde das separate Einbinden die Initialisierungszeit erhöhen.

Daher werden die Inhalte aller Kacheln in einem einzigen Verzeichnis konsolidiert:

```
Custom Scenery/z_autoortho/scenery/aa_zortho4xp_meshes/
```

- Das Präfix `aa_` stellt sicher, dass das Verzeichnis vor den `ao_`-Verzeichnissen gelesen wird
- Bei Namenskonflikten können Dateien bedenkenlos überschrieben werden (identische Masken)

Die `scenery_packs.ini` wird entsprechend angepasst:

```
SCENERY_PACK Custom Scenery/yAutoOrtho_Overlays/
SCENERY_PACK Custom Scenery/z_autoortho/scenery/aa_zortho4xp_meshes/
SCENERY_PACK Custom Scenery/z_ao_eur/
SCENERY_PACK Custom Scenery/z_autoortho/
```

Das `aa_`-Verzeichnis muss **vor** den `ao_`-Verzeichnissen stehen, damit die Ortho4XP-Meshes Vorrang erhalten.

## Mesh-Auflösung mit LiDAR-Daten erhöhen

Wie im [Ortho4XP-Kapitel](../orthophotography/ortho4xp.md) beschrieben, können LiDAR-Daten die Auflösung und Genauigkeit der Geländedarstellung weiter verbessern. Die LiDAR-Daten von [sonny.4lima.de](https://sonny.4lima.de) bieten eine hohe Auflösung für verschiedene Regionen.

Siehe [LiDAR-Daten Integration](../orthophotography/ortho4xp.md#integration-von-lidar-daten) im Ortho4XP-Kapitel.

## Fazit

Die Kombination aus statischer Generierung und Streaming bietet eine flexible Lösung für X-Plane-Nutzer, die sowohl höchste Qualität in bevorzugten Regionen als auch weltweite Abdeckung wünschen. Der Schlüssel liegt in der gezielten Auswahl der Ortho4XP-Regionen und der korrekten Priorisierung in der `scenery_packs.ini`.

---

## Weiterführende Kapitel

| Thema | Seite | Schwerpunkt |
|---|---|---|
| AutoOrtho | [AutoOrtho](autoortho.md) | Streaming-Konfiguration und Cache-Verwaltung |
| XEarthLayer | [XEarthLayer](xearthlayer.md) | Alternative Streaming-Lösung |
| Ortho4XP | [Ortho4XP](../orthophotography/ortho4xp.md#pakete-fur-ortho-streaming-bauen) | Parameter-Referenz, Mesh-only-Pakete und LiDAR-Integration |
| Szenerie-Komponenten | [Wie X-Plane die Welt aufbaut](../aufbau_quellen/scenery_components.md) | scenery_packs.ini-Ladereihenfolge und Prioritätsregeln |
| Dateisystem | [Dateisystem](../../linux/optimizations/filesystem.md) | Speicheroptimierung für lokale Kacheln und Cache |
| GPU & VRAM | [GPU & VRAM](../../fundamentals/performance/gpu_vram.md) | VRAM-Auswirkungen kombinierter Ortho-Quellen |
