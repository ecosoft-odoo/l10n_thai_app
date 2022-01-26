// Copyright (c) 2018, Frappe Technologies Pvt. Ltd. and Contributors
// MIT License. See license.txt

// frappe.provide("erpnext.accounts");
// frappe.provide("erpnext.journal_entry");


frappe.ui.form.on("Payment Entry", {

	refresh: function(frm) {
		if(frm.doc.docstatus == 1) {
			frm.add_custom_button(__("Create Withholding Tax Cert"), function () {
				frm.trigger("create_wht_tax_cert");
			});
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

	create_wht_tax_cert: function() {
		frappe.model.open_mapped_doc({
			method: "l10n_thai_app.l10n_thai_app.doctype.withholding_tax_cert.withholding_tax_cert.create_wht_tax_cert",
			frm: cur_frm
		})
	},

});