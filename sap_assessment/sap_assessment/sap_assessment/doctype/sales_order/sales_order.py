import frappe
from frappe.model.document import Document


class SalesOrder(Document):

    def before_save(self):
        if not self.customer:
            frappe.throw("Customer is required")

        if not self.order_date:
            self.order_date = frappe.utils.today()
