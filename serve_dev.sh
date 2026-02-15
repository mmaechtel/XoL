#!/bin/bash

# Create video symlink if missing (OS-dependent path)
if [ ! -L docs/assets/video ]; then
    case "$(uname)" in
        Linux)  VIDEO_SRC="/mnt/videos/XoL/video" ;;
        Darwin) VIDEO_SRC="/Volumes/video/XoL/video" ;;
    esac
    if [ -d "$VIDEO_SRC" ]; then
        ln -s "$VIDEO_SRC" docs/assets/video
        echo "Created symlink: docs/assets/video -> $VIDEO_SRC"
    fi
fi

# Check video symlink target is accessible (NFS/SMB share mounted?)
if [ -L docs/assets/video ] && [ ! -d docs/assets/video/ ]; then
    echo "⚠  WARNING: docs/assets/video symlink target not accessible!"
    echo "   Mount the video share first (e.g. /mnt/videos/XoL/video)."
    echo "   Videos will be missing from the site."
    echo ""
    read -r -p "Continue anyway? [y/N] " answer
    [[ "$answer" =~ ^[Yy]$ ]] || exit 1
fi

# Development server script that includes VATSIM routes
if [[ "$(uname)" == "Linux" ]]; then
    echo "Copying VATSIM routes for development..."
    cp "$HOME/Work/ATC-Bookings/analyze_vatsim_booking/vatsim_routes.html" ./
    echo "Starting MkDocs development server..."
    mkdocs serve --livereload
else
    # --livereload: workaround for Click 8.x + Python 3.14 bug (flag_value default ignored)
    echo "Starting MkDocs development server (macOS, dirty mode)..."
    mkdocs serve --livereload --dirty
fi
