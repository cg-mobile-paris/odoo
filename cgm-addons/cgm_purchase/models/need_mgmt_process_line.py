# -*- coding: utf-8 -*-

from odoo import fields, models, _
from odoo.exceptions import ValidationError


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
    physical_qty = fields.Float('Physical Qty', digits='Product Unit of Measure', readonly=True)
    available_qty = fields.Float('Available Qty', digits='Product Unit of Measure', readonly=True)
    price_unit = fields.Monetary('Price Unit', required=False)
    seller_id = fields.Many2one('product.supplierinfo', 'Vendor', required=False)
    company_id = fields.Many2one('res.company', 'Company', required=False)
    need_mgmt_process_id = fields.Many2one('need.mgmt.process', 'Need Mgmt Process', required=True, index=True)
    display_type = fields.Selection([('line_section', 'Section'),
                                     ('line_note', 'Note')], default=False, help='Technical field for UX purpose.')
    incoming_qty = fields.Float('Qty To Receive', digits='Product Unit of Measure', readonly=True)
    outgoing_qty = fields.Float('Qty Ordered', digits='Product Unit of Measure', readonly=True)
    projected_qty = fields.Float('Projected Qty', digits='Product Unit of Measure', readonly=True)

    def check_stock(self, warehouse=False):
        """
        Fill stock of the linked product
        :param warehouse:
        :return:
        """
        if not warehouse:
            raise ValidationError(_('Warehouse is required to process this action!'))
        for line in self:
            physical_qty = line.product_id.with_context(warehouse=warehouse.id).qty_available
            outgoing_qty = line.product_id.with_context(warehouse=warehouse.id).outgoing_qty
            available_qty = physical_qty - outgoing_qty
            incoming_qty = line.product_id.with_context(warehouse=warehouse.id).incoming_qty
            projected_qty = available_qty + incoming_qty

            line.write({
                'physical_qty': physical_qty,
                'outgoing_qty': outgoing_qty,
                'available_qty': available_qty,
                'incoming_qty': incoming_qty,
                'projected_qty': projected_qty
            })
        return True
