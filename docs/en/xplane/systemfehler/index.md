# System Errors in X-Plane on Linux

When X-Plane on Linux doesn't work as expected, systematic diagnosis helps. This page points to the relevant sections of the documentation.

## Diagnostics and CLI Parameters

The command line is the most powerful troubleshooting tool on Linux. Log files, safe mode, targeted subsystem isolation, and reproducible benchmarks are covered in detail in:

**[Configuration → Troubleshooting](../config.md#troubleshooting)**

- Reading and interpreting log files (`Log.txt`, rotation, what to look for)
- Safe mode with `--safe_mode=GFX`, `--safe_mode=PLG` etc.
- Isolating audio (`--no_sound`), isolating controllers (`--no_joysticks`)
- Fullscreen issues under Wayland (`--window`, `--full`)
- Performance testing (`--fps_test`, `--require_fps`)
- Launch scripts with profiles (`--pref`, `--dref`)

## GPU Crashes (Device Loss)

A device loss is a GPU crash, signaled by `VK_ERROR_DEVICE_LOST`. Causes, debugging challenges, and Aftermath diagnostics are explained in:

**[Device Losses](geraeteverluste.md)**

- Definition and causes of device losses
- Why GPU debugging is difficult (asynchronous execution, limited tools)
- `--aftermath` for detailed GPU crash analysis
- Common misconceptions (VRAM is not the cause)

## Performance Issues

FPS drops, stutter, and bottlenecks are covered in:

**[Performance](../performance.md)**

## Support

- Official documentation: <https://www.x-plane.com/support>
- X-Plane forum: <https://forums.x-plane.org> — when reporting issues, always include `Log.txt`, error description, and reproduction steps
