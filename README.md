# Marley Frontend — Standalone Demo

This repository contains only the Marley Frontend UI copied into the repository root for direct import into Google AI Studio.

Run:

```bash
npm install
npm run dev
```

The app starts on port 8080 and uses a local demo/mock data layer so the Marley UI can be explored without Frappe, ERPNext, or a Marley backend server.

Original project: earthians/marley_frontend (develop branch).

The UI source remains under `src/` and is otherwise kept as close to the Marley Frontend source as practical; standalone preview compatibility is isolated to the local demo layer and Vite startup configuration.
