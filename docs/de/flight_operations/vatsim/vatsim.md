# VATSim

VATSIM (Virtual Air Traffic Simulation Network) ist das weltweit größte Netzwerk für virtuelle Flugsimulation mit realistischem Flugverkehr und Flugsicherung.

## Aktuelle Flugrouten

Basierend auf VATSIM Bookings und Events werden regelmäßig aktuelle Flugrouten berechnet und zur Verfügung gestellt:

📄 **[Aktuelle VATSIM Flugrouten anzeigen](/Maps/vatsim_routes.html)**

### Wie funktioniert das?

Ein Script sucht online die VATSIM Bookings und Events und errechnet aufgrund der Controller-Abdeckungen und Events mögliche Flüge mit maximaler ATC-Abdeckung. In der HTML-Seite werden dann mögliche Flüge inklusive statistischer Infos angezeigt.

**Besonderheit:** Die Berechnungen erfolgen meistens mit A320-Geschwindigkeit (da dieser Flugzeugtyp am häufigsten genutzt wird). Ist man schneller unterwegs, passen die Zeitfenster noch besser!

Die Datei wird automatisch basierend auf aktuellen VATSIM Bookings und Events generiert und enthält die empfohlenen Flugrouten für die kommenden Events mit optimaler Controller-Abdeckung.

## Was ist VATSIM?

VATSIM bietet Piloten und Fluglotsen die Möglichkeit, in einer realistischen Umgebung zu fliegen und zu arbeiten. Das Netzwerk simuliert echte Flugverkehrsabläufe mit:

- Realistischen Flugplänen
- Live-Fluglotsen
- Wetterdaten
- Flugverkehrsregeln

## Erste Schritte

Um mit VATSIM zu beginnen, benötigen Sie:

1. **VATSIM Account**: Registrieren Sie sich kostenlos auf [vatsim.net](https://vatsim.net)
2. **VATSIM Client**: Laden Sie einen kompatiblen Client herunter (z.B. vPilot, xPilot)
3. **Flugplan**: Erstellen Sie einen realistischen Flugplan
4. **Training**: Besuchen Sie die VATSIM Academy für Grundlagen

## Nützliche Links

- [VATSIM Website](https://vatsim.net)
- [VATSIM Academy](https://academy.vatsim.net)
- [VATSIM Rules](https://vatsim.net/docs/policy)
- [Client Downloads](https://vatsim.net/community/pilots/software)

---

## Weiterführende Kapitel

| Thema | Seite | Schwerpunkt |
|---|---|---|
| Clearance | [Clearance](../atc/clearance.md) | IFR-Freigabeverfahren und CPDLC |
| Pushback & Taxi | [Pushback & Taxi](../atc/pushback_taxi.md) | Rollverfahren am Boden |
| Streckenflug | [Streckenflug](../atc/enroute.md) | Center-Lotse und Frequenzwechsel |
| Anflug | [Anflug](../atc/approach.md) | Anflugverfahren und Radar Vectors |
| Wetter-Briefing | [Wetter-Briefing](../weather/briefing.md) | Wettervorbereitung für Online-Flüge | 