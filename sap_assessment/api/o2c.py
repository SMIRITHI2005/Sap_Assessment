import frappe


@frappe.whitelist()
def generate_delivery_note(sales_order_name):

    sales_order = frappe.get_doc(
        "Sales Order",
        sales_order_name
    )

    # Only submitted Sales Orders can generate Delivery Notes
    if sales_order.docstatus != 1:
        frappe.throw("Sales Order must be submitted first.")

    delivery_note = frappe.new_doc("Delivery Note")

    # Header information
    delivery_note.customer = sales_order.customer
    delivery_note.customer_name = sales_order.customer_name
    delivery_note.sales_order = sales_order.name
    delivery_note.order_date = sales_order.order_date
    delivery_note.delivery_date = frappe.utils.today()

    # Items
    for row in sales_order.items:

        delivery_item = delivery_note.append("items", {})

        delivery_item.item = row.item
        delivery_item.item_name = row.item_name
        delivery_item.quantity = row.quantity
        delivery_item.rate = row.rate
        delivery_item.amount = row.amount

    # Totals
    delivery_note.total_quantity = sales_order.total_quantity
    delivery_note.grand_total = sales_order.grand_total

    delivery_note.insert()

    return delivery_note.name