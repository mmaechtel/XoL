# Z Shell (zsh)

Die Z Shell (zsh) ist eine leistungsstarke und erweiterbare Shell für Unix-Systeme. Sie bietet zahlreiche Verbesserungen gegenüber der Standard-Bash-Shell, wie bessere Autovervollständigung, erweiterte Globbing-Funktionen und ein flexibles Plugin-System.

## Installation

1. zsh wird über den Paketmanager installiert
   ```bash
   sudo apt update
   sudo apt install zsh
   ```

2. zsh wird als Standard-Shell gesetzt
   ```bash
   chsh -s $(which zsh)
   ```

3. Oh My Zsh wird installiert (optional, aber empfohlen)
   ```bash
   sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"
   ```

## Grundlegende Konfiguration

1. Eine `.zshrc`-Datei wird im Home-Verzeichnis erstellt
   ```bash
   touch ~/.zshrc
   ```

2. Grundlegende Konfigurationen werden hinzugefügt
   ```bash
   # Autovervollständigung wird aktiviert
   autoload -U compinit
   compinit

   # Der Prompt wird gesetzt
   PROMPT='%n@%m:%~%# '

   # Die Farbunterstützung wird aktiviert
   autoload -U colors && colors
   ```

## Erweiterte Funktionen

- **Autovervollständigung**: Intelligente Vervollständigung von Befehlen, Dateien und Optionen
- **Globbing**: Erweiterte Musterverarbeitung für Dateinamen
- **Plugin-System**: Einfache Integration von Erweiterungen
- **Themes**: Anpassbare Shell-Themes
- **Aliase**: Benutzerdefinierte Befehlsabkürzungen

## Nützliche Plugins

1. **zsh-autosuggestions**: Vorschläge basierend auf der Befehlsgeschichte
   ```bash
   git clone https://github.com/zsh-users/zsh-autosuggestions ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-autosuggestions
   ```

2. **zsh-syntax-highlighting**: Syntaxhervorhebung für Befehle
   ```bash
   git clone https://github.com/zsh-users/zsh-syntax-highlighting.git ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-syntax-highlighting
   ```

3. **zsh-completions**: Zusätzliche Vervollständigungen
   ```bash
   git clone https://github.com/zsh-users/zsh-completions ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-completions
   ```

## Tipps und Tricks

- `setopt` wird verwendet, um zsh-Optionen zu aktivieren
- `alias` wird für häufig verwendete Befehle genutzt
- Der Prompt wird mit `PROMPT` oder `RPROMPT` konfiguriert
- `history` wird für den Zugriff auf die Befehlsgeschichte verwendet
- `setopt share_history` wird für gemeinsame Befehlsgeschichte zwischen Terminals aktiviert

## Fehlerbehebung

Bei Problemen wird wie folgt vorgegangen:

1. Die `.zshrc`-Datei wird auf Syntaxfehler überprüft
2. Die Konfiguration wird mit `zsh -x` getestet
3. Die Berechtigungen der Konfigurationsdateien werden überprüft
4. Die [zsh-Dokumentation](https://zsh.sourceforge.io/Doc/) wird für weitere Hilfe konsultiert 