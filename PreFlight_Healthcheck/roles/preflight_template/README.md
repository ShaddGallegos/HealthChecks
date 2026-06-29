Preflight template role
======================

This role contains generic checks and fixes. Copy or clone it to create product-specific roles.

Variables
- `preflight_admin_user` — username to create and grant passwordless sudo (default: `admin`)
- `preflight_container_rootless` — boolean to configure rootless podman (default: false)
