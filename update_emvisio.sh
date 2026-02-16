#!/bin/bash

# Exit on error
set -e

# Require GNU rsync (macOS ships openrsync which lacks --delete/--filter support)
if [ "$(uname)" = "Darwin" ]; then
    RSYNC="/usr/local/bin/rsync"
    if [ ! -x "$RSYNC" ]; then
        echo "Error: GNU rsync not found at $RSYNC"
        echo "macOS openrsync lacks required features. Install with: brew install rsync"
        exit 1
    fi
else
    RSYNC=rsync
fi

# Parse arguments
REMOTE_HOST=""
DRY_RUN=false
SKIP_HTML=false

show_help() {
    echo "Usage: $0 [user@]<hostname> [--dry] [--skip-html]"
    echo "  -h, --help   Show this help message"
    echo "  --dry        Dry run (no files will be transferred)"
    echo "  --skip-html  Skip copying extra HTML files (vatsim_routes to Maps/)"
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
    echo "  --skip-html  Skip copying extra HTML files (vatsim_routes to Maps/)"
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

# Rsync options:
#   --delete          Remove files on server that are not in site/
#   --exclude         Protect server-only content from deletion and transfer
#   Maps/ contains external HTML files (airportmap, scenerymap, vatsim_routes)
#   managed outside of MkDocs — protected from rsync --delete
RSYNC_OPTS=(
    -avz
    --delete
    --exclude='stats/'
    --exclude='Maps/'
)

# macOS stores filenames in NFD (decomposed Unicode: u + combining ¨)
# Linux expects NFC (composed: ü). Without conversion, filenames with
# umlauts get 404s on the server.
if [ "$(uname)" = "Darwin" ]; then
    RSYNC_OPTS+=(--iconv=utf-8-mac,utf-8)
fi

# Sync to remote
if [ "$DRY_RUN" = true ]; then
    echo "Performing dry run (no files will be transferred):"
    $RSYNC "${RSYNC_OPTS[@]}" -n ./site/ ${REMOTE_HOST}:${REMOTE_PATH}/
else
    echo "Syncing site to ${REMOTE_HOST}..."
    $RSYNC "${RSYNC_OPTS[@]}" ./site/ ${REMOTE_HOST}:${REMOTE_PATH}/
    echo "Sync completed successfully!"
fi

# Copy extra HTML files to Maps/ on server (unless --skip-html)
VATSIM_SRC="$HOME/Work/ATC-Bookings/analyze_vatsim_booking/vatsim_routes.html"
if [ "$SKIP_HTML" = false ]; then
    if [ -f "$VATSIM_SRC" ]; then
        echo "Copying vatsim_routes.html to Maps/..."
        scp -q "$VATSIM_SRC" ${REMOTE_HOST}:${REMOTE_PATH}/Maps/
    else
        echo "Warning: $VATSIM_SRC not found, skipping"
    fi
else
    echo "Skipping extra HTML files (--skip-html)"
fi