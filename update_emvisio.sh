#!/bin/bash

# Exit on error
set -e

# Require GNU rsync (macOS ships openrsync which lacks --delete/--filter support)
if [ "$(uname)" = "Darwin" ]; then
    if [ -x "/opt/homebrew/bin/rsync" ]; then
        RSYNC="/opt/homebrew/bin/rsync"        # ARM Mac (M1+)
    elif [ -x "/usr/local/bin/rsync" ]; then
        RSYNC="/usr/local/bin/rsync"            # Intel Mac
    else
        echo "Error: GNU rsync not found"
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
NO_VIDEOS=false

show_help() {
    echo "Usage: $0 [user@]<hostname> [--dry] [--skip-html] [--no-videos]"
    echo "  -h, --help    Show this help message"
    echo "  --dry         Dry run (no files will be transferred)"
    echo "  --skip-html   Skip copying extra HTML files (vatsim_routes to Maps/)"
    echo "  --no-videos   Skip video symlink check and exclude videos from sync"
    exit 0
}

for arg in "$@"; do
    case "$arg" in
        -h|--help)   show_help ;;
        --dry)        DRY_RUN=true ;;
        --skip-html)  SKIP_HTML=true ;;
        --no-videos)  NO_VIDEOS=true ;;
        *)           REMOTE_HOST="$arg" ;;
    esac
done

if [ -z "$REMOTE_HOST" ]; then
    echo "Usage: $0 [user@]<hostname> [--dry] [--skip-html] [--no-videos]"
    echo "  --dry         Dry run (no files will be transferred)"
    echo "  --skip-html   Skip copying extra HTML files (vatsim_routes to Maps/)"
    echo "  --no-videos   Skip video symlink check and exclude videos from sync"
    exit 1
fi
REMOTE_PATH="/var/www/html"
LOCAL_PATH="./site"

# Check if site directory exists
if [ ! -d "$LOCAL_PATH" ]; then
    echo "Error: $LOCAL_PATH directory not found. Please run 'mkdocs build' first."
    exit 1
fi

# Video source (OS-dependent share path)
case "$(uname)" in
    Linux)  VIDEO_SRC="/mnt/videos/XoL/video" ;;
    Darwin) VIDEO_SRC="/Volumes/video/XoL/video" ;;
esac

if [ "$NO_VIDEOS" = false ] && [ ! -d "$VIDEO_SRC" ]; then
    echo "Error: Video share not mounted at: $VIDEO_SRC"
    echo "Mount the video share first, or use --no-videos to skip."
    exit 1
fi

# Copy root-level files to site/
cp .htaccess robots.txt llms.txt site/

# Rsync options:
#   --delete          Remove files on server that are not in site/
#   --exclude         Protect server-only content from deletion and transfer
#   Maps/ contains external HTML files (airportmap, scenerymap, vatsim_routes)
#   managed outside of MkDocs — protected from rsync --delete
RSYNC_OPTS=(
    -avz
    --checksum
    --delete
    --exclude='stats/'
    --exclude='Maps/'
    --exclude='assets/video/'
)

# macOS stores filenames in NFD (decomposed Unicode: u + combining ¨)
# Linux expects NFC (composed: ü). Without conversion, filenames with
# umlauts get 404s on the server.
if [ "$(uname)" = "Darwin" ]; then
    RSYNC_OPTS+=(--iconv=utf-8-mac,utf-8)
fi

# Sync site to remote (without videos)
if [ "$DRY_RUN" = true ]; then
    echo "Performing dry run (no files will be transferred):"
    $RSYNC "${RSYNC_OPTS[@]}" -n ./site/ ${REMOTE_HOST}:${REMOTE_PATH}/
else
    echo "Syncing site to ${REMOTE_HOST}..."
    $RSYNC "${RSYNC_OPTS[@]}" ./site/ ${REMOTE_HOST}:${REMOTE_PATH}/
    echo "Site sync completed."
fi

# Sync videos directly from share to remote (unless --no-videos)
if [ "$NO_VIDEOS" = false ] && [ -d "$VIDEO_SRC" ]; then
    VIDEO_RSYNC_OPTS=(-avz --delete --chmod=Do+rX,Fo+r)
    if [ "$(uname)" = "Darwin" ]; then
        VIDEO_RSYNC_OPTS+=(--iconv=utf-8-mac,utf-8)
    fi
    if [ "$DRY_RUN" = true ]; then
        echo "Performing dry run for videos:"
        $RSYNC "${VIDEO_RSYNC_OPTS[@]}" -n "$VIDEO_SRC/" ${REMOTE_HOST}:${REMOTE_PATH}/assets/video/
    else
        echo "Syncing videos from share to ${REMOTE_HOST}..."
        $RSYNC "${VIDEO_RSYNC_OPTS[@]}" "$VIDEO_SRC/" ${REMOTE_HOST}:${REMOTE_PATH}/assets/video/
        echo "Video sync completed."
    fi
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

# Smoke test against both domains (skip on dry run)
if [ "$DRY_RUN" = false ]; then
    SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
    if [ -x "$SCRIPT_DIR/smoke_test.sh" ]; then
        echo ""
        "$SCRIPT_DIR/smoke_test.sh" --pages 10
    fi
fi