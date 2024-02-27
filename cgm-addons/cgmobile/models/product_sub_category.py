# -*- coding: utf-8 -*-
from odoo import fields, models

class ProductSubCategory(models.Model):
    _name = "cgmobile.product_sub_category"
    _description = "Product Sub Category"
    _order = "category_id, name"

    name = fields.Char(required=True)
    active = fields.Boolean(default=True)
    category_id = fields.Many2one('cgmobile.product_category', string='Category', required=True)
