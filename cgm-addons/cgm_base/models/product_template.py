# -*- coding: utf-8 -*-

from odoo import models


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    def name_get(self):
        names = []
        for record in self:
            names.append((record.id, record.default_code or record.name))
        return names
