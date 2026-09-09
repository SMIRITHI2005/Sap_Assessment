import frappe
from frappe.model.document import Document


class SalesInvoice(Document):

    def validate(self):

        if self.paid_amount is None:
            self.paid_amount = 0

        if self.paid_amount > self.grand_total:
            frappe.throw(
                "Paid Amount cannot be greater than Grand Total."
            )

        if self.grand_total and self.grand_total > 0:
            self.payment_completion = (
                self.paid_amount / self.grand_total
            ) * 100
        else:
            self.payment_completion = 0

        if (
            self.grand_total > 0
            and self.paid_amount == self.grand_total
        ):
            self.status = "Paid"
        else:
            self.status = "Unpaid"