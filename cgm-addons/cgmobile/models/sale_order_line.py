# -*- coding: utf-8 -*-
from odoo import _, api, fields, models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    last_purchase_price = fields.Float(string="Last Purchase Price", compute="_compute_last_purchase_price", compute_sudo=True, store=True)

    @api.depends("product_id", "order_id.state")
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