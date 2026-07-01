#!/usr/bin/env bash
set -euo pipefail

THIS_DIR="$(cd "$(dirname "$0")" && pwd)"
HEALTH_ROOT="$(cd "$THIS_DIR/.." && pwd)"
PRE_DIR="$(cd "$HEALTH_ROOT/../PreFlight_Healthcheck/roles" && pwd)"
TARGET_DIR="$HEALTH_ROOT/roles"

if [ "$#" -lt 1 ]; then
  echo "Usage: $0 product1 [product2 ...]"
  exit 1
fi

for product in "$@"; do
  src="$PRE_DIR/$product"
  dst="$TARGET_DIR/$product"
  if [ ! -d "$src" ]; then
    echo "Source role not found: $src" >&2
    continue
  fi
  if [ -d "$dst" ]; then
    echo "Target already exists, skipping: $dst"
    continue
  fi
  echo "Copying $src -> $dst"
  mkdir -p "$(dirname "$dst")"
  cp -a "$src" "$dst"
done

echo "Done. Review and customize $TARGET_DIR/<product>/tasks for product-specific postinstall checks."
