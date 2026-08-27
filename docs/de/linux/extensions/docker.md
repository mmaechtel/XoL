---
title: Docker auf Debian installieren
description: "Docker-Installation auf Debian Schritt für Schritt: Repository-Einrichtung, Paketinstallation, Dienst-Konfiguration und rootless-Nutzung."
---
### [Docker](../../glossary.md#docker) unter Debian installieren: Eine Schritt-für-Schritt-Anleitung

[Docker](../../glossary.md#docker) ist eine weit verbreitete Plattform zur Containerisierung von Anwendungen, die Entwicklern und Administratoren hilft, Anwendungen effizient zu erstellen, bereitzustellen und zu verwalten. Dieses Kapitel erklärt, wie man Docker auf einem Debian-System installiert. Die Anleitung ist sachlich und praxisorientiert, sodass auch Einsteiger problemlos folgen können.

## Voraussetzungen

Voraussetzungen vor dem Start:

- Zugriff auf ein Debian-System
- Root- oder Sudo-Rechte

## Schritt 1: System aktualisieren

Zunächst sicherstellen, dass das Debian-System auf dem neuesten Stand ist. Ein Terminal öffnen und folgende Befehle ausführen:

```bash
sudo apt update
sudo apt upgrade -y
```

Dies aktualisiert die Paketlisten und installiert verfügbare Updates für bereits installierte Software.

## Schritt 2: Erforderliche Abhängigkeiten installieren

Docker benötigt einige grundlegende Pakete, um korrekt zu funktionieren. Installation mit:

```bash
sudo apt install -y apt-transport-https ca-certificates curl gnupg lsb-release
```

Diese Pakete ermöglichen den sicheren Download von Software und die Verwaltung von Repository-Schlüsseln.

## Schritt 3: Docker-Repository hinzufügen

Debian enthält zwar eine ältere Version von Docker im Standard-Repository, aber es ist empfehlenswert, das offizielle Docker-Repository zu verwenden, um die neueste Version zu erhalten. Dazu folgende Schritte:

1. **GPG-Schlüssel hinzufügen:**

   ```bash
   curl -fsSL https://download.docker.com/linux/debian/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
   ```

2. **Repository einrichten:**

   ```bash
   echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/debian $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
   ```

3. **Paketlisten aktualisieren:**
   ```bash
   sudo apt update
   ```

## Schritt 4: Docker installieren

Jetzt lässt sich Docker installieren. Folgenden Befehl ausführen, um die Hauptpakete zu installieren:

```bash
sudo apt install -y docker-ce docker-ce-cli containerd.io
```

- `docker-ce`: Die Docker-Engine selbst.
- `docker-ce-cli`: Die Kommandozeilen-Schnittstelle.
- `containerd.io`: Der Container-Runtime, der von Docker verwendet wird.

## Schritt 5: Docker-Dienst starten und aktivieren

Nach der Installation den Docker-Dienst starten und sicherstellen, dass er beim Systemstart automatisch läuft:

```bash
sudo systemctl start docker
sudo systemctl enable docker
```

## Schritt 6: Installation überprüfen

Um sicherzugehen, dass Docker korrekt installiert wurde, folgenden Befehl ausführen:

```bash
docker --version
```

Die Ausgabe sollte etwa `Docker version 20.10.x, build ...` (oder eine neuere Version) zeigen. Zusätzlich testen, ob Docker funktioniert, indem ein einfacher Container gestartet wird:

```bash
sudo docker run hello-world
```

Dieser Befehl lädt ein Test-Image herunter und führt es aus. Wenn alles korrekt läuft, erscheint eine Bestätigungsnachricht von Docker.

## Schritt 7: Docker ohne Root-Rechte nutzen (optional)

Standardmäßig erfordert Docker Root-Rechte. Um Docker als normaler Benutzer auszuführen, den eigenen Benutzer zur `docker`-Gruppe hinzufügen:

```bash
sudo usermod -aG docker $USER
```

Anschließend ab- und wieder anmelden (oder das Terminal neu starten), damit die Änderungen wirksam werden. Danach lassen sich Docker-Befehle ohne `sudo` ausführen.

## Fazit

Docker ist nun erfolgreich auf Debian installiert. Mit dieser Installation lassen sich Container erstellen, Images verwalten und Anwendungen in isolierten Umgebungen betreiben. Für weitere Anpassungen oder spezifische Konfigurationen bietet die [offizielle Docker-Dokumentation](https://docs.docker.com) detaillierte Informationen.

---

## Weiterführende Kapitel

| Thema | Seite | Schwerpunkt |
|---|---|---|
| KVM | [KVM](kvm.md) | Vollständige Virtualisierung für Windows-Gastsysteme |
| AutoOrtho | [AutoOrtho](../../scenery/ortho_streaming/autoortho.md) | Ortho-Streaming-Tool mit Docker-Unterstützung |
| pyenv | [pyenv](pyenv.md) | Python-Versionsverwaltung für Entwicklung |
| Wine | [Wine](wine.md) | Windows-Programme ohne vollständige VM |
