# -*- coding : UTF-8 -*-


from odoo import fields, models, api


class AccountMove(models.Model):
    _inherit = 'account.move'

    total_qty = fields.Float('Total Qty', compute='_compute_total_qty', digits='Product Unit of Measure', store=True)

    @api.depends('invoice_line_ids', 'invoice_line_ids.quantity')
    def _compute_total_qty(self):
        for move in self:
            move.total_qty = sum(move.invoice_line_ids.mapped('quantity'))
