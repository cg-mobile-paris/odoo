# -*- coding: UTF-8 -*-

import io
import base64

from dateutil.relativedelta import relativedelta

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from odoo.tools.misc import xlsxwriter


class SaleOrderTemplate(models.Model):
    _inherit = 'sale.order.template'

    licence_id = fields.Many2one('product.licence', 'Licence', index=True)
    type = fields.Selection([('sale_order_template', 'Sale Order Template'), ('stock_state', 'Stock State')], 'Type',
                            default='sale_order_template')
    partner_ids = fields.Many2many('res.partner', 'sale_order_template_res_partner_rel', 'template_id', 'partner_id', 'Customers',
                                   domain=[('parent_id', '=', False)])
    state = fields.Selection([('draft', 'Draft'), ('checked', 'Checked'), ('generated', 'Generated'), ('sent', 'Sent'), ('done', 'Done'),
                              ('cancel', 'Cancel')], 'State', default='draft')
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
                template_lines.append((0, 0, {'product_id': product.id, 'product_uom_qty': 0.0}))

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
        partners = self.pricelist_id.partner_ids.filtered(lambda p: not p.parent_id)
        self.update({'partner_ids': [(6, 0, partners.ids)]})

    def button_check_stock(self):
        """
        Check the available quantity of all products
        :return:
        """
        self.ensure_one()
        for line in self.sale_order_template_line_ids.filtered(lambda l: not l.display_type):
            to_date = self.date + relativedelta(days=self.number_of_days)
            quantity = line.product_id.with_context(from_date=self.date, to_date=to_date).virtual_available
            if not quantity:
                line.unlink()
                continue
            line.write({'product_uom_qty': quantity})
        self.write({'state': 'checked'})
        return True

    def button_generate_quotation(self):
        """
        Generate quotation for all partners
        :return:
        """
        self.ensure_one()
        if not self.partner_ids:
            raise ValidationError(_('No customer is associated with the selected price list. \n'
                                    'Please check the configuration of customers or select another price list.'))

        order_obj = self.env['sale.order']
        for partner in self.partner_ids:
            order = order_obj.create({'partner_id': partner.id, 'sale_order_template_id': self.id, 'pricelist_id': self.pricelist_id.id})
            order.onchange_sale_order_template_id()

        self.write({'state': 'generated'})
        return True

    def button_send_quotation(self):
        """
        Send quotation to partners
        :return:
        """
        self.ensure_one()
        orders = self.sale_order_ids.filtered(lambda so: so.state != 'cancel')
        if not orders:
            raise ValidationError(_('There is no quotation generated for this stock state.'))
        for order in orders:
            mail_compose = order._prepare_mail_compose()
            mail_compose._action_send_mail()
        self.write({'state': 'sent'})
        return True

    def button_print_quotation(self):
        """
        Print all quotations
        :return:
        """
        self.ensure_one()
        orders = self.sale_order_ids.filtered(lambda so: so.state != 'cancel')
        if not orders:
            raise ValidationError(_('There is no quotation generated for this stock state.'))
        action_report = self.env.ref('cgm_sale.action_report_stock_state', raise_if_not_found=False)
        if not action_report:
            raise ValidationError(_('There is no report'))
        return action_report.report_action(orders.ids, config=False)

    def button_cancel(self):
        """
        Cancel this stock need
        :return:
        """
        self.ensure_one()
        orders = self.sale_order_ids.filtered(lambda so: so.state != 'cancel')
        if not orders:
            raise ValidationError(_('There is no quotation generated for this stock state.'))
        for order in orders:
            order.action_cancel()
        self.write({'state': 'cancel'})
        return True

    def button_confirm(self):
        """
        Confirm this stock need and all quotations
        :return:
        """
        self.ensure_one()
        self.write({'state': 'done'})
        return True

    def button_draft(self):
        """
        Reset to draft
        :return:
        """
        self.ensure_one()
        self.write({'state': 'draft'})
        return True
