# Copyright (c) 2022, Ecosoft Co., Ltd. and contributors
# For license information, please see license.txt
import json
import frappe
from frappe import _
from frappe.model.document import Document


class WithholdingTaxCert(Document):

    @property
    def total_tax_base(self):
        total = 0.0
        for item in self.items:
            total += item.tax_base
        return total


def check_wht_cert(payment, method=None):
    """ If this payment contain WHT, give warning """
    for tax in payment.taxes:
        account = frappe.get_doc("Account", tax.account_head)
        if account.tax_rate > 0 and account.is_withholding_tax:
            frappe.msgprint(
                msg=_("This payment has withholding tax amount, "
                      "please be reminded to create withholding "
                      "tax certificate for it."),
                title=_("Withholding Cert Warning"),
            )


@frappe.whitelist()
def create_wht_tax_cert(source_name, target_doc=None):
    from frappe.model.mapper import get_mapped_doc

    def set_missing_values(source, target):
        target.voucher_type = "Payment Entry"
        for tax in source.taxes:
            account = frappe.get_doc("Account", tax.account_head)
            if account.tax_rate > 0 and account.is_withholding_tax:
                target.append("items", {
                    "tax_rate": account.tax_rate,
                    "tax_amount": abs(tax.base_tax_amount),
                    "tax_base": abs(tax.base_tax_amount) * 100 / account.tax_rate,
                })
        
    doclist = get_mapped_doc("Payment Entry", source_name, {
		"Payment Entry": {
			"doctype": "Withholding Tax Cert",
            "field_map": {
                "party_name": "supplier",
                "name": "voucher_no",
            }
		},
	}, target_doc, set_missing_values)

    return doclist