from odoo import models, fields, api, _
from odoo.exceptions import UserError


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    barcode = fields.Char('EAN Code', compute='_compute_barcode', store=True)

    @api.depends('move_ids_without_package', 'move_ids_without_package.barcode')
    def _compute_barcode(self):
        for stock in self:
            stock.barcode = stock.move_ids_without_package.mapped('barcode')