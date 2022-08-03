# -*- coding: utf-8 -*-

from odoo import models


class ProductProduct(models.Model):
    _inherit = 'product.product'

    def get_product_multiline_description_sale(self):
        """
        Override to adapt the product name according to the CGM need
        :return:
        """
        name = self.name
        if self.description_sale:
            name += '\n' + self.description_sale
        return name
