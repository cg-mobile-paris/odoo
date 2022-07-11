# -*- coding: utf-8 -*-
from odoo import models, fields


class ProductLicence(models.Model):
    _name = 'product.licence'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'image.mixin']
    _description = 'Product Licence'

    sequence = fields.Integer('Sequence')
    name = fields.Char('Name', required=True)
    notes = fields.Text('Notes')
    active = fields.Boolean('Active', default=True)

