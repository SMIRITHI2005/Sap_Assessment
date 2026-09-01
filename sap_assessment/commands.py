import click
import frappe


@click.command()
def pending_deliveries():
    """Show submitted Sales Orders waiting for delivery."""

    frappe.init(site="assessment.local")
    frappe.connect()

    try:
        orders = frappe.get_all(
            "Sales Order",
            filters={
                "docstatus": 1
            },
            fields=["name", "customer"]
        )

        click.echo("")
        click.echo("===== SALES ORDERS PENDING DELIVERY =====")

        for order in orders:
            delivery_exists = frappe.db.exists(
                "Delivery Note",
                {
                    "sales_order": order.name,
                    "docstatus": 1
                }
            )

            if not delivery_exists:
                click.echo(
                    f"{order.name} | Customer: {order.customer}"
                )

        click.echo("==========================================")

    finally:
        frappe.destroy()


commands = [
    pending_deliveries
]

import click
import frappe


@click.command("o2c-status")
@click.option("--site", default="assessment.local", help="Frappe site to check")
def o2c_status(site):
    """Show a quick O2C document summary."""

    frappe.init(site=site)
    frappe.connect()

    try:
        sales_orders = frappe.db.count("Sales Order")
        delivery_notes = frappe.db.count("Delivery Note")
        sales_invoices = frappe.db.count("Sales Invoice")
        payment_entries = frappe.db.count("Payment Entry")

        click.echo("=== O2C STATUS ===")
        click.echo(f"Site: {site}")
        click.echo(f"Sales Orders: {sales_orders}")
        click.echo(f"Delivery Notes: {delivery_notes}")
        click.echo(f"Sales Invoices: {sales_invoices}")
        click.echo(f"Payment Entries: {payment_entries}")

    finally:
        frappe.destroy()


commands = [
    o2c_status
]
