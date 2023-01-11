# -*- coding: UTF-8 -*-
from odoo import fields, models, api


class ResBank(models.Model):
    _inherit = 'res.bank'

    note = fields.Text(translate=True)
