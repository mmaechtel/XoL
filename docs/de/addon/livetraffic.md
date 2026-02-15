# LiveTraffic

LiveTraffic zeigt realen Flugverkehr in [X-Plane](../glossary.md#x-plane) 12 an, indem es ADS-B-Daten aus öffentlichen und kommerziellen Quellen in Echtzeit darstellt.

## Hintergrund

- **Entwickler:** TwinFan
- **Repository:** [github.com/TwinFan/LiveTraffic](https://github.com/TwinFan/LiveTraffic) (Open Source, MIT-Lizenz)
- **Plattformen:** Windows, macOS, Linux (native Binaries)
- **Kompatibilität:** X-Plane 11 und X-Plane 12
- **Preis:** Kostenlos

LiveTraffic wird aktiv gepflegt und nutzt die [XPMP2](https://github.com/TwinFan/XPMP2)-Bibliothek für GPU-Instancing und [Vulkan](../glossary.md#vulkan-api)-Kompatibilität.

## Funktionsumfang

- **Echtzeit-Flugverkehr:** Reale Flugzeuge statt AI-Traffic, basierend auf ADS-B-Daten
- **TCAS-Integration:** Verkehr erscheint auf TCAS-Displays im Cockpit
- **3D-Sound:** Triebwerke, Fahrwerk, Klappen und Rollen über [FMOD](../glossary.md#fmod) Core API
- **Landung/Start-Vorhersage:** Berechnet Rotate-, Liftoff- und Touchdown-Punkte
- **Contrails:** Kondensstreifen in konfigurierbarem Höhenbereich
- **Map-Layer:** Integration in die X-Plane-interne Karte
- **Aircraft Labels:** Konfigurierbare Fluginformationen über den Flugzeugen
- **CSL-Model-Matching:** Nutzt Bluebell OBJ8 und X-CSL-Pakete für realistische Flugzeugmodelle

### Datenquellen

Drei Kanäle funktionieren sofort ohne Registrierung:

| Kanal | Kosten | Hinweise |
|-------|--------|----------|
| adsb.fi | Kostenlos | Funktioniert sofort, anonym, standardmäßig aktiviert |
| OpenSky Network | Kostenlos | Anonym oder registriert, Abfragelimits gelten |
| Open Glider Network | Kostenlos | Anonym, unbegrenzt |

Weitere Kanäle (Registrierung oder Abo erforderlich):

| Kanal | Kosten | Hinweise |
|-------|--------|----------|
| RealTraffic | Kostenpflichtig | Umfassendste Quelle mit geparkten Flugzeugen und Wetterdaten |
| ADSBHub | Kostenlos | Nur für registrierte Daten-Feeder |
| ADS-B Exchange | Kostenpflichtig | API-Key erforderlich |
| FSCharter v2 | Kostenlos | Virtuelles Verkehrsnetzwerk |

## Mehrwert in der Flugsimulation

LiveTraffic ersetzt den generischen AI-Traffic durch reale Flugbewegungen — das aktuelle Verkehrsaufkommen am Flughafen, reale Callsigns und tatsächliche Routen. Die TCAS-Integration ermöglicht realistische Separation und Traffic Awareness. Mit RealTraffic als Datenquelle werden auch geparkte Flugzeuge und Wetterdaten injiziert.

## Installation

**Download:** [forums.x-plane.org](https://forums.x-plane.org/files/file/49749-livetraffic/)

Die ZIP-Datei nach `Resources/plugins/` entpacken. CSL-Modelle (Bluebell empfohlen) werden im Unterverzeichnis `Resources/plugins/LiveTraffic/Resources/CSL/` abgelegt.

**Abhängigkeiten auf Debian/Ubuntu:**

```bash
sudo apt install libcurl4 xdg-utils
```

### CURL_OPENSSL_4-Problem bei Steam

!!! warning "Plugin lädt nicht bei Steam-Installation"

    Bei X-Plane-Installationen über Steam kann folgender Fehler auftreten:

    ```
    libcurl.so.4: version 'CURL_OPENSSL_4' not found (required by .../LiveTraffic.xpl)
    ```

    Die Steam Runtime liefert eine ältere `libcurl.so.4` aus, der das Symbol `CURL_OPENSSL_4` fehlt. LiveTraffic ist gegen die Systemversion von libcurl gebaut, die dieses Symbol bereitstellt.

    Es gibt keinen universellen Workaround. In manchen Fällen hilft ein `LD_PRELOAD` der System-libcurl in den Steam-Startoptionen, aber das Ergebnis variiert je nach Distribution. Hinweise dazu finden sich in der [LiveTraffic-Dokumentation](https://twinfan.gitbook.io/livetraffic). Bei Nicht-Steam-Installationen tritt das Problem nicht auf.

### RealTraffic-Ports (Firewall)

Bei Nutzung von RealTraffic müssen folgende Ports für eingehenden Verkehr offen sein:

| Port | Protokoll | Zweck |
|------|-----------|-------|
| 10747 | TCP | Direktverbindung |
| 49004 | UDP | Wetterdaten |
| 49005 | UDP | Primäre Verkehrsdaten (RTTFC) |

## Quellen

- [LiveTraffic — GitHub](https://github.com/TwinFan/LiveTraffic)
- [LiveTraffic — Dokumentation](https://twinfan.gitbook.io/livetraffic)
- [XPMP2 — GitHub](https://github.com/TwinFan/XPMP2)
- [LiveTraffic — forums.x-plane.org](https://forums.x-plane.org/files/file/49749-livetraffic/)
