# network_inventory Role

## Title
network_inventory HealthCheck Role

## Synopsis
The network_inventory role performs product-specific health validation and reporting in the Inventory_Healthcheck workflow.

## Quickstart
Run this role through the corresponding top-level runner from /home/sgallego/GIT/HealthChecks:

    cd /home/sgallego/GIT/HealthChecks
    ansible-playbook network_inventory.yml

## Responsibilities
- Load product-specific configuration and secrets
- Validate prerequisites and runtime signals
- Emit structured report artifacts
- Optionally apply safe, explicit changes when enabled

## Variables
Common role defaults discovered from Inventory_Healthcheck/roles/network_inventory/defaults/main.yml:
- network_inventory_target_segments
- network_inventory_discovery_ports
- network_inventory_required_tools

## Tags
Typical tags used by this framework include:
- always, secrets, prereqs, report
- Product roles may also use repos, services, security, and network

## Inputs and Dependencies
- Environment config: ~/.ansible/conf/env.yml
- Sudo/root execution context for system-level checks
- Network/package manager access when install/remediation mode is enabled

## Outputs
- Product report artifacts under configured artifacts_dir
- Role-specific findings for package gaps, service state, and system readiness

## Safety and Execution Mode
- Default behavior is non-destructive report mode
- Install/remediation actions require explicit opt-in
- Respects ansible_check_mode and framework safety flags

## Role Structure
- tasks/main.yml: orchestration entrypoint
- defaults/main.yml: role defaults (when present)
- Optional task includes for tuning/report exports

## Troubleshooting
- Run syntax checks for runner playbooks before execution
- Validate required secrets in ~/.ansible/conf/env.yml
- Confirm artifact path permissions for the executing user

## Validation
    cd /home/sgallego/GIT/HealthChecks
    ansible-playbook --syntax-check network_inventory.yml

## Related Files
- Inventory_Healthcheck/roles/network_inventory/tasks/main.yml
- Inventory_Healthcheck/roles/network_inventory/defaults/main.yml
