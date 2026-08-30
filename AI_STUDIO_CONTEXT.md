# Google AI Studio Context

## Purpose

This repository is a deliberately small source bundle for exploring **Marley Health** and especially **Marley Frontend** in Google AI Studio.

Do not rebuild Frappe or ERPNext inside this repository unless explicitly requested. Their source was removed intentionally to keep AI Studio context focused.

## Repository layout

- `marley/` — Marley Health backend/domain app, upstream `earthians/marley`, branch `version-16`.
- `marley_frontend/` — modern Vue 3 frontend, upstream `earthians/marley_frontend`, branch `develop`.
- `package.json` — root launcher for AI Studio preview.

## Primary frontend

Treat this as the main application when the user asks to preview, analyze, redesign, or experiment with the UI:

`marley_frontend/frontend/`

Technology:

- Vue 3
- Vite
- Frappe UI
- Tailwind CSS
- Vue Router
- Socket.IO client

The original frontend development command is run from `marley_frontend/frontend` with `yarn dev`. The root package delegates to that app so AI Studio can start from the repository root with `npm run dev`.

## Runtime reality

Marley Frontend is not truly standalone. Its Vite configuration enables the Frappe proxy and many views call Frappe/Marley APIs. Therefore:

1. Frontend source, layout, components, routes, styles, forms, navigation, and UX can be inspected and modified here.
2. Backend-dependent data will not be real in a frontend-only AI Studio preview.
3. Do not delete backend API calls merely to make a static preview unless the user asks for a mock/demo mode.
4. If creating a mock/demo mode, keep it isolated and reversible; do not replace production API integrations.

## Key frontend routes

- `/healthcare/` — home/redirect to Waitlist
- `/healthcare/waitlist` — appointment desk
- `/healthcare/kiosk` — patient self-service kiosk
- `/healthcare/QueueSelection` — queue selection
- `/healthcare/bed_management` — bed management

## Goal

When imported into AI Studio, prioritize letting the user understand and experiment with the Marley Frontend UI without flooding the model context with the entire Frappe and ERPNext frameworks.
