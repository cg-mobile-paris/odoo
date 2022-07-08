# -*- coding: utf-8 -*-

from odoo import models, fields


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    form_id = fields.Many2one('product.form', 'Product Form')
