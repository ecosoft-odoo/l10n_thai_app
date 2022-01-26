// Copyright (c) 2022, Ecosoft Co., Ltd. and contributors
// For license information, please see license.txt

frappe.ui.form.on('Tax Invoice', {
	refresh: function(frm) {
		frm.set_query("party_type", function() {
			return {
				filters: {
					"name": ["in", ["Customer", "Supplier"]]
				}
			}
		});
	}
});
