#!/usr/bin/env bash
# sync-platforms.sh — propagate changed skills from canonical (claude) to all other platforms
#
# Usage:
#   ./sync-platforms.sh                    # dry run: show diffs
#   ./sync-platforms.sh --apply            # copy files
#   ./sync-platforms.sh --apply --push     # copy + commit + push each mirror repo

set -euo pipefail

CANONICAL=~/geepers/platforms/claude/skills
PLATFORMS=(clawhub codex gemini manus)
PLATFORM_BASE=~/geepers/platforms

declare -A MIRROR_REPOS
MIRROR_REPOS[clawhub]=~/projects/dreamer-api-skills
MIRROR_REPOS[codex]=~/servers/geepers-gpt
MIRROR_REPOS[gemini]=~/projects/packages/geepers-gemini
MIRROR_REPOS[manus]=~/projects/packages/geepers-manus

APPLY=false
PUSH=false
CHANGED_FILES=()

for arg in "$@"; do
    case $arg in
        --apply) APPLY=true ;;
        --push)  PUSH=true ;;
        --help|-h)
            echo "Usage: $0 [--apply] [--push]"
            echo "  (no flags)   dry run: show what differs"
            echo "  --apply      copy canonical -> platform dirs"
            echo "  --push       after copying, commit + push each mirror repo"
            exit 0
            ;;
    esac
done

if $PUSH && ! $APPLY; then
    echo "Error: --push requires --apply" >&2
    exit 1
fi

echo "Canonical: $CANONICAL"
echo "Mode: $( $APPLY && echo apply || echo dry-run )$( $PUSH && echo ' + push' || echo '' )"
echo ""

# Walk every skill in canonical
diff_count=0
for skill_dir in "$CANONICAL"/*/; do
    skill=$(basename "$skill_dir")
    canonical_file="$CANONICAL/$skill/SKILL.md"

    [ -f "$canonical_file" ] || continue

    for platform in "${PLATFORMS[@]}"; do
        target_file="$PLATFORM_BASE/$platform/skills/$skill/SKILL.md"

        if [ ! -f "$target_file" ]; then
            echo "[MISSING] $platform/$skill/SKILL.md — skill not present in $platform"
            if $APPLY; then
                mkdir -p "$PLATFORM_BASE/$platform/skills/$skill"
                cp "$canonical_file" "$target_file"
                echo "  → copied"
                CHANGED_FILES+=("$platform:skills/$skill/SKILL.md")
            fi
            diff_count=$((diff_count + 1))
        elif ! diff -q "$canonical_file" "$target_file" > /dev/null 2>&1; then
            echo "[DIFF] $platform/$skill/SKILL.md"
            if ! $APPLY; then
                diff "$canonical_file" "$target_file" | head -20 || true
                echo ""
            fi
            if $APPLY; then
                cp "$canonical_file" "$target_file"
                echo "  → synced $platform/$skill/SKILL.md"
                CHANGED_FILES+=("$platform:skills/$skill/SKILL.md")
            fi
            diff_count=$((diff_count + 1))
        fi
    done
done

echo ""
if [ $diff_count -eq 0 ]; then
    echo "All platforms in sync with canonical."
elif $APPLY; then
    echo "$diff_count file(s) synced."
else
    echo "$diff_count diff(s) found. Run with --apply to sync."
fi

# Push each mirror repo that had changes
if $PUSH && [ ${#CHANGED_FILES[@]} -gt 0 ]; then
    echo ""
    echo "Pushing mirror repos..."

    declare -A PLATFORM_HAS_CHANGES
    for entry in "${CHANGED_FILES[@]}"; do
        platform="${entry%%:*}"
        PLATFORM_HAS_CHANGES[$platform]=1
    done

    for platform in "${!PLATFORM_HAS_CHANGES[@]}"; do
        repo="${MIRROR_REPOS[$platform]}"
        if [ ! -d "$repo/.git" ]; then
            echo "  [SKIP] $platform: $repo is not a git repo"
            continue
        fi

        echo "  [$platform] $repo"
        cd "$repo"

        # Collect files changed for this platform
        files_for_platform=()
        for entry in "${CHANGED_FILES[@]}"; do
            if [[ "$entry" == "$platform:"* ]]; then
                files_for_platform+=("${entry#*:}")
            fi
        done

        git add "${files_for_platform[@]}"
        skill_names=$(printf '%s ' "${files_for_platform[@]}" | sed 's|skills/||g; s|/SKILL.md||g')
        git commit -m "sync: update skills from canonical — $skill_names"
        git push
        echo "  → pushed"
        cd - > /dev/null
    done
fi
