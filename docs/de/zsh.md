# Z Shell (zsh)

Die Z Shell (zsh) ist eine leistungsstarke und erweiterbare Shell für Unix-Systeme. Sie bietet zahlreiche Verbesserungen gegenüber der Standard-Bash-Shell, wie bessere Autovervollständigung, erweiterte Globbing-Funktionen und ein flexibles Plugin-System.

## Installation

1. Installieren Sie zsh über den Paketmanager:
   ```bash
   sudo apt update
   sudo apt install zsh
   ```

2. Setzen Sie zsh als Standard-Shell:
   ```bash
   chsh -s $(which zsh)
   ```

3. Installieren Sie Oh My Zsh (optional, aber empfohlen):
   ```bash
   sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"
   ```

## Grundlegende Konfiguration

1. Erstellen Sie eine `.zshrc`-Datei in Ihrem Home-Verzeichnis:
   ```bash
   touch ~/.zshrc
   ```

2. Fügen Sie grundlegende Konfigurationen hinzu:
   ```bash
   # Aktivieren Sie die Autovervollständigung
   autoload -U compinit
   compinit

   # Setzen Sie den Prompt
   PROMPT='%n@%m:%~%# '

   # Aktivieren Sie die Farbunterstützung
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

- Verwenden Sie `setopt` um zsh-Optionen zu aktivieren
- Nutzen Sie `alias` für häufig verwendete Befehle
- Konfigurieren Sie den Prompt mit `PROMPT` oder `RPROMPT`
- Verwenden Sie `history` für den Zugriff auf die Befehlsgeschichte
- Aktivieren Sie `setopt share_history` für gemeinsame Befehlsgeschichte zwischen Terminals

## Fehlerbehebung

Bei Problemen:
1. Überprüfen Sie die `.zshrc`-Datei auf Syntaxfehler
2. Testen Sie die Konfiguration mit `zsh -x`
3. Überprüfen Sie die Berechtigungen der Konfigurationsdateien
4. Konsultieren Sie die [zsh-Dokumentation](https://zsh.sourceforge.io/Doc/) für weitere Hilfe 