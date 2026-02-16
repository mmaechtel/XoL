# Device Losses in X-Plane

## Introduction

Device losses are a known but difficult to analyze problem in X-Plane. The goal is to explain the nature of device losses, their causes, debugging challenges, and measures for problem resolution.

## Definition and Causes

A device loss is a crash of the Graphics Processing Unit (GPU), similar to a software crash on the CPU, but with specific challenges. GPUs execute shaders - small programs that handle tasks such as vertex data transformation, pixel calculations, or object culling. X-Plane uses numerous shader modules, each containing many shader variants. A device loss occurs when a shader or GPU command is executed incorrectly, signaled by the Vulkan error code `VK_ERROR_DEVICE_LOST`.

## Debugging Challenges

Debugging device losses is complex due to the following factors:

1. **Asynchronous Execution**: CPU and GPU work asynchronously, with the CPU often several frames ahead. A crash is only detected with delay, making cause analysis difficult.
2. **Limited Debugging Tools**: Shaders cannot be inspected step by step. The GPU state is only accessible after execution, and in case of a crash, often only fragmented data is available.
3. **Latency in Detection**: The operating system and graphics driver prioritize GPU recovery, leading to delays and visual artifacts before X-Plane registers the error.

## Problem Resolution Measures

For investigating device losses, the command line parameter `--aftermath` is recommended (see also [Configuration → GPU Debugging](../config.md#gpu-debugging) for a quick CLI reference). This activates the Aftermath library (supported for Nvidia, AMD, and Intel GPUs), which collects detailed diagnostic data. When a crash occurs, the message "Encountered a GPU crash!" is displayed, and the collected data helps developers identify the cause. However, Aftermath causes a performance impact and should be used selectively.

In X-Plane 12.2, Aftermath support was revised to insert checkpoints into the command stream for each draw or dispatch command. This fine-grained data enables more precise analysis of the GPU state after a crash. Earlier versions such as 12.06 and 12.1.0 significantly reduced device losses, for example through workarounds for Nvidia driver bugs.

## Misunderstandings

A common misconception is that device losses are caused by insufficient video memory (VRAM) - this is not the case. Plugins or scenery can only indirectly trigger device losses, for example through modifications to shader paths. A/B testing with disabled plugins is helpful for reproducible crashes but often ineffective for rare device losses.

## Conclusion

Device losses in X-Plane are GPU crashes that are difficult to debug due to the complexity of shaders and asynchronous CPU-GPU interaction. Tools like Aftermath and improved implementations in X-Plane 12.2 facilitate diagnosis. Users can contribute to problem resolution by submitting crash reports with Aftermath enabled. Future developments may further reduce the frequency of such errors.

## References

- "What's up with device losses in X-Plane anyways?". Available at: <https://developer.x-plane.com>. Accessed: 2024-05-09. 