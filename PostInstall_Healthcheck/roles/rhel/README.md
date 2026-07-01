# rhel Role

## Title
rhel HealthCheck Role

## Synopsis
The rhel role performs product-specific health validation and reporting in the PostInstall_Healthcheck workflow.

## Quickstart
Run this role through the corresponding top-level runner from /home/sgallego/GIT/HealthChecks:

    cd /home/sgallego/GIT/HealthChecks
    ansible-playbook run_postinstall.yml -e "products=['rhel']"

Apply/remediation mode (opt-in):

    cd /home/sgallego/GIT/HealthChecks
    ansible-playbook run_postinstall.yml -e "products=['rhel'] healthcheck_check_mode_only=false"

## Responsibilities
- Load product-specific configuration and secrets
- Validate prerequisites and runtime signals
- Emit structured report artifacts
- Optionally apply safe, explicit changes when enabled

## Variables
Common role defaults discovered from PostInstall_Healthcheck/roles/rhel/defaults/main.yml:
- rhel_product_repos
- rhel_product_prereq_packages
- rhel_product_required_secrets
- rhel_product_required_mounts

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
    ansible-playbook --syntax-check run_postinstall.yml

## Related Files
- PostInstall_Healthcheck/roles/rhel/tasks/main.yml
- PostInstall_Healthcheck/roles/rhel/defaults/main.yml
