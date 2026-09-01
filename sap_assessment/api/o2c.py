import frappe




def sales_invoice_submitted(doc, method=None):
    frappe.logger("o2c").info(
        f"Sales Invoice {doc.name} submitted for customer {doc.customer}"
    )

    frappe.publish_realtime(
        "o2c_sales_invoice_submitted",
        {
            "doctype": "Sales Invoice",
            "name": doc.name,
            "customer": doc.customer,
            "grand_total": doc.grand_total
        }
    )
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

@frappe.whitelist()
def o2c_sales_order_report():

    SalesOrder = frappe.qb.DocType("Sales Order")
    Customer = frappe.qb.DocType("Customer")

    # Query Builder
    query = (
    frappe.qb.from_(SalesOrder)
    .join(Customer)
    .on(SalesOrder.customer == Customer.name)
    .select(
        SalesOrder.name,
        SalesOrder.customer,
        Customer.customer_name,
        SalesOrder.order_date,
        SalesOrder.grand_total,
        SalesOrder.api_processed
    )
    .where(
    (SalesOrder.docstatus == 1)
    & (SalesOrder.name == "SO-00002")
)
    
    .limit(10)
)

    results = query.run(as_dict=True)

    if not results:
        return []

    # Document API
    first_order = frappe.get_doc(
        "Sales Order",
        results[0]["name"]
    )

    first_order.api_processed = 1
    first_order.save()

    # Database API
    for row in results:
        frappe.db.set_value(
            "Sales Order",
            row["name"],
            "api_processed",
            1
        )

    return results
@frappe.whitelist()
def o2c_recent_sales_orders():

    sales_orders = frappe.get_list(
        "Sales Order",
        fields=[
            "name",
            "owner",
            "customer",
            "customer_name",
            "order_date",
            "grand_total"
        ],
        order_by="creation desc",
        limit_page_length=5
    )

    for order in sales_orders:
        owner_email = frappe.db.get_value(
            "User",
            order.get("owner"),
            "email"
        )

        order["owner_email"] = owner_email

    timestamp = frappe.utils.now()

    return {
        "timestamp": timestamp,
        "sales_orders": sales_orders
    }