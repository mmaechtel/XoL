---
title: KVM
description: "KVM virtualization on Debian for X-Plane: installation, Windows VM setup, USB passthrough for StreamDeck, and SSH key management."
tags:
  - virtualization
  - kvm
  - qemu
---
## KVM

[KVM](../../glossary.md#kvm-kernel-based-virtual-machine) is an open-source virtualization technology integrated into the Linux kernel that enables running virtual machines on a physical computer. It uses hardware virtualization (like Intel VT or AMD-V) to efficiently run guest systems like Linux or Windows.

### Installation

For Debian Bookworm, there are several tutorials describing KVM installation on a Linux system, e.g., [How Do I Properly Install KVM on Linux](https://sysguides.com/install-kvm-on-linux). The following points are particularly important:

**Check System Requirements**

- Make sure your processor supports hardware virtualization (Intel VT-x or AMD-V).
- Check with `egrep -c '(vmx|svm)' /proc/cpuinfo` (value > 0 means support).
- Test KVM acceleration with `kvm-ok` (after installing `cpu-checker` if needed).

**Install Packages**

- For Ubuntu/Debian: `sudo apt install qemu-kvm libvirt-daemon-system libvirt-clients bridge-utils virt-manager`

**Start and Enable Libvirt Service**

- `sudo systemctl enable --now libvirtd`
- Check the status: `sudo systemctl status libvirtd`

**Set User Permissions**

- Add your user to the `libvirt` group: `sudo usermod -aG libvirt $(whoami)`
- Log out and back in for changes to take effect.

**Configure Network (optional)**

- Set up a network bridge using `bridge-utils` if VMs need to be externally accessible (details in the guide). For our purposes, we don't need this.
- NAT is used by default.

**Verify Installation**

- Test KVM with `virsh list --all` (should show an empty VM list if no VMs exist).
- Check loaded modules: `lsmod | grep kvm` (e.g., `kvm_intel` or `kvm_amd`).

**Optimization (optional)**

- Enable TuneD profile `virtual-host`: `sudo tuned-adm profile virtual-host`
- Verify with `tuned-adm active`.

The same applies to installing a Windows OS in KVM, e.g., [How to Properly Install a Windows 11 Virtual Machine on KVM](https://sysguides.com/install-a-windows-11-virtual-machine-on-kvm)

In this context, preparing your own ISO image for Windows as described [here](https://github.com/ntdevlabs/tiny11builder) is interesting.

## WiP: X-Plane Plugins in a Windows OS in KVM

- Streamdeck
    - Add USB Devices
    - StreamDeck for Xplane 12
        - Configure IP address
    - X321 Streamdeck Profile
        - Fonts!
    - Other profiles?
- My FS Flight 

## Copy SSH Key to Server

The easiest way is to use `ssh-copy-id`:

**Create SSH Key (if not exists)**

- Generate key: `ssh-keygen -t ed25519 -C "your@email.com"`
- By default, the key is stored in `~/.ssh/id_ed25519`

**Copy Key to Server**

- Using ssh-copy-id: `ssh-copy-id username@server`
- Alternative manual method:
  ```bash
  cat ~/.ssh/id_ed25519.pub | ssh username@server "mkdir -p ~/.ssh && cat >> ~/.ssh/authorized_keys"
  ```

**Check Permissions**

- On the server, the following permissions should be set:
  ```bash
  chmod 700 ~/.ssh
  chmod 600 ~/.ssh/authorized_keys
  ```

## X-Plane Addons via KVM

Several Windows-only X-Plane addons can be run in a KVM virtual machine. Setup guides and configuration details for specific addons are documented under **[Addons → Via KVM](../../addon/kvm/index.md)**.

---

## Further Reading

| Topic | Page | Focus |
|---|---|---|
| Wine | [Wine](wine.md) | Lighter alternative for some Windows programs |
| Docker | [Docker](docker.md) | Container-based application isolation |
| Nvidia Drivers | [Nvidia Drivers](../optimizations/nvidia.md) | GPU drivers and passthrough relevance |
| Kernel Tuning | [Kernel Tuning](../system/systemtuning.md) | System performance optimization for VMs |