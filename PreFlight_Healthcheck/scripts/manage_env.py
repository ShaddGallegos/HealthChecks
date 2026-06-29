#!/usr/bin/env python3
"""
manage_env.py

Manage ~/.ansible/conf/env.yml and vault password file.

Features:
- Ensure ~/.ansible/conf/ exists
- Ensure ~/.ansible/conf/.vaultpass.txt exists (generate a random password)
- Ensure ~/.ansible/conf/env.yml exists (can be empty)
- Add key/value pairs uniquely per product section
- Encrypt/decrypt using ansible-vault via subprocess when available
"""

import argparse
import os
import sys
import stat
import yaml
import secrets
import subprocess
from pathlib import Path


CONF_DIR = Path.home() / ".ansible" / "conf"
VAULTPASS = CONF_DIR / ".vaultpass.txt"
ENV_FILE = CONF_DIR / "env.yml"


def ensure_conf_dir():
    CONF_DIR.mkdir(parents=True, exist_ok=True)


def ensure_vaultpass():
    if not VAULTPASS.exists():
        token = secrets.token_urlsafe(32)
        with open(VAULTPASS, "w") as f:
            f.write(token + "\n")
        os.chmod(VAULTPASS, stat.S_IRUSR | stat.S_IWUSR)


def ensure_env_file():
    if not ENV_FILE.exists():
        with open(ENV_FILE, "w") as f:
            f.write("# ansible env secrets\n")


def run_vault_encrypt():
    # encrypt in place if ansible-vault exists
    cmd = ["ansible-vault", "encrypt", str(ENV_FILE), "--vault-password-file", str(VAULTPASS)]
    try:
        subprocess.run(cmd, check=True)
    except FileNotFoundError:
        print("ansible-vault not found; env.yml left unencrypted")
    except subprocess.CalledProcessError:
        print("ansible-vault failed to encrypt env.yml; file may be unchanged or partially encrypted")


def run_vault_decrypt():
    cmd = ["ansible-vault", "decrypt", str(ENV_FILE), "--vault-password-file", str(VAULTPASS)]
    try:
        subprocess.run(cmd, check=True)
    except FileNotFoundError:
        print("ansible-vault not found; assuming env.yml is not encrypted")
    except subprocess.CalledProcessError:
        # failed to decrypt (maybe not encrypted), ignore
        pass


def read_env(decrypt=True):
    # Read raw content first to check if it's ansible-vault encrypted
    if not ENV_FILE.exists():
        return {}
    with open(ENV_FILE, "r") as f:
        content = f.read()

    if decrypt and content.lstrip().startswith("$ANSIBLE_VAULT"):
        try:
            run_vault_decrypt()
            with open(ENV_FILE, "r") as f:
                content = f.read()
        except Exception:
            # unable to decrypt but continue with raw content
            pass

    try:
        data = yaml.safe_load(content)
        if isinstance(data, dict):
            return data
        if data is None:
            return {}
    except Exception:
        # fallthrough to key=value parsing
        data = None

    # Fallback: parse simple KEY=VALUE lines into a dict
    parsed = {}
    for line in content.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if "=" in line:
            k, v = line.split("=", 1)
            parsed[k.strip()] = v.strip()
    return parsed


def write_env(data, encrypt=True):
    with open(ENV_FILE, "w") as f:
        yaml.dump(data, f, default_flow_style=False)
    if encrypt:
        try:
            run_vault_encrypt()
        except Exception:
            print("ansible-vault encrypt failed or is not available; env.yml written unencrypted")


def merge_unique(data, product, new_values, reconfigure=False):
    if product not in data or reconfigure:
        data[product] = new_values
        return data
    for k, v in new_values.items():
        if k not in data[product]:
            data[product][k] = v
    return data


def main():
    parser = argparse.ArgumentParser(description="Manage ~/.ansible/conf/env.yml")
    parser.add_argument("--init", action="store_true", help="Initialize conf dir, vaultpass and env file")
    parser.add_argument("--product", help="Product key to modify")
    parser.add_argument("--set", nargs=2, action="append", metavar=("KEY", "VALUE"), help="Set a key/value pair for product")
    parser.add_argument("--reconfigure", action="store_true", help="Replace product section")
    parser.add_argument("--decrypt", action="store_true", help="Decrypt and print env.yml")
    args = parser.parse_args()

    ensure_conf_dir()
    ensure_vaultpass()
    ensure_env_file()

    if args.init:
        print("Initialized", CONF_DIR)
        sys.exit(0)

    data = read_env(decrypt=True)

    if args.decrypt:
        print(yaml.dump(data, default_flow_style=False))
        sys.exit(0)

    if args.product and args.set:
        new_values = {k: v for k, v in args.set}
        data = merge_unique(data, args.product, new_values, reconfigure=args.reconfigure)
        write_env(data, encrypt=True)
        print("Updated env.yml")
        sys.exit(0)

    parser.print_help()


if __name__ == "__main__":
    main()
