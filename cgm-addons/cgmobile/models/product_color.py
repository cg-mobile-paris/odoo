# -*- coding: utf-8 -*-
from odoo import fields, models

class ProductColor(models.Model):
    _name = "cgmobile.product_color"
    _description = "Product Color"
    _order = "name"

    name = fields.Char(required=True)
    active = fields.Boolean(default=True)