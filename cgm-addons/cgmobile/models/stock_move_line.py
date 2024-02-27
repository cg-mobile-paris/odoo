# -*- coding: utf-8 -*-
from odoo import _, api, fields, models


class StockMoveLine(models.Model):
    _inherit = "stock.move.line"

    sale_company_id = fields.Many2one(string='Order Company', related='picking_id.sale_id.company_id', related_sudo=True, store=True)
    movement_type = fields.Selection([
        ('from_amazon_to_amazon', 'Amazon Internal Movement'),
        ('from_amazon_to_stock', 'Return from Amazon'),
        ('from_amazon_to_customer', 'Shipment from Amazon'),
        ('from_amazon_to_supplier', 'Shipment from Amazon'),
        ('from_amazon_to_other', 'Movement from Amazon to Other'),

        ('from_supplier_to_amazon', 'Amazon Stock from Vendor'),
        ('from_supplier_to_stock', 'Stock from Vendor'),
        ('from_supplier_to_customer', 'Shipment from Vendor'),
        ('from_supplier_to_supplier', 'Inter Vendors ???'),
        ('from_supplier_to_other', 'Movement from Supplier to Other'),

        ('from_customer_to_amazon', 'Amazon Re-Stock from Customer'),
        ('from_customer_to_stock', 'Return from Customer'),
        ('from_customer_to_customer', 'Inter Customers ???'),
        ('from_customer_to_supplier', 'Customer Return to Vendor'),
        ('from_customer_to_other', 'Movement from Customer to Other'),

        ('from_stock_to_amazon', 'Amazon Stock'),
        ('from_stock_to_stock', 'Internal Movement'),
        ('from_stock_to_customer', 'Shipment'),
        ('from_stock_to_supplier', 'Return to Vendor'),
        ('from_stock_to_other', 'Movement from Stock to Other'),

        ('from_other_to_amazon', 'Amazon Stock from Other'),
        ('from_other_to_stock', 'Stock from Other'),
        ('from_other_to_customer', 'Movement from Other to Customer'),
        ('from_other_to_supplier', 'Movement from Other to Supplier'),
        ('from_other_to_other', 'Inter Others ???'),

        ('from_stock_to_customer_auto', 'Auto Shipment'),
        ('from_stock_to_b2b', 'B2B Shipment'),
        ('from_stock_to_b2c', 'B2C Shipment'),
        ], string='Movement Type', default='', index=True, readonly=True, compute='_compute_movement_type', compute_sudo=True, store=True)

    avg_purchase_price = fields.Float(compute='_compute_avg_purchase_price', string='Average Purchase Price', compute_sudo=True, store=True)
    last_purchase_price = fields.Float(string="Last Purchase Price", compute="_compute_last_purchase_price", compute_sudo=True, store=True)

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

    def _get_from_type(self):
        self.ensure_one()
        # FIXME V17
        # if self.location_id.amazon_location:
        #     return 'amazon'
        if self.location_id.usage == 'internal':
            return 'stock'
        elif self.location_id.usage == 'customer':
            return 'customer'
        elif self.location_id.usage == 'supplier':
            return 'supplier'
        else:
            return 'other'

    def _get_to_type(self):
        self.ensure_one()
        # FIXME V17
        # if self.location_dest_id.amazon_location:
        #     return 'amazon'
        if self.location_dest_id.usage == 'internal':
            return 'stock'
        elif self.location_dest_id.usage == 'customer':
            return 'customer'
        elif self.location_dest_id.usage == 'supplier':
            return 'supplier'
        else:
            return 'other'

    @api.depends('location_id', 'location_dest_id')
    def _compute_movement_type(self):
        for line in self:
            movement_type = 'from_' + line._get_from_type() + '_to_' + line._get_to_type()
            if movement_type == 'from_stock_to_customer':
                if line.sale_company_id.id == 1:  # B2B
                    movement_type = 'from_stock_to_b2b'
                elif line.sale_company_id.id == 2:  # B2C
                    movement_type = 'from_stock_to_b2c'
                elif not line.picking_id or not line.picking_id.sale_id:
                    movement_type = 'from_stock_to_customer_auto'
            line.movement_type = movement_type
