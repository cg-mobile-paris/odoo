# -*- coding: utf-8 -*-
from odoo import fields, models, api

class ProductTemplate(models.Model):
    _inherit = "product.template"

    default_code = fields.Char(string='SKU')
    barcode = fields.Char(string='EAN')
    upc_code = fields.Char('UPC', compute='_compute_upc_code', inverse='_set_upc_code', store=True)

    @api.depends('product_variant_ids', 'product_variant_ids.upc_code')
    def _compute_upc_code(self):
        unique_variants = self.filtered(lambda template: len(template.product_variant_ids) == 1)
        for template in unique_variants:
            template.upc_code = template.product_variant_ids.upc_code
        for template in (self - unique_variants):
            template.upc_code = False

    def _set_upc_code(self):
        for template in self:
            if len(template.product_variant_ids) == 1:
                template.product_variant_ids.upc_code = template.upc_code

    product_color_id = fields.Many2one('cgmobile.product_color', string='Color')
    product_category_id = fields.Many2one('cgmobile.product_category', string='Category')
    product_sub_category_id = fields.Many2one('cgmobile.product_sub_category', string='Sub Category')
    product_material_id = fields.Many2one('cgmobile.product_material', string='Material')
    product_protection_level_id = fields.Many2one('cgmobile.product_protection_level', string='Protection Level')
    product_collection_id = fields.Many2one('cgmobile.product_collection', string='Collection')

    device_type_id = fields.Many2one('cgmobile.device_type', string='Device Type')
    device_brand_id = fields.Many2one('common.product.brand.ept', string='Device Brand')
    device_model_id = fields.Many2one('cgmobile.device_model', string='Device Model')
