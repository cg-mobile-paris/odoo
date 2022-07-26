# -*- coding: UTF-8 -*-

from odoo import models, fields


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def quotation_create(self):
        self.ensure_one()
        template_id = self._find_mail_template()
        lang = self.env.context.get('lang')
        template = self.env['mail.template'].browse(template_id)
        sample_sales_order = self.company_id._get_sample_sales_order()
        if template.lang:
            lang = template._render_lang(self.ids)[self.id]
        ctx = {
            'mark_so_as_sent': True,
            'custom_layout': "mail.mail_notification_paynow",
            'proforma': self.env.context.get('proforma', False),
            'force_email': True,
            'model_description': self.with_context(lang=lang).type_name,
            'default_use_template': bool(template_id),
        }
        values = {
            'model': 'sale.order',
            'res_id': self.ids[0],
            'composition_mode': 'comment',
            'template_id': template_id
        }
        mail_compose_id = self.env["mail.compose.message"].with_context(**ctx).create(values)
        update_values = mail_compose_id._onchange_template_id(template_id, 'comment', 'sale.order', sample_sales_order.id)['value']
        mail_compose_id.write(update_values)
        return mail_compose_id
