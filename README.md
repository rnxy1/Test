# Full Marley / Frappe AI Studio Source Bundle

This repository is a disposable source bundle for importing into Google AI Studio and studying the complete Marley stack in one place.

It contains:

- `vendor/frappe/` — full Frappe Framework source, branch `version-16`
- `vendor/erpnext/` — full ERPNext source, branch `version-16`
- `vendor/marley/` — full Marley Health source, branch `version-16`
- `vendor/marley_frontend/` — full modern Marley Frontend source, branch `develop`
- `UPSTREAM_VERSIONS.md` — exact upstream commit SHAs currently copied into this repository
- `AI_STUDIO_CONTEXT.md` — guidance for AI Studio when analyzing the bundle

## Try the complete stack in GitHub Codespaces

This repo now also includes a one-click Codespaces runtime for Frappe v16 + ERPNext v16 + Marley Health v16 + Marley Frontend.

Open **Code → Codespaces → Create codespace on main**. The environment automatically builds the four-app stack, creates the test site, and forwards port `8080`.

Login: `Administrator` / `admin`

- `/app` — Frappe / ERPNext / Marley Desk
- `/healthcare` — Marley Frontend

See `DEMO.md` for the short instructions.

## Important

This is not the Royal Clinic production repository.

Do not connect this repository to the Royal Clinic Firebase production project.

The four projects are copied together for source inspection and AI analysis. Their original runtime relationships still apply; placing their source trees in one repository does not by itself convert them into a standalone monorepo.

## Upstream sources

- Frappe Framework: https://github.com/frappe/frappe/tree/version-16
- ERPNext: https://github.com/frappe/erpnext/tree/version-16
- Marley Health: https://github.com/earthians/marley/tree/version-16
- Marley Frontend: https://github.com/earthians/marley_frontend

The vendoring workflow can be run again later to refresh all four source trees and records the exact upstream SHAs in `UPSTREAM_VERSIONS.md`.
