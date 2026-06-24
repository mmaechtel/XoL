# Faktencheck: Alle Plugin-/Addon-Seiten (EN + DE)

**Datum:** 2026-06-24
**Geprüfte Seiten:** 45 Seiten unter `docs/en/addon/` (+ DE-Gegenstücke)
**Methode:** 10 parallele Verifikations-Subagents, je Kategorie, gegen Primärquellen (GitHub/GitLab-APIs, offizielle Projektseiten, x-plane.org-Forum/Gateway via WebSearch, Store-Seiten)
**Primärquellen verifiziert:** github.com, gitlab.com, forums.x-plane.org, x-plane.to, x-codrdesigns.com, twinfan.gitbook.io, xppython3.readthedocs.io, mobiflight.com, sayintentions.ai, myfs.flights, stickandrudderstudios.com, mangostudiossounds.com, 4xplane.nl, store.x-plane.org

---

## Gesamtbilanz

- **Geprüfte Behauptungen:** ~600 über 45 Seiten
- **FAIL:** 25 (auf 13 Seiten)
- **HALLUZINIERT:** 2
- **WARN:** ~20
- **N-V:** ~15 (meist Store-Seiten mit serverseitiger Bot-Sperre)
- **Saubere Seiten ohne Beanstandung:** 24 von 45

---

## Fehler (FAIL/HALLUZINIERT) — Korrekturbedarf

### Traffic / Ground Ops — größtes Cluster (AutoDGS-Deprecation)

**Kernfakt 2026:** AutoDGS ist **deprecated** und vollständig in **openSAM v5.x** (XP12-only) aufgegangen. README: „AutoDGS is deprecated and no longer supported. Use openSAM > v5.x" / „AutoDGS is now included in openSAM". Drei Seiten präsentieren beide noch als komplementäre, getrennt installierte, aktiv gepflegte Plugins → koordinierte Überarbeitung nötig.

1. **autodgs.md:15** — „AutoDGS is actively maintained with regular updates." → deprecated, Support nur Discord. Quelle: github.com/hotbso/AutoDGS
2. **autodgs.md:13** — „Compatibility: X-Plane 12" → README: „It works for XP11 and XP12" (Standalone). Aktuell: openSAM v5.x deckt XP12 ab, XP11 nur Legacy-4.x.
3. **autodgs.md:28** — „Both plugins can run in parallel … AutoDGS automatically skips airports with a sam.xml" → openSAM v5.x inkorporiert AutoDGS; Parallelbetrieb ist Legacy.
4. **autodgs.md:19** — „Activates after landing (beacon on, airtime required)" → README: aktiviert nach Landung, sucht Stände in Taxi-Richtung; „beacon on / airtime" ist openSAM-VDGS-Wording, nicht AutoDGS.
5. **opensam.md:13** — „Compatibility: X-Plane 11 and X-Plane 12 (separate builds)" → README: „This plugin runs on XP12 only. If you want to use it with XP11 stick to a 4.x release." v5.x = XP12-only.
6. **opensam.md:30** — „Combined with AutoDGS … full coverage" → openSAM v5.x deckt Default- + Custom-Airports selbst ab; separates AutoDGS überflüssig auf XP12.
7. **autogate.md:24** — „Jetway docks on beacon off (within 0.5 m)" → README: dockt bei **Triebwerks-Shutdown** („shuts down the plane's engines with the plane within ½m"), nicht Beacon-off. Quelle: github.com/hotbso/AutoGate
8. **autogate.md:13 [HALLUZINIERT]** — „Platforms: Windows, macOS, Linux (native binaries)" → hotbso-Fork baut nur Windows (Makefile.mgw64) + Linux (Makefile.lin64); **kein macOS** für den XP12-Fork.
9. **livetraffic.md:33-34** — Freie Kanäle unvollständig: **Airplanes.live** (frei, anonym, default-on) fehlt komplett. Quelle: twinfan.gitbook.io/livetraffic/introduction/features/channels
10. **livetraffic.md:44** — Kanal-Tabelle vermisst **SayIntentions** und **AutoATC** (beide frei, virtueller Traffic).
11. **livetraffic.md:45 [HALLUZINIERT]** — „FSCharter v2 | Free | Virtual traffic network" → erfordert registrierten FSCharter-Account; „Free" ohne Qualifikation irreführend, „v2"-Label unpräzise.

### Scenery Plugins

12. **xa-snow.md:11** — „LGPL-2.1" → LICENSE-Datei ist **GPL-3.0** (GitHub-API spdx_id „GPL-3.0"; libspng-Komponente zusätzlich BSD-2-Clause). Quelle: github.com/hotbso/xa-snow
13. **noaa_weather.md:13** — „X-Plane 12.1.2+" → README: „X-Plane **12.4 and above** (not tested with previous versions)". 12.1 nur Fallback für alte XPPython3-Nutzer.
14. **aep.md:13** — „Compatibility: X-Plane 12" → Einzelkauf deckt **XP11 und XP12** ab. Store: „both X-Plane 12 and X-Plane 11 included in a single purchase".

### Tools

15. **winctrl.md:47** — `ATTRS{idVendor}=="1002"` → Winwing-USB-HID-Vendor-ID ist **4098**, nicht 1002 (1002 = AMD/ATI PCI-Vendor). Die Beispiel-udev-Regel **funktioniert so nicht**. README nutzt durchgängig `4098`. Quelle: github.com/rswilem/winctrl-xplane-plugin
16. **xgs.md:46** — Forum-URL `…/file/48018-landing-speed-plugin-reloaded/` ist falsch → korrekt ist **file 45734** (`…/45734-landing-speed-plugin-xgs-reloaded/`). 48018 passt nicht zum Plugin.
17. **xorganizer.md (Seite gesamt)** — Fehlt der zentrale Linux-Fakt: XOrganizer ist **Windows-only .NET/WPF, kein nativer Linux-Support**, unter Wine praktisch unbrauchbar (WPF-Rendering scheitert; schreibt Windows-Backslash-Pfade in `scenery_packs.ini`, die X-Plane/Linux nicht erkennt). Seite präsentiert es als problemlos nutzbar. Quelle: research/addons/XOrganizer_Wine_Linux.md (Forum 172160)
18. **xorganizer.md:11-13** — „After purchase, the download link will be provided" → laut 4xplane.nl/research-note Donationware/frei mit optionaler Spende, kein Pflichtkauf.
19. **xorganizer.md:62** — „Automatic Updates: Regular updates" → kein belegter In-App-Auto-Update; Updates sind manuelle Downloads.
20. **xorganizer.md:80** — Forum-URL `…/forum/456-xorganizer/` nicht verifizierbar (wahrscheinlich erfundene Sub-Forum-ID). Korrekt: offizieller Kanal 4xplane.nl oder verifizierte Topics (327186, 332419).

### Scripting

21. **flywithlua.md:10** — „Developer: X-Friese (Florian Schmid)" → X-Friese ist **Carsten Lynker** (GitHub-Profil; Threshold-Abschiedsartikel; MIT-Header „Copyright (c) 2012 Carsten Lynker"). „Florian Schmid" ist erfunden. sparker256 = William Good ist korrekt.

### Cockpit

22. **avitab.md:15** — „The repository is not archived" → Repo `fpw/avitab` ist **archiviert** (GitHub-API `archived: true`, read-only seit ~April 2026); Wartung → `TeamAvitab/avitab`.

### ToLiss

23. **dk_toliss_callout.md:10** — „Developer: cxn0026" → Datei 91367 ist von **DINKIssTyle** (Profil 599292). cxn0026 ist Autor des separaten Cabin-Ready-Skripts (91876).
24. **toliss_ecosystem.md:78** — gleiche falsche Attribution (cxn0026 → **DINKIssTyle**).

---

## Nuancen (WARN) — verbesserbar, aber akzeptabel

- **linuxtrack.md:12,16** — Fork inzwischen **v2.0.1 (Juni 2026, Qt6-Rearchitektur in v2.0.0)**; „v0.99.29 / Qt5/Qt6"-Wording veraltet; kanonisch jetzt GitLab (gitlab.com/fwfa123/linuxtrackx-ir), GitHub nur Mirror.
- **autodgs.md:11 / opensam.md:11 / autogate.md:22** — Lizenz gemischt: Code LGPL-2.1, Assets/VDGS CC-BY bzw. CC BY-NC-SA. Klarstellen (analog AutoGate-Seite).
- **followthegreens.md:13** — XP11/XP12-Support-Matrix („XP12 only für R2") ggf. veraltet; aktuelle FtG 4D unterstützt XP11+12 (XPPython3 4.5+).
- **xppython3.md:12** — Repo-Link `uglyDwarf/x-plane_plugins` ist Legacy-Port; aktuelle v4.x von Peter Buckner (xppython3.readthedocs.io). „(GPL)" nicht belegbar (License-API 404; Docs: „You should never distribute a copy").
- **xppython3.md:14** — „X-Plane 11" → präziser „X-Plane 11.50+ (legacy v3.1.5)".
- **winctrl.md:14** — „X-Plane 12" → README: „X-Plane 11 and X-Plane 12".
- **xgs.md:39** — `64/lin.xpl`-Pfad plausibel (hotbso-Konvention), Release-ZIP-Struktur nicht direkt inspizierbar.
- **simloadmanager.md:14** — SGES als „Dependency" gelistet, upstream nur optionale Integration → „Optional/Recommended".
- **xcamera.md:14** — 11.3 ist Mindestanforderung der 2.4er-Reihe (FAQ); optional klarstellen.
- **xchecklist.md:11** — GitHub-Release 1.27r1 (2017) hängt Forum-Version (1.53) hinterher; Seite nennt keine Version → ggf. Research-Notiz präzisieren.
- **xtextureextractor.md:13** — XP12-Support real, aber GitHub-README nennt nur XP11 (veraltet); keine Korrektur nötig.
- **lst.md:26** — „<5–10% frame rate impact" nicht durch Primärquelle belegt (X-Codr nennt nur „fast performance") → Zahl entfernen/ersetzen.
- **aep.md:44** — „2.1 GB download size" → Quellen nennen „ca. 2 GB", versionsabhängig.
- **noaa_weather.md:11** — „GPLv2" genauer „GPLv2 or later" (aus Datei-Headern, keine LICENSE-Datei).
- **toliss_ecosystem.md:118** — Windshield-Icing-Download zeigt auf generische Kategorie statt Datei 98503 (ZoraBa).
- **mobiflight.md:48 / myfs_flights.md:41 / sayintentions.md** — Autor-eigene „erfolgreich in KVM getestet"-/IP-Konfig-Aussagen, plausibel aber nicht extern belegbar.
- **livetraffic.md:43** — ADSBHub „free for active data feeders" präzisieren.

---

## N-V — nicht (extern) verifizierbar

- **avitab.md:88** — MuPDF-1.26.11-Workaround widerspricht Research-Note („kein Workaround bekannt"); Versionsnummer unbelegt → prüfen oder entfernen.
- **avitab.md:86** — „Bookworm (lcms2 2.14) not affected" ungetestet → „likely not affected".
- **kabinxp.md / terrainradar.md** — Linux-`lin.xpl`-Präsenz nicht aus login-freier Quelle bestätigt (Seiten sind ehrlich gehedged).
- **kosp_project.md:12 / mango_studios.md:19-25** — exakte Versionsnummern/Preise (Store-Seiten serverseitig gesperrt).
- **winctrl.md:24** — ToLiss-Self-Test-Emulation nicht aus README belegbar.

---

## Korrekt (Auswahl) — keine Änderung nötig

24 von 45 Seiten ohne Beanstandung, u. a.: alle 7 FlyLua-Skripte (außer SLM-WARN), opentrack, xpwalkaround, betterpushback, xroad, datareftool, littlexpconnect, skunkcrafts_updater, xlinspeak (bereits 2026-02-20 gefaktencheckt), toicabrdy, toliss_mods, kosp/mango (Inhalt korrekt, nur Versionen N-V).

---

## Hinweis: veraltete Versionen in Research-Notizen (kein Seitenfehler)

- `BetterPushback_Linux.md`: V1.11 → upstream jetzt V1.13 (2026-05-26)
- SimLoad Manager: v3.7 → upstream V4.0 (2026-06-18)
- MobiFlight: 10.5.3 → upstream v11.1 (Mai 2026)

Seiten selbst nennen keine Versionsnummern → nicht betroffen.
