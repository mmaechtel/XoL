#!/bin/bash

# Exit on error
set -e

# Parse arguments
REMOTE_HOST=""
DRY_RUN=false
SKIP_HTML=false

show_help() {
    echo "Usage: $0 [user@]<hostname> [--dry] [--skip-html]"
    echo "  -h, --help   Show this help message"
    echo "  --dry        Dry run (no files will be transferred)"
    echo "  --skip-html  Skip copying extra HTML files (maps, vatsim)"
    exit 0
}

for arg in "$@"; do
    case "$arg" in
        -h|--help)   show_help ;;
        --dry)       DRY_RUN=true ;;
        --skip-html) SKIP_HTML=true ;;
        *)           REMOTE_HOST="$arg" ;;
    esac
done

if [ -z "$REMOTE_HOST" ]; then
    echo "Usage: $0 [user@]<hostname> [--dry] [--skip-html]"
    echo "  --dry        Dry run (no files will be transferred)"
    echo "  --skip-html  Skip copying extra HTML files (maps, vatsim)"
    exit 1
fi
REMOTE_PATH="/var/www/html"
LOCAL_PATH="./site"

# Check if site directory exists
if [ ! -d "$LOCAL_PATH" ]; then
    echo "Error: $LOCAL_PATH directory not found. Please run 'mkdocs build' first."
    exit 1
fi

# Video symlink setup (OS-dependent path)
case "$(uname)" in
    Linux)  VIDEO_SRC="/mnt/videos/XoL/video" ;;
    Darwin) VIDEO_SRC="/Volumes/video/XoL/video" ;;
esac

if [ ! -d "$VIDEO_SRC" ]; then
    echo "Error: Video share not mounted at: $VIDEO_SRC"
    echo "Mount the video share first, then re-run."
    exit 1
elif [ ! -L docs/assets/video ]; then
    ln -s "$VIDEO_SRC" docs/assets/video
    echo "Created symlink: docs/assets/video -> $VIDEO_SRC"
elif [ ! -d docs/assets/video/ ]; then
    rm docs/assets/video
    ln -s "$VIDEO_SRC" docs/assets/video
    echo "Recreated symlink: docs/assets/video -> $VIDEO_SRC"
fi

# Copy .htaccess to disable directory listing
cp .htaccess site/

# Copy extra HTML files unless --skip-html is set
if [ "$SKIP_HTML" = false ]; then
    cp maps.html site
    cp Maps.html site
    cp "$HOME/Work/ATC-Bookings/analyze_vatsim_booking/vatsim_routes.html" site/
else
    echo "Skipping extra HTML files (--skip-html)"
fi

# Sync to remote
if [ "$DRY_RUN" = true ]; then
    echo "Performing dry run (no files will be transferred):"
    rsync -avzn ./site/ ${REMOTE_HOST}:${REMOTE_PATH}/
else
    echo "Syncing site to ${REMOTE_HOST}..."
    rsync -avz ./site/ ${REMOTE_HOST}:${REMOTE_PATH}/
    echo "Sync completed successfully!"
fi