# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    form_id = fields.Many2one('product.form', 'Product Form')
    licence_id = fields.Many2one('product.licence', 'Product Licence')
    material_id = fields.Many2one('product.material', 'Product Material')    
    collection_id = fields.Many2one('product.collection', 'Product Collection')
    device_id = fields.Many2one('product.device', 'Product Device')
    brand_id = fields.Many2one('product.brand', 'Product Brand')
    product_type_product = fields.Selection([('export_service', 'Export Service'), ('goods', 'Goods')], 'CGM Product Type')
    royalties_margins = fields.Selection([('yn', 'YN'), ('yy', 'YY'), ('nn', 'NN'), ('ny', 'NY')], 'Royalties & Margins')
    color_id = fields.Many2one('product.color', 'Product Color')

    @api.constrains('default_code')
    def _check_unique_default_code(self):
        for record in self:
            if self.search([('default_code', '!=', False), ('default_code', '=', record.default_code), ('id', '!=', record.id)], limit=1):
                raise ValidationError(_('An item with the same SKU Code already exists in the system.'))
