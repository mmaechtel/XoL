---
description: Installierte X-Plane-Plugins und -Skripte auf neuere Versionen prüfen und die Bezugsquellen in XoL gegenprüfen
disable-model-invocation: true
---

# Plugin-Check

Führt den Check nach `research/PLUGIN_CHECK.md` aus. Dort stehen Bestand, Quellen, Wege zur
neuesten Version und das Ergebnisformat; diese Datei regelt nur den Ablauf mit Claude.

## Argumente

`$ARGUMENTS`: optional das X-Plane-Verzeichnis. Ohne Argument `~/X-Plane-12`, sonst nachfragen.

## Ablauf

1. `research/PLUGIN_CHECK.md` lesen.
2. **Bestand** selbst aufnehmen (Schritt 1), read-only: nur `Resources/plugins`, ohne Flugzeuge
   und ohne vom Skunkcrafts Updater gepflegte Einträge. Die Liste dem Nutzer kurz zeigen.
3. **Quellen und neueste Versionen** (Schritte 2 und 3) nach `~/.claude/modell-strategie.md`
   verteilen: je Ausschnitt ein `rechercheur`, z. B. GitHub-Einträge, X-Plane.org-Einträge,
   Payware. Für X-Plane.org den Browser, in dem der Nutzer angemeldet ist
   (`list_connected_browsers`; bei mehreren fragen). Jede Angabe eines Rechercheurs mit Quelle;
   „Update verfügbar“ und „eingestellt“ selbst nachprüfen, bevor sie in die Tabelle kommen.
4. **Ergebnis** nach Schritt 4 schreiben und dem Nutzer die aktiven Einträge mit Update nennen.
5. Nichts installieren, ersetzen oder löschen und XoL nicht ändern, ohne dass der Nutzer es
   freigibt.
