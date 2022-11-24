# -*- coding: UTF-8 -*-

from dateutil.relativedelta import relativedelta

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class SaleOrderTemplate(models.Model):
    _name = 'sale.order.template'
    _inherit = ['sale.order.template', 'mail.thread', 'mail.activity.mixin', 'utm.mixin']

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
    warehouse_id = fields.Many2one('stock.warehouse', 'Warehouse', required=False)
    number_of_days = fields.Integer(default=1)
    partner_count = fields.Integer('Partner Count', compute='_compute_partner_count', store=True)

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
        if not result.get('company_id') and 'company_id' not in result:
            result.update({'company_id': self.env.user.company_id.id})
        if not result.get('warehouse_id') and 'warehouse_id' not in result:
            result.update({'warehouse_id': self.env['stock.warehouse'].search([('company_id', '=', self.env.user.company_id.id)],
                                                                              limit=1).id})
        return result

    @api.depends('sale_order_ids')
    def _compute_sale_order_count(self):
        for record in self:
            record.sale_order_count = len(record.sale_order_ids)

    @api.depends('partner_ids')
    def _compute_partner_count(self):
        for record in self:
            record.partner_count = len(record.partner_ids)

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
        warehouse = self.warehouse_id
        for line in self.sale_order_template_line_ids.filtered(lambda l: not l.display_type):
            physical_qty = line.product_id.with_context(warehouse=warehouse.id).qty_available
            outgoing_qty = line.product_id.with_context(warehouse=warehouse.id).outgoing_qty
            available_qty = physical_qty - outgoing_qty
            line.write({'product_uom_qty': available_qty})
        self.write({'state': 'checked'})
        return True

    def button_unlink_lines_with_quantity_lt_0(self):
        """
        Unlink lines with quantity less than 0
        :return:
        """
        self.sale_order_template_line_ids.filtered(lambda line: not line.display_type and line.product_uom_qty <= 0).unlink()
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
        if not self.sale_order_template_line_ids.filtered(lambda line: not line.display_type):
            raise ValidationError(_('There is no line to generate the corresponding stock offers.'))

        order_obj = self.env['sale.order']
        for partner in self.partner_ids:
            order = order_obj.create({'partner_id': partner.id})
            order.onchange_partner_id()
            order.onchange_partner_shipping_id()
            order.write({'pricelist_id': self.pricelist_id.id, 'sale_order_template_id': self.id, 'warehouse_id': self.warehouse_id.id})
            order.onchange_sale_order_template_id()
            break
        self.write({'state': 'generated'})
        return True

    def action_send_by_mail(self):
        """
        Opens a wizard to compose an email, with relevant mail template loaded by default
        :return:
        """
        self.ensure_one()
        template = self.env.ref('cgm_sale.email_template_stock_state', raise_if_not_found=False)
        if not template:
            return False
        ctx = {
            'default_model': 'sale.order.template',
            'default_res_id': self.ids[0],
            'default_use_template': bool(template.id),
            'default_template_id': template.id,
            'default_composition_mode': 'comment',
            'default_partner_ids': self.partner_ids.ids,
            'mark_so_as_sent': True,
            'custom_layout': 'mail.mail_notification_paynow',
            'force_email': True,
        }
        self.write({'state': 'sent'})
        return {
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'mail.compose.message',
            'views': [(False, 'form')],
            'view_id': False,
            'target': 'new',
            'context': ctx,
        }

    def button_download_quotation_xls(self):
        """
        Download stock state xls
        :return:
        """
        self.ensure_one()
        orders = self.sale_order_ids.filtered(lambda so: so.state != 'cancel')
        if not orders:
            raise ValidationError(_('There is no quotation generated for this stock state.'))
        action_report = self.env.ref('cgm_sale.action_report_stock_state_xlsx', raise_if_not_found=False)
        if not action_report:
            raise ValidationError(_('There is no report'))
        return action_report.report_action(orders[0].ids, config=False)

    def button_cancel(self):
        """
        Cancel this stock need
        :return:
        """
        self.ensure_one()
        orders = self.sale_order_ids.filtered(lambda so: so.state != 'cancel')
        # if not orders:
        #     raise ValidationError(_('There is no quotation generated for this stock state.'))
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

    def action_view_customers(self):
        self.ensure_one()
        action = self.env.ref('base.action_partner_form', raise_if_not_found=False).read()[0]
        action['domain'] = [('id', 'in', self.partner_ids.ids)]
        return action
