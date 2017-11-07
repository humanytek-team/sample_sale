# -*- coding: utf-8 -*-
from openerp import models, fields, api, _
from openerp.exceptions import UserError, RedirectWarning, ValidationError


class AccountInvoice(models.Model):
    _inherit = "account.invoice"


    @api.one
    @api.depends('invoice_line_ids.price_subtotal', 'tax_line_ids.amount', 'currency_id', 'company_id', 'date_invoice', 'type', 'sample')
    def _compute_amount(self):
        #print '_compute_amount'
        if self.sample:
            #self.amount_untaxed = sum(line.price_subtotal for line in self.invoice_line_ids)
            self.amount_untaxed = 0.01

            #self.amount_tax = sum(line.amount for line in self.tax_line_ids)
            self.amount_tax = 0.0

            #self.amount_total = self.amount_untaxed + self.amount_tax
            self.amount_total = 0.01

            amount_total_company_signed = self.amount_total
            amount_untaxed_signed = self.amount_untaxed

            if self.currency_id and self.company_id and self.currency_id != self.company_id.currency_id:
                currency_id = self.currency_id.with_context(date=self.date_invoice)
                amount_total_company_signed = currency_id.compute(self.amount_total, self.company_id.currency_id)
                amount_untaxed_signed = currency_id.compute(self.amount_untaxed, self.company_id.currency_id)
            sign = self.type in ['in_refund', 'out_refund'] and -1 or 1
            self.amount_total_company_signed = amount_total_company_signed * sign
            self.amount_total_signed = self.amount_total * sign
            self.amount_untaxed_signed = amount_untaxed_signed * sign
        else:
            super(AccountInvoice,self)._compute_amount()
        #print 'end'


    sample = fields.Boolean('Sample', help='if checked, invoice total amount will be 0.01')