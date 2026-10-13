# Installation Guide

## Prerequisites
- Existing Frappe Bench
- ERPNext installed on target site
- Git and bench access
- Supported Python version for the target Frappe release

## Install
```bash
cd ~/frappe-bench
bench get-app https://github.com/YOUR-GITHUB-USERNAME/erpnext-consignment-workflow.git
bench --site yoursite.example.com install-app consignment_portfolio
bench --site yoursite.example.com migrate
bench build --app consignment_portfolio
bench restart
```

## Verify
```bash
bench --site yoursite.example.com list-apps
bench --site yoursite.example.com execute consignment_portfolio.install.get_installation_status
```

## Re-run Field Installer
```bash
bench --site yoursite.example.com execute consignment_portfolio.install.install_custom_fields
```

## Auto-submit Setting
```bash
bench --site yoursite.example.com set-config consignment_auto_submit_sales_order 1
bench --site yoursite.example.com clear-cache
```
