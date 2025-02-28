## Liquorix Kernel on Debian

The [Liquorix Kernel](../glossary.md#liquorix-kernel) is an optimized version of the Linux kernel focused on desktop and gaming performance. It offers improved response times and performance through special configurations and patches.

## Prerequisites

- Debian installed and updated
- Root or sudo rights

## Step 1: Update System

First, update your system:
```bash
sudo apt update && sudo apt upgrade -y
```

## Step 2: Add Repository

Add the Liquorix repository:

1. **Install dependencies:**
```bash
sudo apt install -y curl gpg
```

2. **Add repository key:**
```bash
curl -s 'https://liquorix.net/linux-liquorix-keyring.gpg' | sudo gpg --dearmor -o /usr/share/keyrings/liquorix-keyring.gpg
```

3. **Set up repository:**
```bash
echo 'deb [signed-by=/usr/share/keyrings/liquorix-keyring.gpg] https://liquorix.net/debian $(lsb_release -cs) main' | sudo tee /etc/apt/sources.list.d/liquorix.list
```

4. **Update package sources:**
```bash
sudo apt update
```

## Step 3: Install Kernel

Install the Liquorix kernel and headers:
```bash
sudo apt install linux-image-liquorix-amd64 linux-headers-liquorix-amd64
```

## Step 4: Reboot System

Restart the system to load the new kernel:
```bash
sudo reboot
```

## Step 5: Verify Installation

After reboot, check the active kernel version:
```bash
uname -r
```

The output should show a Liquorix kernel version (e.g., `6.6.0-1-liquorix-amd64`).

## Troubleshooting

- **Boot Issues**: If the new kernel doesn't start, you can select the standard Debian kernel in the GRUB menu.
- **DKMS Modules**: For drivers like [Nvidia](nvidia.md), [DKMS](../glossary.md#dkms-dynamic-kernel-module-support) is important:
  ```bash
  sudo apt install dkms
  ```

## Conclusion

The Liquorix kernel can improve system performance, especially for desktop applications and gaming. If problems occur, you can always switch back to the standard kernel. 