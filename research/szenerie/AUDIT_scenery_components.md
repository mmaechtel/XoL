# Audit: scenery_components.md

## Kopf

| Feld | Wert |
|------|------|
| **Datei** | `docs/en/scenery_components.md` |
| **Titel** | How X-Plane Builds the World / scenery_packs.ini |
| **Zeilen** | 171 |
| **Aufwand** | M |
| **Audit-Datum** | 2026-02-16 |
| **Gesamtbewertung** | C |

---

## Detail-Tabelle

| # | Zeile | Abschnitt | Behauptung | Typ | Bewertung | Quelle / Beleg | Empfehlung | Entscheidung |
|---|-------|-----------|------------|-----|-----------|----------------|------------|:------------:|
| 1 | 15 | Meshes | "It consists of many small triangles (polygons) that together form a network" | FAK | OK | X-Plane nutzt TIN (Triangulated Irregular Network) in DSF-Dateien. "Polygons" leicht ungenau — tatsächlich ausschließlich Dreiecke. | Optional: "polygons" → "triangles" | korrigiert |
| 2 | 24 | Orthos | "they are placed as image files (e.g., .jpg or .png) on the mesh" | FAK | FAIL | **Eigenes Glossar**, Zeile 88: "DDS files contain GPU-compressed image data (often in DXT/BC format)". Ortho4XP, AutoOrtho, XEarthLayer und XPME generieren/liefern alle DDS-Texturen. .jpg/.png sind Quellformate der Kartendienste, nie das Format in X-Plane. | .jpg/.png → DDS korrigieren | korrigiert |
| 3 | 34 | Autogen | "It often uses data sources like OpenStreetMap to know where cities, forests, or roads are" | FAK | WARN | OSM-Daten sind in Laminar's DSF-Dateien eingebacken (Build-Pipeline). X-Plane liest zur Laufzeit nicht von OSM. SimHeaven (Drittanbieter) nutzt OSM separat. Formulierung suggeriert Laufzeit-Abfrage. | Präzisieren: DSF-Dateien basieren auf OSM-Daten, werden nicht zur Laufzeit abgefragt | korrigiert |
| 4 | 53 | Add-ons | "XPME stream satellite imagery in real time" | FAK | OK | XPME (X-Plane Map Enhancement) existiert, 82 Releases, aktiv entwickelt. Linux-Support seit v4.2.3 (Feb 2026, Beta). | Optional: Beta-Status auf Linux erwähnen | — |
| 5 | 65 | scenery_packs.ini | "X-Plane loads sceneries from bottom to top [...] entries further down have higher priority" | FAK | FAIL | **Widerspruch zu Zeile 160**, zum Beispiel (Zeile 102: "highest priority" oben), und zu static_plus_streaming.md (Zeile 25: "listed before [...] so they take priority"). TOP = höchste Priorität, nicht BOTTOM. | Korrigieren: Einträge weiter oben haben höhere Priorität | korrigiert |
| 6 | 160 | Warum Reihenfolge wichtig | "Entries further up (with higher priority) overwrite entries further down" | FAK | OK | Korrekt. Konsistent mit Beispiel und anderen Seiten. | — | — |
| 7 | 162 | Warum Reihenfolge wichtig | "A logical order helps X-Plane load sceneries more efficiently, which can improve loading times and performance" | FAK | WARN | Nicht belegbar. Reihenfolge beeinflusst nur visuelle Korrektheit (welche Schicht "gewinnt"), nicht Ladegeschwindigkeit. Verwechslung mit aktivierten/deaktivierten Sceneries. | Streichen oder abschwächen ("visual correctness") | gestrichen |
| 8 | 59 | Zweite H1 | Seite hat zwei `# `-Überschriften (Zeile 1 + 59) | DET | FAIL | MkDocs erwartet eine H1 pro Seite. Zweite H1 erzeugt fehlerhafte TOC-Hierarchie. | `# Die richtige Reihenfolge...` → `## Die richtige Reihenfolge...` | korrigiert |
| 9 | 148 | Global Airports | "It should be after custom sceneries and landmarks, but before SimHeaven components and orthos" | FAK | OK | Konsistent mit korrekter Prioritätslogik (top = höchste Priorität). Custom oben, Global Airports darunter, SimHeaven/Orthos/Mesh weiter unten. | — | — |

---

## Struktur-Review

| Aspekt | Bewertung | Anmerkung |
|--------|-----------|-----------|
| Fehlende Themen | OK | Für den Zweck der Seite (Einführung in Scenery-Konzepte) vollständig genug |
| Überflüssiges | WARN | Einige Passagen sind plattformunabhängig (Was ist ein Mesh, Was ist Autogen) und nicht Linux-spezifisch. Für eine Einführungsseite akzeptabel, aber der Ton ist ungewöhnlich basal im Vergleich zum Rest der Doku. |
| Zielgruppe | WARN | Sehr didaktischer, nahezu kindlicher Ton ("like a giant photo glued onto the mesh", "cows, trees, and small huts"). Zielgruppe ist erfahrene Linux-User. Nicht falsch, aber stilistisch inkonsistent mit nvidia.md, systemtools.md, begin.md. |
| Struktur | WARN | Zwei H1-Überschriften. Eigentlich zwei separate Themen (Konzepte + INI-Reihenfolge) auf einer Seite. Keine `---` Trennlinien zwischen Hauptsektionen. |
| Querverweise | OK | Links zu Ortho4XP, Ortho Streaming, XOrganizer vorhanden und korrekt |
| Stilkonsistenz | WARN | Kein einordnender Einstiegssatz (vgl. begin.md, nvidia.md). Kein Sources-Abschnitt am Ende. Kein Prose↔Tabelle↔Code-Wechsel — fast nur Fließtext mit einem Code-Block. |

---

## Gesamtbewertung: C

Die Seite enthält einen **faktischen Fehler** (Prioritätsrichtung scenery_packs.ini, der sich selbst widerspricht), einen **falschen Dateiformats-Hinweis** (.jpg/.png statt DDS), und einen **stilistischen Bruch** mit dem Rest der Dokumentation. Die Grundstruktur (Mesh → Ortho → Autogen → INI-Reihenfolge) ist sinnvoll, der Inhalt braucht aber Korrekturen und stilistische Angleichung.

---

## Lektorat

| # | Zeile | Befund | Korrektur |
|---|-------|--------|-----------|
| L1 | 56 | "This chapter explains..." — redundant, "chapter" unpassend für Webseite | Satz entfernt |
| L2 | 155 | "correct order... crucial for visual correctness" — Wortwiederholung | Umformuliert: "The order... directly affects visual correctness" |

Gesamteindruck nach Korrektur: Seite liest sich flüssig. Erster Teil (Konzepte) ist kompakt und technisch korrekt. Zweiter Teil (INI-Reihenfolge) hat klare Struktur mit Beispiel. Ton konsistent mit nvidia.md, systemtools.md. Sources-Abschnitt ergänzt.

---

## Markdown-Check

- Leerzeile nach jeder Überschrift: OK
- Doppelpunkte vor Listen: OK (keine)
- Listen-Einrückung (4 Spaces): OK
- Code-Block-Tags (`ini`): OK
- `---` Trennlinien zwischen Hauptsektionen: OK
- Sources-Abschnitt am Ende: OK
- Trailing `  ` in Listenpunkten 62–90: Intentionale `<br>` für Function/Why/Example-Struktur — OK

Keine Markdown-Fixes nötig.
