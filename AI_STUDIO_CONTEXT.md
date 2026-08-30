# Google AI Studio Context

## Purpose

This repository is a focused playground for **Marley Health** and especially the **Marley Frontend**. It is designed so Google AI Studio can run and visually explore the frontend without installing the full Frappe/ERPNext backend stack.

Do not add Frappe Framework or ERPNext source trees unless the user explicitly asks for them. They were removed intentionally to keep the project small and frontend-focused.

## Repository layout

- `marley/` — Marley Health backend/domain source, upstream `earthians/marley`, branch `version-16`
- `marley_frontend/` — modern Marley Frontend, upstream `earthians/marley_frontend`, branch `develop`
- `marley_frontend/frontend/src/demo/mockApi.js` — synthetic local API for frontend-only demo mode
- `package.json` — root launcher used by AI Studio

## Start command

From the repository root:

```bash
npm install
npm run dev
```

The root launcher sets `VITE_AI_STUDIO_PREVIEW=1` and runs the Vite frontend on port 8080.

## AI Studio demo mode

`VITE_AI_STUDIO_PREVIEW=1` is a deliberate compatibility/demo mode. In this mode:

- the Vue app mounts without Frappe boot data
- authentication is replaced with a synthetic demo administrator
- Frappe proxy and realtime socket requirements are removed
- the Vue Router base is `/` instead of `/healthcare`
- Frappe UI resources use `src/demo/mockApi.js` instead of a network backend
- synthetic data populates the major Marley screens

The mock layer covers the main frontend workflows: Appointment Desk, patients, practitioners, appointment booking, kiosk/OTP, registration, queue/token displays, vitals, services/payments and bed management. Common mutations return successful demo responses and several update in-memory demo state.

Do not replace the existing production API integrations with hardcoded data. Keep all demo behavior gated behind `VITE_AI_STUDIO_PREVIEW=1` so normal Marley runtime behavior remains available.

## Primary frontend

Treat this directory as the main application for UI/UX work:

`marley_frontend/frontend/`

Technology:

- Vue 3
- Vite
- Frappe UI
- Tailwind CSS
- Vue Router
- Socket.IO client in real runtime

## Preview routes

In AI Studio demo mode:

- `/` redirects to `/waitlist`
- `/waitlist` — Appointment Desk
- `/kiosk` — patient self-service kiosk
- `/Register` — patient registration
- `/Appointment` — appointment booking
- `/QueueSelection` — queue selection
- `/bed_management` — bed management

In a real Frappe installation, Marley Frontend continues to use `/healthcare/...`.

## Data rules

All demo patients and clinical/financial values are synthetic. Do not describe them as real records. Changes in demo mode are temporary/in-memory and may reset when the preview restarts.

## Goal

Prioritize making the original Marley Frontend easy to inspect, navigate, compare, redesign and experiment with inside AI Studio while preserving the real upstream architecture outside preview mode.
