#!/bin/bash
# Smoke test: verify random pages, all videos and posters are reachable on the live site.
# Usage: ./smoke_test.sh [base_url] [--pages N]
#   base_url   defaults to https://emvisio.com
#   --pages N  number of random pages to check (default: 20)

set -euo pipefail

BASE_URL="https://emvisio.com"
NUM_PAGES=20

while [[ $# -gt 0 ]]; do
    case "$1" in
        --pages) NUM_PAGES="$2"; shift 2 ;;
        --pages=*) NUM_PAGES="${1#*=}"; shift ;;
        http*) BASE_URL="${1%/}"; shift ;;
        *) shift ;;
    esac
done

PASS=0
FAIL=0
FAILURES=()

check_url() {
    local url="$1"
    local label="$2"
    local type="$3"
    local status
    status=$(curl -o /dev/null -s -w "%{http_code}" --head --max-time 10 "$url" 2>/dev/null || echo "000")

    printf "  %-65s " "$label"
    if [[ "$status" =~ ^(200|301|302)$ ]]; then
        PASS=$((PASS + 1))
        echo "OK"
    else
        FAIL=$((FAIL + 1))
        FAILURES+=("  $status  [$type] $label")
        echo "FAIL ($status)"
    fi
}

echo "Smoke test: $BASE_URL"
echo "========================================"

# --- 1. Random pages from sitemap ---
SITEMAP="site/sitemap.xml"
if [ ! -f "$SITEMAP" ]; then
    echo "Warning: $SITEMAP not found. Run 'mkdocs build' first."
    echo "Skipping page checks."
else
    PAGES=$(grep -oP '<loc>\K[^<]+' "$SITEMAP" | shuf -n "$NUM_PAGES")
    TOTAL_PAGES=$(grep -c '<loc>' "$SITEMAP")
    echo ""
    echo "Pages ($NUM_PAGES random of $TOTAL_PAGES):"
    while IFS= read -r page_url; do
        label=$(echo "$page_url" | sed "s|${BASE_URL}/||")
        check_url "$page_url" "$label" "PAGE"
    done <<< "$PAGES"
fi

# --- 2. All videos and posters (deduplicated) ---
echo ""
echo "Videos and posters:"

# Extract all video src and poster paths, resolve relative paths, deduplicate
ASSET_URLS=$(grep -rhoP '(src|poster)="[^"]*\.(mp4|jpg)"' docs/ \
    | sed 's/^[^"]*"//;s/"$//' \
    | sed 's|\.\./||g' \
    | sort -u)

while IFS= read -r asset_path; do
    [ -z "$asset_path" ] && continue
    url="${BASE_URL}/${asset_path}"

    if [[ "$asset_path" == *.mp4 ]]; then
        type="VIDEO"
    else
        type="POSTER"
    fi

    check_url "$url" "$asset_path" "$type"
done <<< "$ASSET_URLS"

# --- Summary ---
echo ""
echo "========================================"
TOTAL=$((PASS + FAIL))
echo "Result: $PASS/$TOTAL passed"

if [ ${#FAILURES[@]} -gt 0 ]; then
    echo ""
    echo "FAILURES:"
    for f in "${FAILURES[@]}"; do
        echo "$f"
    done
    exit 1
else
    echo "All checks passed."
    exit 0
fi
