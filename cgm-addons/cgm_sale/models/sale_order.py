# -*- coding: utf-8 -*-

from odoo import models


class SaleOrder(models.Model):
    _inherit = 'sale.order'

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
