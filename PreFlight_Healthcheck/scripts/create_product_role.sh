#!/usr/bin/env bash
set -euo pipefail

if [ "$#" -lt 1 ]; then
  echo "Usage: $0 product_name [product_name ...]"
  exit 2
fi

ROOT_DIR="$(dirname "$(dirname "$0")")"
ROLES_DIR="$ROOT_DIR/roles"
TEMPLATE="$ROLES_DIR/preflight_template"

for p in "$@"; do
  dest="$ROLES_DIR/$p"
  if [ -d "$dest" ]; then
    echo "Role $p already exists, skipping"
    continue
  fi
  cp -a "$TEMPLATE" "$dest"
  echo "Created role $p"
done
