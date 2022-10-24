# -*- coding: utf-8 -*-

from odoo import fields, models


class SaleOrderTemplateLine(models.Model):
    _inherit = 'sale.order.template.line'

    state = fields.Selection(related='sale_order_template_id.state', store=True)
    image = fields.Image('Thumbnail', related='product_id.image_1920', store=True)
    barcode = fields.Char('EAN Code', related='product_id.barcode', store=True)
