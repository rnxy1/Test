# Marley + Marley Frontend — AI Studio Demo

This repository is intentionally focused on the two Marley projects needed for frontend exploration:

- `marley/` — Marley Health source, branch `version-16`
- `marley_frontend/` — modern Marley Frontend source, branch `develop`

Frappe Framework and ERPNext source trees are intentionally not included so Google AI Studio can focus on Marley and its UI.

## Try it in Google AI Studio

Import:

`rnxy1/Test`

Then run from the repository root:

```bash
npm install
npm run dev
```

The launcher starts the Marley Vue/Vite frontend on port `8080` with:

`VITE_AI_STUDIO_PREVIEW=1`

Open the preview root. In demo mode `/` redirects to the populated Appointment Desk.

## Full fake-data demo mode

The repository now contains a local mock Frappe/Marley API layer at:

`marley_frontend/frontend/src/demo/mockApi.js`

When `VITE_AI_STUDIO_PREVIEW=1` is enabled, Marley uses that local layer instead of a real Frappe server. The demo includes populated examples for:

- Appointment Desk with multiple appointment statuses
- patients and practitioners
- departments and appointment types
- booking slots and appointment creation
- patient kiosk and demo OTP workflow
- patient registration/profile data
- queue selection and token displays
- ward, room and bed management
- vacant, occupied, cleaning and maintenance room states
- vitals, rescheduling, payment modes, services and prescription examples
- common actions such as changing status, booking, scheduling admission and admitting a patient

Several demo actions mutate in-memory state so the UI can be clicked and explored rather than functioning as a screenshot-only mock.

Demo data is synthetic and is not connected to any real patient or backend. In-memory changes reset when the preview environment restarts.

## Demo routes

In AI Studio preview mode the useful routes are:

- `/` — redirects to Appointment Desk
- `/waitlist` — Appointment Desk
- `/kiosk` — patient self-service kiosk
- `/Register` — patient registration
- `/Appointment` — appointment booking
- `/QueueSelection` — select queue displays
- `/bed_management` — bed/ward management

The actual installed Marley application still uses `/healthcare/...`; the root-based routes are only for the frontend-only AI Studio preview.

## Isolation from real Marley runtime

The fake backend and authentication bypass activate only when `VITE_AI_STUDIO_PREVIEW=1` is present. Without that flag, the code continues to use the normal Frappe resource fetcher, `/healthcare` router base, authentication, backend APIs and realtime socket behavior.

This makes the demo useful for UI/UX evaluation without converting Marley itself into a standalone application.

## Upstream projects

- Marley Health: https://github.com/earthians/marley/tree/version-16
- Marley Frontend: https://github.com/earthians/marley_frontend

See `UPSTREAM_VERSIONS.md` for the upstream commits used as the source baseline.
