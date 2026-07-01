# PostInstall HealthCheck

## Title
PostInstall HealthCheck and Safe Remediation Framework

## Synopsis
`PostInstall_Healthcheck` validates and optionally tunes deployed Red Hat product environments. The framework runs in non-destructive check/report mode by default and only applies changes when explicitly enabled.

## Quickstart
1. Run in default report-only mode.
2. Review per-role reports and consolidated package-gap rollups.
3. Opt into installs/remediation only when ready.

```bash
cd /home/sgallego/GIT/HealthChecks
ansible-playbook run_postinstall.yml
```

Optional apply mode:
```bash
cd /home/sgallego/GIT/HealthChecks
ansible-playbook run_postinstall.yml -e "healthcheck_check_mode_only=false"
```

## Core Concepts
- Safe default: `healthcheck_check_mode_only: true`
- Install/remediation enabled only when mode is set to `false`
- Unified rollups:
  - `postinstall-package-gap-rollup.json`
  - `postinstall-package-gap-rollup.csv`

## Artifacts
- Role-level postinstall JSON reports.
- Tuning/service/firewall/security evidence.
- Optional product-specific exports (for example Satellite/AAP features).

## Troubleshooting
- Confirm env vars file exists: `~/.ansible/conf/env.yml`
- Ensure writable artifact/report paths for the executing user.
- Run syntax checks before broad execution.

## Testing and Validation
```bash
cd /home/sgallego/GIT/HealthChecks
ansible-playbook --syntax-check run_postinstall.yml
```

## Role Index
- [roles/aap](roles/aap/README.md)
- [roles/aap_eda](roles/aap_eda/README.md)
- [roles/acm](roles/acm/README.md)
- [roles/acs](roles/acs/README.md)
- [roles/ai_enterprise](roles/ai_enterprise/README.md)
- [roles/ai_inference](roles/ai_inference/README.md)
- [roles/amq](roles/amq/README.md)
- [roles/apache_camel](roles/apache_camel/README.md)
- [roles/application_foundations](roles/application_foundations/README.md)
- [roles/ceph](roles/ceph/README.md)
- [roles/certificate_system](roles/certificate_system/README.md)
- [roles/data_grid](roles/data_grid/README.md)
- [roles/developer_hub](roles/developer_hub/README.md)
- [roles/device_edge](roles/device_edge/README.md)
- [roles/directory_server](roles/directory_server/README.md)
- [roles/gitea](roles/gitea/README.md)
- [roles/idm](roles/idm/README.md)
- [roles/insights](roles/insights/README.md)
- [roles/jboss_eap](roles/jboss_eap/README.md)
- [roles/jboss_webserver](roles/jboss_webserver/README.md)
- [roles/keycloak](roles/keycloak/README.md)
- [roles/migration_toolkit](roles/migration_toolkit/README.md)
- [roles/openshift](roles/openshift/README.md)
- [roles/openshift_ai](roles/openshift_ai/README.md)
- [roles/openshift_local](roles/openshift_local/README.md)
- [roles/postinstall_template](roles/postinstall_template/README.md)
- [roles/quarkus](roles/quarkus/README.md)
- [roles/quay](roles/quay/README.md)
- [roles/rhel](roles/rhel/README.md)
- [roles/rhel_ai](roles/rhel_ai/README.md)
- [roles/rhosp](roles/rhosp/README.md)
- [roles/satellite](roles/satellite/README.md)
- [roles/shared_tuning](roles/shared_tuning/README.md)
- [roles/single_node_openshift](roles/single_node_openshift/README.md)
- [roles/three_scale](roles/three_scale/README.md)
