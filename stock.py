# -*- coding: utf-8 -*-
from openerp import models, fields, api, _
from openerp.exceptions import UserError, RedirectWarning, ValidationError

_COST = 0.01

class StockMove(models.Model):
    _inherit = "stock.move"

    # def _prepare_account_move_line(self, qty, cost, credit_account_id, debit_account_id):
    #     print 'qty: ',qty
    #     print 'cost: ',cost

    #     if self.procurement_id and self.procurement_id.sale_line_id and self.procurement_id.sale_line_id.order_id \
    #     and self.procurement_id.sale_line_id.order_id.sample:
    #         cost = _COST
    #     print 'cost2: ',cost
    #     res = super(StockMove,self)._prepare_account_move_line(qty, cost, credit_account_id, debit_account_id)
    #     #print 'res: ',res

    #     return res

    # def _prepare_account_move_line(self, qty, cost, credit_account_id, debit_account_id):
    #     print 'qty: ',qty
    #     print 'cost: ',cost

    #     if self._context.get('force_valuation_amount'):
    #         print self._context.get('force_valuation_amount')

    #     res = super(StockMove,self)._prepare_account_move_line(qty, cost, credit_account_id, debit_account_id)
    #     #print 'res: ',res

    #     if self.procurement_id and self.procurement_id.sale_line_id and self.procurement_id.sale_line_id.order_id \
    #     and self.procurement_id.sale_line_id.order_id.sample:
    #         #print 'is sample'
    #         for x in res:
    #             if len(x) >= 3 and x[2]:
    #                 if x[2]['debit'] != 0:
    #                     print 'debit'
    #                     x[2]['debit'] = 0.01
    #                 if x[2]['credit'] != 0:
    #                     print 'credit'
    #                     x[2]['credit'] = 0.01
    #     return res

    # def _prepare_account_move_line(self, qty, cost, credit_account_id, debit_account_id):

    #     res = super(StockMove,self)._prepare_account_move_line(qty, cost, credit_account_id, debit_account_id)
    #     #print 'res: ',res

    #     if self.procurement_id and self.procurement_id.sale_line_id and self.procurement_id.sale_line_id.order_id \
    #     and self.procurement_id.sale_line_id.order_id.sample:
    #         #print 'is sample'
           
    #         valuation_amount = _COST
    #         value = self.company_id.currency_id.round(valuation_amount * qty)

    #         for x in res:
    #             if len(x) >= 3 and x[2]:
    #                 if x[2]['debit'] != 0:
    #                     print 'debit'
    #                     x[2]['debit'] = value
    #                 if x[2]['credit'] != 0:
    #                     print 'credit'
    #                     x[2]['credit'] = value
    #     return res

    # def _prepare_account_move_line(self, qty, cost, credit_account_id, debit_account_id):
    #     """
    #     Generate the account.move.line values to post to track the stock valuation difference due to the
    #     processing of the given quant.
    #     """
    #     self.ensure_one()
    #     cost = .01
    #     if self._context.get('force_valuation_amount'):
    #         print '1'
    #         valuation_amount = self._context.get('force_valuation_amount')
    #     else:
    #         if self.product_id.cost_method == 'average':
    #             print '2'
    #             valuation_amount = cost if self.location_id.usage == 'supplier' and self.location_dest_id.usage == 'internal' else self.product_id.standard_price
    #         else:
    #             print '3'
    #             valuation_amount = cost if self.product_id.cost_method == 'real' else self.product_id.standard_price
    #     # the standard_price of the product may be in another decimal precision, or not compatible with the coinage of
    #     # the company currency... so we need to use round() before creating the accounting entries.
    #     print 'valuation_amount: ',valuation_amount
    #     debit_value = self.company_id.currency_id.round(valuation_amount * qty)
    #     print 'debit_value: ',debit_value

    #     # check that all data is correct
    #     if self.company_id.currency_id.is_zero(debit_value):
    #         if self.product_id.cost_method == 'standard':
    #             raise UserError(_("The found valuation amount for product %s is zero. Which means there is probably a configuration error. Check the costing method and the standard price") % (self.product_id.name,))
    #         return []
    #     credit_value = debit_value

    #     if self.product_id.cost_method == 'average' and self.company_id.anglo_saxon_accounting:
    #         # in case of a supplier return in anglo saxon mode, for products in average costing method, the stock_input
    #         # account books the real purchase price, while the stock account books the average price. The difference is
    #         # booked in the dedicated price difference account.
    #         if self.location_dest_id.usage == 'supplier' and self.origin_returned_move_id and self.origin_returned_move_id.purchase_line_id:
    #             debit_value = self.origin_returned_move_id.price_unit * qty
    #         # in case of a customer return in anglo saxon mode, for products in average costing method, the stock valuation
    #         # is made using the original average price to negate the delivery effect.
    #         if self.location_id.usage == 'customer' and self.origin_returned_move_id:
    #             debit_value = self.origin_returned_move_id.price_unit * qty
    #             credit_value = debit_value
    #     partner_id = (self.picking_id.partner_id and self.env['res.partner']._find_accounting_partner(self.picking_id.partner_id).id) or False
    #     debit_line_vals = {
    #         'name': self.name,
    #         'product_id': self.product_id.id,
    #         'quantity': qty,
    #         'product_uom_id': self.product_id.uom_id.id,
    #         'ref': self.picking_id.name,
    #         'partner_id': partner_id,
    #         'debit': debit_value,
    #         'credit': 0,
    #         'account_id': debit_account_id,
    #     }
    #     credit_line_vals = {
    #         'name': self.name,
    #         'product_id': self.product_id.id,
    #         'quantity': qty,
    #         'product_uom_id': self.product_id.uom_id.id,
    #         'ref': self.picking_id.name,
    #         'partner_id': partner_id,
    #         'credit': credit_value,
    #         'debit': 0,
    #         'account_id': credit_account_id,
    #     }
    #     print 'credit_value: ',credit_value
    #     print 'debit_value: ',debit_value
    #     res = [(0, 0, debit_line_vals), (0, 0, credit_line_vals)]
    #     if credit_value != debit_value:
    #         # for supplier returns of product in average costing method, in anglo saxon mode
    #         diff_amount = debit_value - credit_value
    #         price_diff_account = self.product_id.property_account_creditor_price_difference
    #         if not price_diff_account:
    #             price_diff_account = self.product_id.categ_id.property_account_creditor_price_difference_categ
    #         if not price_diff_account:
    #             raise UserError(_('Configuration error. Please configure the price difference account on the product or its category to process this operation.'))
    #         price_diff_line = {
    #             'name': self.name,
    #             'product_id': self.product_id.id,
    #             'quantity': qty,
    #             'product_uom_id': self.product_id.uom_id.id,
    #             'ref': self.picking_id.name,
    #             'partner_id': partner_id,
    #             'credit': diff_amount > 0 and diff_amount or 0,
    #             'debit': diff_amount < 0 and -diff_amount or 0,
    #             'account_id': price_diff_account.id,
    #         }
    #         res.append((0, 0, price_diff_line))
    #     return res
