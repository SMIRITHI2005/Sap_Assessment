import dayjs from "dayjs";

console.log("=== O2C Asset Bundle ===");

const today = dayjs();

console.log(
    "O2C Current Date:",
    today.format("YYYY-MM-DD")
);

console.log(
    "O2C Current Date & Time:",
    today.format("YYYY-MM-DD HH:mm:ss")
);

console.log(
    "Expected Delivery Date Example:",
    today.add(7, "day").format("YYYY-MM-DD")
);

console.log(
    "Payment Due Date Example:",
    today.add(30, "day").format("YYYY-MM-DD")
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