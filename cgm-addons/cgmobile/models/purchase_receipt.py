# -*- coding: utf-8 -*-
from odoo import models, fields, _


class PurchaseReceipt(models.Model):
    _name = 'purchase.receipt'
    _description = 'Purchase Receipt'

    purchase_id = fields.Many2one('purchase.order', string='Purchase Order', required=True, ondelete='cascade')
    receipt_date = fields.Datetime(string='Receipt Date', default=fields.Datetime.now, required=True)
    reference = fields.Char(string='Reference', required=False)
    receipt_lines = fields.One2many('purchase.receipt.line', 'purchase_receipt_id', string='Receipt Lines')

class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    purchase_receipt_ids = fields.One2many('purchase.receipt', 'purchase_id', string='Purchase Receipts')

class PurchaseReceiptLines(models.Model):
    _name = 'purchase.receipt.line'
    _description = 'Purchase Receipt Line'

    purchase_receipt_id = fields.Many2one('purchase.receipt', string='Receipt', required=True, ondelete='cascade')
    product_id = fields.Many2one('product.product', string='Product', required=False)
    product_sku = fields.Char(string='SKU', required=True)
    product_qty = fields.Float(string='Quantity', required=True)
