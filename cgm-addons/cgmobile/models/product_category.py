# -*- coding: utf-8 -*-
from odoo import fields, models

class ProductCategory(models.Model):
    _name = "cgmobile.product_category"
    _description = "Product Category"
    _order = "name"

    name = fields.Char(required=True)
    active = fields.Boolean(default=True)