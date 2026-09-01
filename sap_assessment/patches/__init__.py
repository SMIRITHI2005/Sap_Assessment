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
    ON si.sales_order = so.name;
    
 Absolutely. Since you're learning Frappe for your O2C assessment, here's a **practical command cheat sheet** covering the Bench and Frappe commands you'll actually use, plus the important ones you should know for interviews/assessment.

One important distinction first:

```text
BENCH
  ↓
Manages the Frappe environment, apps, sites, processes

FRAPPE / SITE COMMANDS
  ↓
Operate on a particular site's database, apps, cache, migrations, etc.
```

# 🏗️ 1. Bench Commands

## 🔹 Bench basics

| Command           | What it does                           |
| ----------------- | -------------------------------------- |
| `bench --help`    | Shows available Bench commands         |
| `bench version`   | Shows Bench/Frappe/app versions        |
| `bench start`     | Starts local development processes     |
| `bench update`    | Updates Bench/apps and applies updates |
| `bench --verbose` | Shows more detailed command output     |

---

# 🏠 2. Site commands

### Create a site

```bash
bench new-site assessment.local
```

Creates a new Frappe site and its database.

Useful options include:

```bash
bench new-site assessment.local --admin-password password
```

---

### List sites

```bash
bench list-sites
```

Shows sites available in your bench.

---

### Delete a site

```bash
bench drop-site assessment.local
```

⚠️ Destructive — don't use this casually.

---

### Set default site

```bash
bench use assessment.local
```

After this:

```bash
bench console
```

can work against `assessment.local` without repeatedly specifying:

```bash
--site assessment.local
```

---

# 📦 3. App commands

### Create an app

You already used:

```bash
bench new-app sap_assessment
```

Creates:

```text
apps/
└── sap_assessment/
```

---

### Get an app

```bash
bench get-app <app>
```

Downloads an app into the bench.

Example:

```bash
bench get-app erpnext
```

---

### Install an app on a site

```bash
bench --site assessment.local install-app sap_assessment
```

This makes the app available to that site.

---

### Uninstall an app

```bash
bench --site assessment.local uninstall-app sap_assessment
```

⚠️ Be careful: uninstalling can remove app data.

---

### List installed apps

```bash
bench --site assessment.local list-apps
```

You should see something like:

```text
frappe
sap_assessment
```

---

# 🗄️ 4. Database commands

### Migrate

One of the most important commands:

```bash
bench --site assessment.local migrate
```

Synchronizes:

```text
DocTypes
Database schema
Patches
Fixtures
Hooks
Other metadata
```

For example, you added:

```text
api_processed
```

to Sales Order.

After changing the DocType:

```bash
bench --site assessment.local migrate
```

helps synchronize that change with MariaDB.

---

### Backup

```bash
bench --site assessment.local backup
```

Creates a backup of your site's data.

You can also use:

```bash
bench --site assessment.local backup --with-files
```

when you want the site's files included.

---

### Restore

```bash
bench --site assessment.local restore <backup-file>
```

Restores a database backup.

⚠️ Be very careful with this because it replaces database contents.

---

### Database console

Depending on your setup/version:

```bash
bench --site assessment.local mariadb
```

opens the database client.

Then you can run SQL such as:

```sql
SHOW TABLES;
```

or:

```sql
SHOW COLUMNS FROM `tabSales Order`;
```

---

# 🧪 5. Development/testing commands

### Frappe console

```bash
bench --site assessment.local console
```

This is one of your most useful commands.

Example:

```python
frappe.get_doc("Sales Order", "SO-00001")
```

or:

```python
frappe.db.get_value(
    "Sales Order",
    "SO-00001",
    "api_processed"
)
```

Think:

> **Console = Python laboratory for Frappe.**

---

### Execute a Python function

```bash
bench --site assessment.local execute <python.path>
```

Example:

```bash
bench --site assessment.local execute sap_assessment.tasks.daily_maintenance
```

This directly executes your Python function.

---

# 🧹 6. Cache commands

### Clear cache

```bash
bench --site assessment.local clear-cache
```

Useful after changing:

* hooks
* Python code
* configuration
* DocTypes
* cached metadata

---

### Clear website cache

```bash
bench --site assessment.local clear-website-cache
```

Useful when website pages aren't reflecting changes.

---

# 🔧 7. Build/assets commands

When you modify JavaScript/CSS/assets:

```bash
bench build
```

For your app:

```text
sap_assessment
   ↓
public/
   ↓
JS/CSS/assets
   ↓
bench build
   ↓
browser
```

You can also build a specific app:

```bash
bench build --app sap_assessment
```

---

# 📁 8. Bench folder/navigation commands

Useful Linux commands around Bench:

```bash
cd ~/frappe-bench
```

Check files:

```bash
ls
```

Check apps:

```bash
ls apps
```

Check your app:

```bash
ls apps/sap_assessment
```

Check logs:

```bash
ls logs
```

Follow a log:

```bash
tail -f logs/web.log
```

Search logs:

```bash
grep -R "O2C" logs
```

---

# ⚙️ 9. Production commands

These matter more when deploying Frappe to a real server.

### Setup production

```bash
sudo bench setup production <user>
```

This configures things such as:

```text
Nginx
Supervisor
Frappe processes
```

---

### Setup Nginx

```bash
bench setup nginx
```

---

### Setup Supervisor

```bash
bench setup supervisor
```

---

### Enable scheduler

```bash
bench --site assessment.local enable-scheduler
```

---

### Disable scheduler

```bash
bench --site assessment.local disable-scheduler
```

---

### Check scheduler

```bash
bench --site assessment.local doctor
```

This can help diagnose scheduler/background-job problems.

---

# 🔐 10. SSL / HTTPS

For a real public domain, Frappe can configure Let's Encrypt:

```bash
sudo bench setup lets-encrypt yourdomain.com
```

This is **not something you need for your local `assessment.local` development site**.

---

# 🧑‍💻 11. Your custom Bench commands

This is what you were just working on.

You created:

```text
sap_assessment/
└── sap_assessment/
    └── commands.py
```

For example:

```python
@click.command()
def pending_deliveries():
    ...
```

Then Bench can expose it as:

```bash
bench pending-deliveries
```

Remember:

```python
pending_deliveries
```

becomes:

```bash
pending-deliveries
```

because Click converts the underscore-style Python function name to a CLI command name.

---

# 🐍 12. Important Frappe Python commands/APIs

Now this is different from Bench.

These aren't terminal commands.

They're **Python APIs** you use inside:

```text
.py
```

files or:

```bash
bench console
```

---

## Document API

### Get a document

```python
doc = frappe.get_doc(
    "Sales Order",
    "SO-00001"
)
```

---

### Create a document

```python
doc = frappe.new_doc("Sales Order")
```

---

### Save

```python
doc.save()
```

---

### Insert

```python
doc.insert()
```

---

### Submit

```python
doc.submit()
```

---

### Cancel

```python
doc.cancel()
```

---

### Delete

```python
frappe.delete_doc(
    "Sales Order",
    "SO-00001"
)
```

---

### Get last document

```python
frappe.get_last_doc("Sales Order")
```

---

### Cached document

```python
frappe.get_cached_doc(
    "Customer",
    "CUST-00001"
)
```

---

# 🗃️ 13. Database API

### Get one value

```python
frappe.db.get_value(
    "Sales Order",
    "SO-00001",
    "grand_total"
)
```

---

### Get multiple values

```python
frappe.db.get_values(
    "Sales Order",
    {"customer": "ABC"},
    ["name", "grand_total"]
)
```

---

### Get records

```python
frappe.get_list(
    "Sales Order",
    fields=["name", "customer"]
)
```

---

### Get all

```python
frappe.get_all(
    "Sales Order",
    fields=["name", "customer"]
)
```

Remember:

```text
get_list()
   ↓
checks permissions

get_all()
   ↓
bypasses normal permission filtering
```

---

### Check if something exists

```python
frappe.db.exists(
    "Sales Order",
    "SO-00001"
)
```

---

### Update one field

```python
frappe.db.set_value(
    "Sales Order",
    "SO-00001",
    "api_processed",
    1
)
```

This was part of your earlier assignment.

---

### Commit

```python
frappe.db.commit()
```

Usually Frappe manages transactions for normal web requests, so **don't randomly add commits everywhere**.

---

### Rollback

```python
frappe.db.rollback()
```

---

# 🔎 14. Query Builder

You used this too.

```python
SalesOrder = frappe.qb.DocType("Sales Order")
Customer = frappe.qb.DocType("Customer")
```

Then:

```python
query = (
    frappe.qb.from_(SalesOrder)
    .join(Customer)
    .on(SalesOrder.customer == Customer.name)
    .select(
        SalesOrder.name,
        Customer.customer_name
    )
)
```

Run:

```python
results = query.run(as_dict=True)
```

Think:

```text
frappe.qb
   ↓
build SQL using Python
   ↓
JOIN
   ↓
SELECT
   ↓
WHERE
   ↓
run()
```

---

# 🌐 15. API commands

### Whitelist a Python method

```python
@frappe.whitelist()
def my_api():
    return "Hello"
```

Then call it from:

```text
/api/method/<python.path>
```

For your app:

```text
/api/method/sap_assessment.api.o2c.o2c_sales_order_report
```

---

### Client → Server

```javascript
frappe.call({
    method: "sap_assessment.api.o2c.o2c_sales_order_report",

    callback: function(response) {
        console.log(response.message);
    }
});
```

Flow:

```text
JavaScript
   ↓
frappe.call()
   ↓
HTTP
   ↓
@frappe.whitelist()
   ↓
Python
   ↓
Database
   ↓
JSON response
```

---

# 🔔 16. Realtime

Server:

```python
frappe.publish_realtime(
    "o2c_sales_invoice_submitted",
    {
        "name": doc.name
    }
)
```

Client:

```javascript
frappe.realtime.on(
    "o2c_sales_invoice_submitted",
    function(data) {
        console.log(data);
    }
);
```

Flow:

```text
Python
 ↓
publish_realtime()
 ↓
Redis
 ↓
Socket.IO
 ↓
Browser
 ↓
JavaScript listener
```

That's the realtime functionality you were learning earlier.

---

# 📝 17. Logging

```python
logger = frappe.logger("o2c")

logger.info("Sales Invoice submitted")
```

Other levels:

```python
logger.debug(...)
logger.info(...)
logger.warning(...)
logger.error(...)
logger.critical(...)
```

Your O2C example:

```python
frappe.logger("o2c").info(
    f"Sales Invoice {doc.name} submitted"
)
```

---

# 🖥️ 18. Client-side Frappe APIs

These are JavaScript APIs.

### Message

```javascript
frappe.msgprint("Sales Invoice submitted!");
```

### Call backend

```javascript
frappe.call({...});
```

### Form

```javascript
frappe.ui.form.on("Sales Order", {
    refresh(frm) {
        console.log("Sales Order loaded");
    }
});
```

### Dialog

```javascript
let d = new frappe.ui.Dialog({
    title: "Create O2C Task",
    fields: [
        {
            label: "Subject",
            fieldname: "subject",
            fieldtype: "Data"
        }
    ]
});

d.show();
```

### Routing

```javascript
frappe.new_doc("Sales Order");
```

### Realtime

```javascript
frappe.realtime.on("my_event", callback);
```

---

# 🧠 The commands I want you to memorize

Don't try to memorize 100 commands. For your assessment, these are the **core ones**:

```bash
bench start
bench --help
bench version
bench use assessment.local
bench new-site
bench new-app
bench get-app
bench --site assessment.local install-app
bench --site assessment.local list-apps
bench --site assessment.local migrate
bench --site assessment.local console
bench --site assessment.local execute
bench --site assessment.local clear-cache
bench --site assessment.local backup
bench build
bench --site assessment.local enable-scheduler
bench --site assessment.local disable-scheduler


Document API
    frappe.get_doc()
    frappe.new_doc()
    doc.save()
    doc.insert()
    doc.submit()

Database API
    frappe.db.get_value()
    frappe.db.set_value()
    frappe.get_list()
    frappe.get_all()

Query Builder
    frappe.qb

Realtime
    frappe.publish_realtime()
```

That distinction will make a *lot* of your Frappe learning suddenly click."""
