# ERPNext Consignment Workflow

A sanitized, installable Frappe / ERPNext custom app demonstrating how a consignment stock issue can be linked to a customer-facing Sales Order while preserving auditability between inventory and commercial documents.

> **Portfolio project:** Based on a real ERPNext business requirement. Client names, credentials, domains, production data, commercial values, and proprietary implementation details have been removed or generalized.

## What This Demonstrates

- Python business logic
- Frappe document events
- ERPNext document creation
- version-controlled custom-field installation
- DocType JavaScript
- whitelisted server methods
- duplicate / idempotency protection
- linked-document audit trail
- permission-aware recovery action
- bench installation and migration
- Git / GitHub-ready app structure

## Business Flow

```text
Material Request (optional)
        |
        v
Stock Entry - Material Transfer
        |
        | custom_issue_to_outlet = 1
        | custom_outlet_customer = Customer
        v
Outlet Warehouse
        |
        | on_submit
        v
Consignment Service
        |
        +---- idempotency check
        |
        v
Sales Order
        |
        | custom_source_stock_entry
        v
Sales Invoice / Return / Exposure Reporting
```

## Compatibility Target

Written for **Frappe / ERPNext v14 and v15 style APIs**. Test on the exact target version before production use.

## Install

```bash
cd ~/frappe-bench
bench get-app https://github.com/YOUR-GITHUB-USERNAME/erpnext-consignment-workflow.git
bench --site yoursite.example.com install-app consignment_portfolio
bench --site yoursite.example.com migrate
bench build --app consignment_portfolio
bench restart
```

If the Bench version expects the app folder to match the Python package name:

```bash
cd ~/frappe-bench/apps
git clone https://github.com/YOUR-GITHUB-USERNAME/erpnext-consignment-workflow.git consignment_portfolio

cd ~/frappe-bench
./env/bin/pip install -e apps/consignment_portfolio
bench --site yoursite.example.com install-app consignment_portfolio
bench --site yoursite.example.com migrate
bench build --app consignment_portfolio
bench restart
```

## Verify

```bash
bench --site yoursite.example.com execute consignment_portfolio.install.get_installation_status
```

## Custom Fields Installed

### Stock Entry
- `custom_issue_to_outlet`
- `custom_outlet_customer`
- `custom_source_material_request`
- `custom_auto_created_sales_order`

### Sales Order
- `custom_source_stock_entry`
- `custom_order_type`
- `custom_issued_qty`
- `custom_sold_qty`

### Material Request
- `custom_auto_created_stock_entry`

## Optional Auto-Submit

Generated Sales Orders remain in Draft by default.

Enable automatic submission:

```bash
bench --site yoursite.example.com set-config consignment_auto_submit_sales_order 1
bench --site yoursite.example.com clear-cache
```

## Author

**Patrick Umoh**  
ERPNext / Frappe Developer  
Python | REST APIs | ERP Integrations | Business Process Automation
