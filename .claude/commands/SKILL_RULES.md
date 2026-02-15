# Gemeinsame Skill-Regeln

Referenzdatei fuer wiederkehrende Ablaeufe in den Skills. Wird von einzelnen Skills per Verweis eingebunden statt dupliziert.

---

## Quellenstrategie

Primaerquellen in Reihenfolge der Zuverlaessigkeit:

1. **Offizielle Projektdokumentation** (kernel.org, mesa3d.org, developer.x-plane.com)
2. **GitHub-Repositories** (READMEs, Changelogs, Issues, Commit-Messages)
3. **Arch Wiki** (umfassendste Linux-Dokumentation)
4. **Debian-spezifisch** (wiki.debian.org, packages.debian.org, manpages.debian.org)
5. **Man-Pages** (man7.org)

**Nicht verwenden:** Foren-Posts, Drittanbieter-Blogposts, YouTube-Transkripte, ChatGPT-generierte Inhalte.

**Quellenaktualitaet:** Nur Quellen ab 2024 aufwaerts. Aeltere nur bei nachweislich stabiler Information (Kernel-Docs, POSIX-Standards).

---

## Behauptungen extrahieren

Aus der EN-Seite alle pruefbaren Aussagen identifizieren:

**Extrahieren:**

- Konkrete Befehle und ihre beschriebene Wirkung
- Konfigurationswerte und ihre behauptete Auswirkung
- Kausalaussagen ("X bewirkt Y", "weil Z")
- Kompatibilitaetsaussagen ("funktioniert mit/ohne Z")
- Vergleichsaussagen ("X ist schneller/besser als Y")
- Voraussetzungen und Abhaengigkeiten ("erfordert Paket X")

**Nicht pruefen:**

- Allgemeinwissen ("SSDs sind schneller als HDDs")
- Subjektive Wertungen ("fuehlt sich fluessiger an")
- Reine UI-Beschreibungen
- Ueberschriften, Einleitungssaetze ohne faktischen Gehalt
- Wiederholungen bereits anderswo gepruefter Aussagen

---

## Research-Papers laden

```
Glob: research/**/*<thema>*.md
```

Bestehende Research-Papers und Lektorate als Kontext laden. Nicht erneut recherchieren was bereits verifiziert wurde. AUDIT_* und FAKTENCHECK_* sind Pruefprotokolle — nur laden wenn deren Ergebnisse relevant sind, nicht als inhaltliche Quelle verwenden.

---

## Parallele Verifikation (Subagents)

Fuer thematische Gruppen von Behauptungen parallele Subagents starten (Task-Tool mit subagent_type=general-purpose):

- WebSearch fuer aktuelle Informationen
- WebFetch fuer freigegebene Domains (siehe `.claude/settings.local.json`)
- Jedes FAIL/WARN mit Direkt-Zitat aus der Quelle belegen
- Nicht verifizierbare Claims als N/V markieren

---

## EN first — DE nachziehen

1. Analyse und Korrekturen immer zuerst auf der EN-Seite durchfuehren (Quellen sind englisch)
2. Anschliessend die DE-Seite an die korrigierte EN-Version angleichen
3. Nicht 1:1 uebersetzen, sondern sinnerhaltend anpassen
4. Beide Seiten muessen inhaltlich identisch sein

---

## Versionsnummern bereinigen

Entscheidungsbaum aus `research/AUDIT_FLOW.md` anwenden:

- Harte Mindestanforderungen → behalten
- Verhaltens-Grenzen → behalten + Verifikationsbefehl
- Illustrative Versionen → entfernen oder Meta-Formulierung
- Tabellen mit Versionen → behalten

---

## Markdown-Check

`docs/MARKDOWN_RULES.txt` lesen und systematisch auf BEIDE Seiten (EN + DE) anwenden. Verstoesse automatisch korrigieren (keine Rueckfrage noetig).

---

## Build pruefen

```
Bash: mkdocs build
```

Bei Fehlern: Korrigieren und erneut bauen. Erst nach erfolgreichem Build weiter.
