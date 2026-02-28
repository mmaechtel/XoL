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
elif [ -L docs/assets/video ] && [ -d docs/assets/video/ ]; then
    : # Symlink exists and points to valid target — all good
elif [ -L docs/assets/video ]; then
    # Dangling symlink — recreate
    rm docs/assets/video
    ln -s "$VIDEO_SRC" docs/assets/video
    echo "Recreated symlink: docs/assets/video -> $VIDEO_SRC"
elif [ -d docs/assets/video ]; then
    # Real directory instead of symlink — replace it
    echo "WARNING: docs/assets/video is a directory, not a symlink. Replacing..."
    rm -rf docs/assets/video
    ln -s "$VIDEO_SRC" docs/assets/video
    echo "Replaced directory with symlink: docs/assets/video -> $VIDEO_SRC"
else
    # Path doesn't exist — create symlink
    ln -s "$VIDEO_SRC" docs/assets/video
    echo "Created symlink: docs/assets/video -> $VIDEO_SRC"
fi

# --livereload: workaround for Click 8.x + Python 3.14 bug (flag_value default ignored)
echo "Starting MkDocs development server..."
mkdocs serve --livereload
