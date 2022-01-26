// Copyright (c) 2016, Ecosoft Co., Ltd. and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["TH VAT"] = {
	"filters": [
		{
			"fieldname":"company",
			"label": __("Company"),
			"fieldtype": "Link",
			"options": "Company",
			"default": frappe.defaults.get_user_default("Company"),
			"reqd": 1
		},
		{
			"fieldname": "report_type",
			"label": __("Report Type"),
			"fieldtype": "Select",
			"reqd": 1 ,
			"options": [
				{ "value": "sale", "label": __("Sales VAT Report") },
				{ "value": "purchase", "label": __("Purchase VAT Report") },
			],
		},
		{
			"fieldname":"year",
			"label": __("Year"),
			"fieldtype": "Select",
		},
		{
			"fieldname": "month",
			"label": __("Month"),
			"fieldtype": "Select",
			"options": [1,2,3,4,5,6,7,8,9,10,11,12],
		},
	],

	"onload": function() {
		return  frappe.call({
			method: "l10n_thai_app.l10n_thai_app.report.th_vat.th_vat.get_tax_years",
			callback: function(r) {
				var year_filter = frappe.query_report.get_filter("year");
				year_filter.df.options = r.message;
				year_filter.refresh();
				year_filter.set_input(year_filter.df.default);
			}
		});
	}
}
