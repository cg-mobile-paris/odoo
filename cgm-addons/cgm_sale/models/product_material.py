# -*- coding: utf-8 -*-

from odoo import models, fields


class ProductMaterial(models.Model):
    _name = 'product.material'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Product Material'

    sequence = fields.Integer('Sequence')
    name = fields.Char('Name', required=True)
    notes = fields.Text('Notes')
    active = fields.Boolean('Active', default=True)
