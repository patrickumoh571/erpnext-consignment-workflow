"""Business services for the consignment workflow."""

import frappe
from frappe import _
from frappe.utils import nowdate


def ensure_outlet_sales_order(stock_entry):
    """Create or recover one Sales Order for a qualifying Stock Entry."""

    if stock_entry.purpose != "Material Transfer":
        return None

    if not stock_entry.get("custom_issue_to_outlet"):
        return None

    if stock_entry.docstatus != 1:
        frappe.throw(_("The Stock Entry must be submitted before creating the outlet Sales Order."))

    linked = stock_entry.get("custom_auto_created_sales_order")
    if linked and frappe.db.exists("Sales Order", linked):
        return linked

    outlet_customer = stock_entry.get("custom_outlet_customer")
    if not outlet_customer:
        frappe.throw(_("Outlet Customer is required for an outlet issue."))

    existing = frappe.db.get_value(
        "Sales Order",
        {
            "custom_source_stock_entry": stock_entry.name,
            "docstatus": ["<", 2],
        },
        "name",
    )

    if existing:
        stock_entry.db_set(
            "custom_auto_created_sales_order",
            existing,
            update_modified=False,
        )
        _link_source_material_request(stock_entry)
        return existing

    sales_order = _build_sales_order(stock_entry, outlet_customer)
    sales_order.insert()

    if _auto_submit_enabled():
        sales_order.submit()

    stock_entry.db_set(
        "custom_auto_created_sales_order",
        sales_order.name,
        update_modified=False,
    )

    _link_source_material_request(stock_entry)

    frappe.logger("consignment_portfolio").info(
        "Linked Stock Entry %s to Sales Order %s",
        stock_entry.name,
        sales_order.name,
    )

    return sales_order.name


def _build_sales_order(stock_entry, outlet_customer):
    price_list = _get_selling_price_list(outlet_customer)

    items = []
    total_issued_qty = 0.0

    for row in stock_entry.items:
        qty = float(row.qty or 0)
        if qty <= 0:
            continue

        rate = _get_selling_rate(row.item_code, price_list)
        target_warehouse = row.get("t_warehouse") or stock_entry.get("to_warehouse")

        item = {
            "item_code": row.item_code,
            "qty": qty,
            "uom": row.uom,
            "delivery_date": nowdate(),
            "rate": rate,
        }

        if target_warehouse:
            item["warehouse"] = target_warehouse

        items.append(item)
        total_issued_qty += qty

    if not items:
        frappe.throw(
            _("No transferable item quantity was found on Stock Entry {0}.").format(
                stock_entry.name
            )
        )

    return frappe.get_doc(
        {
            "doctype": "Sales Order",
            "company": stock_entry.company,
            "customer": outlet_customer,
            "transaction_date": nowdate(),
            "delivery_date": nowdate(),
            "selling_price_list": price_list,
            "custom_source_stock_entry": stock_entry.name,
            "custom_order_type": "Consignment",
            "custom_issued_qty": total_issued_qty,
            "custom_sold_qty": 0,
            "items": items,
        }
    )


def _get_selling_price_list(customer):
    price_list = frappe.get_cached_value(
        "Customer",
        customer,
        "default_price_list",
    )

    if not price_list:
        price_list = frappe.db.get_single_value(
            "Selling Settings",
            "selling_price_list",
        )

    if not price_list:
        frappe.throw(
            _(
                "No selling Price List is configured. Set a default Price List "
                "for the outlet customer or in Selling Settings."
            )
        )

    return price_list


def _get_selling_rate(item_code, price_list):
    rate = frappe.db.get_value(
        "Item Price",
        {
            "item_code": item_code,
            "price_list": price_list,
            "selling": 1,
        },
        "price_list_rate",
    )

    if rate is None:
        frappe.throw(
            _(
                "No selling Item Price was found for Item {0} in Price List {1}."
            ).format(item_code, price_list)
        )

    return rate


def _link_source_material_request(stock_entry):
    material_requests = {
        row.get("material_request")
        for row in stock_entry.items
        if row.get("material_request")
    }

    if len(material_requests) != 1:
        return

    material_request = next(iter(material_requests))

    stock_entry.db_set(
        "custom_source_material_request",
        material_request,
        update_modified=False,
    )

    if frappe.db.exists("Material Request", material_request):
        current = frappe.db.get_value(
            "Material Request",
            material_request,
            "custom_auto_created_stock_entry",
        )
        if not current:
            frappe.db.set_value(
                "Material Request",
                material_request,
                "custom_auto_created_stock_entry",
                stock_entry.name,
                update_modified=False,
            )


def _auto_submit_enabled():
    value = frappe.conf.get("consignment_auto_submit_sales_order", 0)
    return str(value).lower() in {"1", "true", "yes", "on"}
