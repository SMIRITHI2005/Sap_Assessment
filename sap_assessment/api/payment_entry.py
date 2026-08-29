import frappe


def update_sales_invoice_status(doc, method):
    if not doc.reference_sales_invoice:
        return

    invoice = frappe.get_doc(
        "Sales Invoice",
        doc.reference_sales_invoice
    )

    if doc.paid_amount >= invoice.grand_total:
        invoice.status = "Paid"
        invoice.save(ignore_permissions=True)
