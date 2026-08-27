---
title: Windows-X-Plane-Addons via KVM
description: "Drei Windows-exklusive X-Plane-Addons unter Linux via KVM-Virtualisierung nutzen: My FS Flights, MobiFlight und SayIntentions.AI."
---
# Via KVM

Drei Windows-only Addons, die über [KVM-Virtualisierung](../../linux/extensions/kvm.md) unter Linux nutzbar werden: Ein Windows-Gast führt das Addon aus, X-Plane läuft weiter nativ auf dem Linux-Host, und beide kommunizieren über das Netzwerk. [My FS Flights](myfs_flights.md) zeichnet Flüge auf und gibt KI-gestütztes Landefeedback; sein Connector erkennt den Simulator automatisch, die VM braucht also nur Netzwerkzugriff auf den Host. [MobiFlight](mobiflight.md) bindet Arduino- oder Pico-basierte Hardware-Cockpits an — entweder von einem zweiten Windows-PC aus oder aus einer VM mit USB-Passthrough für die Boards, plus UDP-Relay für Port 49000. [SayIntentions.AI](sayintentions.md) liefert sprachgesteuertes ATC und braucht UDP-Portweiterleitung und Mikrofon-Passthrough in den Gast.

Sofern kein zweiter Windows-PC vorhanden ist, zuerst die VM über das KVM-Kapitel einrichten — die Addon-Seiten bauen auf einem laufenden Windows-Gast auf und ergänzen nur das addon-spezifische Netzwerk und Passthrough.

- **[My FS Flights](myfs_flights.md)** — Flugbuch und Statistiken
- **[MobiFlight](mobiflight.md)** — Hardware-Cockpit-Anbindung
- **[SayIntentions.AI](sayintentions.md)** — KI-gestützte ATC-Kommunikation
