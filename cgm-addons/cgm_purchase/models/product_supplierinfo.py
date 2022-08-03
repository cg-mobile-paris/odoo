# -*- coding: utf-8 -*-

from odoo import models, api


class ProductSupplierinfo(models.Model):
    _inherit = 'product.supplierinfo'

    @api.model
    def _search(self, args, offset=0, limit=None, order=None, count=False, access_rights_uid=None):
        if self._context.get('filter_by_product'):
            product = self.env['product.product'].browse(self._context.get('filter_by_product'))
            args += [('product_tmpl_id', '=', product.product_tmpl_id.id)]
        return super(ProductSupplierinfo, self)._search(args, offset=offset, limit=limit,
                                                        order=order, count=count, access_rights_uid=access_rights_uid)
