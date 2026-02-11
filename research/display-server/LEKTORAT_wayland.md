# Lektorat: wayland.md — Display-Server für X-Plane

**Datum:** 2026-02-09
**Research-Paper:** `research/display-server/wayland_display_server.md`
**Zusätzliche Rohdaten:** `research/display-server/wayland_vs_x11.md`, `research/display-server/wayland_vs_x11_gaming.md`

---

## 1. Informationsbewertung

### 1.1 Empfehlung: X11 für X-Plane (Abschnitt ~15%)

| Kriterium | Bewertung |
|-----------|-----------|
| Relevanz | **Hoch** — zentrale Handlungsempfehlung |
| Mehrwert | **Hoch** — nicht offensichtlich, dass XWayland-Overhead existiert |
| Haltbarkeit | **Mittel** — kann sich mit SDL3-Migration ändern |
| Empfehlung | **Aufnehmen** — als klare Empfehlung am Seitenanfang |

**Begründung:** X-Plane 12.1.3 Release Notes bestätigen explizit: „Force X11 backend in GDK" — Laminar Research selbst umgeht Wayland. Dies ist die belastbarste Aussage der gesamten Recherche.

### 1.2 Wayland vs. X11 Architektur-Überblick (Abschnitt ~10%)

| Kriterium | Bewertung |
|-----------|-----------|
| Relevanz | **Mittel** — Kontext, aber nicht handlungsrelevant |
| Mehrwert | **Gering** — Architektur-Details sind anderswo besser dokumentiert |
| Haltbarkeit | **Hoch** — Grundlagen ändern sich nicht |
| Empfehlung | **Stark kürzen** — 3-4 Sätze, keine Protokoll-Details |

**Begründung:** Linux-erfahrene User kennen die Grundlagen. Nur das Delta erklären: warum verhält sich X-Plane unter Wayland anders als unter X11?

### 1.3 XWayland — Wie es funktioniert (Abschnitt ~10%)

| Kriterium | Bewertung |
|-----------|-----------|
| Relevanz | **Hoch** — erklärt warum X-Plane auf Wayland trotzdem läuft |
| Mehrwert | **Mittel** — „es gibt eine Kompatibilitätsschicht" ist bekannt |
| Haltbarkeit | **Hoch** |
| Empfehlung | **Aufnehmen, kurz** — Kernkonzept in 2-3 Sätzen |

### 1.4 Latenz-Messungen (Abschnitt ~15%)

| Kriterium | Bewertung |
|-----------|-----------|
| Relevanz | **Hoch** — quantifiziert den Unterschied |
| Mehrwert | **Sehr hoch** — Hardware-Messungen sind selten, belastbar |
| Haltbarkeit | **Mittel** — Zahlen können sich mit neuen Compositors ändern |
| Empfehlung | **Aufnehmen als Tabelle** — David Justo und Xaver Hugl |

**Hinweis:** Versionsspezifika (KWin 6.5.4, NVIDIA 580.119.02) in klappbaren Block.

### 1.5 GPU-spezifische Empfehlungen (Abschnitt ~20%)

| Kriterium | Bewertung |
|-----------|-----------|
| Relevanz | **Hoch** — AMD/NVIDIA/Intel haben völlig verschiedene Situationen |
| Mehrwert | **Hoch** — NVIDIA-Mindestanforderungen nicht trivial |
| Haltbarkeit | **Mittel** — Treiber-Versionen ändern sich |
| Empfehlung | **Aufnehmen als Entscheidungstabelle** |

**Versionsspezifika:** Treiber-Mindestversionen in Tabelle OK (Konvention). NVIDIA-Explicit-Sync-Geschichte in klappbaren Block.

### 1.6 Eingabegeräte (Abschnitt ~5%)

| Kriterium | Bewertung |
|-----------|-----------|
| Relevanz | **Hoch** — häufige Sorge bei Display-Server-Wechsel |
| Mehrwert | **Hoch** — „Joysticks sind vom Display-Server unabhängig" beruhigt |
| Haltbarkeit | **Sehr hoch** — Kernel-Interface ändert sich nicht |
| Empfehlung | **Aufnehmen** — kurzer Absatz, keine Codebeispiele nötig |

### 1.7 Session-Wechsel und Fallback (Abschnitt ~15%)

| Kriterium | Bewertung |
|-----------|-----------|
| Relevanz | **Sehr hoch** — konkrete Handlungsanleitung |
| Mehrwert | **Hoch** — Environment-Variables und Login-Screen-Optionen |
| Haltbarkeit | **Hoch** — GDM/SDDM-Methode stabil |
| Empfehlung | **Aufnehmen** — Schritt-für-Schritt |

### 1.8 Troubleshooting (Abschnitt ~10%)

| Kriterium | Bewertung |
|-----------|-----------|
| Relevanz | **Hoch** — Diagnose bei Problemen |
| Mehrwert | **Mittel** — einige Befehle sind generisch |
| Haltbarkeit | **Hoch** |
| Empfehlung | **Aufnehmen** — Szenario-Tabelle wie bei systemtools.md |

### 1.9 Nicht übernommen

| Thema | Grund |
|-------|-------|
| Wayland-Protokoll-Interna (Object IDs, Wire Format) | Zu technisch, kein Handlungsbezug |
| Gamescope als Gaming-Compositor | Eigenes Thema, zu speziell |
| Wine/Proton Wayland-Treiber | Nur relevant für Plugin-Seite (späteres Thema) |
| SDL3 fifo-v1 Protokoll-Details | Zu spezifisch, X-Plane nutzt SDL2 |
| VRR Multi-Monitor Edge Cases | Zu nischig, besser in systemtuning.md oder eigene Seite |
| Migration Path (4 Phasen) | Overengineered für Doku, User können selbst entscheiden |
| Compositor-Architektur-Vergleich (Mutter/KWin/wlroots Internals) | Kein Handlungsbezug |
| DRM Leasing | Nur VR-relevant |

---

## 2. Strukturvorschlag

### Leitprinzip

Die Seite muss **alle Szenarien für X-Plane durchspielen**, nicht nur die Empfehlung geben. Der Leser soll verstehen, was in seiner konkreten Situation passiert — drei Akteure (Wayland, X11, XWayland), drei Session-Typen, GPU-abhängige Unterschiede.

### Gliederung (H2/H3)

```
# Display-Server für X-Plane

## Drei Protokolle — was ist was?
(Wayland, X11, XWayland klar voneinander abgrenzen)

## Was passiert bei X-Plane?
### Szenario 1: X11-Session (empfohlen)
    Login-Screen → "GNOME on Xorg" / "Plasma (X11)"
    X-Plane → X11-Server → GPU → Monitor
    Desktop-Apps → X11-Server → GPU → Monitor
    Alles spricht X11. Kein Umweg, kein Übersetzer.
    + Kein Latenz-Overhead, bewährter Pfad
    + Fullscreen, Multi-Monitor, Identity-Login: alles funktioniert
    - Desktop-Features: kein per-Monitor-VRR, kein unabhängiger Refresh

### Szenario 2: Wayland-Session (Standard seit Debian 12/13)
    Login-Screen → "GNOME" / "Plasma" (Standard = Wayland)
    Desktop-Apps → Wayland-Compositor (nativ, direkt)
    X-Plane → kann kein Wayland → XWayland springt automatisch ein
    X-Plane → XWayland (X11-Server in Wayland) → Compositor → GPU
    + Desktop profitiert von Wayland (VRR, per-Monitor-Refresh, Sicherheit)
    - X-Plane hat XWayland-Overhead (~7ms Latenz, Extra-Kopie pro Frame)
    - Fullscreen-Multi-Monitor problematisch über XWayland
    - Identity-Login: intern auf X11 erzwungen (seit 12.1.3)
    - App kann bei Workspace-Wechsel pausieren

### Szenario 3: Wayland-Session + SDL_VIDEODRIVER=wayland
    Theoretisch: SDL2 versucht, X-Plane direkt auf Wayland zu starten
    Praxis: X-Plane hat kein natives Wayland-Backend
    → Ergebnis unvorhersehbar (Crash, Fallback, oder teilweise funktionierend)
    → Nicht empfohlen, nicht von Laminar getestet

## Latenz im Vergleich
(Tabellen: David Justo Hardware-Messung + Xaver Hugl Compositor-Messung)
(Zeigt messbar: X11 ≈ natives Wayland < XWayland)

## GPU-spezifische Situation
### AMD (RADV)
    Wayland ausgereift, kein Nachteil für Desktop
    X-Plane: trotzdem X11-Session empfohlen (wegen XWayland-Overhead)
    Aber: Wayland-Session funktioniert problemlos, Overhead gering
### NVIDIA
    Wayland erst mit Treiber 555+, Kernel 6.8+ stabil
    Ältere Treiber: X11-Session Pflicht (Explicit Sync fehlt)
    Aktuelle Treiber: Wayland-Session möglich, X-Plane über XWayland
### Intel Arc
    Intel empfiehlt Wayland (Xorg hat bekannte Glitches)
    X-Plane: trotzdem XWayland, aber Arc-spezifische X11-Probleme vermieden

## Session wählen — Schritt für Schritt
### Welche Session nutze ich gerade?
    echo $XDG_SESSION_TYPE
### X11-Session am Login-Screen wählen
    GDM: "GNOME on Xorg", SDDM: "Plasma (X11)"
### Dauerhaft X11 als Standard
    /etc/gdm3/daemon.conf → WaylandEnable=false
### Prüfen ob X-Plane über XWayland läuft
    xlsclients -l | grep -i plane

## Bekannte Probleme unter Wayland (Szenario 2)
(Szenario-Tabelle: Symptom → was passiert technisch → Lösung)

## Eingabegeräte
(Entwarnung: Joysticks/HOTAS umgehen den Display-Server komplett)
(Maus-Konfiguration: libinput vs. xinput — Unterschied erklären)

??? abstract "Hintergrund: Wie Wayland und X11 sich unterscheiden"
(Architektur-Diagramm: Rendering-Pfad, Compositor-Rolle)

??? abstract "Hintergrund: NVIDIA Explicit Sync"
(Timeline, warum NVIDIA Wayland erst spät konnte)

## Quellen
```

### Gewichtung

| Abschnitt | Anteil | Format |
|-----------|--------|--------|
| Drei Protokolle | 10% | Fließtext, klare Definitionen |
| Szenarien 1-3 | 25% | Jeweils Diagramm-artig: Pfad + Pro/Contra |
| Latenz-Vergleich | 10% | Tabellen |
| GPU-spezifisch | 15% | Tabelle + Admonitions per GPU |
| Session wählen | 15% | Code-Blöcke, Schritte |
| Probleme (Szenario 2) | 10% | Szenario-Tabelle |
| Eingabegeräte | 5% | Fließtext |
| Hintergrund (klappbar) | 10% | Klappbare Blöcke |

### Tonalität

- **Didaktisch:** Erst erklären was passiert, dann empfehlen
- Nicht „Wayland ist schlecht" — sondern „X-Plane kann kein natives Wayland, deshalb gibt es einen Umweg"
- Alle drei Szenarien ehrlich darstellen, auch wenn Szenario 3 „nicht empfohlen" ist
- GPU-Abschnitt differenziert: „X11-Session für X-Plane, unabhängig davon ob deine GPU Wayland gut kann"
- Zukunftsausblick ohne spekulative Versprechen

---

## 3. Versionsspezifische Inhalte

### Im Haupttext (Meta-Formulierungen)

- „X-Plane 12 hat derzeit keine native Wayland-Unterstützung" (statt „seit Version 12.1.3")
- „Aktuelle NVIDIA-Treiber unterstützen Wayland mit Explicit Sync" (statt „ab Treiber 555")
- „SDL2 bevorzugt X11 als Standard-Backend" (statt „seit Revert in SDL 2.0.22")

### In Tabellen (Mindestversionen OK)

| GPU | Mindestanforderung Wayland |
|-----|---------------------------|
| NVIDIA | Treiber 555+, Kernel 6.8+ |
| AMD | Mesa 22.0+ |
| Intel Arc | Kernel 6.2+ |

### In klappbaren Blöcken (Details erlaubt)

- NVIDIA Explicit Sync Timeline (555.42.02 beta → 555.58 stable → 560+)
- David Justo Messaufbau (KWin 6.5.4, NVIDIA 580.119.02, Dell AW2725DF 360Hz)
- Xaver Hugl Messbedingungen (120Hz Display)

---

## 4. Quellen-Qualität

### Tier 1 — Belastbar (für Faktencheck geeignet)

| Quelle | Bewertung |
|--------|-----------|
| X-Plane Release Notes | Offizielle Primärquelle, direkt zitierbar |
| NVIDIA README | Herstellerdokumentation, technisch korrekt |
| Arch Wiki | Peer-reviewed, aktuell, technisch präzise |
| Wayland Protocol Specs | Normativ |
| Debian Wiki | Distributionsspezifisch, korrekt |
| libinput Docs | Freedesktop, autoritativ |
| David Justo Hardware-Messung | Reproduzierbar, Methodik dokumentiert |

### Tier 2 — Zuverlässig

| Quelle | Bewertung |
|--------|-----------|
| Phoronix Benchmarks | Kontrolliert, reproduzierbar, etabliert |
| Xaver Hugl Blog | KDE-Kernentwickler, technisch fundiert |
| Mesa Docs | Offiziell, aber nicht immer aktuell |

### Tier 3 — Sekundär (nicht direkt zitieren)

| Quelle | Bewertung |
|--------|-----------|
| X-Plane Forums | Bug-Evidenz, nicht technisch belastbar |
| NVIDIA Developer Forums | Anekdotisch, aber nützlich für Problempatterns |
| Gaming-News (Phoronix News vs. Reviews) | News = Ankündigungen, Reviews = Daten |

### Markierungen für Faktencheck

- [ ] XWayland ~7ms Latenz-Overhead (David Justo) — reproduzierbar?
- [ ] NVIDIA Treiber 555+ als Mindestanforderung — noch aktuell in 2026?
- [ ] SDL2 X11-Default — hat sich das in neueren SDL2-Releases geändert?
- [ ] Intel „empfiehlt Wayland" — offizielle Intel-Aussage verifizieren
- [ ] GDM Fallback auf X11 bei NVIDIA — gilt das noch mit Treiber 580+?

---

## 5. Änderungen an bestehenden Seiten

### config.md (DE + EN)

**Stelle:** Abschnitt „Display Server" (Zeile 81-94 EN)
**Änderung:** Verweis auf neue wayland.md statt eigene Kurzfassung:

> X-Plane 12 hat keine native Wayland-Unterstützung. Für Details und Empfehlungen siehe [Display-Server](wayland.md).

Den bestehenden Tipp-Block und Workaround-Hinweis beibehalten, aber kürzen.

### nvidia.md (DE + EN)

**Stelle:** Abschnitt „Verbesserte Wayland-Unterstützung" (falls vorhanden)
**Änderung:** Querverweis auf wayland.md für Wayland-Spezifika

### glossary.md (DE + EN)

**Neue Einträge:**
- **Wayland** — Display-Server-Protokoll...
- **XWayland** — X11-Kompatibilitätsschicht für Wayland...
- **Display-Server** — Software, die Grafikausgabe und Eingabegeräte verwaltet...
- **Compositor** — Programm, das Fensterinhalte zu einem Bildschirmbild zusammensetzt...

### mkdocs.yml Navigation

**Position:** Linux > Optimierungen (nach systemtools.md, vor filesystem.md)

DE:
```yaml
- 'Display-Server': 'de/wayland.md'
```

EN:
```yaml
- 'Display Server': 'en/wayland.md'
```

---

## 6. Querverweise

| Von | Nach | Art |
|-----|------|-----|
| wayland.md | systemtuning.md | „Latenzquellen" in Tuning-Kontext |
| wayland.md | nvidia.md | GPU-Treiber-Anforderungen |
| config.md | wayland.md | Display-Server-Details |
| systemfehler.md | wayland.md | Fullscreen-Probleme unter Wayland |

---

## 7. Zusammenfassung

Die Seite `wayland.md` wird **pragmatisch und handlungsorientiert**: X-Plane 12 nutzt XWayland, X11-Session empfohlen, GPU-spezifische Differenzierung (AMD profitiert von Wayland, NVIDIA braucht aktuelle Treiber), konkrete Session-Wechsel-Anleitung, Szenario-Tabelle für Troubleshooting. Architektur-Details in klappbare Blöcke.

Geschätzte Seitenlänge: ~250-300 Zeilen (vergleichbar mit systemtools.md).
