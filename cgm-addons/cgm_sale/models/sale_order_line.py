# -*- coding: utf-8 -*-

from odoo import models, fields


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    image = fields.Image('Thumbnail', related='product_id.image_1920', store=True)
