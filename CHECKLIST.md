# HealthChecks — Checklist

Purpose: Collection of Ansible-driven health checks for RHEL products and infrastructure.

Prerequisites
- `ansible-core` installed
- Python 3 and required Python deps for particular checks

Quick start
```bash
cd HealthChecks
# Example runs
ansible-playbook PreFlight_Healthcheck/run_preflight.yml
ansible-playbook Satellite_Healthcheck/satellite_healthcheck.yml
ansible-playbook Inventory_Healthcheck/network_inventory.yml
```

Verify
- Output artifacts appear under `artifacts/` and `reports/`
- Check `generate_reports.yml` to generate consolidated HTML reports

Notes
- See `README.md` for the repository layout and per-check usage details.
