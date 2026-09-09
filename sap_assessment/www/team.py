import frappe


def get_context(context):
    context.user_list = frappe.get_all(
        "User",
        filters={"enabled": 1},
        fields=["full_name", "email"]
    )

    context.title = "Our Team"
    context.no_cache = True

    return context