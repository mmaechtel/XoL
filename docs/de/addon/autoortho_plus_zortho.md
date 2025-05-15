# AutoOrtho + zOrtho4XP

!!! info "Work in Progress"
    Diese Dokumentation befindet sich noch in der Entwicklung und ist nicht vollständig. Die beschriebenen Methoden und Einstellungen werden kontinuierlich überprüft und aktualisiert.

Die Kombination von AutoOrtho mit Ortho4XP bietet eine optimale Lösung für X-Plane-Benutzer, die sowohl die Vorteile des Echtzeit-Streamings als auch hochwertige, lokale Orthophotos nutzen möchten. Diese Anleitung erklärt, wie beide Systeme effektiv zusammenarbeiten können.

## Grundkonzept

Die Kombination basiert auf einem hybriden Ansatz, bei dem AutoOrtho für die allgemeine, weltweite Abdeckung und zOrtho4XP für ausgewählte, hochwertige Regionen eingesetzt wird. Dies ermöglicht eine schnelle Verfügbarkeit von Orthophotos weltweit, höchste Qualität in bevorzugten Fluggebieten, eine optimierte Speichernutzung und Flexibilität bei der Bildquellenauswahl.

## Installation und Konfiguration

### Voraussetzungen

Für die erfolgreiche Kombination von AutoOrtho und Ortho4XP benötigen Sie

- Eine funktionierende AutoOrtho-Installation
- Ortho4XP (Version 1.4 oder höher)
- Ausreichend SSD-Speicher für Ortho4XP-Kacheln
- Python 3.x für Ortho4XP

### Empfohlene Ortho4XP-Einstellungen

Für optimale Ergebnisse mit AutoOrtho verwenden Sie folgende Einstellungen in Ortho4XP 1.4

| Parameter                  | Empfohlener Wert | Beschreibung |
|---------------------------|------------------|--------------|
| `skip_downloads`          | Aktiviert        | Kein Bilddownload nötig |
| `skip_converts`           | Aktiviert        | Kein DDS-Rendering nötig |
| `mask_zl`                 | 16               | Optimale Wasserübergänge |
| `use_masks_for_inland`    | Aktiviert        | Bessere Binnengewässer |
| `distance_masks_too`      | Aktiviert        | Saubere Küstenlinien |
| `custom_dem`              | Optional         | Höhere DEMs für feinere Meshes |
| `curvature_tol`           | 2.0–4.0          | Beeinflusst die Mesh-Komplexität |
| `road_banking_limit`      | 0.3              | Verhindert Build-Fehler |
| `apt_smoothing_pix`       | 8–16             | Glattere Landebahnen |
| `water_tech`              | "XP12"           | Verwendet XP12 Wassertechnologie |

### Einrichtung

Die Einrichtung erfolgt in zwei Hauptschritten. Zuerst erstellen Sie die Ortho4XP-Kacheln für Ihre bevorzugten Fluggebiete. Wählen Sie dabei Zoom-Level 17-19 für maximale Qualität und aktivieren Sie die Overlays. Als Bildquelle können Sie zwischen Bing und Google wählen.

Die korrekte Struktur der scenery_packs.ini ist entscheidend für das Zusammenspiel beider Systeme

```
SCENERY_PACK Custom Scenery/yAutoOrtho_Overlays/
SCENERY_PACK Custom Scenery/zOrtho4XP_+47+011/
SCENERY_PACK Custom Scenery/zOrtho4XP_+48+011/
SCENERY_PACK Custom Scenery/z_ao_eur/
SCENERY_PACK Custom Scenery/z_autoortho/
```

## Optimale Nutzung

### Regionale Priorisierung

Die optimale Nutzung erfordert eine klare Priorisierung der Regionen. Für häufig genutzte Flughäfen empfehlen sich zOrtho4XP-Kacheln mit ZL17-19 in einem 50km Umkreis. Hauptflugrouten profitieren von Kacheln mit ZL16-17, die als Korridore entlang der Route angelegt werden. Für alle anderen Gebiete übernimmt AutoOrtho die Versorgung mit ZL16 als Standard.

### Performance-Optimierung

Eine effektive Performance-Optimierung basiert auf zwei Hauptaspekten: der Cache-Verwaltung und den Grafikeinstellungen. Der AutoOrtho-Cache sollte zwischen 20-30 GB liegen, während die zOrtho4XP-Kacheln nach Bedarf verwaltet werden. Regelmäßige Cache-Bereinigung ist wichtig. Bei den Grafikeinstellungen empfehlen sich maximale Texturen, hohe Objektdichte und minimale Reflexionen.

## Fehlerbehebung

### Häufige Probleme

Die häufigsten Probleme treten bei überlappenden Kacheln auf, wenn mehrere Ortho-Quellen für dieselbe Region vorhanden sind. Dies lässt sich durch eine klare Priorisierung in der scenery_packs.ini beheben. Performance-Probleme entstehen oft durch zu viele hochauflösende Kacheln und können durch eine Reduzierung der zOrtho4XP-Abdeckung gelöst werden. Speicherprobleme bei großen zOrtho4XP-Kacheln erfordern eine selektive Kachelerstellung.

## Best Practices

Eine erfolgreiche Kombination erfordert sorgfältige Planung, regelmäßige Wartung und kontinuierliche Optimierung. Identifizieren Sie Ihre Hauptfluggebiete und planen Sie die zOrtho4XP-Abdeckung unter Berücksichtigung des verfügbaren Speicherplatzes. Die Wartung umfasst regelmäßige Cache-Bereinigung, Überprüfung der scenery_packs.ini und Aktualisierung beider Systeme. Die Optimierung erfolgt durch Anpassung der Zoom-Levels, Balance zwischen Qualität und Performance sowie regelmäßige Überprüfung der Einstellungen.

## Neue Meshes für AutoOrtho

zOrtho4XP kann nicht nur für hochwertige Orthophotos, sondern auch als Mesh-Generator für AutoOrtho verwendet werden. Dies ermöglicht eine verbesserte Geländedarstellung in Kombination mit den AutoOrtho-Texturen.

### Vorteile

Die Verwendung von zOrtho4XP als Mesh-Generator bietet mehrere Vorteile:

- Höhere Auflösung des Geländes
- Bessere Darstellung von Bergen und Tälern
- Präzisere Flughafen-Glättungen
- Optimierte Performance durch lokale Mesh-Daten

### Einrichtung

Die Einrichtung erfolgt in drei Hauptschritten:

1. **Mesh-Generierung**:
    - Starten Sie zOrtho4XP
    - Wählen Sie die gewünschte Region
    - Aktivieren Sie die "Build Mesh" Option
    - Deaktivieren Sie "Build Overlays" und "Build Imagery"
    - Setzen Sie das Mesh-Level auf 1-2 für detaillierteres Gelände
    - Deaktivieren Sie die Bilddownloads (skip_downloads aktiviert)

2. **Verzeichnisse zusammenführen**:
    - Für jede zOrtho4XP-Kachel werden drei Verzeichnisse erstellt:
        - `Earth Nav Data`
        - `terrain`
        - `textures`
    - Diese Verzeichnisse müssen in ein neues Verzeichnis zusammengeführt werden
    - Das neue Verzeichnis sollte mit `aa_` beginnen (z.B. `aa_zortho4xp_meshes`)
    - Speichern Sie das zusammengeführte Verzeichnis unter:
     ```
     Custom Scenery/z_autoortho/scenery/aa_zortho4xp_meshes/
     ```
    - Die Struktur sollte den bestehenden `ao_`-Verzeichnissen entsprechen

3. **scenery_packs.ini anpassen**:
   ```
   SCENERY_PACK Custom Scenery/yAutoOrtho_Overlays/
   SCENERY_PACK Custom Scenery/z_autoortho/scenery/aa_zortho4xp_meshes/
   SCENERY_PACK Custom Scenery/z_ao_eur/
   SCENERY_PACK Custom Scenery/z_autoortho/
   ```
   **Wichtig**: Das `aa_`-Verzeichnis muss direkt vor den `ao_`-Verzeichnissen platziert werden, damit AutoOrtho zuerst dort nach Meshes sucht.

### Best Practices

Die erfolgreiche Nutzung von zOrtho4XP als Mesh-Generator erfordert:

- Sorgfältige Planung der Mesh-Level basierend auf der Flughöhe
- Berücksichtigung des verfügbaren Speicherplatzes
- Regelmäßige Überprüfung der Mesh-Qualität
- Aktualisierung bei Bedarf
- Performance-Monitoring
- Anpassung der Mesh-Level
- Balance zwischen Detail und Performance
- Regionale Priorisierung

## Mesh-Auflösung erhöhen

Wie in zOrtho4XP bereits beschrieben, können LiDAR-Daten verwendet werden, um die Auflösung und Genauigkeit des Geländes zu verbessern. Die LiDAR-Daten von [sonny.4lima.de](https://sonny.4lima.de) bieten eine hohe Auflösung und Genauigkeit für verschiedene Regionen.

### LiDAR-Integration

Siehe Kapitel Integration von [LiDAR-Daten](ortho4xp.md#Integration von LiDAR-Daten) im Abschnitt Ortho4XP.

## Fazit

Die Kombination von AutoOrtho und zOrtho4XP bietet die beste Lösung für X-Plane-Benutzer, die sowohl weltweite Abdeckung als auch höchste Qualität in bevorzugten Regionen wünschen. Mit sorgfältiger Planung und regelmäßiger Wartung können beide Systeme harmonisch zusammenarbeiten und ein optimales Flugerlebnis bieten. 