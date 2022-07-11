# -*- coding: utf-8 -*-
from odoo import models, fields


class ProductDevice(models.Model):
    _name = 'product.device'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Product Device'

    sequence = fields.Integer('Sequence')
    name = fields.Char('Name', required=True)
    notes = fields.Text('Notes')
    active = fields.Boolean('Active', default=True)
