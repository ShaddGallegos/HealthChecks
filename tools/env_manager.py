#!/usr/bin/env python3
"""
Simple env.yml manager for HealthChecks.
Features:
- Ensure ~/.ansible/conf/env.yml exists (encrypted if vault password file present)
- Show/decrypt content
- Add top-level keys uniquely

Requires: ansible-vault and PyYAML (for add/show operations)
"""
import argparse
import os
import subprocess
from pathlib import Path
import sys

HOME = Path(os.path.expanduser('~'))
CONF_DIR = HOME / '.ansible' / 'conf'
ENV_FILE = CONF_DIR / 'env.yml'
VAULTPASS = CONF_DIR / '.vaultpass.txt'


def run(cmd, check=False, capture_output=False):
    return subprocess.run(cmd, shell=True, check=check, capture_output=capture_output, text=True)


def is_encrypted(path: Path):
    # Heuristic: ansible-vault view will succeed for encrypted file if vaultpass exists
    if not path.exists():
        return False
    try:
        if VAULTPASS.exists():
            r = run(f"ansible-vault view {str(path)} --vault-password-file {str(VAULTPASS)}", capture_output=True)
            return r.returncode == 0
        else:
            # no vaultpass, inspect header
            with path.open('r') as fh:
                first = fh.readline()
            return first.startswith('$ANSIBLE_VAULT')
    except Exception:
        return False


def read_env_plain(path: Path):
    if not path.exists():
        return {}
    # try ansible-vault view first
    if VAULTPASS.exists():
        r = run(f"ansible-vault view {str(path)} --vault-password-file {str(VAULTPASS)}", capture_output=True)
        if r.returncode == 0:
            return r.stdout
    # fallback to plain read
    return path.read_text()


def write_env_plain(path: Path, content: str):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content)
    # If vaultpass exists, encrypt the file
    if VAULTPASS.exists():
        run(f"ansible-vault encrypt {str(path)} --vault-password-file {str(VAULTPASS)}")


def ensure_env():
    if ENV_FILE.exists():
        print(f"{ENV_FILE} already exists")
        return 0
    print(f"Creating {ENV_FILE} (encrypted if {VAULTPASS} present)")
    write_env_plain(ENV_FILE, "{}\n")
    return 0


def show_env():
    content = read_env_plain(ENV_FILE)
    print(content)
    return 0


def add_key(key, value):
    try:
        import yaml
    except Exception:
        print('PyYAML is required for add/show operations. Install via: pip install pyyaml')
        return 2
    content = read_env_plain(ENV_FILE)
    try:
        data = yaml.safe_load(content) or {}
    except Exception:
        print('Failed to parse YAML content')
        return 2
    if key in data:
        print(f"Key '{key}' already present; skipping to keep entries unique")
        return 0
    # attempt to parse value as YAML literal
    try:
        val_parsed = yaml.safe_load(value)
    except Exception:
        val_parsed = value
    data[key] = val_parsed
    new_text = yaml.safe_dump(data, default_flow_style=False)
    # write plain then encrypt
    # if file was encrypted, decrypt to tmp then write and re-encrypt
    write_env_plain(ENV_FILE, new_text)
    print(f"Added key '{key}' to {ENV_FILE}")
    return 0


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--ensure', action='store_true', help='Create env.yml if not present')
    p.add_argument('--show', action='store_true', help='Show env.yml contents (decrypted if needed)')
    p.add_argument('--add', nargs=2, metavar=('KEY','VALUE'), help='Add a top-level key (unique)')
    args = p.parse_args()

    if args.ensure:
        return ensure_env()
    if args.show:
        return show_env()
    if args.add:
        k, v = args.add
        return add_key(k, v)
    p.print_help()
    return 0

if __name__ == '__main__':
    sys.exit(main())
