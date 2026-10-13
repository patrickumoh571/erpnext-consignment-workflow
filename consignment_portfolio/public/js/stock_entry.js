frappe.ui.form.on("Stock Entry", {
    refresh(frm) {
        const isSubmitted = frm.doc.docstatus === 1;
        const isOutletIssue = Boolean(frm.doc.custom_issue_to_outlet);
        const linkedSalesOrder = frm.doc.custom_auto_created_sales_order;

        if (isSubmitted && isOutletIssue && !linkedSalesOrder) {
            frm.add_custom_button(__("Create / Recover Sales Order"), async () => {
                const response = await frappe.call({
                    method: "consignment_portfolio.api.recover_sales_order",
                    args: {
                        stock_entry_name: frm.doc.name
                    },
                    freeze: true,
                    freeze_message: __("Checking consignment Sales Order...")
                });

                if (response.message) {
                    frappe.show_alert({
                        message: __("Sales Order {0} is linked", [response.message]),
                        indicator: "green"
                    });

                    await frm.reload_doc();
                }
            }, __("Consignment"));
        }

        if (linkedSalesOrder) {
            frm.add_custom_button(__("Open Sales Order"), () => {
                frappe.set_route("Form", "Sales Order", linkedSalesOrder);
            }, __("Consignment"));
        }
    }
});
