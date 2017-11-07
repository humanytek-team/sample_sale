# -*- coding: utf-8 -*-
from openerp import models, fields, api, _
from openerp.exceptions import UserError, RedirectWarning, ValidationError


class StockMove(models.Model):
    _inherit = "stock.move"

    def _prepare_account_move_line(self, qty, cost, credit_account_id, debit_account_id):
        res = super(StockMove,self)._prepare_account_move_line(qty, cost, credit_account_id, debit_account_id)
        #print 'res: ',res

        if self.procurement_id and self.procurement_id.sale_line_id and self.procurement_id.sale_line_id.order_id \
        and self.procurement_id.sale_line_id.order_id.sample:
            #print 'is sample'
            for x in res:
                if len(x) >= 3 and x[2]:
                    if x[2]['debit'] != 0:
                        print 'debit'
                        x[2]['debit'] = 0.01
                    if x[2]['credit'] != 0:
                        print 'credit'
                        x[2]['credit'] = 0.01
        return res

