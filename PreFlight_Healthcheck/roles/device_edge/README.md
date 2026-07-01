Device Edge PreFlight healthcheck role skeleton.

This role contains discovery checks for Red Hat Device Edge prior to install/upgrade.
Tuning and changes must be implemented in `tasks/tuning.yml` and are only included when `apply_changes: true`.

Defaults and check templates should be updated with product-specific checks following Red Hat documentation.
