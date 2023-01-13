# -*- coding : UTF-8 -*-


from odoo import fields, models, api


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    partner_ref = fields.Char(related="partner_id.ref")
