Implementation Plan: HealthChecks Enhancements
===========================================

Goals
- Ensure PreFlight and PostInstall healthchecks are non-destructive by default.
- Add comprehensive data collection (hardware, OS, network, packages, updates, features, users, permissions).
- Add reporting schema and generators for HTML (fancy), CSV/XLSX, DOCX, PDF.
- Provide opt-in variables for installing required dependencies and applying non-read-only changes.
- Seed product-specific postinstall/preflight roles and expand checks iteratively.

Top-level TODOs
1. Add `install_deps` and `apply_changes` variables to templates; default to false.
2. Make package-install and state-changing tasks conditional on `install_deps` / `apply_changes`.
3. Extend `postinstall_template` to collect hardware information (dmidecode/lsblk/lspci), partition data, subscription/registration, insights/rhc checks (RHEL), update lists, etc.
4. Define a JSON report schema (`PostInstall_Healthcheck/report_schema.json`) with ordered sections for consumer-friendly reports.
5. Implement report builders:
   - `compare_snapshots.py` (exists) — extend to new keys
   - `generate_html_report.py` (exists) — enhance with graphs
   - `build_reports.py` — create CSV/XLSX, DOCX, PDF outputs using optional Python libraries
6. Create `scripts/install_requirements.sh` to optionally install Python reporting libs.
7. Add CI workflow to validate report generation (sample fixtures) — already present; extend as needed.
8. Iterate per-product checks: start with RHEL, Satellite, AAP, OpenShift, Ceph, RHOSP.

Execution plan (first pass)
- Implement items 1,2,3 and 4 in this repo iteration (safe changes, small edits).
- Add `build_reports.py` that calls existing HTML generator, and attempts XLSX/DOCX/PDF if libs available.
- Add `scripts/install_requirements.sh` and `report_schema.json` in `PostInstall_Healthcheck`.

Next iterations
- Implement product-specific deep checks and add them to PreFlight and PostInstall role folders.
- Add visual graphs in HTML using Matplotlib and embed images in reports.
