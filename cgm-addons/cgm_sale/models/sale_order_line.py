# -*- coding: utf-8 -*-

from odoo import models, fields, api


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    image = fields.Image("Thumbnail", related="product_id.image_1920", store=True)
    # parent_delivery_state = fields.Selection("Sale Order Delivery State", related="order_id.delivery_state", store=True)
    remaining_deliverables_dollars = fields.Float("Remaining deliverables dollars", compute='_compute_remaining_deliverables_dollars')
    remaining_deliverables_euros = fields.Float("Remaining deliverables euros", compute='_compute_remaining_deliverables_euros')
    currency_euro_id = fields.Many2one('res.currency', string=" ", default=lambda self: self.env.ref('base.EUR'))
    currency_symbol_euros = fields.Char(string=" ", compute='_get_currency_symbol_euros')
    currency_dollar_id = fields.Many2one('res.currency', string=" ", default=lambda self: self.env.ref('base.USD'))
    currency_symbol_dollars = fields.Char(string=" ", compute='_get_currency_symbol_dollars')
    qty_to_deliver = fields.Float(compute='_compute_qty_to_deliver', store=True, digits='Product Unit of Measure')
    barcode = fields.Char('EAN Code', related='product_id.barcode', store=True)

    def _get_filtered_lines(self):
        return self.filtered(lambda line: line.qty_to_deliver > 0)

    @api.depends('currency_dollar_id')
    def _get_currency_symbol_dollars(self):
        for rec in self:
            rec.currency_symbol_dollars = rec.currency_dollar_id.symbol

    @api.depends('currency_euro_id')
    def _get_currency_symbol_euros(self):
        for rec in self:
            rec.currency_symbol_euros = rec.currency_euro_id.symbol

    @api.depends('qty_to_deliver', 'price_unit', 'discount')
    def _compute_remaining_deliverables_dollars(self):
        for line in self:
            price_unit = line.price_unit * (1 - (line.discount or 0.0) / 100.0)
            remaining_deliverables = line.qty_to_deliver * price_unit
            if line.order_id.currency_id.name == 'EUR':
                exchange_rate = self._get_exchange_rate('EUR', 'USD')
                line.remaining_deliverables_dollars = remaining_deliverables * exchange_rate
            else:
                line.remaining_deliverables_dollars = remaining_deliverables

    @api.depends('remaining_deliverables_dollars')
    def _compute_remaining_deliverables_euros(self):
        exchange_rate = self._get_exchange_rate('USD', 'EUR')
        for line in self:
            line.remaining_deliverables_euros = line.remaining_deliverables_dollars * exchange_rate

    def _get_exchange_rate(self, source_currency_name, target_currency_name):
        source_currency = self.env['res.currency'].search([('name', '=', source_currency_name)], limit=1)
        target_currency = self.env['res.currency'].search([('name', '=', target_currency_name)], limit=1)
        return source_currency._get_conversion_rate(source_currency, target_currency, self.env.company,
                                                    fields.Date.today())
