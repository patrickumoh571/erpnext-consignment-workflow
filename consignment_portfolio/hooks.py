app_name = "consignment_portfolio"
app_title = "Consignment Portfolio"
app_publisher = "Patrick Umoh"
app_description = "ERPNext consignment workflow portfolio app"
app_email = "patrickumoh571@gmail.com"
app_license = "MIT"

required_apps = ["erpnext"]

after_install = "consignment_portfolio.install.after_install"
after_migrate = "consignment_portfolio.install.after_migrate"

doc_events = {
    "Stock Entry": {
        "on_submit": "consignment_portfolio.events.stock_entry.on_submit"
    }
}

doctype_js = {
    "Stock Entry": "public/js/stock_entry.js"
}
