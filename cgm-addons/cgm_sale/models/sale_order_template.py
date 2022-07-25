# -*- coding: UTF-8 -*-

from odoo import models, fields, api, _


class SaleOrderTemplate(models.Model):
    _inherit = 'sale.order.template'

    licence_id = fields.Many2one('product.licence', 'Licence', index=True)
    type = fields.Selection([('sale_order_template', 'Sale Order Template'), ('stock_state', 'Stock State')], 'Type',
                            default='sale_order_template')
    partner_ids = fields.Many2many('res.partner', 'sale_order_template_res_partner_rel', 'template_id', 'partner_id', 'Customers')
    state = fields.Selection([('draft', 'Draft'), ('progress', 'In progress'), ('done', 'Done')], 'State', default='draft')
    sale_order_ids = fields.One2many('sale.order', 'sale_order_template_id', 'Quotations / Orders')
    sale_order_count = fields.Integer('Sale Order Count', compute='_compute_sale_order_count', store=True)

    @api.depends('sale_order_ids')
    def _compute_sale_order_count(self):
        for record in self:
            record.sale_order_count = len(record.sale_order_ids)

    def action_view_sale_orders(self):
        self.ensure_one()
        action = self.env.ref('sale.action_quotations_with_onboarding', raise_if_not_found=False)
        if not action:
            return False
        action = action.read()[0]
        action.update({
            'domain': [('id', 'in', self.sale_order_ids.ids)],
            'context': {'default_sale_order_template_id': self.id, 'search_default_my_quotation': 0}
        })
        return action
