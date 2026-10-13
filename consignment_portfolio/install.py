"""Install and migration helpers."""

import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields

from consignment_portfolio.custom_fields import get_custom_fields


def after_install():
    install_custom_fields()


def after_migrate():
    install_custom_fields()


def install_custom_fields():
    """Idempotently create/update fields required by the workflow."""
    create_custom_fields(get_custom_fields(), update=True)
    frappe.clear_cache()


def get_installation_status():
    expected = get_custom_fields()
    result = {}

    for doctype, fields in expected.items():
        result[doctype] = {}
        for field in fields:
            fieldname = field["fieldname"]
            result[doctype][fieldname] = bool(
                frappe.db.exists(
                    "Custom Field",
                    {"dt": doctype, "fieldname": fieldname},
                )
            )

    return result
