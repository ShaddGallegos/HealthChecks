# HealthChecks

This repository collects several Ansible-based healthcheck and reporting workflows for Red Hat products and supporting infrastructure. Each top-level directory is a focused automation package with its own playbooks, roles, templates, and artifact outputs.

## What lives where

| Directory | Purpose |
| --- | --- |
| [AAP_Healthcheck](AAP_Healthcheck) | Health and tuning checks for Red Hat Ansible Automation Platform environments. It focuses on readiness, configuration evidence, and optional performance tuning for AAP deployments. |
| [Discovery_Healthcheck](Discovery_Healthcheck) | Read-only checks for Red Hat Discovery environments. It validates connectivity, runtime availability, and evidence collection for Discovery workflows. |
| [ennvironments](ennvironments) | A catalog of per-product execution environment definitions used to build Ansible Automation Platform execution environments with Ansible Builder. Each subdirectory typically contains an `execution-environment.yml` file for a specific product or target platform. |
| [Inventory_Healthcheck](Inventory_Healthcheck) | Network and fleet inventory discovery. It fingerprints hosts, enriches results where possible, and exports reports for broad visibility. |
| [PostInstall_Healthcheck](PostInstall_Healthcheck) | Post-install validation and optional remediation framework. It is designed to report by default and only apply changes when explicitly enabled. |
| [PreFlight_Healthcheck](PreFlight_Healthcheck) | Preflight checks for product deployments. It prepares shared variables, prompts for required values, and validates prerequisites before installation or configuration steps. |
| [Satellite_Healthcheck](Satellite_Healthcheck) | Healthcheck, audit, and optional tuning workflow for Red Hat Satellite environments. It validates the deployment and can produce a consolidated report of findings. |

## How the repository is organized

The repository follows a common pattern across the healthcheck areas:

- a primary playbook that drives the workflow
- supporting roles and task files for the checks themselves
- templates for generated configuration or reports
- artifact directories for exported JSON, CSV, or Markdown output
- product-specific execution environment definitions under [ennvironments](ennvironments)

That structure makes the individual healthchecks easier to run independently while still keeping the implementation style consistent across the repo.

## Typical usage

Most workflows are launched from the repository root with `ansible-playbook`, using the playbook that belongs to the area you want to inspect.

Examples:

```bash
ansible-playbook AAP_Healthcheck/aap_production_orchestrator.yml
ansible-playbook Discovery_Healthcheck/discovery_healthcheck.yml
ansible-playbook Inventory_Healthcheck/network_inventory.yml
ansible-playbook run_preflight.yml
ansible-playbook run_postinstall.yml
ansible-playbook Satellite_Healthcheck/satellite_production_orchestrator.yml
```

Some workflows are intentionally report-only by default. Review the README in each directory before running against production systems so you understand what is safe, what is optional, and what inputs are required.

## Repository-level files

- `ansible.cfg` sets repository-wide Ansible behavior.
- `inventory.ini` provides a shared inventory example.
- `run_preflight.yml`, `run_postinstall.yml`, and `setup_env.yml` are top-level orchestration entry points.
- `generate_reports.yml` and `tools/` provide shared reporting and helper utilities.

## Notes

- The directory name `ennvironments` is kept as-is in the repository.
- Several healthchecks produce JSON, Markdown, CSV, or other audit artifacts for later review.
- If you are adding a new healthcheck area, follow the same layout so it fits the rest of the repository cleanly.

## Optional HTTP service

This repository now includes a lightweight HTTP service that can run healthcheck plugins, expose Prometheus metrics, and schedule periodic checks. The service lives in `HealthChecks/service/` and is useful when you want an always-on runner, metrics export, or alerting hooks.

See `HealthChecks/service/README.md` for details on running the service and writing plugin checks.