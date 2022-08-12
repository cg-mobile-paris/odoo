# -*- coding: utf-8 -*-

from odoo import fields, models


class SaleOrderTemplateLine(models.Model):
    _inherit = 'sale.order.template.line'

    state = fields.Selection(related='sale_order_template_id.state', store=True)
