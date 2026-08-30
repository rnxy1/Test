# Marley + Marley Frontend — AI Studio Bundle

This repository is intentionally reduced to the two Marley projects needed for frontend inspection:

- `marley/` — Marley Health source, branch `version-16`
- `marley_frontend/` — modern Marley Frontend source, branch `develop`

Frappe Framework and ERPNext source trees are intentionally **not included** so the repository stays smaller and easier for Google AI Studio to import and analyze.

## Use in Google AI Studio

Import this GitHub repository directly:

`rnxy1/Test`

The repository root contains an AI Studio launcher. Use the normal Node workflow:

```bash
npm install
npm run dev
```

The root launcher starts `marley_frontend/frontend` on port `8080` with `VITE_AI_STUDIO_PREVIEW=1`.

## AI Studio preview mode

The upstream frontend normally waits for a live Frappe API before mounting and redirects unauthenticated users to Frappe login. This bundle adds a small environment-gated preview compatibility layer so AI Studio can display the frontend without a Frappe bench:

- mounts the Vue app without waiting for Frappe boot data
- bypasses the Frappe login redirect only while preview mode is enabled
- provides a local demo user identity
- disables the Frappe development proxy requirement
- avoids opening the realtime socket when no backend exists

These changes are active only when `VITE_AI_STUDIO_PREVIEW=1`; normal Marley runtime behavior remains intact otherwise.

## Frontend routes

The primary source is:

`marley_frontend/frontend/`

Useful routes include:

- `/healthcare/`
- `/healthcare/waitlist`
- `/healthcare/kiosk`
- `/healthcare/QueueSelection`
- `/healthcare/bed_management`

## What remains backend-dependent

The interface can boot for frontend exploration, but real patients, appointments, payments, queues, beds, settings and other healthcare data still come from Frappe/Marley APIs. Those actions may show empty/error states in AI Studio unless a mock backend is added.

## Upstream projects

- Marley Health: https://github.com/earthians/marley/tree/version-16
- Marley Frontend: https://github.com/earthians/marley_frontend

See `UPSTREAM_VERSIONS.md` for the upstream commits used as the source baseline.
