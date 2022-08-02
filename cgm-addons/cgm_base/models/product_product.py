# -*- coding: utf-8 -*-

from odoo import models, api


class ProductProduct(models.Model):
    _inherit = 'product.product'

    def name_get(self):
        names = []
        for record in self:
            names.append((record.id, record.default_code or record.name))
        return names

    @api.depends_context('partner_id')
    def _compute_partner_ref(self):
        for product in self:
            for supplier_info in product.seller_ids:
                if supplier_info.name.id == product._context.get('partner_id'):
                    product_name = supplier_info.product_name or product.default_code or product.name
                    product.partner_ref = '%s%s' % (product.code and '[%s] ' % product.code or '', product_name)
                    break
            else:
                product.partner_ref = product.name
