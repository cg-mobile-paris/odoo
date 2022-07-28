# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    licence_id = fields.Many2one('product.licence', 'Licence')
    device_ids = fields.Many2many('product.device', 'purchase_order_product_device_rel', 'order_id', 'device_id', 'Devices', readonly=True)
    type = fields.Selection([('state_of_needs', 'State of needs'), ('quotation', 'Request for quotation')], 'Type', default='quotation')
    cgm_state = fields.Selection([('draft', 'Draft'), ('sent', 'Sent'),  ('po_generated', 'PO Generated'), ('done', 'Confirmed'),
                                  ('cancel', 'Cancel')], default='draft')
    cgm_name = fields.Char('Name', required=False)

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

    def print_state_need(self):
        self.ensure_one()
        self.write({'cgm_state': 'sent'})
        return self.env.ref('cgm_purchase.report_state_neet').report_action(self)

    def button_generate_purchase_order(self):
        """
        Generate PO from state need
        :return:
        """
        self.ensure_one()
        self.button_confirm()
        self.write({'cgm_state': 'po_generated'})
        return True

    def action_view_purchase_order(self):
        self.ensure_one()
        action = self.env.ref('cgm_purchase.purchase_form_action', raise_if_not_found=False)
        if not action:
            return False
        action = action.read()[0]
        action['res_id'] = self.id
        action['context'] = {'come_from_state_need_action': False}
        return action

    def button_validate(self):
        self.ensure_one()
        self.write({'cgm_state': 'done'})
        return True

    def button_cancel(self):
        result = super(PurchaseOrder, self).button_cancel()
        self.write({'cgm_state': 'cancel'})
        return result

    def button_draft(self):
        result = super(PurchaseOrder, self).button_draft()
        self.write({'cgm_state': 'draft'})
        return result

    def button_send_by_mail(self):
        self.ensure_one()
        self.write({'cgm_state': 'sent'})
        return True

    def button_view_purchase_order(self):
        self.ensure_one()
        return self.action_view_purchase_order()

    def name_get(self):
        names = []
        if not self._context.get('come_from_state_need_action'):
            return super(PurchaseOrder, self).name_get()
        for record in self:
            names.append((record.id, record.cgm_name))
        return names
