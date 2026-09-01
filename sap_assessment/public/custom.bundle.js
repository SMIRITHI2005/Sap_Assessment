console.log("=== O2C Asset Bundle ===");

const today = new Date();
const formatDate = (date) => date.toISOString().slice(0, 10);
const formatDateTime = (date) =>
    date.toISOString().slice(0, 19).replace("T", " ");
const addDays = (date, days) => {
    const nextDate = new Date(date);
    nextDate.setDate(nextDate.getDate() + days);
    return nextDate;
};

console.log(
    "O2C Current Date:",
    formatDate(today)
);

console.log(
    "O2C Current Date & Time:",
    formatDateTime(today)
);

console.log(
    "Expected Delivery Date Example:",
    formatDate(addDays(today, 7))
);

console.log(
    "Payment Due Date Example:",
    formatDate(addDays(today, 30))
);


// O2C document submission sound
const o2c_doctypes = [
    "Sales Order",
    "Delivery Note",
    "Sales Invoice",
    "Payment Entry"
];

frappe.ui.form.on("*", {
    after_save(frm) {
        if (
            o2c_doctypes.includes(frm.doctype) &&
            frm.doc.docstatus === 1
        ) {
            console.log(`${frm.doctype} submitted`);
            
            // Play submission sound
            const audio = new Audio(
                "/assets/sap_assessment/sounds/o2c_submit.mp3"
            );

            audio.play().catch((error) => {
                console.log("Unable to play O2C submission sound:", error);
            });
        }
    }
});

frappe.realtime.on("o2c_sales_invoice_submitted", function(data) {
    console.log("=== REALTIME EVENT RECEIVED ===");
    console.log("Invoice:", data.name);
    console.log("Customer:", data.customer);
    console.log("Grand Total:", data.grand_total);

    frappe.show_alert({
        message: `Sales Invoice ${data.name} submitted successfully`,
        indicator: "green"
    });
});
frappe.ui.form.on("Sales Order", {
    refresh(frm) {

        if (frm.doc.docstatus === 1) {

            frm.add_custom_button(
                "Create Delivery Note",
                function() {

                    let d = new frappe.ui.Dialog({
                        title: "Create Delivery Note",

                        fields: [
                            {
                                label: "Delivery Date",
                                fieldname: "delivery_date",
                                fieldtype: "Date",
                                reqd: 1,
                                default: frappe.datetime.add_days(
                                    frappe.datetime.now_date(),
                                    7
                                )
                            }
                        ],

                        primary_action_label: "Create Delivery Note",

                        primary_action(values) {

                            frappe.call({
                                method: "sap_assessment.api.o2c.create_delivery_note_from_dialog",

                                args: {
                                    sales_order_name: frm.doc.name,
                                    delivery_date: values.delivery_date
                                },

                                callback: function(response) {

                                    if (response.message) {

                                        d.hide();

                                        frappe.msgprint({
                                            title: __("Success"),
                                            indicator: "green",
                                            message: __(
                                                "Delivery Note {0} created successfully.",
                                                [response.message]
                                            )
                                        });

                                    }
                                }
                            });
                        }
                    });

                    d.show();
                }
            );
        }
    }
});