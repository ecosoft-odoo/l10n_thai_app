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
			"fieldname": "supplier_tax_id",
			"label": _("Tax ID"),
			"fieldtype": "Data",
			"width": 100,
		},
		{
			"fieldname": "supplier",
			"label": _("Supplier"),
			"fieldtype": "Data",
			"width": 200,
		},
		{
			"fieldname": "supplier_address",
			"label": _("Address"),
			"fieldtype": "Data",
			"width": 200,
		},
		{
			"fieldname": "date",
			"label": _("Date"),
			"fieldtype": "Date",
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
			"fieldname": "tax_rate",
			"label": _("Rate"),
			"fieldtype": "Percent",
			"width": 20,
		},
		{
			"fieldname": "tax_amount",
			"label": _("Tax Amount"),
			"fieldtype": "Currency",
			"options": "Company:company:default_currency",
			"width": 150,
		},
		{
			"fieldname": "tax_payer",
			"label": _("Tax Payer"),
			"fieldtype": "Data",
			"width": 200,
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

def get_report_fields():
	fields = []
	for p_field in [
			'date', 'supplier', 'supplier_tax_id', 'supplier_address',
			'company', 'company_tax_id', 'tax_payer', 'voucher_type', 'voucher_no',
		]:
		fields.append('`tabWithholding Tax Cert`.`{}`'.format(p_field))

	for c_field in ['tax_base', 'tax_rate', 'tax_amount']:
		fields.append('`tabWithholding Items`.`{}`'.format(c_field))

	return fields

def get_data(filters):
	data = []
	if not (filters.income_tax_form and filters.year and filters.month):
		return data
	# Get date range
	total_days_in_month = monthrange(cint(filters.year), cint(filters.month))[1]
	date_from = "%s-%s-%s" % (filters.year, filters.month, 1)
	date_to = "%s-%s-%s" % (filters.year, filters.month, total_days_in_month)
	data = frappe.db.get_all(
		"Withholding Tax Cert",
		filters={
			"company": filters.company,
			"date": ["between", [date_from, date_to]],
			"income_tax_form": filters.income_tax_form,
			"docstatus": "1",
		},
		fields = get_report_fields(),
		order_by="date"
	)
	return data

@frappe.whitelist()
def get_tax_years():
	year_list = frappe.db.sql_list("""
		select distinct YEAR(date) from `tabWithholding Tax Cert`
		where date is not null
		ORDER BY YEAR(date) DESC
	""")
	if not year_list:
		year_list = [getdate().year]
	return "\n".join(str(year) for year in year_list)
