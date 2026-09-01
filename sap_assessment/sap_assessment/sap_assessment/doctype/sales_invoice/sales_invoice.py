import frappe
from frappe.model.document import Document


class SalesInvoice(Document):

    @property
    def payment_completion(self):
        if self.grand_total and self.grand_total > 0:
            return (self.paid_amount / self.grand_total) * 100

        return 0