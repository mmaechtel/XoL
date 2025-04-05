# Ortho4XP

Ortho4XP is a powerful tool for creating orthophotos for X-Plane. It enables the generation of high-resolution ground textures from satellite imagery and elevation data.

## Sources

Ortho4XP is available in two main versions:

1. **Original version** by Oscar Pilote:
   
   - [GitHub Repository](https://github.com/oscarpilote/Ortho4XP)
   - The original version with basic features
   - [Binaries available](https://github.com/kubilus1/autoortho/releases/tag/0.7.2)

2. **Fork by shred86**:
   
   - [GitHub Repository](https://github.com/shred86/Ortho4XP)
   - [Detailed Documentation](https://github.com/shred86/Ortho4XP/wiki)
   - Contains numerous improvements and new features
   - [Binaries for various operating systems](https://github.com/shred86/Ortho4XP/wiki/Installation)

## Installation

Ortho4XP can be installed in two ways:

### Installation with Binaries (recommended)

1. Download the appropriate version for your operating system:
   - Original version: [Releases](https://github.com/kubilus1/autoortho/releases/tag/0.7.2)
   - shred86 fork: [Installation page](https://github.com/shred86/Ortho4XP/wiki/Installation)
2. Extract the archive
3. Run the executable file

### Manual Installation

1. Download your preferred version of Ortho4XP
2. Make sure Python 3.x is installed
3. Install the required Python packages:
   ```bash
   pip install -r requirements.txt
   ```

### Alternative Installation for Linux

For Linux users, two alternative installation methods are available:
- Installation with Docker (see [Docker documentation](../docker.md))
- Installation with pyenv (see [pyenv documentation](../pyenv.md))

## Basic Usage

1. Start Ortho4XP using the Python file or executable:
   ```bash
   python Ortho4XP.py
   ```

2. In the main window, select:
   - The target area (Tile)
   - The desired zoom level (ZL)
   - The image source (e.g., Bing, Google, Here)

3. Click "Build" to start the process

## Features of the shred86 Fork

The shred86 fork offers numerous improvements over the original version:

### New Features

- Improved user interface with Dark Mode
- Extended configuration options
- Support for more image sources
- Improved error handling and logging
- Automatic updates

### Technical Improvements

- Optimized memory usage
- Faster processing
- Better error tolerance
- Extended compatibility with various systems

### Additional Features

- Batch processing of multiple tiles
- Extended mesh options
- Improved water masks
- Support for more elevation data sources
- Extended configuration files

## Important Notes

- Ortho4XP requires significant storage space for generated textures
- The quality of orthophotos depends on the chosen image source
- Processing can take several hours depending on area size and zoom level
- The shred86 fork offers better performance and more features
- Using binaries significantly simplifies the installation process
- For Linux users, Docker and pyenv provide flexible alternatives to direct installation

## Troubleshooting

If you encounter issues:
1. Check the log files in the Ortho4XP directory
2. Ensure all Python dependencies are installed
3. Consult the [shred86 fork documentation](https://github.com/shred86/Ortho4XP/wiki) for detailed guides
4. Visit the [X-Plane Forum](https://forums.x-plane.org/index.php?/forums/forum/310-ortho4xp/) for additional help 