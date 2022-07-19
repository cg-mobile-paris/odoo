# -*- coding: utf-8 -*-

from odoo import models, fields

PRODUCT_TYPE = [('export_service', 'Export Service'), ('goods', 'Goods')]
ROYALTIES_MARGINS = [('yn', 'YN'), ('yy', 'YY'), ('nn', 'NN'), ('ny', 'NY')]


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    form_id = fields.Many2one('product.form', 'Product Form')
    licence_id = fields.Many2one('product.licence', 'Product Licence')
    material_id = fields.Many2one('product.material', 'Product Material')    
    collection_id = fields.Many2one('product.collection', 'Product Collection')
    device_id = fields.Many2one('product.device', 'Product Device')
    brand_id = fields.Many2one('product.brand', 'Product Brand')
    product_type_product = fields.Selection(PRODUCT_TYPE, 'CGM Product Type')
    royalties_margins = fields.Selection(ROYALTIES_MARGINS, 'Royalties & Margins')
    upc_code = fields.Char('UPC Code')
    color_id = fields.Many2one('product.color', 'Product Color')

    _sql_constraints = [
        ('unique_default_code', 'UNIQUE (default_code)', 'An item with the same SKU Code already exists in the system.')
    ]
