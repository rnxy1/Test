# Marley Runtime Dependency Map

This repository now vendors the complete source trees needed to inspect the Marley stack in one place.

## Vendored source trees

### Frappe Framework
- Repository: https://github.com/frappe/frappe.git
- Branch: `version-16`
- Destination: `vendor/frappe/`

### ERPNext
- Repository: https://github.com/frappe/erpnext.git
- Branch: `version-16`
- Destination: `vendor/erpnext/`

### Marley Health
- Repository: https://github.com/earthians/marley.git
- Branch: `version-16`
- Destination: `vendor/marley/`

### Marley Frontend
- Repository: https://github.com/earthians/marley_frontend.git
- Branch: `develop`
- Destination: `vendor/marley_frontend/`

## Relationship

Frappe Framework is the underlying application framework.
ERPNext runs on Frappe and provides ERP/accounting/business functionality.
Marley Health runs on Frappe and integrates with ERPNext for healthcare and billing workflows.
Marley Frontend provides newer UI/workflows on top of the Frappe/ERPNext/Marley runtime.

All four codebases are included for analysis. The copied layout is for source inspection and does not itself replace the normal Frappe installation process.
