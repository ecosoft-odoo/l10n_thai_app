from . import __version__ as app_version

app_name = "l10n_thai_app"
app_title = "l10n Thai App"
app_publisher = "Ecosoft Co., Ltd."
app_description = "l10n Thai App Module"
app_icon = "octicon octicon-file-directory"
app_color = "green"
app_email = "kittiu@ecosoft.co.th"
app_license = "MIT"

fixtures = [
    {
		"dt": "Custom Field",
		"filters": [("name", "in", [
			"Issue-time_spent",
			"Issue-project_name",
			"Project-support_hours",
			"Project-support_hours_used",
			"Account-is_withholding_tax",
		])],
	},
    {
		"dt": "DocType Link",
		"filters": [["link_doctype", "in", ["Tax Invoice", "Withholding Tax Cert"]]],
	},
    {
		"dt": "Project Type",
		"filters": [["project_type", "in", ["Support Package"]]],
	},
	{
		"dt": "Property Setter",
		"filters": [["name", "in", [
			"Issue-project-mandatory_depends_on",
			"Issue-customer-reqd",
			"Withholding Tax Cert-main-default_print_format",
		]]],
	},
	{
		"dt": "Client Script",
		"filters": [["name", "in", ["Issue-Form"]]],
	},
]


# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/l10n_thai_app/css/l10n_thai_app.css"
# app_include_js = "/assets/l10n_thai_app/js/l10n_thai_app.js"

# include js, css files in header of web template
# web_include_css = "/assets/l10n_thai_app/css/l10n_thai_app.css"
# web_include_js = "/assets/l10n_thai_app/js/l10n_thai_app.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "l10n_thai_app/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
doctype_js = {
	"Journal Entry" : "public/js/journal_entry.js",
	"Payment Entry" : "public/js/payment_entry.js",
}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Installation
# ------------

# before_install = "l10n_thai_app.install.before_install"
# after_install = "l10n_thai_app.install.after_install"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "l10n_thai_app.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

# override_doctype_class = {
# 	"ToDo": "custom_app.overrides.CustomToDo"
# }

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
#	}
# }

doc_events = {
	"Issue": {
		"validate": "l10n_thai_app.l10n_thai_app.support.update_project_support_hours"
	},
	"Sales Invoice": {
		"on_submit": "l10n_thai_app.l10n_thai_app.doctype.tax_invoice.tax_invoice.make_tax_invoice_on_invoice",
	},
	"Purchase Invoice": {
		"on_submit": "l10n_thai_app.l10n_thai_app.doctype.tax_invoice.tax_invoice.make_tax_invoice_on_invoice"
	},
	"Payment Entry": {
		"on_submit": "l10n_thai_app.l10n_thai_app.doctype.tax_invoice.tax_invoice.make_tax_invoice_on_payment",
		"on_submit": "l10n_thai_app.l10n_thai_app.doctype.withholding_tax_cert.withholding_tax_cert.check_wht_cert",
	},
}

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"l10n_thai_app.tasks.all"
# 	],
# 	"daily": [
# 		"l10n_thai_app.tasks.daily"
# 	],
# 	"hourly": [
# 		"l10n_thai_app.tasks.hourly"
# 	],
# 	"weekly": [
# 		"l10n_thai_app.tasks.weekly"
# 	]
# 	"monthly": [
# 		"l10n_thai_app.tasks.monthly"
# 	]
# }

# Testing
# -------

# before_tests = "l10n_thai_app.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "l10n_thai_app.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "l10n_thai_app.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]


# User Data Protection
# --------------------

user_data_fields = [
	{
		"doctype": "{doctype_1}",
		"filter_by": "{filter_by}",
		"redact_fields": ["{field_1}", "{field_2}"],
		"partial": 1,
	},
	{
		"doctype": "{doctype_2}",
		"filter_by": "{filter_by}",
		"partial": 1,
	},
	{
		"doctype": "{doctype_3}",
		"strict": False,
	},
	{
		"doctype": "{doctype_4}"
	}
]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
# 	"l10n_thai_app.auth.validate"
# ]

