# pyenv

pyenv is a Python version management tool that allows you to install and manage multiple Python versions in parallel. It is particularly useful for developers who need to work with different Python versions.

## Installation

### Dependencies

Before you can install pyenv, you need to install some dependencies:

```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install -y make build-essential libssl-dev zlib1g-dev \
libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm \
libncursesw5-dev xz-utils tk-dev libxml2-dev libxmlsec1-dev libffi-dev liblzma-dev

# Fedora
sudo dnf install -y make gcc zlib-devel bzip2 bzip2-devel readline-devel \
sqlite sqlite-devel openssl-devel xz xz-devel libffi-devel findutils

# Arch Linux
sudo pacman -S --needed base-devel openssl zlib xz tk
```

### Installing pyenv

1. Clone the pyenv repository:

```bash
git clone https://github.com/pyenv/pyenv.git ~/.pyenv
```

2. Add pyenv to your shell configuration:

```bash
# For bash
echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bashrc
echo 'command -v pyenv >/dev/null || export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bashrc
echo 'eval "$(pyenv init -)"' >> ~/.bashrc

# For zsh
echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.zshrc
echo 'command -v pyenv >/dev/null || export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.zshrc
echo 'eval "$(pyenv init -)"' >> ~/.zshrc
```

3. Reload your shell configuration:

```bash
# For bash
source ~/.bashrc

# For zsh
source ~/.zshrc
```

## Basic Usage

### Installing Python Versions

To install a new Python version:

```bash
pyenv install 3.12.3
```

### Setting Global Python Version

To use a Python version globally:

```bash
pyenv global 3.12.3
```

### Setting Local Python Version

To use a Python version for a specific directory:

```bash
pyenv local 3.12.3
```

### Listing Available Python Versions

To show all installed Python versions:

```bash
pyenv versions
```

## Advanced Features

### Virtual Environments

pyenv supports virtual environments through the pyenv-virtualenv plugin:

1. Install the plugin:

```bash
git clone https://github.com/pyenv/pyenv-virtualenv.git $(pyenv root)/plugins/pyenv-virtualenv
```

2. Create a virtual environment:

```bash
pyenv virtualenv 3.12.3 myenv
```

3. Activate the virtual environment:

```bash
pyenv activate myenv
```

### Automatic Version Selection

pyenv can automatically select the right Python version based on a `.python-version` file:

```bash
echo "3.12.3" > .python-version
```

### Plugin System

pyenv supports various plugins for additional functionality:

- pyenv-virtualenv: Virtual environments
- pyenv-which-ext: Extended path resolution
- pyenv-update: Automatic updates

## Tips and Tricks

### Checking Current Python Version

```bash
pyenv version
```

### Rehashing pyenv

When you've installed new Python binaries:

```bash
pyenv rehash
```

### Shell Integration

pyenv provides seamless integration with your shell:

```bash
# For zsh
eval "$(pyenv init --path)"
eval "$(pyenv init -)"
eval "$(pyenv virtualenv-init -)"
```

## Troubleshooting

If you encounter issues:

1. Check your shell configuration
2. Ensure all dependencies are installed
3. Verify the permissions of pyenv directories
4. Consult the [official pyenv documentation](https://github.com/pyenv/pyenv#readme) 