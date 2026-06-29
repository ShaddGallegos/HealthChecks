#!/usr/bin/env python3
"""
prompt_for_vars.py

Prompt for product-specific vars and store them into ~/.ansible/conf/env.yml uniquely.
"""

import argparse
import getpass
import yaml
from pathlib import Path
import subprocess
import os
import sys

CONF_DIR = Path.home() / ".ansible" / "conf"
ENV_FILE = CONF_DIR / "env.yml"
VAULTPASS = CONF_DIR / ".vaultpass.txt"


def decrypt_if_needed():
    try:
        subprocess.run(["ansible-vault", "decrypt", str(ENV_FILE), "--vault-password-file", str(VAULTPASS)], check=True)
    except subprocess.CalledProcessError:
        pass


def encrypt_if_needed():
    subprocess.run(["ansible-vault", "encrypt", str(ENV_FILE), "--vault-password-file", str(VAULTPASS)])


def read_env():
    if not ENV_FILE.exists():
        return {}
    try:
        decrypt_if_needed()
    except Exception:
        pass
    with open(ENV_FILE) as f:
        return yaml.safe_load(f) or {}


def write_env(data):
    with open(ENV_FILE, "w") as f:
        yaml.dump(data, f, default_flow_style=False)
    encrypt_if_needed()


def prompt_vars(product, reconfigure=False):
    data = read_env()
    if reconfigure or product not in data:
        data[product] = {}
    print(f"Prompting for variables for {product}. Leave blank to keep existing values.")
    prompts = [
        ("admin_user", "Admin username", "admin"),
        ("admin_password", "Admin password (will be stored encrypted)", ""),
        ("repo_baseurl", "Product repository base URL", ""),
        ("installer_token", "Installer token or password", ""),
        ("container_rootless", "Enable rootless podman (yes/no)", "no"),
    ]
    for key, label, default in prompts:
        existing = data[product].get(key, "")
        if existing:
            prompt = f"{label} [{existing}]: "
        elif default:
            prompt = f"{label} [{default}]: "
        else:
            prompt = f"{label}: "
        if "password" in key or "token" in key:
            val = getpass.getpass(prompt)
        else:
            val = input(prompt)
        if val:
            data[product][key] = val
    write_env(data)
    print("Saved variables to env.yml")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--product", required=True)
    parser.add_argument("--reconfigure", action="store_true")
    args = parser.parse_args()
    prompt_vars(args.product, reconfigure=args.reconfigure)


if __name__ == "__main__":
    main()
