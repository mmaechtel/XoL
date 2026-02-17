## Installing Wine on Debian 12 - Two Ways

[Wine](../../glossary.md#wine-wine-is-not-an-emulator) allows running Windows programs on Linux. Here are two ways to install Wine on Debian 12.

### 1. Installation via Standard Debian Package Sources
First update the system:
```bash
sudo apt update && sudo apt upgrade -y
```

Then install Wine:
```bash
sudo apt install wine
```

Verify the installation:
```bash
wine --version
```

That's it - the Debian version is quick to set up but might not be the latest.

### 2. Installation via WineHQ Repository
For a more recent version, enable 32-bit architecture and add the repository:
```bash
sudo dpkg --add-architecture i386
sudo apt update
sudo mkdir -pm755 /etc/apt/keyrings
sudo wget -O /etc/apt/keyrings/winehq-archive.key https://dl.winehq.org/wine-builds/winehq.key
sudo wget -NP /etc/apt/sources.list.d/ https://dl.winehq.org/wine-builds/debian/dists/bookworm/winehq-bookworm.sources
sudo apt update
```

Install Wine:
```bash
sudo apt install --install-recommends winehq-stable
```

Check version:
```bash
wine --version
```

Optionally configure with `winecfg`. This variant provides the latest stable Wine version.

### Conclusion
The Debian variant is simpler, WineHQ more current. Both are easy to set up, depending on your needs.


## 3. Adding Winetricks

Winetricks is a helper script for installing additional libraries and settings for Wine. Here's how:

```bash
sudo apt install winetricks
```

After installation, Winetricks can be used, e.g., to add DLLs or fonts:

```bash
winetricks dlls
```

Or start a graphical interface:

```bash
winetricks --gui
```

Winetricks facilitates fine-tuning and increases compatibility with some Windows applications.


## 4. Installing the 32-Bit Version

Some older Windows programs require the 32-bit version of Wine. Here's how to install it:

**Enable 32-bit Architecture and Install Wine32**

- Execute the following command that enables 32-bit architecture, updates package sources, and installs Wine32:
  ```bash
  sudo dpkg --add-architecture i386 && sudo apt-get update && sudo apt-get install wine32:i386
  ```

Alternatively, you can execute the steps individually:
```bash
# Enable 32-bit architecture
sudo dpkg --add-architecture i386

# Update package sources
sudo apt-get update

# Install Wine32
sudo apt-get install wine32:i386
```

After installation, you can run 32-bit Windows programs. This is particularly useful for older software or programs that don't have a 64-bit version.

---

## Further Reading

| Topic | Page | Focus |
|---|---|---|
| KVM | [KVM](kvm.md) | Full Windows virtualization as alternative |
| Docker | [Docker](docker.md) | Container-based application isolation |
| Nvidia Drivers | [Nvidia Drivers](../optimizations/nvidia.md) | GPU drivers for Vulkan/DirectX translation |