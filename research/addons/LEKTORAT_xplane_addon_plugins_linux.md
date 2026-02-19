# Lektorat: X-Plane Addon-Plugins unter Linux — Redaktionelle Empfehlungen

Dieses Dokument ist das Briefing fuer die Umsetzung.

---

## Zielgruppe und Leitfrage

**Leser:** Linux-Nutzer mit X-Plane-Erfahrung, grundlegende Linux-Kenntnisse.
**Leitfrage:** Wuerde ein Linux-Nutzer das selbst herausfinden? Wenn ja → weglassen.

---

## Bestandsaufnahme: Bereits dokumentierte Seiten

| Thema | Bestehende Seite | Status |
|---|---|---|
| LinuxTrack | `addon/cockpit/linuxtrack.md` | Aktuell (X-IR Fork v0.99.29) |
| XLinSpeak | `addon/tools/xlinspeak.md` | Aktuell (XP12 Fork) |
| SayIntentions.AI | `addon/kvm/sayintentions.md` | Aktuell (KVM-Workaround) |
| My FS Flights | `addon/kvm/myfs_flights.md` | Aktuell (KVM-Workaround) |
| XCamera | `addon/cockpit/xcamera.md` | Erwaehnt OpenTrack |

---

## Empfehlung: Neue Seiten

### 1. Xchecklist — NEUE SEITE empfohlen

**Datei:** `docs/{lang}/addon/cockpit/xchecklist.md`
**Nav-Position:** Addon > Cockpit (neben Avitab, XCamera)

**Empfehlung:** EIGENE SEITE

| Unterthema | Mehrwert? | Empfehlung |
|---|---|---|
| Grundfunktion (Checklisten) | HOCH | UEBERNEHMEN — zentrales Cockpit-Addon, Linux-nativ |
| TTS-Integration (libspeechd) | HOCH | UEBERNEHMEN — Linux-spezifischer Aspekt |
| Build aus Quellcode | MITTEL | KURZ HALTEN — Pre-Built-Binary ist Standard |
| clist.txt-Format | GERING | WEGLASSEN — Checklisten-Erstellung ist kein Linux-Thema |
| Querverweis XLinSpeak | HOCH | UEBERNEHMEN — erklaert Zusammenspiel |

**Redaktionelle Entscheidung:** Xchecklist ist eines der wichtigsten Cockpit-Plugins und laeuft nativ unter Linux. Der Linux-spezifische Aspekt ist die TTS-Integration via speech-dispatcher. Eine kompakte Seite (Steckbrief, Features, Installation, Linux-TTS-Setup, Querverweis XLinSpeak) ist sinnvoll.

**Geplante Gliederung:**

1. Background (Steckbrief, Entwickler, Plattformen)
2. Features (Kernfunktionen)
3. Value in Flight Simulation (warum relevant)
4. Installation (Download + Debian-Dependencies fuer Build)
5. TTS on Linux (speech-dispatcher, Zusammenspiel mit XLinSpeak)
6. Sources

---

### 2. XP Walkaround — KEINE EIGENE SEITE

**Empfehlung:** WEGLASSEN (vorerst)

| Unterthema | Mehrwert? | Empfehlung |
|---|---|---|
| Plugin-Beschreibung | GERING | Plattformunabhaengig, kein Linux-Spezifikum |
| Installation | GERING | Standard-Plugin-Installation, nichts Linux-spezifisches |

**Redaktionelle Entscheidung:** XP Walkaround laeuft zwar nativ unter Linux, bietet aber keinerlei Linux-spezifische Aspekte. Es ist ein kommerzielles Plugin ohne besondere Konfiguration. Das Prinzip unserer Dokumentation ist: nur Linux-Spezifika. Kann spaeter in eine allgemeine Plugin-Uebersichtsseite aufgenommen werden, wenn `xplane/plugins.md` geschrieben wird.

---

### 3. My FS Flights — KEINE AENDERUNG

Bereits dokumentiert. Keine Ergaenzungen noetig.

---

### 4. Copilot-Plugins — KEINE EIGENE SEITE (vorerst)

**Empfehlung:** KURZ HALTEN — Erwaehnung in kuenftiger `xplane/plugins.md`

| Plugin | Mehrwert? | Empfehlung |
|---|---|---|
| KPCrew | MITTEL | Erwaehnung als Tipp — FlyWithLua-basiert, Linux-kompatibel |
| XAnimCopilot | MITTEL | Erwaehnung als Tipp — 737-spezifisch |
| Speedy Copilot | GERING | Zu nischig fuer eigene Seite |
| XFirstOfficer | GERING | Linux-Support unbestaetigt |
| SmartCopilot | GERING | Shared Cockpit, nicht Linux-spezifisch |

**Redaktionelle Entscheidung:** Keines der Copilot-Plugins hat signifikante Linux-spezifische Aspekte. Sie laufen entweder ueber FlyWithLua (plattformunabhaengig) oder als XPLM-Plugin (mit lin.xpl, keine besondere Konfiguration). Eine Erwaehnung in einer kuenftigen Plugin-Uebersichtsseite ist sinnvoll, aber keine eigene Seite.

**Alternative:** Ein kurzer "Copilot Options on Linux"-Abschnitt koennte in die geplante `xplane/plugins.md` integriert werden (Prio 7 in TODO.md).

---

### 5. Headtracking — BESTEHENDE SEITE ERGAENZEN

**Datei:** `docs/{lang}/addon/cockpit/linuxtrack.md` ODER neue `opentrack.md`

**Empfehlung:** NEUE SEITE `opentrack.md` + Querverweis von `linuxtrack.md`

| Unterthema | Mehrwert? | Empfehlung |
|---|---|---|
| OpenTrack Grundfunktion | HOCH | UEBERNEHMEN — Hauptloesung fuer Headtracking unter Linux |
| NeuralNet Tracker (Webcam) | HOCH | UEBERNEHMEN — Zero-Hardware-Option, Linux-nativ |
| HeadTrack Plugin (amyinorbit) | HOCH | UEBERNEHMEN — empfohlene X-Plane-Bridge unter Linux |
| Build-Anleitung (Debian) | HOCH | UEBERNEHMEN — Linux-spezifisch |
| SmoothTrack | MITTEL | KURZ HALTEN — kurze Erwaehnung als Input-Option |
| AITrack | GERING | WEGLASSEN — archiviert, durch NeuralNet Tracker ersetzt |

**Redaktionelle Entscheidung:** OpenTrack ist die umfassendere und aktivere Loesung gegenueber LinuxTrack. Eine eigene Seite ist gerechtfertigt, weil:
- Die empfohlene Verbindungsmethode (UDP + HeadTrack-Plugin) Linux-spezifisch dokumentiert werden muss
- Der NeuralNet Tracker eine Zero-Hardware-Option bietet, die besonders fuer Linux-Nutzer relevant ist
- Build-Anleitung fuer Debian ein typisches XoL-Thema ist

**Geplante Gliederung:**

1. Background (Steckbrief, Plattformen)
2. Features (6DOF, Tracker-Optionen)
3. Value in Flight Simulation
4. Recommended Linux Setup (Stack-Diagramm)
5. Installation (Debian-Build, AUR, Snap)
6. Configuration (OpenTrack → HeadTrack Plugin via UDP)
7. NeuralNet Tracker (Webcam-Option)
8. SmoothTrack (Smartphone-Option)
9. Sources

**Aenderungen an bestehenden Seiten:**
- `linuxtrack.md`: Querverweis auf `opentrack.md` ergaenzen ("Alternative: OpenTrack offers ...")
- `xcamera.md`: Pruefen ob OpenTrack-Abschnitt aktualisiert werden sollte

---

### 6. TTS — BESTEHENDE SEITE ERGAENZEN

**Datei:** `docs/{lang}/addon/tools/xlinspeak.md` ergaenzen

**Empfehlung:** ERGAENZUNG der bestehenden Seite

| Unterthema | Mehrwert? | Empfehlung |
|---|---|---|
| Piper TTS Manager (PTTSM) | HOCH | UEBERNEHMEN — hochwertige TTS-Alternative fuer Linux |
| TTS-Landschaft Ueberblick | MITTEL | KURZ HALTEN — kurze Matrix am Ende der Seite |
| X-Plane Built-in ATC | GERING | WEGLASSEN — plattformunabhaengig, kein Linux-Spezifikum |

**Redaktionelle Entscheidung:** Die XLinSpeak-Seite kann um einen Abschnitt "Alternative: Piper TTS Manager" ergaenzt werden. Piper TTS Manager laeuft unter Linux und bietet deutlich hoehere Sprachqualitaet — das ist ein relevanter Linux-Tipp. Eine kompakte Erwaehnung (3-5 Absaetze) genuegt, da PTTSM noch Pre-Release ist.

**Alternative:** Eigene Seite fuer PTTSM, wenn das Projekt stabiler wird. Aktuell ist eine Erwaehnung in xlinspeak.md ausreichend.

---

## Zusammenfassung: Empfohlene Aktionen

| Prioritaet | Aktion | Aufwand |
|---|---|---|
| 1 | **Neue Seite: Xchecklist** (`addon/cockpit/xchecklist.md`) | Mittel |
| 2 | **Neue Seite: OpenTrack** (`addon/cockpit/opentrack.md`) | Mittel |
| 3 | **Ergaenzung: XLinSpeak** um Piper TTS Manager | Gering |
| 4 | Querverweis linuxtrack.md → opentrack.md | Gering |
| — | XP Walkaround, Copilot-Plugins: Fuer spaetere Plugin-Uebersicht vormerken | — |
| — | My FS Flights: Keine Aenderung | — |

---

## Offene Fragen

1. **XFirstOfficer Linux-Support:** Nicht verifiziert. Bei Gelegenheit testen oder im Forum nachfragen.
2. **Piper TTS Manager Stabilitaet:** Pre-Release. Bei naechstem Audit erneut pruefen.
3. **SimpleWalkaround Linux-Support:** Nicht bestaetigt. Geringer Mehrwert fuer Dokumentation.
