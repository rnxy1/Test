# Marley AI Studio Source Bundle

This repository is a disposable source bundle for importing into Google AI Studio and studying/adapting Marley Health.

It is intended to contain:

- `vendor/marley/` — full Marley Health source from `earthians/marley`, branch `version-16`
- `vendor/marley_frontend/` — full modern Marley Frontend source from `earthians/marley_frontend`, branch `develop`
- `UPSTREAM_DEPENDENCIES.md` — runtime dependency map for Frappe and ERPNext

## Important

This is **not** the Royal Clinic production repository.

Do not connect this repository to the Royal Clinic Firebase production project.

The goal is to let AI Studio inspect the mature Marley healthcare workflows and modern frontend in one GitHub repository.

Marley is a Frappe/ERPNext healthcare application. Frappe and ERPNext are intentionally referenced rather than fully vendored here because they are much larger and would make AI Studio ingestion unnecessarily heavy.

## Upstream sources

- Marley Health: https://github.com/earthians/marley/tree/version-16
- Marley Frontend: https://github.com/earthians/marley_frontend
- Frappe Framework v16: https://github.com/frappe/frappe/tree/version-16
- ERPNext v16: https://github.com/frappe/erpnext/tree/version-16

The vendoring workflow records the exact upstream commit SHAs in `UPSTREAM_VERSIONS.md`.
