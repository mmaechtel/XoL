# Research: udev Rules for Persistent USB Flight Controller Naming on Linux

**Date:** 2026-02-14
**Scope:** Debian 12/13, flight simulation controllers, X-Plane 12
**Sources:** 2024-2026 primary documentation + stable kernel/udev reference docs

---

## 1. Identifying USB Device Attributes

### 1.1 Quick Overview with lsusb

```bash
lsusb
```

Output format:
```
Bus 003 Device 005: ID 044f:b10a ThrustMaster, Inc. T.16000M Joystick
Bus 003 Device 006: ID 06a3:0763 Saitek PLC Pro Flight Rudder Pedals
```

The `ID` field shows `idVendor:idProduct`. For verbose output including serial numbers:

```bash
lsusb -v -d 044f:b10a 2>/dev/null | grep -E "idVendor|idProduct|iSerial|iProduct"
```

The `iSerial` field shows the device serial number. If `iSerial` is `0` or absent, the device has no serial number.

### 1.2 Detailed Attributes with udevadm

To get all matchable attributes for a specific device:

```bash
# Find the device first
ls /dev/input/by-id/ | grep -i joystick

# Get the full attribute walk for an event device
udevadm info --attribute-walk --name=/dev/input/event15
```

This traverses the device hierarchy (child to parent) and prints every attribute usable in udev rules. Key attributes from the output:

```
looking at device '/devices/pci0000:00/0000:00:14.0/usb3/3-2/3-2.1/3-2.1:1.0/0003:044F:B10A.0005/input/input15/event15':
    KERNEL=="event15"
    SUBSYSTEM=="input"
    ...

looking at parent device '/devices/pci0000:00/0000:00:14.0/usb3/3-2/3-2.1/3-2.1:1.0/0003:044F:B10A.0005/input/input15':
    KERNELS=="input15"
    SUBSYSTEMS=="input"
    ATTRS{name}=="Thrustmaster T.16000M"
    ...

looking at parent device '/devices/pci0000:00/0000:00:14.0/usb3/3-2/3-2.1':
    KERNELS=="3-2.1"
    SUBSYSTEMS=="usb"
    ATTRS{idVendor}=="044f"
    ATTRS{idProduct}=="b10a"
    ATTRS{serial}==""
    ATTRS{devpath}=="2.1"
    ATTRS{busnum}=="3"
    ...
```

**Important distinction:**
- `KERNEL` / `ATTR` / `SUBSYSTEM` -- match the **current** device node only
- `KERNELS` / `ATTRS` / `SUBSYSTEMS` -- search **upward** through parent devices

A single rule can combine attributes from the device itself and from **one** parent device. You cannot mix attributes from different parent levels in one rule.

### 1.3 Environment Properties

```bash
udevadm info --query=property --name=/dev/input/event15
```

Shows properties like:
```
ID_VENDOR_ID=044f
ID_MODEL_ID=b10a
ID_INPUT_JOYSTICK=1
ID_PATH=pci-0000:00:14.0-usb-0:2.1:1.0
ID_PATH_TAG=pci-0000_00_14_0-usb-0_2_1_1_0
DEVPATH=/devices/pci0000:00/0000:00:14.0/usb3/3-2/3-2.1/...
```

These can be matched with `ENV{key}` in rules.

### 1.4 Devices Without Serial Numbers

**Most flight sim controllers do NOT expose USB serial numbers.** This is a widespread issue across consumer joystick hardware. When `iSerial == 0`, the device has no programmed serial number.

**Confirmed behavior by manufacturer:**
- **Thrustmaster:** Generally no serial numbers on TCA, T.16000M, TWCS, T-Flight series. The Warthog (some batches) may have serials.
- **Logitech/Saitek:** X52, X56, Pro Flight Yoke, Rudder Pedals -- generally no serial numbers.
- **VKB:** Gladiator NXT and Gunfighter devices **do expose serial numbers** (e.g., `iSerial: "0042"`). This is a deliberate design choice by VKB.
- **Virpil:** Documentation does not confirm serial number support. Testing required.

### 1.5 Distinguishing Multiple Identical Devices

When two devices share the same `idVendor:idProduct` and have no serial numbers, the only reliable differentiator is the **physical USB port path**.

**Method 1: KERNELS (USB port path)**

```bash
udevadm info --attribute-walk --name=/dev/input/event15 | grep KERNELS
```

The USB port path looks like `3-2.1` (Bus 3, port 2, hub port 1). This is consistent across reboots as long as the device stays plugged into the same physical port.

**Method 2: ATTRS{devpath}**

```bash
udevadm info --attribute-walk --name=/dev/input/event15 | grep devpath
```

Shows the port topology like `"2.1"`.

**Method 3: ENV{ID_PATH}**

```bash
udevadm info --query=property --name=/dev/input/event15 | grep ID_PATH
```

Shows a fully qualified path like `pci-0000:00:14.0-usb-0:2.1:1.0`.

---

## 2. udev Rule Syntax

### 2.1 Rule File Placement

Rules go in `/etc/udev/rules.d/` with `.rules` extension. Files are processed in lexicographic order across all rule directories:

| Directory | Priority | Purpose |
|-----------|----------|---------|
| `/etc/udev/rules.d/` | Highest | Admin overrides |
| `/run/udev/rules.d/` | Medium | Temporary/runtime |
| `/usr/lib/udev/rules.d/` | Lowest | Package defaults |

**Naming convention:** `NN-descriptive-name.rules` where `NN` is a number controlling order. For flight sim controllers:

- `70-flight-controllers.rules` -- after system defaults (60-persistent-input.rules) but before most custom rules
- Lower numbers run first; for symlinks and permissions, 70-89 is typical

### 2.2 Matching Keys (use `==` or `!=`)

| Key | Matches | Scope |
|-----|---------|-------|
| `KERNEL` | Device node name | Current device |
| `SUBSYSTEM` | Device subsystem | Current device |
| `ATTR{file}` | sysfs attribute | Current device |
| `KERNELS` | Kernel name | Current + parents |
| `SUBSYSTEMS` | Subsystem | Current + parents |
| `ATTRS{file}` | sysfs attribute | Current + parents |
| `ENV{key}` | Device property | Current device |
| `ACTION` | Event type | add, remove, change |

### 2.3 Action Keys (use `=` or `+=`)

| Key | Effect |
|-----|--------|
| `SYMLINK+=` | Create symlink (append to list) |
| `MODE=` | Set file permissions |
| `GROUP=` | Set group ownership |
| `OWNER=` | Set user ownership |
| `ENV{key}=` | Set device property |
| `RUN+=` | Execute program |
| `TAG+=` | Add device tag |

### 2.4 String Substitution

| Token | Meaning |
|-------|---------|
| `$kernel` / `%k` | Kernel device name |
| `$number` / `%n` | Kernel device number |
| `$attr{file}` / `%s{file}` | sysfs attribute value |
| `$env{key}` / `%E{key}` | Device property value |

### 2.5 Basic Rule: Permission + Symlink by VID:PID

```
# Thrustmaster T.16000M -- permission and symlink
KERNEL=="event*", SUBSYSTEM=="input", \
    ATTRS{idVendor}=="044f", ATTRS{idProduct}=="b10a", \
    MODE="0660", GROUP="input", \
    SYMLINK+="input/flight-stick"
```

### 2.6 Matching by USB Port Path (for identical devices)

```
# Left throttle quadrant (always plugged into USB port 3-2.1)
KERNEL=="event*", SUBSYSTEM=="input", \
    ATTRS{idVendor}=="044f", ATTRS{idProduct}=="0407", \
    KERNELS=="3-2.1", \
    MODE="0660", GROUP="input", \
    SYMLINK+="input/throttle-left"

# Right throttle quadrant (always plugged into USB port 3-2.2)
KERNEL=="event*", SUBSYSTEM=="input", \
    ATTRS{idVendor}=="044f", ATTRS{idProduct}=="0407", \
    KERNELS=="3-2.2", \
    MODE="0660", GROUP="input", \
    SYMLINK+="input/throttle-right"
```

**Caveat:** The USB port path changes if devices are moved to different physical ports or if a USB hub is added/removed.

### 2.7 Complete Multi-Device Example

File: `/etc/udev/rules.d/70-flight-controllers.rules`

```
# === Flight Sim Controller Permissions & Symlinks ===
#
# Find attributes with:
#   udevadm info --attribute-walk --name=/dev/input/eventNN
#   lsusb -v -d VVVV:PPPP
#
# Reload:
#   sudo udevadm control --reload-rules && sudo udevadm trigger

# --- Thrustmaster T.16000M Joystick ---
KERNEL=="event*", SUBSYSTEM=="input", \
    ATTRS{idVendor}=="044f", ATTRS{idProduct}=="b10a", \
    MODE="0660", GROUP="input", \
    SYMLINK+="input/flight-stick"

# --- Thrustmaster TWCS Throttle ---
KERNEL=="event*", SUBSYSTEM=="input", \
    ATTRS{idVendor}=="044f", ATTRS{idProduct}=="b687", \
    MODE="0660", GROUP="input", \
    SYMLINK+="input/flight-throttle"

# --- Saitek Pro Flight Rudder Pedals ---
KERNEL=="event*", SUBSYSTEM=="input", \
    ATTRS{idVendor}=="06a3", ATTRS{idProduct}=="0763", \
    MODE="0660", GROUP="input", \
    SYMLINK+="input/flight-rudder"

# --- VKB Gladiator NXT (Right) ---
KERNEL=="event*", SUBSYSTEM=="input", \
    ATTRS{idVendor}=="231d", ATTRS{idProduct}=="0200", \
    MODE="0660", GROUP="input", \
    SYMLINK+="input/vkb-stick-right"

# --- VKB Gladiator NXT (Left) ---
KERNEL=="event*", SUBSYSTEM=="input", \
    ATTRS{idVendor}=="231d", ATTRS{idProduct}=="0201", \
    MODE="0660", GROUP="input", \
    SYMLINK+="input/vkb-stick-left"

# --- HOTAS Warthog Joystick ---
KERNEL=="event*", SUBSYSTEM=="input", \
    ATTRS{idVendor}=="044f", ATTRS{idProduct}=="0402", \
    MODE="0660", GROUP="input", \
    SYMLINK+="input/warthog-stick"

# --- HOTAS Warthog Throttle ---
KERNEL=="event*", SUBSYSTEM=="input", \
    ATTRS{idVendor}=="044f", ATTRS{idProduct}=="0404", \
    MODE="0660", GROUP="input", \
    SYMLINK+="input/warthog-throttle"
```

### 2.8 Permission-Only Rule (no symlink)

For cases where you just need X-Plane to access the device:

```
# Grant access to all Thrustmaster devices
KERNEL=="event*", SUBSYSTEM=="input", \
    ATTRS{idVendor}=="044f", \
    MODE="0660", GROUP="input"
```

### 2.9 Using hidraw Subsystem

Some devices (VKB, Virpil) need hidraw access for configuration tools:

```
# VKB hidraw access
SUBSYSTEM=="hidraw", ATTRS{idVendor}=="231d", \
    MODE="0660", GROUP="input"

# Virpil hidraw access
SUBSYSTEM=="hidraw", ATTRS{idVendor}=="3344", \
    MODE="0660", GROUP="input"
```

---

## 3. Reloading and Testing Rules

### 3.1 Reload Rules

```bash
sudo udevadm control --reload-rules
```

This tells `systemd-udevd` to reload all rule files. **However, existing devices are NOT re-evaluated.** New rules only apply when:

- A device is hotplugged (unplugged and plugged back in)
- `udevadm trigger` is used to synthetically re-trigger events

### 3.2 Trigger Re-evaluation

```bash
# Re-trigger ALL input devices
sudo udevadm trigger --subsystem-match=input

# Re-trigger a specific device
sudo udevadm trigger --name-match=/dev/input/event15
```

### 3.3 Test Rules Without Applying

```bash
# Dry-run rule evaluation for a device
sudo udevadm test $(udevadm info --query=path --name=/dev/input/event15)
```

This shows exactly which rules fire and what actions would be taken, without actually modifying anything. Very useful for debugging.

### 3.4 Monitor Live Events

```bash
# Watch device add/remove events in real-time
udevadm monitor --property --udev
```

Then plug/unplug the controller to see all properties assigned.

### 3.5 Verify Symlinks

After reloading and triggering (or re-plugging):

```bash
ls -la /dev/input/flight-*
# Should show symlinks pointing to eventNN
```

### 3.6 Debug Logging

```bash
# Enable verbose udev logging
sudo udevadm control --log-priority=debug
# Check logs
journalctl -u systemd-udevd -f

# Restore normal logging
sudo udevadm control --log-priority=err
```

---

## 4. Flight Sim USB Device Reference

### 4.1 Known Vendor and Product IDs

#### Thrustmaster (VID: 044f)

| PID | Device |
|-----|--------|
| `b10a` | T.16000M Joystick |
| `b687` | TWCS Throttle |
| `b678` | T.Flight Rudder Pedals |
| `b679` | T-Rudder |
| `b108` | T-Flight HOTAS X |
| `0402` | HOTAS Warthog Joystick |
| `0404` | HOTAS Warthog Throttle |
| `0407` | TCA Quadrant Eng 1&2 (Airbus) |
| `0408` | TCA Quadrant Eng 3&4 (Airbus) |
| `040a` | TCA Quadrant Boeing 1&2 |
| `040b` | TCA Quadrant Boeing 3&4 |
| `b68e` | TPR Rudder Pedals |
| `0400` | HOTAS Cougar |

**Note:** The TCA Sidestick Airbus and TCA Yoke Boeing are not yet in the public USB ID databases. Their PIDs must be determined with `lsusb` on the actual hardware. They use VID `044f`.

#### Logitech/Saitek (VID: 06a3 for Saitek, 046d for Logitech-branded)

| PID | Device | VID |
|-----|--------|-----|
| `075c` | X52 Flight Controller | `06a3` |
| `0762` | X52 Pro Flight Control System | `06a3` |
| `0bac` | Pro Flight Yoke | `06a3` |
| `0c2d` | Pro Flight Throttle Quadrant | `06a3` |
| `0763` | Pro Flight Rudder Pedals | `06a3` |
| `0764` | Pro Flight Combat Rudder | `06a3` |

**Note:** The X56 Rhino may appear under either VID `06a3` (original Saitek) or `046d` (Logitech rebrand, post-2018). Check with `lsusb`.

#### VKB (VID: 231d)

| PID | Device |
|-----|--------|
| `0200` | Gladiator NXT (Right) |
| `0201` | Gladiator NXT (Left) |
| `0131` | Gladiator Modern Combat Pro |

VKB devices are known to **expose USB serial numbers** (`iSerial`), making them distinguishable even when using identical models. VKB uses a unique PID per hand (left/right), which simplifies udev rules.

#### Virpil (VID: 3344)

| PID | Device |
|-----|--------|
| `0194` | MongoosT-50CM3 Throttle |
| `0391` | VPC Stick MT-50CM3 |
| `43f5` | WarBRD-D Joystick (Right) |
| `8194` | MongoosT-50CM3 Throttle (Left variant) |

**Note:** Virpil PIDs may vary by firmware version and configuration. Always verify with `lsusb`.

### 4.2 Serial Number Availability

| Manufacturer | Serial Numbers? | Notes |
|-------------|----------------|-------|
| Thrustmaster | Generally **no** | Some Warthog batches may have them |
| Logitech/Saitek | Generally **no** | -- |
| VKB | **Yes** | Deliberate design; unique per device |
| Virpil | **Unconfirmed** | Must test with `lsusb -v` |
| CH Products | Generally **no** | Legacy devices |

### 4.3 Multiple HID Interfaces per Device

Many flight controllers register as **multiple input devices** in Linux:

- **HOTAS Warthog Throttle:** Registers as 2-3 event devices (main axes, buttons, hat switches may be separate)
- **VKB Gladiator:** May register multiple interfaces for different axis groups
- **Thrustmaster TCA Quadrant:** Each engine pair (1&2, 3&4) is a separate USB device with its own PID

This means a single physical controller may create multiple `/dev/input/event*` nodes. When writing symlink rules, the `KERNEL=="event*"` match will fire for **each** interface. To target only the primary input interface, add:

```
KERNEL=="event*", SUBSYSTEM=="input", \
    ATTRS{idVendor}=="044f", ATTRS{idProduct}=="0404", \
    ENV{ID_INPUT_JOYSTICK}=="1", \
    SYMLINK+="input/warthog-throttle"
```

The `ENV{ID_INPUT_JOYSTICK}=="1"` ensures only the joystick-classified interface gets the symlink.

---

## 5. X-Plane Specific Considerations

### 5.1 How X-Plane Accesses Joysticks on Linux

- X-Plane uses **SDL2** for joystick input
- SDL2 on Linux uses the **evdev** backend (`/dev/input/event*`), NOT the legacy joydev interface (`/dev/input/js*`)
- X-Plane reads `/dev/input/event*` files and identifies any device with axes, buttons, or hat switches as a potential joystick
- **Permissions requirement:** The user running X-Plane must have read access to the event device files. Default Debian installs often restrict these to root

### 5.2 SDL2 Joystick GUID Format

SDL2 constructs a 128-bit GUID from device properties:

```
Bytes 0-1:   Bus type (USB = 0x0003, little-endian)
Bytes 2-3:   0x0000
Bytes 4-5:   Vendor ID (little-endian)
Bytes 6-7:   0x0000
Bytes 8-9:   Product ID (little-endian)
Bytes 10-11: 0x0000
Bytes 12-13: Version (little-endian)
Bytes 14-15: 0x0000
```

**Critical insight:** The GUID contains VID:PID but **NOT** the serial number or USB port path. Two identical devices produce **identical GUIDs**. X-Plane uses these GUIDs to match joystick configurations.

### 5.3 Device Ordering Problem

**The core issue:** Linux assigns `/dev/input/event*` numbers dynamically at boot time. The order depends on:

- USB bus enumeration order
- Kernel module loading order (non-deterministic with udev)
- Hub topology scanning order

If event numbers change between reboots, X-Plane may:

1. Assign the wrong controller to the wrong "slot" in its settings
2. Swap axis assignments between devices
3. In the worst case, fail to recognize a previously configured device

X-Plane stores joystick settings in `X-Plane 12/Output/preferences/X-Plane Joystick Settings.prf`. The `.prf` file uses `_joy_location` entries that reference the device by VID/PID. Since all devices of the same model share the same VID/PID, X-Plane cannot distinguish them when event numbers shuffle.

### 5.4 Does X-Plane Respect Symlinks?

**No.** X-Plane (via SDL2) **enumerates `/dev/input/event*` devices directly** and does not follow or use symlinks. The symlinks created by udev rules are useful for:

- **Diagnostic purposes** (quickly identifying which event device is which)
- **Other tools** (evdev-joystick, fftest, custom scripts)
- **NOT for X-Plane device matching**

### 5.5 What Actually Helps with X-Plane Device Ordering

**For different device types** (e.g., one stick + one throttle + one rudder pedal): The VID:PID is different for each, so X-Plane can re-match them regardless of event number changes. udev rules are **not needed** for ordering.

**For multiple identical devices** (e.g., two VKB Gladiator NXT): This is where problems occur. Potential solutions:

1. **VKB devices with serial numbers:** X-Plane can theoretically distinguish them via SDL2 serial number support (SDL 2.24+). Whether X-Plane 12 actually uses this depends on its SDL2 integration.

2. **Different models with different PIDs:** VKB solves this by using different PIDs for left (0201) and right (0200) versions. This is the most reliable solution.

3. **Consistent USB port assignment:** Ensure each device is always plugged into the same physical USB port. While udev rules can create port-specific symlinks for your own reference, X-Plane still relies on event device enumeration.

### 5.6 X-Plane Joystick Config Files

- **`.prf` file:** `Output/preferences/X-Plane Joystick Settings.prf` -- stores per-device axis/button assignments, null zones, sensitivity curves. References devices by VID/PID.
- **`.joy` files:** `Resources/joystick configs/*.joy` -- manufacturer/community default configurations. Matched by `ID: VID:0xNNNNPID:0xNNNN` or device name.
- **Platform-specific:** `.joy` files have per-OS sections (`OS: Linux`). Axis indices differ between platforms.

---

## 6. Modern Alternatives and Complementary Approaches

### 6.1 /dev/input/by-id/ and /dev/input/by-path/

These directories are created automatically by udev (via `60-persistent-input.rules`) and contain stable symlinks:

```bash
ls -la /dev/input/by-id/ | grep joystick
# usb-Thrustmaster_T.16000M-event-joystick -> ../event15
# usb-Thrustmaster_T.16000M-joystick -> ../js0

ls -la /dev/input/by-path/ | grep joystick
# pci-0000:00:14.0-usb-0:2.1:1.0-event-joystick -> ../event15
```

**`by-id/`** names are constructed from manufacturer name + model name (derived from USB descriptors). They are **stable across reboots** but **NOT unique** for identical devices without serial numbers.

**`by-path/`** names encode the physical port path. They are **unique per port** and **stable across reboots**, but change if the device is moved to a different port.

**Do these solve the X-Plane problem?** Partially:
- They provide stable naming for scripts and tools
- X-Plane/SDL2 does NOT use these symlinks for enumeration
- They help you **diagnose** which event device corresponds to which controller

### 6.2 systemd .link Files

systemd `.link` files (in `/etc/systemd/network/`) are designed for **network interface** naming only. They have **no effect on input devices**. Not a viable alternative for joystick naming.

### 6.3 SDL2 Environment Variables

| Variable | Effect |
|----------|--------|
| `SDL_JOYSTICK_DEVICE` | Force-specify device paths (colon-separated). Overrides automatic discovery. |
| `SDL_JOYSTICK_DISABLE_UDEV` | Disable udev-based discovery, fall back to filesystem scanning. |
| `SDL_LINUX_JOYSTICK_CLASSIC` | Use legacy `/dev/input/js*` interface instead of evdev. |
| `SDL_JOYSTICK_HIDAPI` | `0` = disable HIDAPI, use evdev. `1` = prefer HIDAPI. |

**Practical use for X-Plane:**

```bash
# Force specific device order
SDL_JOYSTICK_DEVICE=/dev/input/event15:/dev/input/event16:/dev/input/event17 ./X-Plane-x86_64
```

This is a **viable workaround** for device ordering, but:
- Requires knowing event numbers (which change across reboots)
- Can be combined with by-path symlinks for stability:
  ```bash
  SDL_JOYSTICK_DEVICE=/dev/input/by-path/pci-0000:00:14.0-usb-0:2.1:1.0-event-joystick:/dev/input/by-path/pci-0000:00:14.0-usb-0:2.2:1.0-event-joystick
  ```
- Must be set before X-Plane starts (via wrapper script or desktop file)

### 6.4 udev Joystick Blacklist

The project [udev-joystick-blacklist](https://github.com/denilsonsa/udev-joystick-blacklist) addresses a related problem: non-joystick devices (keyboards, mice, tablets) being misidentified as joysticks in Linux. This causes X-Plane to detect phantom controllers.

Solution: Install the blacklist rules that unset `ID_INPUT_JOYSTICK` on known non-joystick devices:

```bash
sudo curl -o /etc/udev/rules.d/51-these-are-not-joysticks.rules \
    https://raw.githubusercontent.com/denilsonsa/udev-joystick-blacklist/master/51-these-are-not-joysticks.rules
sudo udevadm control --reload-rules
sudo udevadm trigger
```

### 6.5 Practical Recommendation for X-Plane on Linux

**Best approach (in order of effectiveness):**

1. **Use controllers with different VID:PID pairs.** X-Plane identifies devices by VID:PID. As long as each controller model is unique, reboot-stable ordering is automatic. Most typical setups (one stick + one throttle + one rudder) already satisfy this.

2. **For identical devices:** Choose hardware that uses different PIDs per variant (VKB left/right) or exposes serial numbers (VKB).

3. **Install the joystick blacklist** to prevent phantom controllers.

4. **Set permissions via udev rules** so X-Plane can access event devices without root.

5. **Create custom symlinks** for diagnostic convenience and for use with calibration/testing tools.

6. **If ordering is still unstable:** Use a wrapper script that sets `SDL_JOYSTICK_DEVICE` with by-path symlinks.

---

## 7. Complete Practical Setup

### 7.1 Step-by-Step for Debian 12/13

**Step 1: Identify your devices**

```bash
# Quick overview
lsusb | grep -iE "thrust|saitek|logitech|vkb|virpil"

# Detailed attributes (replace eventNN)
udevadm info --attribute-walk --name=/dev/input/event15 | head -50

# Check for serial numbers
sudo lsusb -v -d 044f: 2>/dev/null | grep -E "idVendor|idProduct|iSerial|iProduct"
```

**Step 2: Verify group membership**

```bash
# User must be in 'input' group
groups $USER | grep input

# Add if missing
sudo usermod -aG input $USER
# Log out and back in for this to take effect
```

**Step 3: Create rules file**

```bash
sudo nano /etc/udev/rules.d/70-flight-controllers.rules
```

Content (adapt VID:PID to your hardware):

```
# Flight Sim Controller Permissions & Symlinks
# Reload: sudo udevadm control --reload-rules && sudo udevadm trigger

# Thrustmaster T.16000M
KERNEL=="event*", SUBSYSTEM=="input", ATTRS{idVendor}=="044f", ATTRS{idProduct}=="b10a", \
    MODE="0660", GROUP="input", SYMLINK+="input/flight-stick"

# Thrustmaster TWCS Throttle
KERNEL=="event*", SUBSYSTEM=="input", ATTRS{idVendor}=="044f", ATTRS{idProduct}=="b687", \
    MODE="0660", GROUP="input", SYMLINK+="input/flight-throttle"

# Saitek Pro Flight Rudder Pedals
KERNEL=="event*", SUBSYSTEM=="input", ATTRS{idVendor}=="06a3", ATTRS{idProduct}=="0763", \
    MODE="0660", GROUP="input", SYMLINK+="input/flight-rudder"
```

**Step 4: Reload and test**

```bash
sudo udevadm control --reload-rules
sudo udevadm trigger --subsystem-match=input

# Verify
ls -la /dev/input/flight-*
```

**Step 5: Test with udevadm**

```bash
# Dry-run to verify rules fire correctly
sudo udevadm test $(udevadm info --query=path --name=/dev/input/event15) 2>&1 | grep -E "SYMLINK|MODE|GROUP"
```

---

## Sources

1. [Arch Wiki: udev](https://wiki.archlinux.org/title/Udev) -- comprehensive udev reference with rule syntax, udevadm commands, and examples
2. [freedesktop.org: udev man page](https://www.freedesktop.org/software/systemd/man/latest/udev.html) -- official systemd-udevd reference, complete key/operator documentation
3. [Debian Wiki: udev](https://wiki.debian.org/udev) -- Debian-specific rule placement and naming conventions
4. [X-Plane Developer: Linux Joystick Permissions](https://developer.x-plane.com/2012/09/linux-joystick-permissions/) -- official X-Plane guidance on udev for joystick access
5. [X-Plane Developer: .joy File Specification](https://developer.x-plane.com/article/creating-joystick-configuration-joy-files/) -- joystick config format, VID:PID matching
6. [X-Plane KB: Using Joysticks on Linux](https://www.x-plane.com/kb/using-joysticks-x-plane-11-linux-systems/) -- official X-Plane Linux joystick article
7. [SDL GitHub Issue #4430: Joystick Enumeration Order](https://github.com/libsdl-org/SDL/issues/4430) -- SDL2 device ordering bug, SDL_JOYSTICK_DEVICE workaround
8. [SDL GitHub Issue #5366: Random Multijoystick Order](https://github.com/libsdl-org/SDL/issues/5366) -- identical VID:PID ordering problem, SDL_JOYSTICK_DISABLE_UDEV
9. [NASA IDF Wiki: Differentiating Identical Devices](https://github.com/nasa/IDF/wiki/Differentiating-Identical-Devices) -- KERNELS-based port matching for identical USB devices
10. [Virpil on Linux (GitHub)](https://github.com/LunaBaloona/Virpil_devices_on_Linux/blob/main/Linux_config_and_gaming.md) -- Virpil udev rules and hidraw access
11. [udev-joystick-blacklist (GitHub)](https://github.com/denilsonsa/udev-joystick-blacklist) -- preventing non-joystick devices from being misidentified
12. [game-devices-udev (Codeberg)](https://codeberg.org/fabiscafe/game-devices-udev) -- community-maintained udev rules for game controllers
13. [DeviceHunt USB ID Database: Thrustmaster](https://devicehunt.com/view/type/usb/vendor/044F) -- VID:PID reference for Thrustmaster
14. [DeviceHunt USB ID Database: Saitek](https://devicehunt.com/view/type/usb/vendor/06A3) -- VID:PID reference for Saitek/Logitech
15. [linux-hardware.org: VKB devices](https://linux-hardware.org/?id=usb:231d-0200) -- VKB USB IDs confirmed in Linux
16. [SDL2 Wiki: JoystickGUID](https://wiki.libsdl.org/SDL2/SDL_JoystickGUID) -- GUID construction format
17. [Gentoo Forums: Setting Joystick Order](https://forums.gentoo.org/viewtopic-p-7265636.html) -- community discussion of joystick ordering via udev
