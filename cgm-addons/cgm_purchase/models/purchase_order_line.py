# -*- coding: utf-8 -*-

from odoo import models, fields, api, SUPERUSER_ID


class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    qty_available = fields.Float('Available quantity', related='product_id.qty_available', store=True)
    virtual_available = fields.Float('Projected quantity', related='product_id.virtual_available', store=True)
    qty_expected = fields.Float('Expected quantity', compute='_compute_expected_qty', store=True)
    barcode = fields.Char('EAN Code', related='product_id.barcode', store=True)

    @api.depends('product_qty', 'virtual_available')
    def _compute_expected_qty(self):
        for rec in self:
            domain = [('product_id', '=', rec.product_id.id), ('order_id.state', 'in', ('draft', 'sent', 'to approve'))]
            order_line_qty = sum(self.env['purchase.order.line'].search(domain).mapped('product_qty'))
            rec.qty_expected = order_line_qty + rec.virtual_available

    def _get_product_purchase_description(self, product_lang):
        """
        Override to set line name according to CGM constrains
        :param product_lang:
        :return:
        """
        self.ensure_one()
        name = product_lang.name
        if product_lang.description_purchase:
            name += '\n' + product_lang.description_purchase
        return name

    @api.model
    def create(self, vals):
        product_id = vals.get('product_id')
        if product_id:
            product = self.env['product.product'].browse(product_id)
            if product and product.name:
                vals['name'] = product.name
        return super().create(vals)

    # def migrate(cr, registry):
    #     env = api.Environment(cr, SUPERUSER_ID, {})
    #     purchase_order_lines = env['purchase.order.line'].search([])
    #     for line in purchase_order_lines:
    #         line.name = line.product_id.name




