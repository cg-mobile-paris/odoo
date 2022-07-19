# -*- coding: UTF-8 -*-
import json

from itertools import groupby
from collections import deque
from odoo import models, fields, api
from odoo.osv.expression import AND

TYPE = [('state_of_needs', 'State of needs'), ('quotation', 'Request for quotation')]


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    licence_id = fields.Many2one('product.licence', 'Licence')
    device_ids = fields.Many2many('product.device', 'device_id_order_id', 'device_id', 'order_id', 'Devices',
                                  readonly=True)
    type = fields.Selection(TYPE, 'Type', default='quotation')

    @api.onchange('licence_id')
    def on_change_licence_id(self):
        """
        set order_line and device when licence changed
        :return: None
        """
        if not self.licence_id:
            self.write({'order_line': [(5, 0, 0)], 'device_ids': [(5, 0, 0)]})
            return

        product_ids = self.env["product.product"].search([('licence_id', '=', self.licence_id.id)])
        if not product_ids:
            self.write({'order_line': [(5, 0, 0)], 'device_ids': [(5, 0, 0)]})
            return

        order_line_values = []
        device_ids = self.env["product.device"]

        def by_device_id():
            return lambda r: r.device_id.id

        for device, products in groupby(sorted(product_ids, key=by_device_id()), by_device_id()):
            temp = deque()
            device_id = self.env["product.device"].browse(device)
            device_ids += device_id
            for product_id in products:
                val = (0, 0, {
                    'product_id': product_id.id,
                    'product_qty': 1.0,
                })
                temp.append(val)

            temp.appendleft((0, 0, {'display_type': 'line_section', 'name': device_id.name}))
            order_line_values.extend(temp)

        self.write({'order_line': order_line_values, 'device_ids': [(6, 0, device_ids.ids)]})
        # trigger onchange
        for ol in self.order_line:
            ol.onchange_product_id()

    def confirm_state_of_orders(self):
        self.write({'type': 'quotation'})


class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    product_domain = fields.Char(compute='_compute_product_id_domain')

    @api.depends('order_id.licence_id')
    def _compute_product_id_domain(self):
        for rec in self:
            domain = [('purchase_ok', '=', True), '|', ('company_id', '=', False),
                      ('company_id', '=', rec.order_id.company_id.id)]
            if rec.order_id.licence_id:
                domain = AND([[('licence_id', '=', rec.order_id.licence_id.id)], domain])
            rec.product_domain = json.dumps(domain)
