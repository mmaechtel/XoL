#!/bin/bash

# Video symlink setup (OS-dependent path)
case "$(uname)" in
    Linux)  VIDEO_SRC="/mnt/videos/XoL/video" ;;
    Darwin) VIDEO_SRC="/Volumes/video/XoL/video" ;;
esac

if [ ! -d "$VIDEO_SRC" ]; then
    echo "WARNING: Video share not mounted at: $VIDEO_SRC"
    echo "  Videos and poster images will be missing."
    echo ""
    read -r -p "Continue anyway? [y/N] " answer
    [[ "$answer" =~ ^[Yy]$ ]] || exit 1
elif [ ! -L docs/assets/video ]; then
    ln -s "$VIDEO_SRC" docs/assets/video
    echo "Created symlink: docs/assets/video -> $VIDEO_SRC"
elif [ ! -d docs/assets/video/ ]; then
    rm docs/assets/video
    ln -s "$VIDEO_SRC" docs/assets/video
    echo "Recreated symlink: docs/assets/video -> $VIDEO_SRC"
fi

# --livereload: workaround for Click 8.x + Python 3.14 bug (flag_value default ignored)
echo "Starting MkDocs development server..."
mkdocs serve --livereload
