# -*- coding: utf-8 -*-
from openerp import models, fields, api, _
from openerp.exceptions import UserError, RedirectWarning, ValidationError

_COST = 1


class SaleOrder(models.Model):
    _inherit = "sale.order"


    @api.multi
    @api.onchange('sample')
    def onchange_sample(self):
        for order in self:
            if order.order_line:
                if order.sample:
                    for line in order.order_line:
                        line.price_unit = _COST
                else:
                    for line in order.order_line:
                        line.price_unit = line.product_id.lst_price

    sample = fields.Boolean('Sample')


    @api.multi
    def _prepare_invoice(self):
        #print '_prepare_invoice'
        self.ensure_one()
        invoice_vals = super(SaleOrder,self)._prepare_invoice()
        invoice_vals['sample'] = self.sample
        #print 'end'
        return invoice_vals



    # @api.depends('order_line.price_total','sample')
    # def _amount_all(self):
    #     #print '_amount_all'
    #     #CHECKS IF SALE ORDER IS SAMPLE
    #     if self.sample:
    #         for order in self:
    #             order.update({
    #                 'amount_untaxed': .01,
    #                 'amount_tax': 0,
    #                 'amount_total': .01,
    #             })
    #     else:
    #         super(SaleOrder,self)._amount_all()
    #     #print 'end'

    # @api.depends('order_line.price_total','sample')
    # def _amount_all(self):
    #     print '_amount_all'
        
    #     #CHECKS IF SALE ORDER IS SAMPLE
    #     if self.sample:
    #         for order in self:
    #             amount_untaxed = amount_tax = 0.0
    #             for line in order.order_line:

    #                 #amount_untaxed += line.price_subtotal
    #                 amount_untaxed += (line.product_uom_qty * _COST)

    #                 # FORWARDPORT UP TO 10.0
    #                 if order.company_id.tax_calculation_rounding_method == 'round_globally':

    #                     #price = line.price_unit * (1 - (line.discount or 0.0) / 100.0)
    #                     price = _COST * (1 - (line.discount or 0.0) / 100.0)

    #                     taxes = line.tax_id.compute_all(price, line.order_id.currency_id, line.product_uom_qty, product=line.product_id, partner=order.partner_shipping_id)
    #                     amount_tax += sum(t.get('amount', 0.0) for t in taxes.get('taxes', []))
    #                 else:
    #                     amount_tax += line.price_tax
    #             order.update({
    #                 'amount_untaxed': order.pricelist_id.currency_id.round(amount_untaxed),
    #                 'amount_tax': order.pricelist_id.currency_id.round(amount_tax),
    #                 'amount_total': amount_untaxed + amount_tax,
    #             })
    #     else:
    #         super(SaleOrder,self)._amount_all()


# class SaleOrderLine(models.Model):
#     _inherit = 'sale.order.line'


#     @api.depends('product_uom_qty', 'discount', 'price_unit', 'tax_id', 'order_id.sample')
#     def _compute_amount(self):
#         print '_compute_amount'
#         super(SaleOrderLine,self)._compute_amount()
#         for line in self:
#             if line.order_id.sample:
#                 #price = line.price_unit * (1 - (line.discount or 0.0) / 100.0)
#                 price = _COST * (1 - (line.discount or 0.0) / 100.0)
#                 taxes = line.tax_id.compute_all(price, line.order_id.currency_id, line.product_uom_qty, product=line.product_id, partner=line.order_id.partner_shipping_id)
#                 line.update({
#                     'price_tax': taxes['total_included'] - taxes['total_excluded'],
#                     'price_total': taxes['total_included'],
#                     'price_subtotal': taxes['total_excluded'],
#                 })

    # @api.depends('product_uom_qty', 'discount', 'price_unit', 'tax_id')
    # def _compute_amount(self):
    #     """
    #     Compute the amounts of the SO line.
    #     """
    #     for line in self:
    #         price = line.price_unit * (1 - (line.discount or 0.0) / 100.0)
    #         taxes = line.tax_id.compute_all(price, line.order_id.currency_id, line.product_uom_qty, product=line.product_id, partner=line.order_id.partner_shipping_id)
    #         line.update({
    #             'price_tax': taxes['total_included'] - taxes['total_excluded'],
    #             'price_total': taxes['total_included'],
    #             'price_subtotal': taxes['total_excluded'],
    #         })
