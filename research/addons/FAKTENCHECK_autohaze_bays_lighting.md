# Faktencheck: AutoHaze + Bay's Lighting Mod (EN + DE)

**Datum:** 2026-08-12
**Geprüfte Seiten:** `docs/{en,de}/addon/flylua_scripts/autohaze.md`, `docs/{en,de}/addon/scenery_addons/bays_lighting_mod.md`
**Primärquellen:** forums.x-plane.org/files/file/99665 (AutoHaze), forums.x-plane.org/files/file/97497 (Bay's Lighting Mod)

---

## Hinweis zur Quellenlage

x-plane.org blockiert WebFetch mit HTTP 403. Beide Seiten wurden über die Chrome-Automatisierung direkt gelesen, inklusive Kommentar-Threads (AutoHaze: 123 Kommentare / 17 Reviews, Bay's: 43 Kommentare). Jede Seite hat genau eine Primärquelle — Aussagen über das Zusammenspiel der beiden Addons sind daher **nicht belegbar** und stehen auf den Seiten nur als Hinweis auf die Überschneidung, nicht als Verträglichkeitszusage.

## AutoHaze — bestätigt

| # | Behauptung | Beleg |
|---|------------|-------|
| 1 | Entwickler MrBitsy | „By MrBitsy" |
| 2 | Rückfall auf Default-Turbidity oberhalb der METAR-Sichtgrenze | „whenever conditions are better than 10SM, X-Plane receives no useful visibility data at all and falls back to a default turbidity value" |
| 3 | Gleiche Trübung Mojave vs. Indo-Gangetic Plain, kein Höhenabfall | „the same murky appearance at 30,000ft as it does at circuit height" |
| 4 | CAMS = satellitengemessene AOD an der Position, stündlich | „satellite-measured aerosol optical depth at your exact position, updated hourly" |
| 5 | VisualCrossing / OpenWeatherMap für Bodenbedingungen | „real surface visibility, humidity, temperature, dew point and wind" |
| 6 | Open-Meteo Grenzschichthöhe skaliert die Trübung mit der Höhe | „the real atmospheric boundary layer height is used to scale turbidity with altitude" |
| 7 | Koschmieder- und Linke-Gleichungen statt Lookup-Tabelle | „uses the physically correct Koschmieder and Linke turbidity equations rather than an empirical lookup table" |
| 8 | Regenkopplung der Sicht | „Visibility is also affected by the amount of rain hitting your aircraft!" |
| 9 | Hintergrund-Helper ohne Konsolenblitz und Sim-Pause (ab 2.0) | „a silent background companion (AHHelper.exe) with no console window flash and no X-Plane pause" |
| 10 | Weiche Übergänge, persistente Settings | „Transitions … always gradual, never instant"; „Settings … are restored automatically on startup from the last manual save" |
| 11 | Tastenkürzel für das Fenster (2.3) | „setting a key combination in X-Plane/settings/Autohaze" |
| 12 | Linux/macOS ab 2.4, Entwickler besitzt keines von beiden | „Now compatible with the Mac and Linux - I do not own a Mac or have Linux … I would really appreciate feedback" |
| 13 | 2.4.1 sauberes Ablösen des Helpers von X-Plane | „improve Linux/macOS helper launch so it detaches cleanly from X-Plane" |
| 14 | 2.4.2 CA-Zertifikate gebündelt, ZIP-Paket wegen Dateinamen | „Rebuilt helper binaries with bundled CA certificates to fix SSL certificate errors on some Linux systems"; „distributed as a ZIP package to preserve the correct macOS/Linux helper filenames" |
| 15 | API-Schlüssel für Live-Modus | „Requires: … Free API keys for Live mode" |

## AutoHaze — bewusst nicht übernommen

- **„Freeware":** Die Seite führt kein Lizenzfeld. Auf der Doku-Seite steht deshalb „Kostenloser Download, Spendenlink auf der Download-Seite".
- **„scientifically accurate results across the full range":** Entwicklerbehauptung ohne Prüfmöglichkeit — die Doku nennt nur die verwendeten Gleichungen.
- **`SSL_CERT_FILE` / `SSL_CERT_DIR` / `certifi`-Reihenfolge:** aus dem Kommentar-Thread, widerspricht der Bezeichnung „Binary" und ist nicht in den Release Notes belegt. Nicht übernommen.
- **`AHHelper-linux.py` beim Einzeldownload:** ebenfalls nur aus Kommentaren. Die Doku nennt stattdessen den belegten Grund für das ZIP (Dateinamen bleiben erhalten).
- **Python-Anforderung unter Linux:** Die Quelle sagt „no additional software needed on **Windows 10+**" und trifft für Linux keine Aussage. Die Doku benennt diese Lücke ausdrücklich, statt sie zu füllen.

## Bay's Lighting Mod — bestätigt

| # | Behauptung | Beleg |
|---|------------|-------|
| 1 | Entwickler baylor703, Patreon | „If you would like to support me … patreon.com/c/TheWarsimmer" |
| 2 | Abhängigkeit FlyWithLua NG+ | „This mod requires FlywithLua NG+" (mit Link auf die NG+-Seite) |
| 3 | Nicht mit anderen Lighting-Mods kompatibel | „It is not compatible with other lighting mods" |
| 4 | Geänderte Flughafen-/Beacon-Lichter, Wolken/Streuung, Nacht-Sprites, Cockpit, Dämmerung, Sichtweite | Liste „Major Alterations" |
| 5 | Nav-/Beacon-Lichter am Flugzeug (2.40) | „Slightly modified airplane nav and beacon lights" |
| 6 | Installation: `Resources` überschreiben + `bays_lighting.lua` in Scripts | „Copy and paste the Resources folder … it will ask you to overwrite files" |
| 7 | Rückkehr zum Default möglich | „instructions are included in the download, with the default lighting included" |
| 8 | Ortho deaktiviert die entfernten Lichttexturen → harter Cutoff, mit und ohne Mod | „If you use ortho scenery, these ‚distant light textures' are disabled and will not work … Whether you are using this mod or not, that is how the mechanics of it work" |

## Bay's Lighting Mod — bewusst nicht übernommen

- **Plattformangabe:** Die Quelle nennt keine. Die Doku schreibt deshalb, dass keine Einschränkung angegeben ist, und leitet aus dem Paketinhalt (Texturen + Lua) ab.
- **„nearly seamlessly":** Die Quelle relativiert doppelt („nearly", „so long as you have ortho disabled"). Beide Vorbehalte stehen auf der Doku-Seite.
- **Sichtweiten-Spreizung:** Entwicklerbehauptung; ein Nutzerkommentar berichtet Gegenteiliges, allerdings mit einem zweiten Lighting-Mod parallel installiert (unsauberer Test). Auf der Seite als Entwickleraussage gekennzeichnet.
- **Linux-Bezüge:** In Beschreibung und 43 Kommentaren keine. Keine Linux-Notiz erfunden.

## Eigene Ergänzungen (nicht aus der Quelle)

- Backup-Hinweis vor dem Überschreiben in `Resources` und der Hinweis, dass ein X-Plane-Update den Mod entfernt — als Warnbox gekennzeichnet.
- `LIT_TEX`-Vorbehalt bei der Ortho-Erklärung, abgeglichen mit `docs/*/scenery/ortho_streaming/how_streaming_works.md`, damit sich die beiden Seiten nicht widersprechen.
