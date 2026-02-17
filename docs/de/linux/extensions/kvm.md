---
title: KVM
description: KVM für X-Plane unter Linux
tags:
  - virtualisierung
  - kvm
  - qemu
---

## KVM

[KVM](../../glossary.md#kvm-kernel-based-virtual-machine) ist eine Open-Source-Virtualisierungstechnologie, die im Linux-Kernel integriert ist und es ermöglicht, virtuelle Maschinen auf einem physischen Rechner auszuführen. Sie nutzt Hardware-Virtualisierung (wie Intel VT oder AMD-V), um Gastsysteme wie Linux oder Windows effizient zu betreiben.

### Installation

Für Debian Bookworm gibt es eine Reihe von Tutorials die die Installation von KVM in einem Linux System beschreiben, z.B. [How Do I Properly Install KVM on Linux](https://sysguides.com/install-kvm-on-linux). Folgende Punkte sind dabei besonders wichtig:

**Systemvoraussetzungen prüfen**

- Stelle sicher, dass dein Prozessor Hardware-Virtualisierung unterstützt (Intel VT-x oder AMD-V).
- Überprüfe mit `egrep -c '(vmx|svm)' /proc/cpuinfo` (Wert > 0 bedeutet Unterstützung).
- Teste KVM-Beschleunigung mit `kvm-ok` (nach Installation von `cpu-checker`, falls nötig).

**Pakete installieren**

- Für Ubuntu/Debian: `sudo apt install qemu-kvm libvirt-daemon-system libvirt-clients bridge-utils virt-manager`

**Libvirt-Dienst starten und aktivieren**

- `sudo systemctl enable --now libvirtd`
- Überprüfe den Status: `sudo systemctl status libvirtd`

**Benutzerberechtigungen setzen**

- Füge deinen Benutzer der `libvirt`-Gruppe hinzu: `sudo usermod -aG libvirt $(whoami)`
- Melde dich ab und wieder an, damit die Änderungen wirksam werden.

**Netzwerk konfigurieren (optional)**

- Richte eine Netzwerkbrücke ein, z. B. mit `bridge-utils`, falls VMs extern erreichbar sein sollen (Details in der Anleitung). Für unsere Zwecke benötigen wir diese nicht.
- Standardmäßig wird NAT verwendet.

**Installation überprüfen**

- Teste KVM mit `virsh list --all` (sollte eine leere VM-Liste anzeigen, wenn keine VMs existieren).
- Prüfe geladene Module: `lsmod | grep kvm` (z. B. `kvm_intel` oder `kvm_amd`).

**Optimierung (optional)**

- Aktiviere TuneD-Profil `virtual-host`: `sudo tuned-adm profile virtual-host`
- Überprüfe mit `tuned-adm active`.

Das gleiche gilt für die Installation eines Windows OS in der KVM, z.B. [How to Properly Install a Windows 11 Virtual Machine on KVM](https://sysguides.com/install-a-windows-11-virtual-machine-on-kvm)

In diesem Zusammen ist die Vorbereitung eines eigenen ISO Images für Windows wie z.B. [hier](https://github.com/ntdevlabs/tiny11builder) beschrieben interessant.

## WiP: X-Plane Plugins in einem Windows OS in der KVM

- Streamdeck
    - USB Devices hinzufügen
    - StreamDeck for Xplane 12
        - IP Adresse konfigurieren
    - X321 Streamdeck Profil
        - Fonts!
    - weitere Profile?
- My FS Flight

## SSH Key auf Server kopieren

Der einfachste Weg ist die Verwendung von `ssh-copy-id`:

**SSH Key erstellen (falls noch nicht vorhanden)**

- Key generieren: `ssh-keygen -t ed25519 -C "your@email.com"`
- Standardmäßig wird der Key in `~/.ssh/id_ed25519` gespeichert

**Key auf Server kopieren**

- Mit ssh-copy-id: `ssh-copy-id username@server`
- Alternativ manuell:
  ```bash
  cat ~/.ssh/id_ed25519.pub | ssh username@server "mkdir -p ~/.ssh && cat >> ~/.ssh/authorized_keys"
  ```

**Berechtigungen prüfen**

- Auf dem Server sollten folgende Berechtigungen gesetzt sein:
  ```bash
  chmod 700 ~/.ssh
  chmod 600 ~/.ssh/authorized_keys
  ```

## X-Plane Addons via KVM

Mehrere Windows-only X-Plane-Addons lassen sich in einer KVM-VM betreiben. Einrichtungsanleitungen und Konfigurationsdetails für einzelne Addons sind unter **[Addons → Via KVM](../../addon/kvm/index.md)** dokumentiert.