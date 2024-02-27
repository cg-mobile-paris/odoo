# -*- coding: utf-8 -*-
from odoo import fields, models

class ProductMaterial(models.Model):
    _name = "cgmobile.product_material"
    _description = "Product Material"
    _order = "name"

    name = fields.Char(required=True)
    active = fields.Boolean(default=True)