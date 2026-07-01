# Inventory HealthCheck

## Title
Inventory HealthCheck Suite

## Synopsis
`Inventory_Healthcheck` provides network discovery, service fingerprinting, SSH-assisted enrichment, Red Hat product correlation, and exportable reporting for fleet-level visibility.

## Quickstart
1. Run the inventory playbook from the `HealthChecks` directory.
2. Provide target ranges and credentials in your inventory/vars.
3. Review generated CSV/JSON/XLSX artifacts.

```bash
cd /home/sgallego/GIT/HealthChecks
ansible-playbook network_inventory.yml
```

## Directory Layout
- `roles/network_inventory/`: core scanning, enrichment, correlation, and reporting.
- `Inventory_Healthcheck/NetworkInventoy`: legacy script path kept for parity.
- `Inventory_Healthcheck/README.md`: this guide.

## Inputs
- Target IPs/ranges and scan controls.
- Optional SSH credentials for deep inspection.
- Product alias and confidence-scoring configuration in role vars/defaults.

## Outputs
- Host-level inventory reports.
- Product confidence scoring columns.
- Pivot summary outputs for fleet aggregation.

## Safety Model
- Read-only by default where possible.
- Focuses on discovery/reporting; does not perform remediation.

## Troubleshooting
- Validate scanner prerequisites (`nmap`, `rustscan`, `zmap`, etc.).
- Verify SSH reachability/credentials for enriched detection.
- Re-run with limited host scope for first-pass validation.

## Testing and Validation
```bash
cd /home/sgallego/GIT/HealthChecks
ansible-playbook --syntax-check network_inventory.yml
```

## Role Index
- [roles/network_inventory](roles/network_inventory/README.md)
