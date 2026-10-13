"""Whitelisted API methods."""

import frappe
from frappe import _

from consignment_portfolio.services.consignment import ensure_outlet_sales_order


@frappe.whitelist()
def recover_sales_order(stock_entry_name: str):
    if not stock_entry_name:
        frappe.throw(_("Stock Entry name is required."))

    stock_entry = frappe.get_doc("Stock Entry", stock_entry_name)

    if not frappe.has_permission("Stock Entry", ptype="write", doc=stock_entry):
        frappe.throw(_("You do not have permission to recover this transaction."))

    return ensure_outlet_sales_order(stock_entry)


@frappe.whitelist()
def get_outlet_exposure(outlet_customer: str):
    if not outlet_customer:
        frappe.throw(_("Outlet Customer is required."))

    if not frappe.has_permission("Sales Order", ptype="read"):
        frappe.throw(_("You do not have permission to view Sales Orders."))

    issued = frappe.db.sql(
        """
        SELECT COALESCE(SUM(soi.qty), 0)
        FROM `tabSales Order` so
        INNER JOIN `tabSales Order Item` soi ON soi.parent = so.name
        WHERE so.docstatus = 1
          AND so.customer = %s
          AND so.custom_order_type = 'Consignment'
        """,
        (outlet_customer,),
    )[0][0] or 0

    sold = frappe.db.sql(
        """
        SELECT COALESCE(SUM(sii.qty), 0)
        FROM `tabSales Invoice` si
        INNER JOIN `tabSales Invoice Item` sii ON sii.parent = si.name
        INNER JOIN `tabSales Order` so ON so.name = sii.sales_order
        WHERE si.docstatus = 1
          AND so.docstatus = 1
          AND so.customer = %s
          AND so.custom_order_type = 'Consignment'
        """,
        (outlet_customer,),
    )[0][0] or 0

    return {
        "outlet_customer": outlet_customer,
        "issued_qty": issued,
        "sold_qty": sold,
        "remaining_qty": issued - sold,
    }
