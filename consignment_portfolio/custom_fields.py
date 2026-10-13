"""Version-controlled custom fields required by the app."""


def get_custom_fields():
    return {
        "Stock Entry": [
            {
                "fieldname": "custom_consignment_section",
                "label": "Consignment / Outlet Issue",
                "fieldtype": "Section Break",
                "insert_after": "purpose",
                "collapsible": 1,
            },
            {
                "fieldname": "custom_issue_to_outlet",
                "label": "Issue to Outlet",
                "fieldtype": "Check",
                "insert_after": "custom_consignment_section",
                "default": "0",
            },
            {
                "fieldname": "custom_outlet_customer",
                "label": "Outlet Customer",
                "fieldtype": "Link",
                "options": "Customer",
                "insert_after": "custom_issue_to_outlet",
                "depends_on": "eval:doc.custom_issue_to_outlet==1",
                "mandatory_depends_on": "eval:doc.custom_issue_to_outlet==1",
            },
            {
                "fieldname": "custom_source_material_request",
                "label": "Source Material Request",
                "fieldtype": "Link",
                "options": "Material Request",
                "insert_after": "custom_outlet_customer",
                "read_only": 1,
                "no_copy": 1,
            },
            {
                "fieldname": "custom_auto_created_sales_order",
                "label": "Auto-Created Sales Order",
                "fieldtype": "Link",
                "options": "Sales Order",
                "insert_after": "custom_source_material_request",
                "read_only": 1,
                "no_copy": 1,
            },
        ],
        "Sales Order": [
            {
                "fieldname": "custom_consignment_section",
                "label": "Consignment Traceability",
                "fieldtype": "Section Break",
                "insert_after": "customer",
                "collapsible": 1,
            },
            {
                "fieldname": "custom_source_stock_entry",
                "label": "Source Stock Entry",
                "fieldtype": "Link",
                "options": "Stock Entry",
                "insert_after": "custom_consignment_section",
                "read_only": 1,
                "no_copy": 1,
            },
            {
                "fieldname": "custom_order_type",
                "label": "Order Type",
                "fieldtype": "Select",
                "options": "Standard\nConsignment",
                "insert_after": "custom_source_stock_entry",
                "default": "Standard",
            },
            {
                "fieldname": "custom_issued_qty",
                "label": "Issued Quantity",
                "fieldtype": "Float",
                "insert_after": "custom_order_type",
                "read_only": 1,
                "no_copy": 1,
            },
            {
                "fieldname": "custom_sold_qty",
                "label": "Sold Quantity",
                "fieldtype": "Float",
                "insert_after": "custom_issued_qty",
                "read_only": 1,
                "no_copy": 1,
            },
        ],
        "Material Request": [
            {
                "fieldname": "custom_consignment_section",
                "label": "Consignment Traceability",
                "fieldtype": "Section Break",
                "insert_after": "material_request_type",
                "collapsible": 1,
            },
            {
                "fieldname": "custom_auto_created_stock_entry",
                "label": "Auto-Created Stock Entry",
                "fieldtype": "Link",
                "options": "Stock Entry",
                "insert_after": "custom_consignment_section",
                "read_only": 1,
                "no_copy": 1,
            },
        ],
    }
