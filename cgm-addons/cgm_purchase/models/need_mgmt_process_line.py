# -*- coding: utf-8 -*-

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
    price_unit = fields.Monetary('Price Unit', required=False)
    seller_id = fields.Many2one('product.supplierinfo', 'Vendor', required=False)
    company_id = fields.Many2one('res.company', 'Company', required=False)
    need_mgmt_process_id = fields.Many2one('need.mgmt.process', 'Need Mgmt Process', required=True, index=True)
    display_type = fields.Selection([('line_section', 'Section'),
                                     ('line_note', 'Note')], default=False, help='Technical field for UX purpose.')
    incoming_qty = fields.Float('Qty To Receive', digits='Product Unit of Measure', readonly=True)
    outgoing_qty = fields.Float('Qty Ordered', digits='Product Unit of Measure', readonly=True)

    def check_stock(self, from_date=False, to_date=False, warehouse=False):
        """
        Fill stock of the linked product
        :param from_date:
        :param to_date:
        :param warehouse:
        :return:
        """
        if not from_date or not to_date or not warehouse:
            return False
        for line in self:
            qty_available = line.product_id.with_context(from_date=from_date, to_date=to_date, warehouse=warehouse.id).qty_available
            virtual_available = line.product_id.with_context(from_date=from_date, to_date=to_date, warehouse=warehouse.id).virtual_available
            incoming_qty = line.product_id.with_context(from_date=from_date, to_date=to_date, warehouse=warehouse.id).incoming_qty
            outgoing_qty = line.product_id.with_context(from_date=from_date, to_date=to_date, warehouse=warehouse.id).outgoing_qty
            line.write({
                'qty_available': qty_available,
                'virtual_available': virtual_available,
                'incoming_qty': incoming_qty,
                'outgoing_qty': outgoing_qty,
            })
        return True
