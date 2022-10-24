# -*- coding: utf-8 -*-
from odoo import models, fields


class ProductColor(models.Model):
    _name = 'product.color'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Product Color'

    sequence = fields.Integer('Sequence')
    name = fields.Char('Name', required=True)
    color = fields.Char('Color')
