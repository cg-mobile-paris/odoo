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
    upc_code = fields.Char('UPC Code')

    @api.constrains('default_code')
    def _check_unique_default_code(self):
        for record in self:
            if self.search([('default_code', '!=', False), ('default_code', '=', record.default_code), ('id', '!=', record.id)], limit=1):
                raise ValidationError(_('An item with the same SKU Code already exists in the system.'))

    @api.constrains('barcode')
    def _check_unique_barcode(self):
        for record in self:
            if self.search([('barcode', '!=', False), ('barcode', '=', record.barcode), ('id', '!=', record.id)], limit=1):
                raise ValidationError(_('An item with the same EAN Code already exists in the system.'))

    @api.depends_context('company')
    def _compute_cost_currency_id(self):
        """
            Override to force the currency to USD for all products
        :return:
        """
        for template in self:
            template.cost_currency_id = self.env.ref('base.USD', raise_if_not_found=False).id

    @api.depends('company_id')
    def _compute_currency_id(self):
        """
            Override to force the currency to USD for all products
        :return:
        """
        for template in self:
            template.currency_id = self.env.ref('base.USD', raise_if_not_found=False).id
