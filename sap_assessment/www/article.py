import frappe

def get_context(context):
    context.articles = frappe.get_all(
        "Article",
        filters={"status": "Published"},
        fields=["title", "name"]
    )

    return context