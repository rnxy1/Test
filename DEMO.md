# Run the full Marley stack

This repository includes a GitHub Codespaces configuration that builds and runs these projects together:

- Frappe Framework — `version-16`
- ERPNext — `version-16`
- Marley Health — `version-16`
- Marley Frontend — `develop`

## The only steps you need

1. Open this repository on GitHub.
2. Tap **Code** → **Codespaces** → **Create codespace on main**.
3. Let the Codespace finish its automatic setup.
4. Open the forwarded port **8080** when GitHub shows it.

Login:

- User: `Administrator`
- Password: `admin`

Useful paths:

- `/app` — Frappe / ERPNext / Marley Desk
- `/healthcare` — the modern Marley Frontend

## Notes

This is a disposable test environment, not a production deployment. It uses the standard demo database password and Administrator password shown above.

The first build is heavier because it creates one image containing all four applications. Later starts in the same Codespace reuse that image and the existing Docker volumes.
