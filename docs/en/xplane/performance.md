# X-Plane Performance

The performance of X-Plane is a crucial factor for a smooth and realistic flight experience. In this chapter, various aspects of performance measurement and optimization are examined.

## Performance Metrics

X-Plane offers various ways to measure and monitor performance:

### FPS (Frames per Second)

The FPS display is the most basic metric for performance in X-Plane. It shows how many frames per second the system calculates and displays. The display is located in the upper left corner of the screen by default, but it is not activated. In some installations, the display is already assigned to a hotkey (e.g., Shift+Ctrl+F), but this can be customized in the keyboard settings. For a smooth flight experience, the FPS rate should be consistently above 30 FPS. A rate below 19 FPS results in choppy movements and impairs playability, while 25–35 FPS is acceptable for most users. From 50 FPS onwards, the simulation is perceived as very smooth.

### Frame Time

Frame Time is an important metric that measures the time required to calculate a single frame. This measurement is particularly valuable for identifying performance bottlenecks, as it shows exactly where delays occur in the calculation process. The Frame Time can be viewed through the integrated X-Plane Performance Monitor, which provides detailed insights into the various phases of frame generation.

### CPU and GPU Usage

Monitoring CPU and GPU utilization is a crucial aspect of performance analysis. These metrics help identify hardware bottlenecks and determine whether the processor or graphics card is the limiting factor. Various system monitoring tools are available for this purpose, such as `htop` for CPU utilization or `nvidia-smi` for NVIDIA graphics cards. These tools provide detailed information about current utilization and can assist in optimizing system resources.

## Performance Measurement

### Internal Tools

#### X-Plane Performance Monitor

The integrated Performance Monitor in X-Plane provides detailed insights into:

- Frame Time
- CPU Usage
- GPU Usage
- Memory Usage
- Network Performance

#### Microprofiler

The Microprofiler in X-Plane is a powerful diagnostic tool available in the Developer Menu that provides detailed insights into the simulation's performance. It helps identify bottlenecks in CPU and GPU performance by breaking down the time required for various tasks during frame generation.

##### What is the Microprofiler?

The Microprofiler is a developer tool that measures the time required for different parts of the X-Plane simulation to calculate and render a frame. Unlike the simple FPS display (Frames per Second), which only shows the frame rate and rough CPU/GPU times, the Microprofiler provides a detailed breakdown of the individual processes that contribute to frame creation.

The Microprofiler shows:

- Time per task: How much time (in milliseconds) is required for specific tasks such as physics calculations, scenery rendering, cloud display, or plugin processing
- CPU and GPU utilization: Which component (CPU or GPU) limits the frame cycle
- Bottlenecks: Which specific processes take the most time and thus reduce FPS

##### Activation and Usage

To activate the Microprofiler in X-Plane, follow these steps:

1. Opening the Developer Menu:

    - Start X-Plane and load any scene (e.g., an aircraft on a runway)
    - Move the mouse to the top of the screen to display the menu bar
    - Click on "Developer" (in some versions, it may be called "Developer" or similar, depending on the language)

2. Activating the Microprofiler:

    - In the Developer menu, select the option "Toggle Microprofiler" or "Show Microprofiler"
    - A graphical display appears on the screen, showing performance data in real-time

3. Alternative method via configuration file:

    - In X-Plane Professional or modified installations, the Microprofiler can be activated via the JSON configuration file
    - Set the entry "developer::toggle_microprofiler": "visible" to make the option visible
    - This requires access to the configuration file and is intended for advanced users

4. Keyboard Shortcut (optional):

    - There is no standard keyboard shortcut for the Microprofiler in X-Plane
    - Plugins like "FlyWithLua" can be used to define custom shortcuts

##### Displayed Data and Interpretation

The Microprofiler provides a visual representation of frame generation time, divided into various categories:

1. Frame Time (Total Time per Frame):

    - Definition: The total time in milliseconds required to calculate and render a frame
    - Formula: Frame Time = 1000 ms / FPS
    - Example: At 30 FPS, the frame time is 1000/30 ≈ 33.3 ms

2. Task Categories:

    - Physics Calculations (Flight Model): Time for calculating flight behavior (e.g., aerodynamics, engines)
    - Scenery Rendering: Time for drawing landscapes, buildings, roads
    - Clouds and Weather: Time for displaying clouds, rain, or fog
    - Plugins: Time consumed by installed plugins
    - Swapchain Acquire: Time for synchronization between CPU and GPU
    - Other Tasks: AI aircraft, ATC, network communication, or VR rendering

3. CPU and GPU Time:

    - CPU Time: Time for calculations on the CPU (e.g., physics, plugins, scenery logic)
    - GPU Time: Time for rendering graphics (e.g., textures, shadows, clouds)
    - Interpretation:
        - High CPU Time: CPU is the bottleneck
        - High GPU Time: GPU is the bottleneck

##### Calculation Example

Suppose the Microprofiler shows the following values:

- FPS: 30
- Total Frame Time: 33.3 ms
- Task Distribution:
    - Physics Calculation: 10 ms
    - Scenery Rendering: 8 ms
    - Clouds/Weather: 7 ms
    - Plugins: 5 ms
    - Swapchain Acquire: 3 ms
- Total CPU Time: 20 ms
- Total GPU Time: 13 ms

Now it's possible to analyze in detail which parts (e.g., addons) contribute what kind of load to CPU and GPU.

### External Tools

#### System Monitoring

- **htop**: Detailed CPU and memory usage
- **nvidia-smi**: NVIDIA-specific performance metrics
- **glxgears**: Simple tool for checking OpenGL performance

#### Overlay Tools

- **MangoHUD**: An overlay for Linux that displays performance metrics
- **GOverlay**: Graphical user interface for MangoHUD
- **vulkaninfo**: Detailed information about Vulkan implementation

#### Benchmarking Tools

- **Phoronix Test Suite**: Comprehensive benchmarking suite
- **Unigine Heaven**: Graphics card benchmark
- **GLmark2**: OpenGL benchmark

## Practical Optimization Tips

Based on the FPS display and the Microprofiler, targeted optimizations can be made:

- **CPU Optimization**:

    - Reduction of the number of scenery objects and AI aircraft
    - Lowering of physics calculations per frame ("Flight Models per Frame" to 2–4)
    - Use of less complex add-ons
    - Reduction of cloud details

- **GPU Optimization**:

    - Reduction of texture resolution ("Texture Quality" to Medium or High)
    - Disabling or reducing anti-aliasing and shadows
    - Adjustment of cloud quality

- **General**:

    - Testing in a simple scenery to determine base FPS
    - Use of external tools for additional metrics
    - Regular performance checks with the Microprofiler

## Performance Optimization

### Graphics Settings

- Texture quality adjustment
- Object density optimization
- Cloud density setting
- Shadow quality adjustment

### System Optimization

- Using the Liquorix kernel for better performance
- NVIDIA driver settings optimization
- CPU governor settings adjustment
- Memory usage optimization

### Addon Management

- Monitoring addon performance impact
- Optimal addon loading order
- Regular cleanup of unnecessary addons

## Benchmarking

For systematic performance analysis, it is recommended to:

1. Create a standardized test flight
2. Document base settings
3. Conduct tests with different configurations
4. Compare results

## Troubleshooting

Common performance issues and their solutions:

- Stuttering and frame drops
- High CPU usage
- GPU overload
- Memory leaks
- Network latency

## Best Practices

- Conduct regular performance measurements
- Document changes
- Systematically test configuration changes
- Backup settings before major changes 