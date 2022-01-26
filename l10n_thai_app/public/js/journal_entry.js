// Copyright (c) 2018, Frappe Technologies Pvt. Ltd. and Contributors
// MIT License. See license.txt

// frappe.provide("erpnext.accounts");
// frappe.provide("erpnext.journal_entry");


frappe.ui.form.on("Journal Entry", {

	refresh: function(frm) {
		if(frm.doc.docstatus == 1) {
			frm.add_custom_button(__("Create Tax Invoice"), function () {
				frm.trigger("create_tax_invoice");
			}, __('Make'));
		}
		// if(frm.doc.docstatus > 0) {
		// 	frm.add_custom_button(__("Tax Invoice"), function() {
		// 		frappe.route_options = {
		// 			voucher_no: frm.doc.name,
		// 			company: frm.doc.company
		// 		};
		// 		frappe.set_route("List", "Tax Invoice");
		// 	}, __("View"));
		// }
	},

	create_tax_invoice: function() {
		frappe.model.open_mapped_doc({
			method: "l10n_thai_app.l10n_thai_app.doctype.tax_invoice.tax_invoice.create_tax_invoice",
			frm: cur_frm
		})
	},

});