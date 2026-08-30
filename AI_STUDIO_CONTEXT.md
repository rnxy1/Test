# AI Studio Context — Marley Source Bundle

This repository is a source-analysis bundle.

## Primary code to analyze

### Marley Health
Path: `vendor/marley/`

Upstream: https://github.com/earthians/marley
Pinned branch at import time: `version-16`

Use this for healthcare domain logic, patient records, appointments, encounters, therapy, billing integration, validation rules, and mature workflow behavior.

### Marley Frontend
Path: `vendor/marley_frontend/`

Upstream: https://github.com/earthians/marley_frontend
Pinned branch at import time: `develop`

Use this for the modern Marley UI, appointment desk, registration, waitlist, check-in, queue/token workflows, kiosk, payment UX, reusable frontend components, and navigation patterns.

## Runtime dependencies not copied into this repository

Marley is not standalone. Its runtime depends on:

- Frappe Framework v16: https://github.com/frappe/frappe/tree/version-16
- ERPNext v16: https://github.com/frappe/erpnext/tree/version-16

Do not assume this repository can run by itself without those dependencies.

## Intended use

The repository is primarily meant for AI-assisted inspection, comparison, UI/workflow study, and later selective adaptation into another application.

When analyzing it:

1. Inspect the real source code, not only README files.
2. Distinguish Marley backend/domain behavior from Marley Frontend UI behavior.
3. Trace important frontend actions back to the backend APIs/DocTypes they depend on.
4. Identify reusable healthcare workflows and invariants rather than blindly copying Frappe-specific implementation details.
5. Treat `UPSTREAM_VERSIONS.md` as the record of the exact imported upstream commits.
