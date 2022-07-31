# -*- coding: utf-8 -*-

from odoo import api, fields, models


class NeedMgmtProcessLine(models.Model):
    _name = 'need.mgmt.process.line'
    _description = 'Need Management Process Line'

    name = fields.Char(required=False)
    sequence = fields.Integer('Sequence', default=10)
    currency_id = fields.Many2one(related='need_mgmt_process_id.currency_id')
    product_id = fields.Many2one('product.product', 'Product', required=False)
    image = fields.Image('Thumbnail', related='product_id.image_1920', store=True)
    barcode = fields.Char('EAN Code', related='product_id.barcode', store=True)
    product_qty = fields.Float('Product Qty To Order', required=False)
    qty_available = fields.Float('Available Quantity', readonly=True)
    virtual_available = fields.Float('Projected Quantity', readonly=True)
    qty_expected = fields.Float('Expected Quantity', readonly=True)
    price_unit = fields.Monetary('Price Unit', required=False)
    seller_id = fields.Many2one('product.supplierinfo', 'Vendor', equired=False)
    company_id = fields.Many2one('res.company', 'Company', required=False)
    need_mgmt_process_id = fields.Many2one('need.mgmt.process', 'Need Mgmt Process', required=True, index=True)
    display_type = fields.Selection([('line_section', 'Section'),
                                     ('line_note', 'Note')], default=False, help='Technical field for UX purpose.')

    def check_stock(self):
        """
        Fill stock of the linked product
        :return:
        """
        for line in self:
            line.write({
                'qty_available': line.product_id.qty_available,
                'virtual_available': line.product_id.virtual_available,
                'qty_expected': 10,  # TODO: to be defined
            })
