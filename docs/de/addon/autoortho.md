## Was ist AutoOrtho?

[AutoOrtho](../glossary.md#autoortho) ist ein Tool für X-Plane, das [Orthofotos](../glossary.md#orthofotos) in den Flugsimulator integriert. Es ermöglicht die Nutzung von hochauflösenden Luftbildern als Bodentexturen und verbessert damit die visuelle Realität in X-Plane deutlich. Diese Anleitung beschreibt die Installation unter Debian, sowohl als vorgefertigte [Binary](../glossary.md#binary) als auch aus dem Quellcode in einer `pyenv`-Umgebung mit Z Shell (`zsh`).

## Installation der AutoOrtho Binary unter Debian

Die [Binary](../glossary.md#binary)-Version von AutoOrtho ist eine vorgefertigte, ausführbare Datei, die keine zusätzliche Python-Umgebung erfordert. Sie ist ideal für Nutzer, die eine schnelle und unkomplizierte Installation wünschen. Folgen Sie diesen Schritten:

1. **Download:** Laden Sie die Binary herunter: [AutoOrtho Binary](https://github.com/kubilus1/autoortho/releases/).  
2. **Entpacken:** Extrahieren Sie die ZIP-Datei mit einem Tool wie `unzip` (Installation: `sudo apt install unzip`), z. B.:  
   ```bash
   unzip autoortho-linux-x64-v1.0.0.zip
   ```
3. **Ausführbar machen:** Stellen Sie sicher, dass die Datei ausführbar ist:  
   ```bash
   chmod +x autoortho
   ```
4. **Starten:** Führen Sie die Binary direkt aus:  
   ```bash
   ./autoortho
   ```
5. **Voraussetzung:** Installieren Sie `libfuse2`, da AutoOrtho dies für die Dateisystem-Integration benötigt:  
   ```bash
   sudo apt install libfuse2
   ```

Eine [GUI](../glossary.md#gui-graphical-user-interface) öffnet sich, und die Konfigurationsdatei `.autoortho` wird im Home-Verzeichnis erstellt. Geben Sie das X-Plane-Verzeichnis ein und laden Sie ein Ortho-Set über den "Scenery"-Tab.

## Installation von AutoOrtho aus dem Quellcode unter Debian mit pyenv und zsh

Die Installation aus dem Quellcode bietet mehr Kontrolle und Flexibilität. Mit `pyenv` lassen sich Python-Versionen isolieren und Konflikte mit dem System-Python vermeiden. Die folgenden Schritte führen Sie durch den Prozess.

### Voraussetzungen
AutoOrtho benötigt Python und externe Bibliotheken. Eine `pyenv`-Umgebung erleichtert die Verwaltung von Python-Versionen und Abhängigkeiten.

### Schritt 1: System vorbereiten
Aktualisieren Sie die Paketquellen und installieren Sie die für `pyenv` benötigten Abhängigkeiten:

```bash
sudo apt update
sudo apt install -y build-essential libssl-dev zlib1g-dev libbz2-dev libreadline-dev libsqlite3-dev curl libncursesw5-dev xz-utils tk-dev libxml2-dev libxmlsec1-dev libffi-dev liblzma-dev git
```

Installieren Sie zusätzlich `libfuse2`, das AutoOrtho für die Dateisystem-Integration benötigt:

```bash
sudo apt install libfuse2
```

### Schritt 2: pyenv einrichten
Laden Sie `pyenv` von GitHub herunter:

```bash
git clone https://github.com/pyenv/pyenv.git ~/.pyenv
```

Fügen Sie `pyenv` zu Ihrer `zsh`-Konfiguration hinzu, indem Sie folgende Zeilen in `~/.zshrc` einfügen:

```zsh
export PYENV_ROOT="$HOME/.pyenv"
export PATH="$PYENV_ROOT/bin:$PATH"
eval "$(pyenv init --path)"
eval "$(pyenv init -)"
```

Aktualisieren Sie die Shell:

```zsh
source ~/.zshrc
```

### Schritt 3: Python-Version installieren
Installieren Sie eine Python-Version, z. B. 3.10.16:

```zsh
pyenv install 3.10.16
```

### Schritt 4: AutoOrtho-Quellcode herunterladen
Laden Sie den Quellcode herunter und wechseln Sie in das Verzeichnis:

```zsh
git clone https://github.com/kubilus1/autoortho.git
cd autoortho
```

Setzen Sie die lokale Python-Version:

```zsh
pyenv local 3.10.16
```

### Schritt 5: Abhängigkeiten installieren
Installieren Sie die Python-Abhängigkeiten:

```zsh
pip install -r requirements.txt
```

An dieser Stelle kann es zu einem Fehler kommen, da PySimpleGUI nicht installiert werden kann. Das Paket ist nicht mehr standardmäßig in Python enthalten und muss separat installiert werden. PySimpleGUI kann aus verschiedenen Quellen heruntergeladen werden. Die Installation erfolgt im Verzeichnis `.pyenv/versions/3.10.16/lib/python3.10/site-packages/PySimpleGUI`.

(`libfuse2` wurde bereits in Schritt 1 installiert.)

### Schritt 6: AutoOrtho starten
Starten Sie AutoOrtho:

```zsh
python -i autoortho
```

Eine GUI öffnet sich, und die Konfigurationsdatei `.autoortho` wird im Home-Verzeichnis erstellt. Geben Sie das X-Plane-Verzeichnis ein und laden Sie ein Ortho-Set über den "Scenery"-Tab.

### Schritt 7: Überprüfung
Starten Sie X-Plane, während AutoOrtho läuft. Prüfen Sie die [`scenery_packs.ini`](../glossary.md#scenery_packsini) im [`Custom Scenery`](../glossary.md#custom-scenery)-Ordner von X-Plane auf AutoOrtho-Einträge wie `z_ao_*`.

### Zusätzliche Hinweise
- **Fehlerbehebung:** Bei Problemen können Sie `.autoortho` löschen und AutoOrtho neu starten.  
- **Voraussetzungen:** Eine stabile Internetverbindung ist für das Streaming der Orthofotos erforderlich.
- **FUSE-Konfiguration:** Wenn AutoOrtho als normaler Benutzer ausgeführt wird (was dringend empfohlen wird), muss in der Datei `/etc/fuse.conf` die Option `user_allow_other` aktiviert sein. Dies können Sie entweder mit folgendem Befehl erreichen:
  ```bash
  sudo echo "user_allow_other" >> /etc/fuse.conf
  ```
  Alternativ können Sie die Option auch in einem Editor auskommentieren (Achtung: sudo-Rechte werden auch zum Editieren benötigt):
  ```bash
  sudo nano /etc/fuse.conf
  ```
  Entfernen Sie dann das #-Zeichen vor der Zeile `#user_allow_other`.

### Fazit
Mit diesen Schritten lässt sich AutoOrtho in einer `pyenv`-Umgebung unter Debian mit `zsh` installieren. Die isolierte Umgebung trennt Abhängigkeiten sauber, sodass AutoOrtho in X-Plane reibungslos läuft.
