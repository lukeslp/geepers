#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
export ROOT
DRY_RUN=0
DELETE_MODE=0
BUILD_FIRST=1
PLATFORM="all"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --platform)
      PLATFORM="$2"
      shift 2
      ;;
    --dry-run)
      DRY_RUN=1
      shift
      ;;
    --delete)
      DELETE_MODE=1
      shift
      ;;
    --skip-build)
      BUILD_FIRST=0
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

run_cmd() {
  if [[ "$DRY_RUN" -eq 1 ]]; then
    echo "[dry-run] $*"
  else
    eval "$@"
  fi
}

for line in "${PLATFORM_LINES[@]}"; do
  IFS='|' read -r name output_root mirror_repo metadata_file <<< "$line"

  if [[ "$PLATFORM" != "all" && "$name" != "$PLATFORM" ]]; then
    continue
  fi

  src_root="$ROOT/$output_root"
  src_skills="$src_root/skills"

  if [[ ! -d "$src_skills" ]]; then
    echo "Skipping $name: generated skills not found at $src_skills"
    continue
  fi

  if [[ -z "$mirror_repo" || ! -d "$mirror_repo" ]]; then
    echo "Skipping $name: mirror repo missing ($mirror_repo)"
    continue
  fi

  echo "Syncing $name -> $mirror_repo"
  mkdir -p "$mirror_repo/skills"

  if [[ "$DELETE_MODE" -eq 1 ]]; then
    run_cmd "rsync -a --delete '$src_skills/' '$mirror_repo/skills/'"
  else
    run_cmd "rsync -a '$src_skills/' '$mirror_repo/skills/'"
  fi

  if [[ -n "$metadata_file" && -f "$src_root/$metadata_file" ]]; then
    run_cmd "mkdir -p '$mirror_repo/$(dirname "$metadata_file")'"
    run_cmd "cp '$src_root/$metadata_file' '$mirror_repo/$metadata_file'"
  fi

  if [[ -f "$src_root/aliases.json" ]]; then
    run_cmd "cp '$src_root/aliases.json' '$mirror_repo/aliases.generated.json'"
  fi
done

echo "Sync complete."
