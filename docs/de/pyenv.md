# pyenv

pyenv ist ein Python-Versionsverwaltungstool, das es ermöglicht, mehrere Python-Versionen parallel zu installieren und zu verwalten. Es ist besonders nützlich für Entwickler, die mit verschiedenen Python-Versionen arbeiten müssen.

## Installation

### Abhängigkeiten

Bevor Sie pyenv installieren können, müssen Sie einige Abhängigkeiten installieren. Die benötigten Pakete unterscheiden sich je nach Linux-Distribution:

#### Ubuntu/Debian
```bash
sudo apt-get update
sudo apt-get install -y make build-essential libssl-dev zlib1g-dev \
libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm \
libncursesw5-dev xz-utils tk-dev libxml2-dev libxmlsec1-dev libffi-dev liblzma-dev
```

#### Fedora
```bash
sudo dnf install -y make gcc zlib-devel bzip2 bzip2-devel readline-devel \
sqlite sqlite-devel openssl-devel xz xz-devel libffi-devel findutils
```

#### Arch Linux
```bash
sudo pacman -S --needed base-devel openssl zlib xz tk
```

### Installation von pyenv

Die Installation von pyenv erfolgt in drei Schritten:

1. Klonen Sie das pyenv Repository:

    ```bash
    git clone https://github.com/pyenv/pyenv.git ~/.pyenv
    ```

2. Fügen Sie pyenv zu Ihrer Shell-Konfiguration hinzu. Wählen Sie die Konfiguration für Ihre Shell:

    #### Für bash
    ```bash
    echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bashrc
    echo 'command -v pyenv >/dev/null || export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bashrc
    echo 'eval "$(pyenv init -)"' >> ~/.bashrc
    ```

    #### Für zsh
    ```bash
    echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.zshrc
    echo 'command -v pyenv >/dev/null || export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.zshrc
    echo 'eval "$(pyenv init -)"' >> ~/.zshrc
    ```

3. Laden Sie Ihre Shell-Konfiguration neu:

    #### Für bash
    ```bash
    source ~/.bashrc
    ```

    #### Für zsh
    ```bash
    source ~/.zshrc
    ```

## Grundlegende Verwendung

### Python-Versionen installieren

Um eine neue Python-Version zu installieren, verwenden Sie den folgenden Befehl:

```bash
pyenv install 3.12.3
```

### Globale Python-Version festlegen

Um eine Python-Version global zu verwenden, führen Sie diesen Befehl aus:

```bash
pyenv global 3.12.3
```

### Lokale Python-Version festlegen

Um eine Python-Version für ein bestimmtes Verzeichnis zu verwenden, führen Sie diesen Befehl im gewünschten Verzeichnis aus:

```bash
pyenv local 3.12.3
```

### Verfügbare Python-Versionen auflisten

Um alle installierten Python-Versionen anzuzeigen, verwenden Sie:

```bash
pyenv versions
```

## Erweiterte Funktionen

### Virtuelle Umgebungen

pyenv unterstützt virtuelle Umgebungen über das Plugin pyenv-virtualenv. Die Einrichtung erfolgt in drei Schritten:

1. Installieren Sie das Plugin:

    ```bash
    git clone https://github.com/pyenv/pyenv-virtualenv.git $(pyenv root)/plugins/pyenv-virtualenv
    ```

2. Erstellen Sie eine virtuelle Umgebung:

    ```bash
    pyenv virtualenv 3.12.3 myenv
    ```

3. Aktivieren Sie die virtuelle Umgebung:

    ```bash
    pyenv activate myenv
    ```

### Automatische Versionsauswahl

pyenv kann automatisch die richtige Python-Version basierend auf einer `.python-version` Datei auswählen. Erstellen Sie die Datei mit:

```bash
echo "3.12.3" > .python-version
```

### Plugin-System

pyenv unterstützt verschiedene Plugins für zusätzliche Funktionen:

- pyenv-virtualenv: Virtuelle Umgebungen
- pyenv-which-ext: Erweiterte Pfadauflösung
- pyenv-update: Automatische Updates

## Tipps und Tricks

### Aktuelle Python-Version überprüfen

Um die aktuell verwendete Python-Version zu überprüfen:

```bash
pyenv version
```

### pyenv neu hashen

Wenn Sie neue Python-Binaries installiert haben, führen Sie diesen Befehl aus:

```bash
pyenv rehash
```

### Shell-Integration

Für eine nahtlose Integration mit Ihrer Shell fügen Sie diese Zeilen zu Ihrer Shell-Konfiguration hinzu:

```bash
# Für zsh
eval "$(pyenv init --path)"
eval "$(pyenv init -)"
eval "$(pyenv virtualenv-init -)"
```

## Fehlerbehebung

Bei Problemen gehen Sie wie folgt vor:

1. Überprüfen Sie Ihre Shell-Konfiguration
2. Stellen Sie sicher, dass alle Abhängigkeiten installiert sind
3. Überprüfen Sie die Berechtigungen der pyenv-Verzeichnisse
4. Konsultieren Sie die [offizielle pyenv-Dokumentation](https://github.com/pyenv/pyenv#readme) 