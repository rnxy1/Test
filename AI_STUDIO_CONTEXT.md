# AI Studio Context — Full Marley / Frappe Source Bundle

This repository is a complete source-analysis bundle intended for import into Google AI Studio.

## Included source trees

### Frappe Framework
Path: `vendor/frappe/`

Upstream: https://github.com/frappe/frappe
Branch: `version-16`

Use this to understand the framework runtime, DocTypes, permissions, APIs, hooks, server behavior, desk architecture, background jobs, realtime behavior, and infrastructure relied on by ERPNext and Marley.

### ERPNext
Path: `vendor/erpnext/`

Upstream: https://github.com/frappe/erpnext
Branch: `version-16`

Use this for accounting, invoices, payments, allocations, receivables, journals, reversals, reconciliation, users/roles, HR and the ERP concepts Marley integrates with.

### Marley Health
Path: `vendor/marley/`

Upstream: https://github.com/earthians/marley
Branch: `version-16`

Use this for healthcare domain logic, patient records, appointments, encounters, practitioners, clinical records, therapy, billing integration, validation rules, healthcare workflows, and patient history.

### Marley Frontend
Path: `vendor/marley_frontend/`

Upstream: https://github.com/earthians/marley_frontend
Branch: `develop`

Use this for the modern Marley UI, appointment desk, registration, waitlist, check-in, queue/token workflows, kiosk, payment UX, reusable components, navigation patterns, and frontend/backend API relationships.

## Important architecture note

All four upstream codebases are copied into this repository for AI analysis.

This does NOT mean they form a standalone runnable monorepo simply by being placed next to each other. Their original installation and runtime relationships still apply.

When analyzing the system:

1. Read the actual source code rather than only README files.
2. Trace Marley Frontend actions into Marley/Frappe APIs and DocTypes.
3. Trace Marley billing behavior into ERPNext where applicable.
4. Distinguish domain concepts, backend invariants, frontend UX patterns, and framework-specific implementation details.
5. Treat `UPSTREAM_VERSIONS.md` as the record of the exact imported commits.
6. Do not assume a feature belongs in another project merely because it exists upstream; evaluate suitability first.

## Intended use

The primary purpose of this repository is deep AI-assisted inspection, comparison, architecture study, and selective adaptation of mature healthcare workflows into another system.
