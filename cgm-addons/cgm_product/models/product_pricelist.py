# -*- coding: UTF-8 -*-

from odoo import fields, models


class ProductPricelist(models.Model):
    _inherit = 'product.pricelist'

    partner_ids = fields.One2many('res.partner', 'property_product_pricelist', 'Partners', required=False)
