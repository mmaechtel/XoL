#!/bin/bash
# Smoke test: verify random pages, all videos and posters are reachable on the live site.
# Usage: ./smoke_test.sh [base_url] [--pages N]
#   base_url   defaults to https://emvisio.de (tests both .de and .com)
#   --pages N  number of random pages to check per domain (default: 10)

set -euo pipefail

BASE_URL=""
NUM_PAGES=10

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

run_test() {
    local base_url="$1"
    local lang_filter="$2"  # "de" or "en" or "" for all

    echo "Smoke test: $base_url"
    echo "========================================"

    # --- 1. Random pages from sitemap ---
    SITEMAP="site/sitemap.xml"
    if [ ! -f "$SITEMAP" ]; then
        echo "Warning: $SITEMAP not found. Run 'mkdocs build' first."
        echo "Skipping page checks."
    else
        # Sitemap uses emvisio.com — extract paths and rebuild with target base_url
        if [ -n "$lang_filter" ]; then
            if [ "$lang_filter" = "de" ]; then
                # DE pages: everything that does NOT start with /en/
                PAGES=$(sed -n 's|.*<loc>\([^<]*\)</loc>.*|\1|p' "$SITEMAP" \
                    | sed 's|https://emvisio.com/||' \
                    | grep -v '^en/' \
                    | shuf -n "$NUM_PAGES")
            else
                # EN pages: everything under /en/
                PAGES=$(sed -n 's|.*<loc>\([^<]*\)</loc>.*|\1|p' "$SITEMAP" \
                    | sed 's|https://emvisio.com/||' \
                    | grep '^en/' \
                    | shuf -n "$NUM_PAGES")
            fi
        else
            PAGES=$(sed -n 's|.*<loc>\([^<]*\)</loc>.*|\1|p' "$SITEMAP" \
                | sed 's|https://emvisio.com/||' \
                | shuf -n "$NUM_PAGES")
        fi

        TOTAL_PAGES=$(grep -c '<loc>' "$SITEMAP" || echo 0)
        echo ""
        echo "Pages ($NUM_PAGES random of $TOTAL_PAGES, filter: ${lang_filter:-all}):"
        while IFS= read -r page_path; do
            [ -z "$page_path" ] && continue
            check_url "${base_url}/${page_path}" "$page_path" "PAGE"
        done <<< "$PAGES"
    fi

    # --- 2. Videos and posters (deduplicated, filtered by language) ---
    echo ""
    echo "Videos and posters${lang_filter:+ ($lang_filter)}:"

    ASSET_URLS=$(grep -roh 'src="[^"]*\.mp4"\|src="[^"]*\.jpg"\|poster="[^"]*\.mp4"\|poster="[^"]*\.jpg"' docs/ \
        | sed 's/^[^"]*"//;s/"$//' \
        | sed 's|\.\./||g' \
        | sort -u)

    while IFS= read -r asset_path; do
        [ -z "$asset_path" ] && continue

        # Filter by language if specified
        if [ -n "$lang_filter" ]; then
            case "$asset_path" in
                *video/de/*) [ "$lang_filter" != "de" ] && continue ;;
                *video/en/*) [ "$lang_filter" != "en" ] && continue ;;
            esac
        fi

        if [[ "$asset_path" == *.mp4 ]]; then
            type="VIDEO"
        else
            type="POSTER"
        fi

        check_url "${base_url}/${asset_path}" "$asset_path" "$type"
    done <<< "$ASSET_URLS"

    # --- 3. Content drift check: top changelog date block on index.html ---
    echo ""
    echo "Content drift (changelog top block${lang_filter:+, $lang_filter}):"

    if [ "$lang_filter" = "en" ]; then
        local_index="site/en/index.html"
        live_url="${base_url}/en/"
    else
        local_index="site/index.html"
        live_url="${base_url}/"
    fi

    if [ ! -f "$local_index" ]; then
        echo "  Warning: $local_index not found, skipping drift check"
    else
        local_top=$(grep -oE '<h3 id="[0-9]{4}-[0-9]{2}-[0-9]{2}">' "$local_index" | head -1)
        live_top=$(curl -s --max-time 10 "$live_url" | grep -oE '<h3 id="[0-9]{4}-[0-9]{2}-[0-9]{2}">' | head -1)
        label="$live_url top date block"
        printf "  %-65s " "$label"
        if [ -z "$local_top" ] || [ -z "$live_top" ]; then
            FAIL=$((FAIL + 1))
            FAILURES+=("  --   [DRIFT] $label (local='$local_top' live='$live_top')")
            echo "FAIL (no date block found)"
        elif [ "$local_top" = "$live_top" ]; then
            PASS=$((PASS + 1))
            echo "OK ($local_top)"
        else
            FAIL=$((FAIL + 1))
            FAILURES+=("  --   [DRIFT] $label local=$local_top live=$live_top")
            echo "FAIL (local=$local_top live=$live_top)"
        fi
    fi

    echo ""
}

# Run tests
if [ -n "$BASE_URL" ]; then
    # Single domain specified
    run_test "$BASE_URL" ""
else
    # Default: test both domains with matching language
    run_test "https://emvisio.de" "de"
    run_test "https://emvisio.com" "en"
fi

# --- Summary ---
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
