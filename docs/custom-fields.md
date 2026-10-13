# Custom Fields

The app installs custom fields using Frappe's standard `create_custom_fields()` helper.

The installer runs after both installation and migration, which keeps the setup repeatable and version-controlled.

| DocType | Field | Type |
|---|---|---|
| Stock Entry | `custom_issue_to_outlet` | Check |
| Stock Entry | `custom_outlet_customer` | Link / Customer |
| Stock Entry | `custom_source_material_request` | Link / Material Request |
| Stock Entry | `custom_auto_created_sales_order` | Link / Sales Order |
| Sales Order | `custom_source_stock_entry` | Link / Stock Entry |
| Sales Order | `custom_order_type` | Select |
| Sales Order | `custom_issued_qty` | Float |
| Sales Order | `custom_sold_qty` | Float |
| Material Request | `custom_auto_created_stock_entry` | Link / Stock Entry |

## Why Code Instead of Manual Customization?

- repeatable installation;
- Git history;
- consistent staging and production;
- less configuration drift;
- easier peer review.
