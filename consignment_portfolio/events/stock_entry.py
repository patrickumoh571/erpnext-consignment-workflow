"""Stock Entry document event handlers."""

from consignment_portfolio.services.consignment import ensure_outlet_sales_order


def on_submit(doc, method=None):
    return ensure_outlet_sales_order(doc)
