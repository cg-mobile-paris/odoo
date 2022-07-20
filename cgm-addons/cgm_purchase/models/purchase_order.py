# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    licence_id = fields.Many2one('product.licence', 'Licence')
    device_ids = fields.Many2many('product.device', 'purchase_order_product_device_rel', 'order_id', 'device_id', 'Devices', readonly=True)
    type = fields.Selection([('state_of_needs', 'State of needs'), ('quotation', 'Request for quotation')], 'Type', default='quotation')

    @api.onchange('licence_id')
    def _onchange_licence_id(self):
        """
        Load products according to the selected licence
        :return: None
        """
        if not self.licence_id:
            return {}
        self.update({'order_line': [(6, 0, [])], 'device_ids': [(6, 0, [])]})
        products = self.licence_id.product_ids
        if not products:
            return {}

        device_summary = {}
        for product in products:
            device_summary.setdefault(product.device_id, []).append(product)

        order_lines = []
        devices = self.env['product.device']
        for device, products in device_summary.items():
            order_lines.append((0, 0, {'display_type': 'line_section', 'name': device.name or _('Indefinite')}))
            for product in products:
                order_lines.append((0, 0, {'product_id': product.id, 'product_qty': 1.0}))
            devices += device

        self.update({'order_line': order_lines, 'device_ids': [(6, 0, devices.ids)]})

        for line in self.order_line:
            line.onchange_product_id()

        return {}


class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    qty_available = fields.Float('Available quantity', related='product_id.qty_available')
    virtual_available = fields.Float('Projected quantity', related='product_id.virtual_available')
    qty_expected = fields.Float('Expected quantity', compute='_compute_expected_qty', store=True)

    @api.depends('product_qty', 'virtual_available')
    def _compute_expected_qty(self):
        for rec in self:
            domain = [('product_id', '=', rec.product_id.id), ('order_id.state', 'in', ('draft', 'sent', 'to approve'))]
            order_line_qty = sum(self.env['purchase.order.line'].search(domain).mapped('product_qty'))
            rec.qty_expected = order_line_qty + rec.virtual_available
