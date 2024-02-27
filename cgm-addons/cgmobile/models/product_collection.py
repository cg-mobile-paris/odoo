# -*- coding: utf-8 -*-
from odoo import fields, models

class ProductProtectionLevel(models.Model):
    _name = "cgmobile.product_collection"
    _description = "Product Collection"
    _order = "name"

    name = fields.Char(required=True)
    active = fields.Boolean(default=True)