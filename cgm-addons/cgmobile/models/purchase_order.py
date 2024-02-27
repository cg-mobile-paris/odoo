
# -*- coding: utf-8 -*-
from odoo import _, api, fields, models
import logging
_logger = logging.getLogger(__name__)


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    # Field for delivery state
    delivery_status = fields.Selection([('draft', 'Draft'), ('in_progress', 'In Progress'), ('done', 'Done'), ('cancel','Cancelled')], string='Delivery Status', default='draft', compute='_compute_delivery_status', store=True, compute_sudo=True)

    @api.depends('order_line.qty_to_receive', 'state')
    def _compute_delivery_status(self):
        for order in self:
            if order.state in ['draft', 'sent']:
                order.delivery_status = 'draft'
            elif order.state in  ['cancel']:
                order.delivery_status = 'cancel'
            else:
                if any(line.qty_to_receive > 0 for line in order.order_line.filtered(lambda l: l.product_id.type in ['product', 'consu'])):
                    order.delivery_status = 'in_progress'
                else:
                    order.delivery_status = 'done'

    def set_received(self, receipt_reference, receipt_date, quantities):
        """
        Set the quantities received for the given purchase product SKU
        :param receipt_date: Date of receipt
        :param quantities: list of tuple (SKU, quantity)
        """
        _logger.info('set_received: {"receipt_reference": "%s", "receipt_date": "%s", "": %s}' % (receipt_reference, receipt_date, str(quantities)))

        # check if the purchase receipt is already created
        receipt_date = receipt_date if receipt_date else fields.Datetime.now()
        receipt_reference = receipt_reference.strip() if receipt_reference else str(receipt_date)
        purchase_receipt_id = self.env['purchase.receipt'].sudo().search([('purchase_id', '=', self.id), ('reference', '=', receipt_reference)])
        if purchase_receipt_id:
            # push notification that the purchase receipt already exists
            _logger.info('set_received: Purchase receipt %s already exists: %s' % (receipt_reference, purchase_receipt_id.id))
            self.message_post(body=_("The purchase receipt %s already exists.") % receipt_reference)
            return purchase_receipt_id.id
        else:
            # create the receipt
            purchase_receipt_id = self.env['purchase.receipt'].create({
                'purchase_id': self.id,
                'reference': receipt_reference,
                'receipt_date': receipt_date,
            })
            # push nofication that the purchase receipt has been created
            _logger.info('set_received: Purchase receipt %s created: %s' % (receipt_reference, purchase_receipt_id.id))
            self.message_post(body=_("The purchase receipt %s has been created.") % receipt_reference)

            for quantity in quantities:
                sku = quantity.get('product_sku')
                qty = quantity.get('quantity', 0)
                # create receipt line
                self.env['purchase.receipt.line'].create({
                    'purchase_receipt_id': purchase_receipt_id.id,
                    'product_id': self.env['product.product'].search([('default_code', '=', sku)]).id,
                    'product_qty': qty,
                    'product_sku': sku,
                })

                # if user has the group to apply the purhcase receipt automatically
                if self.env.user.has_group('cgmobile.group_auto_apply_purchase_receipt'):
                    # search product line
                    lines = self.sudo().order_line.filtered(lambda l: l.product_id.default_code == sku)

                    if not lines:
                        # push notification that the product line does not exist
                        _logger.info('set_received: The product line with SKU %s does not exist (quantity: %s).' % (sku, qty))
                        self.message_post(body=_("Purchase Receipt: The product line with SKU %s does not exist (quantity: %s).") % (sku, qty))
                    else:
                        # set the quantity received on pickings
                        lines.move_ids.move_line_ids.filtered(lambda ml: ml.product_id.default_code == sku)[0].qty_done += qty

                        # complete picking are marked as done
                        for picking in lines.move_ids.picking_id:
                            if picking.state == 'assigned':
                                # check if all move_ids are done
                                if all(move.quantity_done == move.product_uom_qty for move in picking.move_lines):
                                    _logger.info('set_received: Picking %s is done.' % picking.name)
                                    picking._action_done()
                                    
            if not self.env.user.has_group('cgmobile.group_auto_apply_purchase_receipt'):
                # push notification that the user does not have the group to apply the purchase receipt automatically
                _logger.info('set_received: The user does not have the group to apply the purchase receipt automatically.')
                self.message_post(body=_("Purchase Receipt: The user does not have the group to apply the purchase receipt automatically."))

        return purchase_receipt_id.id
