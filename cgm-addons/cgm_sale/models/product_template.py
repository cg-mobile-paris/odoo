# -*- coding: utf-8 -*-
from odoo import models, fields


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    licence_id = fields.Many2one('product.licence', 'Licence')
