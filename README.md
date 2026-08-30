# Marley + Marley Frontend — AI Studio Bundle

This repository is intentionally reduced to only the two Marley projects needed for frontend inspection:

- `marley/` — Marley Health source, branch `version-16`
- `marley_frontend/` — modern Marley Frontend source, branch `develop`

Frappe Framework and ERPNext source trees are intentionally **not included** so the repository stays smaller and easier for Google AI Studio to import and analyze.

## Use in Google AI Studio

Import this GitHub repository directly:

`rnxy1/Test`

The repository root contains a small launcher `package.json`. AI Studio can use the normal Node workflow:

```bash
npm install
npm run dev
```

That delegates directly to `marley_frontend/frontend`, the Vue 3 + Vite application.

## What to inspect

The frontend source is under:

`marley_frontend/frontend/`

Useful routes defined by Marley Frontend include:

- `/healthcare/`
- `/healthcare/waitlist`
- `/healthcare/kiosk`
- `/healthcare/QueueSelection`
- `/healthcare/bed_management`

## Important limitation

Marley Frontend was designed to run on top of Frappe + ERPNext + Marley Health and proxies API calls to that backend. This repository is optimized for **frontend preview, code inspection, and AI Studio experimentation**, not a complete healthcare server.

Screens or actions that require live patients, appointments, authentication, payments, queues, beds, or other server data may not function without a Frappe backend.

## Upstream projects

- Marley Health: https://github.com/earthians/marley/tree/version-16
- Marley Frontend: https://github.com/earthians/marley_frontend

See `UPSTREAM_VERSIONS.md` for the exact copied commits.
