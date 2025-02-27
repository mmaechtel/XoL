## Installation von AutoOrtho unter Debian 12 mit pyenv und zsh: Eine Anleitung

AutoOrtho ist ein Tool für X-Plane, das Orthofotos in den Flugsimulator integriert. Dieser Beitrag beschreibt die Installation von AutoOrtho unter Debian 12 (Bookworm) in einer `pyenv`-Umgebung mit der Z Shell (`zsh`). Die Nutzung von `pyenv` ermöglicht isolierte Python-Versionen und vermeidet Konflikte mit dem System-Python. Die Schritte sind im Folgenden detailliert aufgeführt.

### Voraussetzungen
AutoOrtho basiert auf Python und externen Bibliotheken. Eine `pyenv`-Umgebung bietet eine effiziente Möglichkeit, Python-Versionen und Abhängigkeiten zu verwalten.

### Schritt 1: Systemvorbereitung
Aktualisieren Sie die Paketquellen und installieren Sie die erforderlichen Abhängigkeiten für `pyenv`:

```bash
sudo apt update
sudo apt install -y build-essential libssl-dev zlib1g-dev libbz2-dev libreadline-dev libsqlite3-dev curl libncursesw5-dev xz-utils tk-dev libxml2-dev libxmlsec1-dev libffi-dev liblzma-dev git
```

Installieren Sie zusätzlich `libfuse2`, das AutoOrtho für die Dateisystem-Integration benötigt:

```bash
sudo apt install libfuse2
```

### Schritt 2: pyenv einrichten
Laden Sie `pyenv` aus dem GitHub-Repository:

```bash
git clone https://github.com/pyenv/pyenv.git ~/.pyenv
```

Fügen Sie `pyenv` zur `zsh`-Konfiguration hinzu, indem Sie diese Zeilen in `~/.zshrc` einfügen:

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

Installieren Sie das `pyenv-virtualenv`-Plugin für virtuelle Umgebungen:

```zsh
git clone https://github.com/pyenv/pyenv-virtualenv.git ~/.pyenv/plugins/pyenv-virtualenv
source ~/.zshrc
```

!!! note "Hinweis"
`pyenv-virtualenv` wird verwendet, um virtuelle Umgebungen direkt in `pyenv` zu verwalten. Es sorgt für eine saubere Isolierung der AutoOrtho-Abhängigkeiten und erleichtert die Arbeit mit mehreren Python-Versionen.


### Schritt 3: Python-Version installieren
Installieren Sie eine Python-Version, z. B. 3.11.7:

```zsh
pyenv install 3.11.7
```

### Schritt 4: AutoOrtho-Quellcode herunterladen
Laden Sie den AutoOrtho-Quellcode und wechseln Sie in das Verzeichnis:

```zsh
git clone https://github.com/kubilus1/autoortho.git
cd autoortho
```

Setzen Sie die lokale Python-Version:

```zsh
pyenv local 3.11.7
```

### Schritt 5: Virtuelle Umgebung erstellen
Erstellen und aktivieren Sie eine virtuelle Umgebung:

```zsh
pyenv virtualenv 3.11.7 autoortho-env
pyenv activate autoortho-env
```

### Schritt 6: Abhängigkeiten installieren
Installieren Sie die Python-Abhängigkeiten:

```zsh
pip install -r requirements.txt
```

Die Systemabhängigkeit `libfuse2` wurde bereits in Schritt 1 installiert.

### Schritt 7: AutoOrtho starten
Starten Sie AutoOrtho:

```zsh
python autoortho.py
```

Eine GUI öffnet sich, und die Konfigurationsdatei `.autoortho` wird im Home-Verzeichnis erstellt. Geben Sie das X-Plane-Verzeichnis ein und laden Sie ein Ortho-Set über den "Scenery"-Tab.

### Schritt 8: Überprüfung
Starten Sie X-Plane, während AutoOrtho aktiv ist. Kontrollieren Sie die `scenery_packs.ini` im `Custom Scenery`-Ordner von X-Plane, um sicherzustellen, dass AutoOrtho-Einträge (z. B. `z_ao_*`) vorhanden sind.

### Zusätzliche Informationen
- **Umgebung deaktivieren:** Verwenden Sie `pyenv deactivate`, um die virtuelle Umgebung zu verlassen.
- **Fehlerbehebung:** Bei Problemen kann die `.autoortho`-Datei gelöscht und AutoOrtho neu gestartet werden.
- **Systemanforderungen:** Eine stabile Internetverbindung ist für das Streaming der Orthofotos erforderlich.

### Schlussfolgerung
Die Installation von AutoOrtho in einer `pyenv`-Umgebung unter Debian 12 mit `zsh` ist mit diesen Schritten umsetzbar. Die isolierte Umgebung sorgt für eine saubere Trennung der Abhängigkeiten, und AutoOrtho kann anschließend in X-Plane genutzt werden.

---

### Änderungen für zsh
- Alle Verweise auf `~/.bashrc` wurden durch `~/.zshrc` ersetzt.
- Die Shell-Befehle verwenden `zsh` als Syntaxhervorhebung, obwohl die Befehle selbst kompatibel bleiben.
- Der Text bleibt sachlich und neutral, mit Fokus auf technische Genauigkeit.

Dieser Eintrag ist präzise und auf die Nutzung von `zsh` abgestimmt.