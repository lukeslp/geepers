# API Credentials & Configuration Inventory
**Searcher Report** | 2026-02-10

---

## 1. CREDENTIALS FOUND

### Kaggle API Authentication
**Status**: ✅ ACTIVE

**Files**:
- Primary: `/home/coolhand/kaggle.json` (68 bytes)
- Backup: `/home/coolhand/.kaggle/kaggle.json`

**Configuration**:
- Format: JSON
- Type: API credentials
- Location: Standard Kaggle configuration directory

**Used By**:
- data_trove fetchers (potentially)
- Any scripts using `kaggle` Python package

**Permissions**: User-writable (mode 600 recommended for security)

---

### Hugging Face Configuration
**Status**: ⚠️ NO TOKEN FILE FOUND

**Cache Present**: Yes
- Location: `/home/coolhand/html/datavis/data_trove/tools/fetchers/cache/`
- Cached Datasets: 4+ (NUFORC, Social Norms, Social Chemistry, AAC)

**Authentication**:
- No `~/.huggingface/token` file (uses default public access)
- Uses environment variable `HF_TOKEN` if available
- Falls back to public/unauthenticated access

**Hugging Face Datasets Cached**:
1. `datasets--willwade--AACConversations` - AAC corpus
2. `datasets--kcimc--NUFORC` - UFO reports (~2GB)
3. `datasets--socialnormdataset--social` - Social norms
4. `datasets--tasksource--social-chemestry-101` - Social chemistry

---

### Census Bureau API
**Status**: ✅ CONFIGURED (in dev projects)

**Location**: Stored in project `.env` files (not in data_trove)

**Used By**:
- `/home/coolhand/html/datavis/dev/veterans/` - population/employment data
- `/home/coolhand/html/datavis/dev/food_deserts/` - poverty estimates
- `/home/coolhand/html/datavis/dev/housing_crisis/` - housing burden

**Configuration**:
- Key: `CENSUS_API_KEY` (environment variable)
- Endpoint: https://api.census.gov/data/
- Source: https://api.census.gov/data/key_signup.html
- Rate Limiting: None for registered keys

**Datasets Accessed**:
- ACS 5-Year (demographics)
- SAIPE (poverty)
- CBP (business patterns)

---

### GitHub Access
**Status**: ✅ CONFIGURED

**Repository**: https://github.com/lukeslp/data_trove.git

**Authentication**:
- Method: Basic authentication (configured in Git LFS)
- Config File: `/home/coolhand/html/datavis/data_trove/.git/config`
- LFS Access: `basic` mode enabled

**Configuration Details**:
```ini
[lfs "https://github.com/lukeslp/data_trove.git/info/lfs"]
    access = basic
[http]
    postBuffer = 524288000  # 512MB for large uploads
```

**Purpose**:
- Push/pull data_trove repository
- Sync with GitHub mirror
- Git LFS for large files (>100MB)

---

### NOAA / USGS APIs
**Status**: ✅ PUBLIC (no authentication needed)

**Used By**:
- `dev/scars/` - Geological data
- `dev/veterans/` - Tornado/climate data
- Quirky datasets - Aurora, tornadoes, geothermal

**Endpoints**:
- NOAA Weather API: https://api.weather.gov/
- NOAA NCEI: https://www.ncei.noaa.gov/
- USGS Earthquake: https://earthquake.usgs.gov/
- USGS Water: https://waterservices.usgs.gov/

**No Auth Required**: Public access via rate limiting

---

### NASA APIs
**Status**: ✅ PUBLIC (no authentication needed)

**Used By**:
- Quirky datasets: asteroids_real, planets_real, moons_real
- Data fetchers in tools/

**Endpoints**:
- NASA Data API: https://api.nasa.gov/
- JPL Horizons: https://ssd-api.jpl.nasa.gov/

**No Auth Required**: Public access with API key (but optional for most endpoints)

---

## 2. CREDENTIAL STORAGE ANALYSIS

### Secure Storage
✅ **Kaggle**: Stored in home directory with implicit `~/.kaggle/kaggle.json` permissions
✅ **GitHub**: SSL/TLS via HTTPS, LFS authentication integrated
✅ **Census**: Stored in project `.env` files (gitignored)

### Security Gaps
⚠️ **Kaggle credentials**: Readable by all users on system (if not properly restricted)
⚠️ **Hugging Face**: No token configured (relies on unauthenticated access)
⚠️ **Git config**: HTTP post buffer may allow large anonymous uploads (DoS risk)

### Recommendations
1. **Restrict file permissions**:
   ```bash
   chmod 600 ~/.kaggle/kaggle.json
   chmod 600 ~/.kaggle/kaggle.json
   ```

2. **Use environment variables** for sensitive APIs:
   ```bash
   export KAGGLE_USERNAME=...
   export KAGGLE_KEY=...
   export HF_TOKEN=...
   ```

3. **Rotate credentials** periodically (especially GitHub/Kaggle)

4. **Audit access logs** in `.git/config` for unexpected changes

---

## 3. CONFIGURATION FILES INVENTORY

| File | Type | Status | Purpose |
|------|------|--------|---------|
| `/home/coolhand/kaggle.json` | JSON | ✅ Active | Kaggle API auth |
| `/home/coolhand/.kaggle/kaggle.json` | JSON | ✅ Active | Kaggle backup |
| `/home/coolhand/html/datavis/data_trove/.git/config` | INI | ✅ Active | Git LFS config |
| `dev/*/. env` | Shell | ✅ Active | Project secrets (gitignored) |
| `~/.bashrc` or `~/.zshrc` | Shell | ? | Environment exports |
| `~/.ssh/config` | SSH | ? | Git SSH config (if used) |

---

## 4. HUGGING FACE CACHE BREAKDOWN

**Total Cached**: 2+ GB (primarily NUFORC dataset)

**Cache Structure**:
```
tools/fetchers/cache/
├── quirky/
│   ├── datasets--kcimc--NUFORC/ (2+ GB)
│   │   └── snapshots/197d19c561.../nuforc_*.csv
│   ├── datasets--socialnormdataset--social/
│   │   └── snapshots/43de4f85.../data/*.parquet
│   └── datasets--tasksource--social-chemestry-101/
│       └── snapshots/a329cc50.../social-chem-101.v1.0.tsv
└── accessibility/
    └── datasets--willwade--AACConversations/
        └── snapshots/fe117e51.../README.md
```

**Recommendation**: Implement cache cleanup strategy
- Archive old snapshots
- Compress parquet files
- Document cache expiration policy

---

## 5. ENVIRONMENT VARIABLE REFERENCES

### Likely Used (from CLAUDE.md references)
```bash
# Census API
export CENSUS_API_KEY=...

# GitHub
export GH_TOKEN=...          # gh CLI
export GITHUB_TOKEN=...      # git operations

# Hugging Face
export HF_TOKEN=...          # HF dataset access

# Kaggle
export KAGGLE_USERNAME=...
export KAGGLE_KEY=...

# Data paths
export PYTHONPATH=/home/coolhand/shared:$PYTHONPATH
export USE_CACHED_DATA=true  # Use cached API responses
```

### Storage Locations
- Shell config: `~/.bashrc`, `~/.zshrc`, `~/.fish/config.fish`
- Project level: `dev/*/.env` (gitignored)
- System level: `/etc/environment` (root only)

---

## 6. API ENDPOINTS DISCOVERED

### Active Integrations
```
Census Bureau API
├── https://api.census.gov/data/2022/acs/acs5
├── https://api.census.gov/data/2022/saipe
└── https://api.census.gov/data/2022/cbp

GitHub API (for data_trove sync)
├── https://github.com/lukeslp/data_trove.git
└── https://github.com/lukeslp/data_trove/releases

Hugging Face Datasets
├── datasets--kcimc--NUFORC
├── datasets--socialnormdataset--social
├── datasets--tasksource--social-chemestry-101
└── datasets--willwade--AACConversations

NASA APIs
├── https://api.nasa.gov/
├── https://ssd-api.jpl.nasa.gov/

NOAA APIs
├── https://api.weather.gov/
├── https://www.ncei.noaa.gov/

Kaggle API
└── https://kaggle.com/api/v1
```

---

## 7. SECURITY ASSESSMENT

### Critical Items
🔴 **Kaggle credentials file**: World-readable if in default location
🔴 **Git config**: Contains HTTP buffer settings for large uploads

### Important Items
🟡 **No HF token stored**: Relies on unauthenticated access (rate limiting risk)
🟡 **Env variables**: Not centralized (scattered across projects)
🟡 **Cache management**: No documented cleanup strategy

### Good Practices
🟢 **GitHub SSH config**: Uses HTTPS with LFS (secure)
🟢 **Census API**: Uses environment variables (.env pattern)
🟢 **.gitignore**: Properly excludes sensitive files

### Recommendations
1. **Immediate**:
   - Audit all `.env` files for sensitive data
   - Restrict Kaggle JSON permissions to 600
   - Document all credentials in `/documentation/API_KEYS.md`

2. **Short-term**:
   - Centralize environment variables
   - Implement secrets management (e.g., `direnv` or `pass`)
   - Add credentials validation in startup scripts

3. **Long-term**:
   - Use cloud-based secrets management
   - Implement credential rotation
   - Add audit logging for API usage

---

## 8. INTEGRATION POINTS

### Data Collection Pipeline
```
Census API → dev/veterans/ → data_trove/demographic/veterans/ (symlink)
          → dev/food_deserts/ → data_trove/demographic/poverty/ (symlink)

GitHub → data_trove/ ← Git LFS (large files)
      ↓
local cache in tools/fetchers/cache/

Hugging Face → tools/fetchers/cache/ → data_trove/data/quirky/
            → quirky visualizations
```

### Fetch Workflow (from code)
```python
1. Check .env for API_KEY
2. Load from cache if USE_CACHED_DATA=true
3. Fetch from API if cache miss
4. Save to cache for reuse
5. Validate data (FIPS codes, timestamps, etc.)
6. Export to data/ directory
7. Symlink to data_trove/
```

---

## 9. FILES REQUIRING AUDIT

| File | Contains | Action |
|------|----------|--------|
| `/home/coolhand/kaggle.json` | Credentials | Verify permissions (600) |
| `/home/coolhand/.kaggle/kaggle.json` | Credentials | Verify permissions (600) |
| `dev/*/.env` | API keys | Review for exposure |
| `dev/*/.env.example` | Templates | Verify no actual keys |
| `/documentation/API_KEYS.md` | Master list | Verify access control |
| `.git/config` | Auth settings | Review HTTP buffer |

---

## 10. SUMMARY TABLE

| Service | Auth Method | Storage | Status | Risk Level |
|---------|------------|---------|--------|-----------|
| Kaggle | API Key | ~/.kaggle/kaggle.json | ✅ Active | 🟡 Medium |
| Hugging Face | Token | Env var | ⚠️ Default | 🟡 Medium |
| Census Bureau | API Key | .env files | ✅ Active | 🟢 Low |
| GitHub | HTTPS/LFS | .git/config | ✅ Active | 🟢 Low |
| NASA | API Key | Public | ✅ Public | 🟢 Low |
| NOAA | Public | N/A | ✅ Public | 🟢 Low |
| USGS | Public | N/A | ✅ Public | 🟢 Low |

---

**Report Summary**:
- **Credentials Found**: 2 active (Kaggle, GitHub)
- **Configuration Files**: 7+ identified
- **API Integrations**: 7 services (3 authenticated)
- **Security Gaps**: 2-3 items requiring attention
- **Cache Size**: 2+ GB (Hugging Face)
- **Recommendation**: Audit and implement secrets management

