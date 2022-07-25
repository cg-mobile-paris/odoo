# -*- coding: UTF-8 -*-

from odoo import models, fields, api, _

TYPE = [('template', 'quotation template'), ('state', 'Stock state')]
STATE = [('draft', 'Draft'), ('progress', 'In progress'), ('done', 'Done')]


class SaleOrderTemplate(models.Model):
    _inherit = 'sale.order.template'

    licence_id = fields.Many2one('product.licence', 'Licence')
    type = fields.Selection(TYPE, 'Type', default='template')
    partner_ids = fields.Many2many('res.partner', 'customer_n_template', 'customer', 'template', 'Customers')
    state = fields.Selection(STATE, 'Status', default='draft')
    order_ids = fields.One2many('sale.order', 'sale_order_template_id', 'Quotations / Orders')
    order_ids_count = fields.Integer('Quotations / Orders Count', compute='_compute_order_ids')

    @api.depends('order_ids')
    def _compute_order_ids(self):
        for rec in self:
            rec.order_ids_count = len(rec.order_ids)

    def action_view_orders_n_quotations(self):
        return {
            'type': 'ir.actions.act_window',
            'name': _('Quotations / Orders'),
            'res_model': 'sale.order',
            'view_type': 'list',
            'view_mode': 'list',
            'views': [[self.env.ref('sale.view_order_tree').id, 'list'],
                      [False, 'form']],
            'domain': [('id', 'in', self.order_ids.ids)],
            'context': {'default_sale_order_template_id': self.id}
        }
