# -*- coding: utf-8 -*-

from odoo import models, fields, api


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    need_mgmt_process_id = fields.Many2one('need.mgmt.process', 'Need Mgmt Process', required=False)
    total_qty = fields.Float('Total Qty', compute='_compute_total_qty', digits='Product Unit of Measure', store=True)

    @api.depends('order_line.product_qty')
    def _compute_total_qty(self):
        for order in self:
            order.total_qty = sum(order.order_line.mapped('product_qty'))
