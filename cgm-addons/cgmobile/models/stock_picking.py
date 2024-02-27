# -*- coding: utf-8 -*-
from odoo import models, fields, api
from datetime import datetime
from odoo.exceptions import UserError


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    state = fields.Selection(selection_add=[('reservation', 'Reservation')])

    @api.depends('sale_id.reservation')
    def _compute_state(self):
        super(StockPicking, self)._compute_state()
        for picking_id in self:
            if picking_id.state == 'assigned' and picking_id.sale_id.reservation:
                picking_id.state = 'reservation'

    def button_validate(self):
        ret = super(StockPicking, self).button_validate()

        # if no return, all should be good, so let's try to get the shipping label
        if len(self) == 1 and ret is True and self.carrier_tracking_ref:
            return self.action_download_last_attachment()

        return ret

    def get_last_attachment(self):
        return self.env['ir.attachment'].search([
            ('res_model', '=', 'stock.picking'),
            ('res_id', '=', self.id),
            ('mimetype', '=', 'application/pdf')
        ], order='id desc', limit=1)

    def action_download_last_attachment(self):
        attachment = self.get_last_attachment()
        if attachment:
            xml_id = "cgmobile.action_report_shipping_label"
            res = self.env.ref(xml_id).report_action(self, data={'attachment_ids': attachment.ids})
            res['report_name'] += '/' + str(self.id)
            res['id'] = self.env.ref(xml_id).id
            res['close_on_report_download'] = True
            return res
        else:
            return False

    # for the bug fix [CG-32] : FBM orders set as shipped into Amazon without being shipped
    def _sync_pickings(self, account_ids=()):
        """
        Override to avoid to sync non delivery pickings
        """
        customer_location_ids = self.env['stock.location'].search([('usage', '=', 'customer')])
        pick_type_out_ids = self.env['stock.picking.type'].search([('code', '=', 'outgoing')])
        not_to_sync_picking_ids = self.search([('amazon_sync_pending', '=', True), '|', ('picking_type_id', 'not in', pick_type_out_ids.ids), ('location_dest_id', 'not in', customer_location_ids.ids)])
        not_to_sync_picking_ids.amazon_sync_pending = False
        super(StockPicking, self)._sync_pickings(account_ids)

    def _get_carrier_details(self):
        """ Return the shipper name and tracking number if any. """
        self.ensure_one()
        carrier = self.shippo_delivery_provider or (self.carrier_id and self.carrier_id.name)
        return carrier, self.carrier_tracking_ref

    # for the bug fix : An error is raise even with intercompany warehouse
    def _check_carrier_details_compliance(self):
        out_pickings = self.filtered(lambda p: p.location_dest_id.usage == 'customer')
        return super(StockPicking, out_pickings)._check_carrier_details_compliance()

  