# System Errors in X-Plane on Linux

When X-Plane on Linux doesn't work as expected, systematic isolation helps. Device losses — GPU crashes signaled by the Vulkan error code `VK_ERROR_DEVICE_LOST` — are particularly difficult to analyze because CPU and GPU work asynchronously and the crash is detected with delay. The Aftermath tool injects checkpoints into the GPU command stream and reconstructs the state at the time of the error. CLI parameters like safe mode and subsystem isolation narrow down the cause systematically.

## Performance Issues

FPS drops, stutter, and bottlenecks are covered in:

**[Performance](../setup_diagnose/performance.md)**

## GPU Crashes (Device Loss)

A device loss is a GPU crash, signaled by `VK_ERROR_DEVICE_LOST`. Causes, debugging challenges, and Aftermath diagnostics are explained in:

**[Device Losses](geraeteverluste.md)**

- Definition and causes of device losses
- Why GPU debugging is difficult (asynchronous execution, limited tools)
- `--aftermath` for detailed GPU crash analysis
- Common misconceptions (VRAM is not the cause)

## Diagnostics and CLI Parameters

Log files, safe mode, targeted subsystem isolation, and reproducible benchmarks:

**[Diagnostics and CLI Parameters](diagnose.md)**

## Support

- Official documentation: <https://www.x-plane.com/support>
- X-Plane forum: <https://forums.x-plane.org> — when reporting issues, always include `Log.txt`, error description, and reproduction steps
