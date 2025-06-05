# X-Plane Configuration

!!! info "Note"
    This documentation is not yet complete and is currently under development (Work in Progress).

Here you will find important information about configuring X-Plane on Linux.

## Basic Settings

### Graphics Settings

The graphics settings include the choice between Vulkan and OpenGL with their respective advantages and disadvantages, the adjustment of monitor resolution and refresh rate, the configuration of anti-aliasing and texture quality, as well as the adjustment of shadows and reflections. Additionally, there are special graphics options for Nvidia and AMD graphics cards that affect weather and cloud quality.

#### Anti-Aliasing in X-Plane

Aliasing is a phenomenon that occurs due to the discrete sampling of a continuous signal, as described by the **Nyquist-Shannon Theorem**. This theorem states that the sampling frequency must be at least twice as high as the highest signal frequency to avoid aliasing artifacts. In computer graphics, insufficient sampling frequency leads to stair-stepping effects, especially at edges that are not aligned with the pixel grid.

X-Plane offers various anti-aliasing techniques. **SSAA (Super Sampling Anti-Aliasing)** increases the resolution of the rendered image, for example from 1920x1080 to 3840x2160 at 2x SSAA. The memory and computational requirements grow quadratically, which is why this technique is no longer used in newer versions of X-Plane.

**FXAA (Fast Approximate Anti-Aliasing)** is a post-processing technique for edge smoothing. It is computationally efficient and requires no additional memory, but can lead to blurry instruments, especially at 1080p. At 4K resolutions, FXAA shows better results.

**MSAA (Multi-Sample Anti-Aliasing)** is a hardware-implemented technique with a coverage mask per pixel. It is particularly effective at geometric edges but has difficulties with transparent geometries. In X-Plane 12.1, these problems were improved through Alpha-to-Coverage and Alpha-to-One.

X-Plane uses deferred rendering, where metadata is stored in a G-buffer. This reduces overdraw but increases complexity with MSAA, as lighting steps must be executed per sample. The render pipeline includes numerous intermediate steps that further increase complexity.

Not all aliasing artifacts are due to MSAA limitations. Post-processing effects such as Screen-Space Reflections (SSR) can cause artifacts, for example through inaccurate reflections (e.g., sky on objects). These artifacts are not geometric in nature and therefore cannot be fixed by MSAA. FXAA can smooth such edges but does not remove the underlying faulty information.

#### Interior Lighting and PBR

The lighting in X-Plane is based on **Physically Based Rendering (PBR)**, which leads to realistic but also complex lighting effects. Particularly in interior spaces like the cockpit, this can result in unexpected lighting effects. X-Plane is fundamentally capable of distinguishing between interior and exterior areas. This becomes particularly evident when switching to the free camera (key "C"), as the interior lighting adjusts accordingly. However, external light sources such as sky light or atmospheric effects (e.g., sunset) can influence the interior lighting.

The PBR implementation in X-Plane simulates realistic light reflections and absorptions. Materials are influenced by their environment - a cockpit in a pink hangar would take on a corresponding tint. Weather conditions like an orange sunset affect the cockpit lighting, and each material reacts differently to light based on its physical properties.

The current render pipeline of X-Plane has some technical limitations. Each pixel is calculated independently and in parallel, without context about the surrounding geometry. The detection of shielding, for example when a cockpit shouldn't "see" the sky, is computationally intensive. Particularly with narrow geometries like cockpit edges or wing curves, unwanted light from the environment can be captured.

Screen-Space Reflections (SSR) can lead to visible artifacts. Shimmering reflections, like on wet asphalt, can occur due to missing denoising techniques. The lack of ray coherence can lead to uneven reflections. A complete solution to these problems would require significant computational power and drastically reduce the frame rate.

The optimization of interior lighting and the reduction of lighting artifacts have a high priority in X-Plane's development. These problems are among the most common complaints that deter potential users from X-Plane 12. However, the complexity of the implementation requires careful balancing between visual quality and performance.

#### Driver-Based MSAA

MSAA can also be forced through the graphics driver. This leads to faster execution but also to less accurate shading, as the complex X-Plane render pipeline is not taken into account. The driver implementation cannot fully account for the specific requirements of the X-Plane render pipeline.

#### Optimization Recommendations

For optimal image quality, we recommend the following steps: First, FSR should be disabled (slider at maximum). Then, multisampling (MSAA) can be gradually increased, checking performance and image quality after each adjustment. Additional levels can be added if necessary. FXAA can be optionally enabled, taking into account its impact on image sharpness.

If these measures do not result in satisfactory image quality, consideration should be given to using a monitor with higher resolution. A higher native resolution significantly reduces edge flickering but requires a correspondingly powerful graphics card.

#### Conclusion and Outlook

Aliasing is a complex problem that is complicated by physical limits (Nyquist-Shannon Theorem) and the complexity of modern render pipelines. A solution requires improvements in the render pipeline, such as optimized SSR implementations. Currently, no immediate AA improvements are planned for X-Plane 12.2, but continuous optimization work is ongoing.

### Audio Settings

The audio configuration includes the selection of the audio engine between OpenAL and FMOD, precise volume control for different sound sources, configuration of 3D audio settings, setup of external sound cards, and optimization of microphone settings for online flying.

### Controls

The control configuration includes precise calibration of joystick and gamepad, adjustment of keyboard mapping, configuration of rudder pedals, setup of a multi-monitor configuration, and fine-tuning of VR controller settings.

## Performance Optimization

### Rendering Options

The rendering options include detailed settings for object density and view distance, configuration of autogen buildings and vegetation, adjustment of water and cloud effects, control of aircraft and traffic density, and setting of weather complexity.

### Memory Management

The memory management includes optimization of VRAM usage, configuration of RAM paging, adjustment of cache settings, management of Ortho4XP tiles, and implementation of efficient scenery loading strategies.

## Troubleshooting

### Common Issues
* Graphics Driver Conflicts
* Audio Problems
* Performance Drops
* Crashes and Freezes
* Addon Compatibility Issues

### Log Files
* Log.txt: Main Log File
* X-Plane Installer Logs
* Driver Logs
* Addon-specific Logs
* Enabling Debug Modes

**Note regarding X-Plane 12.2:**
Starting with version 12.2.0, X-Plane automatically generates both a new `Log.txt` and `Log_ATC.txt` file upon each startup. This behavior has been observed in a test environment without additional add-ons and appears to be a specific characteristic of the 12,2 version, rather than indicating incompatibilities with third-party software or plugins. 