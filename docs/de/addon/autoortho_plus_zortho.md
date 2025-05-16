# AutoOrtho + zOrtho4XP

!!! info "Work in Progress"
    Diese Dokumentation befindet sich in der Entwicklungsphase und ist nicht vollständig. Die beschriebenen Methoden und Einstellungen werden kontinuierlich evaluiert und aktualisiert.

Die Integration von **AutoOrtho** mit **Ortho4XP** stellt eine optimale Lösung für **X-Plane**-Benutzer dar, die sowohl die Vorteile des **Echtzeit-Streamings** als auch hochwertige, lokale **Orthophotos** nutzen möchten. Diese Anleitung erläutert die effektive Implementierung beider Systeme.

Die Kombination basiert auf einem **hybriden Ansatz**, bei dem **AutoOrtho** für die globale Abdeckung und **zOrtho4XP** für ausgewählte, hochwertige Regionen implementiert wird. Dies ermöglicht eine schnelle Verfügbarkeit von **Orthophotos** weltweit, höchste Qualität in bevorzugten Fluggebieten, eine optimierte Speichernutzung sowie Flexibilität bei der Bildquellenauswahl.

### Einrichtung

Die Implementierung erfolgt in zwei Hauptschritten. Zunächst werden die **Ortho4XP-Kacheln** für die bevorzugten Fluggebiete generiert. Hierbei werden **Zoom-Level** 17-19 für maximale Qualität empfohlen, wobei die **Overlays** zu aktivieren sind, sofern nicht [**SimHeaven**](../scenery.md) implementiert wird. Als Bildquelle kann zwischen **Bing** und **Google** gewählt werden.

Die korrekte Struktur der `scenery_packs.ini` ist essentiell für die Interoperabilität beider Systeme:

```
SCENERY_PACK Custom Scenery/yAutoOrtho_Overlays/
SCENERY_PACK Custom Scenery/zOrtho4XP_+47+011/
SCENERY_PACK Custom Scenery/zOrtho4XP_+48+011/
SCENERY_PACK Custom Scenery/z_ao_eur/
SCENERY_PACK Custom Scenery/z_autoortho/
```

### Optimale Nutzung

Die effiziente Nutzung erfordert eine präzise **Priorisierung** der Regionen. Für häufig frequentierte Flughäfen werden **zOrtho4XP-Kacheln** mit **ZL**17-19 in einem 50km-Radius empfohlen. Hauptflugrouten profitieren von Kacheln mit **ZL**16-17, die als **Korridore** entlang der Route implementiert werden. Für alle übrigen Gebiete übernimmt **AutoOrtho** die Versorgung mit **ZL**16 als Standard.

Eine erfolgreiche Integration erfordert eine systematische Planung, regelmäßige Wartung und kontinuierliche Optimierung. Die Identifikation der Hauptfluggebiete und die Planung der **zOrtho4XP-Abdeckung** unter Berücksichtigung des verfügbaren Speicherplatzes sind entscheidend. Die Wartung umfasst die regelmäßige **Cache-Bereinigung**, Validierung der `scenery_packs.ini` und Aktualisierung beider Systeme. Die Optimierung erfolgt durch die Anpassung der **Zoom-Levels**, die Balance zwischen Qualität und Performance sowie die regelmäßige Überprüfung der Konfiguration.

### Fehlerbehebung

Die häufigsten Probleme treten bei überlappenden **Kacheln** auf, wenn mehrere **Ortho-Quellen** für dieselbe Region vorhanden sind. Dies kann durch eine präzise **Priorisierung** in der `scenery_packs.ini` behoben werden. Performance-Probleme resultieren häufig aus einer übermäßigen Anzahl hochauflösender **Kacheln** und können durch eine Reduzierung der **zOrtho4XP-Abdeckung** optimiert werden oder mit alternativen **Settings** bei der Erzeugung der Kachel.

## Neue Meshes für AutoOrtho

**zOrtho4XP** kann nicht nur für hochwertige **Orthophotos**, sondern auch als **Mesh-Generator** für **AutoOrtho** implementiert werden. Dies ermöglicht eine verbesserte **Geländedarstellung** in Kombination mit den **AutoOrtho-Texturen**.

### Vorteile

Die Implementierung von **zOrtho4XP** als **Mesh-Generator** bietet folgende Vorteile für **AutoOrtho**:

- Erhöhte Auflösung der **Geländedarstellung**
- Präzisere Darstellung **topographischer Merkmale**
- Verbesserte **topographische Darstellung** durch **Ortho Patches**

### Empfohlene Ortho4XP-Einstellungen

Für optimale Ergebnisse mit **AutoOrtho** sind die folgenden Parameter in **Ortho4XP 1.4** essentiell:

| Parameter                  | Empfohlener Wert | Beschreibung |
|---------------------------|------------------|--------------|
| `skip_downloads`          | Aktiviert        | Deaktiviert den Bilddownload |
| `skip_converts`           | Aktiviert        | Deaktiviert das DDS-Rendering |

Die übrigen Parameter werden im [**Ortho4XP-Kapitel**](ortho4xp.md) detailliert erläutert.

### Einrichtung

Die Implementierung erfolgt in drei Hauptschritten:

1. **Mesh-Generierung**:
    - Initialisierung von **zOrtho4XP**
    - Selektion der gewünschten Region
    - Aktivierung der "**Build Mesh**" Option
    - Deaktivierung von "**Build Overlays**" und "**Build Imagery**"
    - Konfiguration des **Mesh-Levels** auf 1-2 für detaillierteres Gelände
    - Deaktivierung der Bilddownloads (`skip_downloads` aktiviert)

2. **Verzeichnisstruktur**:
    - **Ortho4XP** generiert pro Kachel (z.B. `zOrtho4XP_+51+00`) drei Verzeichnisse:
        - `Earth Nav Data`
        - `terrain`
        - `textures`
    - Die separate Integration dieser Verzeichnisse in das **AutoOrtho-Konfigurationsverzeichnis** und die `scenery_packs.ini` würde die Initialisierungszeit signifikant erhöhen, da **AutoOrtho** jedes Verzeichnis beim Start mountet.
    - Daher werden die Inhalte dieser drei Verzeichnisse pro Kachel in einem einzigen Verzeichnis (z.B. `aa_zortho4xp_meshes`) konsolidiert.
    - Bei Namenskonflikten während des Kopiervorgangs können die Dateien bedenkenlos überschrieben werden, da es sich um identische **Masken** handelt.
    - Das neue Verzeichnis sollte mit `aa_` beginnen (z.B. `aa_zortho4xp_meshes`), um die korrekte Lese-Reihenfolge zu gewährleisten.
    - Speicherung des konsolidierten Verzeichnisses unter `z_autoortho/scenery`:
       ```
       Custom Scenery/z_autoortho/scenery/aa_zortho4xp_meshes/
       ```
    - Die Struktur entspricht somit den bestehenden `ao_`-Verzeichnissen

3. **scenery_packs.ini Konfiguration**:
   ```
   SCENERY_PACK Custom Scenery/yAutoOrtho_Overlays/
   SCENERY_PACK Custom Scenery/z_autoortho/scenery/aa_zortho4xp_meshes/
   SCENERY_PACK Custom Scenery/z_ao_eur/
   SCENERY_PACK Custom Scenery/z_autoortho/
   ```
   **Wichtig**: Das `aa_`-Verzeichnis muss vor den `ao_`-Verzeichnissen platziert werden, um die korrekte **Mesh-Priorisierung** zu gewährleisten.

### Best Practices

Die effektive Nutzung von **zOrtho4XP** als **Mesh-Generator** erfordert:

- Systematische Planung der **Mesh-Level** basierend auf der Flughöhe
- Berücksichtigung der verfügbaren **Speicherkapazität**
- Regelmäßige **Qualitätskontrolle** der **Meshes**
- Bedarfsorientierte Aktualisierung
- Kontinuierliches **Performance-Monitoring**
- Optimierung der **Mesh-Level**
- Ausgewogene Balance zwischen **Detailgrad** und Performance
- Regionale **Priorisierung**

## Mesh-Auflösung erhöhen

Wie im [**Ortho4XP-Kapitel**](ortho4xp.md) beschrieben, können **LiDAR-Daten** zur Verbesserung der Auflösung und Genauigkeit der **Geländedarstellung** implementiert werden. Die **LiDAR-Daten** von [sonny.4lima.de](https://sonny.4lima.de) bieten eine hohe Auflösung und Präzision für verschiedene Regionen.

### LiDAR-Integration

Siehe Kapitel [**LiDAR-Daten Integration**](ortho4xp.md#Integration von LiDAR-Daten) im **Ortho4XP-Abschnitt**.

## Fazit

Die Integration von **AutoOrtho** und **zOrtho4XP** bietet eine optimale Lösung für **X-Plane**-Benutzer, die sowohl globale Abdeckung als auch höchste Qualität in bevorzugten Regionen anstreben. Durch systematische Planung und regelmäßige Wartung können beide Systeme effektiv integriert werden und ein optimales Flugerlebnis gewährleisten. 