#!/bin/bash
# Rebuild all skill zip files from source

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SOURCE_DIR="$SCRIPT_DIR/source"
ZIPS_DIR="$SCRIPT_DIR/zips"

echo "Rebuilding skill zips..."

mkdir -p "$ZIPS_DIR"

for skill_dir in "$SOURCE_DIR"/*/; do
    skill_name=$(basename "$skill_dir")
    cd "$skill_dir"
    rm -f "$ZIPS_DIR/${skill_name}.zip"
    zip -r "$ZIPS_DIR/${skill_name}.zip" .
    echo "  OK ${skill_name}.zip"
done

echo ""
echo "Done! Zips ready in: $ZIPS_DIR"
ls -lh "$ZIPS_DIR"
