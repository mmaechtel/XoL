#!/bin/bash
# Toggle video symlink between NFS share and empty dummy directory.
# Usage: ./video_dummy.sh on   — replace symlink with dummy dir
#        ./video_dummy.sh off  — restore symlink to NFS share

LINK="docs/assets/video"

case "$(uname)" in
    Linux)  VIDEO_SRC="/mnt/videos/XoL/video" ;;
    Darwin) VIDEO_SRC="/Volumes/video/XoL/video" ;;
esac

case "$1" in
    on)
        if [ -d "$LINK" ] && [ ! -L "$LINK" ]; then
            echo "Dummy already active."
            exit 0
        fi
        rm -f "$LINK"
        mkdir -p "$LINK/de" "$LINK/en"
        echo "Dummy directory created. mkdocs serve will work without videos."
        ;;
    off)
        if [ -L "$LINK" ]; then
            echo "Symlink already active → $VIDEO_SRC"
            exit 0
        fi
        rm -rf "$LINK"
        ln -s "$VIDEO_SRC" "$LINK"
        echo "Symlink restored → $VIDEO_SRC"
        ;;
    *)
        echo "Usage: $0 {on|off}"
        exit 1
        ;;
esac
