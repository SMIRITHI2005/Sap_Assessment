import frappe


def sales_invoice_submitted(doc, method):
    frappe.msgprint(
        f"O2C Hook executed for Sales Invoice {doc.name}"
    )
