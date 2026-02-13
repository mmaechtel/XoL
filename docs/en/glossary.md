---
title: Glossary
description: Term explanations around X-Plane and Linux
tags:
  - reference
---

# Glossary

## A

### Airport Enhancement Package (AEP)

A scenery addon by X-Codr Designs for X-Plane that enhances default airports with more detailed models, higher resolution textures, and new technologies. It replaces airport buildings, facades, ground objects, static vehicles, as well as runway lights, beacons, and navigation aids with modern versions. [More details](../addon/aep.md)

### Airport Elements

The various components of an airport in X-Plane, such as buildings, facades, ground objects, static vehicles, runway lights, beacons, and navigation aids. The [Airport Enhancement Package (AEP)](../addon/aep.md) enhances these elements with more detailed models and higher resolution textures.

### Airport Vegetation

The 3D vegetation elements on airports in X-Plane. In the [Airport Enhancement Package (AEP)](../addon/aep.md), the default airport vegetation is replaced with new, more detailed 3D models for a more realistic representation.

### AutoOrtho

A tool for X-Plane that integrates orthophotos directly into the flight simulator. It enables streaming of high-resolution aerial imagery as ground textures without the need to download and convert them beforehand. The software can be installed either as a pre-built binary or from source code.

## B

### Binary

A pre-compiled, executable file of a program. Unlike installation from source code, a binary can be executed directly without requiring additional compilation steps.

### Blade Element Theory

A calculation method in aerodynamics where an aircraft is divided into many small segments to simulate airflow and forces in real-time.

## C

### Compositor

A program that combines the contents of multiple windows into the final screen image. Under Wayland, the compositor also serves as the display server and window manager (e.g., Mutter for GNOME, KWin for KDE). Under X11, the compositor is a separate program that can be bypassed by fullscreen applications.

### Custom Scenery

A directory in X-Plane where additional scenery files are stored. This is also where AutoOrtho's generated ortho textures are integrated.

## D

### Display Server

Software that manages graphics output and input devices for applications. X11 (Xorg) and Wayland are the two display server protocols on Linux. X-Plane 12 supports only X11. See [Display Server](../displayserver.md).

### Docker

A platform for containerizing applications that enables packaging and running software in standardized units (containers). Docker simplifies the deployment and management of applications across different environments.

### DKMS (Dynamic Kernel Module Support)

A framework that enables automatic recompilation of kernel modules when kernel updates occur. Particularly important for drivers like Nvidia that are not included in the standard kernel.

### Dynamic Libraries

Also known as shared libraries, these are reusable collections of program code that can be loaded and shared by different programs at runtime. They typically have a .so (shared object) extension on Linux and allow for more efficient memory usage and easier updates.

## E

### evdev

Event Device — the Linux kernel input interface that exposes input devices via `/dev/input/event*`. X-Plane uses SDL2 with the evdev backend for controller detection. Not to be confused with the older joystick interface (`/dev/input/js*`).

## F

### FAA

Federal Aviation Administration - the US aviation authority that sets standards for flight simulations and training devices.

### FMOD

A proprietary audio engine by Firelight Technologies. X-Plane 12 uses FMOD Studio 2.02 for all audio output. On Linux, FMOD communicates with PulseAudio or PipeWire.

## G

### GUI (Graphical User Interface)

A graphical user interface that enables interaction with a program through graphical elements such as windows, buttons, and menus. In AutoOrtho, the GUI is used to configure the X-Plane directory and load ortho sets.

### Ground Markings

The markings and pavements on airports in X-Plane. In the [Airport Enhancement Package (AEP)](../addon/aep.md), these are replaced with new, high-resolution textures that support X-Plane 12's weather effects and create realistic patterns without repetition.

## H

### HDR

High Dynamic Range - a graphics technique that can display a particularly large brightness range, leading to more realistic lighting effects.

## K

### KVM (Kernel-based Virtual Machine)

A virtualization solution integrated into the Linux kernel that enables running virtual machines with near-native performance. KVM utilizes hardware virtualization features of modern processors for efficient virtualization.

## L

### ldd

A command-line program in Linux that displays all dynamic library dependencies of an executable file. It is an important diagnostic tool for identifying missing or incompatible libraries required for running a program like X-Plane.

### Linux

A free, open-source operating system known for its stability, security, and adaptability.

### Liquorix Kernel

An optimized version of the Linux kernel focused on performance. Often provides better response times and performance for desktop systems and gaming.

## N

### Nouveau

The default open-source driver for Nvidia graphics cards in Linux. Often disabled when installing the proprietary Nvidia driver.

### Nvidia Driver

Proprietary driver software from Nvidia for their graphics cards. Compared to the open-source Nouveau driver, it often provides better performance and more features, especially for 3D applications and gaming.

## O

### Ortho4XP

A tool for creating photorealistic landscape textures for X-Plane from various satellite image sources.

### Orthophotos

Orthophotos (or orthoimages) are geometrically corrected aerial photographs of the Earth's surface. In X-Plane, they are used as high-resolution ground textures to achieve a realistic representation of the landscape.

## P

### PBR

Physically Based Rendering - a graphics technique that simulates physical properties of materials and light to create realistic representations.

### Plugin

A software extension that adds additional functionality to X-Plane. Plugins can be developed by third parties.

### pyenv

A tool for managing multiple Python versions on a system. It allows installation and use of multiple Python versions side by side without affecting the system Python.

## R

### RADV

The open-source Vulkan driver for AMD GPUs within the Mesa driver stack. RADV is the default Vulkan driver on Linux systems with AMD graphics cards and is used directly by X-Plane 12.

## S

### scenery_packs.ini

A configuration file in X-Plane's Custom Scenery folder that determines the load order of installed scenery. AutoOrtho automatically adds entries with the prefix `z_ao_` here.

### Single-CPU

Describes the current architecture of X-Plane, where the main simulation runs on a single processor core.

## T

### 32-Bit Compatibility

The ability of a 64-bit Linux system to run and support 32-bit applications and libraries. This may be necessary for some programs or plugins that have not yet been optimized for 64-bit architectures. In Debian, 32-bit support is activated by adding the i386 architecture and installing corresponding libraries.

## V

### Vulkan API

A modern, cross-platform graphics interface with low overhead used by X-Plane for graphics rendering. Compared to OpenGL, Vulkan often provides better performance through more efficient CPU usage and more direct GPU control.

## W

### Wayland

A modern display server protocol for Linux, successor to X11. The compositor handles both display server and window manager duties. Wayland offers better security and per-monitor refresh rates, but X-Plane 12 cannot speak Wayland natively and uses XWayland instead. See [Display Server](../displayserver.md).

### Wine (Wine Is Not an Emulator)

A compatibility layer that enables running Windows programs on Linux. Wine translates Windows API calls to POSIX calls without emulating Windows itself.

## X

### X11 (Xorg)

The classic display server protocol for Linux, in use since 1984. A central X server manages all graphics and input. X-Plane speaks X11 natively. See [Display Server](../displayserver.md).

### X-Plane

A highly realistic flight simulator available for various platforms (Windows, macOS, Linux).

### XWayland

A compatibility layer that runs a complete X11 server inside a Wayland session. When an X11 application (like X-Plane) starts on a Wayland desktop, XWayland handles the translation automatically. The extra translation adds latency. See [Wayland Session](../displayserver_wayland.md).

### Xroads

A library for X-Plane 11 & 12 that optimizes the display of roads in Ortho4XP scenery.

## Z

### Zink

An OpenGL translation layer within Mesa that converts OpenGL commands into Vulkan commands. X-Plane 12 ships its own Zink driver so that plugins using OpenGL for rendering can work within the Vulkan render pipeline.
