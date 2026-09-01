"""SELECT
    so.name,
    so.customer,
    so.order_date,
    so.grand_total
FROM `tabSales Order` so
JOIN `tabCustomer` c
    ON so.customer = c.name;
    
import frappe

SalesOrder = frappe.qb.DocType("Sales Order")
DeliveryNote = frappe.qb.DocType("Delivery Note")

query = (
    frappe.qb.from_(SalesOrder)
    .left_join(DeliveryNote)
    .on(DeliveryNote.sales_order == SalesOrder.name)
    .select(
        SalesOrder.name,
        SalesOrder.customer,
        DeliveryNote.name
    )
)

results = query.run(as_dict=True)    

SELECT
    so.name AS sales_order,
    so.customer,
    dn.name AS delivery_note,
    si.name AS sales_invoice
FROM `tabSales Order` so

LEFT JOIN `tabDelivery Note` dn
    ON dn.sales_order = so.name

LEFT JOIN `tabSales Invoice` si
    ON si.sales_order = so.name;"""