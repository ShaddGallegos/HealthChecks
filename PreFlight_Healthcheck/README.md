PreFlight Healthcheck
=====================

This directory contains a reusable Ansible "preflight" role template, a prompting role,
helper scripts to manage `~/.ansible/conf/env.yml` (encrypted with `ansible-vault`),
and a simple playbook to run checks for a given product.

Quick commands
- Initialize vault and env file:

```
./scripts/manage_env.py --init
```

- Create product roles from the template (defaults to a common set):

```
./scripts/create_product_role.sh rhel aap satellite
```

- Prompt for variables for a product (invoked by the playbook or run locally):

```
./scripts/prompt_for_vars.py --product rhel
```

- Run the preflight checks (example):

```
ansible-playbook preflight.yml -i inventory.ini -e "product_name=rhel" --vault-password-file ~/.ansible/conf/.vaultpass.txt
```

Files of interest
- `roles/preflight_template` — the generic role that performs checks and fixes.
- `roles/preflight_prompt` — role that invokes the prompt helper for product variables.
- `scripts/manage_env.py` — creates/updates/encrypts `~/.ansible/conf/env.yml` (adds keys uniquely).
- `scripts/prompt_for_vars.py` — prompts for product-specific secrets/variables and stores them.
- `scripts/create_product_role.sh` — clones the template into `roles/<product>`.

Notes
- `~/.ansible/conf/env.yml` is encrypted with `ansible-vault` by default and the vault password is stored in
  `~/.ansible/conf/.vaultpass.txt` (created with permissions 600 if it doesn't exist).
- By default new keys are appended for a product and existing keys are preserved unless `--reconfigure` is used
  with `manage_env.py` or the prompting script.
