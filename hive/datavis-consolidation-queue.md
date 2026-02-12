# Task Queue: Dataset Consolidation & Reorganization

**Generated**: 2026-02-10 02:15
**Project**: datavis (data infrastructure)
**Total Tasks**: 15
**Quick Wins**: 3
**Blocked**: 2
**Execution Phase**: Analysis complete, ready for execution

---

## Overview

This queue executes the dataset consolidation plan to:
1. Rename data_trove -> data-hoard (GitHub + local)
2. Replace fragile symlinks with real data copies
3. Harvest unharvested dev/ data into data-hoard
4. Archive redundant ~/datasets/ directory
5. Publish 20 quirky _real datasets as themed bundles (GitHub + HuggingFace + Kaggle)
6. Clean up dead HuggingFace entries
7. Consolidate public platform presence (fix naming, verify coverage)

**Naming Corrections Applied**:
- NO "kaggle-data" naming used anywhere
- Use `-atlas` for geographic/mappable data (e.g., `natural-world-atlas`)
- Use `-dataset` for categorical/analytical data (e.g., `earth-phenomena-dataset`)
- Use `-data` for time-series/analytical data (e.g., `solar-system-data`)

**Existing GitHub Repos (lukeslp/*)**:
- strange-places-dataset
- us-inequality-atlas
- accessibility-atlas
- us-attention-data
- joshua-project-data
- language-data
- us-disasters-mashup
- data_trove (rename to data-hoard)

**New GitHub Repos to Create**:
- natural-world-atlas
- earth-phenomena-dataset
- historical-sites-atlas
- unexplained-dataset
- solar-system-data

---

## Ready to Build (Prioritized by Dependency Order)

### 1. [QW] Re-authenticate GitHub

**Source**: Plan Section 8, line 133
**Impact**: 5 | **Effort**: 1 | **Priority**: 8.5
**Description**: GitHub token (gho_41s...) appears expired. Must re-authenticate before any GitHub API operations (renames, repo creation, push).
**Blockers**: Blocks all Steps 1-7
**Files**: None (CLI operation)
**Command**: `gh auth logout && gh auth login`

**Why First**: All subsequent GitHub operations fail without valid auth.

---

### 2. [QW] Rename data_trove -> data-hoard (Local Filesystem)

**Source**: Plan Section 1 + Step 2, lines 54-67
**Impact**: 4 | **Effort**: 1 | **Priority**: 7.5
**Description**: Rename local directory `/home/coolhand/html/datavis/data_trove/` to `data-hoard`. Create backwards-compatibility symlink so existing URLs `dr.eamer.dev/datavis/data_trove/` still resolve.
**Depends on**: Task 1 (actually local-only, can run in parallel)
**Files**: `/home/coolhand/html/datavis/data_trove/` → `/home/coolhand/html/datavis/data-hoard/`
**Commands**:
```bash
cd /home/coolhand/html/datavis
mv data_trove data-hoard
ln -s data-hoard data_trove
git add -A
git commit -m "rename: data_trove -> data-hoard (local filesystem)"
```

**Verification**:
```bash
ls -la /home/coolhand/html/datavis/ | grep data
# data-hoard/  (directory)
# data_trove -> data-hoard  (symlink)
```

---

### 3. [QW] Rename GitHub Remote: data_trove -> data-hoard

**Source**: Plan Section 1, lines 54-67
**Impact**: 4 | **Effort**: 2 | **Priority**: 7.0
**Description**: Use GitHub API to rename `lukeslp/data_trove` repository to `lukeslp/data-hoard`. Update local `.git/config` to track new remote URL.
**Depends on**: Task 1 (GitHub auth)
**Files**: `.git/config`, GitHub repository metadata
**Commands**:
```bash
cd /home/coolhand/html/datavis/data-hoard
# Rename via GitHub API
gh repo rename data-hoard --repo lukeslp/data_trove

# Update local git config to track new remote
git remote set-url origin https://github.com/lukeslp/data-hoard.git
git remote -v  # Verify new URL

git push -u origin master
```

**Verification**:
```bash
curl -I https://github.com/lukeslp/data-hoard
# Should return 200
curl -I https://github.com/lukeslp/data_trove
# Should return 301 (redirect to data-hoard) or 404
```

---

### 4. Rename GitHub Remote: forget_me_not -> forget-me-not (Kebab-case)

**Source**: Plan Section 1, lines 10-11
**Impact**: 3 | **Effort**: 2 | **Priority**: 6.0
**Description**: Update kebab-case convention: rename `forget_me_not` repository to `forget-me-not` for consistency with other repos (strange-places-dataset, us-inequality-atlas, etc.).
**Depends on**: Task 1 (GitHub auth)
**Files**: GitHub repository metadata
**Commands**:
```bash
# Rename via GitHub API
gh repo rename forget-me-not --repo lukeslp/forget_me_not

# If local clone exists, update remote URL
cd /home/coolhand/html/datavis/forget_me_not
git remote set-url origin https://github.com/lukeslp/forget-me-not.git
git push -u origin master
```

**Note**: May not have local clone - this is primarily GitHub cleanup.

---

### 5. Replace Symlinks with Real Data Copies

**Source**: Plan Section 2, lines 66-77
**Impact**: 4 | **Effort**: 2 | **Priority**: 6.5
**Description**: Find all symlinks in `/home/coolhand/html/datavis/data-hoard/` (currently demographic/ and economic/ directories point to dev/ projects) and replace with actual data copies. Eliminates fragility if dev/ directory is modified or moved.
**Depends on**: Task 2 (data-hoard exists locally)
**Files**:
- `/home/coolhand/html/datavis/data-hoard/demographic/veterans/` (symlink -> copy)
- `/home/coolhand/html/datavis/data-hoard/demographic/poverty/` (symlink -> copy)
- `/home/coolhand/html/datavis/data-hoard/economic/housing/` (symlink -> copy, if exists)

**Commands**:
```bash
cd /home/coolhand/html/datavis/data-hoard

# Find all symlinks
find . -type l

# For each symlink, replace with real copy
for link in $(find . -type l); do
  target=$(readlink "$link")
  rm "$link"
  cp -r "$target" "$link"
done

# Verify no symlinks remain
find . -type l  # Should return empty
```

**Verification**:
```bash
find /home/coolhand/html/datavis/data-hoard -type l
# Should return nothing
```

**Commit**: After verification, commit the change:
```bash
git add -A
git commit -m "refactor: replace symlinks with real data copies in data-hoard"
git push origin master
```

---

### 6. Harvest Unharvested dev/ Data into data-hoard

**Source**: Plan Section 3, lines 79-87
**Impact**: 4 | **Effort**: 2 | **Priority**: 6.5
**Description**: Three dev/ projects have data NOT yet backed up anywhere:
- `dev/scars/data/` (420MB) → `data-hoard/data/inequality/scars/`
- `dev/nyc_housing/data/` (32MB) → `data-hoard/data/urban/nyc_housing/`
- `dev/housing_crisis/data/` (already via symlink in Step 5, but ensure real copy)

These are high-value datasets at risk of loss if dev/ is cleaned up.

**Depends on**: Task 2 (data-hoard exists locally)
**Files**:
- `/home/coolhand/html/datavis/dev/scars/data/` (source)
- `/home/coolhand/html/datavis/dev/nyc_housing/data/` (source)
- `/home/coolhand/html/datavis/dev/housing_crisis/data/` (source)

**Commands**:
```bash
cd /home/coolhand/html/datavis/data-hoard

# Create directory structure if not exists
mkdir -p data/inequality data/urban

# Copy scars data (420MB - watch for disk space)
cp -r ../dev/scars/data/ data/inequality/scars/

# Copy nyc_housing data (32MB)
cp -r ../dev/nyc_housing/data/ data/urban/nyc_housing/

# Copy housing_crisis data (verify not just symlink)
cp -r ../dev/housing_crisis/data/ data/housing_crisis/
# Or if already exists and is real, skip

# Verify copies succeeded
du -sh data/inequality/scars/  # Should show ~420MB
du -sh data/urban/nyc_housing/  # Should show ~32MB
```

**Verification**:
```bash
find /home/coolhand/html/datavis/data-hoard/data/inequality/scars -type f | wc -l
# Should match source file count
```

**Commit**:
```bash
git add -A
git commit -m "feat: harvest scars and nyc_housing data into data-hoard (backup protection)"
git push origin master
```

**Note**: After successful backup, consider if dev/ projects should be archived or cleaned up. For now, keep as source-of-truth until migration complete.

---

### 7. Archive ~/datasets/ Directory

**Source**: Plan Section 4, lines 89-96
**Impact**: 3 | **Effort**: 2 | **Priority**: 5.5
**Description**: `/home/coolhand/datasets/` contains 100% redundant data. All files exist in primary locations:
- etymology_atlas → canonical at `/home/coolhand/servers/diachronica/`
- bluesky data → already on Kaggle + HuggingFace
- housing/veterans → now in data-hoard (Tasks 5-6)
- strange-places → in data-hoard/data/wild/

Move entire directory to archive for safe cleanup.

**Depends on**: Task 6 (all data harvested first)
**Files**: `/home/coolhand/datasets/` → `/home/coolhand/storage/archived/datasets/`

**Commands**:
```bash
# Create archive destination if not exists
mkdir -p /home/coolhand/storage/archived/

# Move datasets directory
mv /home/coolhand/datasets /home/coolhand/storage/archived/datasets

# Verify move succeeded
ls /home/coolhand/storage/archived/datasets/ | wc -l
# Should show file count

# Remove from git tracking (if tracked)
cd /home/coolhand/html/datavis/
git status  # Check if datasets submodule or tracked
# If tracked: git rm --cached ../datasets && git commit -m "archive: move datasets to storage/archived"
```

**Verification**:
```bash
ls /home/coolhand/datasets
# Should fail (no such file/dir)
ls /home/coolhand/storage/archived/datasets/
# Should show archived contents
```

---

### 8. Create GitHub Repo: natural-world-atlas

**Source**: Plan Section 6, lines 121-122
**Impact**: 4 | **Effort**: 3 | **Priority**: 5.5
**Description**: New GitHub repository for geographic/mappable datasets: deep_sea, bioluminescence, carnivorous_plants, fossils, caves, geothermal. These are real datasets from OpenFoodFacts, Paleobiology DB, NASA, NOAA.
**Depends on**: Task 1 (GitHub auth), Tasks 5-6 (data ready)
**Files**: Source data in `/home/coolhand/html/datavis/data-hoard/data/quirky/`

**Datasets Included**:
- deep_sea (200K) - OpenFoodFacts marine organisms
- bioluminescence (43K) - NOAA/NASA bioluminescent species
- carnivorous_plants (610) - USDA plants
- fossils (22K) - Paleobiology Database
- caves (70K) - USDA karst features
- geothermal (8.8K) - USGS geothermal sites

**Commands**:
```bash
cd /tmp
gh repo create lukeslp/natural-world-atlas --public --source=/dev/null --description "Geographic datasets of natural phenomena: deep sea organisms, bioluminescence, carnivorous plants, fossils, caves, geothermal features"

# Initialize repo
cd natural-world-atlas
git init
git branch -M main

# Copy data from data-hoard
mkdir -p data
cp /home/coolhand/html/datavis/data-hoard/data/quirky/deep_sea* data/
cp /home/coolhand/html/datavis/data-hoard/data/quirky/bioluminescence* data/
cp /home/coolhand/html/datavis/data-hoard/data/quirky/carnivorous_plants* data/
cp /home/coolhand/html/datavis/data-hoard/data/quirky/fossils* data/
cp /home/coolhand/html/datavis/data-hoard/data/quirky/caves* data/
cp /home/coolhand/html/datavis/data-hoard/data/quirky/geothermal* data/

# Create README.md with metadata
cat > README.md << 'EOF'
# natural-world-atlas

Geographic datasets documenting Earth's natural phenomena.

## Datasets

- **deep_sea** (200K) - Marine organism observations
- **bioluminescence** (43K) - Bioluminescent species catalog
- **carnivorous_plants** (610) - Carnivorous plant species
- **fossils** (22K) - Fossil records
- **caves** (70K) - Karst cave systems
- **geothermal** (8.8K) - Geothermal sites and hot springs

## Sources

All data sourced from public APIs and databases.
EOF

git add .
git commit -m "init: natural-world-atlas with 6 real datasets"
git remote add origin https://github.com/lukeslp/natural-world-atlas.git
git push -u origin main
```

**Verification**:
```bash
curl -I https://github.com/lukeslp/natural-world-atlas
# Should return 200
```

---

### 9. Create GitHub Repo: earth-phenomena-dataset

**Source**: Plan Section 6, lines 123-122
**Impact**: 4 | **Effort**: 3 | **Priority**: 5.5
**Description**: New GitHub repository for dynamic Earth phenomena: tornadoes, asteroids, atmospheric events, radio signals. Themed for temporal/dynamic analysis.
**Depends on**: Task 1 (GitHub auth), Tasks 5-6 (data ready)

**Datasets Included**:
- tornadoes (70K) - NOAA Storm Events Database
- asteroids (41K) - NASA Planetary Data System
- atmospheric (426) - NOAA atmospheric anomalies
- radio_signals (48) - Anomalous signals catalog

**Commands**:
```bash
cd /tmp
gh repo create lukeslp/earth-phenomena-dataset --public --description "Real-time and historical Earth phenomena: tornado events, asteroid tracking, atmospheric phenomena, radio signal observations"

# Initialize and populate (similar pattern to Task 8)
cd earth-phenomena-dataset
git init && git branch -M main
mkdir -p data
cp /home/coolhand/html/datavis/data-hoard/data/quirky/tornadoes* data/
cp /home/coolhand/html/datavis/data-hoard/data/quirky/asteroids* data/
cp /home/coolhand/html/datavis/data-hoard/data/quirky/atmospheric* data/
cp /home/coolhand/html/datavis/data-hoard/data/quirky/radio_signals* data/

# Create README
cat > README.md << 'EOF'
# earth-phenomena-dataset

Datasets tracking dynamic Earth phenomena.

## Datasets

- **tornadoes** (70K) - Tornado occurrences and characteristics
- **asteroids** (41K) - Near-Earth asteroid tracking
- **atmospheric** (426) - Atmospheric anomalies and events
- **radio_signals** (48) - Anomalous radio observations

## Sources

All data from NOAA, NASA, and other public repositories.
EOF

git add . && git commit -m "init: earth-phenomena-dataset"
git remote add origin https://github.com/lukeslp/earth-phenomena-dataset.git
git push -u origin main
```

---

### 10. Create GitHub Repo: historical-sites-atlas

**Source**: Plan Section 6, lines 123-124
**Impact**: 4 | **Effort**: 3 | **Priority**: 5.5
**Description**: New GitHub repository for geographic historical sites: ancient ruins, megaliths, lighthouses, shipwrecks.
**Depends on**: Task 1 (GitHub auth), Tasks 5-6 (data ready)

**Datasets Included**:
- ancient_ruins (97K) - UNESCO/archaeological sites
- megaliths (15.5K) - Megalithic monuments
- lighthouses (14.6K) - Navigation lighthouses worldwide
- shipwrecks (5.6K) - Historic shipwreck locations

---

### 11. Create GitHub Repo: unexplained-dataset

**Source**: Plan Section 6, lines 124-125
**Impact**: 3 | **Effort**: 3 | **Priority**: 5.0
**Description**: New GitHub repository for unexplained phenomena: cryptids, witch trials, famous disappearances, ghost ships.
**Depends on**: Task 1 (GitHub auth), Tasks 5-6 (data ready)

**Datasets Included**:
- cryptids (3.7K) - Cryptid sightings
- witch_trials (10.9K) - Historical witch trial records
- famous_disappearances (16) - Notable disappearance cases
- famous_ghost_ships (15) - Ghost ship documentation

---

### 12. Create GitHub Repo: solar-system-data

**Source**: Plan Section 6, lines 125-126 (optional: fold asteroids into earth-phenomena)
**Impact**: 3 | **Effort**: 2 | **Priority**: 4.5
**Description**: Optional repository combining solar system data. If asteroids included here, remove from earth-phenomena-dataset. Current plan folds asteroids into earth-phenomena (dynamic/temporal focus).
**Depends on**: Task 1 (GitHub auth)
**Status**: OPTIONAL - Depends on user preference re: asteroid categorization

**Note**: Plan recommends folding asteroids into earth-phenomena-dataset. Skip this task unless user specifies solar system focus.

---

### 13. Publish All 5 New Repos to HuggingFace

**Source**: Plan Section 6, lines 119-126
**Impact**: 4 | **Effort**: 3 | **Priority**: 5.0
**Description**: Create HuggingFace dataset entries for:
1. natural-world-atlas
2. earth-phenomena-dataset
3. historical-sites-atlas
4. unexplained-dataset
5. (optional) solar-system-data

Requires HuggingFace API key and lukeslp account.

**Depends on**: Tasks 8-12 (GitHub repos exist with data + README)

**Commands** (sample for one repo):
```bash
# Requires huggingface_hub Python package
pip install huggingface_hub

# Authenticate
huggingface-cli login
# Enter token from https://huggingface.co/settings/tokens

# Create dataset
huggingface-cli repo create natural-world-atlas --type dataset --organization lukeslp

# Upload data
cd /tmp/natural-world-atlas
git clone https://huggingface.co/datasets/lukeslp/natural-world-atlas
cp -r data/* natural-world-atlas/
cd natural-world-atlas
git add . && git commit -m "init: upload natural-world-atlas datasets"
git push
```

**Verification**:
```bash
curl -I https://huggingface.co/datasets/lukeslp/natural-world-atlas
# Should return 200
```

---

### 14. Publish All 5 New Repos to Kaggle

**Source**: Plan Section 6 (implied)
**Impact**: 3 | **Effort**: 3 | **Priority**: 4.5
**Description**: Create Kaggle dataset entries for all 5 new bundles. Requires Kaggle API key.
**Depends on**: Tasks 8-12 (GitHub repos exist with data + README)

**Commands**:
```bash
pip install kaggle

# Create kaggle.json in ~/.kaggle/
# {
#   "username": "lucassteuber",
#   "key": "[your_kaggle_api_key]"
# }
chmod 600 ~/.kaggle/kaggle.json

# Create dataset
kaggle datasets create \
  --folder /tmp/natural-world-atlas/data \
  --public \
  --dir-mode tar

# Follow interactive prompts for dataset name, description, etc.
```

**Note**: Kaggle dataset creation process is more manual than HuggingFace. May require web UI interaction.

---

### 15. Clean Up Dead HuggingFace Entries

**Source**: Plan Section 7, lines 129-130
**Impact**: 2 | **Effort**: 1 | **Priority**: 3.0
**Description**: Delete 4 orphaned 404 placeholders from HuggingFace:
- inequality-atlas (lukesteuber - typo in account name, use lukeslp)
- americas-political-economy
- pnw-language-isolates
- expatriation-pathways

**Depends on**: None (cleanup task)

**Commands**:
```bash
# Requires huggingface_hub
huggingface-cli delete-repo inequality-atlas --type dataset --organization lukesteuber
huggingface-cli delete-repo americas-political-economy --type dataset --organization lukeslp
huggingface-cli delete-repo pnw-language-isolates --type dataset --organization lukeslp
huggingface-cli delete-repo expatriation-pathways --type dataset --organization lukeslp
```

**Verification**:
```bash
curl -I https://huggingface.co/datasets/lukeslp/americas-political-economy
# Should return 404
```

---

## Deferred (Not Blocking)

### Update data-hoard index.html

**Source**: Plan Section 8, line 151
**Impact**: 2 | **Effort**: 2 | **Priority**: 2.5
**Description**: Update catalog page at `/home/coolhand/html/datavis/data-hoard/index.html` to reflect new dataset additions and symlink->copy changes. Current index.html has ~35% coverage gap (76 of 200+ datasets listed).
**Status**: DEFERRED - Can execute after data consolidation complete
**See**: System reminder MEMORY.md notes on data_trove structure

---

## Blocked Tasks

**None currently blocked** - all tasks proceed in dependency order after GitHub auth (Task 1).

---

## Statistics

| Category | Count |
|----------|-------|
| High priority (>6) | 5 |
| Medium priority (4-6) | 9 |
| Low priority (<4) | 1 |
| Quick wins | 2 |
| Blocked | 0 |
| GitHub operations | 8 |
| Local filesystem ops | 5 |
| Publication platforms | 3 |

---

## Verification Checklist

After all tasks complete:

- [ ] `ls -la /home/coolhand/html/datavis/` shows data-hoard/ (dir) and data_trove -> data-hoard (symlink)
- [ ] `git config --get remote.origin.url` returns `https://github.com/lukeslp/data-hoard.git`
- [ ] `find /home/coolhand/html/datavis/data-hoard -type l` returns empty (no symlinks)
- [ ] `du -sh /home/coolhand/html/datavis/data-hoard/data/inequality/scars/` returns ~420MB
- [ ] `du -sh /home/coolhand/html/datavis/data-hoard/data/urban/nyc_housing/` returns ~32MB
- [ ] `/home/coolhand/datasets` directory does not exist (archived)
- [ ] `/home/coolhand/storage/archived/datasets/` contains archived files
- [ ] GitHub repos exist: lukeslp/{natural-world-atlas, earth-phenomena-dataset, historical-sites-atlas, unexplained-dataset}
- [ ] HuggingFace datasets exist: lukeslp/{natural-world-atlas, earth-phenomena-dataset, historical-sites-atlas, unexplained-dataset}
- [ ] Kaggle datasets exist: lucassteuber/{natural-world-atlas, earth-phenomena-dataset, historical-sites-atlas, unexplained-dataset}
- [ ] curl https://dr.eamer.dev/datavis/data_trove/ returns 200 (symlink still works via Caddy)
- [ ] curl https://github.com/lukeslp/data_trove returns 301/404 (old URL redirects or gone)

---

## Execution Notes

**Git Safety Protocol**:
1. Before EVERY commit, run: `git log --oneline -3` to confirm expected commits
2. Before EVERY commit, run: `git diff --stat` to verify only intended changes
3. Batch commits logically (e.g., all local renames together, all GitHub ops together)
4. Push after each major milestone to avoid losing work

**Disk Space Considerations**:
- Task 6 copies ~420MB (scars) + ~32MB (nyc_housing) = ~452MB additional
- Ensure `/home/coolhand/html/datavis/` has sufficient free space
- Check with: `df -h /home/coolhand/html/datavis/`

**Time Estimate**:
- GitHub auth + renames: ~10 min
- Local filesystem ops (Tasks 2, 5-7): ~30 min
- Data copies (Task 6): ~15 min (depends on disk I/O)
- GitHub repo creation (Tasks 8-12): ~45 min
- HuggingFace publication (Task 13): ~45 min
- Kaggle publication (Task 14): ~30 min (plus manual web UI)
- Cleanup (Task 15): ~10 min
- **Total**: ~3 hours (sequential) or ~1.5 hours (parallelized where possible)

**Parallelization Opportunities**:
- Tasks 2-4 can run in parallel (local renames + GitHub renames)
- Tasks 5-7 can run in parallel (symlink replacement + data harvesting + archive)
- Tasks 8-12 can run in parallel (create 5 GitHub repos simultaneously)
- Tasks 13-14 can run in parallel (HF + Kaggle publication)

---

**Status**: READY FOR EXECUTION
**Next Action**: Start with Task 1 (GitHub auth re-authentication)
