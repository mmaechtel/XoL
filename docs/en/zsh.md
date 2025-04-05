# Z Shell (zsh)

The Z Shell (zsh) is a powerful and extensible shell for Unix systems. It offers numerous improvements over the standard Bash shell, including better autocompletion, advanced globbing features, and a flexible plugin system.

## Installation

1. Install zsh using the package manager:
   ```bash
   sudo apt update
   sudo apt install zsh
   ```

2. Set zsh as your default shell:
   ```bash
   chsh -s $(which zsh)
   ```

3. Install Oh My Zsh (optional, but recommended):
   ```bash
   sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"
   ```

## Basic Configuration

1. Create a `.zshrc` file in your home directory:
   ```bash
   touch ~/.zshrc
   ```

2. Add basic configurations:
   ```bash
   # Enable autocompletion
   autoload -U compinit
   compinit

   # Set the prompt
   PROMPT='%n@%m:%~%# '

   # Enable color support
   autoload -U colors && colors
   ```

## Advanced Features

- **Autocompletion**: Intelligent command, file, and option completion
- **Globbing**: Advanced pattern matching for filenames
- **Plugin System**: Easy integration of extensions
- **Themes**: Customizable shell themes
- **Aliases**: Custom command shortcuts

## Useful Plugins

1. **zsh-autosuggestions**: Suggestions based on command history
   ```bash
   git clone https://github.com/zsh-users/zsh-autosuggestions ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-autosuggestions
   ```

2. **zsh-syntax-highlighting**: Syntax highlighting for commands
   ```bash
   git clone https://github.com/zsh-users/zsh-syntax-highlighting.git ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-syntax-highlighting
   ```

3. **zsh-completions**: Additional completions
   ```bash
   git clone https://github.com/zsh-users/zsh-completions ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-completions
   ```

## Tips and Tricks

- Use `setopt` to enable zsh options
- Use `alias` for frequently used commands
- Configure the prompt with `PROMPT` or `RPROMPT`
- Use `history` to access command history
- Enable `setopt share_history` for shared command history between terminals

## Troubleshooting

If you encounter issues:
1. Check the `.zshrc` file for syntax errors
2. Test the configuration with `zsh -x`
3. Verify permissions of configuration files
4. Consult the [zsh documentation](https://zsh.sourceforge.io/Doc/) for additional help 