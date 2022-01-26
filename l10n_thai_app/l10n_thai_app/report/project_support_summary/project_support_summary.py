# Copyright (c) 2013, Ecosoft Co., Ltd. and contributors
# For license information, please see license.txt

import frappe
from frappe import _


def execute(filters=None):
	columns = get_columns()
	data = get_data(filters)
	chart = get_chart_data(data)
	return columns, data, None, chart, None

def get_columns():
	return [
		{
			"fieldname": "customer",
			"label": _("Customer"),
			"fieldtype": "Link",
			"options": "Customer",
			"width": 200,
		},
		{
			"fieldname": "name",
			"label": _("Project ID"),
			"fieldtype": "Link",
			"options": "Project",
			"width": 100,
		},
		{
			"fieldname": "project_name",
			"label": _("Project Name"),
			"fieldtype": "Data",
			"width": 200,
		},
		{
			"fieldname": "status",
			"label": _("Status"),
			"fieldtype": "Data",
			"width": 120,
		},
		{
			"fieldname": "support_hours",
			"label": _("Hours"),
			"fieldtype": "Float",
			"width": 80,
		},
		{
			"fieldname": "support_hours_used",
			"label": _("Used"),
			"fieldtype": "Float",
			"width": 80,
		},
		{
			"fieldname": "support_hours_bal",
			"label": _("Balance"),
			"fieldtype": "Float",
			"width": 80,
		},
	]

def get_data(filters):
	filters.project_type = "Support Package"
	data = frappe.db.get_all(
	"Project", filters=filters,
	fields=[
		"name", "status", "customer", "project_name", "support_hours", "support_hours_used",
	],
	order_by="customer")
	for project in data:
		project.project_code = "%s / %s" % (project.customer, project.name)
		project.support_hours = (project.support_hours or 0) / 3600
		project.support_hours_used = (project.support_hours_used or 0) / 3600
		project.support_hours_bal = project.support_hours - project.support_hours_used
	return data

def get_chart_data(data):
	labels = []
	used = []
	balance = []

	for project in data:
		labels.append(project.project_code)
		used.append(project.support_hours_used)
		balance.append(project.support_hours_bal)

	return {
		"data": {
			'labels': labels[:30],
			'datasets': [
				{
					"name": "Used",
					"values": used[:30]
				},
				{
					"name": "Balance",
					"values": balance[:30]
				},
			]
		},
		"type": "bar",
		"colors": ["#fc4f51", "#7575ff"],
		"barOptions": {
			"stacked": True
		}
	}