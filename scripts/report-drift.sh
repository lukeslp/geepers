#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
STRICT=0
SKIP_MISSING=0
BUILD_FIRST=0
PLATFORM="all"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --platform)
      PLATFORM="$2"
      shift 2
      ;;
    --strict)
      STRICT=1
      shift
      ;;
    --skip-missing)
      SKIP_MISSING=1
      shift
      ;;
    --build)
      BUILD_FIRST=1
      shift
      ;;
    *)
      echo "Unknown option: $1" >&2
      exit 1
      ;;
  esac
done

if [[ "$BUILD_FIRST" -eq 1 ]]; then
  python3 "$ROOT/scripts/build-platform-packages.py" --platform all --clean
fi

mapfile -t PLATFORM_LINES < <(python3 - <<'PY'
import yaml
from pathlib import Path
import os
root = Path(os.environ["ROOT"])
cfg = yaml.safe_load((root / "manifests/platforms.yaml").read_text(encoding="utf-8"))
for name, details in (cfg.get("platforms") or {}).items():
    out = details.get("output_root", "")
    mirror = details.get("mirror_repo", "")
    metadata = details.get("metadata_file", "")
    print(f"{name}|{out}|{mirror}|{metadata}")
PY
)

DRIFT_COUNT=0

for line in "${PLATFORM_LINES[@]}"; do
  IFS='|' read -r name output_root mirror_repo metadata_file <<< "$line"

  if [[ "$PLATFORM" != "all" && "$name" != "$PLATFORM" ]]; then
    continue
  fi

  src_root="$ROOT/$output_root"
  src_skills="$src_root/skills"

  if [[ ! -d "$src_skills" ]]; then
    echo "[warn] $name generated skills not found: $src_skills"
    ((DRIFT_COUNT++)) || true
    continue
  fi

  if [[ -z "$mirror_repo" || ! -d "$mirror_repo" ]]; then
    if [[ "$SKIP_MISSING" -eq 1 ]]; then
      echo "[skip] $name mirror missing: $mirror_repo"
      continue
    fi
    echo "[warn] $name mirror missing: $mirror_repo"
    ((DRIFT_COUNT++)) || true
    continue
  fi

  echo "Checking drift for $name"

  if ! diff -qr "$src_skills" "$mirror_repo/skills" >/tmp/geepers_drift_${name}.txt 2>&1; then
    echo "[drift] $name skill directory differs"
    sed -n '1,40p' /tmp/geepers_drift_${name}.txt
    ((DRIFT_COUNT++)) || true
  else
    echo "[ok] $name skills match"
  fi

  if [[ -n "$metadata_file" && -f "$src_root/$metadata_file" ]]; then
    if [[ ! -f "$mirror_repo/$metadata_file" ]]; then
      echo "[drift] $name missing metadata in mirror: $metadata_file"
      ((DRIFT_COUNT++)) || true
    elif ! cmp -s "$src_root/$metadata_file" "$mirror_repo/$metadata_file"; then
      echo "[drift] $name metadata differs: $metadata_file"
      ((DRIFT_COUNT++)) || true
    else
      echo "[ok] $name metadata matches"
    fi
  fi
done

echo "Drift check complete. Differences: $DRIFT_COUNT"

if [[ "$STRICT" -eq 1 && "$DRIFT_COUNT" -gt 0 ]]; then
  exit 1
fi
