# -*- coding: utf-8 -*-
from openerp import models, fields, api, _
from openerp.exceptions import UserError, RedirectWarning, ValidationError


class SaleOrder(models.Model):
    _inherit = "sale.order"


    @api.multi
    def _prepare_invoice(self):
        #print '_prepare_invoice'
        self.ensure_one()
        invoice_vals = super(SaleOrder,self)._prepare_invoice()
        invoice_vals['sample'] = self.sample
        #print 'end'
        return invoice_vals


    @api.depends('order_line.price_total','sample')
    def _amount_all(self):
        #print '_amount_all'
        #CHECKS IF SALE ORDER IS SAMPLE
        if self.sample:
            for order in self:
                order.update({
                    'amount_untaxed': .01,
                    'amount_tax': 0,
                    'amount_total': .01,
                })
        else:
            super(SaleOrder,self)._amount_all()
        #print 'end'


    sample = fields.Boolean('Sample', help='if checked, sale order total amount will be 0.01')