#!/usr/bin/env bash
set -euo pipefail

echo "Installing optional Python reporting requirements into current environment or venv..."
REQS=(python-docx openpyxl weasyprint matplotlib pandas jinja2)

if [ -n "${VIRTUAL_ENV-}" ]; then
  echo "Using virtualenv: $VIRTUAL_ENV"
else
  echo "No VIRTUAL_ENV detected — install into current Python environment"
fi

python3 -m pip install --upgrade pip
for r in "${REQS[@]}"; do
  echo "Installing $r..."
  python3 -m pip install "$r" || echo "Failed to install $r (continue)"
done

echo "Done. Note: wkhtmltopdf is not installed by this script; install via system package manager if you need PDF from HTML via wkhtmltopdf."
