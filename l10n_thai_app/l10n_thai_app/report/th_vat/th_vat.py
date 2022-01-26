# Copyright (c) 2013, Ecosoft Co., Ltd. and contributors
# For license information, please see license.txt

from calendar import monthrange

import frappe
from frappe import _
from frappe.utils import cint, getdate, get_url_to_list


def execute(filters=None):
	columns = get_columns()
	data = get_data(filters)
	return columns, data

def get_columns():
	return [
		{
			"fieldname": "tax_invoice_date",
			"label": _("Date"),
			"fieldtype": "Date",
			"width": 100,
		},
		{
			"fieldname": "tax_invoice_number",
			"label": _("Number"),
			"fieldtype": "Data",
			"width": 200,
		},
		{
			"fieldname": "party",
			"label": _("Party"),
			"fieldtype": "Data",
			"width": 200,
		},
		{
			"fieldname": "party_tax_id",
			"label": _("Tax ID"),
			"fieldtype": "Data",
			"width": 100,
		},
		{
			"fieldname": "party_branch_id",
			"label": _("Branch ID"),
			"fieldtype": "Data",
			"width": 100,
		},
		{
			"fieldname": "tax_base",
			"label": _("Base Amount"),
			"fieldtype": "Currency",
			"options": "Company:company:default_currency",
			"width": 150,
		},
		{
			"fieldname": "tax_amount",
			"label": _("Tax Amount"),
			"fieldtype": "Currency",
			"options": "Company:company:default_currency",
			"width": 150,
		},
		{
			"fieldname": "voucher_type",
			"label": _("Ref Type"),
			"fieldtype": "Link",
			"options": "DocType",
			"hidden": 1,
			"width": 200,
		},
		{
			"fieldname": "voucher_no",
			"label": _("Reference"),
			"fieldtype": "Dynamic Link",
			"options": "voucher_type",
			"width": 200,
		},
	]

def get_data(filters):
	data = []
	if frappe.db.exists("TH VAT Settings", filters.company) is None:
		url = get_url_to_list("TH VAT Settings")
		frappe.msgprint(_('Create <a href="{}">TH VAT Settings</a> for this company').format(url))
		return data
	if not (filters.report_type and filters.year and filters.month):
		return data
	# Get report account code
	account = False
	if filters.report_type == "sale":
		account = frappe.db.get_singles_value("TH VAT Settings", "sales_vat_account")
	if filters.report_type == "purchase":
		account = frappe.db.get_singles_value("TH VAT Settings", "purchase_vat_account")
	# Get date range
	total_days_in_month = monthrange(cint(filters.year), cint(filters.month))[1]
	date_from = "%s-%s-%s" % (filters.year, filters.month, 1)
	date_to = "%s-%s-%s" % (filters.year, filters.month, total_days_in_month)
	data = frappe.db.get_all(
		"Tax Invoice",
		filters={
			"company": filters.company,
			"tax_invoice_date": ["between", [date_from, date_to]],
			"account": account,
			"docstatus": ["in", ("1", "2")],  # submitted, cancelled
		},
		fields=[
			"tax_invoice_date", "tax_invoice_number", "party_type", "party", "party_tax_id", "tax_base", "tax_amount", "voucher_type", "voucher_no", "docstatus"
		],
		order_by="tax_invoice_date, tax_invoice_number"
	)
	company = frappe.get_doc("Company", filters.company)
	for rec in data:
		rec.company = company  # Add company to be used as print header
		if rec.docstatus == 2:
			rec.tax_invoice_number = _("%s (Cancelled)") % rec.tax_invoice_number
			rec.tax_base = 0
			rec.tax_amount = 0
	return data


@frappe.whitelist()
def get_tax_years():
	year_list = frappe.db.sql_list("""
		select distinct YEAR(tax_invoice_date) from `tabTax Invoice`
		where tax_invoice_date is not null
		ORDER BY YEAR(tax_invoice_date) DESC
	""")
	if not year_list:
		year_list = [getdate().year]
	return "\n".join(str(year) for year in year_list)
