# -*- coding: utf-8 -*-
from odoo import models, fields


class ProductBrand(models.Model):
    _name = 'product.brand'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Product Brand'

    sequence = fields.Integer('Sequence')
    name = fields.Char('Name', required=True)
    notes = fields.Text('Notes')
    active = fields.Boolean('Active', default=True)
