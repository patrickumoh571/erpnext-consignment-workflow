from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SERVICE = ROOT / "consignment_portfolio" / "services" / "consignment.py"


def test_service_contains_idempotency_guard():
    source = SERVICE.read_text(encoding="utf-8")
    assert "custom_auto_created_sales_order" in source
    assert "custom_source_stock_entry" in source


def test_service_requires_submitted_stock_entry():
    source = SERVICE.read_text(encoding="utf-8")
    assert "stock_entry.docstatus != 1" in source


def test_service_does_not_use_valuation_rate_as_sales_price():
    source = SERVICE.read_text(encoding="utf-8")
    assert "valuation_rate" not in source
    assert "Item Price" in source
