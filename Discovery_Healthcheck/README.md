# Discovery HealthCheck

## Purpose

This healthcheck provides a safe, read-only baseline for Red Hat Discovery environments.
It is aligned with the Discovery positioning from Red Hat article 4605801 as a reporting tool,
and focuses on readiness and evidence collection instead of remediation.

## What It Checks

- Container runtime availability (podman/docker) and version
- Presence of Discovery-related image names in local runtime images
- DNS and HTTPS reachability to key endpoints used by Discovery workflows
- Discovery-related services/containers and recent journal errors
- Structured JSON plus Markdown report output

## Run

```bash
cd /home/sgallego/GIT/HealthChecks/Discovery_Healthcheck
ansible-playbook discovery_healthcheck.yml
```

## Artifacts

By default, artifacts are written to:

- ./discovery_reports/discovery_healthcheck_report.json
- ./discovery_reports/discovery_healthcheck_report.md

You can override the output path:

```bash
ansible-playbook discovery_healthcheck.yml -e "discovery_healthcheck_output_dir=/tmp/discovery_reports"
```

## Notes

- The checks are intentionally non-destructive.
- Some environments require proxies or custom trust chains; those typically show up as warnings in connectivity checks.
- You can add Satellite/Capsule-specific checks in new task files and include them from tasks/main.yml.
