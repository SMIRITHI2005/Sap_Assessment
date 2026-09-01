import frappe
from frappe.utils import getdate, today


def daily_maintenance():
    """Daily O2C background maintenance job."""

    current_date = getdate(today())

    overdue_invoices = frappe.get_all(
        "Sales Invoice",
        filters={
            "docstatus": 1,
            "status": "Unpaid",
            "due_date": ["<", current_date]
        },
        fields=[
            "name",
            "customer",
            "due_date",
            "outstanding_amount"
        ]
    )

    if overdue_invoices:
        message = (
            f"O2C Daily Maintenance: "
            f"{len(overdue_invoices)} overdue Sales Invoice(s) found."
        )

        frappe.log_error(
            title="O2C Daily Maintenance",
            message=message
        )
    else:
        frappe.log_error(
            title="O2C Daily Maintenance",
            message="O2C Daily Maintenance completed. No overdue invoices found."
        )