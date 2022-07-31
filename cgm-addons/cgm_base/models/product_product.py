# -*- coding: utf-8 -*-

from odoo import models


class ProductProduct(models.Model):
    _inherit = 'product.product'

    def name_get(self):
        names = []
        for record in self:
            names.append((record.id, record.default_code or record.name))
        return names
