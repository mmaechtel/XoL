## What is AutoOrtho?

[AutoOrtho](../glossary.md#autoortho) is a tool for X-Plane that integrates [orthophotos](../glossary.md#orthophotos) into the flight simulator. It enables the use of high-resolution aerial imagery as ground textures, significantly enhancing the visual realism in X-Plane. This guide describes the installation on Debian 12 (Bookworm), both as a pre-built [binary](../glossary.md#binary) and from source code in a `pyenv` environment using Z Shell (`zsh`).

## Installing the AutoOrtho Binary on Debian 12

The [binary](../glossary.md#binary) version of AutoOrtho is a pre-compiled executable that doesn't require an additional Python environment. It's ideal for users who want a quick and straightforward installation. Follow these steps:

1. **Download:** Get the binary from: [AutoOrtho Binary](https://github.com/kubilus1/autoortho/releases/).  
2. **Extract:** Unpack the ZIP file using a tool like `unzip` (install with `sudo apt install unzip`), e.g.:  
   ```bash
   unzip autoortho-linux-x64-v1.0.0.zip
   ```
3. **Make executable:** Ensure the file is executable:  
   ```bash
   chmod +x autoortho
   ```
4. **Launch:** Run the binary directly:  
   ```bash
   ./autoortho
   ```
5. **Prerequisite:** Install `libfuse2`, as AutoOrtho needs it for filesystem integration:  
   ```bash
   sudo apt install libfuse2
   ```

A [GUI](../glossary.md#gui-graphical-user-interface) will open, and the configuration file `.autoortho` will be created in your home directory. Enter the X-Plane directory and load an ortho set through the "Scenery" tab.

### Step 7: Verification
Start X-Plane while AutoOrtho is running. Check the [`scenery_packs.ini`](../glossary.md#scenery_packsini) in X-Plane's [`Custom Scenery`](../glossary.md#custom-scenery) folder for AutoOrtho entries like `z_ao_*`.

## Installing AutoOrtho from Source on Debian 12 with pyenv and zsh

Installing from source offers more control and flexibility. Using `pyenv` allows you to isolate Python versions and avoid conflicts with the system Python. The following steps will guide you through the process.

### Prerequisites
AutoOrtho requires Python and external libraries. A `pyenv` environment makes it easier to manage Python versions and dependencies.

### Step 1: Prepare the System
Update package sources and install dependencies required for `pyenv`:

```bash
sudo apt update
sudo apt install -y build-essential libssl-dev zlib1g-dev libbz2-dev libreadline-dev libsqlite3-dev curl libncursesw5-dev xz-utils tk-dev libxml2-dev libxmlsec1-dev libffi-dev liblzma-dev git
```

Also install `libfuse2`, which AutoOrtho needs for filesystem integration:

```bash
sudo apt install libfuse2
```

### Step 2: Set up pyenv
Download `pyenv` from GitHub:

```bash
git clone https://github.com/pyenv/pyenv.git ~/.pyenv
```

Add `pyenv` to your `zsh` configuration by adding these lines to `~/.zshrc`:

```zsh
export PYENV_ROOT="$HOME/.pyenv"
export PATH="$PYENV_ROOT/bin:$PATH"
eval "$(pyenv init --path)"
eval "$(pyenv init -)"
```

Update the shell:

```zsh
source ~/.zshrc
```

### Step 3: Install Python Version
Install a Python version, e.g., 3.10.16:

```zsh
pyenv install 3.10.16
```

### Step 4: Download AutoOrtho Source Code
Get the source code and change to its directory:

```zsh
git clone https://github.com/kubilus1/autoortho.git
cd autoortho
```

Set the local Python version:

```zsh
pyenv local 3.10.16
```

### Step 5: Install Dependencies
Install the Python dependencies:

```zsh
pip install -r requirements.txt
```

At this point, you might encounter an error as PySimpleGUI cannot be installed. The package is no longer included in Python by default and needs to be installed separately. PySimpleGUI can be downloaded from various sources. Installation takes place in the directory `.pyenv/versions/3.10.16/lib/python3.10/site-packages/PySimpleGUI`.

(`libfuse2` was already installed in Step 1.)

### Step 6: Launch AutoOrtho
Start AutoOrtho:

```zsh
python -i autoortho
```

A GUI will open, and the configuration file `.autoortho` will be created in your home directory. Enter the X-Plane directory and load an ortho set through the "Scenery" tab.

### Step 7: Verification
Start X-Plane while AutoOrtho is running. Check the [`scenery_packs.ini`](../glossary.md#scenery_packsini) in X-Plane's [`Custom Scenery`](../glossary.md#custom-scenery) folder for AutoOrtho entries like `z_ao_*`.

### Additional Notes
- **Troubleshooting:** If problems occur, you can delete `.autoortho` and restart AutoOrtho.  
- **Requirements:** A stable internet connection is required for streaming orthophotos.
- **FUSE Configuration:** When running AutoOrtho as a regular user (which is strongly recommended), the `user_allow_other` option must be enabled in `/etc/fuse.conf`. You can either do this with the following command:
  ```bash
  sudo echo "user_allow_other" >> /etc/fuse.conf
  ```
  Alternatively, you can uncomment the option in an editor (Note: sudo rights are also needed for editing):
  ```bash
  sudo nano /etc/fuse.conf
  ```
  Then remove the # character in front of the line `#user_allow_other`.

### Conclusion
Following these steps, you can install AutoOrtho in a `pyenv` environment on Debian 12 with `zsh`. The isolated environment cleanly separates dependencies, ensuring AutoOrtho runs smoothly in X-Plane.

