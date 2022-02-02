# Copyright (c) 2022, Ecosoft Co., Ltd. and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.website.website_generator import WebsiteGenerator
from erpnext.accounts.utils import get_account_currency
from frappe.utils import add_months, get_last_day


class TaxInvoice(WebsiteGenerator):
    
    def validate_tax_invoice(self):
        if not all([
            self.tax_invoice_number, self.tax_invoice_date, self.party_type, self.party,
            self.account, self.tax_base, self.tax_amount, self.voucher_type, self.voucher_no, self.company
        ]):
            frappe.throw(_("All fields are required before submission."))

    def compute_report_date(self):
        dt = self.tax_invoice_date
        if dt:
            dt = add_months(dt, int(self.months_delayed))
            frappe.db.set_value(self.doctype, self.name, "report_date", get_last_day(dt))
        else:
            frappe.db.set_value(self.doctype, self.name, "report_date", False)
        self.reload()

    def on_submit(self):
        self.validate_tax_invoice()
        self.compute_report_date()

    def on_update_after_submit(self):
        self.compute_report_date()


def make_tax_invoice(invoice, payment=None, alloc_percent=1):
    """ Create Tax Invoice from invoice tax table """
    from erpnext.accounts.general_ledger import make_gl_entries, make_reverse_gl_entries

    for tax in invoice.get("taxes"):
        # Create Tax Invoice
        tax_invoice_dict = prepare_tax_invoice_dict(tax, invoice, payment, alloc_percent)
        if not tax_invoice_dict:
            continue
        # Make Tax Invoice
        tinv = frappe.new_doc("Tax Invoice")
        tinv.update(tax_invoice_dict)
        tinv.insert()
        # Add adjustment tax GL for payment entry, 1. undue vat account -> 2. vat acount
        if payment:
            gl_entries = get_gl_entries(tax, tinv, payment, alloc_percent)
            make_gl_entries(gl_entries)
        # Auto submit tax invoice document for sales tax
        if invoice.doctype == "Sales Invoice":
            tinv.submit()

def get_gl_entries(tax, tinv, payment, alloc_percent):
    gl_entries = []
    dr_or_cr = ["debit", "credit"] if payment.payment_type == "Receive" else ["credit", "debit"]
    account_currency = get_account_currency(tax.account_head)
    for i in range(2):
        account = tax.account_head if i == 0 else tinv.account
        gl_entries.append(
            payment.get_gl_dict({
                "account": account,
                "against": payment.party,
                dr_or_cr[i]: alloc_percent * abs(tax.base_tax_amount),
                dr_or_cr[i] + "_in_account_currency":
                    alloc_percent * abs(
                        tax.base_tax_amount if account_currency==payment.company_currency
                        else tax.tax_amount
                    ),
                "cost_center": tax.cost_center
            }, account_currency, item=tax)
        )
    return gl_entries

def make_tax_invoice_on_invoice(invoice, method=None):
    """ Create Tax Invoice from document submission """
    make_tax_invoice(invoice)

def make_tax_invoice_on_payment(payment, method=None):
    """ Create Tax Invoice from payment submission (undue to due vat) """
    for ref in payment.get("references"):
        alloc_percent = ref.allocated_amount / ref.total_amount
        invoice = frappe.get_doc(ref.reference_doctype, ref.reference_name)
        # Make tax invoice only when invoice was using undue vat
        if invoice.get("taxes"):
            if ref.reference_doctype not in ("Sales Invoice", "Purchase Invoice"):
                frappe.throw(_("Invalid reference doctype fo Tax Invoice"))
            make_tax_invoice(invoice, payment, alloc_percent)

def prepare_tax_invoice_dict(tax, invoice, payment=None, alloc_percent=None):
    """ Prepare tax invoice dict
        1) On invoice and tax account is vat
        2) On payment and tax account on invoice is undue vat -> vat
    """
    doc = payment or invoice
    setting = frappe.get_doc("TH VAT Settings")
    # Get final vat account
    account = False
    if payment:  # On Payment
        if invoice.doctype == "Sales Invoice":
            if tax.account_head == setting.undue_sales_vat_account:
                account = setting.sales_vat_account
        if invoice.doctype == "Purchase Invoice":
            if tax.account_head == setting.undue_purchase_vat_account:
                account = setting.purchase_vat_account
    else:  # On Invoice
        if invoice.doctype == "Sales Invoice":
            if tax.account_head == setting.sales_vat_account:
                account = setting.sales_vat_account
        if invoice.doctype == "Purchase Invoice":
            if tax.account_head == setting.purchase_vat_account:
                account = setting.purchase_vat_account
    if not account:
        return {}
    vals = {
        "account": account,
        "tax_base": alloc_percent * (tax.base_total - tax.base_tax_amount),
        "tax_amount": alloc_percent * (tax.base_tax_amount),
        "voucher_type": doc.doctype,
        "voucher_no": doc.name,
        "company": doc.company,
    }
    # Get tax invoice, for case Sales Invoice
    if invoice.doctype == "Sales Invoice":
        vals.update({
            "tax_invoice_number": doc.name,
            "tax_invoice_date": doc.posting_date,
        })
    # Get party from Invoice
    vals.update({
        "party_type": invoice.doctype == "Sales Invoice" and "Customer" or "Supplier",
        "party": invoice.doctype == "Sales Invoice" and invoice.customer or invoice.supplier,
    })
    # Get party Tax ID
    vals.update({
        "party_tax_id": frappe.get_value(vals["party_type"], vals["party"], "tax_id"),
    })
    return vals

@frappe.whitelist()
def create_tax_invoice(source_name, target_doc=None):
    from frappe.model.mapper import get_mapped_doc

    def set_missing_values(source, target):
        for al in source.accounts:
            if al.party_type and al.party:
                (target.party_type, target.party) = (al.party_type, al.party)
                target.party_tax_id = frappe.get_value(al.party_type, al.party, "tax_id")
            account = frappe.get_doc("Account", al.account)
            th_vat_settings = frappe.get_doc("TH VAT Settings")
            if th_vat_settings.sales_vat_account == account.name:
                target.tax_amount = al.credit - al.debit
            elif th_vat_settings.purchase_vat_account == account.name:
                target.tax_amount = al.debit - al.credit
            target.account = account.name
        
    doclist = get_mapped_doc("Journal Entry", source_name, {
		"Journal Entry": {
			"doctype": "Tax Invoice",
            "field_map": {
                "voucher_type": "voucher_type",
                "name": "voucher_no",
            }
		},
	}, target_doc, set_missing_values)

    return doclist
