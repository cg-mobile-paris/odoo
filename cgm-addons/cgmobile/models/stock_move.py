# -*- coding: utf-8 -*-
from odoo import _, api, fields, models


class StockMove(models.Model):
    _inherit = "stock.move"

    avg_purchase_price = fields.Float(compute='_compute_avg_purchase_price', string='Average Purchase Price', compute_sudo=True, store=True)
    last_purchase_price = fields.Float(string="Last Purchase Price", compute="_compute_last_purchase_price", compute_sudo=True, store=True)

    qty_to_receive = fields.Float(compute='_compute_qty_to_receive', string='Qty to Receive', store=True, compute_sudo=True)

    @api.depends('product_id', 'state')
    def _compute_last_purchase_price(self):
        for rec in self:
            if rec.product_id:
                last_purchase_price = (
                    self.env["purchase.order.line"]
                    .search(
                        [
                            ("company_id", "=", rec.company_id.id),
                            ("product_id", "=", rec.product_id.id),
                            ("order_id.state", "in", ["purchase", "done"]),
                        ],
                        order="id desc",
                        limit=1,
                    )
                    .price_unit
                )
                rec.last_purchase_price = last_purchase_price

    @api.depends('product_id', 'state')
    def _compute_avg_purchase_price(self):
        for line in self:
            if not line.product_id:
                line.avg_purchase_price = 0.0
                continue
            line = line.with_company(line.company_id)
            product = line.product_id
            product_cost = product.standard_price
            if not product_cost:
                if not line.avg_purchase_price:
                    line.avg_purchase_price = 0.0
            else:
                line.avg_purchase_price = product_cost

    @api.depends('product_id', 'quantity', 'product_uom_qty')
    def _compute_qty_to_receive(self):
        for line in self:
            if line.product_id:
                line.qty_to_receive = line.product_uom_qty - line.quantity
