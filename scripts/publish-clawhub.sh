#!/usr/bin/env bash
# Publish all geepers skills to Clawhub from the generated clawhub-package.json.
#
# Prerequisites:
#   npm install -g clawhub
#   clawhub auth login
#
# Usage:
#   bash scripts/publish-clawhub.sh [--dry-run]

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
MANIFEST="$REPO_ROOT/clawhub-package.json"

if [ ! -f "$MANIFEST" ]; then
    echo "Missing $MANIFEST — run 'python3 scripts/build-manifests.py' first"
    exit 1
fi

DRY_RUN=""
if [ "${1:-}" = "--dry-run" ]; then
    DRY_RUN="echo [dry-run]"
fi

SKILLS=$(python3 -c "
import json
data = json.load(open('$MANIFEST'))
for s in data['skills']:
    print(s['path'])
")

COUNT=0
for skill_path in $SKILLS; do
    full_path="$REPO_ROOT/$skill_path"
    slug="lukeslp/$(basename "$skill_path")"
    if [ -d "$full_path" ]; then
        echo "Publishing $slug from $skill_path"
        $DRY_RUN npx clawhub publish "$full_path" --slug "$slug"
        COUNT=$((COUNT + 1))
    else
        echo "SKIP: $full_path not found"
    fi
done

echo ""
echo "Published $COUNT skills to Clawhub."
