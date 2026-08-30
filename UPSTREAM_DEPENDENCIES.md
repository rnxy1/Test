# Marley Runtime Dependency Map

This repository vendors the two Marley codebases that are most useful for AI-assisted analysis and UI/workflow adaptation.

## Vendored

### Marley Health
- Repository: https://github.com/earthians/marley.git
- Branch: `version-16`
- Destination: `vendor/marley/`

### Marley Frontend
- Repository: https://github.com/earthians/marley_frontend.git
- Branch: `develop`
- Destination: `vendor/marley_frontend/`

## Runtime dependencies (referenced, not vendored)

### Frappe Framework
- Repository: https://github.com/frappe/frappe.git
- Branch: `version-16`

### ERPNext
- Repository: https://github.com/frappe/erpnext.git
- Branch: `version-16`

Marley Health uses Frappe and ERPNext as runtime dependencies. Marley Frontend also assumes the Frappe/ERPNext/Healthcare runtime and Frappe APIs.

For Royal Clinic work, do not blindly copy these runtime dependencies into the Firebase application. Use them to understand upstream behavior and reimplement only the selected concepts in the Royal Clinic architecture.
