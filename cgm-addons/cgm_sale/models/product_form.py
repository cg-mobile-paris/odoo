# -*- coding: utf-8 -*-
from odoo import models, fields


class ProductForm(models.Model):
    _name = 'product.form'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Product Form'

    sequence = fields.Integer('Sequence')
    name = fields.Char('Name', required=True)
    notes = fields.Text('Notes')
    active = fields.Boolean('Active', default=True)
