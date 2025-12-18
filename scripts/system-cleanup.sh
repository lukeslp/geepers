#!/bin/bash
# System Cleanup Script
# Generated: 2025-12-15
# Purpose: Clean accumulated cruft from checkpoint sweep

set -e

TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/home/coolhand/geepers/archive/${TIMESTAMP}-cleanup-backup"
LOG_FILE="/home/coolhand/geepers/logs/cleanup-${TIMESTAMP}.log"

mkdir -p "$BACKUP_DIR"
mkdir -p /home/coolhand/geepers/logs

log() {
    echo "[$(date +%Y-%m-%d\ %H:%M:%S)] $1" | tee -a "$LOG_FILE"
}

log "=== System Cleanup Started ==="

# 1. Commit staged git changes
log "Step 1: Committing staged changes..."
cd /home/coolhand
if [ -n "$(git status --porcelain)" ]; then
    log "Found $(git status --porcelain | wc -l) uncommitted changes"
    git add -A
    git commit -m "chore(cleanup): checkpoint sweep - remove stale files and update configs

- Clean up Gemini antigravity code tracker files
- Remove archived game projects (immigration-game, eldritch-turkey-fps, moria-web)
- Clean up geepers_agents symlink reorganization
- Update session state and status files

🤖 Generated with Claude Code (https://claude.com/claude-code)

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>" 2>&1 | tee -a "$LOG_FILE"
    log "✓ Changes committed"
else
    log "✓ No changes to commit"
fi

# 2. Rotate large service logs
log "Step 2: Rotating service logs >10MB..."
LOG_COUNT=0
for logfile in /home/coolhand/.service_manager/logs/*.log; do
    SIZE=$(stat -f%z "$logfile" 2>/dev/null || stat -c%s "$logfile" 2>/dev/null || echo 0)
    if [ "$SIZE" -gt 10485760 ]; then  # 10MB
        BASENAME=$(basename "$logfile")
        log "  Rotating $BASENAME ($(numfmt --to=iec-i --suffix=B $SIZE))..."
        cp "$logfile" "$BACKUP_DIR/${BASENAME}.${TIMESTAMP}"
        # Keep last 1000 lines
        tail -n 1000 "$logfile" > "$logfile.tmp"
        mv "$logfile.tmp" "$logfile"
        LOG_COUNT=$((LOG_COUNT + 1))
    fi
done
log "✓ Rotated $LOG_COUNT log files"

# 3. Clean old temp files
log "Step 3: Cleaning temp files >14 days old..."
TEMP_COUNT=$(find /tmp -user coolhand -type f -mtime +14 2>/dev/null | wc -l)
if [ "$TEMP_COUNT" -gt 0 ]; then
    log "  Found $TEMP_COUNT files to clean..."
    find /tmp -user coolhand -type f -mtime +14 -delete 2>&1 | tee -a "$LOG_FILE"
    log "✓ Cleaned $TEMP_COUNT temp files"
else
    log "✓ No old temp files found"
fi

# 4. Clean pip cache (keep last 30 days)
log "Step 4: Cleaning pip cache..."
PIP_BEFORE=$(du -sh /home/coolhand/.cache/pip 2>/dev/null | awk '{print $1}')
if command -v pip &> /dev/null; then
    pip cache purge 2>&1 | tee -a "$LOG_FILE" || log "  Note: pip cache purge failed or not supported"
fi
PIP_AFTER=$(du -sh /home/coolhand/.cache/pip 2>/dev/null | awk '{print $1}')
log "✓ Pip cache: $PIP_BEFORE → $PIP_AFTER"

# 5. Clean old Python cache directories (optional)
log "Step 5: Cleaning Python __pycache__ in non-active projects..."
PYCACHE_COUNT=0
for cache_dir in $(find /home/coolhand/projects/packages/archived -name "__pycache__" -type d 2>/dev/null); do
    rm -rf "$cache_dir"
    PYCACHE_COUNT=$((PYCACHE_COUNT + 1))
done
for cache_dir in $(find /home/coolhand/html/games/inbox -name "__pycache__" -type d 2>/dev/null); do
    rm -rf "$cache_dir"
    PYCACHE_COUNT=$((PYCACHE_COUNT + 1))
done
log "✓ Cleaned $PYCACHE_COUNT __pycache__ directories from archived projects"

# 6. Report zombie processes (manual cleanup needed)
log "Step 6: Checking for zombie processes..."
ZOMBIES=$(ps aux | grep coolhand | grep -E "(defunct|Z)" | grep -v grep | wc -l)
if [ "$ZOMBIES" -gt 0 ]; then
    log "⚠ Found $ZOMBIES zombie processes (manual cleanup recommended):"
    ps aux | grep coolhand | grep -E "(defunct|Z)" | grep -v grep | tee -a "$LOG_FILE"
else
    log "✓ No zombie processes found"
fi

# Summary
log "=== Cleanup Complete ==="
log "Backup location: $BACKUP_DIR"
log "Log file: $LOG_FILE"
log ""
log "Disk space freed:"
du -sh "$BACKUP_DIR" 2>/dev/null | awk '{print "  Logs backed up: " $1}' | tee -a "$LOG_FILE"

log ""
log "Recommendations:"
log "  - Review zombie processes if any were found"
log "  - Check /home/coolhand/.cursor/projects/*/worker.log manually if needed"
log "  - Schedule this script weekly via cron for maintenance"
