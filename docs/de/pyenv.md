# pyenv

pyenv ist ein Python-Versionsverwaltungstool, das es ermöglicht, mehrere Python-Versionen parallel zu installieren und zu verwalten. Es ist besonders nützlich für Entwickler, die mit verschiedenen Python-Versionen arbeiten müssen.

## Installation und Einrichtung

### Abhängigkeiten und Installation

Bevor pyenv installiert werden kann, müssen einige Abhängigkeiten installiert werden. Die benötigten Pakete unterscheiden sich je nach Linux-Distribution:

#### Ubuntu/Debian
```bash
sudo apt-get update
sudo apt-get install -y make build-essential libssl-dev zlib1g-dev \
libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm \
libncursesw5-dev xz-utils tk-dev libxml2-dev libxmlsec1-dev libffi-dev liblzma-dev
```

Die Installation von pyenv erfolgt in drei Schritten:

1. Das pyenv Repository wird geklont:

    ```bash
    git clone https://github.com/pyenv/pyenv.git ~/.pyenv
    ```

2. pyenv wird zur Shell-Konfiguration hinzugefügt. Die Konfiguration wird je nach Shell gewählt:

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

3. Die Shell-Konfiguration wird neu geladen:

    #### Für bash
    ```bash
    source ~/.bashrc
    ```

    #### Für zsh
    ```bash
    source ~/.zshrc
    ```

## Grundlegende Verwendung und Python-Versionen

### Python-Versionen verwalten

Um eine neue Python-Version zu installieren, wird der folgende Befehl verwendet:

```bash
pyenv install 3.12.3
```

Um eine Python-Version global zu verwenden, wird dieser Befehl ausgeführt:

```bash
pyenv global 3.12.3
```

Um eine Python-Version für ein bestimmtes Verzeichnis zu verwenden, wird dieser Befehl im gewünschten Verzeichnis ausgeführt:

```bash
pyenv local 3.12.3
```

Um alle installierten Python-Versionen anzuzeigen, wird folgender Befehl verwendet:

```bash
pyenv versions
```

## Erweiterte Funktionen und Plugins

### Virtuelle Umgebungen und Plugin-System

pyenv unterstützt virtuelle Umgebungen über das Plugin pyenv-virtualenv. Die Einrichtung erfolgt in drei Schritten:

1. Das Plugin wird installiert:

    ```bash
    git clone https://github.com/pyenv/pyenv-virtualenv.git $(pyenv root)/plugins/pyenv-virtualenv
    ```

2. Eine virtuelle Umgebung wird erstellt:

    ```bash
    pyenv virtualenv 3.12.3 myenv
    ```

3. Die virtuelle Umgebung wird aktiviert:

    ```bash
    pyenv activate myenv
    ```

pyenv kann automatisch die richtige Python-Version basierend auf einer `.python-version` Datei auswählen. Die Datei wird wie folgt erstellt:

```bash
echo "3.12.3" > .python-version
```

pyenv unterstützt verschiedene Plugins für zusätzliche Funktionen:

- pyenv-virtualenv: Virtuelle Umgebungen
- pyenv-which-ext: Erweiterte Pfadauflösung
- pyenv-update: Automatische Updates

## System-Verwaltung und Fehlerbehebung

### System-Status und Wartung

Um die aktuell verwendete Python-Version zu überprüfen, wird folgender Befehl verwendet:

```bash
pyenv version
```

Wenn neue Python-Binaries installiert wurden, wird dieser Befehl ausgeführt:

```bash
pyenv rehash
```

Für eine nahtlose Integration mit der Shell werden diese Zeilen zur Shell-Konfiguration hinzugefügt:

```bash
# Für zsh
eval "$(pyenv init --path)"
eval "$(pyenv init -)"
eval "$(pyenv virtualenv-init -)"
```

### Fehlerbehebung

Bei Problemen wird wie folgt vorgegangen:

1. Die Shell-Konfiguration wird überprüft
2. Es wird sichergestellt, dass alle Abhängigkeiten installiert sind
3. Die Berechtigungen der pyenv-Verzeichnisse werden überprüft
4. Die [offizielle pyenv-Dokumentation](https://github.com/pyenv/pyenv#readme) wird konsultiert 