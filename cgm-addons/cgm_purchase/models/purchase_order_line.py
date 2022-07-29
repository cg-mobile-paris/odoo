# -*- coding: utf-8 -*-

from odoo import models, fields, api


class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    qty_available = fields.Float('Available quantity', related='product_id.qty_available', store=True)
    virtual_available = fields.Float('Projected quantity', related='product_id.virtual_available', store=True)
    qty_expected = fields.Float('Expected quantity', compute='_compute_expected_qty', store=True)

    @api.depends('product_qty', 'virtual_available')
    def _compute_expected_qty(self):
        for rec in self:
            domain = [('product_id', '=', rec.product_id.id), ('order_id.state', 'in', ('draft', 'sent', 'to approve'))]
            order_line_qty = sum(self.env['purchase.order.line'].search(domain).mapped('product_qty'))
            rec.qty_expected = order_line_qty + rec.virtual_available
