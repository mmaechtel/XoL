### [Docker](../glossary.md#docker) unter Debian installieren: Eine Schritt-für-Schritt-Anleitung

[Docker](../glossary.md#docker) ist eine weit verbreitete Plattform zur Containerisierung von Anwendungen, die Entwicklern und Administratoren hilft, Anwendungen effizient zu erstellen, bereitzustellen und zu verwalten. Dieses Kapitel erklärt, wie man Docker auf einem Debian-System installiert. Die Anleitung ist sachlich und praxisorientiert, sodass auch Einsteiger problemlos folgen können.

## Voraussetzungen

Bevor Sie beginnen, stellen Sie sicher, dass:

- Sie Zugriff auf ein Debian-System haben
- Sie über Root- oder Sudo-Rechte verfügen

## Schritt 1: System aktualisieren

Zunächst sollten Sie sicherstellen, dass Ihr Debian-System auf dem neuesten Stand ist. Öffnen Sie ein Terminal und führen Sie folgende Befehle aus:

```bash
sudo apt update
sudo apt upgrade -y
```

Dies aktualisiert die Paketlisten und installiert verfügbare Updates für bereits installierte Software.

## Schritt 2: Erforderliche Abhängigkeiten installieren

Docker benötigt einige grundlegende Pakete, um korrekt zu funktionieren. Installieren Sie diese mit:

```bash
sudo apt install -y apt-transport-https ca-certificates curl gnupg lsb-release
```

Diese Pakete ermöglichen den sicheren Download von Software und die Verwaltung von Repository-Schlüsseln.

## Schritt 3: Docker-Repository hinzufügen

Debian enthält zwar eine ältere Version von Docker im Standard-Repository, aber es ist empfehlenswert, das offizielle Docker-Repository zu verwenden, um die neueste Version zu erhalten. Folgen Sie diesen Schritten:

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

Jetzt können Sie Docker installieren. Führen Sie den folgenden Befehl aus, um die Hauptpakete zu installieren:

```bash
sudo apt install -y docker-ce docker-ce-cli containerd.io
```

- `docker-ce`: Die Docker-Engine selbst.
- `docker-ce-cli`: Die Kommandozeilen-Schnittstelle.
- `containerd.io`: Der Container-Runtime, der von Docker verwendet wird.

## Schritt 5: Docker-Dienst starten und aktivieren

Nach der Installation müssen Sie den Docker-Dienst starten und sicherstellen, dass er beim Systemstart automatisch läuft:

```bash
sudo systemctl start docker
sudo systemctl enable docker
```

## Schritt 6: Installation überprüfen

Um sicherzugehen, dass Docker korrekt installiert wurde, führen Sie diesen Befehl aus:

```bash
docker --version
```

Sie sollten eine Ausgabe wie `Docker version 20.10.x, build ...` (oder eine neuere Version) sehen. Testen Sie außerdem, ob Docker funktioniert, indem Sie einen einfachen Container starten:

```bash
sudo docker run hello-world
```

Dieser Befehl lädt ein Test-Image herunter und führt es aus. Wenn alles korrekt läuft, erhalten Sie eine Bestätigungsnachricht von Docker.

## Schritt 7: Docker ohne Root-Rechte nutzen (optional)

Standardmäßig erfordert Docker Root-Rechte. Wenn Sie Docker als normaler Benutzer ausführen möchten, fügen Sie Ihren Benutzer zur `docker`-Gruppe hinzu:

```bash
sudo usermod -aG docker $USER
```

Melden Sie sich anschließend ab und wieder an (oder starten Sie das Terminal neu), damit die Änderungen wirksam werden. Danach können Sie Docker-Befehle ohne `sudo` ausführen.

## Fazit

Sie haben Docker nun erfolgreich auf Debian installiert. Mit dieser Installation können Sie Container erstellen, Images verwalten und Anwendungen in isolierten Umgebungen betreiben. Falls Sie weitere Anpassungen oder spezifische Konfigurationen benötigen, bietet die [offizielle Docker-Dokumentation](https://docs.docker.com) detaillierte Informationen.
