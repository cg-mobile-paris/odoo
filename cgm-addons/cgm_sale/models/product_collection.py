# -*- coding: utf-8 -*-
from odoo import models, fields


class ProductCollection(models.Model):
    _name = 'product.collection'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'image.mixin']
    _description = 'Product Collection'

    sequence = fields.Integer('Sequence')
    name = fields.Char('Name', required=True)
    notes = fields.Text('Notes')
    date_start = fields.Date('Date start')
    date_end = fields.Date('Date end')
    active = fields.Boolean('Active', default=True)
