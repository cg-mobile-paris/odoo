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
    pricelist_id = fields.Many2one('product.pricelist', string='Price List', required=False)
    date = fields.Date('Date', required=False)

    @api.model
    def default_get(self, fields_list):
        """
        Override native method to set date by default
        :param fields_list:
        :return:
        """
        result = super(SaleOrderTemplate, self).default_get(fields_list)
        if not result.get('date') and 'date' not in result:
            result.update({'date': fields.Date.today()})
        return result

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

    @api.onchange('licence_id')
    def _onchange_licence_id(self):
        """
        Load products according to the selected licence
        :return: None
        """
        if not self.licence_id:
            return {}
        self.update({'sale_order_template_line_ids': [(6, 0, [])]})
        products = self.licence_id.product_ids
        if not products:
            return {}

        device_summary = {}
        for product in products:
            device_summary.setdefault(product.device_id, []).append(product)

        template_lines = []
        for device, products in device_summary.items():
            template_lines.append((0, 0, {'display_type': 'line_section', 'name': device.name or _('Indefinite')}))
            for product in products:
                template_lines.append((0, 0, {'product_id': product.id, 'product_uom_qty': 1.0}))

        self.update({'sale_order_template_line_ids': template_lines})

        for line in self.sale_order_template_line_ids:
            line._onchange_product_id()

        return {}

    @api.onchange('pricelist_id')
    def _onchange_pricelist_id(self):
        """
        Load partners of selected pricelist
        :return:
        """
        if not self.pricelist_id:
            return {}
        self.update({'partner_ids': [(6, 0, self.pricelist_id.partner_ids.ids)]})
