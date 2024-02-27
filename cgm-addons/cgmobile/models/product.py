# -*- coding: utf-8 -*-
from odoo import fields, models, api

class ProductProduct(models.Model):
    _inherit = "product.product"

    default_code = fields.Char(string='SKU')
    barcode = fields.Char(string='EAN')
    upc_code = fields.Char('UPC')