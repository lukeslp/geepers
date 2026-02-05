#!/bin/bash
# Rebuild all skill zip files from source

SKILLS_DIR="$HOME/geepers/skills"
SOURCE_DIR="$SKILLS_DIR/source"
ZIPS_DIR="$SKILLS_DIR/zips"

echo "Rebuilding skill zips..."

for skill_dir in "$SOURCE_DIR"/*/; do
    skill_name=$(basename "$skill_dir")
    cd "$skill_dir"
    rm -f "$ZIPS_DIR/${skill_name}.zip"
    zip -r "$ZIPS_DIR/${skill_name}.zip" .
    echo "  ✓ ${skill_name}.zip"
done

echo ""
echo "Done! Zips ready in: $ZIPS_DIR"
ls -lh "$ZIPS_DIR"
