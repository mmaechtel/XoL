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

# Schneller Review-Build: ohne Social Cards und Git-Daten (~20 s statt Minuten)
export XOL_FULL_BUILD=false
echo "Building site (fast mode: no social cards, no git dates)..."
mkdocs build || exit 1

# Videos nicht kopieren, sondern verlinken — der Build schließt assets/video aus
ln -sfn "$VIDEO_SRC" site/assets/video
trap 'rm -f site/assets/video' EXIT

# PHP-Server statt mkdocs serve: streamt Videos vom Share mit Range-Support
# (mkdocs serve liest Dateien komplett ein und blockiert bei großen MP4s)
PORT="${PORT:-8000}"
echo "Serving site/ at http://127.0.0.1:${PORT}/  (Ctrl+C to stop)"
php -S "127.0.0.1:${PORT}" -t site
