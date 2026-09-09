import frappe


def execute(filters=None):
    filters = filters or {}

    columns = [
        {
            "label": "Invoice ID",
            "fieldname": "invoice_id",
            "fieldtype": "Link",
            "options": "Sales Invoice",
            "width": 150
        },
        {
            "label": "Customer",
            "fieldname": "customer",
            "fieldtype": "Link",
            "options": "Customer",
            "width": 180
        },
        {
            "label": "Invoice Date",
            "fieldname": "invoice_date",
            "fieldtype": "Date",
            "width": 120
        },
        {
            "label": "Invoice Amount",
            "fieldname": "invoice_amount",
            "fieldtype": "Currency",
            "width": 140
        },
        {
            "label": "Status",
            "fieldname": "status",
            "fieldtype": "Data",
            "width": 120
        }
    ]

    conditions = {}

    if filters.get("from_date") and filters.get("to_date"):
        conditions["invoice_date"] = [
            "between",
            [filters["from_date"], filters["to_date"]]
        ]

    elif filters.get("from_date"):
        conditions["invoice_date"] = [
            ">=",
            filters["from_date"]
        ]

    elif filters.get("to_date"):
        conditions["invoice_date"] = [
            "<=",
            filters["to_date"]
        ]

    if filters.get("customer"):
        conditions["customer"] = filters["customer"]

    if filters.get("status"):
        conditions["status"] = filters["status"]

    data = frappe.get_all(
        "Sales Invoice",
        filters=conditions,
        fields=[
            "name as invoice_id",
            "customer",
            "invoice_date",
            "grand_total as invoice_amount",
            "status"
        ],
        order_by="invoice_date desc",
        limit_page_length=50
    )

    return columns, data