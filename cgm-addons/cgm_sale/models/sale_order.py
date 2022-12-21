# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    company_currency_id = fields.Many2one('res.currency', 'Company Currency', readonly=True,
                                          default=lambda self: self.env.company.currency_id, copy=False)
    amount_total_in_currency = fields.Monetary('Total', readonly=True, currency_field='company_currency_id', copy=False)
    total_qty = fields.Float('Total Qty', compute='_compute_total_qty', digits='Product Unit of Measure', store=True)
    bank_id = fields.Many2one('res.partner.bank', string='Bank account')
    bank_partner_id = fields.Many2one('res.partner', string='Bank partner', related='company_id.partner_id')

    @api.depends('order_line', 'order_line.product_uom_qty')
    def _compute_total_qty(self):
        for order in self:
            order.total_qty = sum(order.order_line.mapped('product_uom_qty'))

    def _prepare_mail_compose(self):
        self.ensure_one()
        template = self.env.ref('cgm_sale.email_template_stock_state', raise_if_not_found=False)
        lang = self.env.context.get('lang')
        if template.lang:
            lang = template._render_lang(self.ids)[self.id]
        ctx = {
            'mark_so_as_sent': True,
            'custom_layout': 'mail.mail_notification_paynow',
            'proforma': self.env.context.get('proforma', False),
            'force_email': True,
            'model_description': self.with_context(lang=lang).type_name,
            'default_use_template': bool(template.id),
        }
        values = {
            'model': 'sale.order',
            'res_id': self.id,
            'composition_mode': 'comment',
            'template_id': template.id
        }
        mail_compose = self.env['mail.compose.message'].with_context(**ctx).create(values)
        update_values = mail_compose._onchange_template_id(template.id, 'comment', 'sale.order', self.id)['value']
        mail_compose.write(update_values)
        return mail_compose

    def compute_amount_total_in_currency(self):
        self.ensure_one()
        try:
            amount = self.sudo().order_amount_total_in_currency()
        except UserError as e:
            self.message_post(body=str(e))
            amount = 0.0
        self.write({'amount_total_in_currency': amount})

    def order_amount_total_in_currency(self):
        """
        return the amount once it is converted to company currency
        raise error can not update currency rates
        """
        self.ensure_one()
        if self.currency_id == self.company_currency_id:
            return self.amount_total
        if not (self.company_id.update_currency_rates()):
            raise UserError(_('Unable to connect to the online exchange rate platform. '
                              'The web service may be temporary down. Please try again in a moment.'))
        return self.company_currency_id._convert(self.amount_total, self.currency_id, self.company_id,
                                                 fields.Date.today())

    def action_confirm(self):
        res = super(SaleOrder, self).action_confirm()
        for order in self:
            order.compute_amount_total_in_currency()
        return res

    def _prepare_invoice(self):
        self.ensure_one()
        res = super(SaleOrder, self)._prepare_invoice()
        res['partner_bank_id'] = self.bank_id.id or self.company_id.partner_id.bank_ids.filtered(
            lambda bank: bank.company_id.id in (self.company_id.id, False))[:1].id
        return res
