# Clearance

Beim Einholen einer IFR-Clearance (Instrument Flight Rules) muss sich der Pilot auf mehrere wichtige Informationen vorbereiten. Hier ist eine Minimal-Zusammenfassung:

## Vorbereitung 
* **Jeppesen oder Navigraph Charts** – für SIDs, Wegpunkte und Frequenzen.
* **FMS und Navigationsdatenbanken** – für Flugroutenvalidierung und Eingaben.
* **Flugplan** (erstellt mit z.B. Simbrief) liegt dann z.B. als PDF vor
* **ATIS-Frequenz oder digitale Anfrage (z. B. über Hoppie-Netzwerk)** für aktuelle Wetterinformationen und aktive Piste
* **FMGS/MCDU** entsprechend Flugplan programmieren

## Phrasologie

*Pilot*:
„Frankfurt Delivery, Lufthansa 123, IFR to Munich, stand A16, information Alpha, request clearance."

*ATC*:
„Lufthansa 123, cleared to Munich via MARUN 3F departure, initial climb 5000 feet, squawk 4712, contact departure on 119.9."

## Wo sind die nötigen Infos:
1. **Clearance-Delivery Frequenz** - um die Freigabe anzufragen, steht auf der Airport Karte (10-9)
2. **Flugnummer und Flugzeugkennung** - Flugplan bzw. programmierte FMGS/MCDU
3. **Abflug- und Zielflughafen** - Flugplan bzw. programmierte FMGS/MCDU
4. **Geplanter Flugweg, Departure** – Flugplan bzw. programmierte FMGS/MCDU, evtl. entsprechend geänderter Piste (siehe ATIS) angepasst
5. **Zielhöhe (initial climb altitude)** – oft auf der Departure (SID) Karte gegeben
6. **Funkfrequenz für die Departure** - oft auf der Departure (SID) Karte gegeben.
7. **Squawk** - ist individuell, gut zuhören!

## Clearance digital einholen
* **AOC Menü im MCDU** (falls verfügbar) erlaubt z. B. das Einholen einer Predeparture Clearance (PDC) digital.

### **ToLiss Airbus– Departure Clearance über CPDLC anfordern**

1. **MCDU Menü aufrufen**:

    * Drücke `<MCDU MENU>`, dann `<ATSU>`, danach `<AOC MENU>`, anschließend `<DEPARTURE CLEARANCE>`.

2. **Felder, die ausgefüllt werden müssen**:

    * **Flight Number**: Wird automatisch aus der INIT-Seite übernommen, kann aber manuell geändert werden.
    * **Departure Airport**: Ebenfalls automatisch ausgefüllt, bei Bedarf anpassbar.
    * **Arrival Airport**: Wird aus dem FMGS übernommen.
    * **Gate Number**: Manuell eingeben (z. B. `A14`).
    * **ATIS ID**: Eingeben der aktuellen ATIS-ID (z. B. `D`).
    * **Station ID** (rechts unten): Hier kommt die **Hoppie ID** des ATC-Controllers rein, bei VATSIM z. B. `EDDHDEL`.

3. **Anfrage absenden**:

    * Sobald alle Felder korrekt ausgefüllt sind **und** ein gültiger Hoppie-Login im ISCS eingetragen ist, erscheint ein `*` neben  **<REQUEST SEND>**.
    * Betätige `<REQUEST SEND>`, um die Clearance-Anfrage per Telex zu senden.

4. **Nachricht empfangen und bestätigen**:

    * Die Pre-Departure Clearance erscheint auf der Seite **Received Messages**.
    * Dort kannst Du sie lesen und mit LSK bestätigen/akzeptieren.


**Hinweis**: Ohne gültigen Hoppie-Code oder wenn Pflichtfelder fehlen, ist das Senden der Anfrage nicht möglich.


## Wie geht's weiter?
Wenn man die Clearance korrekt zurückgelesen hat geht's weiter mit:

* **Funkfrequenzen für Appron/Ground** - steht auf der Airport Karte (10-9) 