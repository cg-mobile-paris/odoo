# -*- coding: UTF-8 -*-

from odoo import models, fields


class ResPartner(models.Model):
    _inherit = 'res.partner'

    property_payment_term_id = fields.Many2one(tracking=True)
    property_account_receivable_id = fields.Many2one(tracking=True)
    property_account_payable_id = fields.Many2one(tracking=True)
