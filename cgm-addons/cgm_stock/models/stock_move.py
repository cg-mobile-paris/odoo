from odoo import models, fields, api, _
from odoo.exceptions import UserError


class StockMove(models.Model):
    _inherit = 'stock.move'

    barcode = fields.Char('EAN Code', related='product_id.barcode', store=True)
