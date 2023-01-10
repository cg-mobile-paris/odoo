# -*- coding: utf-8 -*-

from odoo import models

class SaleAdvancePaymentInv(models.TransientModel):
    _inherit = "sale.advance.payment.inv"

    def _prepare_invoice_values(self, order, name, amount, so_line):
        res = super(SaleAdvancePaymentInv, self)._prepare_invoice_values(order, name, amount, so_line)
        res['partner_bank_id'] = order.bank_id.id or order.company_id.partner_id.bank_ids[:1].id
        return res