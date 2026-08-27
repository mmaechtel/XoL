---
title: "KVM, Wine, Docker: Linux-Werkzeuge"
description: "Linux-Hilfsprogramme für X-Plane: KVM für Windows-VMs, Wine für Installer, Docker-Container, pyenv für Python-Plugins und zsh-Shell-Setup."
---
# Hilfsprogramme

Nicht jedes X-Plane-Tool läuft nativ unter Linux, und nicht jede Linux-Voreinstellung passt zu einem Simulator-Arbeitsplatz. Diese Sektion sammelt die Hilfsprogramme, die diese Lücken schließen — von der vollständigen Windows-Virtualisierung bis zur Shell-Konfiguration.

[KVM](kvm.md) stellt eine komplette Windows-VM unter Debian mit USB-Passthrough bereit — der Weg für Addons wie StreamDeck oder MobiFlight, die gar keinen Linux-Build haben; die Addon-Sektion [Via KVM](../../addon/kvm/index.md) baut darauf auf. [Wine](wine.md) ist die leichtere Option für einfachere Windows-Installer und Werkzeuge, inklusive 32-Bit-Unterstützung und Winetricks. [Docker](docker.md) isoliert Entwicklungs- und Testumgebungen von der Paketausstattung des Hosts. [pyenv](pyenv.md) verwaltet parallele Python-Versionen für Scripting und Plugin-Entwicklung, ohne das System-Python anzutasten. [zsh](zsh.md) rundet das Ganze mit einer komfortableren Shell für die tägliche Arbeit am System ab: Autovervollständigung, Syntax-Highlighting und Plugins.

Wer wegen eines reinen Windows-Addons hier ist, beginnt mit KVM; die übrigen Kapitel sind unabhängig und lassen sich nach Bedarf auswählen.

- **[KVM](kvm.md)** — Windows-Virtualisierung für Add-ons ohne native Linux-Unterstützung
- **[Docker](docker.md)** — Isolierte Entwicklungs- und Test-Umgebungen
- **[Wine](wine.md)** — Windows-basierte Tools und Installer
- **[pyenv](pyenv.md)** — Python-Umgebungen für Scripting und Plugins
- **[zsh](zsh.md)** — Leistungsfähige Shell-Konfiguration
