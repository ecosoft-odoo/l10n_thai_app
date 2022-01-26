// Copyright (c) 2016, Ecosoft Co., Ltd. and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Project Support Summary"] = {
	"filters": [
		{
			"fieldname": "customer",
			"label": __("Customer"),
			"fieldtype": "Link",
			"options": "Customer",
			"reqd": 0,
		},
		{
			"fieldname": "name",
			"label": __("Project"),
			"fieldtype": "Link",
			"options": "Project",
			"reqd": 0,
		},
		{
			"fieldname": "status",
			"label": __("Status"),
			"fieldtype": "Select",
			"options": "Open\nCompleted\nCancelled",
			"default": "Open",
			"reqd": 0,
		},
	]
};
