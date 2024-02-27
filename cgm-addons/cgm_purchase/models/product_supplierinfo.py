# -*- coding: utf-8 -*-

from odoo import models, api


class ProductSupplierinfo(models.Model):
    _inherit = 'product.supplierinfo'

    @api.model
    def _search(self, domain, offset=0, limit=None, order=None, access_rights_uid=None):
        if self._context.get('filter_by_product'):
            product = self.env['product.product'].browse(self._context.get('filter_by_product'))
            domain += [('product_tmpl_id', '=', product.product_tmpl_id.id)]
        return super(ProductSupplierinfo, self)._search(domain, offset=offset, limit=limit,
                                                        order=order, access_rights_uid=access_rights_uid)
