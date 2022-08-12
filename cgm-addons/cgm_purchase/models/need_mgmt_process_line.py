# -*- coding: utf-8 -*-

from dateutil.relativedelta import relativedelta

from odoo import fields, models


class NeedMgmtProcessLine(models.Model):
    _name = 'need.mgmt.process.line'
    _description = 'Need Management Process Line'

    name = fields.Char(required=False)
    sequence = fields.Integer('Sequence', default=10)
    currency_id = fields.Many2one(related='need_mgmt_process_id.currency_id')
    product_id = fields.Many2one('product.product', 'Product', required=False)
    image = fields.Image('Thumbnail', related='product_id.image_1920', store=True)
    barcode = fields.Char('EAN Code', related='product_id.barcode', store=True)
    product_qty = fields.Float('Qty To Order', digits='Product Unit of Measure', required=False)
    qty_available = fields.Float('Physical Qty', digits='Product Unit of Measure', readonly=True)
    virtual_available = fields.Float('Available Qty', digits='Product Unit of Measure', readonly=True)
    qty_projected = fields.Float('Projected Qty', digits='Product Unit of Measure', readonly=True)
    price_unit = fields.Monetary('Price Unit', required=False)
    seller_id = fields.Many2one('product.supplierinfo', 'Vendor', required=False)
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
            to_date = line.need_mgmt_process_id.date + relativedelta(days=line.need_mgmt_process_id.number_of_days)
            qty_available = line.product_id.with_context(from_date=line.need_mgmt_process_id.date, to_date=to_date).qty_available
            virtual_available = line.product_id.with_context(from_date=line.need_mgmt_process_id.date, to_date=to_date).virtual_available
            line.write({
                'qty_available': qty_available,
                'virtual_available': virtual_available,
                'qty_projected': 0,
            })
