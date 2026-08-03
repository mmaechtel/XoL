# Faktencheck Bereich 5 — docs/en/scenery/ortho_streaming/xpme.md

Prüfdatum: 2026-08-03. Alle Belege am 2026-08-03 abgerufen.

Nicht nutzbar (wie vorgegeben): forums.x-plane.org (403). Nicht benötigt.
Zusatzbefund zur Methodik: `www.aiflygo.com/docs/license/` wurde zunächst per WebFetch
zusammengefasst; die Zusammenfassung enthielt ein Zitat zur 7-Tage-Rückgabe, das im
Rohtext der Seite **nicht existiert** (siehe B5-06). Alle Belege unten stammen daher aus
dem gegrepten Roh-HTML, nicht aus Modell-Zusammenfassungen.

---

## B5-01 Preise 5 $ / 40 $
Behauptung (Z. 13): "The order form at `k.aiflygo.com/purchase` prices the X-Plane 12 license at **$5 for 30 days** and **$40 for 365 days**. The form builds its price display dynamically, so confirm the current figures there before paying."
Urteil: BESTÄTIGT
Beleg: https://k.aiflygo.com/build/_shared/chunk-AMV4J3FB.js — `XP30:{price:"$5",buymeacoffee:"https://buymeacoffee.com/derekhe/e/249495"}` und `XP365:{price:"$40",buymeacoffee:"https://www.buymeacoffee.com/derekhe/e/222691"}` (Stand: 2026-08-03)
Ergänzend, dass die Anzeige tatsächlich dynamisch ist: https://k.aiflygo.com/build/routes/purchase-3FUJ4CI4.js — `(0,e.jsx)("div",{className:"order-option-price",children:l&&C[`${l}30`]?.price})` (Stand: 2026-08-03). Das statische HTML von https://k.aiflygo.com/purchase (9.537 Bytes) enthält keine einzige Geldbetrags-Zeichenkette; sichtbar sind nur die Optionen "30 Days Short term use" und "365 Days (1 Year) Long term use, better value".
Belegstärke: **nur JavaScript/API** — die Beträge sind weiterhin NICHT als sichtbarer Seitentext belegbar, exakt wie in der früheren Recherche. Die Zahlen selbst sind unverändert korrekt.
Tragweite: hoch
Vorschlag: keine Änderung. Die Formulierung "The form builds its price display dynamically, so confirm the current figures there before paying" ist die sachlich richtige Absicherung und sollte unbedingt stehen bleiben. Optional präzisierend: Der MSFS-Jahrespreis liegt bei $30 (`MSFS365:{price:"$30"}`), der X-Plane-Jahrespreis bei $40 — die Seite nennt korrekt den X-Plane-Wert.

## B5-02 Keine dauerhafte Lizenz
Behauptung (Z. 13): "There is no perpetual license."
Urteil: BESTÄTIGT
Beleg: https://k.aiflygo.com/purchase — sichtbarer Formulartext: "License Duration: 30 Days Short term use 365 Days (1 Year) Long term use, better value" (Stand: 2026-08-03). https://www.aiflygo.com/docs/license/ — "If the time has expired, you can purchase it again." (Stand: 2026-08-03)
Belegstärke: sichtbarer Seitentext (Umkehrschluss: nur zwei befristete Optionen angeboten, kein Lifetime-Produkt)
Tragweite: hoch
Vorschlag: keine Änderung.

## B5-03 Eine Lizenz pro PC, Hardwarebindung
Behauptung (Z. 15): "One license is valid for exactly one PC and is bound to the hardware — changing the CPU or disk, or reinstalling the system, can invalidate it."
Urteil: BESTÄTIGT, aber unvollständig
Beleg: https://www.aiflygo.com/docs/license/ — "Replacing the CPU hard disk, reinstalling the system, etc. may cause the license to be invalid. **You can use your username and email to relink to the new device.**" sowie "A device can only be linked to one device, if you use it elsewhere, the previous authorization will be invalidated." und "No, you can't use the license on multiple devices. If you need to use it on different computers, please use different usernames for differnt computers." (Stand: 2026-08-03). Zusätzlich https://k.aiflygo.com/purchase, sichtbar: "One license can only be used by one pc. If you are purchasing for multiple devices, please enter different usernames" (Stand: 2026-08-03)
Belegstärke: sichtbarer Seitentext
Tragweite: hoch (Kaufentscheidung)
Vorschlag: Den Halbsatz zur Wiederverknüpfung ergänzen, sonst liest sich der Warnkasten dramatischer als die Lizenzlage. Etwa: "…changing the CPU or disk, or reinstalling the system, can invalidate it; the vendor documents that the license can be re-linked to the new device with the same username and email." Ebenfalls erwähnenswert, weil es eine echte Falle ist: "If you link machine A and use it on machine B, then machine A will be added to the blacklist and cannot use the authorization again."

## B5-04 Kommerzielle Nutzung untersagt
Behauptung (Z. 15): "Commercial use is explicitly prohibited: flight schools, training centers, any for-profit operation."
Urteil: BESTÄTIGT (mit Paraphrase-Abweichung)
Beleg: https://k.aiflygo.com/purchase — "Non-commercial Use Only: This software is licensed for personal, non-commercial use only. Any commercial use, including but not limited to use in flight training centers, commercial flight operations, or any for-profit activities is strictly prohibited without explicit written permission." (Stand: 2026-08-03)
Belegstärke: sichtbarer Seitentext
Tragweite: mittel
Vorschlag: "flight schools" steht so nicht in der Quelle; der Anbieter nennt "flight training centers, commercial flight operations". Außerdem fehlt der Vorbehalt "without explicit written permission". Ersatz: "Commercial use is prohibited without explicit written permission — the vendor names flight training centers, commercial flight operations, and any for-profit activity."

## B5-05 Zahlung über PayPal oder Buy Me a Coffee
Behauptung (Z. 15): "Payment runs through PayPal or Buy Me a Coffee"
Urteil: BESTÄTIGT
Beleg: https://k.aiflygo.com/purchase — sichtbarer Formulartext: "Payment Method: PayPal BuyMeACoffee" (Stand: 2026-08-03); zusätzlich BuyMeACoffee-Produkt-URLs in chunk-AMV4J3FB.js
Belegstärke: sichtbarer Seitentext
Tragweite: niedrig
Vorschlag: keine Änderung.

## B5-06 7 Tage Rückgabefrist — **WIDERRUFEN, der Befund war falsch**

!!! Korrektur 2026-08-04 (Gegenprüfung)

    Dieser Punkt ist widerlegt. Die Rückgabefrist steht wörtlich auf der Lizenzseite:
    `<h1 id="ask-for-refund">Ask for refund</h1>` … *„If you are not satisfied with the pro
    license, please tell me why and I will give you a refund. The refund period is 7 days after
    I sent out the license."* Nachgeprüft am 2026-08-04 per `curl` auf das Roh-HTML von
    <https://www.aiflygo.com/docs/license/> (HTTP 200, 32.181 Bytes, vier Treffer auf „refund"),
    zusätzlich bestätigt im Wayback-Snapshot vom 2025-11-26. Die untenstehende Volltextsuche muss
    also fehlgeschlagen sein — vermutlich wurde eine gerenderte oder gekürzte Fassung durchsucht.
    Der Abschnitt steht am **Ende** der Seite, hinter „Ask for help", und fehlt im
    Inhaltsverzeichnis, das unten zitiert wird.

    Der Fehler ist in `docs/{de,en}/scenery/ortho_streaming/xpme.md` eingebaut worden und dort
    am 2026-08-04 korrigiert. Lehre: Ein „kommt im Roh-HTML kein einziges Mal vor" braucht die
    Angabe, welche Datei durchsucht wurde und wie groß sie war.

### Ursprünglicher Befund (überholt)
Behauptung (Z. 15): "and the vendor states a 7-day refund window."
Urteil: UNBELEGBAR
Beleg: kein Beleg auffindbar. Das Wort "refund" kommt im Roh-HTML von https://www.aiflygo.com/docs/license/, https://k.aiflygo.com/purchase, https://www.aiflygo.com/docs/xplane-map-enhancement/{faq,download,usage}/ und https://www.aiflygo.com/docs/msfs-map-enhancement/faq/ **kein einziges Mal** vor (grep über die abgerufenen Dateien, Stand 2026-08-03). Die Inhaltsverzeichnisse der Lizenzseite lauten vollständig: "Purchase / How to use the license / When does license become invalid? / Error when Linking Device / Can I unlink my device…? / Can I use my license on multiple devices? / I changed my computer…" — kein Rückgabe-Abschnitt.
Das Einzige, was existiert, ist eine Kulanzzusage des Entwicklers im Issue-Tracker, ohne jede Frist: https://github.com/derekhe/xplane-map-enhancement-release/issues/296 — derekhe, 2025-12-19: "If you don't santisfied with this and I can offer you a refund, please email hesicong at gmail.com with your receipt." (Stand: 2026-08-03)
Belegstärke: keine (Gegenbeleg indirekt: Volltextsuche über alle Anbieterseiten)
Tragweite: **hoch** — das ist die kritischste Angabe der Seite. Wer im Vertrauen auf eine zugesicherte 7-Tage-Rückgabe kauft, hat keinen dokumentierten Anspruch. Mutmaßlicher Ursprung: eine frühere, per LLM zusammengefasste Abfrage der Lizenzseite; dieselbe Halluzination ("The refund period is 7 days after I sent out the license.") trat bei diesem Faktencheck erneut auf, ließ sich im Rohtext aber nicht wiederfinden.
Vorschlag: Aussage ersatzlos streichen. Falls ein Hinweis gewünscht ist, nur belegbar: "The vendor documents no refund policy; refunds have been granted informally on request via the issue tracker." Sicherer ist die Streichung plus der bereits vorhandene Satz "Please test the free versions and make sure it works before purchasing the pro version." (sichtbar auf k.aiflygo.com/purchase) als Ersatz-Absicherung.

## B5-07 Frei-gegen-Pro-Tabelle (Z. 41–49)
Behauptung: Kartenquellen ArcGIS/Bing/Google frei, weitere in Pro; Bildqualität nur "medium"; Farbanpassung, Vorabladen, hochauflösende Bodentexturen nur Pro; neue Funktionen zuerst Pro.
Urteil: BESTÄTIGT (alle sechs Zeilen wörtlich)
Beleg: https://www.aiflygo.com/docs/xplane-map-enhancement/faq/, Abschnitt "Differences Between Free and Professional Versions" — "The Free version provides access to ArcGIS, Bing, and Google Maps." / "The Professional version offers additional map sources with superior image quality and more frequent updates." / "The Free version is limited to medium image quality, while the Professional version supports high-quality settings." / "The Free version does not include map color adjustment capabilities." / "The Free version does not support the preloading feature." / "The Free version does not support high-resolution ground textures." / "New features and optimizations are typically introduced in the Professional version first." (Stand: 2026-08-03)
Belegstärke: sichtbarer Seitentext
Tragweite: mittel
Vorschlag: keine Änderung. Die Tabelle gibt die Quelle 1:1 wieder.

## B5-08 Vorabladen als Anbieter-Empfehlung gegen Unschärfe und Stottern
Behauptung (Z. 51): "**Preloading** is the vendor's own recommended remedy for the two most common complaints — blurry imagery and stuttering when tiles arrive late — and it is a Pro-only feature."
Urteil: BESTÄTIGT
Beleg: https://www.aiflygo.com/docs/xplane-map-enhancement/faq/ — "Blurry Maps … Enable the 'Preload' feature in settings (Professional version only)." und "Occasional Stuttering During Gameplay … To mitigate these issues, it's strongly recommended to enable the 'Preload' feature, which caches map data in advance." (Stand: 2026-08-03)
Belegstärke: sichtbarer Seitentext
Tragweite: mittel
Vorschlag: keine Änderung.

## B5-09 Kartendaten-Copyright, Unterhaltungszweck
Behauptung (Z. 53): "copyright to the map data belongs to the map providers, and the vendor states the tool is for entertainment use only."
Urteil: BESTÄTIGT
Beleg: https://www.aiflygo.com/docs/license/ — "Map copyrights belong to the original map companies." und "Please note that MSFS/XP Map Enhancement Pro Version is intended for entertainment purposes only." (Stand: 2026-08-03)
Belegstärke: sichtbarer Seitentext
Tragweite: niedrig
Vorschlag: keine Änderung.

## B5-10 Mount-Layer WinFSP / FUSE-T / FUSE 3
Behauptung (Z. 19): "WinFSP on Windows, FUSE-T on macOS, and FUSE 3 on Linux."
Urteil: BESTÄTIGT
Beleg: https://www.aiflygo.com/docs/xplane-map-enhancement/download/ — "Linux users need to install FUSE3, aria2, and .NET 10.0 runtime and ASP.NET runtime." / "Install macfuse through homebrew or download from https://github.com/macos-fuse-t/fuse-t/releases — brew install macos-fuse-t/homebrew-cask/fuse-t" / Abschnittsüberschrift "winfsp-2.1.25156.msi (Optional) — During installation, this will be automatically installed." (Stand: 2026-08-03). FAQ-Abschnitt "WinFSP Mounting Errors (Windows)" bestätigt den Mount-Charakter: "Please check if the base package and X-Plane are on NTFS drives. Other file systems like exFAT are not supported for mounting."
Belegstärke: sichtbarer Seitentext
Tragweite: niedrig
Vorschlag: keine Änderung.

## B5-11 DDS-Konvertierung als Hauptquelle der CPU-Last
Behauptung (Z. 19): "the documentation names the DDS conversion as a main source of CPU load."
Urteil: BESTÄTIGT
Beleg: https://www.aiflygo.com/docs/xplane-map-enhancement/faq/, "Why is CPU Usage So High?" — "X-Plane 12 doesn't natively optimize for enhanced map processing, requiring the application to handle substantial image processing and DDS file operations. This naturally results in elevated CPU utilization." (Stand: 2026-08-03)
Belegstärke: sichtbarer Seitentext
Tragweite: niedrig
Vorschlag: keine Änderung.

## B5-12 Basispakete: Ortho4XP-Fork auf ZL16
Behauptung (Z. 21): "regional DSF/terrain data generated with a modified Ortho4XP fork at ZL16"
Urteil: BESTÄTIGT
Beleg: https://www.aiflygo.com/docs/xplane-map-enhancement/faq/, "How to fix terrain issues using Ortho4XP" — "The base package is built from Ortho4XP. … Use the modifed version of Ortho4XP to create the tiles. The modified version is available at: https://github.com/derekhe/Ortho4XP … Create a new Ortho4XP tile using the same zoom level (Z16) as the base package. … In the genereated tile, copy the files from 'Earth nav data' and overwrite the files in the base package." (Stand: 2026-08-03)
Belegstärke: sichtbarer Seitentext
Tragweite: mittel
Vorschlag: keine Änderung. (Der Beleg trägt auch die "DSF/terrain"-Formulierung — "Earth nav data" ist der DSF-Ordner.)

## B5-13 Basispakete: Cloudflare, kein Handbetrieb, Proxy/VPN
Behauptung (Z. 23 / Z. 101): "Base packages cannot be installed by hand. They are hosted on Cloudflare and pulled by the in-app downloader … Users behind restrictive networks are told to configure an HTTP proxy or a VPN."
Urteil: BESTÄTIGT
Beleg: https://www.aiflygo.com/docs/xplane-map-enhancement/download/ — "There is no manual installation of base packages. The base packages are hosted on cloudflare. If you have network issue downloading the base package, please try to setup a http proxy or use VPN to download the base package." (Stand: 2026-08-03)
Belegstärke: sichtbarer Seitentext
Tragweite: mittel
Vorschlag: keine Änderung.

## B5-14 aria2c als Transfer-Backend, sequenzielle Installation
Behauptung (Z. 23): "which uses `aria2c` as its transfer backend and installs the selected packages sequentially."
Urteil: teilweise UNBELEGBAR
Beleg (aria2 als Downloader): https://github.com/derekhe/xplane-map-enhancement-release/issues/552 — Titel "Africa Base Package download fails with aria2 total length mismatch" (Stand: 2026-08-03), plus die Abhängigkeit "Linux users need to install FUSE3, aria2, …" auf der Download-Seite. Das Binary heißt `aria2c`, aber der Anbieter schreibt durchgehend "aria2".
Beleg (sequenziell): **keiner**. Die Download-Seite kennt nur "Click the 'Downloader' icon, select the base package you wish to download, then click the 'Download' button or 'Batch install'". Über die Reihenfolge oder Parallelität der Installation steht nichts.
Belegstärke: aria2 = indirekt erschlossen (Issue-Tracker + Abhängigkeitsliste); "sequentially" = keine
Tragweite: mittel
Vorschlag: "sequentially" streichen oder auf das Belegbare zurücknehmen: "…pulled by the in-app downloader, which relies on `aria2`; the UI offers single downloads and a 'Batch install' for multiple regions."

## B5-15 Kartenquellen und Wechsel im Flug
Behauptung (Z. 25): "Map sources selectable in the interface are Bing, ArcGIS, Google, and Apple. Switching sources mid-flight is possible but does not take effect immediately — X-Plane has to reload the affected textures."
Urteil: BESTÄTIGT
Beleg: https://www.aiflygo.com/docs/xplane-map-enhancement/usage/ — "In the main interface, you can select different map providers such as Bing, ArcGIS, Google, and Apple." und "You can switch maps during the game, but the changes won't take effect immediately. X-Plane needs some time to load the latest images. If you want to see the changes instantly, you can try clearing the cache." (Stand: 2026-08-03)
Belegstärke: sichtbarer Seitentext
Tragweite: niedrig
Vorschlag: keine Änderung.

## B5-16 "Nicht dokumentiert": Cache-Architektur
Behauptung (Z. 29): "Settings expose a clearable image cache and the docs warn against slow storage, but there is no published description of cache tiers, sizing, or eviction."
Urteil: BESTÄTIGT (Stand unverändert)
Beleg: https://www.aiflygo.com/docs/xplane-map-enhancement/faq/ — "Clear the image cache in the mod settings to remove potentially corrupted cached images." und "Ensure the disk where the cache is stored is stable and has no bad sectors."; https://www.aiflygo.com/docs/xplane-map-enhancement/download/ — "Avoid using HDDs or external hard drives, as their slow read speeds may cause performance issues." Volltextsuche über FAQ, Download- und Usage-Seite ergibt keine Angabe zu Cache-Größe, -Stufen oder -Verdrängung. (Stand: 2026-08-03)
Belegstärke: sichtbarer Seitentext (Negativbefund durch Volltextprüfung)
Tragweite: niedrig
Vorschlag: keine Änderung.

## B5-17 "Nicht dokumentiert": Zoomstufen der Bilddaten
Behauptung (Z. 30): "ZL16 refers to the mesh in the base packages. No zoom level is published for the streamed imagery in either tier."
Urteil: BESTÄTIGT
Beleg: Die einzige ZL-Angabe der gesamten Anbieterdoku ist "the same zoom level (Z16) as the base package" (FAQ, Ortho4XP-Abschnitt). Für die gestreamten Bilddaten existieren nur qualitative Stufen: "Try switching ground texture resolution to 'Normal'" (FAQ, "Blurry Maps") — ohne Zahlenwert. (Stand: 2026-08-03)
Belegstärke: sichtbarer Seitentext (Negativbefund)
Tragweite: niedrig
Vorschlag: keine Änderung. Optional könnte die Seite erwähnen, dass es eine benannte Einstellung "ground texture resolution" mit der Stufe "Normal" gibt — das ist der einzige greifbare Anhaltspunkt.

## B5-18 "Nicht dokumentiert": Bedeutung von "high-resolution ground textures"
Behauptung (Z. 31): "The Pro feature is described in marketing terms only; no resolution, no zoom level, no figures."
Urteil: BESTÄTIGT
Beleg: Die einzigen Fundstellen sind "The Free version does not support high-resolution ground textures." (FAQ) und "Note that the preload feature may cause particularly high CPU usage when high-resolution ground textures are enabled." (FAQ) — beide ohne jede Kennzahl. (Stand: 2026-08-03)
Belegstärke: sichtbarer Seitentext (Negativbefund)
Tragweite: niedrig
Vorschlag: keine Änderung.

## B5-19 Systemvoraussetzungen: .NET 10 / ASP.NET Core 10, aria2, FUSE 3
Behauptung (Z. 59–62): "Linux x86_64 with FUSE 3" / ".NET 10 runtime and ASP.NET Core 10 runtime" / "`aria2`"
Urteil: BESTÄTIGT
Beleg: https://www.aiflygo.com/docs/xplane-map-enhancement/download/ — "Linux users need to install FUSE3, aria2, and .NET 10.0 runtime and ASP.NET runtime." (Stand: 2026-08-03). FAQ: "please manually install the .NET 10 runtime and ASP.NET 10 runtime." Das `_amd64.deb`-Asset im Release-Repo belegt x86_64.
Belegstärke: sichtbarer Seitentext
Tragweite: mittel
Vorschlag: keine Änderung. (Kleinigkeit: Der Anbieter schreibt "ASP.NET runtime"/"ASP.NET 10 runtime", das Paket heißt `aspnetcore-runtime-10.0` — "ASP.NET Core 10" der Seite ist korrekt hergeleitet.)

## B5-20 X-Plane 11 nicht offiziell unterstützt
Behauptung (Z. 60): "X-Plane 12 (X-Plane 11 works for some users but is not officially supported)"
Urteil: BESTÄTIGT
Beleg: https://www.aiflygo.com/docs/xplane-map-enhancement/faq/, "Is XP11 Supported?" — "While X-Plane 11 has been tested by some users and is compatible with this enhancement, users may encounter various issues, particularly with loading speeds. For the best experience, X-Plane 12 is recommended. Please note that X-Plane 11 is not officially supported, and any issues encountered while using it may not be addressed in future updates." (Stand: 2026-08-03)
Belegstärke: sichtbarer Seitentext
Tragweite: niedrig
Vorschlag: keine Änderung.

## B5-21 SSD empfohlen, keine HDD/externen Laufwerke
Behauptung (Z. 63): "SSD for base packages and cache — the docs explicitly advise against HDDs and external drives"
Urteil: BESTÄTIGT
Beleg: https://www.aiflygo.com/docs/xplane-map-enhancement/download/ — "Avoid using HDDs or external hard drives, as their slow read speeds may cause performance issues." (Stand: 2026-08-03). FAQ ergänzend: "If you've installed the game, cache files, or base package on a slow storage device (such as a USB drive or HDD), move them to faster storage (SSD)."
Belegstärke: sichtbarer Seitentext
Tragweite: niedrig
Vorschlag: keine Änderung.

## B5-22 Rund 200 parallele Verbindungen als Vorgabe
Behauptung (Z. 64): "the client opens roughly 200 parallel connections by default"
Urteil: BESTÄTIGT
Beleg: https://www.aiflygo.com/docs/xplane-map-enhancement/faq/ — "Confirm that the number of concurrent connections is adequate; the default value of 200 is recommended." und "The application utilizes approximately 200 parallel loading threads. If your router cannot efficiently handle this load, try reducing the network loading threads value in settings (try 150, 100, or 50)…" (Stand: 2026-08-03). Auf Linux sichtbar in einem Fehlerbild: https://github.com/derekhe/xplane-map-enhancement-release/issues/557 — Titel "fuse: unknown option(s): '-o max_threads=200'Bug:" (Stand: 2026-08-03)
Belegstärke: sichtbarer Seitentext
Tragweite: niedrig
Vorschlag: keine Änderung.

## B5-23 "Memory Optimization" in den erweiterten Einstellungen
Behauptung (Z. 65): "the docs describe the tool as memory-intensive and offer a 'Memory Optimization' option in the advanced settings"
Urteil: BESTÄTIGT
Beleg: https://www.aiflygo.com/docs/xplane-map-enhancement/faq/ — "If you have limited available memory, you can enable the 'Memory Optimization' option in the 'Advanced Settings' to reduce memory usage and decrease the likelihood of crashes." und "Map enhancement consumes a lot of CPU and memory" (Stand: 2026-08-03)
Belegstärke: sichtbarer Seitentext
Tragweite: niedrig
Vorschlag: keine Änderung.

## B5-24 apt-Befehl
Behauptung (Z. 74): "sudo apt install libfuse3-dev aria2 dotnet-runtime-10.0 aspnetcore-runtime-10.0"
Urteil: BESTÄTIGT (wörtlich identisch)
Beleg: https://www.aiflygo.com/docs/xplane-map-enhancement/download/, Abschnitt "For Linux Users" — "For Debian-based systems: sudo apt install libfuse3-dev aria2 dotnet-runtime-10.0 aspnetcore-runtime-10.0" (Stand: 2026-08-03)
Belegstärke: sichtbarer Seitentext
Tragweite: mittel
Vorschlag: keine Änderung. Der Hinweis auf Z. 67 (Paket ggf. nicht in Debian stable) bleibt eine berechtigte redaktionelle Einordnung, keine Anbieterbehauptung.

## B5-25 Linux-Artefakte .AppImage und _amd64.deb
Behauptung (Z. 77): "Linux is served as an `.AppImage` and as a `_amd64.deb`"
Urteil: BESTÄTIGT
Beleg: https://api.github.com/repos/derekhe/xplane-map-enhancement-release/releases — Assets z. B. `xplane-map-enhancement-4.7.3.AppImage` und `xplane-map-enhancement_4.7.3_amd64.deb` (Stand: 2026-08-03). Die Dateinamensschemata der Codebeispiele auf Z. 81/84 stimmen exakt.
Belegstärke: nur API (GitHub Releases API; Assetnamen)
Tragweite: mittel
Vorschlag: keine Änderung.

## B5-26 "Nicht jedes Release bringt Linux-Dateien mit"
Behauptung (Z. 89): "Not every release ships Linux assets. Several releases contain only the Windows `.exe` and the macOS `.dmg`, including recent ones — the `.AppImage` and `.deb` appear in most releases but not reliably in the newest."
Urteil: BESTÄTIGT
Beleg: https://api.github.com/repos/derekhe/xplane-map-enhancement-release/releases?per_page=25 (Stand: 2026-08-03). Vollständige Auswertung der letzten 25 Releases:

| Release | Datum | Linux-Assets |
|---|---|---|
| 4.7.4 | 2026-07-19 | **NEIN** (nur .dmg + .exe) |
| 4.7.3 | 2026-07-15 | ja (AppImage + deb) |
| 4.7.2 | 2026-07-01 | ja (AppImage + deb; kein .dmg) |
| 4.7.1 | 2026-06-25 | ja |
| 4.7.0 | 2026-06-22 | ja |
| 4.6.2 | 2026-06-20 | **NEIN** (nur .dmg + .exe) |
| 4.6.1 | 2026-06-11 | ja |
| 4.6.0 | 2026-05-26 | ja |
| 4.5.0 | 2026-05-07 | **NEIN** (nur .dmg + .exe) |
| 4.4.4 | 2026-04-24 | ja |
| 4.4.3 | 2026-04-23 | **NEIN** (nur .exe) |
| 4.4.2 | 2026-04-11 | **NEIN** (nur .dmg + .exe) |
| 4.4.1 | 2026-04-10 | ja |
| 4.4.0 | 2026-04-06 | ja |
| 4.3.1 | 2026-03-18 | ja |
| 4.3.0 | 2026-03-14 | ja |
| 4.2.8 | 2026-03-07 | ja (kein .exe) |
| 4.2.7 | 2026-03-07 | ja (nur Linux) |
| 4.2.6 | 2026-02-26 | ja |
| 4.2.5 | 2026-02-08 | ja |
| 4.2.4 | 2026-02-07 | **NEIN** (nur .exe) |
| 4.2.3 | 2026-02-04 | ja |
| 4.2.2 | 2026-01-26 | **NEIN** (nur .dmg + .exe) |
| 4.2.1 | 2026-01-24 | **NEIN** (nur .exe) |
| 4.2.0 | 2026-01-21 | **NEIN** (nur .dmg + .exe) |

Bilanz: 16 von 25 Releases mit Linux-Assets, 9 ohne. Das **jüngste** Release (4.7.4) hat keine — die Formulierung "including recent ones … but not reliably in the newest" trifft exakt zu.
Belegstärke: nur API (GitHub Releases API — belastbar, da Primärquelle)
Tragweite: hoch (praktische Auswirkung auf Linux-Nutzer, Kernaussage des Warnkastens)
Vorschlag: keine Änderung. Der Warnkasten ist inhaltlich präzise und kommt ohne Versionsnummern aus, entspricht also der Repo-Regel.

## B5-27 Startreihenfolge und Beenden
Behauptung (Z. 91): "The application must be running and started before X-Plane so that the virtual filesystem is mounted; on exit the order is reversed — close X-Plane first, then press 'Stop' in XPME, otherwise the mount is not cleaned up properly."
Urteil: BESTÄTIGT (der Nachsatz leicht überdehnt)
Beleg: https://www.aiflygo.com/docs/xplane-map-enhancement/usage/ — "Before launching the game, open the X-Plane Map Enhancement application on your desktop." / "Once settings are configured, select your desired map … and click Start." / "To exit properly, you **must** close the game first, then click 'Stop' in the enhancement application." (Stand: 2026-08-03). Zur Bereinigung nur allgemein, im FAQ-Abschnitt "My XPlane Crashed": "In the Mod, click 'Start', wait a few seconds, then click 'Stop', and exit the Mod. This ensures that all operations performed by the Mod are completely cleaned up."
Belegstärke: sichtbarer Seitentext; die Begründung "otherwise the mount is not cleaned up properly" ist **indirekt erschlossen** — der Anbieter nennt keine Folge, sondern nur "To exit properly".
Tragweite: mittel
Vorschlag: Begründung entschärfen: "…close X-Plane first, then press 'Stop' in XPME; the vendor calls this the only proper exit path and states that it ensures all operations of the tool are cleaned up." Damit entfällt die nicht belegte Behauptung über den Einhängepunkt.

## B5-28 Szenerie-Konflikte Ortho4XP und HD Mesh Scenery
Behauptung (Z. 99): "Ortho4XP and X-Plane HD Mesh Scenery override XPME's base packages and are named as known conflicts"
Urteil: BESTÄTIGT
Beleg: https://www.aiflygo.com/docs/xplane-map-enhancement/faq/, "Game Images Not Loading, Still Showing Default Scenery" — "If you have Ortho4XP installed, you need to remove it because Ortho4XP will override the enhanced maps. … Currently known conflicting scenery plugins: Ortho4XP / X-Plane HD Mesh Scenery" (Stand: 2026-08-03)
Belegstärke: sichtbarer Seitentext
Tragweite: mittel
Vorschlag: keine Änderung. (Nuance, optional: Der Anbieter dokumentiert im FAQ-Abschnitt "How to fix terrain issues using Ortho4XP" durchaus einen Weg, selbst erzeugte Ortho4XP-Z16-Kacheln **in das Basispaket hineinzukopieren** — das ist kein Parallelbetrieb, aber es ist mehr als ein reines "must be removed". Ein Halbsatz dazu würde die Seite genauer machen.)

## B5-29 Vorabladen mit hochauflösenden Texturen kann die Leistung verschlechtern
Behauptung (Z. 100): "Preloading with high-resolution textures enabled is explicitly called out as capable of degrading simulator performance."
Urteil: BESTÄTIGT
Beleg: https://www.aiflygo.com/docs/xplane-map-enhancement/faq/, "High CPU Usage During Loading" — "Note that the preload feature may cause particularly high CPU usage when high-resolution ground textures are enabled. If you experience performance degradation in the simulator, consider temporarily disabling this feature." (Stand: 2026-08-03)
Belegstärke: sichtbarer Seitentext
Tragweite: mittel
Vorschlag: keine Änderung.

## B5-30 X-Plane 12 nicht für Textursubstitution optimiert
Behauptung (Z. 100): "The vendor states that X-Plane 12 is not optimized for this kind of texture substitution"
Urteil: BESTÄTIGT
Beleg: https://www.aiflygo.com/docs/xplane-map-enhancement/faq/ — "X-Plane 12 doesn't natively optimize for enhanced map processing, requiring the application to handle substantial image processing and DDS file operations." (Stand: 2026-08-03)
Belegstärke: sichtbarer Seitentext
Tragweite: niedrig
Vorschlag: keine Änderung.

## B5-31 Windows-zentrierte Dokumentation
Behauptung (Z. 98): "Setup guides, FAQ, and troubleshooting are written for Windows. WinFSP notes, NTFS requirements, antivirus exclusions, and page-file advice do not apply to Linux and have no documented Linux equivalents."
Urteil: BESTÄTIGT
Beleg: https://www.aiflygo.com/docs/xplane-map-enhancement/download/ — eigener Abschnitt "Setup antivirus software" mit "If you use microsoft defender, software will add the exclusion automatically" und "Kaspersky:" / "Norn VPN:"; FAQ: "Please check if the base package and X-Plane are on NTFS drives."; FAQ-Abschnitt "Windows 10 Related Issues" mit "Set-ProcessMitigation -Name XplaneMapEnhancement.exe -Disable UserShadowStack"; Usage: "If you have disabled the page file or set a size limitation for it, ensure you enable it and set it to be automatically managed by the operating system." Die einzigen Linux-Passagen der gesamten Doku sind der Vier-Zeilen-Abschnitt "For Linux Users" auf der Download-Seite. (Stand: 2026-08-03)
Belegstärke: sichtbarer Seitentext
Tragweite: niedrig
Vorschlag: keine Änderung.

## B5-32 "Keine unabhängigen Linux-Erfahrungsberichte überprüfbar"
Behauptung (Z. 102): "**No independent Linux experience reports were verifiable** for this page. The relevant community thread lives on a forum that blocks automated retrieval, so nothing here rests on it."
Urteil: FALSCH (in dieser Absolutheit)
Beleg: Der GitHub-Issue-Tracker des Release-Repos ist frei abrufbar und enthält mehrere unabhängige Linux-Berichte. Beispiele:
https://github.com/derekhe/xplane-map-enhancement-release/issues/471 (2026-05-30, "Bug: Error on exit on Linux (minor)") — "Thank you for offering XPME for Linux! Works great with one very minor issue on application shutdown … Running on latest ArchLinux." mit den Feldern "Operating System: Linux", "XPlane Map Enhancement Version: 4.6.0", "Base Package Version: 4.0.3".
https://github.com/derekhe/xplane-map-enhancement-release/issues/557 (2026-07-21) — "fuse: unknown option(s): '-o max_threads=200'".
Eine Volltextsuche `repo:derekhe/xplane-map-enhancement-release linux` liefert 20 Treffer. (Stand: 2026-08-03)
Belegstärke: nur API (GitHub Search/Issues API), Primärquelle, frei einsehbar
Tragweite: **mittel–hoch** — die Seite verzichtet auf eine belastbare, zugängliche Quelle und behauptet zugleich, es gebe keine.
Vorschlag: Ersetzen durch: "Community feedback on Linux is thin but not absent: the release repository's issue tracker carries Linux-tagged reports — a working setup on Arch Linux with a non-zero exit code on shutdown, and a FUSE mount failure over the `max_threads=200` option. The larger community thread lives on a forum that blocks automated retrieval and is not drawn on here." Alternativ die Aussage ganz streichen — belegbare Berichte existieren, also ist die Negativaussage nicht haltbar.

## B5-33 Vergleichstabelle: AutoOrtho-Lizenz "Open (GPL)"
Behauptung (Z. 110): "| Source code | Closed | **Open (GPL)** | Open |"
Urteil: FALSCH
Beleg: https://api.github.com/repos/kubilus1/autoortho — `"license": {"spdx_id": "Apache-2.0"}`; https://api.github.com/repos/ProgrammingDinosaur/autoortho4xplane — `"license": {"spdx_id": "Apache-2.0"}` (Stand: 2026-08-03). Beide AutoOrtho-Repos, Original wie aktiver Fork, stehen unter **Apache-2.0**, nicht unter GPL. Zum Vergleich XEarthLayer: https://api.github.com/repos/samsoir/xearthlayer — `"license": {"spdx_id": "MIT"}`.
Ergänzend: Weder `docs/en/scenery/ortho_streaming/autoortho.md` noch `xearthlayer.md` nennen überhaupt eine Lizenz (grep über beide Dateien: kein Treffer für "GPL"/"licen"). Die Angabe "GPL" stammt also aus keiner Stelle der eigenen Doku und ist zudem sachlich falsch.
Belegstärke: nur API (GitHub Repos API, SPDX-Feld — Primärquelle)
Tragweite: **hoch** — Lizenzaussage, falsch, und die einzige Stelle im Repo, an der eine Lizenz für AutoOrtho behauptet wird.
Vorschlag: Zeile ändern zu "| Source code | Closed | Open (Apache-2.0) | Open (MIT) |". Damit sind alle drei Spalten belegt.

## B5-34 Vergleichstabelle: übrige AutoOrtho- und XEarthLayer-Spalten
Behauptung (Z. 112–119): Platform, Mount layer, Terrain data, Map sources, Imagery zoom level, Cache, Configuration, Combinable with Ortho4XP tiles.
Urteil: BESTÄTIGT (konsistent mit der eigenen Doku)
Beleg (jeweils Repo-intern, Stand: Arbeitskopie 2026-08-03):
- Platform AutoOrtho "Windows, Linux, macOS (Apple Silicon)" — `docs/en/scenery/ortho_streaming/autoortho.md`, Z. 43: "running on Windows, Linux (with FUSE), or macOS (Apple Silicon)". XEarthLayer "Linux only" — `xearthlayer.md`, Z. 85: "XEarthLayer is currently only available for Linux. Windows and macOS support are not implemented."
- Mount layer FUSE — `xearthlayer.md`, Z. 22: "XEarthLayer uses a **FUSE-based virtual file system**"; `autoortho.md`, Z. 12: "AutoOrtho implements a FUSE-based streaming system".
- Map sources AutoOrtho "Bing, Google, Here, Yandex, Apple" — `autoortho.md`, Z. 69: "Map Provider: Choice between Bing, Google, Here, Yandex, and Apple Maps". XEarthLayer "Bing, Google, Apple, ArcGIS, MapBox, USGS" — `xearthlayer.md`, Z. 66–71, exakt diese sechs.
- Imagery zoom AutoOrtho "Up to ZL18" — `autoortho.md`, Z. 93: "| Max zoom level | Up to ZL18 | Up to ZL19 |" und Z. 12: "using zoom levels up to ZL18".
- Cache AutoOrtho "Configurable size, automatic eviction" — `autoortho.md`, Z. 70: "Cache Size: Maximum cache size in GB — when the limit is reached, older tiles are automatically removed". XEarthLayer "Three-tier, configurable" — `xearthlayer.md`, Z. 46–54.
- Terrain data XEarthLayer "DSF/TER packages via `xearthlayer packages install`" — `xearthlayer.md`, Z. 197: "Regional packages | Integrated CLI install (`xearthlayer packages install`)"; Terrain data AutoOrtho "Uses X-Plane scenery plus overlay downloads" — ebd. Z. 197: "Integrated overlay downloads".
- Configuration XEarthLayer "CLI plus `config.ini`" — `xearthlayer.md`, Z. 163: "Three settings in `~/.xearthlayer/config.ini`"; AutoOrtho "GUI" — `autoortho.md`, Z. 68–72 (Settings-Panel).
- Combinable with Ortho4XP tiles "Yes" für beide — `static_plus_streaming.md`, Z. 8: "Ortho4XP generates high-resolution, local tiles (up to ZL19) … while a streaming solution (e.g., AutoOrtho) handles global coverage" und Z. 28: "Ortho4XP tiles must be listed before the streaming entries so they take priority."
Belegstärke: sichtbarer Seitentext (repo-intern)
Tragweite: mittel
Vorschlag: keine Änderung. Einzige Randnotiz: "Imagery zoom level: Provider-dependent" für XEarthLayer steht so nicht in `xearthlayer.md` — dort ist gar keine Zoomstufe genannt. Die Angabe widerspricht nichts, ist aber nicht aus der eigenen Doku ableitbar; "Not documented" wäre exakter.

## B5-35 Zwei Simulatoren, eine Produktfamilie
Behauptung (Z. 8 / Z. 127): "XPME is one product family covering two simulators — Microsoft Flight Simulator and X-Plane." / "XPME is the only one of the three that covers both X-Plane and Microsoft Flight Simulator with one product family and one interface"
Urteil: BESTÄTIGT (erster Teil), teilweise UNBELEGBAR (Zusatz "one interface")
Beleg: https://k.aiflygo.com/purchase — sichtbar: "Product: Microsoft Flight Simulator 2020/24 X-Plane 12"; Doku-Navigation auf https://www.aiflygo.com/docs/xplane-map-enhancement/faq/ listet parallel "MSFS Map Enhancement" und "XPlane Map Enhancement"; die Disclaimer sprechen durchgehend von "MSFS/XP Map Enhancement Pro Version" (Stand: 2026-08-03). Separate Lizenzen und separate Downloads sind belegt (getrennte Preis-Keys `MSFS30/MSFS365` vs. `XP30/XP365`, getrenntes Release-Repo `xplane-map-enhancement-release`).
Belegstärke: sichtbarer Seitentext
Tragweite: niedrig
Vorschlag: "one interface" streichen — es sind zwei getrennte Anwendungen mit getrennten Lizenzen und getrennten Basispaketen; die Seite sagt das auf Z. 8 selbst ("its own documentation, its own base packages, and its own license"), Z. 127 widerspricht dem. Ersatz: "…covers both X-Plane and Microsoft Flight Simulator within one product family (separate applications and separate licenses), which is its clearest structural advantage."

## B5-36 Abschnitt "Sources" — alle sechs URLs
Behauptung (Z. 146–151): sechs Quell-URLs.
Urteil: BESTÄTIGT (alle sechs auflösbar), eine mit Einschränkung
Beleg (alle Stand: 2026-08-03):
1. https://github.com/derekhe/xplane-map-enhancement-release/releases — erreichbar, API liefert 25+ Releases. OK.
2. https://www.aiflygo.com/docs/xplane-map-enhancement/download/ — HTTP 200, 32.974 Bytes, Titel "Download and Installation | Map Enhancement". OK.
3. https://www.aiflygo.com/docs/xplane-map-enhancement/usage/ — HTTP 200, 28.614 Bytes, Titel "Software Usage and Configuration | Map Enhancement". OK.
4. https://www.aiflygo.com/docs/xplane-map-enhancement/faq/ — HTTP 200, 47.050 Bytes, Titel "FAQ Guide | Map Enhancement". OK.
5. https://www.aiflygo.com/docs/license/ — HTTP 200, Titel "License", Abschnitte "Purchase / How to use the license / When does license become invalid? / …". OK.
6. https://k.aiflygo.com/purchase — HTTP 200, 9.537 Bytes, Titel-Text "Purchase License". **Einschränkung:** liefert eine JavaScript-gerenderte Seite; ohne JS sind Produkt- und Dauerauswahl sichtbar, die **Preise nicht** (siehe B5-01). Als Beleg für Preise nur mit JS-Ausführung tauglich.
Belegstärke: sichtbarer Seitentext / HTTP-Status
Tragweite: niedrig
Vorschlag: keine Änderung an der Liste. Alle sechs sind offizielle Primärquellen und liegen innerhalb der 5–8er-Vorgabe.

---

## Bilanz

| Urteil | Anzahl |
|---|---|
| BESTÄTIGT | 30 (B5-01…05, 07…13, 15…31, 34…36) |
| FALSCH | 2 (B5-32, B5-33) |
| VERALTET | 0 |
| UNBELEGBAR | 2 (B5-06 vollständig, B5-14 teilweise) |
| davon BESTÄTIGT mit Korrekturvorschlag | 4 (B5-03, B5-04, B5-27, B5-35) |

Änderungsbedarf nach Dringlichkeit:
1. **B5-06** — "7-day refund window" streichen (nirgends belegt, Kaufentscheidungsrelevanz).
2. **B5-33** — AutoOrtho-Lizenz von "GPL" auf "Apache-2.0" korrigieren.
3. **B5-32** — Behauptung "no independent Linux experience reports were verifiable" korrigieren.
4. **B5-03** — Relink-Möglichkeit ergänzen; **B5-04** Zitattreue; **B5-14** "sequentially" streichen; **B5-27** Begründung entschärfen; **B5-35** "one interface" streichen.
