# pyenv

pyenv is a Python version management tool that allows you to install and manage multiple Python versions in parallel. It is particularly useful for developers who need to work with different Python versions.

## Installation and Setup

### Dependencies and Installation

Before you can install pyenv, you need to install some dependencies:

```bash
sudo apt-get update
sudo apt-get install -y make build-essential libssl-dev zlib1g-dev \
libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm \
libncursesw5-dev xz-utils tk-dev libxml2-dev libxmlsec1-dev libffi-dev liblzma-dev
```

For other distributions, see the [pyenv wiki](https://github.com/pyenv/pyenv/wiki#suggested-build-environment).

The installation of pyenv consists of three steps:

1. Clone the pyenv repository:

    ```bash
    git clone https://github.com/pyenv/pyenv.git ~/.pyenv
    ```

2. Add pyenv to your shell configuration. Choose the configuration for your shell:

    #### For bash
    ```bash
    echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bashrc
    echo 'command -v pyenv >/dev/null || export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bashrc
    echo 'eval "$(pyenv init -)"' >> ~/.bashrc
    ```

    #### For zsh
    ```bash
    echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.zshrc
    echo 'command -v pyenv >/dev/null || export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.zshrc
    echo 'eval "$(pyenv init -)"' >> ~/.zshrc
    ```

3. Reload your shell configuration:

    #### For bash
    ```bash
    source ~/.bashrc
    ```

    #### For zsh
    ```bash
    source ~/.zshrc
    ```

## Basic Usage and Python Versions

### Managing Python Versions

To install a new Python version, use the following command:

```bash
pyenv install 3.12.3
```

To use a Python version globally, execute this command:

```bash
pyenv global 3.12.3
```

To use a Python version for a specific directory, execute this command in the desired directory:

```bash
pyenv local 3.12.3
```

To show all installed Python versions, use:

```bash
pyenv versions
```

## Advanced Features and Plugins

### Virtual Environments and Plugin System

pyenv supports virtual environments through the pyenv-virtualenv plugin. The setup consists of three steps:

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

pyenv can automatically select the right Python version based on a `.python-version` file. Create the file with:

```bash
echo "3.12.3" > .python-version
```

pyenv supports various plugins for additional functionality:

- pyenv-virtualenv: Virtual environments
- pyenv-which-ext: Extended path resolution
- pyenv-update: Automatic updates

## System Management and Troubleshooting

### System Status and Maintenance

To check the currently used Python version:

```bash
pyenv version
```

When you've installed new Python binaries, execute this command:

```bash
pyenv rehash
```

For seamless integration with your shell, add these lines to your shell configuration:

```bash
# For zsh
eval "$(pyenv init --path)"
eval "$(pyenv init -)"
eval "$(pyenv virtualenv-init -)"
```

### Troubleshooting

If you encounter issues, proceed as follows:

1. Check your shell configuration
2. Ensure all dependencies are installed
3. Verify the permissions of pyenv directories
4. Consult the [official pyenv documentation](https://github.com/pyenv/pyenv#readme) 