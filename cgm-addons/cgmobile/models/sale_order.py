# -*- coding: utf-8 -*-
from odoo import _, api, fields, models

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    # Field for delivery state
    delivery_status = fields.Selection([('draft', 'Draft'), ('in_progress', 'In Progress'), ('done', 'Done'), ('cancel','Cancelled')], string='Delivery Status', default='draft', compute='_compute_delivery_status', store=True, compute_sudo=True)

    reservation = fields.Boolean(string='Reservation', default=False, readonly=True)

    # override fiscal position field to add compute method based on sales team
    fiscal_position_id = fields.Many2one('account.fiscal.position', string='Fiscal Position', compute='_compute_fiscal_position', store=True, readonly=False, compute_sudo=True)

    @api.depends('team_id')
    def _compute_fiscal_position(self):
        for order in self:
            if order.team_id.fiscal_position_id:
                order.fiscal_position_id = order.team_id.fiscal_position_id

    @api.depends('order_line.qty_to_deliver', 'state')
    def _compute_delivery_status(self):
        for order in self:
            if order.state in ['draft', 'sent']:
                order.delivery_status = 'draft'
            elif order.state in  ['cancel']:
                order.delivery_status = 'cancel'
            else:
                if any(line.qty_to_deliver > 0 for line in order.order_line.filtered(lambda l: l.product_id.type in ['product', 'consu'])):
                    order.delivery_status = 'in_progress'
                else:
                    order.delivery_status = 'done'

    def action_reserve(self):
        self.write({'reservation': True})
    
    def action_unreserve(self):
        self.write({'reservation': False})


    def action_reserve_and_confirm(self):
        self.action_reserve()
        self.action_confirm()

    # Override to prevent lock when reservation is active
    def action_done(self):
        return super(SaleOrder, self.filtered(lambda o: o.reservation == False)).action_done()

    def action_cancel(self):
        self.action_unreserve()
        return super(SaleOrder, self).action_cancel()
    

    # override create method to add default values for fiscal position
    def create(self, vals):
        if isinstance(vals, list):
            values = vals
        else:
            values = [vals]
        
        for val in values:
            if val.get('team_id'):
                team = self.env['crm.team'].browse(val['team_id'])
                if team.fiscal_position_id:
                    val['fiscal_position_id'] = team.fiscal_position_id.id

        return super(SaleOrder, self).create(vals)

