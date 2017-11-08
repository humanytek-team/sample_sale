# -*- coding: utf-8 -*-
from openerp import models, fields, api, _
from openerp.exceptions import UserError, RedirectWarning, ValidationError

_COST = 0.01

class AccountInvoice(models.Model):
    _inherit = "account.invoice"


    @api.multi
    def get_taxes_values(self):
        print 'get_taxes_values'
        if self.sample:
            tax_grouped = {}
            for line in self.invoice_line_ids:
                #price_unit = line.price_unit * (1 - (line.discount or 0.0) / 100.0)
                price_unit = _COST * (1 - (line.discount or 0.0) / 100.0)

                taxes = line.invoice_line_tax_ids.compute_all(price_unit, self.currency_id, line.quantity, line.product_id, self.partner_id)['taxes']
                for tax in taxes:
                    val = self._prepare_tax_line_vals(line, tax)
                    key = self.env['account.tax'].browse(tax['id']).get_grouping_key(val)

                    if key not in tax_grouped:
                        tax_grouped[key] = val
                    else:
                        tax_grouped[key]['amount'] += val['amount']
                        tax_grouped[key]['base'] += val['base']
            return tax_grouped
        else:
            super(AccountInvoice,self).get_taxes_values()

    @api.one
    @api.depends('invoice_line_ids.price_subtotal', 'tax_line_ids.amount', 'currency_id', 'company_id', 'date_invoice', 'type', 'sample')
    def _compute_amount(self):
        #print '_compute_amount'
        if self.sample:
            #self.amount_untaxed = sum(line.price_subtotal for line in self.invoice_line_ids)
            #self.amount_untaxed = 0.01
            self.amount_untaxed = sum((line.quantity * _COST) for line in self.invoice_line_ids)

            #self.amount_tax = sum(line.amount for line in self.tax_line_ids)
            #self.amount_tax = 0.0
            self.amount_tax = sum(line.amount for line in self.tax_line_ids)

            #self.amount_total = self.amount_untaxed + self.amount_tax
            #self.amount_total = 0.01
            self.amount_total = self.amount_untaxed + self.amount_tax

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


    sample = fields.Boolean('Sample')