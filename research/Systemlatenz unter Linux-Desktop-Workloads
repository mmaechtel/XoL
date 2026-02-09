# Systemlatenz unter Linux-Desktop-Workloads

## Wissenschaftliche Zusammenfassung eines praxisbasierten Konfigurationsdialogs

---

## Abstract

Dieser Text fasst eine praxisorientierte Analyse zur Konfiguration eines Linux-Systems für latenzsensitive Anwendungen zusammen. Ausgangspunkt war ein beobachtetes Fehlverhalten bei USB-Gerätezuordnung sowie periodische Mikroruckler in einer interaktiven Simulation. Die Untersuchung entwickelte sich von Geräteschicht-Determinismus über Kernel-Scheduling bis zur Energie- und I/O-Verwaltung.

Zentrale Erkenntnis:
**Nicht Rechenleistung, sondern zeitliche Deterministik bestimmt die wahrgenommene Systemleistung.**

Die einzelnen Probleme erwiesen sich als unterschiedliche Manifestationen desselben Grundprinzips — konkurrierende asynchrone Ereignisse stören einen periodischen Hauptthread.

---

## 1. Determinismus der Geräteerkennung

### Problem

Die Reihenfolge erkannter Eingabegeräte änderte sich abhängig vom Kerneltyp.
Anwendungen verloren dadurch ihre Konfiguration.

### Ursache

Linux nummeriert Eingabegeräte nach Initialisierungszeitpunkt:

```
Hardware → USB → HID → evdev → Anwendung
```

Parallelisierung im Kernel verändert nur Mikrosekunden der Erkennung, aber:

> Anwendungen speichern nicht Geräte — sondern Reihenfolge.

Damit entsteht eine scheinbar zufällige Neukonfiguration.

### Lösungskonzept

Ein stabiler Systemzustand erfordert **Identitätsbindung statt Positionsbindung**:

| Instabil     | Stabil                |
| ------------ | --------------------- |
| js0, event17 | persistente Geräte-ID |
| Reihenfolge  | eindeutige Zuordnung  |

### Erkenntnis

Das Problem war kein Treiber- oder Kernelproblem, sondern fehlende Abstraktionsebene.
Determinismus muss unterhalb der Anwendung hergestellt werden.

---

## 2. Scheduling und CPU-Topologie

### Ausgangsfrage

Soll eine Anwendung feste CPU-Kerne exklusiv erhalten?

### Klassisches Modell

Historisch wurde Latenz reduziert durch:

- CPU-Isolation
- feste Affinität
- Realtime-Priorität

Das basiert auf der Annahme:

> Der Scheduler trifft schlechte Entscheidungen.

### Beobachtung auf moderner Hardware

Aktuelle Scheduler (CFS/EEVDF) berücksichtigen:

- Cache-Lokalität (`wake_affine`-Mechanismus)
- Wake-Frequenz (`record_wakee()` / `wake_wide()`)
- Lag-basierte Fairness (EEVDF: schlafende Threads akkumulieren positiven Lag)

Dadurch optimiert das System die Platzierung latenzsensitiver Threads automatisch — nicht durch Erkennung eines „Hauptthreads", sondern durch Bevorzugung häufig aufwachender, cache-lokaler Threads.

Feste Zuweisung führt zu:

| Effekt                      | Folge                      |
| --------------------------- | -------------------------- |
| Verlust adaptiver Migration | geringerer Boost           |
| schlechtere Cache-Nutzung   | höhere Varianz             |
| thermische Limitierung      | niedrigere Spitzenleistung |

### Erkenntnis

Optimierung verschiebt sich von **Kontrolle des Schedulers** zu **Vermeidung externer Störungen**.

---

## 3. Energieverwaltung als Latenzquelle

### Beobachtetes Symptom

Regelmäßige kurze Unterbrechungen trotz stabiler Auslastung.

### Analyse

Nicht CPU-Last, sondern Übergänge zwischen Energiestufen verursachen Verzögerungen:

| Komponente | Ereignis             | Verzögerung          |
| ---------- | -------------------- | -------------------- |
| CPU        | tiefer Schlafzustand | Aufwachlatenz        |
| SSD        | Energiesparmodus     | Initialisierungszeit |
| Boost      | thermisches Limit    | Taktreduktion        |

Die Anwendung wartet nicht auf Berechnung — sondern auf Hardwarereaktion.

### Optimierungsprinzip

Nicht maximale Frequenz, sondern minimale Übergangskosten:

> Begrenzen statt deaktivieren.

---

## 4. Interrupt-Interferenz

### Beobachtung

Eingabegeräte oder I/O-Aktivität erzeugten kurze Ruckler.

### Ursache

Hardware-Interrupts konkurrieren mit dem Hauptthread um CPU-Zeit.
Ein einzelner Interrupt kann den Frame-Zeitplan verletzen.

### Systemisches Muster

```
periodischer Hauptthread
+ zufälliger Interrupt
= verpasste Deadline
```

### Lösung

Räumliche Trennung statt Prioritätseskalation:

| Methode           | Wirkung              |
| ----------------- | -------------------- |
| Priorität erhöhen | verzögert nur andere |
| Interrupt bündeln | verhindert Kollision |

---

## 5. Speicher- und I/O-Subsystem

### Phänomen

Ruckler beim Laden neuer Datenbereiche.

### Analyse

Der Kernel optimiert Durchsatz durch gebündelte Hintergrundarbeit:

- Writeback
- Cache-Bereinigung
- Paging

Diese erzeugen seltene, aber lange Blockierungen.

### Prinzip

Durchschnittsgeschwindigkeit vs. maximale Verzögerung:

| Optimierung        | Ergebnis                           |
| ------------------ | ---------------------------------- |
| Durchsatzoptimiert | schneller, aber ungleichmäßig      |
| Latenzoptimiert    | gleichmäßig, geringfügig langsamer |

Die Wahrnehmung folgt dem zweiten Modell.

---

## 6. Kerneltyp und Konfigurationsstrategie

### Zwei Modelle

| Kernel      | Aufgabe des Tunings |
| ----------- | ------------------- |
| generisch   | Reaktion erzwingen  |
| low-latency | Störungen entfernen |

Dies erklärt, warum identische Einstellungen gegenteilige Effekte haben können.

### Zentrale Einsicht

Tuning hängt nicht von der Distribution ab, sondern von der **Scheduling-Philosophie des Kernels**.

---

## 7. Übergreifendes Prinzip

Alle beobachteten Probleme lassen sich vereinheitlichen:

```
periodischer Hauptprozess
vs.
asynchrone Systemereignisse
```

Die sichtbare Leistung wird bestimmt durch:

> maximale Verzögerung pro Zyklus, nicht mittlere Rechenzeit

---

## 8. Fazit

Die Untersuchung zeigt eine Verschiebung in der Systemoptimierung für interaktive Workloads:

Klassischer Ansatz:

> Leistung durch Kontrolle erhöhen

Moderner Ansatz (insbesondere bei Low-Latency-Kerneln):

> Stabilität durch Entstörung erreichen

Moderne Systeme entscheiden Scheduling korrekt, solange externe Einflüsse keine zufälligen Wartezeiten erzeugen.

Damit ergibt sich eine allgemeine Regel:

**Für interaktive Anwendungen mit engen Timing-Anforderungen ist zeitliche Vorhersagbarkeit oft wirkungsvoller als maximale Rechenleistung.**

---

## Kernaussagen

1. Geräte müssen identitäts- statt positionsbasiert adressiert werden
2. CPU-Isolation kann adaptive Optimierung verhindern
3. Energiesparübergänge dominieren wahrgenommene Leistung
4. Interrupt-Platzierung ist wichtiger als Priorität
5. Durchsatzoptimierung erzeugt Latenzspitzen
6. Kerneltyp bestimmt die korrekte Tuningstrategie

---

Diese Punkte beschreiben kein spezielles Programm, sondern ein generelles Verhalten moderner Linux-Systeme bei interaktiven Echtzeit-ähnlichen Workloads.
