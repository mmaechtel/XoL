# Faktencheck: XLinSpeak (EN + DE)

**Datum:** 2026-02-20
**Geprüfte Seiten:** `docs/en/addon/tools/xlinspeak.md`, `docs/de/addon/tools/xlinspeak.md`
**Primärquellen verifiziert:** github.com (sparker256/XLinSpeak, uglyDwarf/x-plane_plugins, JT8D-17/Piper-TTS-Manager-for-X-Plane, OHF-Voice/piper1-gpl, rhasspy/piper), huggingface.co, packages.debian.org, developer.x-plane.com

---

## Korrigierte Fehler (2)

### 1. PTTSM Status "Active development"
**Datei:** `xlinspeak.md:58` (EN) / `xlinspeak.md:58` (DE)
**Behauptung:** "Active development (no versioned releases)"
**Befund:** Repo hat 8 Commits, alle vom 14. März 2024. Seitdem keine Aktivität.
**Korrektur:** Status auf "No versioned releases" / "Keine versionierten Releases" geändert.

### 2. Plattform-Bestätigung "Debian/Ubuntu 22.04 and Fedora 39"
**Datei:** `xlinspeak.md:69` (EN) / `xlinspeak.md:69` (DE)
**Behauptung:** "Confirmed working on Debian/Ubuntu 22.04 and Fedora 39"
**Befund:** README sagt Arch Linux, Fedora 39, Ubuntu 22.04 (kein Debian). Beide Plattformen veraltet (Fedora 39 EOL Nov 2024). Als FlyWithLua-Skript distributionsunabhängig.
**Korrektur:** Satz entfernt.

## Verbesserte Nuancen (2)

### 1. X-Plane ATC "pre-recorded" → "pre-generated"
**Datei:** `xlinspeak.md:16` (EN) / `xlinspeak.md:16` (DE)
**Befund:** X-Plane 12 ATC nutzt cloud-TTS-generierte Audio-Snippets (Amazon Polly SSML), keine Studioaufnahmen. "Pre-generated" ist präziser.
**Korrektur:** "pre-recorded" → "pre-generated" / "voraufgezeichnete" → "vorgenerierte"

### 2. Gleiche Anpassung in TTS-Vergleichstabelle
**Datei:** `xlinspeak.md:81` (EN) / `xlinspeak.md:81` (DE)
**Korrektur:** Tabelleneintrag ebenfalls auf "Pre-generated" / "Vorgenerierte" geändert.

## Korrekt (12) — keine Änderung nötig

| # | Behauptung | Quelle |
|---|------------|--------|
| 1 | XLinSpeak Entwickler uglyDwarf + sparker256 | GitHub Profile + Commit-Historie |
| 2 | Repository sparker256/XLinSpeak existiert | GitHub API — letzter Commit Feb 2023 |
| 3 | Original-Repo uglyDwarf existiert | GitHub — XLinSpeak-Verzeichnis vorhanden |
| 4 | Binary Hooking Mechanismus | Quellcode-Analyse: ELF-Symbol-Lookup + Code-Patching + NASM-Trampoline |
| 5 | Build-Deps: libspeechd-dev nasm gcc | Makefile bestätigt alle drei |
| 6 | Binary-Pfad XLinSpeak/lin_x64/XLinSpeak.xpl | GitHub Repo-Inhalt |
| 7 | XP12-Kompatibilität (sparker256 Fork) | README: SDK 400 Minimum |
| 8 | espeak-ng Backend zuverlässig | Debian-Pakete, Arch Wiki, keine Problemberichte |
| 9 | Piper als speech-dispatcher Backend unzuverlässig | GitHub Discussions #328, Issues #561 — Probleme bestätigt bis 2025 |
| 10 | PTTSM Entwickler JT8D-17, Lizenz EUPL-1.2 | GitHub Repo |
| 11 | OHF-Voice/piper1-gpl als Piper-Quelle | rhasspy/piper archiviert Okt 2025, Nachfolger bestätigt |
| 12 | Voice Models auf HuggingFace piper-voices | Repo aktiv, 35 Sprachen, MIT-Lizenz |
